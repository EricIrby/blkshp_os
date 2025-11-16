"""Examples of how to use subscription enforcement in BLKSHP OS.

This file demonstrates various patterns for implementing subscription-based
access control across DocTypes, API endpoints, and background jobs.
"""

from functools import partial

import frappe

from blkshp_os.core_platform.enforcement import (
    enforce_feature_access_for_doctype,
    enforce_module_access_for_doctype,
    require_feature_access,
    require_module_access,
)

# ============================================================================
# Example 1: API Endpoint Enforcement
# ============================================================================


@frappe.whitelist()
@require_module_access("inventory")
def create_stock_entry(item_code, qty, warehouse):
    """Create a stock entry (requires inventory module access).

    This API endpoint is protected by module-level enforcement.
    Tenant users without the inventory module will receive a 403 error.
    BLKSHP Operations staff can access but their actions are logged.
    """
    doc = frappe.get_doc(
        {
            "doctype": "Stock Entry",
            "stock_entry_type": "Material Receipt",
            "items": [
                {
                    "item_code": item_code,
                    "qty": qty,
                    "t_warehouse": warehouse,
                }
            ],
        }
    )
    doc.insert()
    doc.submit()
    return {"status": "success", "name": doc.name}


@frappe.whitelist()
@require_feature_access("analytics.finance_dashboard")
def get_financial_dashboard_data(company, period):
    """Get financial dashboard data (requires specific feature).

    This demonstrates feature-level enforcement. Even if a user has the
    analytics module, they need the specific finance_dashboard feature.
    """
    # Implementation would fetch financial metrics
    return {
        "revenue": 1000000,
        "expenses": 750000,
        "profit": 250000,
    }


@frappe.whitelist()
@require_module_access("procurement")
@require_feature_access("procurement.ottimate_import")
def import_from_ottimate(api_key, date_range):
    """Import data from Ottimate (requires module AND feature).

    This demonstrates stacking multiple enforcement decorators.
    Users need both the procurement module and the ottimate_import feature.
    """
    # Implementation would handle Ottimate integration
    return {"status": "imported", "records": 42}


# ============================================================================
# Example 2: DocType Controller Enforcement
# ============================================================================


class StockEntry:
    """Example DocType controller with enforcement.

    This shows how to add enforcement to DocType lifecycle methods.
    """

    def validate(self):
        """Validate stock entry (requires inventory module)."""
        # Enforce module access before validation
        require_module_access(
            "inventory",
            context={
                "doctype": self.doctype,
                "name": self.name,
                "event": "validate",
            },
        )

        # Continue with normal validation
        self.validate_items()
        self.validate_warehouses()

    def before_submit(self):
        """Before submit hook (requires audit workflow feature for reconciliations)."""
        if self.stock_entry_type == "Stock Reconciliation":
            require_feature_access(
                "inventory.audit_workflows",
                context={
                    "doctype": self.doctype,
                    "name": self.name,
                    "event": "before_submit",
                    "entry_type": self.stock_entry_type,
                },
            )


class PurchaseOrder:
    """Example Purchase Order with module enforcement."""

    def validate(self):
        """Validate purchase order (requires procurement module)."""
        require_module_access(
            "procurement",
            context={
                "doctype": self.doctype,
                "name": self.name,
                "event": "validate",
            },
        )

    def on_submit(self):
        """On submit, check if auto-ordering feature is enabled."""
        if self.is_auto_order:
            require_feature_access(
                "procurement.auto_ordering",
                context={
                    "doctype": self.doctype,
                    "name": self.name,
                    "event": "on_submit",
                },
            )


# ============================================================================
# Example 3: Using hooks.py for DocType Enforcement
# ============================================================================

# In your hooks.py, you can configure enforcement like this:
"""
from functools import partial
from blkshp_os.core_platform.enforcement import (
	enforce_module_access_for_doctype,
	enforce_feature_access_for_doctype,
)

doc_events = {
	# Module-level enforcement for all Stock Entry operations
	"Stock Entry": {
		"before_insert": partial(
			enforce_module_access_for_doctype,
			module_key="inventory"
		),
	},

	# Feature-level enforcement for Stock Reconciliation submits
	"Stock Reconciliation": {
		"before_submit": partial(
			enforce_feature_access_for_doctype,
			feature_key="inventory.audit_workflows"
		),
	},

	# Module enforcement for Purchase Orders
	"Purchase Order": {
		"before_insert": partial(
			enforce_module_access_for_doctype,
			module_key="procurement"
		),
		"before_submit": partial(
			enforce_module_access_for_doctype,
			module_key="procurement"
		),
	},

	# Module enforcement for Products
	"Item": {
		"before_insert": partial(
			enforce_module_access_for_doctype,
			module_key="products"
		),
	},
}
"""


