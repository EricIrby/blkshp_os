# Copyright (c) 2025, BLKSHP and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today


class TestBatchNumber(FrappeTestCase):
    """Test cases for Batch Number DocType"""

    def setUp(self):
        """Set up test data before each test"""
        # Ensure test data exists
        self.company = self._ensure_company()
        self.product = self._ensure_product()
        self.department = self._ensure_department()

    def _ensure_company(self):
        """Helper to get or create test company."""
        existing_company = frappe.db.get_value(
            "Company", {"company_name": "_Test Company"}, "name"
        )
        if existing_company:
            return existing_company

        company = frappe.get_doc({
            "doctype": "Company",
            "company_name": "_Test Company",
            "company_code": "TEST",
            "default_currency": "USD"
        })
        company.insert(ignore_permissions=True)
        return company.name

    def _ensure_product(self):
        """Helper to get or create test product."""
        existing_product = frappe.db.get_value("Product", "TEST-BATCH-PROD", "name")
        if existing_product:
            return existing_product

        product = frappe.get_doc({
            "doctype": "Product",
            "product_name": "Test Batch Product",
            "product_code": "TEST-BATCH-PROD",
            "company": self.company,
            "primary_count_unit": "kg",
            "volume_conversion_unit": "",
            "weight_conversion_unit": ""
        })
        product.insert(ignore_permissions=True)
        return product.name

    def _ensure_department(self):
        """Helper to get or create test department."""
        existing_dept = frappe.db.get_value(
            "Department",
            {"department_code": "TEST-DEPT", "company": self.company},
            "name"
        )
        if existing_dept:
            return existing_dept

        dept = frappe.get_doc({
            "doctype": "Department",
            "department_name": "Test Batch Dept",
            "department_code": "TEST-DEPT",
            "department_type": "Food",
            "company": self.company
        })
        dept.insert(ignore_permissions=True)
        return dept.name

    def tearDown(self):
        """Clean up after each test"""
        # Delete test batches
        frappe.db.delete("Batch Number", {
            "product": self.product
        })
        frappe.db.commit()

    def test_batch_creation(self):
        """Test basic batch number creation"""
        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": today(),
            "expiration_date": add_days(today(), 30)
        })
        batch.insert()

        # Verify batch was created
        self.assertTrue(batch.name)
        self.assertTrue(batch.batch_id)
        self.assertEqual(batch.status, "Active")
        self.assertEqual(batch.shelf_life_in_days, 30)

    def test_auto_naming(self):
        """Test automatic batch_id generation"""
        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": today()
        })
        batch.insert()

        # Verify batch_id follows format: {product_code}-{YYYY}-{####}
        year = frappe.utils.getdate(today()).year
        self.assertTrue(batch.batch_id.startswith(f"TEST-BATCH-PROD-{year}-"))
        self.assertEqual(len(batch.batch_id.split("-")[-1]), 4)  # 4-digit sequence

    def test_date_validation(self):
        """Test that expiration date must be after manufacturing date"""
        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": today(),
            "expiration_date": add_days(today(), -1)  # Invalid: before manufacturing
        })

        # Should raise validation error
        with self.assertRaises(frappe.ValidationError):
            batch.insert()

    def test_shelf_life_calculation(self):
        """Test automatic shelf life calculation"""
        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": today(),
            "expiration_date": add_days(today(), 45)
        })
        batch.insert()

        self.assertEqual(batch.shelf_life_in_days, 45)

    def test_status_expired(self):
        """Test that status updates to Expired when expiration date passes"""
        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": add_days(today(), -60),
            "expiration_date": add_days(today(), -1)  # Expired yesterday
        })
        batch.insert()

        self.assertEqual(batch.status, "Expired")

    def test_status_consumed(self):
        """Test that status updates to Consumed when quantity is zero"""
        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": today(),
            "expiration_date": add_days(today(), 30),
            "quantity": 0
        })
        batch.insert()

        self.assertEqual(batch.status, "Consumed")

    def test_get_batch_balance(self):
        """Test get_batch_balance query function"""
        from blkshp_os.inventory.doctype.batch_number.batch_number import get_batch_balance

        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": today(),
            "quantity": 100.5
        })
        batch.insert()

        balance = get_batch_balance(batch.name)
        self.assertEqual(balance, 100.5)

    def test_get_expiring_batches(self):
        """Test get_expiring_batches query function"""
        from blkshp_os.inventory.doctype.batch_number.batch_number import get_expiring_batches

        # Create batch expiring in 15 days
        batch = frappe.get_doc({
            "doctype": "Batch Number",
            "product": self.product,
            "department": self.department,
            "company": self.company,
            "manufacturing_date": today(),
            "expiration_date": add_days(today(), 15),
            "quantity": 50
        })
        batch.insert()

        # Query for batches expiring within 30 days
        expiring = get_expiring_batches(
            department=self.department,
            company=self.company,
            within_days=30
        )

        # Should find our batch
        batch_ids = [b.batch_id for b in expiring]
        self.assertIn(batch.batch_id, batch_ids)

    def test_get_available_batches_fifo(self):
        """Test get_available_batches returns batches in FIFO order"""
        from blkshp_os.inventory.doctype.batch_number.batch_number import get_available_batches

        # Create 3 batches with different manufacturing dates
        for i in range(3):
            batch = frappe.get_doc({
                "doctype": "Batch Number",
                "product": self.product,
                "department": self.department,
                "company": self.company,
                "manufacturing_date": add_days(today(), -30 + (i * 10)),
                "expiration_date": add_days(today(), 60),
                "quantity": 100
            })
            batch.insert()

        # Query available batches
        available = get_available_batches(
            self.product,
            self.department,
            self.company
        )

        # Should return 3 batches in FIFO order (oldest first)
        self.assertEqual(len(available), 3)

        # Verify order: manufacturing dates should be ascending
        for i in range(len(available) - 1):
            self.assertLessEqual(
                frappe.utils.getdate(available[i].manufacturing_date),
                frappe.utils.getdate(available[i + 1].manufacturing_date)
            )
