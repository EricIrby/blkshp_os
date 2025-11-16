"""Intercompany Settlement DocType for managing intercompany balance settlements."""

from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt, get_datetime, nowdate


class IntercompanySettlement(Document):
    """Intercompany Settlement for reconciling and settling balances between companies.

    Settlements require dual approval - permissions in both the source and target
    companies. This ensures proper segregation of duties for intercompany fund transfers.
    """

    def validate(self):
        """Validate settlement configuration."""
        self.validate_companies_in_same_group()
        self.validate_settlement_amount()
        self.validate_dual_permissions()

    def validate_companies_in_same_group(self):
        """Ensure source and target companies are in the same company group."""
        if self.source_company == self.target_company:
            frappe.throw(_("Source and target companies cannot be the same"))

        # Get company groups for both companies
        source_group = frappe.db.get_value("Company", self.source_company, "company_group")
        target_group = frappe.db.get_value("Company", self.target_company, "company_group")

        if not source_group or not target_group:
            frappe.throw(_("Both companies must belong to a Company Group for intercompany settlements"))

        if source_group != target_group:
            frappe.throw(
                _("Source and target companies must be in the same Company Group. "
                  f"{self.source_company} is in {source_group}, "
                  f"{self.target_company} is in {target_group}")
            )

    def validate_settlement_amount(self):
        """Validate settlement amount is positive."""
        if flt(self.settlement_amount) <= 0:
            frappe.throw(_("Settlement amount must be greater than zero"))

    def validate_dual_permissions(self):
        """Validate user has permissions in both companies (dual approval)."""
        if self.docstatus == 1:  # On submit
            user = frappe.session.user

            # System roles bypass permission checks
            if self._user_has_system_role(user):
                return

            # Check source company permission
            if not self._user_has_company_permission(user, self.source_company):
                frappe.throw(
                    _(f"User {user} does not have permission for source company {self.source_company}")
                )

            # Check target company permission
            if not self._user_has_company_permission(user, self.target_company):
                frappe.throw(
                    _(f"User {user} does not have permission for target company {self.target_company}")
                )

    def _user_has_system_role(self, user: str) -> bool:
        """Check if user has system roles that bypass restrictions."""
        system_roles = ["System Manager", "Administrator", "Accounts Manager"]
        user_roles = frappe.get_roles(user)
        return any(role in user_roles for role in system_roles)

    def _user_has_company_permission(self, user: str, company: str) -> bool:
        """Check if user has permission for the given company."""
        # Check user permissions for company
        has_permission = frappe.db.exists({
            "doctype": "User Permission",
            "user": user,
            "allow": "Company",
            "for_value": company,
        })
        return bool(has_permission)

    def before_submit(self):
        """Set submission details."""
        self.settlement_date = nowdate()
        self.submitted_by = frappe.session.user
        self.submitted_at = get_datetime()

    def on_submit(self):
        """Create Journal Entries for the settlement."""
        self.create_settlement_journal_entries()

    def create_settlement_journal_entries(self):
        """Create paired Journal Entries for the intercompany settlement.

        Creates two JEs:
        1. Source company: Credit "Due To [Target]"
        2. Target company: Debit "Due From [Source]"
        """
        # TODO: This requires intercompany accounts to be set up
        # For now, we'll store the reference but not create JEs
        # This will be implemented when the intercompany account structure is in place

        self.db_set("status", "Settled")
        frappe.msgprint(_("Settlement recorded. Journal entries will be created once intercompany accounts are configured."))

    def on_cancel(self):
        """Handle settlement cancellation."""
        # Settlements should be reversed, not cancelled, per decision log
        frappe.throw(_("Settlements cannot be cancelled. Please create a reversal settlement instead."))
