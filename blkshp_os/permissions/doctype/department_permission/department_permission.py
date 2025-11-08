"""Department Permission child DocType controller."""
from __future__ import annotations

from typing import Iterable

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.permissions.service import (
	PERMISSION_FLAGS,
	get_permission_flags as service_get_permission_flags,
)


class DepartmentPermission(Document):
	"""Child table storing department-level permission overrides for a user."""

	def validate(self) -> None:
		self._ensure_department_exists_and_active()
		self._ensure_company_alignment()
		self._ensure_permission_selected()
		self._ensure_no_duplicate_assignments()
		self._validate_effective_dates()

	def _ensure_department_exists_and_active(self) -> None:
		if not self.department:
			raise frappe.ValidationError(_("Department is required."))

		is_active = frappe.db.get_value("Department", self.department, "is_active")
		if is_active is None:
			raise frappe.ValidationError(_("Department {0} does not exist.").format(self.department))
		if not is_active:
			raise frappe.ValidationError(_("Department {0} is inactive.").format(self.department))

	def _ensure_company_alignment(self) -> None:
		"""Validate department belongs to the same company as the parent user (if provided)."""
		department_company = frappe.db.get_value("Department", self.department, "company")
		if not department_company:
			return

		# Some implementations store company on the User document (custom field).
		user_company = frappe.db.get_value("User", self.parent, "company")
		if user_company and user_company != department_company:
			raise frappe.ValidationError(
				_("Department {0} belongs to company {1}, which does not match user company {2}.").format(
					self.department, department_company, user_company
				)
			)

	def _ensure_permission_selected(self) -> None:
		if not any(bool(getattr(self, flag, False)) for flag in PERMISSION_FLAGS):
			raise frappe.ValidationError(_("Select at least one permission for the department access."))

	def _ensure_no_duplicate_assignments(self) -> None:
		if not self.parent or not self.department:
			return

		duplicates = frappe.get_all(
			"Department Permission",
			filters={
				"parent": self.parent,
				"parenttype": self.parenttype,
				"department": self.department,
				"name": ("!=", self.name or "NEW-DEPARTMENT-PERM"),
			},
			pluck="name",
		)
		if duplicates:
			raise frappe.ValidationError(
				_("Department {0} is already assigned to this user.").format(self.department)
			)

	def _validate_effective_dates(self) -> None:
		if self.valid_from and self.valid_upto and self.valid_from > self.valid_upto:
			raise frappe.ValidationError(_("Valid Upto must be on or after Valid From."))


def get_permission_flags() -> Iterable[str]:
	"""Return the list of supported permission flags."""
	return service_get_permission_flags()


