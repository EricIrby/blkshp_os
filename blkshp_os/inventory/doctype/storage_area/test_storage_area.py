import frappe
from frappe.tests.utils import FrappeTestCase


class TestStorageArea(FrappeTestCase):
    def test_create_storage_area(self):
        doc = frappe.get_doc(
            {
                "doctype": "Storage Area",
                "storage_area_name": "Main Cooler",
                "storage_area_code": "MAIN-COOLER",
            }
        )
        doc.insert()

        self.assertEqual(doc.storage_area_name, "Main Cooler")
        self.assertEqual(doc.storage_area_code, "MAIN-COOLER")
