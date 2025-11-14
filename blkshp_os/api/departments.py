"""REST API endpoints for Department operations."""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _


@frappe.whitelist()
def get_department_details(department: str) -> dict[str, Any]:
    """
    Get comprehensive department details including products and users.

    Args:
            department: Department name/ID

    Returns:
            Dictionary with department details, products, and users
    """
    if not department:
        frappe.throw(_("Department is required"))

    # Check if user has read permission for this department
    from blkshp_os.permissions.service import has_department_permission

    if not has_department_permission(frappe.session.user, department, "can_read"):
        frappe.throw(
            _("You do not have permission to view this department"),
            frappe.PermissionError,
        )

    # Get department document
    dept_doc = frappe.get_doc("Department", department)

    # Get products assigned to this department
    products = frappe.call(
        "blkshp_os.departments.doctype.department.department.get_products",
        department=department,
    )

    # Get users with access to this department
    users = frappe.call(
        "blkshp_os.departments.doctype.department.department.get_users",
        department=department,
    )

    return {
        "department": dept_doc.as_dict(),
        "products": products,
        "users": users,
        "product_count": len(products) if products else 0,
        "user_count": len(users) if users else 0,
    }


@frappe.whitelist()
def get_accessible_departments(
    permission_flag: str = "can_read",
) -> list[dict[str, Any]]:
    """
    Get list of departments accessible to the current user.

    Args:
            permission_flag: Permission level to check (default: can_read)

    Returns:
            List of department dictionaries with basic info
    """
    from blkshp_os.permissions.service import get_accessible_departments as get_depts

    department_names = get_depts(frappe.session.user, permission_flag=permission_flag)

    if not department_names:
        return []

    departments = frappe.get_all(
        "Department",
        filters={"name": ["in", department_names]},
        fields=[
            "name",
            "department_name",
            "department_code",
            "department_type",
            "company",
            "is_active",
            "parent_department",
        ],
        order_by="department_name asc",
    )

    return departments


@frappe.whitelist()
def get_department_hierarchy(department: str | None = None) -> list[dict[str, Any]]:
    """
    Get department hierarchy tree structure.

    Args:
            department: Root department (if None, returns all top-level departments)

    Returns:
            List of departments with nested children
    """
    from blkshp_os.permissions.service import get_accessible_departments as get_depts

    # Get accessible departments for the user
    accessible = set(get_depts(frappe.session.user, permission_flag="can_read"))

    if not accessible:
        return []

    # Build filter for root departments
    filters: dict[str, Any] = {"name": ["in", list(accessible)], "is_active": 1}

    if department:
        # Get children of specific department
        filters["parent_department"] = department
    else:
        # Get top-level departments (no parent)
        filters["parent_department"] = ["in", [None, ""]]

    departments = frappe.get_all(
        "Department",
        filters=filters,
        fields=[
            "name",
            "department_name",
            "department_code",
            "department_type",
            "parent_department",
            "is_active",
        ],
        order_by="department_name asc",
    )

    # Recursively get children for each department
    for dept in departments:
        children = get_department_hierarchy(dept["name"])
        if children:
            dept["children"] = children
            dept["has_children"] = True
        else:
            dept["has_children"] = False

    return departments


@frappe.whitelist()
def assign_products_to_department(
    department: str,
    products: list[str],
    is_primary: bool = False,
    par_level: float | None = None,
    order_quantity: float | None = None,
) -> dict[str, Any]:
    """
    Bulk assign products to a department.

    Args:
            department: Department name/ID
            products: List of product names/IDs
            is_primary: Mark as primary department for these products
            par_level: Default par level for all products
            order_quantity: Default order quantity for all products

    Returns:
            Dictionary with success status and results
    """
    from blkshp_os.permissions.service import has_department_permission

    if not has_department_permission(frappe.session.user, department, "can_write"):
        frappe.throw(
            _("You do not have permission to modify this department"),
            frappe.PermissionError,
        )

    if not products:
        frappe.throw(_("No products specified"))

    results = {"success": [], "failed": [], "total": len(products)}

    for product in products:
        try:
            product_doc = frappe.get_doc("Product", product)

            # Check if department already assigned
            existing = False
            for row in product_doc.get("departments", []):
                if row.department == department:
                    existing = True
                    break

            if not existing:
                product_doc.append(
                    "departments",
                    {
                        "department": department,
                        "is_primary": is_primary,
                        "par_level": par_level,
                        "order_quantity": order_quantity,
                    },
                )
                product_doc.save(ignore_permissions=True)
                results["success"].append(product)
            else:
                results["failed"].append(
                    {"product": product, "reason": "Already assigned to department"}
                )
        except Exception as e:
            results["failed"].append({"product": product, "reason": str(e)})

    return results


