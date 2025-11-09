"""Department DocType controller."""
from __future__ import annotations

import json
from collections.abc import Iterable
from typing import Any, TypedDict

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.permissions import service as permission_service


SETTINGS_TYPE_MAP: dict[str, type | tuple[type, ...]] = {
	"eoq_enabled": bool,
	"eoq_calculation_method": str,
	"eoq_safety_stock_factor": (int, float),
	"reorder_point_buffer": (int, float),
	"reorder_point_method": str,
	"default_ordering_day": str,
	"minimum_order_amount": (int, float),
	"require_order_approval": bool,
	"allow_inter_department_transfers": bool,
	"require_approval_for_transfers": bool,
	"transfer_approval_roles": list,
	"inventory_count_frequency": str,
	"require_count_approval": bool,
	"variance_threshold": (int, float),
	"budget_alert_threshold": (int, float),
	"budget_alert_frequency": str,
	"budget_fiscal_year": str,
	"custom_settings": dict,
}


class DepartmentSettings(TypedDict, total=False):
	eoq_enabled: bool
	eoq_calculation_method: str
	eoq_safety_stock_factor: float
	reorder_point_buffer: float
	reorder_point_method: str
	default_ordering_day: str
	minimum_order_amount: float
	require_order_approval: bool
	allow_inter_department_transfers: bool
	require_approval_for_transfers: bool
	transfer_approval_roles: list[str]
	inventory_count_frequency: str
	require_count_approval: bool
	variance_threshold: float
	budget_alert_threshold: float
	budget_alert_frequency: str
	budget_fiscal_year: str
	custom_settings: dict[str, Any]


class Department(Document):
	"""Department master - foundation for department-based segmentation."""

	def autoname(self) -> None:
		"""Generate a unique name per company using the normalized department code."""
		code = self._normalized_code()
		if not code:
			raise frappe.ValidationError(_("Department Code is required to name the record."))

		company = (self.company or "").strip()
		if not company:
			raise frappe.ValidationError(_("Company is required before naming the department."))

		company_code = (
			frappe.db.get_value("Company", company, "company_code") or company
		)
		company_code = (company_code or "").strip().upper().replace(" ", "-")
		if not company_code:
			raise frappe.ValidationError(_("Company Code is required to name the department."))

		self.name = f"{code}-{company_code}"

	def validate(self) -> None:
		self._normalize_fields()
		self._validate_required_fields()
		self._validate_department_code_uniqueness()
		self._validate_parent_department()
		self._validate_settings_json()

	def before_save(self) -> None:
		self._normalize_fields()

	def _normalize_fields(self) -> None:
		self.department_name = (self.department_name or "").strip()
		if self.department_code:
			self.department_code = self._normalized_code()
		if self.parent_department == "":
			self.parent_department = None

	def _normalized_code(self) -> str:
		return (self.department_code or "").strip().upper()

	def _validate_required_fields(self) -> None:
		if not self.department_name:
			raise frappe.ValidationError(_("Department Name is required."))
		if not self.company:
			raise frappe.ValidationError(_("Company is required."))
		if not self._normalized_code():
			raise frappe.ValidationError(_("Department Code is required."))

	def _validate_department_code_uniqueness(self) -> None:
		"""Ensure department code is unique within company (case-insensitive)."""
		code = self._normalized_code()
		filters = {"department_code": code, "company": self.company}
		if self.name and not self.is_new():
			filters["name"] = ("!=", self.name)

		if frappe.db.exists("Department", filters):
			raise frappe.ValidationError(
				_("Department Code {0} already exists for company {1}.").format(code, self.company)
			)

	def _validate_parent_department(self) -> None:
		if not self.parent_department:
			return

		if self.parent_department == self.name:
			raise frappe.ValidationError(_("Parent Department cannot be the same as the department."))

		parent_company = frappe.db.get_value("Department", self.parent_department, "company")
		if parent_company and parent_company != self.company:
			raise frappe.ValidationError(_("Parent Department must belong to the same company."))

		self._validate_no_circular_reference(self.parent_department)

	def _validate_no_circular_reference(self, parent: str) -> None:
		"""Ensure there is no circular reference in the department hierarchy."""
		seen = {self.name}
		current = parent
		while current:
			if current in seen:
				raise frappe.ValidationError(_("Circular department hierarchy detected."))
			seen.add(current)
			current = frappe.db.get_value("Department", current, "parent_department")

	def _validate_settings_json(self) -> None:
		if not self.settings:
			return

		if isinstance(self.settings, dict):
			settings_dict = self.settings
		else:
			try:
				settings_dict = json.loads(self.settings)
			except ValueError as exc:
				raise frappe.ValidationError(_("Settings must be valid JSON.")) from exc

		for key, expected_type in SETTINGS_TYPE_MAP.items():
			if key not in settings_dict:
				continue

			value = settings_dict[key]
			if expected_type is list:
				if not isinstance(value, list):
					raise frappe.ValidationError(
						_("Settings key {0} must be a list.").format(frappe.bold(key))
					)
			elif expected_type is dict:
				if not isinstance(value, dict):
					raise frappe.ValidationError(
						_("Settings key {0} must be a dictionary.").format(frappe.bold(key))
					)
			elif isinstance(expected_type, tuple):
				if not isinstance(value, expected_type):
					raise frappe.ValidationError(
						_("Settings key {0} must be numeric.").format(frappe.bold(key))
					)
			elif not isinstance(value, expected_type):
				raise frappe.ValidationError(
					_("Settings key {0} must be of type {1}.").format(
						frappe.bold(key), expected_type.__name__
					)
				)

		self.settings = json.dumps(settings_dict, sort_keys=True)


