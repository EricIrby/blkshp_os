"""Tests for inventory API endpoints."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, today

from blkshp_os.api import inventory as inventory_api


class TestInventoryAPI(FrappeTestCase):
    """Test inventory REST API endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Create test company
        if not frappe.db.exists("Company", "TEST-INV-API"):
            company = frappe.new_doc("Company")
            company.company_name = "Inventory API Test Company"
            company.company_code = "TEST-INV-API"
            company.default_currency = "USD"
            company.insert(ignore_permissions=True)

        # Create test department
        if not frappe.db.exists("Department", {"department_code": "TEST-INV-DEPT", "company": "TEST-INV-API"}):
            dept = frappe.new_doc("Department")
            dept.department_name = "Test Inventory Department"
            dept.department_code = "TEST-INV-DEPT"
            dept.department_type = "Other"
            dept.company = "TEST-INV-API"
            dept.is_active = 1
            dept.insert(ignore_permissions=True)

        # Create test product
        if not frappe.db.exists("Product", "TEST-INV-PRODUCT"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-INV-PRODUCT"
            product.product_name = "Test Inventory Product"
            product.company = "TEST-INV-API"
            product.primary_count_unit = "lb"
            product.volume_conversion_unit = ""
            product.weight_conversion_unit = ""
            product.insert(ignore_permissions=True)

        frappe.db.commit()

    def tearDown(self):
        """Clean up after each test."""
        # Delete test stock ledger entries
        frappe.db.delete("Stock Ledger Entry", {
            "product": "TEST-INV-PRODUCT",
            "department": "TEST-INV-DEPT-TEST-INV-API"
        })

        # Delete test inventory balances
        balance_name = "TEST-INV-PRODUCT-TEST-INV-DEPT-TEST-INV-API-TEST-INV-API"
        if frappe.db.exists("Inventory Balance", balance_name):
            frappe.delete_doc("Inventory Balance", balance_name, force=True)

        frappe.db.commit()

    def test_list_inventory_balances(self):
        """Test listing inventory balances."""
        # Create a test balance
        balance = frappe.new_doc("Inventory Balance")
        balance.product = "TEST-INV-PRODUCT"
        balance.department = "TEST-INV-DEPT-TEST-INV-API"
        balance.company = "TEST-INV-API"
        balance.quantity = 100
        balance.insert(ignore_permissions=True)

        # Query via API
        result = inventory_api.list_inventory_balances(
            product="TEST-INV-PRODUCT",
            limit=10,
        )

        self.assertIn("balances", result)
        self.assertIn("total", result)
        self.assertGreater(result["total"], 0)
        self.assertTrue(any(
            b["product"] == "TEST-INV-PRODUCT" for b in result["balances"]
        ))

    def test_get_inventory_balance(self):
        """Test getting specific inventory balance."""
        # Create a test balance
        balance = frappe.new_doc("Inventory Balance")
        balance.product = "TEST-INV-PRODUCT"
        balance.department = "TEST-INV-DEPT-TEST-INV-API"
        balance.company = "TEST-INV-API"
        balance.quantity = 50
        balance.insert(ignore_permissions=True)

        # Query via API
        result = inventory_api.get_inventory_balance(
            product="TEST-INV-PRODUCT",
            department="TEST-INV-DEPT-TEST-INV-API",
            company="TEST-INV-API",
        )

        self.assertEqual(result["product"], "TEST-INV-PRODUCT")
        self.assertEqual(result["quantity"], 50)

    def test_query_stock_balance(self):
        """Test querying stock balance from ledger."""
        # Create a test stock ledger entry
        entry = frappe.new_doc("Stock Ledger Entry")
        entry.product = "TEST-INV-PRODUCT"
        entry.department = "TEST-INV-DEPT-TEST-INV-API"
        entry.company = "TEST-INV-API"
        entry.actual_qty = 25
        entry.posting_date = today()
        entry.voucher_type = "Inventory Audit"
        entry.voucher_no = "TEST-AUDIT-API-001"
        entry.insert(ignore_links=True)
        entry.submit()

        # Query via API
        result = inventory_api.query_stock_balance(
            product="TEST-INV-PRODUCT",
            department="TEST-INV-DEPT-TEST-INV-API",
            company="TEST-INV-API",
        )

        self.assertEqual(result["product"], "TEST-INV-PRODUCT")
        self.assertIn("balance", result)

    def test_list_batches(self):
        """Test listing batch numbers."""
        # Create a test batch-tracked product
        if not frappe.db.exists("Product", "TEST-BATCH-API"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-API"
            product.product_name = "Test Batch API Product"
            product.company = "TEST-INV-API"
            product.primary_count_unit = "lb"
            product.volume_conversion_unit = ""
            product.weight_conversion_unit = ""
            product.has_batch_no = 1
            product.insert(ignore_permissions=True)

        # Create a test batch
        batch = frappe.new_doc("Batch Number")
        batch.product = "TEST-BATCH-API"
        batch.department = "TEST-INV-DEPT-TEST-INV-API"
        batch.company = "TEST-INV-API"
        batch.manufacturing_date = today()
        batch.expiration_date = add_days(today(), 30)
        batch.insert(ignore_permissions=True)
        batch_name = batch.name

        # Query via API
        result = inventory_api.list_batches(
            product="TEST-BATCH-API",
            limit=10,
        )

        self.assertIn("batches", result)
        self.assertIn("total", result)
        self.assertGreater(result["total"], 0)

        # Cleanup
        frappe.delete_doc("Batch Number", batch_name, force=True)
        frappe.delete_doc("Product", "TEST-BATCH-API", force=True)

    def test_get_batch(self):
        """Test getting specific batch details."""
        # Create a test batch-tracked product
        if not frappe.db.exists("Product", "TEST-BATCH-API-2"):
            product = frappe.new_doc("Product")
            product.product_code = "TEST-BATCH-API-2"
            product.product_name = "Test Batch API Product 2"
            product.company = "TEST-INV-API"
            product.primary_count_unit = "lb"
            product.volume_conversion_unit = ""
            product.weight_conversion_unit = ""
            product.has_batch_no = 1
            product.insert(ignore_permissions=True)

        # Create a test batch
        batch = frappe.new_doc("Batch Number")
        batch.product = "TEST-BATCH-API-2"
        batch.department = "TEST-INV-DEPT-TEST-INV-API"
        batch.company = "TEST-INV-API"
        batch.manufacturing_date = today()
        batch.expiration_date = add_days(today(), 30)
        batch.insert(ignore_permissions=True)
        batch_name = batch.name

        # Query via API
        result = inventory_api.get_batch(batch_name)

        self.assertEqual(result["product"], "TEST-BATCH-API-2")
        self.assertEqual(result["department"], "TEST-INV-DEPT-TEST-INV-API")

        # Cleanup
        frappe.delete_doc("Batch Number", batch_name, force=True)
        frappe.delete_doc("Product", "TEST-BATCH-API-2", force=True)

    def test_list_audits(self):
        """Test listing inventory audits."""
        # Create a test audit
        audit = frappe.new_doc("Inventory Audit")
        audit.audit_name = "Test API Audit"
        audit.company = "TEST-INV-API"
        audit.audit_date = today()
        audit.append("audit_departments", {
            "department": "TEST-INV-DEPT-TEST-INV-API"
        })
        audit.insert(ignore_permissions=True)
        audit_name = audit.name

        # Query via API
        result = inventory_api.list_audits(
            company="TEST-INV-API",
            limit=10,
        )

        self.assertIn("audits", result)
        self.assertIn("total", result)

        # Cleanup
        frappe.delete_doc("Inventory Audit", audit_name, force=True)

    def test_get_audit(self):
        """Test getting specific audit details."""
        # Create a test audit
        audit = frappe.new_doc("Inventory Audit")
        audit.audit_name = "Test API Audit 2"
        audit.company = "TEST-INV-API"
        audit.audit_date = today()
        audit.append("audit_departments", {
            "department": "TEST-INV-DEPT-TEST-INV-API"
        })
        audit.insert(ignore_permissions=True)
        audit_name = audit.name

        # Query via API
        result = inventory_api.get_audit(audit_name)

        self.assertEqual(result["audit_name"], "Test API Audit 2")
        self.assertEqual(result["company"], "TEST-INV-API")
        self.assertIn("departments", result)

        # Cleanup
        frappe.delete_doc("Inventory Audit", audit_name, force=True)

    def test_create_audit(self):
        """Test creating inventory audit via API."""
        audit_data = {
            "audit_name": "Test API Created Audit",
            "company": "TEST-INV-API",
            "audit_date": today(),
            "departments": [
                {"department": "TEST-INV-DEPT-TEST-INV-API"}
            ],
        }

        result = inventory_api.create_audit(audit_data)

        self.assertIn("name", result)
        self.assertEqual(result["audit_name"], "Test API Created Audit")
        self.assertEqual(result["status"], "Setup")

        # Cleanup
        frappe.delete_doc("Inventory Audit", result["name"], force=True)

    def test_update_audit_status(self):
        """Test updating audit status via API."""
        # Create a test audit
        audit = frappe.new_doc("Inventory Audit")
        audit.audit_name = "Test API Status Update"
        audit.company = "TEST-INV-API"
        audit.audit_date = today()
        audit.append("audit_departments", {
            "department": "TEST-INV-DEPT-TEST-INV-API"
        })
        audit.insert(ignore_permissions=True)
        audit_name = audit.name

        # Update status via API
        result = inventory_api.update_audit_status(
            audit_name=audit_name,
            action="mark_in_progress",
        )

        self.assertEqual(result["status"], "In Progress")
        self.assertEqual(result["action_performed"], "mark_in_progress")

        # Cleanup
        frappe.delete_doc("Inventory Audit", audit_name, force=True)
