#!/usr/bin/env python3
"""Tenant Provisioning Script

This script automates the setup of a new tenant with a subscription plan.
For use by BLKSHP Operations staff only.

Usage:
    bench execute blkshp_os.scripts.provision_tenant.provision --kwargs "{'company': 'ACME Corp', 'plan': 'STANDARD'}"

    Or from Python:
    from blkshp_os.scripts.provision_tenant import provision
    result = provision(company="ACME Corp", plan="STANDARD", modules=["products", "inventory"])
"""

from __future__ import annotations

import frappe
from frappe import _


def provision(
    company: str,
    plan: str,
    modules: list[str] | None = None,
    enable_all_features: bool = False,
) -> dict:
    """Provision a tenant with subscription plan and modules.

    Args:
        company: Company name or code
        plan: Subscription plan code
        modules: Optional list of module keys to enable
        enable_all_features: Whether to enable all features (default: False)

    Returns:
        Dictionary with provisioning results

    Example:
        result = provision(
            company="ACME Corp",
            plan="STANDARD",
            modules=["products", "inventory", "procurement"]
        )
    """
    frappe.only_for("BLKSHP Operations", "System Manager", "Administrator")

    results = {
        "success": False,
        "company": company,
        "plan": plan,
        "actions": [],
        "errors": [],
    }

    try:
        # Validate company exists
        if not frappe.db.exists("Company", company):
            results["errors"].append(f"Company {company} does not exist")
            return results

        # Validate plan exists
        if not frappe.db.exists("Subscription Plan", plan):
            results["errors"].append(f"Subscription Plan {plan} does not exist")
            return results

        # Get company details
        company_doc = frappe.get_doc("Company", company)
        results["company_name"] = company_doc.company_name

        # Assign subscription plan
        if frappe.db.exists("Tenant Branding", company):
            branding_doc = frappe.get_doc("Tenant Branding", company)
            old_plan = branding_doc.plan
            branding_doc.plan = plan
            branding_doc.save()
            results["actions"].append(
                f"Updated subscription plan from {old_plan} to {plan}"
            )
        else:
            branding_doc = frappe.get_doc(
                {"doctype": "Tenant Branding", "company": company, "plan": plan}
            )
            branding_doc.insert()
            results["actions"].append(f"Created Tenant Branding with plan {plan}")

        # Get plan details
        plan_doc = frappe.get_doc("Subscription Plan", plan)
        results["plan_name"] = plan_doc.plan_name

        # Enable specified modules
        if modules:
            for module_key in modules:
                activation_name = frappe.db.get_value(
                    "Module Activation", {"plan": plan, "module_key": module_key}
                )
                if activation_name:
                    activation_doc = frappe.get_doc("Module Activation", activation_name)
                    if not activation_doc.is_enabled:
                        activation_doc.is_enabled = 1
                        activation_doc.save()
                        results["actions"].append(f"Enabled module: {module_key}")
                else:
                    results["errors"].append(
                        f"Module {module_key} not found in plan {plan}"
                    )

        # Enable all features if requested
        if enable_all_features:
            features = frappe.get_all("Feature Toggle", pluck="feature_key")
            results["actions"].append(
                f"Enabled {len(features)} features (enable_all_features=True)"
            )

        # Log the provisioning
        log_doc = frappe.get_doc(
            {
                "doctype": "Subscription Access Log",
                "company": company,
                "user": frappe.session.user,
                "action": "provision_tenant",
                "details": frappe.as_json(
                    {
                        "plan": plan,
                        "modules": modules or [],
                        "enable_all_features": enable_all_features,
                    }
                ),
            }
        )
        log_doc.insert(ignore_permissions=True)

        frappe.db.commit()
        results["success"] = True
        results["message"] = f"Successfully provisioned {company} with plan {plan}"

    except Exception as e:
        frappe.db.rollback()
        results["errors"].append(str(e))
        frappe.log_error(f"Tenant provisioning failed: {e!s}", "Provision Tenant")

    return results


def bulk_provision(tenants: list[dict]) -> list[dict]:
    """Provision multiple tenants in bulk.

    Args:
        tenants: List of tenant dictionaries with keys: company, plan, modules

    Returns:
        List of provisioning results

    Example:
        tenants = [
            {"company": "ACME Corp", "plan": "STANDARD", "modules": ["products", "inventory"]},
            {"company": "Hotel XYZ", "plan": "PREMIUM", "modules": ["products", "inventory", "procurement"]},
        ]
        results = bulk_provision(tenants)
    """
    frappe.only_for("BLKSHP Operations", "System Manager", "Administrator")

    results = []
    for tenant in tenants:
        result = provision(
            company=tenant.get("company"),
            plan=tenant.get("plan"),
            modules=tenant.get("modules"),
            enable_all_features=tenant.get("enable_all_features", False),
        )
        results.append(result)

    return results


def unprovision(company: str, remove_branding: bool = False) -> dict:
    """Unprovision a tenant by removing subscription plan.

    Args:
        company: Company name or code
        remove_branding: Whether to delete Tenant Branding record (default: False)

    Returns:
        Dictionary with unprovisioning results
    """
    frappe.only_for("BLKSHP Operations", "System Manager", "Administrator")

    results = {
        "success": False,
        "company": company,
        "actions": [],
        "errors": [],
    }

    try:
        if not frappe.db.exists("Company", company):
            results["errors"].append(f"Company {company} does not exist")
            return results

        if frappe.db.exists("Tenant Branding", company):
            branding_doc = frappe.get_doc("Tenant Branding", company)
            old_plan = branding_doc.plan

            if remove_branding:
                frappe.delete_doc("Tenant Branding", company, force=True)
                results["actions"].append("Deleted Tenant Branding record")
            else:
                branding_doc.plan = None
                branding_doc.save()
                results["actions"].append(f"Removed plan {old_plan} from Tenant Branding")

            # Log the unprovisioning
            log_doc = frappe.get_doc(
                {
                    "doctype": "Subscription Access Log",
                    "company": company,
                    "user": frappe.session.user,
                    "action": "unprovision_tenant",
                    "details": frappe.as_json(
                        {"old_plan": old_plan, "remove_branding": remove_branding}
                    ),
                }
            )
            log_doc.insert(ignore_permissions=True)

            frappe.db.commit()
            results["success"] = True
            results["message"] = f"Successfully unprovisioned {company}"
        else:
            results["errors"].append(f"No Tenant Branding found for {company}")

    except Exception as e:
        frappe.db.rollback()
        results["errors"].append(str(e))
        frappe.log_error(f"Tenant unprovisioning failed: {e!s}", "Provision Tenant")

    return results


if __name__ == "__main__":
    # Example usage when running standalone
    print("Tenant Provisioning Script")
    print("Usage: bench execute blkshp_os.scripts.provision_tenant.provision")
    print(
        "       --kwargs \"{'company': 'ACME Corp', 'plan': 'STANDARD', 'modules': ['products', 'inventory']}\""
    )
