"""Subscription and feature matrix helpers."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Mapping, MutableMapping

import frappe

FeatureValue = Any


@dataclass(frozen=True)
class FeatureToggleMetadata:
	"""Metadata describing a feature toggle."""

	key: str
	name: str
	category: str | None
	default_enabled: bool
	description: str | None = None


@dataclass(frozen=True)
class ModuleActivationState:
	"""Represents a module's activation state within a subscription plan."""

	key: str
	label: str
	is_enabled: bool
	is_required: bool
	depends_on: tuple[str, ...] = field(default_factory=tuple)
	feature_overrides: Mapping[str, FeatureValue] = field(default_factory=dict)


@dataclass(frozen=True)
class SubscriptionPlanState:
	"""Key metadata for a subscription plan."""

	name: str
	plan_code: str
	plan_name: str
	is_active: bool
	is_default: bool
	default_feature_overrides: Mapping[str, FeatureValue] = field(default_factory=dict)
	billing_frequency: str | None = None
	billing_currency: str | None = None
	base_price: float | None = None


@dataclass(frozen=True)
class SubscriptionContext:
	"""Aggregated view of plan, modules, and effective feature toggles."""

	plan: SubscriptionPlanState | None
	modules: Mapping[str, ModuleActivationState]
	feature_states: Mapping[str, FeatureValue]
	registry: Mapping[str, FeatureToggleMetadata]


_CONTEXT_CACHE: MutableMapping[str, SubscriptionContext] = {}


def clear_subscription_context_cache() -> None:
	"""Clear the in-process cache of subscription contexts."""
	_CONTEXT_CACHE.clear()


def resolve_plan_for_company(company: str | None) -> str | None:
	"""Return the plan code assigned to the provided company (or the default plan)."""
	if company:
		branding_plan = frappe.db.get_value("Tenant Branding", {"company": company}, "plan")
		if branding_plan:
			return branding_plan

	default_plan = frappe.db.get_value(
		"Subscription Plan",
		{"is_default": 1, "is_active": 1},
		"name",
		order_by="modified desc",
	)
	return default_plan


def get_subscription_context(
	*, company: str | None = None, plan_code: str | None = None, use_cache: bool = True
) -> SubscriptionContext:
	"""Return the subscription context for the supplied plan/company."""

	if not plan_code:
		plan_code = resolve_plan_for_company(company)

	cache_key = plan_code or "__no_plan__"
	if use_cache and cache_key in _CONTEXT_CACHE:
		return _CONTEXT_CACHE[cache_key]

	context = _build_subscription_context(plan_code)
	if use_cache:
		_CONTEXT_CACHE[cache_key] = context
	return context


def _build_subscription_context(plan_code: str | None) -> SubscriptionContext:
	registry = _load_feature_registry()
	feature_states: dict[str, FeatureValue] = {
		key: metadata.default_enabled for key, metadata in registry.items()
	}

	modules: dict[str, ModuleActivationState] = {}
	plan_state: SubscriptionPlanState | None = None

	if plan_code:
		plan_state = _load_plan_state(plan_code)
		if plan_state:
			_apply_feature_overrides(feature_states, plan_state.default_feature_overrides)
			modules = _load_module_states(plan_state)
			for module in modules.values():
				if module.is_enabled:
					_apply_feature_overrides(feature_states, module.feature_overrides)

	return SubscriptionContext(
		plan=plan_state,
		modules=modules,
		feature_states=feature_states,
		registry=registry,
	)


def _load_feature_registry() -> dict[str, FeatureToggleMetadata]:
	rows = frappe.get_all(
		"Feature Toggle",
		fields=["feature_key", "feature_name", "category", "default_enabled", "description"],
	)
	registry: dict[str, FeatureToggleMetadata] = {}
	for row in rows:
		key = (row.feature_key or "").strip().lower()
		if not key:
			continue
		registry[key] = FeatureToggleMetadata(
			key=key,
			name=row.feature_name or key,
			category=row.category,
			default_enabled=bool(row.default_enabled),
			description=row.description,
		)
	return registry


def _load_plan_state(plan_code: str) -> SubscriptionPlanState | None:
	if not frappe.db.exists("Subscription Plan", plan_code):
		return None

	row = frappe.db.get_value(
		"Subscription Plan",
		plan_code,
		[
			"name",
			"plan_code",
			"plan_name",
			"is_active",
			"is_default",
			"default_feature_overrides",
			"billing_frequency",
			"billing_currency",
			"base_price",
		],
		as_dict=True,
	)
	if not row:
		return None

	return SubscriptionPlanState(
		name=row.name,
		plan_code=row.plan_code,
		plan_name=row.plan_name,
		is_active=bool(row.is_active),
		is_default=bool(row.is_default),
		default_feature_overrides=_safe_json_load(row.default_feature_overrides),
		billing_frequency=row.billing_frequency,
		billing_currency=row.billing_currency,
		base_price=float(row.base_price) if row.base_price is not None else None,
	)


def _load_module_states(plan: SubscriptionPlanState) -> dict[str, ModuleActivationState]:
	rows = frappe.get_all(
		"Module Activation",
		filters={"plan": plan.name},
		fields=[
			"module_key",
			"module_label",
			"is_enabled",
			"is_required",
			"depends_on",
			"feature_overrides",
		],
		order_by="module_key asc",
	)

	modules: dict[str, ModuleActivationState] = {}
	for row in rows:
		key = (row.module_key or "").strip().lower()
		if not key:
			continue
		depends_on = tuple(
			token.strip().lower()
			for token in (row.depends_on or "").split(",")
			if token.strip()
		)
		module_state = ModuleActivationState(
			key=key,
			label=row.module_label or key.title(),
			is_enabled=bool(row.is_enabled),
			is_required=bool(row.is_required),
			depends_on=depends_on,
			feature_overrides=_safe_json_load(row.feature_overrides),
		)
		modules[key] = module_state
	return modules


def _apply_feature_overrides(target: MutableMapping[str, FeatureValue], overrides: Mapping[str, FeatureValue]) -> None:
	for raw_key, value in overrides.items():
		key = (raw_key or "").strip().lower()
		if not key:
			continue
		target[key] = value


def _safe_json_load(raw: Any) -> dict[str, FeatureValue]:
	if not raw:
		return {}
	if isinstance(raw, dict):
		return raw
	try:
		loaded = json.loads(raw)
	except (TypeError, ValueError):
		return {}
	if isinstance(loaded, dict):
		return loaded
	return {}

