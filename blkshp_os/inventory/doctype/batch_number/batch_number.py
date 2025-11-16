# Copyright (c) 2025, BLKSHP and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import add_days, getdate, now_datetime, today


class BatchNumber(Document):
    """
    Batch/lot number tracking for inventory items.

    Enables traceability and expiration management for perishable products.
    Each batch represents a specific production run with manufacturing and
    expiration dates.
    """

    def autoname(self) -> None:
        """
        Auto-generate batch_id if not provided.

        Format: {product_code}-{YYYY}-{####}
        Example: TOMATO-2025-0001
        """
        if not self.batch_id:
            product_code = frappe.db.get_value("Product", self.product, "product_code")
            if not product_code:
                frappe.throw(_("Product {0} not found").format(self.product))

            year = getdate(self.manufacturing_date or today()).year

            # Use SQL to find the next sequence number atomically with row locking
            # FOR UPDATE prevents race conditions during batch ID generation
            result = frappe.db.sql(
                """
                SELECT COALESCE(MAX(CAST(SUBSTRING_INDEX(batch_id, '-', -1) AS UNSIGNED)), 0) + 1
                FROM `tabBatch Number`
                WHERE product = %s AND batch_id LIKE %s
                FOR UPDATE
                """,
                (self.product, f"{product_code}-{year}-%"),
                as_list=True
            )

            next_seq = int(result[0][0]) if result else 1
            self.batch_id = f"{product_code}-{year}-{next_seq:04d}"

    def validate(self) -> None:
        """Validate batch data before saving."""
        self.validate_dates()
        self.calculate_shelf_life()
        self.update_status()

    def before_save(self) -> None:
        """Set default values before saving."""
        if not self.status:
            self.status = "Active"

    def validate_dates(self) -> None:
        """Ensure expiration date is after manufacturing date."""
        if self.manufacturing_date and self.expiration_date:
            if getdate(self.expiration_date) <= getdate(self.manufacturing_date):
                frappe.throw(
                    _("Expiration date must be after manufacturing date")
                )

    def calculate_shelf_life(self) -> None:
        """
        Calculate shelf life in days if both dates are provided.

        Always recalculates when dates change, since shelf_life_in_days
        is read-only in the UI and should reflect the date range.
        """
        if self.manufacturing_date and self.expiration_date:
            mfg_date = getdate(self.manufacturing_date)
            exp_date = getdate(self.expiration_date)
            self.shelf_life_in_days = (exp_date - mfg_date).days

    def update_status(self) -> None:
        """
        Auto-update status based on expiration date and quantity.

        - Expired: expiration_date has passed
        - Consumed: quantity is 0 or negative
        - Active: otherwise

        Note: Manual Expired/Consumed status overrides are preserved unless
        self.flags.force_status_recalc is set.
        """
        # Preserve manual Expired/Consumed overrides unless forced
        if self.status in ("Expired", "Consumed") and not self.flags.get("force_status_recalc"):
            return

        if self.expiration_date and getdate(self.expiration_date) < getdate(today()):
            self.status = "Expired"
        elif self.quantity is not None and self.quantity <= 0:
            self.status = "Consumed"
        else:
            self.status = "Active"

    def update_quantity_from_ledger(self) -> None:
        """
        Recalculate quantity from Stock Ledger Entries.

        This should be called whenever a Stock Ledger Entry is created
        or cancelled for this batch.

        Note: This method relies on being called within a transaction context
        (typically from Stock Ledger Entry submission lifecycle).

        Performance: For optimal performance as ledger volume grows, ensure
        Stock Ledger Entry has an index covering:
        (batch_number, product, department, company, docstatus, is_cancelled)
        This will be addressed in BLK-47.
        """
        # Lock the batch row to prevent concurrent quantity updates
        frappe.db.sql(
            "SELECT name FROM `tabBatch Number` WHERE name = %s FOR UPDATE",
            (self.name,)
        )

        total_qty = frappe.db.sql(
            """
            SELECT SUM(actual_qty) as total
            FROM `tabStock Ledger Entry`
            WHERE batch_number = %s
                AND product = %s
                AND department = %s
                AND company = %s
                AND docstatus = 1
                AND is_cancelled = 0
            """,
            (self.name, self.product, self.department, self.company),
            as_dict=1
        )

        self.quantity = total_qty[0].total if total_qty and total_qty[0].total else 0
        self.db_set("quantity", self.quantity, update_modified=False)

        # Update status based on new quantity (force recalculation)
        self.flags.force_status_recalc = True
        self.update_status()
        self.db_set("status", self.status, update_modified=False)


# Scheduled task to update batch statuses daily
def update_batch_statuses():
    """
    Daily scheduled job to mark expired batches.

    Scans all Active batches and updates status to Expired if
    expiration_date has passed. Uses bulk SQL UPDATE for performance
    and atomicity.

    Performance: For optimal performance as data grows, consider adding
    a composite index on (status, expiration_date) via a migration script.
    Individual indexes on these fields are already in place.
    """
    # Get count of batches to be updated (before the update for portability)
    count = frappe.db.count(
        "Batch Number",
        filters={
            "status": "Active",
            "expiration_date": ["<", today()]
        }
    )

    if count:
        # Use bulk SQL UPDATE instead of iterating through batches
        frappe.db.sql(
            """
            UPDATE `tabBatch Number`
            SET status = 'Expired'
            WHERE status = 'Active'
              AND expiration_date < %s
            """,
            (today(),)
        )
        frappe.logger().info(f"Marked {count} batches as Expired")


# Query functions for batch management

def get_batch_balance(batch_name: str | None) -> float:
    """
    Get current quantity for a specific batch.

    Args:
        batch_name (str): Batch Number document name (usually same as batch_id field)

    Returns:
        float: Current batch quantity
    """
    if not batch_name:
        return 0

    return frappe.db.get_value("Batch Number", batch_name, "quantity") or 0


def get_expiring_batches(
    department: str | None = None,
    company: str | None = None,
    within_days: int = 30
) -> list[dict]:
    """
    Get batches expiring within specified days.

    Args:
        department (str, optional): Filter by department
        company (str, optional): Filter by company
        within_days (int): Number of days to look ahead (default 30)

    Returns:
        list: List of expiring batch records
    """
    filters = {
        "status": ["in", ["Active"]],
        "expiration_date": ["between", [today(), add_days(today(), within_days)]],
        "quantity": [">", 0]
    }

    if department:
        filters["department"] = ["=", department]
    if company:
        filters["company"] = ["=", company]

    return frappe.get_all(
        "Batch Number",
        filters=filters,
        fields=[
            "name",
            "batch_id",
            "product",
            "department",
            "quantity",
            "expiration_date",
            "manufacturing_date"
        ],
        order_by="expiration_date asc"
    )


def get_available_batches(product: str, department: str, company: str) -> list[dict]:
    """
    Get available batches for a product/department (FIFO order).

    Returns batches ordered by manufacturing_date (oldest first)
    for FIFO consumption.

    Args:
        product (str): Product name
        department (str): Department name
        company (str): Company name

    Returns:
        list: List of available batch records
    """
    return frappe.get_all(
        "Batch Number",
        filters={
            "product": ["=", product],
            "department": ["=", department],
            "company": ["=", company],
            "status": ["=", "Active"],
            "quantity": [">", 0]
        },
        fields=[
            "name",
            "batch_id",
            "quantity",
            "manufacturing_date",
            "expiration_date"
        ],
        order_by="manufacturing_date asc, creation asc"
    )
