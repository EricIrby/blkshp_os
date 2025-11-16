"""Tests for Company Group DocType."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompanyGroup(FrappeTestCase):
    """Test Company Group functionality."""

    def tearDown(self):
        """Clean up test data."""
        frappe.db.rollback()

    def test_create_company_group(self):
        """Test creating a company group."""
        # Create test companies
        company1 = self._create_test_company("TEST-CG-CO1", "Test Company 1")
        company2 = self._create_test_company("TEST-CG-CO2", "Test Company 2")

        # Create company group
        group = frappe.get_doc({
            "doctype": "Company Group",
            "group_name": "Test Group",
            "group_code": "TEST-GROUP",
            "description": "Test company group",
            "enable_intercompany_transactions": 1,
            "member_companies": [
                {"company": company1, "is_parent_company": 1},
                {"company": company2, "is_parent_company": 0},
            ]
        })
        group.insert()

        self.assertEqual(group.group_name, "Test Group")
        self.assertEqual(len(group.member_companies), 2)

    def test_unique_group_code(self):
        """Test that group codes must be unique."""
        company1 = self._create_test_company("TEST-CG-CO3", "Test Company 3")

        # Create first group
        group1 = frappe.get_doc({
            "doctype": "Company Group",
            "group_name": "Test Group 1",
            "group_code": "TEST-UNIQUE",
            "member_companies": [
                {"company": company1},
            ]
        })
        group1.insert()

        # Try to create second group with same code
        group2 = frappe.get_doc({
            "doctype": "Company Group",
            "group_name": "Test Group 2",
            "group_code": "TEST-UNIQUE",
            "member_companies": [
                {"company": company1},
            ]
        })

        with self.assertRaises(frappe.ValidationError):
            group2.insert()

    def test_company_cannot_be_in_multiple_groups(self):
        """Test that a company can only belong to one group."""
        company1 = self._create_test_company("TEST-CG-CO4", "Test Company 4")

        # Create first group
        group1 = frappe.get_doc({
            "doctype": "Company Group",
            "group_name": "Test Group A",
            "group_code": "TEST-A",
            "member_companies": [
                {"company": company1},
            ]
        })
        group1.insert()

        # Try to add same company to another group
        group2 = frappe.get_doc({
            "doctype": "Company Group",
            "group_name": "Test Group B",
            "group_code": "TEST-B",
            "member_companies": [
                {"company": company1},
            ]
        })

        with self.assertRaises(frappe.ValidationError):
            group2.insert()

    def test_group_requires_at_least_one_company(self):
        """Test that groups must have at least one member company."""
        group = frappe.get_doc({
            "doctype": "Company Group",
            "group_name": "Empty Group",
            "group_code": "TEST-EMPTY",
            "member_companies": []
        })

        with self.assertRaises(frappe.ValidationError):
            group.insert()

    def _create_test_company(self, code: str, name: str) -> str:
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
