"""Extensions to the Frappe User DocType."""
from __future__ import annotations

from typing import Any, Iterable

import frappe

from blkshp_os.core_platform.services import get_subscription_context

from . import service


class UserPermissionMixin:
	"""Mixin attached to Frappe's User Doctype at runtime."""

	_subscription_context_cache_attr = "_blkshp_subscription_context"

	def get_department_permissions(self, permission_flag: str | None = None) -> list[dict[str, object]]:
		"""Return Department Permission rows linked to this user."""
		return service.get_user_department_permissions(
			user=self.name,
			permission_flag=permission_flag,
		)

	def has_department_permission(self, department: str, permission_flag: str = "can_read") -> bool:
		"""Return True when the user has the requested permission for the department."""
		return service.has_department_permission(
			user=self.name,
			department=department,
			permission_flag=permission_flag,
		)

	def get_accessible_departments(
		self, permission_flag: str = "can_read", include_inactive: bool = False
	) -> list[str]:
		"""Return departments accessible to this user for the supplied permission flag."""
		return service.get_accessible_departments(
			user=self.name,
			permission_flag=permission_flag,
			include_inactive=include_inactive,
		)

	def get_company(self) -> str | None:
		"""Return the company associated with this user, if available."""
		company = getattr(self, "company", None)
		if company:
			return company

		for department in self.get_accessible_departments():
			department_company = frappe.db.get_value("Department", department, "company")
			if department_company:
				return department_company
		return None

	def get_subscription_context(
		self, *, company: str | None = None, refresh: bool = False
	):
		"""Return the cached subscription context for the user."""
		cache_key = self._subscription_context_cache_attr
		if not refresh and hasattr(self, cache_key):
			return getattr(self, cache_key)

		context = get_subscription_context(company=company or self.get_company())
		setattr(self, cache_key, context)
		return context

	def clear_subscription_context_cache(self) -> None:
		"""Clear the cached subscription context for this user instance."""
		cache_key = self._subscription_context_cache_attr
		if hasattr(self, cache_key):
			delattr(self, cache_key)

	def get_subscription_plan_code(self, *, company: str | None = None, refresh: bool = False) -> str | None:
		"""Return the plan code assigned to this user (via company/branding)."""
		context = self.get_subscription_context(company=company, refresh=refresh)
		if context.plan:
			return context.plan.plan_code
		return None

	def is_module_enabled(
		self, module_key: str, *, company: str | None = None, refresh: bool = False
	) -> bool:
		"""Return True if the specified module is enabled for the user."""
		normalized_key = (module_key or "").strip().lower()
		if not normalized_key:
			return False

		if self._is_internal_operator():
			return True

		context = self.get_subscription_context(company=company, refresh=refresh)
		module = context.modules.get(normalized_key)
		return bool(module and module.is_enabled)

	def is_feature_enabled(
		self, feature_key: str, *, company: str | None = None, refresh: bool = False
	) -> bool:
		"""Return True if the specified feature toggle is enabled for the user."""
		normalized_key = (feature_key or "").strip().lower()
		if not normalized_key:
			return False

		if self._is_internal_operator():
			return True

		context = self.get_subscription_context(company=company, refresh=refresh)
		value: Any | None = context.feature_states.get(normalized_key)

		if isinstance(value, bool):
			return value
		if isinstance(value, dict):
			return bool(value)
		if value is None:
			metadata = context.registry.get(normalized_key)
			return bool(metadata.default_enabled) if metadata else False
		return bool(value)

	def _is_internal_operator(self) -> bool:
		"""Return True if the user is part of the BLKSHP operations staff."""
		if self.name in ("Administrator",):
			return True
		roles = set(frappe.get_roles(self.name))
		operations_roles = set(service.SYSTEM_ROLES_BYPASS) | {"BLKSHP Operations"}
		return bool(roles.intersection(operations_roles))

	@staticmethod
	def get_permission_flags() -> Iterable[str]:
		"""Expose valid department permission flags."""
		return service.get_permission_flags()

