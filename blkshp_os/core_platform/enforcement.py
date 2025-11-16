"""Subscription enforcement hooks for module and feature access control.

This module provides decorators and functions for enforcing subscription-based
access control across DocTypes, API endpoints, and background jobs.

Usage Examples:
        # As a decorator for API methods:
        @frappe.whitelist()
        @require_module_access("inventory")
        def create_stock_entry():
                pass

        # As a function call in DocType controllers:
        def validate(self):
                require_module_access("procurement")

        # For feature-level enforcement:
        @require_feature_access("analytics.finance_dashboard")
        def get_financial_metrics():
                pass

        # In doc_events:
        doc_events = {
                "Stock Entry": {
                        "before_insert": "path.to.enforce_inventory_module",
                }
        }
"""

from __future__ import annotations

import functools
import json
from collections.abc import Callable
from typing import Any, TypeVar

import frappe
from frappe import _
from frappe.utils import now

from blkshp_os.permissions import service as permission_service

# Type variable for generic decorator support
F = TypeVar("F", bound=Callable[..., Any])


class SubscriptionAccessDenied(frappe.PermissionError):
    """Custom exception for subscription-based access denial.

    This exception extends frappe.PermissionError to ensure proper handling
    in the Frappe framework while providing specific context for subscription
    enforcement failures.

    Attributes:
            message: User-friendly error message
            module_key: Module key that was checked (if applicable)
            feature_key: Feature key that was checked (if applicable)
            user: User who was denied access
    """

    def __init__(
        self,
        message: str,
        module_key: str | None = None,
        feature_key: str | None = None,
        user: str | None = None,
    ):
        """Initialize the SubscriptionAccessDenied exception.

        Args:
                message: User-friendly error message
                module_key: Module key that was denied (optional)
                feature_key: Feature key that was denied (optional)
                user: User who was denied access (optional)
        """
        super().__init__(message)
        self.module_key = module_key
        self.feature_key = feature_key
        self.user = user or frappe.session.user
        self.http_status_code = 403


def _log_access_denial(
    user: str,
    access_type: str,
    access_key: str,
    context: dict[str, Any] | None = None,
    bypass_reason: str | None = None,
) -> None:
    """Log subscription access denial or admin bypass to audit trail.

    Creates a Subscription Access Log entry for audit and compliance purposes.
    This function is called automatically by enforcement helpers and should not
    typically be called directly.

    Args:
            user: User attempting access
            access_type: Either "Module" or "Feature"
            access_key: The module_key or feature_key being accessed
            context: Additional context (DocType, method, endpoint, etc.)
            bypass_reason: If admin bypassed, the reason (role) for bypass
    """
    try:
        context = context or {}

        # Get request context if available
        if frappe.request and hasattr(frappe.request, "path"):
            context.setdefault("endpoint", frappe.request.path)
            context.setdefault("method", frappe.request.method)

        # Get DocType context if in document context
        if frappe.flags.in_install or frappe.flags.in_migrate:
            return  # Don't log during install/migrate

        log_entry = {
            "doctype": "Subscription Access Log",
            "timestamp": now(),
            "user": user,
            "access_type": access_type,
            "access_key": access_key,
            "action": "Bypass" if bypass_reason else "Denied",
            "bypass_reason": bypass_reason,
            "context_data": json.dumps(context, default=str),
            "ip_address": (
                frappe.local.request_ip if hasattr(frappe.local, "request_ip") else None
            ),
        }

        # Insert without triggering additional validations
        frappe.get_doc(log_entry).insert(ignore_permissions=True)
        frappe.db.commit()

    except Exception as e:
        # Don't fail the request if logging fails
        frappe.log_error(
            title="Subscription Access Logging Failed",
            message=f"Failed to log access for user {user}: {e!s}",
        )


