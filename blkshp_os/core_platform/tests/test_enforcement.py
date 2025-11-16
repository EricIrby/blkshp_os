"""Comprehensive tests for subscription enforcement hooks."""

from __future__ import annotations

import unittest
from unittest.mock import MagicMock, patch

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.core_platform.enforcement import (
    SubscriptionAccessDenied,
    enforce_feature_access_for_doctype,
    enforce_module_access_for_doctype,
    get_access_log_summary,
    require_feature_access,
    require_module_access,
)


class TestSubscriptionEnforcement(FrappeTestCase):
    """Test suite for subscription enforcement functionality."""

    def setUp(self):
        """Set up test fixtures."""
        # Ensure we're running as Administrator
        frappe.set_user("Administrator")

        # Clear any existing test users
        for user_email in ["tenant_user@test.com", "admin_user@test.com"]:
            if frappe.db.exists("User", user_email):
                frappe.delete_doc("User", user_email, force=True, ignore_permissions=True)

        # Create test tenant user
        self.tenant_user = frappe.get_doc(
            {
                "doctype": "User",
                "email": "tenant_user@test.com",
                "first_name": "Tenant",
                "last_name": "User",
                "enabled": 1,
                "send_welcome_email": 0,
            }
        ).insert(ignore_permissions=True)

        # Assign basic role to tenant user
        self.tenant_user.add_roles("Sales User")

        # Create test admin user
        self.admin_user = frappe.get_doc(
            {
                "doctype": "User",
                "email": "admin_user@test.com",
                "first_name": "Admin",
                "last_name": "User",
                "enabled": 1,
                "send_welcome_email": 0,
            }
        ).insert(ignore_permissions=True)

        # Assign BLKSHP Operations role
        self.admin_user.add_roles("BLKSHP Operations")

        frappe.db.commit()

    def tearDown(self):
        """Clean up test data."""
        # Ensure we're running as Administrator
        frappe.set_user("Administrator")

        # Delete test users
        for user_email in ["tenant_user@test.com", "admin_user@test.com"]:
            if frappe.db.exists("User", user_email):
                frappe.delete_doc("User", user_email, force=True, ignore_permissions=True)

        # Clear access logs
        frappe.db.delete("Subscription Access Log")
        frappe.db.commit()

    def test_module_enforcement_blocks_tenant_user(self):
        """Test that module enforcement blocks tenant users without access."""
        with patch(
            "blkshp_os.permissions.service.user_has_module_access"
        ) as mock_access:
            mock_access.return_value = False

            with self.assertRaises(SubscriptionAccessDenied) as context:
                require_module_access(
                    "inventory",
                    user=self.tenant_user.email,
                    log_denial=True,
                )

            # Verify exception details
            self.assertEqual(context.exception.module_key, "inventory")
            self.assertEqual(context.exception.user, self.tenant_user.email)
            self.assertIn("inventory", str(context.exception))

            # Verify access log was created
            logs = frappe.get_all(
                "Subscription Access Log",
                filters={
                    "user": self.tenant_user.email,
                    "access_type": "Module",
                    "access_key": "inventory",
                    "action": "Denied",
                },
                limit=1,
            )
            self.assertEqual(len(logs), 1)

    def test_feature_enforcement_blocks_tenant_user(self):
        """Test that feature enforcement blocks tenant users without access."""
        with patch("blkshp_os.permissions.service.user_has_feature") as mock_access:
            mock_access.return_value = False

            with self.assertRaises(SubscriptionAccessDenied) as context:
                require_feature_access(
                    "analytics.finance_dashboard",
                    user=self.tenant_user.email,
                    log_denial=True,
                )

            # Verify exception details
            self.assertEqual(
                context.exception.feature_key, "analytics.finance_dashboard"
            )
            self.assertEqual(context.exception.user, self.tenant_user.email)
            self.assertIn("analytics.finance_dashboard", str(context.exception))

            # Verify access log was created
            logs = frappe.get_all(
                "Subscription Access Log",
                filters={
                    "user": self.tenant_user.email,
                    "access_type": "Feature",
                    "access_key": "analytics.finance_dashboard",
                    "action": "Denied",
                },
                limit=1,
            )
            self.assertEqual(len(logs), 1)

    def test_admin_bypass_with_logging(self):
        """Test that BLKSHP Operations users bypass enforcement with logging."""
        with patch(
            "blkshp_os.permissions.service._user_bypasses_subscription_gates"
        ) as mock_bypass:
            mock_bypass.return_value = True

            # Should not raise exception
            try:
                require_module_access(
                    "inventory",
                    user=self.admin_user.email,
                    log_denial=True,
                )
            except SubscriptionAccessDenied:
                self.fail("Admin user should bypass enforcement")

            # Verify bypass was logged
            logs = frappe.get_all(
                "Subscription Access Log",
                filters={
                    "user": self.admin_user.email,
                    "access_type": "Module",
                    "access_key": "inventory",
                    "action": "Bypass",
                },
                limit=1,
            )
            self.assertEqual(len(logs), 1)

            # Verify bypass reason is logged
            log = frappe.get_doc("Subscription Access Log", logs[0].name)
            self.assertIsNotNone(log.bypass_reason)
            self.assertIn("BLKSHP Operations", log.bypass_reason)

    def test_api_enforcement_decorator(self):
        """Test that decorator works on whitelisted methods."""

        @frappe.whitelist()
        @require_module_access("procurement")
        def test_api_method():
            return {"status": "success"}

        with patch(
            "blkshp_os.permissions.service.user_has_module_access"
        ) as mock_access:
            # Set session user
            frappe.set_user(self.tenant_user.email)

            # Test blocked access
            mock_access.return_value = False
            with self.assertRaises(SubscriptionAccessDenied):
                test_api_method()

            # Test allowed access
            mock_access.return_value = True
            result = test_api_method()
            self.assertEqual(result["status"], "success")

    def test_feature_decorator_on_function(self):
        """Test feature decorator on regular functions."""

        @require_feature_access("products.bulk_operations")
        def bulk_update_products():
            return "updated"

        with patch("blkshp_os.permissions.service.user_has_feature") as mock_access:
            frappe.set_user(self.tenant_user.email)

            # Test blocked access
            mock_access.return_value = False
            with self.assertRaises(SubscriptionAccessDenied):
                bulk_update_products()

            # Test allowed access
            mock_access.return_value = True
            result = bulk_update_products()
            self.assertEqual(result, "updated")

    def test_doctype_hook_enforcement(self):
        """Test that DocType event hooks work correctly."""
        # Create a mock document
        mock_doc = MagicMock()
        mock_doc.doctype = "Stock Entry"
        mock_doc.name = "TEST-SE-001"

        with patch(
            "blkshp_os.permissions.service.user_has_module_access"
        ) as mock_access:
            frappe.set_user(self.tenant_user.email)

            # Test module enforcement blocks
            mock_access.return_value = False
            with self.assertRaises(SubscriptionAccessDenied):
                enforce_module_access_for_doctype(
                    mock_doc,
                    method="before_insert",
                    module_key="inventory",
                )

            # Test module enforcement allows
            mock_access.return_value = True
            try:
                enforce_module_access_for_doctype(
                    mock_doc,
                    method="before_insert",
                    module_key="inventory",
                )
            except SubscriptionAccessDenied:
                self.fail("Should not raise exception when user has access")

    def test_feature_hook_enforcement(self):
        """Test feature-level DocType hook enforcement."""
        mock_doc = MagicMock()
        mock_doc.doctype = "Stock Reconciliation"
        mock_doc.name = "TEST-SR-001"

        with patch("blkshp_os.permissions.service.user_has_feature") as mock_access:
            frappe.set_user(self.tenant_user.email)

            # Test feature enforcement blocks
            mock_access.return_value = False
            with self.assertRaises(SubscriptionAccessDenied):
                enforce_feature_access_for_doctype(
                    mock_doc,
                    method="before_submit",
                    feature_key="inventory.audit_workflows",
                )

            # Test feature enforcement allows
            mock_access.return_value = True
            try:
                enforce_feature_access_for_doctype(
                    mock_doc,
                    method="before_submit",
                    feature_key="inventory.audit_workflows",
                )
            except SubscriptionAccessDenied:
                self.fail("Should not raise exception when user has access")

    def test_direct_function_call_enforcement(self):
        """Test enforcement when called directly (not as decorator)."""
        with patch(
            "blkshp_os.permissions.service.user_has_module_access"
        ) as mock_access:
            frappe.set_user(self.tenant_user.email)

            # Test that it raises when called directly
            mock_access.return_value = False
            with self.assertRaises(SubscriptionAccessDenied):
                require_module_access(
                    "procurement",
                    user=self.tenant_user.email,
                    context={"doctype": "Purchase Order", "name": "PO-001"},
                )

    def test_context_data_logging(self):
        """Test that context data is properly logged."""
        context = {
            "doctype": "Purchase Order",
            "name": "PO-001",
            "event": "before_submit",
        }

        with patch(
            "blkshp_os.permissions.service.user_has_module_access"
        ) as mock_access:
            mock_access.return_value = False

            try:
                require_module_access(
                    "procurement",
                    user=self.tenant_user.email,
                    log_denial=True,
                    context=context,
                )
            except SubscriptionAccessDenied:
                pass

            # Verify context was logged
            logs = frappe.get_all(
                "Subscription Access Log",
                filters={
                    "user": self.tenant_user.email,
                    "access_key": "procurement",
                },
                fields=["name", "context_data"],
                limit=1,
            )

            self.assertEqual(len(logs), 1)
            log = frappe.get_doc("Subscription Access Log", logs[0].name)

            # Parse and verify context
            import json

            logged_context = json.loads(log.context_data)
            self.assertEqual(logged_context["doctype"], "Purchase Order")
            self.assertEqual(logged_context["name"], "PO-001")
            self.assertEqual(logged_context["event"], "before_submit")

    def test_get_access_log_summary(self):
        """Test access log summary retrieval function."""
        # Create some test logs
        with patch(
            "blkshp_os.permissions.service.user_has_module_access"
        ) as mock_access:
            mock_access.return_value = False

            # Create multiple denied access attempts
            for module in ["inventory", "procurement", "analytics"]:
                try:
                    require_module_access(
                        module,
                        user=self.tenant_user.email,
                        log_denial=True,
                    )
                except SubscriptionAccessDenied:
                    pass

        # Test retrieval
        logs = get_access_log_summary(
            user=self.tenant_user.email,
            access_type="Module",
            action="Denied",
            limit=10,
        )

        self.assertGreaterEqual(len(logs), 3)
        for log in logs:
            self.assertEqual(log["user"], self.tenant_user.email)
            self.assertEqual(log["access_type"], "Module")
            self.assertEqual(log["action"], "Denied")

    def test_no_logging_when_disabled(self):
        """Test that logging can be disabled."""
        with patch(
            "blkshp_os.permissions.service.user_has_module_access"
        ) as mock_access:
            mock_access.return_value = False

            # Count logs before
            logs_before = frappe.db.count("Subscription Access Log")

            try:
                require_module_access(
                    "inventory",
                    user=self.tenant_user.email,
                    log_denial=False,  # Disabled logging
                )
            except SubscriptionAccessDenied:
                pass

            # Count logs after
            logs_after = frappe.db.count("Subscription Access Log")

            # Should not have created a log
            self.assertEqual(logs_before, logs_after)

    def test_exception_attributes(self):
        """Test that SubscriptionAccessDenied exception has correct attributes."""
        exception = SubscriptionAccessDenied(
            message="Access denied",
            module_key="inventory",
            feature_key=None,
            user="test@example.com",
        )

        self.assertEqual(exception.module_key, "inventory")
        self.assertIsNone(exception.feature_key)
        self.assertEqual(exception.user, "test@example.com")
        self.assertEqual(exception.http_status_code, 403)
        self.assertIsInstance(exception, frappe.PermissionError)

    def test_system_manager_bypass(self):
        """Test that System Manager role also bypasses enforcement."""
        # Create system manager user
        sys_manager = frappe.get_doc(
            {
                "doctype": "User",
                "email": "sysmanager@test.com",
                "first_name": "System",
                "last_name": "Manager",
                "enabled": 1,
                "send_welcome_email": 0,
            }
        ).insert(ignore_permissions=True)
        sys_manager.add_roles("System Manager")
        frappe.db.commit()

        with patch(
            "blkshp_os.permissions.service._user_bypasses_subscription_gates"
        ) as mock_bypass:
            mock_bypass.return_value = True

            # Should not raise exception
            try:
                require_module_access(
                    "inventory",
                    user=sys_manager.email,
                    log_denial=True,
                )
            except SubscriptionAccessDenied:
                self.fail("System Manager should bypass enforcement")

        # Cleanup
        frappe.delete_doc("User", sys_manager.email, force=True)
        frappe.db.commit()

    def test_administrator_bypass(self):
        """Test that Administrator bypasses enforcement."""
        with patch(
            "blkshp_os.permissions.service._user_bypasses_subscription_gates"
        ) as mock_bypass:
            mock_bypass.return_value = True

            # Should not raise exception
            try:
                require_module_access(
                    "inventory",
                    user="Administrator",
                    log_denial=True,
                )
            except SubscriptionAccessDenied:
                self.fail("Administrator should bypass enforcement")

    def test_decorator_without_parentheses_raises_error(self):
        """Test that using decorator without () raises helpful error."""
        with self.assertRaises(TypeError) as context:
            # This should raise TypeError
            @require_module_access
            def test_func():
                pass

        self.assertIn("requires a module_key argument", str(context.exception))

    def test_multiple_enforcement_checks(self):
        """Test multiple enforcement checks in sequence."""

        @require_module_access("inventory")
        @require_feature_access("inventory.audit_workflows")
        def complex_operation():
            return "success"

        with (
            patch(
                "blkshp_os.permissions.service.user_has_module_access"
            ) as mock_module,
            patch("blkshp_os.permissions.service.user_has_feature") as mock_feature,
        ):

            frappe.set_user(self.tenant_user.email)

            # Both allowed
            mock_module.return_value = True
            mock_feature.return_value = True
            result = complex_operation()
            self.assertEqual(result, "success")

            # Module denied
            mock_module.return_value = False
            mock_feature.return_value = True
            with self.assertRaises(SubscriptionAccessDenied) as context:
                complex_operation()
            self.assertIsNotNone(context.exception.module_key)

            # Feature denied (but module allowed)
            mock_module.return_value = True
            mock_feature.return_value = False
            with self.assertRaises(SubscriptionAccessDenied) as context:
                complex_operation()
            self.assertIsNotNone(context.exception.feature_key)


def run_tests():
    """Helper function to run enforcement tests."""
    unittest.main()


if __name__ == "__main__":
    run_tests()
