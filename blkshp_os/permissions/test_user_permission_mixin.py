"""Tests for the UserPermissionMixin subscription helpers."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.core_platform.services import clear_subscription_context_cache


class TestUserPermissionMixinSubscription(FrappeTestCase):
    """Validate the subscription-aware helpers built into the user mixin."""

    _is_loaded = False

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not cls._is_loaded:
            for module, doctype in [
                ("core_platform", "feature_toggle"),
                ("core_platform", "subscription_plan"),
                ("core_platform", "module_activation"),
                ("core_platform", "tenant_branding"),
                ("permissions", "department_permission"),
            ]:
                frappe.reload_doc(module, "doctype", doctype)
            cls._is_loaded = True

    def setUp(self) -> None:
        super().setUp()
        frappe.db.rollback()
        clear_subscription_context_cache()

    def test_standard_user_inherits_plan_features(self) -> None:
        self._ensure_role("Employee")
        company = self._create_company("Test Hospitality", "TH", "USD")
        department = self._create_department("Test Hospitality", "DEP-TH", company.name)
        self._create_tenant_branding(company.name, "FOUNDATION")

        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": "foundation.user@example.com",
                "first_name": "Foundation",
                "send_welcome_email": 0,
                "time_zone": "UTC",
            }
        )
        user.append("roles", {"role": "Employee"})
        user.company = company.name
        user.append(
            "department_permissions",
            {
                "department": department.name,
                "can_read": 1,
            },
        )
        user.insert(ignore_permissions=True)

        user_doc = frappe.get_doc("User", user.name)
        self.assertEqual(user_doc.get_company(), company.name)
        self.assertEqual(user_doc.get_subscription_plan_code(), "FOUNDATION")
        self.assertTrue(user_doc.is_module_enabled("core"))
        self.assertTrue(user_doc.is_module_enabled("inventory"))
        self.assertTrue(user_doc.is_feature_enabled("core.workspace.access"))
        self.assertTrue(user_doc.is_feature_enabled("inventory.audit_workflows"))
        self.assertFalse(user_doc.is_module_enabled("nonexistent-module"))
        self.assertFalse(user_doc.is_feature_enabled("nonexistent.feature"))

    def test_internal_operator_bypasses_gating(self) -> None:
        self._ensure_role("System Manager")
        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": "ops@example.com",
                "first_name": "Ops",
                "send_welcome_email": 0,
                "time_zone": "UTC",
            }
        )
        user.append("roles", {"role": "System Manager"})
        user.insert(ignore_permissions=True)

        user_doc = frappe.get_doc("User", user.name)
        self.assertTrue(user_doc.is_module_enabled("nonexistent-module"))
        self.assertTrue(user_doc.is_feature_enabled("imaginary.feature"))

    def _create_company(self, company_name: str, abbr: str, default_currency: str):
        existing = frappe.db.exists("Company", company_name)
        if existing:
            return frappe.get_doc("Company", existing)
        company = frappe.get_doc(
            {
                "doctype": "Company",
                "company_name": company_name,
                "abbr": abbr,
                "default_currency": default_currency,
            }
        )
        return company.insert(ignore_permissions=True)

    def _create_department(
        self, department_name: str, department_code: str, company: str
    ):
        existing = frappe.db.exists(
            "Department", {"department_code": department_code, "company": company}
        )
        if existing:
            return frappe.get_doc("Department", existing)
        department = frappe.get_doc(
            {
                "doctype": "Department",
                "department_name": department_name,
                "department_code": department_code,
                "department_type": "Other",
                "company": company,
                "is_active": 1,
            }
        )
        return department.insert(ignore_permissions=True)

    def _create_tenant_branding(self, company: str, plan: str) -> None:
        if frappe.db.exists("Tenant Branding", company):
            branding = frappe.get_doc("Tenant Branding", company)
            branding.plan = plan
            branding.save(ignore_permissions=True)
            return
        branding = frappe.get_doc(
            {
                "doctype": "Tenant Branding",
                "company": company,
                "plan": plan,
                "theme_name": "Default",
            }
        )
        branding.insert(ignore_permissions=True)

    def _ensure_role(self, role_name: str) -> None:
        if frappe.db.exists("Role", role_name):
            return
        role = frappe.get_doc({"doctype": "Role", "role_name": role_name})
        role.insert(ignore_permissions=True)
