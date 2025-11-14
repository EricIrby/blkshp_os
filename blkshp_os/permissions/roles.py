"""Role management service for BLKSHP OS.

This module provides functions for managing roles and checking role-based permissions.
"""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _

from blkshp_os.permissions.constants import (
    ALL_PERMISSIONS,
    PERMISSION_CATEGORIES,
    get_permission,
    is_valid_permission,
)


def get_user_roles(user: str | None = None) -> list[str]:
    """Get list of roles assigned to a user."""
    if not user:
        user = frappe.session.user

    return frappe.get_roles(user)


def has_role(user: str | None = None, role: str | None = None) -> bool:
    """Check if user has a specific role."""
    if not role:
        return False

    roles = get_user_roles(user)
    return role in roles


def get_role_permissions(role: str) -> list[dict[str, Any]]:
    """Get all custom permissions for a role."""
    if not frappe.db.exists("Role", role):
        return []

    return frappe.get_all(
        "Role Permission",
        filters={"parent": role, "parenttype": "Role", "is_granted": 1},
        fields=[
            "permission_code",
            "permission_name",
            "permission_category",
            "description",
            "department_restricted",
        ],
        order_by="permission_category asc, permission_name asc",
    )


def get_user_permissions(user: str | None = None) -> dict[str, list[dict[str, Any]]]:
    """
    Get all permissions for a user from all their roles.

    Returns dictionary with permission codes as keys and list of roles granting that permission.
    """
    if not user:
        user = frappe.session.user

    roles = get_user_roles(user)
    if not roles:
        return {}

    # Get all role permissions for user's roles
    role_perms = frappe.get_all(
        "Role Permission",
        filters={"parent": ["in", roles], "parenttype": "Role", "is_granted": 1},
        fields=[
            "parent as role",
            "permission_code",
            "permission_name",
            "permission_category",
            "department_restricted",
        ],
    )

    # Group by permission code
    permissions: dict[str, list[dict[str, Any]]] = {}
    for perm in role_perms:
        code = perm["permission_code"]
        if code not in permissions:
            permissions[code] = []
        permissions[code].append(perm)

    return permissions


def has_permission(user: str | None = None, permission_code: str | None = None) -> bool:
    """
    Check if user has a specific permission.

    Args:
            user: User email (defaults to current user)
            permission_code: Permission code to check

    Returns:
            True if user has the permission through any of their roles
    """
    if not user:
        user = frappe.session.user

    if not permission_code:
        return False

    # System Manager and Administrator have all permissions
    if has_role(user, "System Manager") or has_role(user, "Administrator"):
        return True

    # Validate permission code
    if not is_valid_permission(permission_code):
        return False

    # Check if user has permission through any role
    roles = get_user_roles(user)
    if not roles:
        return False

    count = frappe.db.count(
        "Role Permission",
        filters={
            "parent": ["in", roles],
            "parenttype": "Role",
            "permission_code": permission_code,
            "is_granted": 1,
        },
    )

    return count > 0


def has_any_permission(
    user: str | None = None, permission_codes: list[str] | None = None
) -> bool:
    """Check if user has any of the specified permissions."""
    if not user:
        user = frappe.session.user

    if not permission_codes:
        return False

    # System Manager and Administrator have all permissions
    if has_role(user, "System Manager") or has_role(user, "Administrator"):
        return True

    for code in permission_codes:
        if has_permission(user, code):
            return True

    return False


def has_all_permissions(
    user: str | None = None, permission_codes: list[str] | None = None
) -> bool:
    """Check if user has all of the specified permissions."""
    if not user:
        user = frappe.session.user

    if not permission_codes:
        return True

    # System Manager and Administrator have all permissions
    if has_role(user, "System Manager") or has_role(user, "Administrator"):
        return True

    for code in permission_codes:
        if not has_permission(user, code):
            return False

    return True


def get_permissions_by_category(
    user: str | None = None,
) -> dict[str, list[dict[str, Any]]]:
    """Get user's permissions grouped by category."""
    if not user:
        user = frappe.session.user

    permissions = get_user_permissions(user)

    # Group by category
    by_category: dict[str, list[dict[str, Any]]] = {
        cat: [] for cat in PERMISSION_CATEGORIES
    }

    for code, perm_list in permissions.items():
        if perm_list:
            category = perm_list[0].get("permission_category", "Other")
            if category not in by_category:
                by_category[category] = []

            perm_def = get_permission(code)
            if perm_def:
                by_category[category].append(
                    {
                        "code": code,
                        "name": perm_def["name"],
                        "description": perm_def["description"],
                        "department_restricted": perm_def["department_restricted"],
                        "granted_by_roles": [p["role"] for p in perm_list],
                    }
                )

    # Remove empty categories
    return {k: v for k, v in by_category.items() if v}


