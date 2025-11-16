"""Company Group DocType for intercompany accounting."""

from __future__ import annotations

import frappe
from frappe.model.document import Document


class CompanyGroup(Document):
    """Company Group for intercompany accounting and consolidated reporting.

    A Company Group represents a set of companies that conduct intercompany
    transactions and require consolidated reporting. All companies in a group
    share accounting rules and can transact with each other.
    """

    def validate(self):
        """Validate Company Group configuration."""
        self.validate_unique_group_code()
        self.validate_member_companies()

    def validate_unique_group_code(self):
        """Ensure group code is unique."""
        if self.is_new():
            existing = frappe.db.exists("Company Group", {"group_code": self.group_code})
            if existing and existing != self.name:
                frappe.throw(f"Company Group with code {self.group_code} already exists")

    def validate_member_companies(self):
        """Validate that member companies exist and are not in other groups."""
        if not self.member_companies:
            frappe.throw("Company Group must have at least one member company")

        for row in self.member_companies:
            # Verify company exists
            if not frappe.db.exists("Company", row.company):
                frappe.throw(f"Company {row.company} does not exist")

            # Check if company is in another group
            other_groups = frappe.db.sql(
                """
                SELECT parent
                FROM `tabCompany Group Member`
                WHERE company = %s AND parent != %s
                """,
                (row.company, self.name),
            )
            if other_groups:
                frappe.throw(
                    f"Company {row.company} is already a member of group {other_groups[0][0]}"
                )

    def on_update(self):
        """Update company references when group membership changes."""
        # Update Company.company_group field for all members
        for row in self.member_companies:
            frappe.db.set_value("Company", row.company, "company_group", self.name)

    def on_trash(self):
        """Clean up company references when group is deleted."""
        # Clear company_group field from member companies
        for row in self.member_companies:
            frappe.db.set_value("Company", row.company, "company_group", None)
