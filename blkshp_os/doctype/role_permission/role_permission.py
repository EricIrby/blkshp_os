"""Role Permission child DocType controller."""
from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.permissions.constants import get_permission, is_valid_permission


class RolePermission(Document):
	"""Child table storing custom permissions for a role."""

	def validate(self) -> None:
		self._validate_permission_code()
		self._populate_permission_details()

	def _validate_permission_code(self) -> None:
		"""Validate that permission code exists in the registry."""
		if not self.permission_code:
			raise frappe.ValidationError(_("Permission Code is required."))

		if not is_valid_permission(self.permission_code):
			raise frappe.ValidationError(
				_("Invalid permission code: {0}. Must be a valid permission from the registry.").format(
					self.permission_code
				)
			)

	def _populate_permission_details(self) -> None:
		"""Auto-populate permission details from registry."""
		if not self.permission_code:
			return

		perm_def = get_permission(self.permission_code)
		if perm_def:
			self.permission_name = perm_def["name"]
			self.permission_category = perm_def["category"]
			self.description = perm_def["description"]
			self.department_restricted = perm_def["department_restricted"]

