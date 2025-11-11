"""Feature matrix and profile helpers."""
from __future__ import annotations

import copy
from typing import Any, Mapping

import frappe
from frappe.utils import now

from .subscription_context import (
	ModuleActivationState,
	SubscriptionContext,
	SubscriptionPlanState,
	get_subscription_context,
	resolve_plan_for_company,
)
from blkshp_os.permissions import roles as role_service
from blkshp_os.permissions import service as permission_service


FEATURE_MATRIX_CACHE_KEY = "blkshp_os:core_platform:feature_matrix"
_CACHE_PLAN_FALLBACK = "__no_plan__"
_ADMIN_MESSAGE = "Feature toggles are administered solely by BLKSHP Operations."


def _normalize_plan_key(plan_code: str | None) -> str:
	"""Return the normalized cache key for a plan code."""
	if not plan_code:
		return _CACHE_PLAN_FALLBACK
	return (plan_code or "").strip().lower() or _CACHE_PLAN_FALLBACK


def _load_cache() -> dict[str, dict[str, Any]]:
	"""Load the cached feature matrix map from frappe.cache."""
	cache = frappe.cache()
	cached = cache.get_value(FEATURE_MATRIX_CACHE_KEY)
	return cached or {}


def _store_cache(cache_map: Mapping[str, dict[str, Any]]) -> None:
	"""Persist the provided cache map."""
	frappe.cache().set_value(FEATURE_MATRIX_CACHE_KEY, dict(cache_map))


def clear_feature_matrix_cache() -> None:
	"""Clear the cached feature matrix payloads."""
	frappe.cache().delete_value(FEATURE_MATRIX_CACHE_KEY)


def _serialize_plan(plan: SubscriptionPlanState | None) -> dict[str, Any] | None:
	"""Return a serializable representation of the subscription plan."""
	if not plan:
		return None
	return {
		"name": plan.name,
		"code": plan.plan_code,
		"label": plan.plan_name,
		"is_active": bool(plan.is_active),
		"is_default": bool(plan.is_default),
		"billing_frequency": plan.billing_frequency,
		"billing_currency": plan.billing_currency,
		"base_price": plan.base_price,
		"default_feature_overrides": dict(plan.default_feature_overrides),
	}


def _serialize_module(module: ModuleActivationState) -> dict[str, Any]:
	"""Return a serializable representation of the module activation state."""
	return {
		"key": module.key,
		"label": module.label,
		"is_enabled": bool(module.is_enabled),
		"is_required": bool(module.is_required),
		"depends_on": list(module.depends_on),
		"feature_overrides": dict(module.feature_overrides),
	}


def _serialize_registry(context: SubscriptionContext) -> dict[str, dict[str, Any]]:
	"""Return the flattened feature registry metadata."""
	return {
		key: {
			"key": metadata.key,
			"name": metadata.name,
			"category": metadata.category,
			"default_enabled": bool(metadata.default_enabled),
			"description": metadata.description,
		}
		for key, metadata in context.registry.items()
	}


def _build_plan_matrix(
	context: SubscriptionContext,
	plan_code: str | None,
) -> dict[str, Any]:
	"""Construct the plan-level feature matrix payload."""
	modules = [_serialize_module(module) for module in context.modules.values()]
	modules.sort(key=lambda entry: entry["key"])

	enabled_modules = [module["key"] for module in modules if module["is_enabled"]]

	return {
		"plan_code": context.plan.plan_code if context.plan else plan_code,
		"plan": _serialize_plan(context.plan),
		"modules": modules,
		"enabled_modules": enabled_modules,
		"feature_states": dict(context.feature_states),
		"registry": _serialize_registry(context),
		"administration": {
			"managed_by": "BLKSHP Operations",
			"message": _ADMIN_MESSAGE,
		},
	}


