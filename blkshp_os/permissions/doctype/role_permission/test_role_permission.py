"""Test cases for Role Permission child DocType."""

from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]


class TestRolePermission(FrappeTestCase):
    """Test Role Permission validation and functionality."""

    def setUp(self) -> None:
        super().setUp()
        self.test_role = self._ensure_role("Test Role Permission")

    def tearDown(self) -> None:
        frappe.db.rollback()
        super().tearDown()

    def test_permission_code_required(self) -> None:
        """Test that permission code is required."""
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append("custom_permissions", {"is_granted": 1})
        with self.assertRaises(frappe.ValidationError):
            role_doc.save(ignore_permissions=True)

    def test_invalid_permission_code(self) -> None:
        """Test that invalid permission codes are rejected."""
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions",
            {"permission_code": "invalid.permission", "is_granted": 1},
        )
        with self.assertRaises(frappe.ValidationError):
            role_doc.save(ignore_permissions=True)

    def test_valid_permission_code(self) -> None:
        """Test that valid permission codes are accepted."""
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.view", "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        # Verify saved
        role_doc.reload()
        self.assertEqual(len(role_doc.custom_permissions), 1)
        self.assertEqual(role_doc.custom_permissions[0].permission_code, "orders.view")

    def test_permission_details_auto_populated(self) -> None:
        """Test that permission details are auto-populated from registry."""
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.create", "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        # Verify details were populated
        role_doc.reload()
        perm = role_doc.custom_permissions[0]
        self.assertEqual(perm.permission_name, "Create Orders")
        self.assertEqual(perm.permission_category, "Orders")
        self.assertIsNotNone(perm.description)
        self.assertTrue(perm.department_restricted)

    def _ensure_role(self, role_name: str) -> str:
        if frappe.db.exists("Role", role_name):
            return role_name

        role = frappe.get_doc(
            {"doctype": "Role", "role_name": role_name, "desk_access": 1}
        )
        role.insert(ignore_permissions=True)
        return role_name
