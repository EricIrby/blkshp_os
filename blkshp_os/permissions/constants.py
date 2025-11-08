"""Permission constants and registry for BLKSHP OS.

This module defines all available permissions in the system, organized by
functional category. These permissions are used in role definitions and
permission checking throughout the application.
"""
from __future__ import annotations

from typing import TypedDict


class PermissionDefinition(TypedDict):
	"""Definition of a single permission."""
	code: str
	name: str
	description: str
	category: str
	department_restricted: bool


# Orders Permissions (11 permissions)
ORDERS_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "orders.view",
		"name": "View Orders",
		"description": "View purchase orders",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.create",
		"name": "Create Orders",
		"description": "Create new purchase orders",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.edit",
		"name": "Edit Orders",
		"description": "Edit draft purchase orders",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.delete",
		"name": "Delete Orders",
		"description": "Delete draft purchase orders",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.place",
		"name": "Place Orders",
		"description": "Submit orders to vendors",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.edit_placed",
		"name": "Edit Placed Orders",
		"description": "Edit orders after they've been placed",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.receive",
		"name": "Receive Orders",
		"description": "Mark orders as received",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.mark_received",
		"name": "Mark Order Received",
		"description": "Mark entire order as received",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.cancel",
		"name": "Cancel Orders",
		"description": "Cancel placed orders",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.view_cost",
		"name": "View Order Costs",
		"description": "View cost information on orders",
		"category": "Orders",
		"department_restricted": True
	},
	{
		"code": "orders.export",
		"name": "Export Orders",
		"description": "Export order data",
		"category": "Orders",
		"department_restricted": True
	}
]

# Invoices Permissions (13 permissions)
INVOICES_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "invoices.view",
		"name": "View Invoices",
		"description": "View vendor invoices",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.create",
		"name": "Create Invoices",
		"description": "Create new invoices",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.edit",
		"name": "Edit Invoices",
		"description": "Edit draft invoices",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.delete",
		"name": "Delete Invoices",
		"description": "Delete draft invoices",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.process",
		"name": "Process Invoices",
		"description": "Process and reconcile invoices",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.approve",
		"name": "Approve Invoices",
		"description": "Approve invoices for payment",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.reject",
		"name": "Reject Invoices",
		"description": "Reject invoices",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.mark_paid",
		"name": "Mark Invoice Paid",
		"description": "Mark invoices as paid",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.view_cost",
		"name": "View Invoice Costs",
		"description": "View cost information on invoices",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.ocr_upload",
		"name": "Upload Invoice OCR",
		"description": "Upload invoices for OCR processing",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.ocr_review",
		"name": "Review OCR Results",
		"description": "Review and correct OCR results",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.export",
		"name": "Export Invoices",
		"description": "Export invoice data",
		"category": "Invoices",
		"department_restricted": True
	},
	{
		"code": "invoices.accounting_export",
		"name": "Export to Accounting",
		"description": "Export invoices to accounting system",
		"category": "Invoices",
		"department_restricted": False
	}
]

# Audits/Inventory Permissions (8 permissions)
AUDITS_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "audits.view",
		"name": "View Audits",
		"description": "View inventory audits",
		"category": "Audits",
		"department_restricted": True
	},
	{
		"code": "audits.open",
		"name": "Open Audit",
		"description": "Open new inventory audit",
		"category": "Audits",
		"department_restricted": True
	},
	{
		"code": "audits.do",
		"name": "Do Audit",
		"description": "Perform inventory counts",
		"category": "Audits",
		"department_restricted": True
	},
	{
		"code": "audits.close",
		"name": "Close Audit",
		"description": "Close and finalize audits",
		"category": "Audits",
		"department_restricted": True
	},
	{
		"code": "audits.delete",
		"name": "Delete Audit",
		"description": "Delete audits",
		"category": "Audits",
		"department_restricted": True
	},
	{
		"code": "audits.view_historic",
		"name": "View Historic Audits",
		"description": "View past audits",
		"category": "Audits",
		"department_restricted": True
	},
	{
		"code": "audits.update_price",
		"name": "Update Item Audit Price",
		"description": "Update item count unit price during audit",
		"category": "Audits",
		"department_restricted": True
	},
	{
		"code": "audits.export",
		"name": "Export Audits",
		"description": "Export audit data",
		"category": "Audits",
		"department_restricted": True
	}
]

