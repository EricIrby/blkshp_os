"""REST API endpoints for Inventory domain."""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.utils import flt, get_datetime

from blkshp_os.inventory.doctype.stock_ledger_entry.stock_ledger_entry import (
    get_batch_movements,
    get_stock_balance,
    get_stock_balance_by_batch,
    get_stock_movements,
    get_stock_value,
)
from blkshp_os.permissions import service as permission_service


@frappe.whitelist()
def list_inventory_balances(
    product: str | None = None,
    department: str | None = None,
    company: str | None = None,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List inventory balances with optional filters.

    Args:
        product: Filter by product code
        department: Filter by department
        company: Filter by company
        limit: Maximum number of results
        offset: Pagination offset

    Returns:
        Dictionary with balances list and metadata
    """
    filters = {}
    if product:
        filters["product"] = product
    if department:
        filters["department"] = department
    if company:
        filters["company"] = company

    # Apply department permissions if not system role
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        accessible_departments = permission_service.get_accessible_departments(user)
        if not accessible_departments:
            return {"balances": [], "total": 0, "limit": limit, "offset": offset}

        if department and department not in accessible_departments:
            frappe.throw(
                _("You do not have permission to access this department."),
                frappe.PermissionError,
            )

        if not department:
            filters["department"] = ("in", accessible_departments)

    total = frappe.db.count("Inventory Balance", filters)
    balances = frappe.get_all(
        "Inventory Balance",
        filters=filters,
        fields=[
            "name",
            "product",
            "department",
            "company",
            "quantity",
            "last_updated",
            "last_audit_date",
        ],
        limit=limit,
        start=offset,
        order_by="product asc, department asc",
    )

    return {
        "balances": balances,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@frappe.whitelist()
def get_inventory_balance(
    product: str,
    department: str,
    company: str,
) -> dict[str, Any]:
    """Get specific inventory balance for product/department/company.

    Args:
        product: Product code
        department: Department name
        company: Company name

    Returns:
        Inventory balance details
    """
    if not all([product, department, company]):
        frappe.throw(_("Product, department, and company are required."))

    # Check department permission
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        if not permission_service.has_department_permission(user, department):
            frappe.throw(
                _("You do not have permission to access this department."),
                frappe.PermissionError,
            )

    balance_name = f"{product}-{department}-{company}"
    if not frappe.db.exists("Inventory Balance", balance_name):
        frappe.throw(_(f"Inventory balance not found: {balance_name}"))

    balance = frappe.get_doc("Inventory Balance", balance_name)

    return {
        "product": balance.product,
        "department": balance.department,
        "company": balance.company,
        "quantity": balance.quantity,
        "last_updated": balance.last_updated,
        "last_audit_date": balance.last_audit_date,
    }


@frappe.whitelist()
def query_stock_balance(
    product: str,
    department: str,
    company: str,
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Query current stock balance from Stock Ledger Entries.

    Args:
        product: Product code
        department: Department name
        company: Company name
        as_of_date: Optional date to query balance as of (ISO format)

    Returns:
        Stock balance information
    """
    if not all([product, department, company]):
        frappe.throw(_("Product, department, and company are required."))

    # Check department permission
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        if not permission_service.has_department_permission(user, department):
            frappe.throw(
                _("You do not have permission to access this department."),
                frappe.PermissionError,
            )

    date_param = get_datetime(as_of_date) if as_of_date else None
    balance = get_stock_balance(product, department, company, as_of_date=date_param)

    return {
        "product": product,
        "department": department,
        "company": company,
        "balance": balance,
        "as_of_date": as_of_date,
    }


@frappe.whitelist()
def query_stock_value(
    product: str,
    department: str,
    company: str,
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Query current stock value from Stock Ledger Entries.

    Args:
        product: Product code
        department: Department name
        company: Company name
        as_of_date: Optional date to query value as of (ISO format)

    Returns:
        Stock value information
    """
    if not all([product, department, company]):
        frappe.throw(_("Product, department, and company are required."))

    # Check department permission
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        if not permission_service.has_department_permission(user, department):
            frappe.throw(
                _("You do not have permission to access this department."),
                frappe.PermissionError,
            )

    date_param = get_datetime(as_of_date) if as_of_date else None
    value = get_stock_value(product, department, company, as_of_date=date_param)

    return {
        "product": product,
        "department": department,
        "company": company,
        "value": value,
        "as_of_date": as_of_date,
    }


@frappe.whitelist()
def query_stock_movements(
    product: str,
    department: str,
    company: str,
    from_date: str,
    to_date: str,
) -> dict[str, Any]:
    """Query stock movements for a product/department within a date range.

    Args:
        product: Product code
        department: Department name
        company: Company name
        from_date: Start date (ISO format)
        to_date: End date (ISO format)

    Returns:
        List of stock movements
    """
    if not all([product, department, company, from_date, to_date]):
        frappe.throw(_("Product, department, company, from_date, and to_date are required."))

    # Check department permission
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        if not permission_service.has_department_permission(user, department):
            frappe.throw(
                _("You do not have permission to access this department."),
                frappe.PermissionError,
            )

    from_date_param = get_datetime(from_date)
    to_date_param = get_datetime(to_date)

    movements = get_stock_movements(
        product, department, company, from_date_param, to_date_param
    )

    return {
        "product": product,
        "department": department,
        "company": company,
        "from_date": from_date,
        "to_date": to_date,
        "movements": movements,
    }


@frappe.whitelist()
def query_batch_balance(
    product: str,
    department: str,
    company: str,
    batch_number: str | None = None,
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Query stock balance by batch number.

    Args:
        product: Product code
        department: Department name
        company: Company name
        batch_number: Optional specific batch number (if None, returns all batches)
        as_of_date: Optional date to query balance as of (ISO format)

    Returns:
        Batch balance information
    """
    if not all([product, department, company]):
        frappe.throw(_("Product, department, and company are required."))

    # Check department permission
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        if not permission_service.has_department_permission(user, department):
            frappe.throw(
                _("You do not have permission to access this department."),
                frappe.PermissionError,
            )

    date_param = get_datetime(as_of_date) if as_of_date else None
    balance = get_stock_balance_by_batch(
        product, department, company, batch_number=batch_number, as_of_date=date_param
    )

    return {
        "product": product,
        "department": department,
        "company": company,
        "batch_number": batch_number,
        "as_of_date": as_of_date,
        "balance": balance,
    }


@frappe.whitelist()
def query_batch_movements(
    batch_number: str,
    from_date: str | None = None,
    to_date: str | None = None,
) -> dict[str, Any]:
    """Query movements for a specific batch number.

    Args:
        batch_number: Batch number
        from_date: Optional start date (ISO format)
        to_date: Optional end date (ISO format)

    Returns:
        List of batch movements
    """
    if not batch_number:
        frappe.throw(_("Batch number is required."))

    # Get batch to check department permission
    batch_doc = frappe.get_doc("Batch Number", batch_number)

    # Check department permission
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        if not permission_service.has_department_permission(user, batch_doc.department):
            frappe.throw(
                _("You do not have permission to access this batch's department."),
                frappe.PermissionError,
            )

    from_date_param = get_datetime(from_date) if from_date else None
    to_date_param = get_datetime(to_date) if to_date else None

    movements = get_batch_movements(
        batch_number, from_date=from_date_param, to_date=to_date_param
    )

    return {
        "batch_number": batch_number,
        "product": batch_doc.product,
        "department": batch_doc.department,
        "from_date": from_date,
        "to_date": to_date,
        "movements": movements,
    }


@frappe.whitelist()
def list_batches(
    product: str | None = None,
    department: str | None = None,
    company: str | None = None,
    active_only: bool = True,
    limit: int = 100,
    offset: int = 0,
) -> dict[str, Any]:
    """List batch numbers with optional filters.

    Args:
        product: Filter by product code
        department: Filter by department
        company: Filter by company
        active_only: Only return non-expired batches
        limit: Maximum number of results
        offset: Pagination offset

    Returns:
        Dictionary with batches list and metadata
    """
    filters = {}
    if product:
        filters["product"] = product
    if department:
        filters["department"] = department
    if company:
        filters["company"] = company

    # Apply department permissions if not system role
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        accessible_departments = permission_service.get_accessible_departments(user)
        if not accessible_departments:
            return {"batches": [], "total": 0, "limit": limit, "offset": offset}

        if department and department not in accessible_departments:
            frappe.throw(
                _("You do not have permission to access this department."),
                frappe.PermissionError,
            )

        if not department:
            filters["department"] = ("in", accessible_departments)

    # Filter for active batches
    if active_only:
        from frappe.utils import today

        filters["expiration_date"] = (">=", today())

    total = frappe.db.count("Batch Number", filters)
    batches = frappe.get_all(
        "Batch Number",
        filters=filters,
        fields=[
            "name",
            "product",
            "department",
            "company",
            "manufacturing_date",
            "expiration_date",
            "quantity",
        ],
        limit=limit,
        start=offset,
        order_by="expiration_date asc, product asc",
    )

    return {
        "batches": batches,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@frappe.whitelist()
def get_batch(batch_number: str) -> dict[str, Any]:
    """Get specific batch number details.

    Args:
        batch_number: Batch number

    Returns:
        Batch details
    """
    if not batch_number:
        frappe.throw(_("Batch number is required."))

    batch = frappe.get_doc("Batch Number", batch_number)

    # Check department permission
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        if not permission_service.has_department_permission(user, batch.department):
            frappe.throw(
                _("You do not have permission to access this batch's department."),
                frappe.PermissionError,
            )

    return {
        "name": batch.name,
        "product": batch.product,
        "department": batch.department,
        "company": batch.company,
        "manufacturing_date": batch.manufacturing_date,
        "expiration_date": batch.expiration_date,
        "quantity": batch.quantity,
    }


@frappe.whitelist()
def list_audits(
    status: str | None = None,
    department: str | None = None,
    company: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    """List inventory audits with optional filters.

    Args:
        status: Filter by audit status (Setup, Ready, In Progress, Review, Closed, Locked)
        department: Filter by department
        company: Filter by company
        limit: Maximum number of results
        offset: Pagination offset

    Returns:
        Dictionary with audits list and metadata
    """
    filters = {}
    if status:
        filters["status"] = status
    if company:
        filters["company"] = company

    # Apply department permissions if not system role
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        accessible_departments = permission_service.get_accessible_departments(user)
        if not accessible_departments:
            return {"audits": [], "total": 0, "limit": limit, "offset": offset}

        # For audits, we need to check the child table for departments
        # This is more complex, so we'll fetch all and filter
        audits_list = frappe.get_all(
            "Inventory Audit",
            filters=filters,
            fields=[
                "name",
                "audit_name",
                "status",
                "company",
                "audit_date",
                "closed_by",
                "closed_at",
            ],
            limit=limit * 2,  # Get more to allow for filtering
            start=offset,
            order_by="audit_date desc",
        )

        # Filter by accessible departments
        filtered_audits = []
        for audit in audits_list:
            audit_deps = frappe.get_all(
                "Inventory Audit Department",
                filters={"parent": audit.name},
                fields=["department"],
                pluck="department",
            )
            if any(dept in accessible_departments for dept in audit_deps):
                filtered_audits.append(audit)
                if len(filtered_audits) >= limit:
                    break

        return {
            "audits": filtered_audits,
            "total": len(filtered_audits),
            "limit": limit,
            "offset": offset,
        }

    total = frappe.db.count("Inventory Audit", filters)
    audits = frappe.get_all(
        "Inventory Audit",
        filters=filters,
        fields=[
            "name",
            "audit_name",
            "status",
            "company",
            "audit_date",
            "closed_by",
            "closed_at",
        ],
        limit=limit,
        start=offset,
        order_by="audit_date desc",
    )

    return {
        "audits": audits,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@frappe.whitelist()
def get_audit(audit_name: str) -> dict[str, Any]:
    """Get specific inventory audit details.

    Args:
        audit_name: Audit document name

    Returns:
        Audit details including departments, categories, and lines
    """
    if not audit_name:
        frappe.throw(_("Audit name is required."))

    audit = frappe.get_doc("Inventory Audit", audit_name)

    # Check if user has access to at least one department in this audit
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        accessible_departments = permission_service.get_accessible_departments(user)
        audit_departments = [dept.department for dept in audit.audit_departments]

        if not any(dept in accessible_departments for dept in audit_departments):
            frappe.throw(
                _("You do not have permission to access this audit."),
                frappe.PermissionError,
            )

    return {
        "name": audit.name,
        "audit_name": audit.audit_name,
        "status": audit.status,
        "company": audit.company,
        "audit_date": audit.audit_date,
        "closed_by": audit.closed_by,
        "closed_at": audit.closed_at,
        "departments": [
            {"department": dept.department} for dept in audit.audit_departments
        ],
        "categories": [
            {"category": cat.category} for cat in audit.audit_categories
        ],
        "storage_locations": [
            {"storage_area": loc.storage_area}
            for loc in audit.audit_storage_locations
        ],
        "counting_tasks_count": len(audit.counting_tasks or []),
        "audit_lines_count": len(audit.audit_lines or []),
    }


@frappe.whitelist()
def create_audit(data: dict[str, Any] | str) -> dict[str, Any]:
    """Create a new inventory audit.

    Args:
        data: Audit data including audit_name, company, audit_date, departments, etc.

    Returns:
        Created audit details
    """
    if isinstance(data, str):
        data = frappe.parse_json(data)

    if not isinstance(data, dict):
        frappe.throw(_("Invalid payload for audit creation."))

    # Verify user has permission for specified departments
    user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(user):
        accessible_departments = permission_service.get_accessible_departments(user)
        requested_departments = [dept.get("department") for dept in data.get("departments", [])]

        if not all(dept in accessible_departments for dept in requested_departments):
            frappe.throw(
                _("You do not have permission to create audits for some of the specified departments."),
                frappe.PermissionError,
            )

    audit = frappe.get_doc(
        {
            "doctype": "Inventory Audit",
            **data,
        }
    )
    audit.insert()

    return {
        "name": audit.name,
        "audit_name": audit.audit_name,
        "status": audit.status,
    }


@frappe.whitelist()
def update_audit_status(
    audit_name: str,
    action: str,
    user: str | None = None,
) -> dict[str, Any]:
    """Update inventory audit status.

    Args:
        audit_name: Audit document name
        action: Action to perform (create_tasks, mark_in_progress, mark_review, close)
        user: User performing the action (for close_audit)

    Returns:
        Updated audit status
    """
    if not audit_name:
        frappe.throw(_("Audit name is required."))

    if action not in ["create_tasks", "mark_in_progress", "mark_review", "close"]:
        frappe.throw(_("Invalid action. Must be one of: create_tasks, mark_in_progress, mark_review, close"))

    audit = frappe.get_doc("Inventory Audit", audit_name)

    # Check if user has access to at least one department in this audit
    current_user = frappe.session.user
    if not permission_service._user_bypasses_subscription_gates(current_user):
        accessible_departments = permission_service.get_accessible_departments(current_user)
        audit_departments = [dept.department for dept in audit.audit_departments]

        if not any(dept in accessible_departments for dept in audit_departments):
            frappe.throw(
                _("You do not have permission to modify this audit."),
                frappe.PermissionError,
            )

    # Perform the requested action
    if action == "create_tasks":
        audit.create_counting_tasks()
    elif action == "mark_in_progress":
        audit.mark_in_progress()
    elif action == "mark_review":
        audit.mark_review()
    elif action == "close":
        audit.close_audit(user=user or current_user)

    audit.save()

    return {
        "name": audit.name,
        "status": audit.status,
        "action_performed": action,
    }
