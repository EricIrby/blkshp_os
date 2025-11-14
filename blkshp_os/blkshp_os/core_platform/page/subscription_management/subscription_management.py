"""Subscription Management Page - Backend Methods

This module provides backend methods for the BLKSHP Operations subscription management interface.
All methods are restricted to BLKSHP Operations and System Manager roles.
"""

from __future__ import annotations

from typing import Any

import frappe
from frappe import _

from blkshp_os.blkshp_os.core_platform.services.subscription_context import (
	get_subscription_context,
	resolve_plan_for_company,
)


@frappe.whitelist()
def get_all_tenants() -> list[dict[str, Any]]:
	"""
	Get all companies with their subscription details.

	Returns:
		List of tenant dictionaries with company, plan, and module information.
	"""
	frappe.only_for("BLKSHP Operations", "System Manager")

	# Get all companies
	companies = frappe.get_all(
		"Company",
		fields=["name", "company_name", "abbr", "country"],
		filters={"is_group": 0},  # Only leaf companies, not parent groups
		order_by="company_name asc",
	)

	tenants = []
	for company in companies:
		# Get plan from Tenant Branding
		plan_code = resolve_plan_for_company(company.name)

		# Get subscription context
		context = get_subscription_context(company=company.name)

		# Count enabled modules
		enabled_modules = [
			{"key": mod.key, "label": mod.label, "is_required": mod.is_required}
			for mod in context.modules.values()
			if mod.is_enabled
		]

		tenant_data = {
			"company": company.name,
			"company_name": company.company_name,
			"abbr": company.abbr,
			"country": company.country,
			"plan_code": plan_code,
			"plan_name": context.plan.plan_name if context.plan else None,
			"billing_frequency": context.plan.billing_frequency if context.plan else None,
			"base_price": context.plan.base_price if context.plan else None,
			"enabled_modules": enabled_modules,
			"module_count": len(enabled_modules),
			"has_overrides": bool(context.plan and context.plan.default_feature_overrides)
			if context.plan
			else False,
		}
		tenants.append(tenant_data)

	return tenants


@frappe.whitelist()
def get_tenant_details(company: str) -> dict[str, Any]:
	"""
	Get detailed subscription information for a specific tenant.

	Args:
		company: Company name

	Returns:
		Detailed tenant information with full module and feature data.
	"""
	frappe.only_for("BLKSHP Operations", "System Manager")

	if not frappe.db.exists("Company", company):
		frappe.throw(_("Company {0} does not exist").format(company))

	# Get subscription context
	context = get_subscription_context(company=company)

	# Get all available plans
	available_plans = frappe.get_all(
		"Subscription Plan",
		filters={"is_active": 1},
		fields=["name", "plan_code", "plan_name", "billing_frequency", "base_price"],
		order_by="plan_name asc",
	)

	# Get current plan details
	current_plan = None
	if context.plan:
		current_plan = {
			"code": context.plan.plan_code,
			"name": context.plan.plan_name,
			"billing_frequency": context.plan.billing_frequency,
			"base_price": context.plan.base_price,
			"is_default": context.plan.is_default,
		}

	# Get module details
	modules = [
		{
			"key": mod.key,
			"label": mod.label,
			"is_enabled": mod.is_enabled,
			"is_required": mod.is_required,
			"depends_on": list(mod.depends_on),
			"feature_overrides": dict(mod.feature_overrides),
		}
		for mod in context.modules.values()
	]

	# Get feature states
	features = [
		{
			"key": key,
			"name": meta.name,
			"category": meta.category,
			"value": context.feature_states.get(key),
			"default": meta.default_enabled,
		}
		for key, meta in context.registry.items()
	]

	return {
		"company": company,
		"current_plan": current_plan,
		"available_plans": available_plans,
		"modules": modules,
		"features": features,
	}


