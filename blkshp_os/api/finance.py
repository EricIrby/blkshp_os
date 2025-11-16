"""REST API endpoints for finance and intercompany operations."""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _

from blkshp_os.accounting import intercompany_service
from blkshp_os.permissions import service as permission_service


@frappe.whitelist()
def get_intercompany_balance(
    source_company: str,
    target_company: str,
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Get intercompany balance between two companies.

    Args:
        source_company: The company code
        target_company: The counterparty company code
        as_of_date: Optional date to calculate balance as of (ISO format: YYYY-MM-DD)

    Returns:
        {
            "source_company": str,
            "target_company": str,
            "balance": float,
            "as_of_date": str,
            "currency": str
        }

    Permissions:
        User must have read access to at least one of the companies,
        or have a system role (BLKSHP Operations, System Manager, Administrator).
    """
    user = frappe.session.user

    # Check permissions
    if not permission_service._user_bypasses_subscription_gates(user):
        has_source_perm = _user_has_company_permission(user, source_company)
        has_target_perm = _user_has_company_permission(user, target_company)

        if not (has_source_perm or has_target_perm):
            frappe.throw(
                _("You do not have permission to view balances for these companies"),
                frappe.PermissionError
            )

    return intercompany_service.get_intercompany_balance(
        source_company, target_company, as_of_date
    )


@frappe.whitelist()
def list_intercompany_balances(
    company: str | None = None,
    company_group: str | None = None,
) -> dict[str, Any]:
    """List intercompany balances.

    Args:
        company: Optional company to filter balances for
        company_group: Optional group to get balances within

    Returns:
        {
            "balances": [
                {
                    "source_company": str,
                    "target_company": str,
                    "balance": float,
                    "currency": str
                },
                ...
            ],
            "total": int
        }

    Permissions:
        If company is specified, user must have read access to that company.
        If company_group is specified, user must have access to at least one company in the group.
        System roles bypass permission checks.
    """
    user = frappe.session.user

    # Check permissions
    if not permission_service._user_bypasses_subscription_gates(user):
        if company:
            if not _user_has_company_permission(user, company):
                frappe.throw(
                    _(f"You do not have permission to view balances for {company}"),
                    frappe.PermissionError
                )
        elif company_group:
            # User must have access to at least one company in the group
            companies = frappe.db.get_all(
                "Company Group Member",
                filters={"parent": company_group},
                pluck="company"
            )
            has_access = any(
                _user_has_company_permission(user, comp) for comp in companies
            )
            if not has_access:
                frappe.throw(
                    _(f"You do not have permission to view balances for group {company_group}"),
                    frappe.PermissionError
                )

    balances = intercompany_service.get_all_intercompany_balances(
        company=company,
        company_group=company_group,
    )

    return {
        "balances": balances,
        "total": len(balances),
    }


@frappe.whitelist()
def list_settlements(
    company: str | None = None,
    status: str | None = None,
    limit: int = 50,
    offset: int = 0,
) -> dict[str, Any]:
    """List intercompany settlements.

    Args:
        company: Optional company to filter settlements for (as source or target)
        status: Optional status filter (Draft, Settled, Cancelled)
        limit: Maximum number of results (default: 50)
        offset: Pagination offset (default: 0)

    Returns:
        {
            "settlements": [
                {
                    "name": str,
                    "source_company": str,
                    "target_company": str,
                    "settlement_amount": float,
                    "settlement_currency": str,
                    "settlement_date": str,
                    "status": str,
                    "submitted_by": str
                },
                ...
            ],
            "total": int,
            "limit": int,
            "offset": int
        }

    Permissions:
        If company is specified, user must have read access to that company.
        System roles bypass permission checks.
    """
    user = frappe.session.user
    limit = int(limit)
    offset = int(offset)

    # Check permissions
    if company and not permission_service._user_bypasses_subscription_gates(user):
        if not _user_has_company_permission(user, company):
            frappe.throw(
                _(f"You do not have permission to view settlements for {company}"),
                frappe.PermissionError
            )

    settlements = intercompany_service.get_pending_settlements(
        company=company,
        status=status,
    )

    # Apply pagination
    total = len(settlements)
    settlements = settlements[offset:offset + limit]

    return {
        "settlements": settlements,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@frappe.whitelist()
def get_settlement(settlement_name: str) -> dict[str, Any]:
    """Get specific settlement details.

    Args:
        settlement_name: Settlement document name

    Returns:
        Settlement document dict

    Permissions:
        User must have read access to source or target company.
        System roles bypass permission checks.
    """
    user = frappe.session.user

    if not frappe.db.exists("Intercompany Settlement", settlement_name):
        frappe.throw(
            _(f"Settlement {settlement_name} not found"),
            frappe.DoesNotExistError
        )

    settlement = frappe.get_doc("Intercompany Settlement", settlement_name)

    # Check permissions
    if not permission_service._user_bypasses_subscription_gates(user):
        has_source_perm = _user_has_company_permission(user, settlement.source_company)
        has_target_perm = _user_has_company_permission(user, settlement.target_company)

        if not (has_source_perm or has_target_perm):
            frappe.throw(
                _("You do not have permission to view this settlement"),
                frappe.PermissionError
            )

    return settlement.as_dict()


@frappe.whitelist()
def create_settlement(settlement_data: dict[str, Any]) -> dict[str, Any]:
    """Create a new intercompany settlement.

    Args:
        settlement_data: Settlement data including:
            - source_company (required)
            - target_company (required)
            - settlement_amount (required)
            - settlement_currency (required)
            - description (optional)
            - payment_method (optional)
            - reference_number (optional)

    Returns:
        Created settlement document dict

    Permissions:
        User must have write access to both source and target companies.
        System roles bypass permission checks.
    """
    user = frappe.session.user

    # Validate required fields
    required_fields = ["source_company", "target_company", "settlement_amount", "settlement_currency"]
    for field in required_fields:
        if not settlement_data.get(field):
            frappe.throw(_(f"{field} is required"))

    # Check permissions
    if not permission_service._user_bypasses_subscription_gates(user):
        source_company = settlement_data["source_company"]
        target_company = settlement_data["target_company"]

        if not _user_has_company_permission(user, source_company, "can_write"):
            frappe.throw(
                _(f"You do not have write permission for {source_company}"),
                frappe.PermissionError
            )

        if not _user_has_company_permission(user, target_company, "can_write"):
            frappe.throw(
                _(f"You do not have write permission for {target_company}"),
                frappe.PermissionError
            )

    # Create settlement
    settlement = frappe.get_doc({
        "doctype": "Intercompany Settlement",
        **settlement_data
    })
    settlement.insert()

    return {
        "name": settlement.name,
        "source_company": settlement.source_company,
        "target_company": settlement.target_company,
        "settlement_amount": settlement.settlement_amount,
        "status": settlement.status,
    }


@frappe.whitelist()
def submit_settlement(settlement_name: str) -> dict[str, Any]:
    """Submit an intercompany settlement.

    Args:
        settlement_name: Settlement document name

    Returns:
        Updated settlement document dict

    Permissions:
        User must have submit permission for both source and target companies (dual approval).
        System roles bypass permission checks.
    """
    user = frappe.session.user

    if not frappe.db.exists("Intercompany Settlement", settlement_name):
        frappe.throw(
            _(f"Settlement {settlement_name} not found"),
            frappe.DoesNotExistError
        )

    settlement = frappe.get_doc("Intercompany Settlement", settlement_name)

    # Check permissions (dual approval enforced in the doctype validate method)
    if not permission_service._user_bypasses_subscription_gates(user):
        source_perm = _user_has_company_permission(user, settlement.source_company, "can_submit")
        target_perm = _user_has_company_permission(user, settlement.target_company, "can_submit")

        if not (source_perm and target_perm):
            frappe.throw(
                _("You must have submit permission for both companies to approve this settlement"),
                frappe.PermissionError
            )

    settlement.submit()

    return {
        "name": settlement.name,
        "status": settlement.status,
        "settlement_date": settlement.settlement_date,
        "submitted_by": settlement.submitted_by,
    }


def _user_has_company_permission(user: str, company: str, permission_flag: str = "can_read") -> bool:
    """Check if user has permission for a company.

    This is a simplified check using User Permissions. In a full implementation,
    this would integrate with the department permission system.
    """
    # Check if user has explicit user permission for the company
    has_permission = frappe.db.exists({
        "doctype": "User Permission",
        "user": user,
        "allow": "Company",
        "for_value": company,
    })

    return bool(has_permission)
