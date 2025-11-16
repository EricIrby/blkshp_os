"""Tests for permission service helpers."""

from __future__ import annotations

import json

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]

from blkshp_os.core_platform.services import clear_subscription_context_cache
from blkshp_os.permissions import service


class TestPermissionService(FrappeTestCase):
    """Exercise the department permission helper functions."""

    _is_doctype_reloaded = False

    def setUp(self) -> None:
        super().setUp()
        if not self.__class__._is_doctype_reloaded:
            frappe.clear_cache(doctype="Department")
            frappe.reload_doc("departments", "doctype", "department")
            for doctype in (
                "feature_toggle",
                "subscription_plan",
                "module_activation",
                "tenant_branding",
            ):
                frappe.reload_doc("core_platform", "doctype", doctype)
            self.__class__._is_doctype_reloaded = True
        clear_subscription_context_cache()
        self.company = self._ensure_company()
        self.user = self._ensure_user("permission_service@example.com")
        self.kitchen = self._create_department("KITCHEN", "Kitchen")
        self.bar = self._create_department("BAR", "Bar")

    def tearDown(self) -> None:
        frappe.db.rollback()
        super().tearDown()

    def test_permission_flags_constant(self) -> None:
        flags = service.get_permission_flags()
        self.assertIn("can_read", flags)
        self.assertIn("can_write", flags)
        self.assertEqual(len(flags), len(set(flags)))

    def test_get_accessible_departments_returns_active_departments(self) -> None:
        self._create_department_permission(self.kitchen.name, can_read=1)
        self._create_department_permission(self.bar.name, can_read=1, can_write=1)

        self.bar.is_active = 0
        self.bar.save(ignore_permissions=True)

        departments = service.get_accessible_departments(self.user)
        self.assertEqual(departments, [self.kitchen.name])

        all_departments = service.get_accessible_departments(
            self.user, include_inactive=True
        )
        self.assertCountEqual(all_departments, [self.kitchen.name, self.bar.name])

    def test_has_department_permission_checks_flag(self) -> None:
        self._create_department_permission(self.kitchen.name, can_read=1)
        self.assertTrue(service.has_department_permission(self.user, self.kitchen.name))
        self.assertFalse(
            service.has_department_permission(self.user, self.kitchen.name, "can_write")
        )

    def test_system_manager_bypasses_department_restrictions(self) -> None:
        user_doc = frappe.get_doc("User", self.user)
        user_doc.add_roles("System Manager")

        departments = service.get_accessible_departments(self.user)
        self.assertIn(self.kitchen.name, departments)
        self.assertIn(self.bar.name, departments)

    def test_get_user_company(self) -> None:
        # Create department permission so user has an accessible department
        self._create_department_permission(self.kitchen.name, can_read=1)
        # The get_company method will find the company from the accessible department
        self.assertEqual(service.get_user_company(self.user), self.company)

    def test_user_has_module_and_feature_access(self) -> None:
        self._ensure_role("Employee")
        user_doc = frappe.get_doc("User", self.user)
        user_doc.company = self.company
        user_doc.add_roles("Employee")
        user_doc.save(ignore_permissions=True)

        self._create_tenant_branding(self.company, "FOUNDATION")

        self.assertTrue(service.user_has_module_access(self.user, "core"))
        self.assertTrue(service.user_has_feature(self.user, "core.workspace.access"))
        self.assertFalse(
            service.user_has_module_access(self.user, "nonexistent-module")
        )
        self.assertFalse(service.user_has_feature(self.user, "nonexistent.feature"))

    def test_operations_role_bypasses_feature_checks(self) -> None:
        self._ensure_role("System Manager")
        user_doc = frappe.get_doc("User", self.user)
        user_doc.company = None
        user_doc.add_roles("System Manager")
        user_doc.save(ignore_permissions=True)

        self.assertTrue(service.user_has_module_access(self.user, "imaginary-module"))
        self.assertTrue(service.user_has_feature(self.user, "imaginary.feature"))

    def _ensure_company(self, name: str = "Permissions Test Company") -> str:
        existing = frappe.db.exists("Company", {"company_name": name})
        if existing:
            return existing

        company = frappe.get_doc(
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
        company.insert(ignore_permissions=True)
        return company.name

    def _ensure_user(self, email: str) -> str:
        if frappe.db.exists("User", email):
            return email

        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": email,
                "first_name": "Permissions",
                "last_name": "Tester",
                "send_welcome_email": 0,
            }
        )
        user.insert(ignore_permissions=True)
        return email

    def _create_department(self, code: str, name: str) -> frappe.Document:
        department = frappe.get_doc(
            {
                "doctype": "Department",
                "department_code": code,
                "department_name": name,
                "department_type": "Food",
                "company": self.company,
                "settings": json.dumps({"custom_settings": {}}),
            }
        )
        department.insert(ignore_permissions=True)
        return department

    def _create_department_permission(self, department: str, **flags: int) -> None:
        default_flags = {flag: 0 for flag in service.get_permission_flags()}
        default_flags.update(flags)
        permission = frappe.get_doc(
            {
                "doctype": "Department Permission",
                "parent": self.user,
                "parenttype": "User",
                "parentfield": "department_permissions",
                "department": department,
                **default_flags,
            }
        )
        permission.insert(ignore_permissions=True)

    def _create_tenant_branding(self, company: str, plan: str) -> None:
        if frappe.db.exists("Tenant Branding", company):
            doc = frappe.get_doc("Tenant Branding", company)
            doc.plan = plan
            doc.save(ignore_permissions=True)
            return
        doc = frappe.get_doc(
            {
                "doctype": "Tenant Branding",
                "company": company,
                "plan": plan,
                "theme_name": "Default",
            }
        )
        doc.insert(ignore_permissions=True)

    def _ensure_role(self, role_name: str) -> None:
        if frappe.db.exists("Role", role_name):
            return
        role = frappe.get_doc({"doctype": "Role", "role_name": role_name})
        role.insert(ignore_permissions=True)
