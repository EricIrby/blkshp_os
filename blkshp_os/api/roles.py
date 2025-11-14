"""REST API endpoints for Role and Permission operations."""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _

from blkshp_os.permissions import roles as role_service
from blkshp_os.permissions.constants import (
    ALL_PERMISSIONS,
    PERMISSION_CATEGORIES,
    get_permission,
)
from blkshp_os.permissions.constants import (
    get_permissions_by_category as get_perms_by_cat,
)


@frappe.whitelist()
def get_available_permissions() -> list[dict[str, Any]]:
    """
    Get list of all available permissions.

    Returns:
            List of permission definitions
    """
    return role_service.get_available_permissions()


@frappe.whitelist()
def get_permissions_by_category(
    category: str | None = None,
) -> dict[str, list[dict[str, Any]]] | list[dict[str, Any]]:
    """
    Get permissions grouped by category or for a specific category.

    Args:
            category: Optional category name

    Returns:
            Dictionary of permissions by category or list for specific category
    """
    if category:
        perms = get_perms_by_cat(category)
        return [
            {
                "code": p["code"],
                "name": p["name"],
                "description": p["description"],
                "department_restricted": p["department_restricted"],
            }
            for p in perms
        ]

    # Return all permissions grouped by category
    result: dict[str, list[dict[str, Any]]] = {}
    for cat in PERMISSION_CATEGORIES:
        perms = get_perms_by_cat(cat)
        result[cat] = [
            {
                "code": p["code"],
                "name": p["name"],
                "description": p["description"],
                "department_restricted": p["department_restricted"],
            }
            for p in perms
        ]

    return result


@frappe.whitelist()
def get_user_permissions(user: str | None = None) -> dict[str, Any]:
    """
    Get all permissions for a user.

    Args:
            user: User email (defaults to current user)

    Returns:
            Dictionary with user's permissions and roles
    """
    if not user:
        user = frappe.session.user

    # Check permission to view other users' permissions
    if user != frappe.session.user and not frappe.has_role("System Manager"):
        frappe.throw(
            _("You do not have permission to view other users' permissions"),
            frappe.PermissionError,
        )

    roles = role_service.get_user_roles(user)
    permissions = role_service.get_user_permissions(user)
    by_category = role_service.get_permissions_by_category(user)

    return {
        "user": user,
        "roles": roles,
        "permissions": permissions,
        "permissions_by_category": by_category,
        "total_permissions": len(permissions),
    }


@frappe.whitelist()
def check_permission(permission_code: str, user: str | None = None) -> dict[str, Any]:
    """
    Check if user has a specific permission.

    Args:
            permission_code: Permission code to check
            user: User email (defaults to current user)

    Returns:
            Dictionary with permission check result
    """
    if not user:
        user = frappe.session.user

    has_perm = role_service.has_permission(user, permission_code)
    perm_def = get_permission(permission_code)

    result = {
        "user": user,
        "permission_code": permission_code,
        "has_permission": has_perm,
    }

    if perm_def:
        result.update(
            {
                "permission_name": perm_def["name"],
                "permission_category": perm_def["category"],
                "department_restricted": perm_def["department_restricted"],
            }
        )

    # If user has permission, show which roles grant it
    if has_perm:
        user_perms = role_service.get_user_permissions(user)
        if permission_code in user_perms:
            result["granted_by_roles"] = [
                p["role"] for p in user_perms[permission_code]
            ]

    return result


@frappe.whitelist()
def get_role_permissions(role: str) -> dict[str, Any]:
    """
    Get all permissions for a role.

    Args:
            role: Role name

    Returns:
            Dictionary with role permissions
    """
    if not frappe.db.exists("Role", role):
        frappe.throw(_("Role {0} does not exist").format(role))

    permissions = role_service.get_role_permissions(role)
    summary = role_service.get_role_summary(role)

    return {"role": role, "permissions": permissions, "summary": summary}


@frappe.whitelist()
def create_custom_role(
    role_name: str, permissions: list[str] | None = None, description: str | None = None
) -> dict[str, Any]:
    """
    Create a new custom role.

    Args:
            role_name: Name of the role
            permissions: List of permission codes
            description: Role description

    Returns:
            Created role information
    """
    # Check permission to create roles
    if not frappe.has_role("System Manager"):
        frappe.throw(
            _("You do not have permission to create roles"), frappe.PermissionError
        )

    role = role_service.create_role(role_name, permissions, description)

    return {
        "role": role.name,
        "message": _("Role {0} created successfully").format(role_name),
        "permissions_count": len(role.custom_permissions or []),
    }