@frappe.whitelist()
def change_tenant_plan(company: str, new_plan: str, reason: str = "") -> dict[str, Any]:
	"""
	Change the subscription plan for a tenant.

	Args:
		company: Company name
		new_plan: New subscription plan code
		reason: Reason for the change (for audit log)

	Returns:
		Success message and updated tenant data.
	"""
	frappe.only_for("BLKSHP Operations", "System Manager")

	if not frappe.db.exists("Company", company):
		frappe.throw(_("Company {0} does not exist").format(company))

	if not frappe.db.exists("Subscription Plan", new_plan):
		frappe.throw(_("Subscription Plan {0} does not exist").format(new_plan))

	# Get or create Tenant Branding record
	if frappe.db.exists("Tenant Branding", company):
		branding_doc = frappe.get_doc("Tenant Branding", company)
		old_plan = branding_doc.plan
		branding_doc.plan = new_plan
		branding_doc.save()
	else:
		branding_doc = frappe.get_doc(
			{
				"doctype": "Tenant Branding",
				"company": company,
				"plan": new_plan,
			}
		)
		old_plan = None
		branding_doc.insert()

	# Log the change
	_log_admin_action(
		action="change_plan",
		company=company,
		details={
			"old_plan": old_plan,
			"new_plan": new_plan,
			"reason": reason,
		},
	)

	frappe.db.commit()

	return {
		"success": True,
		"message": _("Subscription plan updated to {0}").format(new_plan),
		"old_plan": old_plan,
		"new_plan": new_plan,
	}


@frappe.whitelist()
def toggle_module(
	company: str, module_key: str, enabled: bool, reason: str = ""
) -> dict[str, Any]:
	"""
	Enable or disable a specific module for a tenant.

	Args:
		company: Company name
		module_key: Module key to toggle
		enabled: Whether to enable or disable (accepts bool, int, or string)
		reason: Reason for the change (for audit log)

	Returns:
		Success message.
	"""
	frappe.only_for("BLKSHP Operations", "System Manager")

	# Convert enabled to boolean (handles string "true"/"false" from JavaScript)
	enabled = frappe.parse_json(enabled) if isinstance(enabled, str) else bool(enabled)

	if not frappe.db.exists("Company", company):
		frappe.throw(_("Company {0} does not exist").format(company))

	# Get current plan
	plan_code = resolve_plan_for_company(company)
	if not plan_code:
		frappe.throw(_("No subscription plan assigned to {0}").format(company))

	# Check if module activation exists
	# Get the Module Activation document name
	activation_name = frappe.db.get_value(
		"Module Activation",
		{"plan": plan_code, "module_key": module_key},
		"name"
	)
	if not activation_name:
		frappe.throw(
			_("Module {0} not found in plan {1}").format(module_key, plan_code)
		)

	# Update module activation
	activation_doc = frappe.get_doc("Module Activation", activation_name)

	# Check if module is required
	if not enabled and activation_doc.is_required:
		frappe.throw(_("Cannot disable required module {0}").format(module_key))

	old_state = activation_doc.is_enabled
	activation_doc.is_enabled = int(enabled)
	activation_doc.save()

	# Log the change
	_log_admin_action(
		action="toggle_module",
		company=company,
		details={
			"module_key": module_key,
			"old_state": bool(old_state),
			"new_state": enabled,
			"reason": reason,
		},
	)

	frappe.db.commit()

	return {
		"success": True,
		"message": _("Module {0} {1}").format(
			module_key, _("enabled") if enabled else _("disabled")
		),
	}


def _log_admin_action(action: str, company: str, details: dict[str, Any]) -> None:
	"""
	Log an admin action to the Subscription Access Log.

	Args:
		action: Action type (e.g., 'change_plan', 'toggle_module')
		company: Company affected
		details: Additional details about the action
	"""
	try:
		log_doc = frappe.get_doc(
			{
				"doctype": "Subscription Access Log",
				"company": company,
				"user": frappe.session.user,
				"action": action,
				"details": frappe.as_json(details),
				"ip_address": frappe.local.request_ip if hasattr(frappe.local, "request_ip") else None,
			}
		)
		log_doc.insert(ignore_permissions=True)
	except Exception as e:
		# Don't fail the main operation if logging fails
		frappe.log_error(f"Failed to log admin action: {str(e)}", "Subscription Management")
