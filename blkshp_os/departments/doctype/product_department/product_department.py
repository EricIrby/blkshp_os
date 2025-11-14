"""Product Department child DocType controller."""

from __future__ import annotations

from decimal import Decimal

import frappe
from frappe import _
from frappe.model.document import Document

NUMERIC_FIELDS = ("par_level", "order_quantity")


class ProductDepartment(Document):
    """Child table defining product-to-department allocations and overrides."""

    def validate(self) -> None:
        self._ensure_department_exists()
        self._ensure_department_is_active()
        self._ensure_unique_department_assignment()
        self._ensure_single_primary_department()
        self._validate_numeric_fields()
        self._apply_department_defaults()

    def _ensure_department_exists(self) -> None:
        if not self.department:
            raise frappe.ValidationError(_("Department is required."))
        if not frappe.db.exists("Department", self.department):
            raise frappe.ValidationError(
                _("Department {0} does not exist.").format(self.department)
            )

    def _ensure_department_is_active(self) -> None:
        if not frappe.db.get_value("Department", self.department, "is_active"):
            raise frappe.ValidationError(
                _("Department {0} is inactive.").format(self.department)
            )

    def _ensure_unique_department_assignment(self) -> None:
        if not (self.parent and self.parenttype):
            return

        duplicate = frappe.get_all(
            "Product Department",
            filters={
                "parent": self.parent,
                "parenttype": self.parenttype,
                "department": self.department,
                "name": ("!=", self.name or "NEW-PRODUCT-DEPT"),
            },
            limit=1,
        )
        if duplicate:
            raise frappe.ValidationError(
                _("Department {0} is already assigned to this product.").format(
                    self.department
                )
            )

    def _ensure_single_primary_department(self) -> None:
        if not self.is_primary:
            return

        parent_doc = self._get_parent_doc()
        if not parent_doc:
            return

        primary_count = sum(
            1
            for row in parent_doc.departments
            if row.is_primary and row.name != self.name
        )
        if primary_count:
            raise frappe.ValidationError(
                _("Only one department can be marked as primary per product.")
            )

    def _validate_numeric_fields(self) -> None:
        for field in NUMERIC_FIELDS:
            value = getattr(self, field, None)
            if value is None:
                continue
            if value < 0:
                raise frappe.ValidationError(
                    _("Field {0} cannot be negative for department {1}.").format(
                        frappe.bold(field), self.department
                    )
                )

    def _apply_department_defaults(self) -> None:
        if self.default_storage_area:
            return

        default_storage_area = frappe.db.get_value(
            "Department", self.department, "default_storage_area"
        )
        if default_storage_area:
            self.default_storage_area = default_storage_area

    def _get_parent_doc(self) -> Document | None:
        parent_doc = getattr(self, "parent_doc", None)
        if parent_doc:
            return parent_doc

        if not (self.parent and self.parenttype):
            return None

        try:
            return frappe.get_doc(self.parenttype, self.parent)
        except frappe.DoesNotExistError:
            return None


def normalize_numeric(value: float | int | Decimal | None) -> float | None:
    """Return normalized float value for numeric fields (helper for tests)."""
    if value is None:
        return None
    return float(Decimal(value))