# Products/Items Permissions (7 permissions)
ITEMS_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "items.view",
		"name": "View Items",
		"description": "View product/item list",
		"category": "Items",
		"department_restricted": True
	},
	{
		"code": "items.create",
		"name": "Create Items",
		"description": "Create new items",
		"category": "Items",
		"department_restricted": True
	},
	{
		"code": "items.edit",
		"name": "Edit Items",
		"description": "Edit item details",
		"category": "Items",
		"department_restricted": True
	},
	{
		"code": "items.delete",
		"name": "Delete Items",
		"description": "Delete items",
		"category": "Items",
		"department_restricted": True
	},
	{
		"code": "items.import",
		"name": "Import Items",
		"description": "Bulk import items",
		"category": "Items",
		"department_restricted": True
	},
	{
		"code": "items.export",
		"name": "Export Items",
		"description": "Export item data",
		"category": "Items",
		"department_restricted": True
	},
	{
		"code": "items.manage_categories",
		"name": "Manage Item Categories",
		"description": "Create and manage item categories",
		"category": "Items",
		"department_restricted": False
	}
]

# Vendors Permissions (6 permissions)
VENDORS_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "vendors.view",
		"name": "View Vendors",
		"description": "View vendor list",
		"category": "Vendors",
		"department_restricted": False
	},
	{
		"code": "vendors.create",
		"name": "Create Vendors",
		"description": "Create new vendors",
		"category": "Vendors",
		"department_restricted": False
	},
	{
		"code": "vendors.edit",
		"name": "Edit Vendors",
		"description": "Edit vendor details",
		"category": "Vendors",
		"department_restricted": False
	},
	{
		"code": "vendors.delete",
		"name": "Delete Vendors",
		"description": "Delete vendors",
		"category": "Vendors",
		"department_restricted": False
	},
	{
		"code": "vendors.import",
		"name": "Import Vendors",
		"description": "Bulk import vendors",
		"category": "Vendors",
		"department_restricted": False
	},
	{
		"code": "vendors.export",
		"name": "Export Vendors",
		"description": "Export vendor data",
		"category": "Vendors",
		"department_restricted": False
	}
]

# Recipes Permissions (3 permissions)
RECIPES_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "recipes.view",
		"name": "View Recipes",
		"description": "View recipes",
		"category": "Recipes",
		"department_restricted": True
	},
	{
		"code": "recipes.create",
		"name": "Create Recipes",
		"description": "Create new recipes",
		"category": "Recipes",
		"department_restricted": True
	},
	{
		"code": "recipes.edit",
		"name": "Edit Recipes",
		"description": "Edit recipes",
		"category": "Recipes",
		"department_restricted": True
	},
	{
		"code": "recipes.delete",
		"name": "Delete Recipes",
		"description": "Delete recipes",
		"category": "Recipes",
		"department_restricted": True
	}
]

# Transfers & Depletions Permissions (8 permissions)
TRANSFERS_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "transfers.view",
		"name": "View Transfers",
		"description": "View inventory transfers",
		"category": "Transfers",
		"department_restricted": True
	},
	{
		"code": "transfers.create",
		"name": "Create Transfers",
		"description": "Create inventory transfers",
		"category": "Transfers",
		"department_restricted": True
	},
	{
		"code": "transfers.approve",
		"name": "Approve Transfers",
		"description": "Approve transfer requests",
		"category": "Transfers",
		"department_restricted": True
	},
	{
		"code": "transfers.cancel",
		"name": "Cancel Transfers",
		"description": "Cancel transfers",
		"category": "Transfers",
		"department_restricted": True
	}
]

DEPLETIONS_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "depletions.view",
		"name": "View Depletions",
		"description": "View manual depletions",
		"category": "Depletions",
		"department_restricted": True
	},
	{
		"code": "depletions.create",
		"name": "Create Depletions",
		"description": "Create manual depletions",
		"category": "Depletions",
		"department_restricted": True
	},
	{
		"code": "depletions.edit",
		"name": "Edit Depletions",
		"description": "Edit depletions",
		"category": "Depletions",
		"department_restricted": True
	},
	{
		"code": "depletions.delete",
		"name": "Delete Depletions",
		"description": "Delete depletions",
		"category": "Depletions",
		"department_restricted": True
	}
]