# ============================================================================
# Example 4: Background Job Enforcement
# ============================================================================


def scheduled_inventory_sync():
    """Scheduled job to sync inventory (requires inventory module).

    Background jobs should also enforce subscription rules.
    Use the system user but check module availability for the company.
    """
    # For background jobs, you might want to check per-company
    companies = frappe.get_all("Company", filters={"disabled": 0}, pluck="name")

    for company in companies:
        # Check if this company has inventory module enabled
        try:
            require_module_access(
                "inventory",
                user=frappe.session.user,
                context={
                    "job": "scheduled_inventory_sync",
                    "company": company,
                },
            )

            # Perform sync for this company
            sync_inventory_for_company(company)

        except Exception as e:
            # Log error but continue with other companies
            frappe.log_error(
                title=f"Inventory Sync Failed: {company}",
                message=str(e),
            )


def sync_inventory_for_company(company):
    """Perform actual inventory sync."""
    pass  # Implementation here


# ============================================================================
# Example 5: Conditional Feature Enforcement
# ============================================================================


@frappe.whitelist()
def bulk_update_products(items):
    """Bulk update products with conditional feature enforcement.

    This shows how to conditionally enforce features based on operation type.
    """
    # Always require products module
    require_module_access("products")

    # If bulk operation, require special feature
    if len(items) > 10:
        require_feature_access(
            "products.bulk_operations",
            context={
                "operation": "bulk_update",
                "item_count": len(items),
            },
        )

    # Perform bulk update
    for item in items:
        doc = frappe.get_doc("Item", item["item_code"])
        doc.update(item)
        doc.save()

    return {"status": "success", "updated": len(items)}


# ============================================================================
# Example 6: Checking Access Without Raising Exception
# ============================================================================


@frappe.whitelist()
def get_available_operations():
    """Return list of operations available to current user.

    This demonstrates checking access without raising exceptions,
    useful for building dynamic UIs.
    """
    from blkshp_os.permissions import service as permission_service

    user = frappe.session.user
    operations = []

    # Check module access
    if permission_service.user_has_module_access(user, "inventory"):
        operations.append(
            {
                "key": "create_stock_entry",
                "label": "Create Stock Entry",
                "module": "inventory",
            }
        )

    if permission_service.user_has_module_access(user, "procurement"):
        operations.append(
            {
                "key": "create_purchase_order",
                "label": "Create Purchase Order",
                "module": "procurement",
            }
        )

    # Check feature access
    if permission_service.user_has_feature(user, "products.bulk_operations"):
        operations.append(
            {
                "key": "bulk_update_products",
                "label": "Bulk Update Products",
                "feature": "products.bulk_operations",
            }
        )

    if permission_service.user_has_feature(user, "analytics.finance_dashboard"):
        operations.append(
            {
                "key": "view_finance_dashboard",
                "label": "View Finance Dashboard",
                "feature": "analytics.finance_dashboard",
            }
        )

    return operations


# ============================================================================
# Example 7: Custom Error Messages
# ============================================================================


@frappe.whitelist()
def premium_report():
    """Generate premium report with custom error message."""
    try:
        require_feature_access("analytics.premium_reports")
    except Exception:
        # You can catch and re-raise with custom message
        frappe.throw(
            "This report is only available on Premium and Enterprise plans. "
            "Please contact sales@blkshp.co to upgrade your subscription.",
            title="Premium Feature Required",
        )

    # Generate report
    return {"data": "premium report data"}


# ============================================================================
# Example 8: Report Access Control
# ============================================================================


def get_report_data(report_name, filters):
    """Get report data with enforcement based on report type."""
    # Map reports to required modules/features
    report_requirements = {
        "Stock Balance": {"module": "inventory"},
        "Purchase Analytics": {"module": "procurement"},
        "Financial Dashboard": {"feature": "analytics.finance_dashboard"},
        "Inventory Audit Report": {"feature": "inventory.audit_workflows"},
    }

    requirement = report_requirements.get(report_name, {})

    if "module" in requirement:
        require_module_access(
            requirement["module"],
            context={"report": report_name},
        )
    elif "feature" in requirement:
        require_feature_access(
            requirement["feature"],
            context={"report": report_name},
        )

    # Fetch and return report data
    return {"columns": [], "data": []}
