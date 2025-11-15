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

    def test_default_valuation_method(self):
        """Test that default valuation method is set."""
        company = self._ensure_company()

        product = frappe.new_doc("Product")
        product.product_name = "Test Valuation Product"
        product.product_code = "TEST-VAL-001"
        product.company = company
        product.primary_count_unit = "each"
        product.insert(ignore_permissions=True)

        # Should default to Moving Average
        self.assertEqual(product.valuation_method, "Moving Average")
        self.assertEqual(product.valuation_rate, 0.0)

    def test_valuation_fields_validation(self):
        """Test validation of valuation fields."""
        company = self._ensure_company()

        product = frappe.new_doc("Product")
        product.product_name = "Test Valuation Validation"
        product.product_code = "TEST-VAL-002"
        product.company = company
        product.primary_count_unit = "lb"
        product.valuation_rate = -10.0  # Negative value

        # Should throw error for negative valuation rate
        with self.assertRaises(frappe.ValidationError):
            product.insert(ignore_permissions=True)

    def test_valuation_method_options(self):
        """Test different valuation method options."""
        company = self._ensure_company()

        # Test Moving Average
        product1 = frappe.new_doc("Product")
        product1.product_name = "Moving Average Product"
        product1.product_code = "TEST-VAL-MA"
        product1.company = company
        product1.primary_count_unit = "each"
        product1.valuation_method = "Moving Average"
        product1.valuation_rate = 5.50
        product1.insert(ignore_permissions=True)

        self.assertEqual(product1.valuation_method, "Moving Average")
        self.assertEqual(product1.valuation_rate, 5.50)

        # Test FIFO
        product2 = frappe.new_doc("Product")
        product2.product_name = "FIFO Product"
        product2.product_code = "TEST-VAL-FIFO"
        product2.company = company
        product2.primary_count_unit = "each"
        product2.valuation_method = "FIFO"
        product2.valuation_rate = 3.25
        product2.insert(ignore_permissions=True)

        self.assertEqual(product2.valuation_method, "FIFO")
        self.assertEqual(product2.valuation_rate, 3.25)

        # Test Manual
        product3 = frappe.new_doc("Product")
        product3.product_name = "Manual Product"
        product3.product_code = "TEST-VAL-MANUAL"
        product3.company = company
        product3.primary_count_unit = "each"
        product3.valuation_method = "Manual"
        product3.valuation_rate = 10.00
        product3.insert(ignore_permissions=True)

        self.assertEqual(product3.valuation_method, "Manual")
        self.assertEqual(product3.valuation_rate, 10.00)

    def test_default_incoming_rate(self):
        """Test default incoming rate field."""
        company = self._ensure_company()

        product = frappe.new_doc("Product")
        product.product_name = "Test Incoming Rate Product"
        product.product_code = "TEST-VAL-INCOMING"
        product.company = company
        product.primary_count_unit = "lb"
        product.default_incoming_rate = 2.75
        product.insert(ignore_permissions=True)

        self.assertEqual(product.default_incoming_rate, 2.75)

    def test_negative_default_incoming_rate_validation(self):
        """Test that negative default incoming rate is rejected."""
        company = self._ensure_company()

        product = frappe.new_doc("Product")
        product.product_name = "Test Negative Incoming"
        product.product_code = "TEST-VAL-NEG-INCOMING"
        product.company = company
        product.primary_count_unit = "each"
        product.default_incoming_rate = -5.00  # Negative value

        with self.assertRaises(frappe.ValidationError):
            product.insert(ignore_permissions=True)

    def _ensure_company(self):
        """Helper to get or create test company."""
        existing_company = frappe.db.get_value(
            "Company", {"company_name": "Test Company"}, "name"
        )
        if existing_company:
            return existing_company

        company = frappe.get_doc(
            {
                "doctype": "Company",
                "company_name": "Test Company",
                "company_code": "TESTCO",
                "default_currency": "USD",
            }
        )
        company.insert(ignore_permissions=True)
        return company.name