def get_feature_matrix(
	*, plan_code: str | None = None, company: str | None = None, refresh: bool = False
) -> dict[str, Any]:
	"""Return the plan-level feature matrix for the supplied plan/company.

	When refresh is False the serialized payload is cached in frappe.cache()
	using a normalized plan key. Invalidation is handled via DocType hooks
	by calling :func:`clear_subscription_context_cache` and
	:func:`clear_feature_matrix_cache`.
	"""
	resolved_plan = plan_code or resolve_plan_for_company(company)
	cache_key = _normalize_plan_key(resolved_plan)
	cache_map = {} if refresh else _load_cache()

	if not refresh and cache_key in cache_map:
		payload = copy.deepcopy(cache_map[cache_key])
	else:
		context = get_subscription_context(
			company=company, plan_code=resolved_plan, use_cache=not refresh
		)
		payload = _build_plan_matrix(context, resolved_plan)
		if not refresh:
			cache_map[cache_key] = copy.deepcopy(payload)
			_store_cache(cache_map)

	payload["generated_at"] = now()
	return payload


def _evaluate_module_access(user: str, modules: list[dict[str, Any]], refresh: bool) -> dict[str, bool]:
	"""Return a mapping of module key to access flag for the user."""
	access_map: dict[str, bool] = {}
	for module in modules:
		key = module["key"]
		access_map[key] = permission_service.user_has_module_access(user, key, refresh=refresh)
	return access_map


def _evaluate_feature_access(
	user: str,
	registry: Mapping[str, Any],
	refresh: bool,
) -> dict[str, bool]:
	"""Return a mapping of feature key to access flag for the user."""
	access_map: dict[str, bool] = {}
	for feature_key in registry.keys():
		access_map[feature_key] = permission_service.user_has_feature(
			user, feature_key, refresh=refresh
		)
	return access_map


def get_feature_matrix_for_user(
	user: str | None = None,
	*,
	company: str | None = None,
	refresh: bool = False,
) -> dict[str, Any]:
	"""Return the feature matrix augmented with user-specific access flags."""
	if not user:
		user = frappe.session.user

	user_company = company or permission_service.get_user_company(user)
	matrix = get_feature_matrix(plan_code=None, company=user_company, refresh=refresh)

	result = copy.deepcopy(matrix)
	module_access = _evaluate_module_access(user, result["modules"], refresh)
	feature_access = _evaluate_feature_access(user, result["registry"], refresh)

	for module in result["modules"]:
		module["user_has_access"] = module_access[module["key"]]

	result["user_accessible_modules"] = [
		key for key, has_access in module_access.items() if has_access
	]
	result["user_feature_access"] = feature_access
	result["user"] = {
		"id": user,
		"company": user_company,
		"roles": frappe.get_roles(user),
	}
	return result


def _summarize_permissions(user: str) -> dict[str, Any]:
	"""Return a permissions summary for the provided user."""
	by_category = role_service.get_permissions_by_category(user)
	total_permissions = sum(len(entries) for entries in by_category.values())
	return {
		"roles": frappe.get_roles(user),
		"by_category": by_category,
		"total": total_permissions,
	}


def get_user_profile(
	user: str | None = None,
	*,
	refresh: bool = False,
) -> dict[str, Any]:
	"""Return a read-only profile summary for the tenant user."""
	if not user:
		user = frappe.session.user

	user_doc = frappe.get_cached_doc("User", user)
	matrix = get_feature_matrix_for_user(user=user, refresh=refresh)
	departments = permission_service.get_user_department_permissions(user)

	permissions = _summarize_permissions(user)
	module_summary = [
		{
			"key": module["key"],
			"label": module["label"],
			"is_enabled": module["is_enabled"],
			"user_has_access": module["user_has_access"],
		}
		for module in matrix["modules"]
	]

	return {
		"user": {
			"id": user_doc.name,
			"full_name": user_doc.full_name,
			"email": user_doc.email,
			"enabled": bool(user_doc.enabled),
			"roles": permissions["roles"],
		},
		"company": matrix["user"]["company"],
		"departments": departments,
		"permissions": {
			"by_category": permissions["by_category"],
			"total": permissions["total"],
		},
		"subscription": {
			"plan_code": matrix["plan_code"],
			"plan": matrix["plan"],
			"modules": module_summary,
			"user_feature_access": matrix["user_feature_access"],
			"administration": matrix["administration"],
		},
		"generated_at": matrix["generated_at"],
	}


