"""Tests for role management service."""

from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]

from blkshp_os.permissions import roles as role_service


class TestRolesService(FrappeTestCase):
    """Test role management service functions."""

    _is_role_setup_done = False

    def setUp(self) -> None:
        super().setUp()
        if not self.__class__._is_role_setup_done:
            self._ensure_role_customizations()
            self.__class__._is_role_setup_done = True
        self.test_user = self._ensure_user("roles_test@example.com")
        self.test_role = self._create_role("Test Role Service")

    def tearDown(self) -> None:
        frappe.db.rollback()
        super().tearDown()

    def test_get_user_roles(self) -> None:
        """Test getting user roles."""
        # Assign role to user
        user_doc = frappe.get_doc("User", self.test_user)
        user_doc.append("roles", {"role": self.test_role})
        user_doc.save(ignore_permissions=True)

        roles = role_service.get_user_roles(self.test_user)
        self.assertIn(self.test_role, roles)

    def test_has_role(self) -> None:
        """Test checking if user has a role."""
        user_doc = frappe.get_doc("User", self.test_user)
        user_doc.append("roles", {"role": self.test_role})
        user_doc.save(ignore_permissions=True)

        self.assertTrue(role_service.has_role(self.test_user, self.test_role))
        self.assertFalse(role_service.has_role(self.test_user, "Nonexistent Role"))

    def test_get_role_permissions(self) -> None:
        """Test getting permissions for a role."""
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.view", "is_granted": 1}
        )
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.create", "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        perms = role_service.get_role_permissions(self.test_role)
        self.assertEqual(len(perms), 2)
        perm_codes = [p["permission_code"] for p in perms]
        self.assertIn("orders.view", perm_codes)
        self.assertIn("orders.create", perm_codes)

    def test_has_permission(self) -> None:
        """Test checking if user has a permission."""
        # Add permission to role
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.view", "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        # Assign role to user
        user_doc = frappe.get_doc("User", self.test_user)
        user_doc.append("roles", {"role": self.test_role})
        user_doc.save(ignore_permissions=True)

        # Check permission
        self.assertTrue(role_service.has_permission(self.test_user, "orders.view"))
        self.assertFalse(role_service.has_permission(self.test_user, "orders.create"))

    def test_system_manager_has_all_permissions(self) -> None:
        """Test that System Manager has all permissions."""
        admin_user = "Administrator"
        self.assertTrue(role_service.has_permission(admin_user, "orders.view"))
        self.assertTrue(role_service.has_permission(admin_user, "invoices.approve"))
        self.assertTrue(
            role_service.has_permission(admin_user, "director.manage_stores")
        )

    def test_create_role(self) -> None:
        """Test creating a new custom role."""
        role_name = "Test Created Role"
        permissions = ["orders.view", "orders.create"]
        description = "Test role description"

        role = role_service.create_role(role_name, permissions, description)

        self.assertEqual(role.role_name, role_name)
        self.assertEqual(role.role_description, description)
        self.assertTrue(role.is_custom_role)
        self.assertEqual(len(role.custom_permissions), 2)

    def test_update_role_permissions_add(self) -> None:
        """Test adding permissions to a role."""
        initial_perms = ["orders.view"]
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": initial_perms[0], "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        # Add more permissions
        new_perms = ["orders.create", "orders.edit"]
        role_service.update_role_permissions(self.test_role, new_perms, replace=False)

        # Verify
        role_doc.reload()
        perm_codes = [p.permission_code for p in role_doc.custom_permissions]
        self.assertEqual(len(perm_codes), 3)
        self.assertIn("orders.view", perm_codes)
        self.assertIn("orders.create", perm_codes)
        self.assertIn("orders.edit", perm_codes)

    def test_update_role_permissions_replace(self) -> None:
        """Test replacing all permissions for a role."""
        # Add initial permissions
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.view", "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        # Replace with new permissions
        new_perms = ["invoices.view", "invoices.create"]
        role_service.update_role_permissions(self.test_role, new_perms, replace=True)

        # Verify
        role_doc.reload()
        perm_codes = [p.permission_code for p in role_doc.custom_permissions]
        self.assertEqual(len(perm_codes), 2)
        self.assertNotIn("orders.view", perm_codes)
        self.assertIn("invoices.view", perm_codes)
        self.assertIn("invoices.create", perm_codes)

    def test_revoke_role_permission(self) -> None:
        """Test revoking a permission from a role."""
        # Add permissions
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.view", "is_granted": 1}
        )
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.create", "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        # Revoke one permission
        role_service.revoke_role_permission(self.test_role, "orders.create")

        # Verify
        role_doc.reload()
        perm_codes = [p.permission_code for p in role_doc.custom_permissions]
        self.assertEqual(len(perm_codes), 1)
        self.assertIn("orders.view", perm_codes)
        self.assertNotIn("orders.create", perm_codes)

    def test_get_role_summary(self) -> None:
        """Test getting role summary."""
        # Add permissions
        role_doc = frappe.get_doc("Role", self.test_role)
        role_doc.append(
            "custom_permissions", {"permission_code": "orders.view", "is_granted": 1}
        )
        role_doc.append(
            "custom_permissions", {"permission_code": "invoices.view", "is_granted": 1}
        )
        role_doc.save(ignore_permissions=True)

        # Assign to user
        user_doc = frappe.get_doc("User", self.test_user)
        user_doc.append("roles", {"role": self.test_role})
        user_doc.save(ignore_permissions=True)

        # Get summary
        summary = role_service.get_role_summary(self.test_role)

        self.assertEqual(summary["role"], self.test_role)
        self.assertEqual(summary["permission_count"], 2)
        self.assertGreaterEqual(summary["user_count"], 1)
        self.assertIn("Orders", summary["permissions_by_category"])
        self.assertIn("Invoices", summary["permissions_by_category"])

    def _ensure_user(self, email: str) -> str:
        if frappe.db.exists("User", email):
            return email

        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": email,
                "first_name": "Roles",
                "last_name": "Test",
                "send_welcome_email": 0,
            }
        )
        user.insert(ignore_permissions=True)
        return email

    def _create_role(self, role_name: str) -> str:
        if frappe.db.exists("Role", role_name):
            return role_name

        role = frappe.get_doc(
            {
                "doctype": "Role",
                "role_name": role_name,
                "desk_access": 1,
                "is_custom_role": 1,
            }
        )
        role.insert(ignore_permissions=True)
        return role_name

    def _ensure_role_customizations(self) -> None:
        """Ensure Role DocType has custom fields and child table used by the service."""
        frappe.clear_cache(doctype="Role")
        frappe.reload_doc("permissions", "doctype", "role_permission")

        custom_fields = [
            {
                "fieldname": "custom_permissions",
                "label": "Custom Permissions",
                "fieldtype": "Table",
                "insert_after": "desk_access",
                "options": "Role Permission",
                "description": "Custom application permissions for this role",
            },
            {
                "fieldname": "is_custom_role",
                "label": "Is Custom Role",
                "fieldtype": "Check",
                "insert_after": "custom_permissions",
                "description": "Mark as custom role (not a Frappe standard role)",
                "default": "0",
            },
            {
                "fieldname": "role_description",
                "label": "Role Description",
                "fieldtype": "Small Text",
                "insert_after": "is_custom_role",
                "description": "Description of this role's purpose and permissions",
            },
        ]

        for field in custom_fields:
            if not frappe.db.exists(
                "Custom Field",
                {"dt": "Role", "fieldname": field["fieldname"]},
            ):
                doc = frappe.get_doc(
                    {
                        "doctype": "Custom Field",
                        "dt": "Role",
                        "fieldname": field["fieldname"],
                        "label": field["label"],
                        "fieldtype": field["fieldtype"],
                        "insert_after": field.get("insert_after"),
                        "options": field.get("options"),
                        "default": field.get("default"),
                        "description": field.get("description"),
                    }
                )
                doc.insert(ignore_permissions=True, ignore_if_duplicate=True)

        frappe.clear_cache(doctype="Role")
        frappe.get_meta("Role", cached=False)
