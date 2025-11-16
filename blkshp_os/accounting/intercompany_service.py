"""Service layer for intercompany accounting operations."""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _
from frappe.utils import flt


def get_intercompany_balance(
    source_company: str,
    target_company: str,
    as_of_date: str | None = None,
) -> dict[str, Any]:
    """Get intercompany balance between two companies.

    Args:
        source_company: The company owing/receiving the balance
        target_company: The counterparty company
        as_of_date: Optional date to calculate balance as of (ISO format)

    Returns:
        Dictionary containing:
        - source_company: Source company code
        - target_company: Target company code
        - balance: Net balance (positive = source owes target)
        - as_of_date: Date the balance was calculated
        - currency: Balance currency

    The balance is calculated from GL Entries with the "Due To" and "Due From"
    intercompany accounts. This requires the intercompany account structure to
    be set up.
    """
    # Validate companies exist and are in same group
    _validate_companies_in_same_group(source_company, target_company)

    # TODO: Implement actual GL Entry query once intercompany accounts exist
    # For now, return a placeholder structure
    balance = {
        "source_company": source_company,
        "target_company": target_company,
        "balance": 0.0,
        "as_of_date": as_of_date or frappe.utils.nowdate(),
        "currency": "USD",  # TODO: Get from company default currency
        "note": "Intercompany account structure not yet configured"
    }

    return balance


def get_all_intercompany_balances(
    company: str | None = None,
    company_group: str | None = None,
) -> list[dict[str, Any]]:
    """Get all intercompany balances for a company or group.

    Args:
        company: Optional company to filter balances for
        company_group: Optional group to get balances within

    Returns:
        List of balance dictionaries
    """
    balances = []

    if company:
        # Get all companies in the same group as the specified company
        group = frappe.db.get_value("Company", company, "company_group")
        if not group:
            return balances

        companies = _get_companies_in_group(group)
        companies.remove(company)

        # Get balance with each other company
        for other_company in companies:
            balance = get_intercompany_balance(company, other_company)
            if flt(balance["balance"]) != 0:
                balances.append(balance)

    elif company_group:
        # Get all pairwise balances within the group
        companies = _get_companies_in_group(company_group)

        for i, source in enumerate(companies):
            for target in companies[i + 1:]:
                balance = get_intercompany_balance(source, target)
                if flt(balance["balance"]) != 0:
                    balances.append(balance)

    return balances


def get_pending_settlements(
    company: str | None = None,
    status: str | None = None,
) -> list[dict[str, Any]]:
    """Get pending intercompany settlements.

    Args:
        company: Optional company to filter settlements for
        status: Optional status filter (Draft, Settled, Cancelled)

    Returns:
        List of settlement dictionaries
    """
    filters = {"docstatus": ["<", 2]}  # Not cancelled

    if company:
        # Include settlements where company is source or target
        filters = {
            "docstatus": ["<", 2],
        }
        # Use OR condition for source/target
        settlements = frappe.db.get_all(
            "Intercompany Settlement",
            filters=filters,
            fields=["name", "source_company", "target_company", "settlement_amount",
                    "settlement_currency", "settlement_date", "status", "submitted_by"],
            or_filters={
                "source_company": company,
                "target_company": company,
            },
            order_by="modified desc",
        )
    else:
        if status:
            filters["status"] = status

        settlements = frappe.db.get_all(
            "Intercompany Settlement",
            filters=filters,
            fields=["name", "source_company", "target_company", "settlement_amount",
                    "settlement_currency", "settlement_date", "status", "submitted_by"],
            order_by="modified desc",
        )

    return settlements


def _validate_companies_in_same_group(company1: str, company2: str) -> None:
    """Validate that two companies are in the same company group.

    Raises:
        ValidationError: If companies are not in the same group
    """
    if company1 == company2:
        frappe.throw(_("Cannot calculate intercompany balance for the same company"))

    group1 = frappe.db.get_value("Company", company1, "company_group")
    group2 = frappe.db.get_value("Company", company2, "company_group")

    if not group1 or not group2:
        frappe.throw(_("Both companies must belong to a Company Group"))

    if group1 != group2:
        frappe.throw(
            _(f"Companies must be in the same group. "
              f"{company1} is in {group1}, {company2} is in {group2}")
        )


def _get_companies_in_group(group_code: str) -> list[str]:
    """Get all companies in a company group.

    Args:
        group_code: Company Group code

    Returns:
        List of company codes
    """
    companies = frappe.db.get_all(
        "Company Group Member",
        filters={"parent": group_code},
        fields=["company"],
        pluck="company",
    )
    return companies
