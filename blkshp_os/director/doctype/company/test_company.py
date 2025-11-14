import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompany(FrappeTestCase):
    def test_create_company(self):
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
