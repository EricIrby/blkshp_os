"""JWT Token Manager for SPA Authentication.

Provides JWT-based authentication for single-page applications consuming
the BLKSHP OS REST APIs. Tokens are stateless and include user, company,
and permission claims.
"""

from __future__ import annotations

import datetime
from typing import Any

import frappe
import jwt
from frappe import _
from frappe.utils import get_datetime, now_datetime


# Token expiration times
ACCESS_TOKEN_EXPIRY_HOURS = 1  # Short-lived access tokens
REFRESH_TOKEN_EXPIRY_DAYS = 30  # Long-lived refresh tokens


def generate_access_token(user: str) -> str:
    """Generate a short-lived JWT access token for API requests.

    Args:
        user: User email

    Returns:
        JWT access token string

    Token includes:
        - user: User email
        - exp: Expiration timestamp
        - iat: Issued at timestamp
        - type: "access"
        - company: User's default company
        - roles: User's roles
    """
    if not frappe.db.exists("User", user):
        frappe.throw(_("User {0} does not exist").format(user))

    # Get user details
    user_doc = frappe.get_doc("User", user)

    # Get user's companies and roles
    companies = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Company"},
        pluck="for_value"
    )

    roles = [role.role for role in user_doc.roles]

    # Generate token payload
    now = now_datetime()
    expiry = now + datetime.timedelta(hours=ACCESS_TOKEN_EXPIRY_HOURS)

    payload = {
        "user": user,
        "exp": int(expiry.timestamp()),
        "iat": int(now.timestamp()),
        "type": "access",
        "companies": companies or [],
        "roles": roles,
        "full_name": user_doc.full_name,
    }

    # Get secret from site config
    secret = frappe.conf.get("jwt_secret") or frappe.conf.get("secret_key")
    if not secret:
        frappe.throw(_("JWT secret not configured. Set jwt_secret in site_config.json"))

    # Encode token
    token = jwt.encode(payload, secret, algorithm="HS256")

    return token


def generate_refresh_token(user: str) -> str:
    """Generate a long-lived JWT refresh token.

    Args:
        user: User email

    Returns:
        JWT refresh token string

    Refresh tokens are used to obtain new access tokens without re-authentication.
    They have a longer expiry time but fewer claims.
    """
    if not frappe.db.exists("User", user):
        frappe.throw(_("User {0} does not exist").format(user))

    # Generate token payload
    now = now_datetime()
    expiry = now + datetime.timedelta(days=REFRESH_TOKEN_EXPIRY_DAYS)

    payload = {
        "user": user,
        "exp": int(expiry.timestamp()),
        "iat": int(now.timestamp()),
        "type": "refresh",
    }

    # Get secret from site config
    secret = frappe.conf.get("jwt_secret") or frappe.conf.get("secret_key")
    if not secret:
        frappe.throw(_("JWT secret not configured. Set jwt_secret in site_config.json"))

    # Encode token
    token = jwt.encode(payload, secret, algorithm="HS256")

    return token


def verify_token(token: str, token_type: str = "access") -> dict[str, Any]:
    """Verify and decode a JWT token.

    Args:
        token: JWT token string
        token_type: Expected token type ("access" or "refresh")

    Returns:
        Decoded token payload

    Raises:
        jwt.ExpiredSignatureError: If token is expired
        jwt.InvalidTokenError: If token is invalid
        frappe.AuthenticationError: If token type doesn't match
    """
    # Get secret from site config
    secret = frappe.conf.get("jwt_secret") or frappe.conf.get("secret_key")
    if not secret:
        frappe.throw(_("JWT secret not configured"))

    try:
        # Decode and verify token
        payload = jwt.decode(token, secret, algorithms=["HS256"])

        # Verify token type
        if payload.get("type") != token_type:
            frappe.throw(
                _("Invalid token type. Expected {0}, got {1}").format(
                    token_type, payload.get("type")
                ),
                frappe.AuthenticationError
            )

        # Verify user still exists and is enabled
        user = payload.get("user")
        if not user or not frappe.db.exists("User", user):
            frappe.throw(_("User from token does not exist"), frappe.AuthenticationError)

        user_doc = frappe.get_doc("User", user)
        if user_doc.enabled == 0:
            frappe.throw(_("User is disabled"), frappe.AuthenticationError)

        return payload

    except jwt.ExpiredSignatureError:
        frappe.throw(_("Token has expired"), frappe.AuthenticationError)
    except jwt.InvalidTokenError as e:
        frappe.throw(_("Invalid token: {0}").format(str(e)), frappe.AuthenticationError)


def refresh_access_token(refresh_token: str) -> str:
    """Generate a new access token using a refresh token.

    Args:
        refresh_token: Valid refresh token

    Returns:
        New access token

    Raises:
        frappe.AuthenticationError: If refresh token is invalid or expired
    """
    # Verify refresh token
    payload = verify_token(refresh_token, token_type="refresh")

    user = payload.get("user")
    if not user:
        frappe.throw(_("Invalid refresh token"), frappe.AuthenticationError)

    # Generate new access token
    return generate_access_token(user)


def authenticate_request() -> str:
    """Authenticate the current request using JWT from Authorization header.

    Returns:
        Authenticated user email

    Raises:
        frappe.AuthenticationError: If authentication fails

    This function should be called at the beginning of protected endpoints to
    verify the JWT token and set the user session.
    """
    # Get Authorization header
    auth_header = frappe.get_request_header("Authorization")

    if not auth_header:
        frappe.throw(_("Authorization header missing"), frappe.AuthenticationError)

    # Extract token from "Bearer <token>" format
    parts = auth_header.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        frappe.throw(_("Invalid Authorization header format. Use: Bearer <token>"), frappe.AuthenticationError)

    token = parts[1]

    # Verify token
    payload = verify_token(token, token_type="access")

    user = payload.get("user")
    if not user:
        frappe.throw(_("Invalid token payload"), frappe.AuthenticationError)

    # Set user in session
    frappe.set_user(user)

    return user


def get_token_info(token: str) -> dict[str, Any]:
    """Get information about a token without fully authenticating.

    Args:
        token: JWT token string

    Returns:
        Dictionary with token information (user, expiry, type, etc.)

    Useful for debugging and token inspection.
    """
    try:
        # Decode without verification to inspect (for debugging only)
        # In production, always use verify_token() for actual authentication
        secret = frappe.conf.get("jwt_secret") or frappe.conf.get("secret_key")
        payload = jwt.decode(token, secret, algorithms=["HS256"], options={"verify_signature": False})

        # Calculate time until expiry
        exp_timestamp = payload.get("exp")
        if exp_timestamp:
            exp_datetime = datetime.datetime.fromtimestamp(exp_timestamp)
            time_remaining = exp_datetime - datetime.datetime.now()
            payload["expires_in_seconds"] = int(time_remaining.total_seconds())
            payload["expires_in_minutes"] = int(time_remaining.total_seconds() / 60)
            payload["is_expired"] = time_remaining.total_seconds() <= 0

        return payload
    except Exception as e:
        return {"error": str(e)}
