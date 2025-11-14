"""Test cases for Department Permission child DocType."""

from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]


class TestDepartmentPermission(FrappeTestCase):
    """Test Department Permission validation and functionality."""

    _is_doctype_reloaded = False

    def setUp(self) -> None:
        super().setUp()
        if not self.__class__._is_doctype_reloaded:
            frappe.reload_doc("permissions", "doctype", "department_permission")
            frappe.clear_cache(doctype="Department")
            frappe.reload_doc("departments", "doctype", "department")
            frappe.reload_doc("core", "doctype", "user")
            frappe.reload_doc("core", "doctype", "user_role")
            self._ensure_user_customizations()
            self.__class__._is_doctype_reloaded = True
        self.company = self._ensure_company()
        self.user = self._ensure_user("dept_perm_test@example.com")
        self.department = self._create_department("TESTDEPT", "Test Department")

    def tearDown(self) -> None:
        frappe.db.rollback()
        super().tearDown()

    def test_department_required(self) -> None:
        """Test that department field is required."""
        user_doc = frappe.get_doc("User", self.user)
        user_doc.append("department_permissions", {"can_read": 1})
        with self.assertRaises(frappe.ValidationError):
            user_doc.save(ignore_permissions=True)

    def test_at_least_one_permission_required(self) -> None:
        """Test that at least one permission flag must be set."""
        user_doc = frappe.get_doc("User", self.user)
        user_doc.append(
            "department_permissions",
            {
                "department": self.department.name,
                "can_read": 0,
                "can_write": 0,
                "can_create": 0,
                "can_delete": 0,
                "can_submit": 0,
                "can_cancel": 0,
                "can_approve": 0,
            },
        )
        with self.assertRaises(frappe.ValidationError):
            user_doc.save(ignore_permissions=True)

    def test_inactive_department_validation(self) -> None:
        """Test that inactive departments cannot be assigned."""
        self.department.is_active = 0
        self.department.save(ignore_permissions=True)

        user_doc = frappe.get_doc("User", self.user)
        user_doc.append(
            "department_permissions",
            {"department": self.department.name, "can_read": 1},
        )
        with self.assertRaises(frappe.ValidationError):
            user_doc.save(ignore_permissions=True)

    def test_duplicate_department_assignment(self) -> None:
        """Test that same department cannot be assigned twice to same user."""
        user_doc = frappe.get_doc("User", self.user)
        user_doc.append(
            "department_permissions",
            {"department": self.department.name, "can_read": 1},
        )
        user_doc.save(ignore_permissions=True)

        # Try to add same department again
        user_doc.append(
            "department_permissions",
            {"department": self.department.name, "can_write": 1},
        )
        with self.assertRaises(frappe.ValidationError):
            user_doc.save(ignore_permissions=True)

    def test_valid_date_range(self) -> None:
        """Test that valid_upto must be after valid_from."""
        user_doc = frappe.get_doc("User", self.user)
        user_doc.append(
            "department_permissions",
            {
                "department": self.department.name,
                "can_read": 1,
                "valid_from": "2025-12-31",
                "valid_upto": "2025-01-01",
            },
        )
        with self.assertRaises(frappe.ValidationError):
            user_doc.save(ignore_permissions=True)

    def test_successful_permission_assignment(self) -> None:
        """Test successful department permission assignment."""
        user_doc = frappe.get_doc("User", self.user)
        user_doc.append(
            "department_permissions",
            {
                "department": self.department.name,
                "can_read": 1,
                "can_write": 1,
                "is_active": 1,
            },
        )
        user_doc.save(ignore_permissions=True)

        # Verify saved
        user_doc.reload()
        self.assertEqual(len(user_doc.department_permissions), 1)
        self.assertEqual(
            user_doc.department_permissions[0].department, self.department.name
        )
        self.assertEqual(user_doc.department_permissions[0].can_read, 1)
        self.assertEqual(user_doc.department_permissions[0].can_write, 1)

    def _ensure_company(self, name: str = "Test Company Dept Perm") -> str:
        existing = frappe.db.exists("Company", {"company_name": name})
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

    def _ensure_user(self, email: str) -> str:
        if frappe.db.exists("User", email):
            return email

        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": email,
                "first_name": "Department",
                "last_name": "Permission Test",
                "send_welcome_email": 0,
            }
        )
        user.insert(ignore_permissions=True)
        return email

    def _create_department(self, code: str, name: str) -> frappe.Document:
        existing = frappe.db.exists(
            "Department",
            {"department_code": code, "company": self.company},
        )
        if existing:
            return frappe.get_doc("Department", existing)

        department = frappe.get_doc(
            {
                "doctype": "Department",
                "department_code": code,
                "department_name": name,
                "department_type": "Food",
                "company": self.company,
                "is_active": 1,
            }
        )
        department.insert(ignore_permissions=True)
        return department

    @classmethod
    def _ensure_user_customizations(cls) -> None:
        from frappe.custom.doctype.custom_field.custom_field import create_custom_field

        if not frappe.db.exists(
            "Custom Field",
            {"dt": "User", "fieldname": "department_permissions"},
        ):
            create_custom_field(
                "User",
                {
                    "doctype": "Custom Field",
                    "fieldname": "department_permissions",
                    "label": "Department Permissions",
                    "fieldtype": "Table",
                    "insert_after": "roles",
                    "options": "Department Permission",
                    "reqd": 0,
                },
                ignore_validate=True,
                is_system_generated=False,
            )

        frappe.clear_cache(doctype="User")
