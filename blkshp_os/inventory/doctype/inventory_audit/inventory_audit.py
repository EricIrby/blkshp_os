from __future__ import annotations

from collections import defaultdict
from collections.abc import Iterable

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime  # type: ignore[import]

STATUS_SEQUENCE = (
    "Setup",
    "Ready",
    "In Progress",
    "Review",
    "Closed",
    "Locked",
)


class InventoryAudit(Document):
    """Inventory audit lifecycle controller."""

    def validate(self) -> None:
        self._ensure_valid_status()
        self._ensure_unique_scope()

    def create_counting_tasks(self) -> None:
        """Generate counting tasks from the configured scope."""
        if not self.audit_departments:
            frappe.throw(
                _("Add at least one department before creating counting tasks.")
            )

        storage_map, general_storages = self._build_storage_map()
        categories = self._get_distinct_categories()

        self.set("counting_tasks", [])

        for dept_row in self.audit_departments:
            department = dept_row.department
            storages = storage_map.get(department, []) or []
            if general_storages:
                storages.extend(general_storages)

            if not storages:
                storages = [None]

            if categories:
                for storage in storages:
                    for category in categories:
                        self._append_task(department, storage, category)
            else:
                for storage in storages:
                    self._append_task(department, storage, None)

        if self.status == "Setup":
            self.status = "Ready"

    def mark_in_progress(self) -> None:
        if self.status not in {"Setup", "Ready"}:
            return
        self.status = "In Progress"

    def mark_review(self) -> None:
        if self.status not in {"Ready", "In Progress"}:
            return
        self.status = "Review"

    def close_audit(self, user: str | None = None) -> None:
        if self.status not in {"Review", "In Progress", "Ready"}:
            frappe.throw(
                _(
                    "Audit must be in Review, In Progress, or Ready status before closing."
                )
            )

        totals: dict[tuple[str, str], float] = defaultdict(float)
        unique_products: set[str] = set()
        total_value = 0.0

        for line in self.audit_lines or []:
            product = line.product
            if not product:
                frappe.throw(_("Audit lines require a product."))

            department = line.department or self._infer_department_for_line(line)
            if not department:
                frappe.throw(_("Audit lines require a department."))

            quantity_primary = self._convert_line_quantity_to_primary(line)
            line.quantity_primary = quantity_primary

            expected = line.expected_quantity or 0.0
            line.variance = quantity_primary - expected

            unit_cost = line.unit_cost or 0.0
            total_value += unit_cost * quantity_primary

            totals[(product, department)] += quantity_primary
            unique_products.add(product)

        # Generate Stock Ledger Entries using actual counted quantities vs current balances
        try:
            self.generate_stock_ledger_entries(totals)
        except Exception as e:
            frappe.throw(
                _("Failed to generate Stock Ledger Entries: {0}").format(str(e))
            )

        self.total_products_counted = len(unique_products)
        self.total_value = total_value
        self.closed_by = user or getattr(frappe.session, "user", None)  # type: ignore[attr-defined]
        self.closed_at = now_datetime()
        self.status = "Closed"

    def calculate_variance(self) -> dict[str, float]:
        """Return variance per product in primary units."""
        variances: dict[str, float] = defaultdict(float)
        for line in self.audit_lines or []:
            product = line.product
            if not product:
                continue
            quantity_primary = self._convert_line_quantity_to_primary(line)
            expected = line.expected_quantity or 0.0
            variance = quantity_primary - expected
            line.variance = variance
            variances[product] += variance
        return dict(variances)

    def generate_stock_ledger_entries(self, totals: dict[tuple[str, str], float]) -> list[str]:
        """
        Generate Stock Ledger Entries based on counted quantities vs current balances.

        Aggregates counted quantities by (product, department) and compares against
        current inventory balances to determine the actual adjustment needed.
        Creates one Stock Ledger Entry per unique (product, department) pair.

        Args:
            totals: Dict mapping (product, department) to total counted quantity

        Returns:
            list[str]: Names of created Stock Ledger Entries
        """
        created_entries: list[str] = []

        # Create Stock Ledger Entry for each (product, department) with adjustment
        for (product, department), counted_qty in totals.items():
            # Get current inventory balance
            from blkshp_os.inventory.doctype.stock_ledger_entry.stock_ledger_entry import (
                get_stock_balance,
            )

            current_balance = get_stock_balance(product, department, self.company)

            # Calculate adjustment needed: counted - current_balance
            adjustment = counted_qty - current_balance

            # Skip if no adjustment needed
            if adjustment == 0:
                continue

            # Create Stock Ledger Entry
            entry = frappe.new_doc("Stock Ledger Entry")
            entry.product = product
            entry.department = department
            entry.company = self.company
            entry.actual_qty = adjustment  # Adjustment to bring balance to counted quantity
            entry.posting_date = self.audit_date or frappe.utils.today()
            entry.posting_time = frappe.utils.nowtime()
            entry.voucher_type = "Inventory Audit"
            entry.voucher_no = self.name

            try:
                entry.insert(ignore_permissions=True)
                entry.submit()
                created_entries.append(entry.name)

                frappe.msgprint(
                    _("Created Stock Ledger Entry {0} for {1}/{2} (counted: {3}, current: {4}, adjustment: {5})").format(
                        entry.name, product, department, counted_qty, current_balance, adjustment
                    ),
                    alert=True,
                )
            except Exception as e:
                frappe.log_error(
                    title=f"Stock Ledger Entry Creation Failed for {product}/{department}",
                    message=str(e),
                )
                frappe.throw(
                    _("Failed to create Stock Ledger Entry for {0}/{1}: {2}").format(
                        product, department, str(e)
                    )
                )

        if created_entries:
            frappe.msgprint(
                _("Successfully generated {0} Stock Ledger Entries").format(
                    len(created_entries)
                ),
                indicator="green",
            )

        return created_entries

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------
    def _ensure_valid_status(self) -> None:
        if self.status not in STATUS_SEQUENCE:
            frappe.throw(
                _("Invalid status {0}. Must be one of: {1}.").format(
                    self.status, ", ".join(STATUS_SEQUENCE)
                )
            )

    def _ensure_unique_scope(self) -> None:
        self._ensure_unique_field(self.audit_departments, "department", _("Department"))
        self._ensure_unique_field(
            self.audit_storage_locations, "storage_area", _("Storage Area")
        )
        self._ensure_unique_field(
            self.audit_categories,
            "product_category",
            _("Product Category"),
        )

    def _ensure_unique_field(
        self,
        rows: Iterable[Document] | None,
        fieldname: str,
        label: str,
    ) -> None:
        seen: set[str] = set()
        for row in rows or []:
            value = getattr(row, fieldname, None)
            if not value:
                continue
            if value in seen:
                frappe.throw(_("Duplicate {0}: {1}.").format(label, value))
            seen.add(value)

    def _build_storage_map(self) -> tuple[dict[str, list[str]], list[str]]:
        storage_map: dict[str, list[str]] = defaultdict(list)
        general_storages: list[str] = []

        for row in self.audit_storage_locations or []:
            storage_name = row.storage_area
            if not storage_name:
                continue

            storage_doc = frappe.get_doc("Storage Area", storage_name)
            department = storage_doc.department
            if department:
                storage_map[department].append(storage_doc.name)
            else:
                general_storages.append(storage_doc.name)

        return storage_map, general_storages

    def _get_distinct_categories(self) -> list[str]:
        return sorted(
            {
                row.product_category
                for row in self.audit_categories or []
                if row.product_category
            }
        )

    def _append_task(
        self,
        department: str,
        storage_area: str | None,
        category: str | None,
    ) -> None:
        self.append(
            "counting_tasks",
            {
                "department": department,
                "storage_area": storage_area,
                "category": category,
                "status": "Pending",
            },
        )

    def _convert_line_quantity_to_primary(self, line: Document) -> float:
        product_doc = frappe.get_doc("Product", line.product)
        unit = line.unit or product_doc.primary_count_unit or ""
        quantity = line.quantity or 0.0
        return float(product_doc.convert_to_primary_unit(unit, quantity))

    def _infer_department_for_line(self, line: Document) -> str | None:
        if line.department:
            return line.department
        if line.storage_area:
            storage_doc = frappe.get_doc("Storage Area", line.storage_area)
            return storage_doc.department
        return None
