"""Tests for centralized unit conversion service."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.products import conversion


class TestConversions(FrappeTestCase):
    """Validate centralized unit conversion service."""

    def setUp(self) -> None:
        super().setUp()
        frappe.db.rollback()

        self.company = self._ensure_company("Conversion Test Company")
        self.department = self._create_department("CONV-DEPT", "Conversion Department")
        self.vendor = self._ensure_vendor("Test Vendor")

    def tearDown(self) -> None:
        frappe.set_user("Administrator")
        frappe.db.rollback()
        super().tearDown()

    def test_primary_conversion(self) -> None:
        """Test conversion to and from primary unit."""
        # Create product with volume conversion
        product_name = self._create_product(
            "Soda Can",
            extra_fields={
                "primary_count_unit": "each",
                "volume_conversion_unit": "fl oz",
                "volume_conversion_factor": 12.0,
            },
        )

        # Convert from volume unit to primary
        result = conversion.convert_to_primary_unit(product_name, "fl oz", 24.0)
        self.assertAlmostEqual(result, 2.0, places=4)

        # Convert from primary to volume unit
        result = conversion.convert_from_primary_unit(product_name, "fl oz", 2.0)
        self.assertAlmostEqual(result, 24.0, places=4)

        # Convert from primary to primary (should return same)
        result = conversion.convert_to_primary_unit(product_name, "each", 5.0)
        self.assertEqual(result, 5.0)

        result = conversion.convert_from_primary_unit(product_name, "each", 5.0)
        self.assertEqual(result, 5.0)

    def test_between_units(self) -> None:
        """Test conversion between two non-primary units."""
        # Create product with volume and weight conversions
        product_name = self._create_product(
            "Beer Keg",
            extra_fields={
                "primary_count_unit": "each",
                "volume_conversion_unit": "fl oz",
                "volume_conversion_factor": 1984.0,  # 15.5 gallons = 1984 fl oz
            },
        )

        # Convert from gallon to fl oz (via primary)
        # 1 gallon = 128 fl oz
        # 1 each (keg) = 1984 fl oz = 15.5 gallons
        result = conversion.convert_between_units(product_name, "gallon", "fl oz", 1.0)
        self.assertAlmostEqual(result, 128.0, places=2)

        # Convert from fl oz to gallon
        result = conversion.convert_between_units(
            product_name, "fl oz", "gallon", 128.0
        )
        self.assertAlmostEqual(result, 1.0, places=2)

        # Convert from primary to gallon
        result = conversion.convert_between_units(product_name, "each", "gallon", 1.0)
        self.assertAlmostEqual(result, 15.5, places=2)

        # Convert from gallon to primary
        result = conversion.convert_between_units(product_name, "gallon", "each", 15.5)
        self.assertAlmostEqual(result, 1.0, places=4)

    def test_purchase_unit_conversion(self) -> None:
        """Test conversion with purchase units."""
        product_name = self._create_product(
            "Coca Cola Cans",
            extra_fields={
                "primary_count_unit": "each",
                "volume_conversion_unit": "fl oz",
                "volume_conversion_factor": 12.0,
            },
        )

        # Add purchase unit
        product_doc = frappe.get_doc("Product", product_name)
        product_doc.append(
            "purchase_units",
            {
                "purchase_unit": "case",
                "conversion_to_primary_cu": 24.0,
                "vendor": self.vendor,
            },
        )
        product_doc.save(ignore_permissions=True)

        # Convert from case to primary
        result = conversion.convert_to_primary_unit(product_name, "case", 2.0)
        self.assertEqual(result, 48.0)

        # Convert from primary to case
        result = conversion.convert_from_primary_unit(product_name, "case", 48.0)
        self.assertEqual(result, 2.0)

        # Convert from case to fl oz
        result = conversion.convert_between_units(product_name, "case", "fl oz", 1.0)
        self.assertAlmostEqual(result, 288.0, places=2)  # 24 each * 12 fl oz

    def test_standard_volume_conversions(self) -> None:
        """Test standard volume unit conversions."""
        product_name = self._create_product(
            "Water",
            extra_fields={
                "primary_count_unit": "ml",
                "volume_conversion_unit": "ml",
                "volume_conversion_factor": 1.0,
            },
        )

        # Convert between standard volume units
        result = conversion.convert_between_units(product_name, "gallon", "fl oz", 1.0)
        self.assertAlmostEqual(result, 128.0, places=2)

        result = conversion.convert_between_units(product_name, "quart", "fl oz", 1.0)
        self.assertAlmostEqual(result, 32.0, places=2)

        result = conversion.convert_between_units(product_name, "pint", "fl oz", 1.0)
        self.assertAlmostEqual(result, 16.0, places=2)

        result = conversion.convert_between_units(product_name, "liter", "ml", 1.0)
        self.assertAlmostEqual(result, 1000.0, places=2)

    def test_standard_weight_conversions(self) -> None:
        """Test standard weight unit conversions."""
        product_name = self._create_product(
            "Flour",
            extra_fields={
                "primary_count_unit": "lb",
                "weight_conversion_unit": "lb",
                "weight_conversion_factor": 1.0,
            },
        )

        # Convert between standard weight units
        result = conversion.convert_between_units(product_name, "lb", "oz", 1.0)
        self.assertAlmostEqual(result, 16.0, places=2)

        result = conversion.convert_between_units(product_name, "lb", "g", 1.0)
        self.assertAlmostEqual(result, 453.592, places=2)

        result = conversion.convert_between_units(product_name, "kg", "g", 1.0)
        self.assertAlmostEqual(result, 1000.0, places=2)

    def test_get_available_units(self) -> None:
        """Test getting available count units for a product."""
        product_name = self._create_product(
            "Multi-Unit Product",
            extra_fields={
                "primary_count_unit": "each",
                "volume_conversion_unit": "fl oz",
                "volume_conversion_factor": 12.0,
                "weight_conversion_unit": "g",
                "weight_conversion_factor": 360.0,
            },
        )

        # Add purchase unit
        product_doc = frappe.get_doc("Product", product_name)
        product_doc.append(
            "purchase_units",
            {
                "purchase_unit": "case",
                "conversion_to_primary_cu": 24.0,
                "vendor": self.vendor,
            },
        )
        product_doc.save(ignore_permissions=True)

        units = conversion.get_available_count_units(product_name)

        # Should include primary, volume, weight, purchase units, and standard units
        self.assertIn("each", units)
        self.assertIn("fl oz", units)
        self.assertIn("g", units)
        self.assertIn("case", units)
        self.assertIn("gallon", units)  # Standard volume
        self.assertIn("lb", units)  # Standard weight

    def test_invalid_conversion_raises_error(self) -> None:
        """Test that invalid conversions raise ValidationError."""
        product_name = self._create_product(
            "Simple Product",
            extra_fields={
                "primary_count_unit": "each",
            },
        )

        # Try to convert from invalid unit
        with self.assertRaises(frappe.ValidationError):
            conversion.convert_to_primary_unit(product_name, "invalid_unit", 1.0)

        # Try to convert to invalid unit
        with self.assertRaises(frappe.ValidationError):
            conversion.convert_from_primary_unit(product_name, "invalid_unit", 1.0)

    def test_conversion_with_product_dict(self) -> None:
        """Test conversion using product data dict instead of name."""
        product_name = self._create_product(
            "Dict Test Product",
            extra_fields={
                "primary_count_unit": "each",
                "volume_conversion_unit": "fl oz",
                "volume_conversion_factor": 12.0,
            },
        )

        # Load product data
        product_doc = frappe.get_doc("Product", product_name)
        product_data = {
            "name": product_doc.name,
            "primary_count_unit": product_doc.primary_count_unit,
            "volume_conversion_unit": product_doc.volume_conversion_unit,
            "volume_conversion_factor": product_doc.volume_conversion_factor,
            "weight_conversion_unit": product_doc.weight_conversion_unit,
            "weight_conversion_factor": product_doc.weight_conversion_factor,
            "purchase_units": None,
        }

        # Convert using dict
        result = conversion.convert_to_primary_unit(product_data, "fl oz", 24.0)
        self.assertAlmostEqual(result, 2.0, places=4)

        result = conversion.convert_from_primary_unit(product_data, "fl oz", 2.0)
        self.assertAlmostEqual(result, 24.0, places=4)

    def test_conversion_with_product_document(self) -> None:
        """Test conversion using Product Document object directly (BUG FIX TEST)."""
        product_name = self._create_product(
            "Document Test Product",
            extra_fields={
                "primary_count_unit": "each",
                "volume_conversion_unit": "fl oz",
                "volume_conversion_factor": 12.0,
            },
        )

        # Load Product Document
        product_doc = frappe.get_doc("Product", product_name)

        # Test Document methods (these pass self as Document object)
        result = product_doc.convert_to_primary_unit("fl oz", 24.0)
        self.assertAlmostEqual(result, 2.0, places=4)

        result = product_doc.convert_from_primary_unit("fl oz", 2.0)
        self.assertAlmostEqual(result, 24.0, places=4)

        result = product_doc.convert_between_units("fl oz", "each", 12.0)
        self.assertAlmostEqual(result, 1.0, places=4)

        # Test passing Document directly to conversion module
        result = conversion.convert_to_primary_unit(product_doc, "fl oz", 24.0)
        self.assertAlmostEqual(result, 2.0, places=4)

        result = conversion.convert_from_primary_unit(product_doc, "fl oz", 2.0)
        self.assertAlmostEqual(result, 24.0, places=4)

        result = conversion.convert_between_units(product_doc, "fl oz", "each", 12.0)
        self.assertAlmostEqual(result, 1.0, places=4)

        # Test get_available_count_units with Document
        units = product_doc.get_available_count_units()
        self.assertIn("each", units)
        self.assertIn("fl oz", units)

        units = conversion.get_available_count_units(product_doc)
        self.assertIn("each", units)
        self.assertIn("fl oz", units)

    # -------------------------------------------------------------------------
    # Helpers
    # -------------------------------------------------------------------------

    def _ensure_company(self, name: str) -> str:
        existing = frappe.db.get_value("Company", {"company_name": name})
        if existing:
            return existing

        code = "".join(part[0] for part in name.split() if part).upper()[:8] or "COMP"
        company = frappe.get_doc(
            {
                "doctype": "Company",
                "company_name": name,
                "company_code": code,
                "default_currency": "USD",
            }
        )
        company.insert(ignore_permissions=True)
        return company.name

    def _create_department(self, code: str, name: str) -> frappe.Document:
        department = frappe.get_doc(
            {
                "doctype": "Department",
                "department_code": code,
                "department_name": name,
                "department_type": "Food",
                "company": self.company,
            }
        )
        department.insert(ignore_permissions=True)
        return department

    def _ensure_vendor(self, name: str) -> str:
        """Ensure a test vendor exists."""
        existing = frappe.db.get_value("Vendor", {"vendor_name": name})
        if existing:
            return existing

        vendor = frappe.get_doc(
            {
                "doctype": "Vendor",
                "vendor_name": name,
                "vendor_code": name.upper().replace(" ", "-"),
                "company": self.company,
            }
        )
        vendor.insert(ignore_permissions=True)
        return vendor.name

    def _create_product(
        self,
        product_name: str,
        extra_fields: dict | None = None,
    ) -> str:
        from blkshp_os.products import service

        payload = {
            "product_name": product_name,
            "product_code": product_name.upper().replace(" ", "-"),
            "company": self.company,
            "product_type": "Food",
            "primary_count_unit": "each",
            "default_department": self.department.name,
            "departments": [
                {
                    "department": self.department.name,
                    "is_primary": 1,
                }
            ],
            "volume_conversion_unit": "",
            "volume_conversion_factor": None,
            "weight_conversion_unit": "",
            "weight_conversion_factor": None,
        }

        if extra_fields:
            payload.update(extra_fields)

        doc = service.create_product(payload)
        return doc["name"]
