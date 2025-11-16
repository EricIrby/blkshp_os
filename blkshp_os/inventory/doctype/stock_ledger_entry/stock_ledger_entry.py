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
        self.validate_batch()
        self.calculate_qty_after_transaction()
        # Valuation calculation will be added in BLK-44

    def on_submit(self):
        """Update inventory balance and batch quantity after submission."""
        self.update_inventory_balance()
        self.update_batch_quantity()

    def on_cancel(self):
        """Mark as cancelled and update inventory balance and batch quantity."""
        self.db_set("is_cancelled", 1)
        self.update_inventory_balance(reverse=True)
        self.update_batch_quantity()

    def validate(self):
        """Validate the stock ledger entry."""
        # Prevent modification after submission
        if self.docstatus == 1 and self.has_value_changed("actual_qty"):
            frappe.throw(
                _("Cannot modify Stock Ledger Entry after submission. Entry is immutable.")
            )

    def set_posting_datetime(self):
        """Combine posting_date and posting_time into posting_datetime."""
        if not self.posting_date:
            self.posting_date = frappe.utils.today()
        if not self.posting_time:
            self.posting_time = frappe.utils.nowtime()

        posting_datetime = get_datetime(f"{self.posting_date} {self.posting_time}")
        self.posting_datetime = posting_datetime

    def set_item_code_and_uom(self):
        """
        Populate the entry's item_code and stock_uom from the linked Product when appropriate.

        Sets item_code to the Product's product_code and stock_uom to the Product's primary_count_unit
        if this entry has a product specified and item_code is not already set.
        """
        if self.product and not self.item_code:
            result = frappe.db.get_value(
                "Product",
                self.product,
                ["product_code", "primary_count_unit"]
            )
            if not result:
                frappe.throw(_("Product {0} does not exist").format(self.product))
            product_code, primary_unit = result
            self.item_code = product_code
            self.stock_uom = primary_unit

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

    def validate_batch(self):
        """
        Validate batch number requirements.

        If product.has_batch_no = 1, batch_number is required.
        Also validates that batch matches product and department.
        """
        # Check if product requires batch tracking
        has_batch = frappe.db.get_value("Product", self.product, "has_batch_no")

        if has_batch and not self.batch_number:
            frappe.throw(
                _("Batch Number is required for Product {0}").format(self.product)
            )

        # If batch is provided, validate it matches product/department
        if self.batch_number:
            batch = frappe.get_doc("Batch Number", self.batch_number)

            if batch.product != self.product:
                frappe.throw(
                    _("Batch {0} is for Product {1}, not {2}").format(
                        self.batch_number, batch.product, self.product
                    )
                )

            if batch.department != self.department:
                frappe.throw(
                    _("Batch {0} is for Department {1}, not {2}").format(
                        self.batch_number, batch.department, self.department
                    )
                )

            if batch.company != self.company:
                frappe.throw(
                    _("Batch {0} is for Company {1}, not {2}").format(
                        self.batch_number, batch.company, self.company
                    )
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
        previous_entry = frappe.get_all(
            "Stock Ledger Entry",
            filters=filters,
            fields=["qty_after_transaction"],
            order_by="posting_datetime desc",
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

        Args:
            reverse (bool): If True, subtract instead of using the new balance (for cancellation)
        """
        balance_name = f"{self.product}-{self.department}-{self.company}"

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

    def update_batch_quantity(self):
        """
        Update the Batch Number quantity from Stock Ledger Entries.

        Recalculates the batch quantity by summing all Stock Ledger Entries
        for this batch. Called on submit and cancel to keep batch quantities accurate.
        """
        if not self.batch_number:
            return

        # Get the batch document
        batch = frappe.get_doc("Batch Number", self.batch_number)

        # Recalculate quantity from ledger
        batch.update_quantity_from_ledger()


# Query functions for external use

def _validate_stock_query_params(product, department, company):
    """Validate common parameters for stock query functions."""
    # Validate required parameters
    if not product:
        frappe.throw(_("Product is required"))
    if not department:
        frappe.throw(_("Department is required"))
    if not company:
        frappe.throw(_("Company is required"))

    # Validate entities exist
    if not frappe.db.exists("Product", product):
        frappe.throw(_("Product {0} does not exist").format(product))
    if not frappe.db.exists("Department", department):
        frappe.throw(_("Department {0} does not exist").format(department))
    if not frappe.db.exists("Company", company):
        frappe.throw(_("Company {0} does not exist").format(company))


def get_stock_balance(product, department, company, as_of_date=None):
    """
    Return the stock quantity for a product in a department and company as of a given date.

    If `as_of_date` is provided, the result reflects the most recent submitted, non-cancelled
    ledger entry with `posting_datetime` <= `as_of_date`; otherwise it uses the latest submitted,
    non-cancelled entry. Returns 0 if no matching entries exist.

    Parameters:
        product (str): Product identifier.
        department (str): Department identifier.
        company (str): Company identifier.
        as_of_date (datetime, optional): Cutoff datetime to calculate the balance; when omitted,
            the latest entry is used.

    Returns:
        float: Stock balance quantity as of the specified date.

    Raises:
        ValidationError: If `product`, `department`, or `company` is missing or does not exist.
    """
    _validate_stock_query_params(product, department, company)

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
    entry = frappe.get_all(
        "Stock Ledger Entry",
        filters=filters,
        fields=["qty_after_transaction"],
        order_by="posting_datetime desc",
        limit=1,
    )

    return entry[0].qty_after_transaction if entry else 0


def get_stock_value(product, department, company, as_of_date=None):
    """
    Return the stock monetary value of a product in a department for a company as of a given datetime.

    Parameters:
        product (str): Product identifier.
        department (str): Department identifier.
        company (str): Company identifier.
        as_of_date (datetime, optional): Include ledger entries with posting_datetime <= this value.
            If omitted, uses the current time.

    Returns:
        float: Stock value in company currency; `0` when no matching ledger entry exists.

    Raises:
        ValidationError: If `product`, `department`, or `company` is missing or does not exist.
    """
    _validate_stock_query_params(product, department, company)

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
    entry = frappe.get_all(
        "Stock Ledger Entry",
        filters=filters,
        fields=["stock_value"],
        order_by="posting_datetime desc",
        limit=1,
    )

    return entry[0].stock_value if entry else 0


def get_stock_movements(product, department, company, from_date, to_date):
    """
    Return stock ledger entries for a product and department between two datetimes.

    Parameters:
        product (str): Product identifier.
        department (str): Department identifier.
        company (str): Company identifier.
        from_date (datetime): Start of the date/time range (inclusive).
        to_date (datetime): End of the date/time range (inclusive).

    Returns:
        list[dict]: Ordered list of stock ledger entry records with keys:
            - name (str)
            - posting_datetime (datetime)
            - actual_qty (float)
            - qty_after_transaction (float)
            - valuation_rate (float)
            - stock_value (float)
            - voucher_type (str)
            - voucher_no (str)

    Raises:
        ValidationError: If required parameters are missing, entities don't exist,
            or `from_date` is after `to_date`.
    """
    _validate_stock_query_params(product, department, company)

    # Validate date parameters
    if not from_date:
        frappe.throw(_("From date is required"))
    if not to_date:
        frappe.throw(_("To date is required"))

    # Validate date range
    if get_datetime(from_date) > get_datetime(to_date):
        frappe.throw(_("From date cannot be after To date"))

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


# Batch-specific query functions

def get_stock_balance_by_batch(product, department, company, batch_number=None, as_of_date=None):
    """
    Get stock balance for a specific batch.

    Args:
        product (str): Product name
        department (str): Department name
        company (str): Company name
        batch_number (str, optional): Specific batch to query. If None, returns all batches.
        as_of_date (datetime, optional): Date to calculate balance. Defaults to now.

    Returns:
        dict or float: If batch_number specified, returns float quantity.
                      If batch_number is None, returns dict of {batch: quantity}
    """
    _validate_stock_query_params(product, department, company)

    filters = {
        "product": product,
        "department": department,
        "company": company,
        "docstatus": 1,
        "is_cancelled": 0,
    }

    if batch_number:
        filters["batch_number"] = batch_number

    if as_of_date:
        filters["posting_datetime"] = ["<=", as_of_date]

    # Use SQL aggregation for better performance
    entries = frappe.get_all(
        "Stock Ledger Entry",
        filters=filters,
        fields=["batch_number", "SUM(actual_qty) as qty"],
        group_by="batch_number"
    )

    if batch_number:
        # Return single batch quantity
        return entries[0].qty if entries else 0
    else:
        # Return dict of all batches with quantities
        return {e.batch_number: e.qty for e in entries if e.batch_number}


def get_batch_movements(batch_number, from_date=None, to_date=None):
    """
    Get all stock movements for a specific batch.

    Args:
        batch_number (str): Batch Number name
        from_date (datetime, optional): Start date
        to_date (datetime, optional): End date

    Returns:
        list: List of stock ledger entries for the batch
    """
    if not batch_number:
        frappe.throw(_("Batch Number is required"))

    if not frappe.db.exists("Batch Number", batch_number):
        frappe.throw(_("Batch Number {0} does not exist").format(batch_number))

    filters = {
        "batch_number": batch_number,
        "docstatus": 1,
        "is_cancelled": 0,
    }

    if from_date and to_date:
        if get_datetime(from_date) > get_datetime(to_date):
            frappe.throw(_("From date cannot be after To date"))
        filters["posting_datetime"] = ["between", [from_date, to_date]]
    elif from_date:
        filters["posting_datetime"] = [">=", from_date]
    elif to_date:
        filters["posting_datetime"] = ["<=", to_date]

    return frappe.get_all(
        "Stock Ledger Entry",
        filters=filters,
        fields=[
            "name",
            "posting_datetime",
            "product",
            "department",
            "company",
            "actual_qty",
            "qty_after_transaction",
            "valuation_rate",
            "voucher_type",
            "voucher_no",
        ],
        order_by="posting_datetime asc",
    )