@frappe.whitelist()
def get_department_settings(department: str, setting_key: str | None = None) -> Any:
    """
    Get department settings.

    Args:
            department: Department name/ID
            setting_key: Specific setting key (if None, returns all settings)

    Returns:
            Setting value or all settings dictionary
    """
    from blkshp_os.departments.doctype.department.department import (
        get_department_setting,
    )
    from blkshp_os.permissions.service import has_department_permission

    if not has_department_permission(frappe.session.user, department, "can_read"):
        frappe.throw(
            _("You do not have permission to view this department"),
            frappe.PermissionError,
        )

    if setting_key:
        return get_department_setting(department, setting_key)
    else:
        # Return all settings
        settings = frappe.db.get_value("Department", department, "settings")
        if settings:
            import json

            return json.loads(settings) if isinstance(settings, str) else settings
        return {}


@frappe.whitelist()
def update_department_settings(
    department: str, settings: dict[str, Any]
) -> dict[str, Any]:
    """
    Update department settings.

    Args:
            department: Department name/ID
            settings: Dictionary of settings to update

    Returns:
            Updated settings dictionary
    """
    from blkshp_os.permissions.service import has_department_permission

    if not has_department_permission(frappe.session.user, department, "can_write"):
        frappe.throw(
            _("You do not have permission to modify this department"),
            frappe.PermissionError,
        )

    dept_doc = frappe.get_doc("Department", department)

    # Get existing settings
    import json

    existing_settings = {}
    if dept_doc.settings:
        existing_settings = (
            json.loads(dept_doc.settings)
            if isinstance(dept_doc.settings, str)
            else dept_doc.settings
        )

    # Update with new settings
    existing_settings.update(settings)

    # Save
    dept_doc.settings = json.dumps(existing_settings)
    dept_doc.save(ignore_permissions=True)

    return existing_settings


@frappe.whitelist()
def get_department_statistics(department: str) -> dict[str, Any]:
    """
    Get statistics for a department.

    Args:
            department: Department name/ID

    Returns:
            Dictionary with various statistics
    """
    from blkshp_os.permissions.service import has_department_permission

    if not has_department_permission(frappe.session.user, department, "can_read"):
        frappe.throw(
            _("You do not have permission to view this department"),
            frappe.PermissionError,
        )

    # Get product count
    product_count = frappe.db.count(
        "Product Department",
        filters={"department": department, "parenttype": "Product"},
    )

    # Get user count
    user_count = frappe.db.count(
        "Department Permission",
        filters={"department": department, "parenttype": "User", "can_read": 1},
    )

    # Get inventory value (if inventory module exists)
    inventory_value = 0
    try:
        inventory_balance = frappe.db.sql(
            """
			SELECT SUM(quantity * unit_cost) as total_value
			FROM `tabInventory Balance`
			WHERE department = %s
		""",
            department,
            as_dict=True,
        )
        if inventory_balance and inventory_balance[0].get("total_value"):
            inventory_value = inventory_balance[0]["total_value"]
    except Exception:
        # Inventory Balance table might not exist yet
        pass

    # Get child department count
    child_count = frappe.db.count(
        "Department", filters={"parent_department": department}
    )

    return {
        "department": department,
        "product_count": product_count,
        "user_count": user_count,
        "inventory_value": inventory_value,
        "child_department_count": child_count,
    }