@frappe.whitelist()
def get_products(department: str) -> list[dict[str, object]]:
	"""Return products assigned to a department sorted by primary flag and name."""
	department = (department or "").strip()
	if not department:
		raise frappe.ValidationError(_("Department is required."))

	return frappe.get_all(
		"Product Department",
		filters={
			"department": department,
			"parenttype": "Product",
		},
		fields=["parent as product", "is_primary"],
		order_by="is_primary desc, parent asc",
	)


@frappe.whitelist()
def get_users(department: str) -> list[dict[str, object]]:
	"""Return users with explicit access to the department."""
	department = (department or "").strip()
	if not department:
		raise frappe.ValidationError(_("Department is required."))

	return frappe.get_all(
		"Department Permission",
		filters={
			"department": department,
			"parenttype": "User",
			"can_read": 1,
		},
		fields=[
			"parent as user",
			"can_read",
			"can_write",
			"can_create",
			"can_delete",
			"can_submit",
			"can_cancel",
			"can_approve",
		],
		order_by="parent asc",
	)


def get_default_storage_area(department: str) -> str | None:
	return frappe.db.get_value("Department", department, "default_storage_area")


def get_default_gl_code(department: str) -> str | None:
	return frappe.db.get_value("Department", department, "default_gl_code")


def get_department_setting(
	department: str, setting_key: str, default_value: Any | None = None
) -> Any | None:
	settings = frappe.db.get_value("Department", department, "settings")
	if not settings:
		return default_value

	if isinstance(settings, str):
		try:
			settings_dict: DepartmentSettings = json.loads(settings)
		except ValueError:
			return default_value
	else:
		settings_dict = settings

	return settings_dict.get(setting_key, default_value)


def get_accessible_departments(user: str, permission_flag: str = "can_read") -> list[str]:
    """Return list of departments that user can access with given permission flag."""
    return permission_service.get_accessible_departments(user, permission_flag=permission_flag)


def apply_department_defaults(product: str, department: str) -> None:
	"""Apply department-level defaults to the Product Department child record."""
	product_doc = frappe.get_doc("Product", product)
	for row in getattr(product_doc, "departments", []):
		if row.department != department:
			continue

		if not getattr(row, "default_storage_area", None):
			row.default_storage_area = get_default_storage_area(department)

		if hasattr(row, "default_gl_code") and not getattr(row, "default_gl_code", None):
			row.default_gl_code = get_default_gl_code(department)

	product_doc.flags.ignore_validate_update_after_submit = True
	product_doc.save(ignore_permissions=True)


def SETTINGS_PERMISSION_FLAGS() -> Iterable[str]:
    """Expose permission flags shared with Department Permission DocType."""
    return permission_service.get_permission_flags()
