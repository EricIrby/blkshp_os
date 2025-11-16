"""Tests for Intercompany Settlement DocType."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase


class TestIntercompanySettlement(FrappeTestCase):
    """Test Intercompany Settlement functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        # Create test companies
        cls.company1 = cls._create_test_company("SETTLE-CO1", "Settlement Test Co 1")
        cls.company2 = cls._create_test_company("SETTLE-CO2", "Settlement Test Co 2")
        cls.company3 = cls._create_test_company("SETTLE-CO3", "Settlement Test Co 3")

        # Create company groups
        cls.group1 = cls._create_company_group(
            "SETTLE-GRP1",
            "Settlement Group 1",
            [cls.company1, cls.company2]
        )
        cls.group2 = cls._create_company_group(
            "SETTLE-GRP2",
            "Settlement Group 2",
            [cls.company3]
        )

    def tearDown(self):
        """Clean up after each test."""
        frappe.db.rollback()

    def test_create_settlement(self):
        """Test creating an intercompany settlement."""
        settlement = frappe.get_doc({
            "doctype": "Intercompany Settlement",
            "source_company": self.company1,
            "target_company": self.company2,
            "settlement_amount": 10000.00,
            "settlement_currency": "USD",
            "description": "Test settlement",
            "payment_method": "Bank Transfer",
        })
        settlement.insert()

        self.assertEqual(settlement.source_company, self.company1)
        self.assertEqual(settlement.target_company, self.company2)
        self.assertEqual(settlement.settlement_amount, 10000.00)
        self.assertEqual(settlement.status, "Draft")

    def test_settlement_requires_different_companies(self):
        """Test that source and target must be different companies."""
        settlement = frappe.get_doc({
            "doctype": "Intercompany Settlement",
            "source_company": self.company1,
            "target_company": self.company1,  # Same company
            "settlement_amount": 5000.00,
            "settlement_currency": "USD",
        })

        with self.assertRaises(frappe.ValidationError):
            settlement.insert()

    def test_settlement_requires_same_group(self):
        """Test that companies must be in the same group."""
        settlement = frappe.get_doc({
            "doctype": "Intercompany Settlement",
            "source_company": self.company1,  # In group1
            "target_company": self.company3,  # In group2
            "settlement_amount": 5000.00,
            "settlement_currency": "USD",
        })

        with self.assertRaises(frappe.ValidationError):
            settlement.insert()

    def test_settlement_amount_must_be_positive(self):
        """Test that settlement amount must be greater than zero."""
        settlement = frappe.get_doc({
            "doctype": "Intercompany Settlement",
            "source_company": self.company1,
            "target_company": self.company2,
            "settlement_amount": 0,  # Invalid
            "settlement_currency": "USD",
        })

        with self.assertRaises(frappe.ValidationError):
            settlement.insert()

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
