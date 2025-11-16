"""Tests for finance API endpoints."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import today

from blkshp_os.api import finance as finance_api


class TestFinanceAPI(FrappeTestCase):
    """Test finance and intercompany REST API endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Create test companies
        cls.company1 = cls._create_test_company("FIN-API-CO1", "Finance API Test Co 1")
        cls.company2 = cls._create_test_company("FIN-API-CO2", "Finance API Test Co 2")
        cls.company3 = cls._create_test_company("FIN-API-CO3", "Finance API Test Co 3")

        # Create company group
        cls.group = cls._create_company_group(
            "FIN-API-GRP",
            "Finance API Test Group",
            [cls.company1, cls.company2]
        )

        frappe.db.commit()

    def tearDown(self):
        """Clean up after each test."""
        # Delete test settlements
        frappe.db.delete("Intercompany Settlement", {
            "source_company": ["in", [self.company1, self.company2, self.company3]]
        })
        frappe.db.commit()

    def test_get_intercompany_balance(self):
        """Test getting intercompany balance between two companies."""
        result = finance_api.get_intercompany_balance(
            source_company=self.company1,
            target_company=self.company2,
        )

        self.assertEqual(result["source_company"], self.company1)
        self.assertEqual(result["target_company"], self.company2)
        self.assertIn("balance", result)
        self.assertIn("currency", result)

    def test_list_intercompany_balances_by_company(self):
        """Test listing intercompany balances for a specific company."""
        result = finance_api.list_intercompany_balances(
            company=self.company1,
        )

        self.assertIn("balances", result)
        self.assertIn("total", result)
        self.assertIsInstance(result["balances"], list)

    def test_list_intercompany_balances_by_group(self):
        """Test listing intercompany balances for a company group."""
        result = finance_api.list_intercompany_balances(
            company_group=self.group,
        )

        self.assertIn("balances", result)
        self.assertIn("total", result)
        self.assertIsInstance(result["balances"], list)

    def test_list_settlements(self):
        """Test listing settlements."""
        # Create a test settlement
        settlement = frappe.get_doc({
            "doctype": "Intercompany Settlement",
            "source_company": self.company1,
            "target_company": self.company2,
            "settlement_amount": 5000.00,
            "settlement_currency": "USD",
            "description": "Test API settlement",
        })
        settlement.insert(ignore_permissions=True)

        # Query via API
        result = finance_api.list_settlements(
            company=self.company1,
            limit=10,
        )

        self.assertIn("settlements", result)
        self.assertIn("total", result)
        self.assertGreater(result["total"], 0)

    def test_get_settlement(self):
        """Test getting specific settlement details."""
        # Create a test settlement
        settlement = frappe.get_doc({
            "doctype": "Intercompany Settlement",
            "source_company": self.company1,
            "target_company": self.company2,
            "settlement_amount": 3000.00,
            "settlement_currency": "USD",
            "description": "Test API get settlement",
        })
        settlement.insert(ignore_permissions=True)

        # Query via API
        result = finance_api.get_settlement(settlement.name)

        self.assertEqual(result["name"], settlement.name)
        self.assertEqual(result["source_company"], self.company1)
        self.assertEqual(result["target_company"], self.company2)

    def test_create_settlement(self):
        """Test creating settlement via API."""
        settlement_data = {
            "source_company": self.company1,
            "target_company": self.company2,
            "settlement_amount": 10000.00,
            "settlement_currency": "USD",
            "description": "API created settlement",
            "payment_method": "Bank Transfer",
        }

        result = finance_api.create_settlement(settlement_data)

        self.assertIn("name", result)
        self.assertEqual(result["source_company"], self.company1)
        self.assertEqual(result["target_company"], self.company2)
        self.assertEqual(result["status"], "Draft")

        # Verify it was created
        self.assertTrue(frappe.db.exists("Intercompany Settlement", result["name"]))

    def test_create_settlement_validation(self):
        """Test settlement creation validates required fields."""
        # Missing required field
        settlement_data = {
            "source_company": self.company1,
            # Missing target_company
            "settlement_amount": 5000.00,
            "settlement_currency": "USD",
        }

        with self.assertRaises(frappe.ValidationError):
            finance_api.create_settlement(settlement_data)

    @staticmethod
    def _create_test_company(code: str, name: str) -> str:
        """Create a test company if it doesn't exist."""
        if not frappe.db.exists("Company", code):
            company = frappe.get_doc({
                "doctype": "Company",
                "company_name": name,
                "company_code": code,
                "default_currency": "USD",
            })
            company.insert(ignore_permissions=True)
        return code

    @staticmethod
    def _create_company_group(code: str, name: str, companies: list[str]) -> str:
        """Create a test company group if it doesn't exist."""
        if not frappe.db.exists("Company Group", code):
            group = frappe.get_doc({
                "doctype": "Company Group",
                "group_name": name,
                "group_code": code,
                "enable_intercompany_transactions": 1,
                "member_companies": [
                    {"company": company} for company in companies
                ]
            })
            group.insert(ignore_permissions=True)
        return code