# Reports & Analytics Permissions (4 permissions)
REPORTS_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "reports.view",
		"name": "View Reports",
		"description": "View standard reports",
		"category": "Reports",
		"department_restricted": True
	},
	{
		"code": "reports.export",
		"name": "Export Reports",
		"description": "Export report data",
		"category": "Reports",
		"department_restricted": True
	},
	{
		"code": "reports.custom",
		"name": "Create Custom Reports",
		"description": "Create custom reports",
		"category": "Reports",
		"department_restricted": False
	},
	{
		"code": "reports.dashboard",
		"name": "View Dashboard",
		"description": "View analytics dashboard",
		"category": "Reports",
		"department_restricted": True
	}
]

# System & Settings Permissions (5 permissions)
SYSTEM_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "system.settings",
		"name": "Store Settings",
		"description": "Manage store settings",
		"category": "System",
		"department_restricted": False
	},
	{
		"code": "system.users",
		"name": "Manage Users",
		"description": "Create and manage users",
		"category": "System",
		"department_restricted": False
	},
	{
		"code": "system.roles",
		"name": "Manage Roles",
		"description": "Create and manage roles",
		"category": "System",
		"department_restricted": False
	},
	{
		"code": "system.team_accounts",
		"name": "Manage Team Accounts",
		"description": "Manage shared team accounts",
		"category": "System",
		"department_restricted": False
	},
	{
		"code": "system.integrations",
		"name": "Manage Integrations",
		"description": "Configure system integrations",
		"category": "System",
		"department_restricted": False
	}
]

# Director-Level Permissions (8 permissions)
DIRECTOR_PERMISSIONS: list[PermissionDefinition] = [
	{
		"code": "director.view_all_stores",
		"name": "View All Stores",
		"description": "View data across all stores",
		"category": "Director",
		"department_restricted": False
	},
	{
		"code": "director.manage_stores",
		"name": "Manage Stores",
		"description": "Add and manage stores",
		"category": "Director",
		"department_restricted": False
	},
	{
		"code": "director.corporate_vendors",
		"name": "Manage Corporate Vendors",
		"description": "Manage corporate-level vendors",
		"category": "Director",
		"department_restricted": False
	},
	{
		"code": "director.corporate_products",
		"name": "Manage Corporate Products",
		"description": "Manage corporate-level products",
		"category": "Director",
		"department_restricted": False
	},
	{
		"code": "director.corporate_recipes",
		"name": "Manage Corporate Recipes",
		"description": "Manage corporate-level recipes",
		"category": "Director",
		"department_restricted": False
	},
	{
		"code": "director.store_sync",
		"name": "Store Sync Operations",
		"description": "Sync data across stores",
		"category": "Director",
		"department_restricted": False
	},
	{
		"code": "director.reports",
		"name": "Director Reports",
		"description": "Access director-level reports",
		"category": "Director",
		"department_restricted": False
	},
	{
		"code": "director.manage_permissions",
		"name": "Manage Director Permissions",
		"description": "Manage other directors' permissions",
		"category": "Director",
		"department_restricted": False
	}
]

# Aggregate all permissions
ALL_PERMISSIONS: list[PermissionDefinition] = (
	ORDERS_PERMISSIONS +
	INVOICES_PERMISSIONS +
	AUDITS_PERMISSIONS +
	ITEMS_PERMISSIONS +
	VENDORS_PERMISSIONS +
	RECIPES_PERMISSIONS +
	TRANSFERS_PERMISSIONS +
	DEPLETIONS_PERMISSIONS +
	REPORTS_PERMISSIONS +
	SYSTEM_PERMISSIONS +
	DIRECTOR_PERMISSIONS
)

# Permission code to definition mapping
PERMISSION_MAP: dict[str, PermissionDefinition] = {
	perm["code"]: perm for perm in ALL_PERMISSIONS
}

# Permission categories
PERMISSION_CATEGORIES: list[str] = [
	"Orders",
	"Invoices",
	"Audits",
	"Items",
	"Vendors",
	"Recipes",
	"Transfers",
	"Depletions",
	"Reports",
	"System",
	"Director"
]


def get_permission(code: str) -> PermissionDefinition | None:
	"""Get permission definition by code."""
	return PERMISSION_MAP.get(code)


def get_permissions_by_category(category: str) -> list[PermissionDefinition]:
	"""Get all permissions in a category."""
	return [perm for perm in ALL_PERMISSIONS if perm["category"] == category]


def get_all_permission_codes() -> list[str]:
	"""Get list of all permission codes."""
	return [perm["code"] for perm in ALL_PERMISSIONS]


def is_valid_permission(code: str) -> bool:
	"""Check if permission code is valid."""
	return code in PERMISSION_MAP

