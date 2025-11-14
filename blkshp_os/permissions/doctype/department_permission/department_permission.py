"""Department Permission child DocType controller."""

from __future__ import annotations

from collections.abc import Iterable

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import cint, getdate

from blkshp_os.permissions.service import (
    get_permission_flags as service_get_permission_flags,
)


class DepartmentPermission(Document):
    """Child table storing department-level permission overrides for a user."""

    def validate(self) -> None:
        run_department_permission_validation(self)


def run_department_permission_validation(
    doc: Document, method: str | None = None
) -> None:
    """Shared validation logic for Department Permission rows."""
    _ensure_department_exists_and_active(doc)
    _ensure_company_alignment(doc)
    _ensure_permission_selected(doc)
    _ensure_no_duplicate_assignments(doc)
    _validate_effective_dates(doc)


def validate_user_department_permissions(
    user_doc: Document, method: str | None = None
) -> None:
    """Validate all Department Permission rows attached to a User."""
    for row in user_doc.get("department_permissions", []):
        run_department_permission_validation(row)


def _ensure_department_exists_and_active(doc: Document) -> None:
    if not doc.get("department"):
        raise frappe.ValidationError(_("Department is required."))

    is_active = frappe.db.get_value("Department", doc.department, "is_active")
    if is_active is None:
        raise frappe.ValidationError(
            _("Department {0} does not exist.").format(doc.department)
        )
    if not cint(is_active):
        raise frappe.ValidationError(
            _("Department {0} is inactive.").format(doc.department)
        )


def _ensure_company_alignment(doc: Document) -> None:
    """Validate department belongs to the same company as the parent user (if provided)."""
    department_company = frappe.db.get_value("Department", doc.department, "company")
    if not department_company:
        return

    user_company = None
    if frappe.db.has_column("User", "company"):
        user_company = frappe.db.get_value("User", doc.parent, "company")
    if user_company and user_company != department_company:
        raise frappe.ValidationError(
            _(
                "Department {0} belongs to company {1}, which does not match user company {2}."
            ).format(doc.department, department_company, user_company)
        )


def _ensure_permission_selected(doc: Document) -> None:
    flags = service_get_permission_flags()
    if sum(cint(doc.get(flag)) for flag in flags) == 0:
        raise frappe.ValidationError(
            _("Select at least one permission for the department access.")
        )


def _ensure_no_duplicate_assignments(doc: Document) -> None:
    if not doc.get("parent") or not doc.get("department"):
        return

    parent_doc = getattr(doc, "get_parent_doc", lambda: None)()
    if parent_doc:
        child_table = doc.parentfield or "department_permissions"
        in_memory_duplicates = [
            row
            for row in parent_doc.get(child_table, [])
            if row is not doc
            and cint(getattr(row, "docstatus", 0)) != 2
            and row.get("department") == doc.department
        ]
        if in_memory_duplicates:
            raise frappe.ValidationError(
                _("Department {0} is already assigned to this user.").format(
                    doc.department
                )
            )

    if not doc.name or doc.name.startswith("NEW-"):
        return

    duplicates = frappe.get_all(
        "Department Permission",
        filters={
            "parent": doc.parent,
            "parenttype": doc.parenttype or "User",
            "department": doc.department,
            "name": ("!=", doc.name or "NEW-DEPARTMENT-PERM"),
        },
        pluck="name",
    )
    if duplicates:
        raise frappe.ValidationError(
            _("Department {0} is already assigned to this user.").format(doc.department)
        )


def _validate_effective_dates(doc: Document) -> None:
    if doc.get("valid_from") and doc.get("valid_upto"):
        valid_from = getdate(doc.valid_from)
        valid_upto = getdate(doc.valid_upto)
        if valid_from > valid_upto:
            raise frappe.ValidationError(
                _("Valid Upto must be on or after Valid From.")
            )


def get_permission_flags() -> Iterable[str]:
    """Return the list of supported permission flags."""
    return service_get_permission_flags()
