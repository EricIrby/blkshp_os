from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]


class TestInventoryAudit(FrappeTestCase):
    """Exercise inventory audit workflow helpers."""

    _is_reloaded = False

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not cls._is_reloaded:
            for doctype in (
                "inventory_audit_department",
                "inventory_audit_storage_location",
                "inventory_audit_category",
                "inventory_counting_task",
                "inventory_audit_line",
                "inventory_audit",
            ):
                frappe.clear_cache(doctype=doctype.replace("_", " ").title())
                frappe.reload_doc("inventory", "doctype", doctype)
            frappe.reload_doc("inventory", "doctype", "inventory_balance")
            cls._is_reloaded = True

    def setUp(self) -> None:
        super().setUp()
        self.company = self._ensure_company()
        self.department_a = self._ensure_department("Inventory Audit Dept A")
        self.department_b = self._ensure_department("Inventory Audit Dept B")
        self.storage_a = self._ensure_storage_area("Dry Storage A", self.department_a)
        self.storage_b = self._ensure_storage_area("Cooler B", self.department_b)
        self.storage_general = self._ensure_storage_area("General Storage", None)
        self._ensure_role("System User")
        self.product = self._ensure_product("Inventory Audit Product", base_cost=2.5)
        self.audit_user = self._ensure_user("auditor@example.com")

    def tearDown(self) -> None:
        frappe.db.rollback()
        super().tearDown()

    def test_create_counting_tasks_generates_scope_matrix(self) -> None:
        audit = frappe.get_doc(
            {
                "doctype": "Inventory Audit",
                "audit_name": "January Audit Matrix",
                "audit_date": "2025-01-31",
                "company": self.company,
                "audit_departments": [
                    {"department": self.department_a},
                    {"department": self.department_b},
                ],
                "audit_storage_locations": [
                    {"storage_area": self.storage_a},
                    {"storage_area": self.storage_b},
                    {"storage_area": self.storage_general},
                ],
                "audit_categories": [
                    {"product_category": self._ensure_category("Beer")},
                    {"product_category": self._ensure_category("Wine")},
                ],
            }
        )
        audit.insert(ignore_permissions=True)

        audit.create_counting_tasks()
        audit.save(ignore_permissions=True)

        self.assertEqual(audit.status, "Ready")
        self.assertEqual(len(audit.counting_tasks or []), 8)

        task_matrix = {
            (task.department, task.storage_area, task.category)
            for task in audit.counting_tasks or []
        }
        expected_combinations = {
            (self.department_a, self.storage_a, self._ensure_category("Beer")),
            (self.department_a, self.storage_a, self._ensure_category("Wine")),
            (self.department_a, self.storage_general, self._ensure_category("Beer")),
            (self.department_a, self.storage_general, self._ensure_category("Wine")),
            (self.department_b, self.storage_b, self._ensure_category("Beer")),
            (self.department_b, self.storage_b, self._ensure_category("Wine")),
            (self.department_b, self.storage_general, self._ensure_category("Beer")),
            (self.department_b, self.storage_general, self._ensure_category("Wine")),
        }
        self.assertSetEqual(task_matrix, expected_combinations)

    def test_close_audit_updates_inventory_balances(self) -> None:
        audit = frappe.get_doc(
            {
                "doctype": "Inventory Audit",
                "audit_name": "February Audit Close",
                "audit_date": "2025-02-15",
                "company": self.company,
                "status": "Review",
                "audit_departments": [{"department": self.department_a}],
                "audit_lines": [
                    {
                        "product": self.product,
                        "department": self.department_a,
                        "quantity": 12,
                        "unit": "each",
                        "expected_quantity": 10,
                        "unit_cost": 3.25,
                    }
                ],
            }
        )
        audit.insert(ignore_permissions=True)

        audit.close_audit(user=self.audit_user)
        audit.save(ignore_permissions=True)

        self.assertEqual(audit.status, "Closed")
        self.assertEqual(audit.total_products_counted, 1)
        self.assertAlmostEqual(audit.total_value, 39.0)
        self.assertEqual(audit.audit_lines[0].variance, 2.0)
        self.assertEqual(audit.audit_lines[0].quantity_primary, 12.0)

        balance_name = frappe.db.exists(
            "Inventory Balance",
            {
                "product": self.product,
                "department": self.department_a,
                "company": self.company,
            },
        )
        self.assertIsNotNone(balance_name)
        balance = frappe.get_doc("Inventory Balance", balance_name)
        self.assertAlmostEqual(balance.quantity, 12.0)
        self.assertEqual(
            balance.last_audit_date.isoformat() if balance.last_audit_date else None,
            "2025-02-15",
        )

    def test_calculate_variance_returns_product_totals(self) -> None:
        audit = frappe.get_doc(
            {
                "doctype": "Inventory Audit",
                "audit_name": "Variance Example",
                "audit_date": "2025-03-01",
                "company": self.company,
                "audit_departments": [{"department": self.department_a}],
                "audit_lines": [
                    {
                        "product": self.product,
                        "department": self.department_a,
                        "quantity": 5,
                        "unit": "each",
                        "expected_quantity": 4,
                    },
                    {
                        "product": self.product,
                        "department": self.department_a,
                        "quantity": 3,
                        "unit": "each",
                        "expected_quantity": 5,
                    },
                ],
            }
        ).insert(ignore_permissions=True)

        variances = audit.calculate_variance()
        self.assertIn(self.product, variances)
        self.assertAlmostEqual(variances[self.product], -1.0)
        self.assertAlmostEqual(audit.audit_lines[0].variance, 1.0)
        self.assertAlmostEqual(audit.audit_lines[1].variance, -2.0)

    def _ensure_company(self, name: str = "Inventory Audit Company") -> str:
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

    def _ensure_user(self, email: str) -> str:
        if frappe.db.exists("User", email):
            return email

        doc = frappe.get_doc(
            {
                "doctype": "User",
                "email": email,
                "first_name": "Audit",
                "last_name": "User",
                "enabled": 1,
                "send_welcome_email": 0,
                "roles": [{"role": "System User"}],
            }
        )
        doc.insert(ignore_permissions=True)
        return email

    def _ensure_role(self, role_name: str) -> None:
        if frappe.db.exists("Role", role_name):
            return

        doc = frappe.get_doc(
            {
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 0,
            }
        )
        doc.insert(ignore_permissions=True)

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

    def _ensure_storage_area(self, name: str, department: str | None) -> str:
        existing = frappe.db.exists("Storage Area", {"storage_area_name": name})
        if existing:
            return existing

        doc = frappe.get_doc(
            {
                "doctype": "Storage Area",
                "storage_area_name": name,
                "storage_area_code": "".join(
                    part[0] for part in name.split() if part
                ).upper()[:8]
                or "STORE",
                "company": self.company,
                "department": department,
            }
        )
        doc.insert(ignore_permissions=True)
        return doc.name

    def _ensure_product(self, name: str, base_cost: float) -> str:
        existing = frappe.db.exists("Product", {"product_name": name})
        if existing:
            return existing

        doc = frappe.get_doc(
            {
                "doctype": "Product",
                "product_name": name,
                "primary_count_unit": "each",
                "default_department": self.department_a,
                "company": self.company,
                "volume_conversion_unit": "ml",
                "volume_conversion_factor": 1,
                "weight_conversion_unit": "g",
                "weight_conversion_factor": 1,
                "valuation_rate": base_cost,
                "standard_rate": base_cost,
            }
        )
        doc.insert(ignore_permissions=True)
        return doc.name

    def _ensure_category(self, name: str) -> str:
        existing = frappe.db.exists("Product Category", {"category_name": name})
        if existing:
            return existing

        doc = frappe.get_doc(
            {
                "doctype": "Product Category",
                "category_name": name,
                "category_code": "".join(
                    part[0] for part in name.split() if part
                ).upper()[:8]
                or "CAT",
                "company": self.company,
            }
        )
        doc.insert(ignore_permissions=True)
        return doc.name
