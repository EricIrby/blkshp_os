"""Department DocType controller."""
from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document


class Department(Document):
	"""Department master - foundation for department-based segmentation."""

	def autoname(self) -> None:
		"""Use department code as the document name."""
		code = (self.department_code or "").strip()
		if not code:
			raise frappe.ValidationError(_("Department Code is required to name the record."))
		self.name = code

	def validate(self) -> None:
		self._validate_required_fields()
		self._validate_department_code_uniqueness()
		self._validate_parent_department()

	def _validate_required_fields(self) -> None:
		if not (self.department_name or "").strip():
			raise frappe.ValidationError(_("Department Name is required."))
		if not self.company:
			raise frappe.ValidationError(_("Company is required."))

	def _validate_department_code_uniqueness(self) -> None:
		"""Ensure department code is unique within company (case-insensitive)."""
		code = (self.department_code or "").strip()
		if not code:
			raise frappe.ValidationError(_("Department Code is required."))

		filters = {
			"department_code": code,
			"company": self.company,
		}
		if self.name:
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
			"can_approve",
		],
		order_by="parent asc",
	)
