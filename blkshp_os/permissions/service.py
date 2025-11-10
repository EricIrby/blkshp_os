"""Shared permission helpers for department-aware access control."""
from __future__ import annotations

from typing import Iterable, Sequence

import frappe
from frappe import _

from blkshp_os.core_platform.services import get_subscription_context

PERMISSION_FLAGS: tuple[str, ...] = (
	"can_read",
	"can_write",
	"can_create",
	"can_delete",
	"can_submit",
	"can_cancel",
	"can_approve",
)

SYSTEM_ROLES_BYPASS: tuple[str, ...] = ("System Manager", "Administrator")


def get_permission_flags() -> tuple[str, ...]:
	"""Return the supported department permission flags."""
	return PERMISSION_FLAGS


def validate_permission_flag(permission_flag: str) -> str:
	"""Raise if the provided permission flag is not supported."""
	if permission_flag not in PERMISSION_FLAGS:
		raise frappe.ValidationError(_("Unsupported permission flag: {0}").format(permission_flag))
	return permission_flag


def _user_bypasses_department_permissions(user: str | None) -> bool:
	"""Return True if the user should bypass department permission filtering."""
	if not user or user in ("Administrator", "Guest"):
		return True
	user_roles = set(frappe.get_roles(user))
	return any(role in user_roles for role in SYSTEM_ROLES_BYPASS)


def get_user_company(user: str | None) -> str | None:
	"""Return the company associated with the provided user."""
	if not user:
		return None
	user_doc = frappe.get_cached_doc("User", user)
	get_company = getattr(user_doc, "get_company", None)
	if callable(get_company):
		return get_company()
	return frappe.db.get_value("User", user, "company")


def get_user_subscription_context(user: str | None, *, refresh: bool = False):
	"""Return the subscription context for the supplied user."""
	if not user:
		return get_subscription_context(plan_code=None)
	user_doc = frappe.get_cached_doc("User", user)
	get_context = getattr(user_doc, "get_subscription_context", None)
	if callable(get_context):
		return get_context(refresh=refresh)
	return get_subscription_context(company=get_user_company(user))


def user_has_module_access(user: str | None, module_key: str, *, refresh: bool = False) -> bool:
	"""Return True when the user has access to the supplied module."""
	if not user:
		return False
	user_doc = frappe.get_cached_doc("User", user)
	check = getattr(user_doc, "is_module_enabled", None)
	if callable(check):
		return check(module_key, refresh=refresh)

	context = get_subscription_context(company=get_user_company(user), use_cache=not refresh)
	module = context.modules.get((module_key or "").strip().lower())
	return bool(module and module.is_enabled)


def user_has_feature(user: str | None, feature_key: str, *, refresh: bool = False) -> bool:
	"""Return True when the user has access to the supplied feature toggle."""
	if not user:
		return False
	user_doc = frappe.get_cached_doc("User", user)
	check = getattr(user_doc, "is_feature_enabled", None)
	if callable(check):
		return check(feature_key, refresh=refresh)

	context = get_subscription_context(company=get_user_company(user), use_cache=not refresh)
	return bool(context.feature_states.get((feature_key or "").strip().lower()))


def get_accessible_departments(
	user: str, permission_flag: str = "can_read", include_inactive: bool = False
) -> list[str]:
	"""Return the list of departments the user may access for the provided permission flag."""
	if _user_bypasses_department_permissions(user):
		active_filter = {} if include_inactive else {"is_active": 1}
		return frappe.get_all("Department", filters=active_filter, pluck="name")

	validate_permission_flag(permission_flag)

	permissions = frappe.get_all(
		"Department Permission",
		filters={
			"parent": user,
			"parenttype": "User",
			permission_flag: 1,
		},
		fields=["department"],
	)
	departments = {row.department for row in permissions if row.department}

	if not departments:
		return []

	if include_inactive:
		return sorted(departments)

	active_departments = frappe.get_all(
		"Department",
		filters={
			"name": ["in", list(departments)],
			"is_active": 1,
		},
		pluck="name",
	)
	return sorted(active_departments)


def has_department_permission(
	user: str, department: str, permission_flag: str = "can_read", include_inactive: bool = False
) -> bool:
	"""Return True when the user has the requested permission for the department."""
	if _user_bypasses_department_permissions(user):
		return True

	validate_permission_flag(permission_flag)
	if not department:
		return False

	if not include_inactive:
		is_active = frappe.db.get_value("Department", department, "is_active") or 0
		if not is_active:
			return False

	filters = {
		"parent": user,
		"parenttype": "User",
		"department": department,
		permission_flag: 1,
	}
	if frappe.db.exists("Department Permission", filters):
		return True

	return False


def get_user_department_permissions(
	user: str,
	permission_flag: str | None = None,
	include_inactive: bool = False,
) -> list[dict[str, object]]:
	"""Return full Department Permission rows for the user."""
	if _user_bypasses_department_permissions(user):
		departments = frappe.get_all(
			"Department",
			filters={} if include_inactive else {"is_active": 1},
			fields=["name as department"],
		)
		return [
			{
				"department": row.department,
				**{flag: 1 for flag in PERMISSION_FLAGS},
			}
			for row in departments
		]

	filters: dict[str, object] = {
		"parent": user,
		"parenttype": "User",
	}
	if permission_flag:
		validate_permission_flag(permission_flag)
		filters[permission_flag] = 1

	permissions = frappe.get_all(
		"Department Permission",
		filters=filters,
		fields=["name", "department", *PERMISSION_FLAGS, "valid_from", "valid_upto", "notes"],
		order_by="department asc",
	)

	if include_inactive or not permissions:
		return permissions

	department_names = {row.department for row in permissions if row.department}
	if not department_names:
		return []

	active_departments = set(
		frappe.get_all(
			"Department",
			filters={"name": ["in", list(department_names)], "is_active": 1},
			pluck="name",
		)
	)
	return [row for row in permissions if row["department"] in active_departments]


def build_department_filter_clause(departments: Sequence[str]) -> str:
	"""Return SQL clause filtering Department.name within provided departments."""
	if not departments:
		return "1=2"
	safe_departments = ", ".join(frappe.db.escape(dep) for dep in departments)
	return f"`tabDepartment`.`name` in ({safe_departments})"


def get_department_permission_clause(user: str, permission_flag: str = "can_read") -> str:
	"""Return the SQL condition restricting Department queries for the user."""
	if _user_bypasses_department_permissions(user):
		return ""

	departments = get_accessible_departments(user, permission_flag=permission_flag)
	if not departments:
		return "1=2"
	return build_department_filter_clause(departments)


