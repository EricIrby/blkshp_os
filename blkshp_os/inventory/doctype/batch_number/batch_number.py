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

    def autoname(self):
        """
        Auto-generate batch_id if not provided.

        Format: {product_code}-{YYYY}-{####}
        Example: TOMATO-2025-0001
        """
        if not self.batch_id:
            product_code = frappe.db.get_value("Product", self.product, "product_code")
            year = getdate(self.manufacturing_date or today()).year

            # Find next sequence number for this product and year
            existing_batches = frappe.get_all(
                "Batch Number",
                filters={
                    "product": self.product,
                    "batch_id": ["like", f"{product_code}-{year}-%"]
                },
                pluck="batch_id"
            )

            # Extract sequence numbers and find max
            sequence_numbers = []
            for batch in existing_batches:
                try:
                    seq = int(batch.split("-")[-1])
                    sequence_numbers.append(seq)
                except (ValueError, IndexError):
                    pass

            next_seq = max(sequence_numbers, default=0) + 1
            self.batch_id = f"{product_code}-{year}-{next_seq:04d}"

    def validate(self):
        """Validate batch data before saving."""
        self.validate_dates()
        self.calculate_shelf_life()
        self.update_status()

    def before_save(self):
        """Set default values before saving."""
        if not self.status:
            self.status = "Active"

    def validate_dates(self):
        """Ensure expiration date is after manufacturing date."""
        if self.manufacturing_date and self.expiration_date:
            if getdate(self.expiration_date) <= getdate(self.manufacturing_date):
                frappe.throw(
                    _("Expiration date must be after manufacturing date")
                )

    def calculate_shelf_life(self):
        """Calculate shelf life in days if both dates are provided."""
        if self.manufacturing_date and self.expiration_date and not self.shelf_life_in_days:
            mfg_date = getdate(self.manufacturing_date)
            exp_date = getdate(self.expiration_date)
            self.shelf_life_in_days = (exp_date - mfg_date).days

    def update_status(self):
        """
        Auto-update status based on expiration date and quantity.

        - Expired: expiration_date has passed
        - Consumed: quantity is 0 or negative
        - Active: otherwise
        """
        if self.expiration_date and getdate(self.expiration_date) < getdate(today()):
            self.status = "Expired"
        elif self.quantity is not None and self.quantity <= 0:
            self.status = "Consumed"
        elif self.status == "Expired" or self.status == "Consumed":
            # Don't automatically revert to Active - manual override needed
            pass
        else:
            self.status = "Active"

    def update_quantity_from_ledger(self):
        """
        Recalculate quantity from Stock Ledger Entries.

        This should be called whenever a Stock Ledger Entry is created
        or cancelled for this batch.
        """
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

        # Update status based on new quantity
        self.update_status()
        self.db_set("status", self.status, update_modified=False)


# Scheduled task to update batch statuses daily
def update_batch_statuses():
    """
    Daily scheduled job to mark expired batches.

    Scans all Active batches and updates status to Expired if
    expiration_date has passed.
    """
    expired_batches = frappe.get_all(
        "Batch Number",
        filters={
            "status": "Active",
            "expiration_date": ["<", today()]
        },
        pluck="name"
    )

    for batch_name in expired_batches:
        batch = frappe.get_doc("Batch Number", batch_name)
        batch.status = "Expired"
        batch.db_set("status", "Expired")
        frappe.db.commit()

    if expired_batches:
        frappe.logger().info(f"Marked {len(expired_batches)} batches as Expired")


# Query functions for batch management

def get_batch_balance(batch_id):
    """
    Get current quantity for a specific batch.

    Args:
        batch_id (str): Batch Number name

    Returns:
        float: Current batch quantity
    """
    if not batch_id:
        return 0

    return frappe.db.get_value("Batch Number", batch_id, "quantity") or 0


def get_expiring_batches(department=None, company=None, within_days=30):
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
        "expiration_date": ["<=", add_days(today(), within_days)],
        "expiration_date": [">=", today()],
        "quantity": [">", 0]
    }

    if department:
        filters["department"] = department
    if company:
        filters["company"] = company

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


def get_available_batches(product, department, company):
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
            "product": product,
            "department": department,
            "company": company,
            "status": "Active",
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
