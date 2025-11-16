"""Tests for subscription context helpers."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.core_platform.services import (
    clear_subscription_context_cache,
    get_subscription_context,
    resolve_plan_for_company,
)


class TestSubscriptionContext(FrappeTestCase):
    """Ensure subscription context aggregation behaves as expected."""

    _is_loaded = False

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        if not cls._is_loaded:
            for doctype in (
                "feature_toggle",
                "subscription_plan",
                "module_activation",
                "tenant_branding",
            ):
                frappe.reload_doc("core_platform", "doctype", doctype)
            cls._is_loaded = True

    def setUp(self) -> None:
        super().setUp()
        frappe.db.rollback()
        clear_subscription_context_cache()

    def test_resolve_plan_default(self) -> None:
        plan_code = resolve_plan_for_company(company=None)
        self.assertEqual(plan_code, "FOUNDATION")

    def test_context_includes_modules_and_features(self) -> None:
        context = get_subscription_context(plan_code="FOUNDATION", use_cache=False)
        self.assertIsNotNone(context.plan)
        self.assertIn("core", context.modules)
        self.assertTrue(context.modules["core"].is_enabled)
        self.assertIn("inventory.audit_workflows", context.feature_states)
        self.assertTrue(context.feature_states["inventory.audit_workflows"])

    def test_context_cache_reuse(self) -> None:
        context_a = get_subscription_context(plan_code="FOUNDATION")
        context_b = get_subscription_context(plan_code="FOUNDATION")
        self.assertIs(context_a, context_b)

    def test_cache_cleared_after_module_update(self) -> None:
        context_initial = get_subscription_context(plan_code="FOUNDATION")
        inventory_initial = context_initial.modules["inventory"].is_enabled

        module_name = frappe.get_value(
            "Module Activation",
            {"plan": "FOUNDATION", "module_key": "inventory"},
            "name",
        )
        self.assertIsNotNone(module_name)
        module_doc = frappe.get_doc("Module Activation", module_name)
        try:
            module_doc.is_enabled = 0 if inventory_initial else 1
            module_doc.save(ignore_permissions=True)

            context_after = get_subscription_context(plan_code="FOUNDATION")
            self.assertNotEqual(
                context_after.modules["inventory"].is_enabled,
                inventory_initial,
            )
        finally:
            module_doc.is_enabled = 1 if inventory_initial else 0
            module_doc.save(ignore_permissions=True)
