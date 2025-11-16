"""Tests for authentication API endpoints."""

from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.api import auth as auth_api
from blkshp_os.auth import jwt_manager


class TestAuthAPI(FrappeTestCase):
    """Test JWT authentication endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test user."""
        cls.test_user_email = "auth-test@example.com"
        cls.test_password = "TestPassword123!"

        # Create test user if doesn't exist
        if not frappe.db.exists("User", cls.test_user_email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": cls.test_user_email,
                "first_name": "Auth",
                "last_name": "Test",
                "send_welcome_email": 0,
                "enabled": 1,
            })
            user.insert(ignore_permissions=True)

            # Set password
            user.new_password = cls.test_password
            user.save(ignore_permissions=True)

        frappe.db.commit()

    def tearDown(self):
        """Reset session."""
        frappe.set_user("Administrator")

    def test_login_success(self):
        """Test successful login returns tokens."""
        result = auth_api.login(
            username=self.test_user_email,
            password=self.test_password
        )

        self.assertIn("access_token", result)
        self.assertIn("refresh_token", result)
        self.assertEqual(result["token_type"], "Bearer")
        self.assertIn("expires_in", result)
        self.assertIn("user", result)
        self.assertEqual(result["user"]["email"], self.test_user_email)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials fails."""
        with self.assertRaises(frappe.AuthenticationError):
            auth_api.login(
                username=self.test_user_email,
                password="WrongPassword"
            )

    def test_login_nonexistent_user(self):
        """Test login with nonexistent user fails."""
        with self.assertRaises(frappe.AuthenticationError):
            auth_api.login(
                username="nonexistent@example.com",
                password="password"
            )

    def test_token_generation(self):
        """Test JWT token generation."""
        access_token = jwt_manager.generate_access_token(self.test_user_email)
        self.assertIsInstance(access_token, str)
        self.assertTrue(len(access_token) > 0)

        refresh_token = jwt_manager.generate_refresh_token(self.test_user_email)
        self.assertIsInstance(refresh_token, str)
        self.assertTrue(len(refresh_token) > 0)

    def test_token_verification(self):
        """Test JWT token verification."""
        access_token = jwt_manager.generate_access_token(self.test_user_email)

        payload = jwt_manager.verify_token(access_token, token_type="access")

        self.assertEqual(payload["user"], self.test_user_email)
        self.assertEqual(payload["type"], "access")
        self.assertIn("exp", payload)
        self.assertIn("iat", payload)

    def test_refresh_token(self):
        """Test refreshing access token."""
        # Generate refresh token
        refresh_token = jwt_manager.generate_refresh_token(self.test_user_email)

        # Use it to get a new access token
        result = auth_api.refresh(refresh_token=refresh_token)

        self.assertIn("access_token", result)
        self.assertEqual(result["token_type"], "Bearer")
        self.assertIn("expires_in", result)

        # Verify the new access token works
        new_access_token = result["access_token"]
        payload = jwt_manager.verify_token(new_access_token, token_type="access")
        self.assertEqual(payload["user"], self.test_user_email)

    def test_refresh_with_access_token_fails(self):
        """Test that using an access token to refresh fails."""
        access_token = jwt_manager.generate_access_token(self.test_user_email)

        with self.assertRaises(frappe.AuthenticationError):
            auth_api.refresh(refresh_token=access_token)

    def test_verify_token_endpoint(self):
        """Test token verification endpoint."""
        access_token = jwt_manager.generate_access_token(self.test_user_email)

        result = auth_api.verify_token(token=access_token)

        self.assertTrue(result["valid"])
        self.assertIsNotNone(result["payload"])
        self.assertIsNone(result["error"])
        self.assertEqual(result["payload"]["user"], self.test_user_email)

    def test_verify_invalid_token(self):
        """Test verifying an invalid token."""
        result = auth_api.verify_token(token="invalid.token.here")

        self.assertFalse(result["valid"])
        self.assertIsNone(result["payload"])
        self.assertIsNotNone(result["error"])

    def test_token_info_endpoint(self):
        """Test token info endpoint."""
        access_token = jwt_manager.generate_access_token(self.test_user_email)

        info = auth_api.token_info(token=access_token)

        self.assertIn("user", info)
        self.assertIn("type", info)
        self.assertIn("exp", info)
        self.assertIn("iat", info)
        self.assertEqual(info["user"], self.test_user_email)
        self.assertEqual(info["type"], "access")

    def test_logout_endpoint(self):
        """Test logout endpoint."""
        refresh_token = jwt_manager.generate_refresh_token(self.test_user_email)

        result = auth_api.logout(refresh_token=refresh_token)

        self.assertTrue(result["success"])
        self.assertIn("message", result)

    def test_profile_endpoint_requires_auth(self):
        """Test profile endpoint requires authentication."""
        # Set user to Guest
        frappe.set_user("Guest")

        with self.assertRaises(frappe.AuthenticationError):
            auth_api.profile()

    def test_profile_endpoint_with_auth(self):
        """Test profile endpoint with authenticated user."""
        # Set user
        frappe.set_user(self.test_user_email)

        result = auth_api.profile()

        self.assertIn("user", result)
        self.assertEqual(result["user"]["email"], self.test_user_email)
        self.assertIn("full_name", result["user"])
        self.assertIn("roles", result["user"])