def require_module_access(
    module_key: str,
    user: str | None = None,
    log_denial: bool = True,
    context: dict[str, Any] | None = None,
) -> Callable[[F], F]:
    """Decorator/function to enforce module access based on subscription.

    This can be used as a decorator or called directly in code. When a tenant
    user lacks access, a SubscriptionAccessDenied exception is raised. Admin
    users (BLKSHP Operations, System Manager, Administrator) bypass enforcement
    but their actions are logged for audit purposes.

    Args:
            module_key: The module key to check (e.g., "inventory", "procurement")
            user: User to check (defaults to frappe.session.user)
            log_denial: Whether to log denied access attempts
            context: Additional context for logging (DocType, method, etc.)

    Returns:
            Decorator function or None if used as function call

    Raises:
            SubscriptionAccessDenied: If user lacks module access

    Examples:
            # As decorator:
            @frappe.whitelist()
            @require_module_access("inventory")
            def create_stock_entry():
                    return {"status": "ok"}

            # As function call:
            def validate(self):
                    require_module_access("procurement", context={"doctype": self.doctype})
    """

    def check_access(
        checked_user: str | None = None, check_context: dict[str, Any] | None = None
    ) -> None:
        """Perform the actual access check."""
        checked_user = checked_user or user or frappe.session.user
        check_context = check_context or context or {}

        # Check if user bypasses subscription gates
        if permission_service._user_bypasses_subscription_gates(checked_user):
            # Log bypass for audit trail
            if log_denial:
                bypass_roles = set(frappe.get_roles(checked_user))
                bypass_reason = ", ".join(
                    role
                    for role in permission_service.SUBSCRIPTION_BYPASS_ROLES
                    if role in bypass_roles
                )
                _log_access_denial(
                    user=checked_user,
                    access_type="Module",
                    access_key=module_key,
                    context=check_context,
                    bypass_reason=bypass_reason,
                )
            return  # Access granted

        # Check module access
        has_access = permission_service.user_has_module_access(
            checked_user, module_key, refresh=False
        )

        if not has_access:
            # Log denial
            if log_denial:
                _log_access_denial(
                    user=checked_user,
                    access_type="Module",
                    access_key=module_key,
                    context=check_context,
                )

            # Raise exception
            raise SubscriptionAccessDenied(
                message=_(
                    "Access denied: The {0} module is not enabled in your subscription plan. "
                    "Please contact your administrator to upgrade your plan."
                ).format(module_key),
                module_key=module_key,
                user=checked_user,
            )

    # If used as function call (not decorator), check immediately
    if callable(module_key):
        # This handles the case where @require_module_access is used without ()
        raise TypeError(
            "require_module_access requires a module_key argument. "
            "Use @require_module_access('module_key') instead of @require_module_access"
        )

    # Return decorator
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Build context from function metadata
            func_context = context.copy() if context else {}
            func_context.setdefault("function", func.__name__)
            func_context.setdefault("module", func.__module__)

            # Check access before executing function
            check_access(check_context=func_context)

            # Execute original function
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    # If user is provided, this is a direct call (not a decorator)
    # Execute check immediately and return no-op decorator
    if user is not None:
        check_access()
        return lambda f: f  # Return no-op decorator

    return decorator


def require_feature_access(
    feature_key: str,
    user: str | None = None,
    log_denial: bool = True,
    context: dict[str, Any] | None = None,
) -> Callable[[F], F]:
    """Decorator/function to enforce feature access based on subscription.

    Similar to require_module_access but for feature-level enforcement.
    Feature keys follow the pattern "category.feature_name" (e.g.,
    "analytics.finance_dashboard").

    Args:
            feature_key: The feature key to check (e.g., "analytics.finance_dashboard")
            user: User to check (defaults to frappe.session.user)
            log_denial: Whether to log denied access attempts
            context: Additional context for logging

    Returns:
            Decorator function or None if used as function call

    Raises:
            SubscriptionAccessDenied: If user lacks feature access

    Examples:
            # As decorator:
            @frappe.whitelist()
            @require_feature_access("analytics.finance_dashboard")
            def get_dashboard_data():
                    return {"revenue": 10000}

            # As function call:
            def get_report(self):
                    require_feature_access(
                            "procurement.ottimate_import",
                            context={"report": self.name}
                    )
    """

    def check_access(
        checked_user: str | None = None, check_context: dict[str, Any] | None = None
    ) -> None:
        """Perform the actual access check."""
        checked_user = checked_user or user or frappe.session.user
        check_context = check_context or context or {}

        # Check if user bypasses subscription gates
        if permission_service._user_bypasses_subscription_gates(checked_user):
            # Log bypass for audit trail
            if log_denial:
                bypass_roles = set(frappe.get_roles(checked_user))
                bypass_reason = ", ".join(
                    role
                    for role in permission_service.SUBSCRIPTION_BYPASS_ROLES
                    if role in bypass_roles
                )
                _log_access_denial(
                    user=checked_user,
                    access_type="Feature",
                    access_key=feature_key,
                    context=check_context,
                    bypass_reason=bypass_reason,
                )
            return  # Access granted

        # Check feature access
        has_access = permission_service.user_has_feature(
            checked_user, feature_key, refresh=False
        )

        if not has_access:
            # Log denial
            if log_denial:
                _log_access_denial(
                    user=checked_user,
                    access_type="Feature",
                    access_key=feature_key,
                    context=check_context,
                )

            # Raise exception
            raise SubscriptionAccessDenied(
                message=_(
                    "Access denied: The {0} feature is not enabled in your subscription plan. "
                    "Please contact your administrator to enable this feature."
                ).format(feature_key),
                feature_key=feature_key,
                user=checked_user,
            )

    # If used as function call (not decorator), check immediately
    if callable(feature_key):
        raise TypeError(
            "require_feature_access requires a feature_key argument. "
            "Use @require_feature_access('feature_key') instead of @require_feature_access"
        )

    # Return decorator
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Build context from function metadata
            func_context = context.copy() if context else {}
            func_context.setdefault("function", func.__name__)
            func_context.setdefault("module", func.__module__)

            # Check access before executing function
            check_access(check_context=func_context)

            # Execute original function
            return func(*args, **kwargs)

        return wrapper  # type: ignore

    # If user is provided, this is a direct call (not a decorator)
    # Execute check immediately and return no-op decorator
    if user is not None:
        check_access()
        return lambda f: f  # Return no-op decorator

    return decorator


