# Copyright (c) 2025, BLKSHP and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import get_datetime, now_datetime


class StockLedgerEntry(Document):
    """
    Immutable transaction log for all inventory movements.

    Each entry records a single inventory transaction with:
    - Quantity change (actual_qty)
    - Running balance (qty_after_transaction)
    - Valuation information (rates and values)
    - Source document reference (voucher_type, voucher_no)
    """

    def before_insert(self):
        """Set computed fields before inserting the document."""
        self.set_posting_datetime()
        self.set_item_code_and_uom()
        self.set_warehouse_from_department()

    def before_submit(self):
        """Calculate running balance and valuation before submission."""
        self.validate_product_and_department()
        self.validate_no_backdated_entries()
        self.calculate_qty_after_transaction()
        # Valuation calculation will be added in BLK-44

    def on_submit(self):
        """Update inventory balance after submission."""
        self.update_inventory_balance()

    def on_cancel(self):
        """Mark as cancelled and update inventory balance."""
        self.validate_no_future_entries()
        self.db_set("is_cancelled", 1)
        self.update_inventory_balance(reverse=True)

    def validate(self):
        """Validate the stock ledger entry."""
        # Prevent modification after submission
        if self.docstatus == 1 and self.has_value_changed("actual_qty"):
            frappe.throw(
                _("Cannot modify Stock Ledger Entry after submission. Entry is immutable.")
            )

        # Update computed fields on every save (in case department changes)
        self.set_posting_datetime()
        self.set_item_code_and_uom()
        self.set_warehouse_from_department()

    def set_posting_datetime(self):
        """Combine posting_date and posting_time into posting_datetime."""
        if not self.posting_date:
            self.posting_date = frappe.utils.today()
        if not self.posting_time:
            self.posting_time = frappe.utils.nowtime()

        posting_datetime = get_datetime(f"{self.posting_date} {self.posting_time}")
        self.posting_datetime = posting_datetime

    def set_item_code_and_uom(self):
        """Set item_code and stock_uom from Product."""
        if self.product:
            product = frappe.get_doc("Product", self.product)
            self.item_code = product.product_code
            self.stock_uom = product.primary_count_unit

    def set_warehouse_from_department(self):
        """Set warehouse field to department name for ERPNext compatibility."""
        if self.department and not self.warehouse:
            self.warehouse = self.department

    def validate_product_and_department(self):
        """Validate that product and department exist and are active."""
        if not frappe.db.exists("Product", self.product):
            frappe.throw(_("Product {0} does not exist").format(self.product))

        if not frappe.db.exists("Department", self.department):
            frappe.throw(_("Department {0} does not exist").format(self.department))

    def validate_no_backdated_entries(self):
        """
        Prevent backdated entries that would corrupt the running balance.

        Validates that this entry's posting_datetime is not earlier than
        any existing entries for the same product/department combination.
        """
        if self.is_new():
            # Check if there are any future entries
            future_entries = frappe.db.count(
                "Stock Ledger Entry",
                filters={
                    "product": self.product,
                    "department": self.department,
                    "company": self.company,
                    "docstatus": 1,
                    "is_cancelled": 0,
                    "posting_datetime": [">", self.posting_datetime],
                },
            )

            if future_entries > 0:
                frappe.throw(
                    _(
                        "Cannot create backdated entry. There are {0} future entries for {1} in {2}. "
                        "Backdated entries would corrupt the running balance."
                    ).format(future_entries, self.product, self.department)
                )

    def validate_no_future_entries(self):
        """
        Prevent cancellation of entries when subsequent entries exist.

        Validates that no entries exist with posting_datetime after this entry.
        Canceling middle entries would leave subsequent balances incorrect.
        """
        future_entries = frappe.db.sql(
            """
            SELECT name, posting_datetime
            FROM `tabStock Ledger Entry`
            WHERE product = %(product)s
                AND department = %(department)s
                AND company = %(company)s
                AND docstatus = 1
                AND is_cancelled = 0
                AND posting_datetime > %(posting_datetime)s
            ORDER BY posting_datetime ASC
            LIMIT 1
            """,
            {
                "product": self.product,
                "department": self.department,
                "company": self.company,
                "posting_datetime": self.posting_datetime,
            },
            as_dict=1,
        )

        if future_entries:
            frappe.throw(
                _(
                    "Cannot cancel this entry. There are subsequent entries starting from {0}. "
                    "Canceling this entry would corrupt running balances. "
                    "Please cancel all subsequent entries first, or contact your system administrator."
                ).format(future_entries[0].posting_datetime)
            )

    def calculate_qty_after_transaction(self):
        """
        Calculate running balance by getting the previous balance and adding actual_qty.

        This is the core of the ledger system - maintaining an accurate running balance
        for each product/department combination.
        """
        # Get the previous balance from the most recent ledger entry
        previous_balance = self.get_previous_balance()

        # Calculate new balance
        self.qty_after_transaction = previous_balance + self.actual_qty

    def get_previous_balance(self):
        """
        Get the most recent qty_after_transaction for this product/department.

        Returns 0 if no previous entries exist.
        """
        filters = {
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "docstatus": 1,  # Only submitted entries
            "is_cancelled": 0,  # Exclude cancelled entries
            "posting_datetime": ["<", self.posting_datetime],
        }

        # Get the most recent entry before this one
        # Secondary sort by creation to handle entries with same posting_datetime
        previous_entry = frappe.get_all(
            "Stock Ledger Entry",
            filters=filters,
            fields=["qty_after_transaction"],
            order_by="posting_datetime desc, creation desc",
            limit=1,
        )

        if previous_entry:
            return previous_entry[0].qty_after_transaction
        else:
            # No previous entries, check Inventory Balance for starting point
            return self.get_inventory_balance_qty()

    def get_inventory_balance_qty(self):
        """
        Get current quantity from Inventory Balance.

        This serves as the starting point if no previous ledger entries exist.
        """
        balance_name = f"{self.product}-{self.department}-{self.company}"

        if frappe.db.exists("Inventory Balance", balance_name):
            return frappe.db.get_value("Inventory Balance", balance_name, "quantity") or 0
        return 0

    def update_inventory_balance(self, reverse=False):
        """
        Update the Inventory Balance document with the new running balance.

        Uses database-level locking to prevent concurrent update race conditions.

        Args:
            reverse (bool): If True, subtract instead of using the new balance (for cancellation)
        """
        balance_name = f"{self.product}-{self.department}-{self.company}"

        # Use SELECT FOR UPDATE to lock the row during update
        # This prevents concurrent transactions from corrupting the balance
        frappe.db.sql(
            """
            SELECT name FROM `tabInventory Balance`
            WHERE name = %s
            FOR UPDATE
            """,
            balance_name,
        )

        if frappe.db.exists("Inventory Balance", balance_name):
            balance_doc = frappe.get_doc("Inventory Balance", balance_name)
        else:
            # Create new Inventory Balance if it doesn't exist
            balance_doc = frappe.new_doc("Inventory Balance")
            balance_doc.product = self.product
            balance_doc.department = self.department
            balance_doc.company = self.company

        if reverse:
            # On cancellation, subtract the actual_qty
            balance_doc.quantity = (balance_doc.quantity or 0) - self.actual_qty
        else:
            # On submission, set to the calculated balance
            balance_doc.quantity = self.qty_after_transaction

        balance_doc.last_updated = now_datetime()

        # Update last_audit_date if this entry is from an Inventory Audit
        if self.voucher_type == "Inventory Audit" and not reverse:
            balance_doc.last_audit_date = self.posting_date

        balance_doc.save(ignore_permissions=True)