def create_role(
    role_name: str, permissions: list[str] | None = None, description: str | None = None
) -> frappe.Document:
    """
    Create a new custom role with specified permissions.

    Args:
            role_name: Name of the role
            permissions: List of permission codes to grant
            description: Optional description of the role

    Returns:
            Created Role document
    """
    if frappe.db.exists("Role", role_name):
        frappe.throw(_("Role {0} already exists").format(role_name))

    role = frappe.get_doc(
        {
            "doctype": "Role",
            "role_name": role_name,
            "is_custom_role": 1,
            "role_description": description or "",
            "desk_access": 1,
        }
    )

    # Add permissions
    if permissions:
        for perm_code in permissions:
            if not is_valid_permission(perm_code):
                frappe.msgprint(_("Skipping invalid permission: {0}").format(perm_code))
                continue

            role.append(
                "custom_permissions", {"permission_code": perm_code, "is_granted": 1}
            )

    role.insert(ignore_permissions=True)
    return role


def update_role_permissions(
    role: str, permissions: list[str], replace: bool = False
) -> frappe.Document:
    """
    Update permissions for a role.

    Args:
            role: Role name
            permissions: List of permission codes
            replace: If True, replace all permissions. If False, add to existing.

    Returns:
            Updated Role document
    """
    role_doc = frappe.get_doc("Role", role)

    if replace:
        # Clear existing permissions
        role_doc.custom_permissions = []

    # Add new permissions
    existing_codes = {p.permission_code for p in role_doc.custom_permissions}

    for perm_code in permissions:
        if not is_valid_permission(perm_code):
            frappe.msgprint(_("Skipping invalid permission: {0}").format(perm_code))
            continue

        if perm_code not in existing_codes:
            role_doc.append(
                "custom_permissions", {"permission_code": perm_code, "is_granted": 1}
            )

    role_doc.save(ignore_permissions=True)
    return role_doc


def revoke_role_permission(role: str, permission_code: str) -> frappe.Document:
    """Revoke a specific permission from a role."""
    role_doc = frappe.get_doc("Role", role)

    # Find and remove the permission
    to_remove = []
    for idx, perm in enumerate(role_doc.custom_permissions):
        if perm.permission_code == permission_code:
            to_remove.append(idx)

    # Remove in reverse order to maintain indices
    for idx in reversed(to_remove):
        role_doc.remove(role_doc.custom_permissions[idx])

    role_doc.save(ignore_permissions=True)
    return role_doc


def get_available_permissions() -> list[dict[str, Any]]:
    """Get list of all available permissions."""
    return [
        {
            "code": perm["code"],
            "name": perm["name"],
            "description": perm["description"],
            "category": perm["category"],
            "department_restricted": perm["department_restricted"],
        }
        for perm in ALL_PERMISSIONS
    ]


def get_role_summary(role: str) -> dict[str, Any]:
    """Get summary information about a role."""
    if not frappe.db.exists("Role", role):
        frappe.throw(_("Role {0} does not exist").format(role))

    role_doc = frappe.get_doc("Role", role)

    # Count users with this role
    user_count = frappe.db.count(
        "Has Role", filters={"role": role, "parenttype": "User"}
    )

    # Get permission count
    permission_count = len(role_doc.custom_permissions or [])

    # Get permissions by category
    perms_by_category: dict[str, int] = {}
    for perm in role_doc.custom_permissions or []:
        perm_def = get_permission(perm.permission_code)
        if perm_def:
            category = perm_def["category"]
            perms_by_category[category] = perms_by_category.get(category, 0) + 1

    return {
        "role": role,
        "description": (
            role_doc.role_description if hasattr(role_doc, "role_description") else ""
        ),
        "is_custom": (
            role_doc.is_custom_role if hasattr(role_doc, "is_custom_role") else False
        ),
        "user_count": user_count,
        "permission_count": permission_count,
        "permissions_by_category": perms_by_category,
    }
