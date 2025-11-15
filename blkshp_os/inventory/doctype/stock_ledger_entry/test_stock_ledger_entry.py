# Copyright (c) 2025, BLKSHP and Contributors
# See license.txt

import frappe
import unittest
from frappe.utils import now_datetime, add_to_date, get_datetime


class TestStockLedgerEntry(unittest.TestCase):
    """Test cases for Stock Ledger Entry DocType."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are used by multiple tests."""
        # Create test company
        if not frappe.db.exists("Company", "Test Company"):
            company = frappe.new_doc("Company")
            company.company_name = "Test Company"
            company.abbr = "TC"
            company.default_currency = "USD"
            company.insert(ignore_if_duplicate=True)

        # Create test department
        if not frappe.db.exists("Department", "Test Kitchen"):
            dept = frappe.new_doc("Department")
            dept.department_name = "Test Kitchen"
            dept.company = "Test Company"
            dept.insert(ignore_if_duplicate=True)

        # Create test product
        if not frappe.db.exists("Product", "TEST-TOMATO"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-TOMATO"
            product.product_name = "Test Tomatoes"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.insert(ignore_if_duplicate=True)

        frappe.db.commit()

    def tearDown(self):
        """Clean up after each test."""
        # Delete test stock ledger entries
        frappe.db.delete("Stock Ledger Entry", {
            "product": "TEST-TOMATO",
            "department": "Test Kitchen"
        })

        # Reset inventory balance
        balance_name = "TEST-TOMATO-Test Kitchen-Test Company"
        if frappe.db.exists("Inventory Balance", balance_name):
            frappe.db.set_value("Inventory Balance", balance_name, "quantity", 0)

        frappe.db.commit()

    def test_create_stock_ledger_entry(self):
        """Test basic creation of stock ledger entry."""
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-TOMATO"
        entry.department = "Test Kitchen"
        entry.company = "Test Company"
        entry.actual_qty = 10
        entry.posting_date = frappe.utils.today()
        entry.posting_time = frappe.utils.nowtime()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-001"
        entry.insert()

        self.assertEqual(entry.product, "TEST-TOMATO")
        self.assertEqual(entry.actual_qty, 10)
        self.assertIsNotNone(entry.posting_datetime)

    def test_auto_set_item_code_and_uom(self):
        """Test automatic setting of item_code and stock_uom from Product."""
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-TOMATO"
        entry.department = "Test Kitchen"
        entry.company = "Test Company"
        entry.actual_qty = 5
        entry.posting_date = frappe.utils.today()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-002"
        entry.insert()

        self.assertEqual(entry.item_code, "TEST-TOMATO")
        self.assertEqual(entry.stock_uom, "lb")

    def test_auto_set_posting_datetime(self):
        """Test automatic setting of posting_datetime from date and time."""
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-TOMATO"
        entry.department = "Test Kitchen"
        entry.company = "Test Company"
        entry.actual_qty = 5
        entry.posting_date = "2025-11-15"
        entry.posting_time = "10:30:00"
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-003"
        entry.insert()

        expected_datetime = get_datetime("2025-11-15 10:30:00")
        self.assertEqual(entry.posting_datetime, expected_datetime)

    def test_running_balance_calculation(self):
        """Test running balance calculation across multiple entries."""
        # Entry 1: +10 (balance should be 10)
        entry1 = self.create_test_entry(actual_qty=10, posting_time="10:00:00")
        entry1.submit()

        self.assertEqual(entry1.qty_after_transaction, 10)

        # Entry 2: +5 (balance should be 15)
        entry2 = self.create_test_entry(actual_qty=5, posting_time="11:00:00")
        entry2.submit()

        self.assertEqual(entry2.qty_after_transaction, 15)

        # Entry 3: -3 (balance should be 12)
        entry3 = self.create_test_entry(actual_qty=-3, posting_time="12:00:00")
        entry3.submit()

        self.assertEqual(entry3.qty_after_transaction, 12)

    def test_inventory_balance_update(self):
        """Test that Inventory Balance is updated after entry submission."""
        balance_name = "TEST-TOMATO-Test Kitchen-Test Company"

        # Create and submit entry
        entry = self.create_test_entry(actual_qty=20)
        entry.submit()

        # Check Inventory Balance
        self.assertTrue(frappe.db.exists("Inventory Balance", balance_name))
        balance_qty = frappe.db.get_value("Inventory Balance", balance_name, "quantity")
        self.assertEqual(balance_qty, 20)

    def test_immutability_after_submit(self):
        """Test that entry cannot be modified after submission."""
        entry = self.create_test_entry(actual_qty=10)
        entry.submit()

        # Try to modify actual_qty
        entry.actual_qty = 15

        with self.assertRaises(frappe.ValidationError):
            entry.save()

    def test_cancellation(self):
        """Test entry cancellation and balance reversal."""
        # Create and submit entry
        entry = self.create_test_entry(actual_qty=10)
        entry.submit()

        self.assertEqual(entry.qty_after_transaction, 10)

        # Cancel entry
        entry.cancel()

        self.assertEqual(entry.is_cancelled, 1)

        # Check that balance was reversed
        balance_name = "TEST-TOMATO-Test Kitchen-Test Company"
        balance_qty = frappe.db.get_value("Inventory Balance", balance_name, "quantity")
        self.assertEqual(balance_qty, 0)

    def test_get_stock_balance_function(self):
        """Test get_stock_balance query function."""
        from blkshp_os.inventory.doctype.stock_ledger_entry.stock_ledger_entry import (
            get_stock_balance,
        )

        # Create multiple entries
        entry1 = self.create_test_entry(actual_qty=10, posting_time="10:00:00")
        entry1.submit()

        entry2 = self.create_test_entry(actual_qty=5, posting_time="11:00:00")
        entry2.submit()

        # Get current balance
        balance = get_stock_balance("TEST-TOMATO", "Test Kitchen", "Test Company")
        self.assertEqual(balance, 15)

    def test_get_stock_balance_as_of_date(self):
        """Test get_stock_balance with as_of_date parameter."""
        from blkshp_os.inventory.doctype.stock_ledger_entry.stock_ledger_entry import (
            get_stock_balance,
        )

        # Create entries on different dates
        entry1 = self.create_test_entry(
            actual_qty=10,
            posting_date="2025-11-10",
            posting_time="10:00:00"
        )
        entry1.submit()

        entry2 = self.create_test_entry(
            actual_qty=5,
            posting_date="2025-11-15",
            posting_time="10:00:00"
        )
        entry2.submit()

        # Get balance as of 2025-11-12 (should only include entry1)
        balance = get_stock_balance(
            "TEST-TOMATO",
            "Test Kitchen",
            "Test Company",
            as_of_date=get_datetime("2025-11-12 23:59:59")
        )
        self.assertEqual(balance, 10)

        # Get balance as of 2025-11-16 (should include both)
        balance = get_stock_balance(
            "TEST-TOMATO",
            "Test Kitchen",
            "Test Company",
            as_of_date=get_datetime("2025-11-16 23:59:59")
        )
        self.assertEqual(balance, 15)

    def test_get_stock_movements_function(self):
        """Test get_stock_movements query function."""
        from blkshp_os.inventory.doctype.stock_ledger_entry.stock_ledger_entry import (
            get_stock_movements,
        )

        # Create entries
        entry1 = self.create_test_entry(
            actual_qty=10,
            posting_date="2025-11-10",
            voucher_no="AUDIT-001"
        )
        entry1.submit()

        entry2 = self.create_test_entry(
            actual_qty=5,
            posting_date="2025-11-15",
            voucher_no="AUDIT-002"
        )
        entry2.submit()

        # Get movements in date range
        movements = get_stock_movements(
            "TEST-TOMATO",
            "Test Kitchen",
            "Test Company",
            get_datetime("2025-11-01"),
            get_datetime("2025-11-20")
        )

        self.assertEqual(len(movements), 2)
        self.assertEqual(movements[0].actual_qty, 10)
        self.assertEqual(movements[1].actual_qty, 5)

    def test_negative_stock(self):
        """Test that negative stock is allowed (configurable in future)."""
        # Create entry with -10 when balance is 0
        entry = self.create_test_entry(actual_qty=-10)
        entry.submit()

        self.assertEqual(entry.qty_after_transaction, -10)

    def test_zero_quantity_entry(self):
        """Test entry with zero quantity (edge case)."""
        entry = self.create_test_entry(actual_qty=0)
        entry.submit()

        self.assertEqual(entry.qty_after_transaction, 0)

    def test_multiple_products_same_department(self):
        """Test that balances are tracked separately per product."""
        # Create another test product
        if not frappe.db.exists("Product", "TEST-ONION"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-ONION"
            product.product_name = "Test Onions"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.insert()

        # Create entries for different products
        tomato_entry = self.create_test_entry(actual_qty=10, product="TEST-TOMATO")
        tomato_entry.submit()

        onion_entry = self.create_test_entry(actual_qty=5, product="TEST-ONION")
        onion_entry.submit()

        # Verify separate balances
        self.assertEqual(tomato_entry.qty_after_transaction, 10)
        self.assertEqual(onion_entry.qty_after_transaction, 5)

        # Cleanup
        frappe.db.delete("Stock Ledger Entry", {"product": "TEST-ONION"})
        frappe.delete_doc("Product", "TEST-ONION", force=True)

    # Helper methods

    def create_test_entry(
        self,
        actual_qty,
        product="TEST-TOMATO",
        department="Test Kitchen",
        posting_date=None,
        posting_time=None,
        voucher_no=None
    ):
        """Create a test stock ledger entry without submitting it."""
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = product
        entry.department = department
        entry.company = "Test Company"
        entry.actual_qty = actual_qty
        entry.posting_date = posting_date or frappe.utils.today()
        entry.posting_time = posting_time or frappe.utils.nowtime()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = voucher_no or f"TEST-AUDIT-{frappe.generate_hash(length=8)}"
        entry.insert()
        return entry
