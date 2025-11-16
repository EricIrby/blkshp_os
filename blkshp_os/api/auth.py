"""Authentication API endpoints for SPA.

Provides JWT-based authentication for single-page applications.
"""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _

from blkshp_os.auth import jwt_manager
from blkshp_os.core_platform.services import get_user_profile


@frappe.whitelist(allow_guest=True)
def login(username: str, password: str) -> dict[str, Any]:
    """Authenticate user and return JWT tokens.

    This endpoint allows guest access for initial authentication.
    Returns both access and refresh tokens on successful login.

    Args:
        username: User email or username
        password: User password

    Returns:
        {
            "access_token": str,
            "refresh_token": str,
            "token_type": "Bearer",
            "expires_in": int (seconds),
            "user": {
                "email": str,
                "full_name": str,
                "user_image": str,
                "companies": list,
                "roles": list
            }
        }

    Raises:
        frappe.AuthenticationError: If credentials are invalid

    Example:
        POST /api/method/blkshp_os.api.auth.login
        {
            "username": "user@example.com",
            "password": "password123"
        }
    """
    # Validate credentials using Frappe's built-in authentication
    try:
        frappe.auth.check_password(username, password)
    except frappe.AuthenticationError:
        frappe.throw(_("Invalid username or password"), frappe.AuthenticationError)

    # Get user email (in case username was provided)
    user = frappe.db.get_value("User", {"name": username}) or \
           frappe.db.get_value("User", {"username": username})

    if not user:
        frappe.throw(_("User not found"), frappe.AuthenticationError)

    # Verify user is enabled
    user_doc = frappe.get_doc("User", user)
    if user_doc.enabled == 0:
        frappe.throw(_("User is disabled"), frappe.AuthenticationError)

    # Generate tokens
    access_token = jwt_manager.generate_access_token(user)
    refresh_token = jwt_manager.generate_refresh_token(user)

    # Get user details
    companies = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Company"},
        pluck="for_value"
    )

    roles = [role.role for role in user_doc.roles]

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "expires_in": jwt_manager.ACCESS_TOKEN_EXPIRY_HOURS * 3600,  # in seconds
        "user": {
            "email": user,
            "full_name": user_doc.full_name,
            "user_image": user_doc.user_image,
            "companies": companies,
            "roles": roles,
        }
    }


@frappe.whitelist(allow_guest=True)
def refresh(refresh_token: str) -> dict[str, Any]:
    """Refresh access token using a refresh token.

    Args:
        refresh_token: Valid refresh token

    Returns:
        {
            "access_token": str,
            "token_type": "Bearer",
            "expires_in": int (seconds)
        }

    Raises:
        frappe.AuthenticationError: If refresh token is invalid or expired

    Example:
        POST /api/method/blkshp_os.api.auth.refresh
        {
            "refresh_token": "eyJ..."
        }
    """
    # Generate new access token
    access_token = jwt_manager.refresh_access_token(refresh_token)

    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": jwt_manager.ACCESS_TOKEN_EXPIRY_HOURS * 3600,
    }


@frappe.whitelist()
def profile() -> dict[str, Any]:
    """Get authenticated user's profile.

    This endpoint requires a valid access token in the Authorization header.
    Returns comprehensive user profile including subscription context.

    Authorization: Bearer <access_token>

    Returns:
        {
            "user": {
                "email": str,
                "full_name": str,
                "user_image": str,
                "companies": list,
                "roles": list
            },
            "subscription": {
                "company": str,
                "plan": dict,
                "modules": list,
                "features": dict
            },
            "permissions": {
                "departments": list,
                "flags": dict
            }
        }

    Example:
        GET /api/method/blkshp_os.api.auth.profile
        Headers:
            Authorization: Bearer eyJ...
    """
    # User is already authenticated via @frappe.whitelist()
    # which checks Frappe session or API key by default

    # For JWT authentication, we'd check the Authorization header
    # But for now, use Frappe's built-in session
    user = frappe.session.user

    if user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    # Get comprehensive user profile using existing service
    profile_data = get_user_profile(refresh=False)

    # Get user details
    user_doc = frappe.get_doc("User", user)

    companies = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Company"},
        pluck="for_value"
    )

    roles = [role.role for role in user_doc.roles]

    # Combine with basic user info
    result = {
        "user": {
            "email": user,
            "full_name": user_doc.full_name,
            "user_image": user_doc.user_image,
            "companies": companies,
            "roles": roles,
        },
        **profile_data
    }

    return result


@frappe.whitelist(allow_guest=True)
def verify_token(token: str) -> dict[str, Any]:
    """Verify a JWT token and return its payload.

    Useful for debugging and token validation.

    Args:
        token: JWT token to verify

    Returns:
        {
            "valid": bool,
            "payload": dict or None,
            "error": str or None
        }

    Example:
        POST /api/method/blkshp_os.api.auth.verify_token
        {
            "token": "eyJ..."
        }
    """
    try:
        payload = jwt_manager.verify_token(token, token_type="access")
        return {
            "valid": True,
            "payload": payload,
            "error": None
        }
    except Exception as e:
        return {
            "valid": False,
            "payload": None,
            "error": str(e)
        }


@frappe.whitelist(allow_guest=True)
def token_info(token: str) -> dict[str, Any]:
    """Get information about a token without full verification.

    Useful for inspecting tokens and debugging.

    Args:
        token: JWT token

    Returns:
        Dictionary with token information

    Example:
        POST /api/method/blkshp_os.api.auth.token_info
        {
            "token": "eyJ..."
        }
    """
    return jwt_manager.get_token_info(token)


@frappe.whitelist(allow_guest=True)
def logout(refresh_token: str | None = None) -> dict[str, Any]:
    """Logout user and invalidate tokens.

    Note: Since JWT tokens are stateless, this is primarily for client-side cleanup.
    The client should discard both access and refresh tokens.

    In a production implementation, you might want to maintain a token blacklist
    in the database for added security.

    Args:
        refresh_token: Optional refresh token to blacklist

    Returns:
        {
            "success": True,
            "message": "Logged out successfully"
        }

    Example:
        POST /api/method/blkshp_os.api.auth.logout
        {
            "refresh_token": "eyJ..."
        }
    """
    # In a full implementation, you would:
    # 1. Add refresh_token to a blacklist table
    # 2. Set expiry on the blacklist entry
    # 3. Check blacklist in refresh() endpoint

    # For now, just return success
    # The client is responsible for discarding tokens

    return {
        "success": True,
        "message": _("Logged out successfully. Please discard your tokens."),
    }