def enforce_module_access_for_doctype(doc, method=None, module_key: str | None = None):
    """Generic doc_events hook for enforcing module access on DocType operations.

    This function can be used in hooks.py doc_events to enforce module access
    for DocType operations like before_insert, before_save, before_submit, etc.

    Args:
            doc: The document being operated on
            method: The event method (before_insert, etc.) - automatically passed by Frappe
            module_key: Module key to enforce (if None, must be set via doctype metadata)

    Example in hooks.py:
            doc_events = {
                    "Stock Entry": {
                            "before_insert": "blkshp_os.core_platform.enforcement.enforce_inventory_module",
                    }
            }

    Or with partial application:
            from functools import partial
            doc_events = {
                    "Purchase Order": {
                            "before_insert": partial(
                                    enforce_module_access_for_doctype,
                                    module_key="procurement"
                            ),
                    }
            }
    """
    if not module_key:
        # Try to get module from doctype metadata
        module_key = frappe.db.get_value("DocType", doc.doctype, "module")
        if not module_key:
            frappe.log_error(
                title="Enforcement Configuration Error",
                message=f"No module_key specified for {doc.doctype} enforcement",
            )
            return

    # Enforce module access
    require_module_access(
        module_key=module_key,
        user=frappe.session.user,  # Force immediate execution
        context={
            "doctype": doc.doctype,
            "name": doc.name,
            "event": method or "unknown",
        },
    )


def enforce_feature_access_for_doctype(
    doc, method=None, feature_key: str | None = None
):
    """Generic doc_events hook for enforcing feature access on DocType operations.

    Similar to enforce_module_access_for_doctype but for feature-level enforcement.

    Args:
            doc: The document being operated on
            method: The event method - automatically passed by Frappe
            feature_key: Feature key to enforce

    Example in hooks.py:
            from functools import partial
            doc_events = {
                    "Stock Reconciliation": {
                            "before_submit": partial(
                                    enforce_feature_access_for_doctype,
                                    feature_key="inventory.audit_workflows"
                            ),
                    }
            }
    """
    if not feature_key:
        frappe.log_error(
            title="Enforcement Configuration Error",
            message=f"No feature_key specified for {doc.doctype} enforcement",
        )
        return

    # Enforce feature access
    require_feature_access(
        feature_key=feature_key,
        user=frappe.session.user,  # Force immediate execution
        context={
            "doctype": doc.doctype,
            "name": doc.name,
            "event": method or "unknown",
        },
    )


def get_access_log_summary(
    user: str | None = None,
    access_type: str | None = None,
    action: str | None = None,
    limit: int = 100,
) -> list[dict[str, Any]]:
    """Retrieve subscription access log entries for reporting and audit.

    This function is useful for administrators to review access patterns,
    denied access attempts, and admin bypasses.

    Args:
            user: Filter by specific user
            access_type: Filter by "Module" or "Feature"
            action: Filter by "Denied" or "Bypass"
            limit: Maximum number of records to return

    Returns:
            List of access log entries with timestamps, users, and context

    Example:
            # Get all denied access attempts in last 24 hours
            from frappe.utils import add_days, now
            logs = get_access_log_summary(action="Denied", limit=1000)
            recent = [log for log in logs if log.timestamp > add_days(now(), -1)]
    """
    filters = {}
    if user:
        filters["user"] = user
    if access_type:
        filters["access_type"] = access_type
    if action:
        filters["action"] = action

    logs = frappe.get_all(
        "Subscription Access Log",
        filters=filters,
        fields=[
            "name",
            "timestamp",
            "user",
            "access_type",
            "access_key",
            "action",
            "bypass_reason",
            "context_data",
            "ip_address",
        ],
        order_by="timestamp desc",
        limit=limit,
    )

    # Parse context_data JSON
    for log in logs:
        try:
            if log.get("context_data"):
                log["context"] = json.loads(log["context_data"])
            else:
                log["context"] = {}
        except (json.JSONDecodeError, TypeError):
            log["context"] = {}

    return logs


@frappe.whitelist()
def get_my_access_logs(limit: int = 50) -> list[dict[str, Any]]:
    """API endpoint for users to view their own access log history.

    This allows users to see when they've been denied access or when
    they've accessed restricted features (if they have bypass roles).

    Args:
            limit: Maximum number of records to return

    Returns:
            List of access log entries for the current user
    """
    return get_access_log_summary(
        user=frappe.session.user,
        limit=min(int(limit), 500),  # Cap at 500
    )
