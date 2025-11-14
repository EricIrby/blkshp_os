from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]


class TestInventoryBalance(FrappeTestCase):
    """Validate Inventory Balance helpers and invariants."""

    _is_reloaded = False

    def setUp(self) -> None:
        super().setUp()
        if not self.__class__._is_reloaded:
            frappe.clear_cache(doctype="Inventory Balance")
            frappe.reload_doc("inventory", "doctype", "inventory_balance")
            self.__class__._is_reloaded = True
        self.company = self._ensure_company()
        self.department = self._ensure_department("Inventory QA Dept")
        self.product = self._ensure_product("Inventory QA Product")

    def tearDown(self) -> None:
        frappe.db.rollback()
        super().tearDown()

    def test_autoname_uses_product_department_company(self) -> None:
        doc = frappe.get_doc(
            {
                "doctype": "Inventory Balance",
                "product": self.product,
                "department": self.department,
                "company": self.company,
                "quantity": 5,
            }
        ).insert(ignore_permissions=True)

        expected_name = f"{self.product}-{self.department}-{self.company}"
        self.assertEqual(doc.name, expected_name)

    def test_unique_constraint_prevents_duplicates(self) -> None:
        frappe.get_doc(
            {
                "doctype": "Inventory Balance",
                "product": self.product,
                "department": self.department,
                "company": self.company,
                "quantity": 1,
            }
        ).insert(ignore_permissions=True)

        with self.assertRaises(frappe.ValidationError):
            frappe.get_doc(
                {
                    "doctype": "Inventory Balance",
                    "product": self.product,
                    "department": self.department,
                    "company": self.company,
                    "quantity": 2,
                }
            ).insert(ignore_permissions=True)

    def test_update_for_creates_or_updates_balance(self) -> None:
        from blkshp_os.inventory.doctype.inventory_balance.inventory_balance import (  # Local import for test runner
            InventoryBalance,
        )

        doc = InventoryBalance.update_for(
            self.product,
            self.department,
            self.company,
            quantity=12.5,
            last_audit_date="2025-01-15",
        )
        self.assertEqual(doc.quantity, 12.5)
        self.assertEqual(doc.last_audit_date, "2025-01-15")

        updated = InventoryBalance.update_for(
            self.product,
            self.department,
            self.company,
            quantity=4.25,
        )
        self.assertEqual(updated.name, doc.name)
        self.assertAlmostEqual(updated.quantity, 4.25)

    def _ensure_company(self, name: str = "Inventory QA Company") -> str:
        existing = frappe.db.exists("Company", {"company_name": name})
        if existing:
            return existing

        doc = frappe.get_doc(
            {
                "doctype": "Company",
                "company_name": name,
                "company_code": "".join(
                    part[0] for part in name.split() if part
                ).upper()[:8]
                or "COMP",
                "default_currency": "USD",
            }
        )
        doc.insert(ignore_permissions=True)
        return doc.name

    def _ensure_department(self, name: str) -> str:
        existing = frappe.db.exists("Department", {"department_name": name})
        if existing:
            return existing

        doc = frappe.get_doc(
            {
                "doctype": "Department",
                "department_name": name,
                "department_code": "".join(
                    part[0] for part in name.split() if part
                ).upper()[:8]
                or "DEPT",
                "department_type": "Food",
                "company": self.company,
            }
        )
        doc.insert(ignore_permissions=True)
        return doc.name

    def _ensure_product(self, name: str) -> str:
        existing = frappe.db.exists("Product", {"product_name": name})
        if existing:
            return existing

        doc = frappe.get_doc(
            {
                "doctype": "Product",
                "product_name": name,
                "primary_count_unit": "each",
                "default_department": self.department,
                "company": self.company,
                "volume_conversion_unit": "ml",
                "volume_conversion_factor": 1,
                "weight_conversion_unit": "g",
                "weight_conversion_factor": 1,
            }
        )
        doc.insert(ignore_permissions=True)
        return doc.name
