"""Role Permission child DocType controller."""

from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.permissions.constants import get_permission, is_valid_permission


class RolePermission(Document):
    """Child table storing custom permissions for a role."""

    def validate(self) -> None:
        run_role_permission_validation(self)


def run_role_permission_validation(doc: Document, method: str | None = None) -> None:
    _validate_permission_code(doc)
    _populate_permission_details(doc)


def validate_role_permissions(role_doc: Document, method: str | None = None) -> None:
    for row in role_doc.get("custom_permissions", []):
        run_role_permission_validation(row)


def _validate_permission_code(doc: Document) -> None:
    """Validate that permission code exists in the registry."""
    if not doc.get("permission_code"):
        raise frappe.ValidationError(_("Permission Code is required."))

    if not is_valid_permission(doc.permission_code):
        raise frappe.ValidationError(
            _(
                "Invalid permission code: {0}. Must be a valid permission from the registry."
            ).format(doc.permission_code)
        )


def _populate_permission_details(doc: Document) -> None:
    """Auto-populate permission details from registry."""
    if not doc.get("permission_code"):
        return

    perm_def = get_permission(doc.permission_code)
    if perm_def:
        doc.permission_name = perm_def["name"]
        doc.permission_category = perm_def["category"]
        doc.description = perm_def["description"]
        doc.department_restricted = 1 if perm_def["department_restricted"] else 0
