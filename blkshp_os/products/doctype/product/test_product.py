import math

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.products.doctype.product.product import VOLUME_TO_ML


class TestProduct(FrappeTestCase):
    def test_purchase_and_volume_conversions(self):
        existing_company = frappe.db.get_value(
            "Company", {"company_name": "Test Company"}, "name"
        )
        if existing_company:
            company = frappe.get_doc("Company", existing_company)
        else:
            company = frappe.get_doc(
                {
                    "doctype": "Company",
                    "company_name": "Test Company",
                    "company_code": "TESTCO",
                }
            )
            company.insert(ignore_permissions=True)

        product = frappe.new_doc("Product")
        product.product_name = "Test Soda"
        product.product_code = "TEST-SODA"
        product.company = company.name
        product.primary_count_unit = "each"
        product.volume_conversion_unit = "fl oz"
        product.volume_conversion_factor = 12

        product.append(
            "purchase_units",
            {
                "purchase_unit": "case",
                "vendor": "Test Vendor",
                "conversion_to_primary_cu": 24,
            },
        )

        each_qty = product.convert_to_primary_unit("case", 2)
        self.assertEqual(each_qty, 48)

        each_qty_from_volume = product.convert_to_primary_unit("gallon", 1)
        expected_each_from_volume = (
            VOLUME_TO_ML["gallon"]
            / VOLUME_TO_ML[product.volume_conversion_unit.lower()]
        ) / product.volume_conversion_factor
        self.assertTrue(
            math.isclose(each_qty_from_volume, expected_each_from_volume, rel_tol=1e-6),
            f"Expected ~{expected_each_from_volume}, got {each_qty_from_volume}",
        )

        gallons = product.convert_from_primary_unit("gallon", each_qty_from_volume)
        self.assertTrue(
            math.isclose(gallons, 1.0, rel_tol=1e-6),
            f"Expected ~1 gallon, got {gallons}",
        )
