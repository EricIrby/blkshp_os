import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompany(FrappeTestCase):
    def tearDown(self):
        """Clean up test data."""
        # Delete test company if it exists
        if frappe.db.exists("Company", "TEST"):
            frappe.delete_doc("Company", "TEST", force=True)
        frappe.db.commit()

    def test_create_company(self):
        # Clean up any existing test company first
        if frappe.db.exists("Company", "TEST"):
            frappe.delete_doc("Company", "TEST", force=True)
            frappe.db.commit()

        doc = frappe.get_doc(
            {
                "doctype": "Company",
                "company_name": "Test Company",
                "company_code": "TEST",
            }
        )
        doc.insert()

        self.assertEqual(doc.company_name, "Test Company")
        self.assertEqual(doc.company_code, "TEST")