# Query functions for external use

def get_stock_balance(product, department, company, as_of_date=None):
    """
    Get stock balance for a product/department as of a specific date.

    Args:
        product (str): Product name
        department (str): Department name
        company (str): Company name
        as_of_date (datetime, optional): Date to calculate balance. Defaults to now.

    Returns:
        float: Stock balance quantity
    """
    filters = {
        "product": product,
        "department": department,
        "company": company,
        "docstatus": 1,
        "is_cancelled": 0,
    }

    if as_of_date:
        filters["posting_datetime"] = ["<=", as_of_date]

    # Get the most recent entry
    # Secondary sort by creation to handle entries with same posting_datetime
    entry = frappe.get_all(
        "Stock Ledger Entry",
        filters=filters,
        fields=["qty_after_transaction"],
        order_by="posting_datetime desc, creation desc",
        limit=1,
    )

    return entry[0].qty_after_transaction if entry else 0


def get_stock_value(product, department, company, as_of_date=None):
    """
    Get stock value for a product/department as of a specific date.

    Args:
        product (str): Product name
        department (str): Department name
        company (str): Company name
        as_of_date (datetime, optional): Date to calculate value. Defaults to now.

    Returns:
        float: Stock value in currency
    """
    filters = {
        "product": product,
        "department": department,
        "company": company,
        "docstatus": 1,
        "is_cancelled": 0,
    }

    if as_of_date:
        filters["posting_datetime"] = ["<=", as_of_date]

    # Get the most recent entry
    # Secondary sort by creation to handle entries with same posting_datetime
    entry = frappe.get_all(
        "Stock Ledger Entry",
        filters=filters,
        fields=["stock_value"],
        order_by="posting_datetime desc, creation desc",
        limit=1,
    )

    return entry[0].stock_value if entry else 0


def get_stock_movements(product, department, company, from_date, to_date):
    """
    Get all stock movements for a product/department in a date range.

    Args:
        product (str): Product name
        department (str): Department name
        company (str): Company name
        from_date (datetime): Start date
        to_date (datetime): End date

    Returns:
        list: List of stock ledger entries
    """
    filters = {
        "product": product,
        "department": department,
        "company": company,
        "docstatus": 1,
        "is_cancelled": 0,
        "posting_datetime": ["between", [from_date, to_date]],
    }

    return frappe.get_all(
        "Stock Ledger Entry",
        filters=filters,
        fields=[
            "name",
            "posting_datetime",
            "actual_qty",
            "qty_after_transaction",
            "valuation_rate",
            "stock_value",
            "voucher_type",
            "voucher_no",
        ],
        order_by="posting_datetime asc",
    )
