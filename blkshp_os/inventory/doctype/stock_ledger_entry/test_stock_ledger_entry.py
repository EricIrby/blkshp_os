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

    def test_batch_required_validation(self):
        """Test that batch is required when product.has_batch_no = 1."""
        # Create product with batch tracking
        if not frappe.db.exists("Product", "TEST-BATCH-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-PRODUCT"
            product.product_name = "Test Batch Product"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.has_batch_no = 1
            product.insert()

        # Try to create entry without batch - should fail
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-BATCH-PRODUCT"
        entry.department = "Test Kitchen"
        entry.company = "Test Company"
        entry.actual_qty = 10
        entry.posting_date = frappe.utils.today()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-BATCH-001"
        entry.insert()

        with self.assertRaises(frappe.ValidationError) as context:
            entry.submit()

        self.assertIn("Batch Number is required", str(context.exception))

        # Cleanup
        frappe.delete_doc("Product", "TEST-BATCH-PRODUCT", force=True)

    def test_batch_matching_validation(self):
        """Test that batch must match product, department, and company."""
        # Create batch-tracked product
        if not frappe.db.exists("Product", "TEST-BATCH-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-PRODUCT"
            product.product_name = "Test Batch Product"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.has_batch_no = 1
            product.insert()

        # Create batch
        if not frappe.db.exists("Batch Number", "TEST-BATCH-001"):
            batch = frappe.new_doc("Batch Number")
            batch.product = "TEST-BATCH-PRODUCT"
            batch.department = "Test Kitchen"
            batch.company = "Test Company"
            batch.manufacturing_date = frappe.utils.today()
            batch.expiration_date = frappe.utils.add_days(frappe.utils.today(), 30)
            batch.insert()

        # Try to use batch with wrong product
        if not frappe.db.exists("Product", "TEST-WRONG-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-WRONG-PRODUCT"
            product.product_name = "Wrong Product"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.has_batch_no = 1
            product.insert()

        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-WRONG-PRODUCT"
        entry.department = "Test Kitchen"
        entry.company = "Test Company"
        entry.batch_number = "TEST-BATCH-001"
        entry.actual_qty = 10
        entry.posting_date = frappe.utils.today()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-BATCH-002"
        entry.insert()

        with self.assertRaises(frappe.ValidationError) as context:
            entry.submit()

        self.assertIn("Batch", str(context.exception))

        # Cleanup
        frappe.delete_doc("Batch Number", "TEST-BATCH-001", force=True)
        frappe.delete_doc("Product", "TEST-BATCH-PRODUCT", force=True)
        frappe.delete_doc("Product", "TEST-WRONG-PRODUCT", force=True)

    def test_batch_quantity_update_on_submit(self):
        """Test that batch quantity is updated when entry is submitted."""
        # Create batch-tracked product
        if not frappe.db.exists("Product", "TEST-BATCH-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-PRODUCT"
            product.product_name = "Test Batch Product"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.has_batch_no = 1
            product.insert()

        # Create batch
        batch = frappe.new_doc("Batch Number")
        batch.product = "TEST-BATCH-PRODUCT"
        batch.department = "Test Kitchen"
        batch.company = "Test Company"
        batch.manufacturing_date = frappe.utils.today()
        batch.expiration_date = frappe.utils.add_days(frappe.utils.today(), 30)
        batch.insert()
        batch_name = batch.name

        # Create entry with batch
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-BATCH-PRODUCT"
        entry.department = "Test Kitchen"
        entry.company = "Test Company"
        entry.batch_number = batch_name
        entry.actual_qty = 10
        entry.posting_date = frappe.utils.today()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-BATCH-003"
        entry.insert()
        entry.submit()

        # Check batch quantity was updated
        batch.reload()
        self.assertEqual(batch.quantity, 10)

        # Cleanup
        entry.cancel()
        frappe.delete_doc("Batch Number", batch_name, force=True)
        frappe.delete_doc("Product", "TEST-BATCH-PRODUCT", force=True)

    def test_batch_quantity_update_on_cancel(self):
        """Test that batch quantity is updated when entry is cancelled."""
        # Create batch-tracked product
        if not frappe.db.exists("Product", "TEST-BATCH-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-PRODUCT"
            product.product_name = "Test Batch Product"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.has_batch_no = 1
            product.insert()

        # Create batch
        batch = frappe.new_doc("Batch Number")
        batch.product = "TEST-BATCH-PRODUCT"
        batch.department = "Test Kitchen"
        batch.company = "Test Company"
        batch.manufacturing_date = frappe.utils.today()
        batch.expiration_date = frappe.utils.add_days(frappe.utils.today(), 30)
        batch.insert()
        batch_name = batch.name

        # Create and submit entry
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-BATCH-PRODUCT"
        entry.department = "Test Kitchen"
        entry.company = "Test Company"
        entry.batch_number = batch_name
        entry.actual_qty = 10
        entry.posting_date = frappe.utils.today()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-BATCH-004"
        entry.insert()
        entry.submit()

        # Cancel entry
        entry.cancel()

        # Check batch quantity was updated (should be 0)
        batch.reload()
        self.assertEqual(batch.quantity, 0)

        # Cleanup
        frappe.delete_doc("Batch Number", batch_name, force=True)
        frappe.delete_doc("Product", "TEST-BATCH-PRODUCT", force=True)

    def test_get_stock_balance_by_batch(self):
        """Test get_stock_balance_by_batch query function."""
        from blkshp_os.inventory.doctype.stock_ledger_entry.stock_ledger_entry import (
            get_stock_balance_by_batch,
        )

        # Create batch-tracked product
        if not frappe.db.exists("Product", "TEST-BATCH-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-PRODUCT"
            product.product_name = "Test Batch Product"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.has_batch_no = 1
            product.insert()

        # Create two batches
        batch1 = frappe.new_doc("Batch Number")
        batch1.product = "TEST-BATCH-PRODUCT"
        batch1.department = "Test Kitchen"
        batch1.company = "Test Company"
        batch1.manufacturing_date = frappe.utils.today()
        batch1.expiration_date = frappe.utils.add_days(frappe.utils.today(), 30)
        batch1.insert()

        batch2 = frappe.new_doc("Batch Number")
        batch2.product = "TEST-BATCH-PRODUCT"
        batch2.department = "Test Kitchen"
        batch2.company = "Test Company"
        batch2.manufacturing_date = frappe.utils.today()
        batch2.expiration_date = frappe.utils.add_days(frappe.utils.today(), 30)
        batch2.insert()

        # Create entries for both batches
        entry1 = frappe.new_doc("Stock Ledger Entry")
        entry1.product = "TEST-BATCH-PRODUCT"
        entry1.department = "Test Kitchen"
        entry1.company = "Test Company"
        entry1.batch_number = batch1.name
        entry1.actual_qty = 10
        entry1.posting_date = frappe.utils.today()
        entry1.voucher_type = "Inventory Audit"
        entry1.voucher_no = "TEST-AUDIT-BATCH-005"
        entry1.insert()
        entry1.submit()

        entry2 = frappe.new_doc("Stock Ledger Entry")
        entry2.product = "TEST-BATCH-PRODUCT"
        entry2.department = "Test Kitchen"
        entry2.company = "Test Company"
        entry2.batch_number = batch2.name
        entry2.actual_qty = 5
        entry2.posting_date = frappe.utils.today()
        entry2.voucher_type = "Inventory Audit"
        entry2.voucher_no = "TEST-AUDIT-BATCH-006"
        entry2.insert()
        entry2.submit()

        # Test single batch query
        balance = get_stock_balance_by_batch(
            "TEST-BATCH-PRODUCT",
            "Test Kitchen",
            "Test Company",
            batch_number=batch1.name
        )
        self.assertEqual(balance, 10)

        # Test all batches query
        all_batches = get_stock_balance_by_batch(
            "TEST-BATCH-PRODUCT",
            "Test Kitchen",
            "Test Company"
        )
        self.assertEqual(all_batches[batch1.name], 10)
        self.assertEqual(all_batches[batch2.name], 5)

        # Cleanup
        entry1.cancel()
        entry2.cancel()
        frappe.delete_doc("Batch Number", batch1.name, force=True)
        frappe.delete_doc("Batch Number", batch2.name, force=True)
        frappe.delete_doc("Product", "TEST-BATCH-PRODUCT", force=True)

    def test_get_batch_movements(self):
        """Test get_batch_movements query function."""
        from blkshp_os.inventory.doctype.stock_ledger_entry.stock_ledger_entry import (
            get_batch_movements,
        )

        # Create batch-tracked product
        if not frappe.db.exists("Product", "TEST-BATCH-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-PRODUCT"
            product.product_name = "Test Batch Product"
            product.company = "Test Company"
            product.primary_count_unit = "lb"
            product.has_batch_no = 1
            product.insert()

        # Create batch
        batch = frappe.new_doc("Batch Number")
        batch.product = "TEST-BATCH-PRODUCT"
        batch.department = "Test Kitchen"
        batch.company = "Test Company"
        batch.manufacturing_date = frappe.utils.today()
        batch.expiration_date = frappe.utils.add_days(frappe.utils.today(), 30)
        batch.insert()

        # Create multiple entries
        entry1 = frappe.new_doc("Stock Ledger Entry")
        entry1.product = "TEST-BATCH-PRODUCT"
        entry1.department = "Test Kitchen"
        entry1.company = "Test Company"
        entry1.batch_number = batch.name
        entry1.actual_qty = 10
        entry1.posting_date = "2025-11-10"
        entry1.posting_time = "10:00:00"
        entry1.voucher_type = "Inventory Audit"
        entry1.voucher_no = "TEST-AUDIT-BATCH-007"
        entry1.insert()
        entry1.submit()

        entry2 = frappe.new_doc("Stock Ledger Entry")
        entry2.product = "TEST-BATCH-PRODUCT"
        entry2.department = "Test Kitchen"
        entry2.company = "Test Company"
        entry2.batch_number = batch.name
        entry2.actual_qty = -3
        entry2.posting_date = "2025-11-15"
        entry2.posting_time = "10:00:00"
        entry2.voucher_type = "Inventory Audit"
        entry2.voucher_no = "TEST-AUDIT-BATCH-008"
        entry2.insert()
        entry2.submit()

        # Get all movements
        movements = get_batch_movements(batch.name)
        self.assertEqual(len(movements), 2)
        self.assertEqual(movements[0].actual_qty, 10)
        self.assertEqual(movements[1].actual_qty, -3)

        # Get movements with date filter
        movements = get_batch_movements(
            batch.name,
            from_date=get_datetime("2025-11-12"),
            to_date=get_datetime("2025-11-20")
        )
        self.assertEqual(len(movements), 1)
        self.assertEqual(movements[0].actual_qty, -3)

        # Cleanup
        entry1.cancel()
        entry2.cancel()
        frappe.delete_doc("Batch Number", batch.name, force=True)
        frappe.delete_doc("Product", "TEST-BATCH-PRODUCT", force=True)

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