@frappe.whitelist()
def update_role_permissions(
    role: str, permissions: list[str], replace: bool = False
) -> dict[str, Any]:
    """
    Update permissions for a role.

    Args:
            role: Role name
            permissions: List of permission codes
            replace: If True, replace all permissions

    Returns:
            Updated role information
    """
    # Check permission to modify roles
    if not frappe.has_role("System Manager"):
        frappe.throw(
            _("You do not have permission to modify roles"), frappe.PermissionError
        )

    role_doc = role_service.update_role_permissions(role, permissions, replace)

    return {
        "role": role,
        "message": _("Role permissions updated successfully"),
        "permissions_count": len(role_doc.custom_permissions or []),
    }


@frappe.whitelist()
def revoke_permission(role: str, permission_code: str) -> dict[str, Any]:
    """
    Revoke a permission from a role.

    Args:
            role: Role name
            permission_code: Permission code to revoke

    Returns:
            Result message
    """
    # Check permission to modify roles
    if not frappe.has_role("System Manager"):
        frappe.throw(
            _("You do not have permission to modify roles"), frappe.PermissionError
        )

    role_doc = role_service.revoke_role_permission(role, permission_code)

    return {
        "role": role,
        "permission_code": permission_code,
        "message": _("Permission revoked successfully"),
        "permissions_count": len(role_doc.custom_permissions or []),
    }


@frappe.whitelist()
def get_role_summary(role: str) -> dict[str, Any]:
    """
    Get summary information about a role.

    Args:
            role: Role name

    Returns:
            Role summary
    """
    return role_service.get_role_summary(role)


@frappe.whitelist()
def get_permission_categories() -> list[str]:
    """Get list of all permission categories."""
    return PERMISSION_CATEGORIES


@frappe.whitelist()
def search_permissions(query: str) -> list[dict[str, Any]]:
    """
    Search permissions by name or description.

    Args:
            query: Search query

    Returns:
            List of matching permissions
    """
    query_lower = query.lower()

    results = []
    for perm in ALL_PERMISSIONS:
        if (
            query_lower in perm["name"].lower()
            or query_lower in perm["description"].lower()
            or query_lower in perm["code"].lower()
        ):
            results.append(
                {
                    "code": perm["code"],
                    "name": perm["name"],
                    "description": perm["description"],
                    "category": perm["category"],
                    "department_restricted": perm["department_restricted"],
                }
            )

    return results


@frappe.whitelist()
def bulk_assign_permissions(role: str, permission_codes: list[str]) -> dict[str, Any]:
    """
    Bulk assign multiple permissions to a role.

    Args:
            role: Role name
            permission_codes: List of permission codes to assign

    Returns:
            Result with success/failure counts
    """
    # Check permission to modify roles
    if not frappe.has_role("System Manager"):
        frappe.throw(
            _("You do not have permission to modify roles"), frappe.PermissionError
        )

    role_doc = frappe.get_doc("Role", role)
    existing_codes = {p.permission_code for p in role_doc.custom_permissions}

    added = 0
    skipped = 0
    invalid = []

    for code in permission_codes:
        if code in existing_codes:
            skipped += 1
            continue

        if not get_permission(code):
            invalid.append(code)
            continue

        role_doc.append(
            "custom_permissions", {"permission_code": code, "is_granted": 1}
        )
        added += 1

    if added > 0:
        role_doc.save(ignore_permissions=True)

    return {
        "role": role,
        "added": added,
        "skipped": skipped,
        "invalid": invalid,
        "message": _("Added {0} permission(s), skipped {1}, invalid {2}").format(
            added, skipped, len(invalid)
        ),
    }


@frappe.whitelist()
def clone_role(
    source_role: str, new_role_name: str, description: str | None = None
) -> dict[str, Any]:
    """
    Clone an existing role with all its permissions.

    Args:
            source_role: Role to clone from
            new_role_name: Name for the new role
            description: Optional description

    Returns:
            Created role information
    """
    # Check permission to create roles
    if not frappe.has_role("System Manager"):
        frappe.throw(
            _("You do not have permission to create roles"), frappe.PermissionError
        )

    if not frappe.db.exists("Role", source_role):
        frappe.throw(_("Source role {0} does not exist").format(source_role))

    # Get permissions from source role
    source_perms = role_service.get_role_permissions(source_role)
    permission_codes = [p["permission_code"] for p in source_perms]

    # Create new role
    role = role_service.create_role(new_role_name, permission_codes, description)

    return {
        "role": role.name,
        "source_role": source_role,
        "message": _("Role {0} cloned from {1}").format(new_role_name, source_role),
        "permissions_count": len(role.custom_permissions or []),
    }
