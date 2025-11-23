# BLKSHP OS Admin UI Guide

## Overview

The BLKSHP OS Admin UI provides internal BLKSHP Operations staff with tools to manage tenant subscriptions, feature toggles, and module activations. This interface is **restricted to BLKSHP Operations and System Manager roles only** and is not accessible to tenants.

**Access:** Navigate to the **BLKSHP OS** workspace in Frappe Desk.

---

## Subscription Management

### Manage Tenants Page

The central hub for managing all tenant subscriptions.

**Path:** BLKSHP OS Workspace → Manage Tenants
**Or:** `/app/subscription-management`

#### Features

**Dashboard Stats**
- Total number of tenants
- Tenants with assigned plans
- Tenants without plans

**Tenant Table**
- Company name and code
- Current subscription plan (with badge)
- Billing frequency and price
- Number of enabled modules
- Override indicators

**Actions Per Tenant**
1. **View Details** - See comprehensive tenant information
2. **Change Plan** - Modify subscription plan with audit logging

#### Viewing Tenant Details

Click "Details" on any tenant to see:

**Current Plan Information**
- Plan code and name
- Billing frequency
- Base price

**Modules**
- List of all modules
- Enabled/disabled status
- Required module indicators
- Toggle buttons for non-required modules

**Features**
- All feature toggle states
- Default values and overrides

#### Changing a Subscription Plan

1. Click "Change Plan" for the tenant
2. Select new plan from dropdown
3. Enter reason for change (required for audit)
4. Confirm action

**What Happens:**
- Tenant Branding record is updated
- Change is logged in Subscription Access Log
- Plan takes effect immediately

#### Toggling Modules

From the tenant details dialog:

1. Find the module in the modules list
2. Click "Enable" or "Disable" button (only available for non-required modules)
3. Enter reason for change (required for audit)
4. Confirm action

**Restrictions:**
- Required modules cannot be disabled
- Changes are logged for audit purposes

---

## Subscription Plans

Manage the available subscription tiers.

**Path:** BLKSHP OS Workspace → Subscription Plans
**Or:** `/app/subscription-plan`

### Creating a Plan

1. Click "New" in Subscription Plan list
2. Fill in required fields:
   - **Plan Name** - Human-readable name (e.g., "Standard Tier")
   - **Plan Code** - Unique identifier (e.g., "STANDARD")
   - **Billing Frequency** - Monthly, Quarterly, or Annually
   - **Base Price** - Price per billing period
3. Optionally set as Default Plan
4. Add Feature Overrides in JSON format (optional)
5. Save

### Plan Fields

| Field | Type | Description |
|-------|------|-------------|
| Plan Name | Data | Display name for the plan |
| Plan Code | Data | Unique identifier (uppercase recommended) |
| Default Plan | Check | Mark if this is the default for new tenants |
| Active | Check | Whether plan is available for assignment |
| Billing Frequency | Select | Monthly, Quarterly, or Annually |
| Currency | Link | Billing currency |
| Base Price | Currency | Price charged per billing frequency |
| Description | Text | Plan description and notes |
| Default Feature Overrides | JSON | Feature flag overrides for this plan |

### Feature Overrides Format

Feature overrides are stored as JSON:

```json
{
  "products.bulk_operations": true,
  "inventory.audit_workflows": true,
  "analytics.finance_dashboard": false
}
```

---

## Feature Toggles

Manage available feature flags across the platform.

**Path:** BLKSHP OS Workspace → Feature Toggles
**Or:** `/app/feature-toggle`

### Creating a Feature Toggle

1. Click "New" in Feature Toggle list
2. Fill in required fields:
   - **Feature Name** - Human-readable name
   - **Feature Key** - Programmatic identifier (e.g., "products.bulk_operations")
   - **Category** - Functional area (Products, Inventory, etc.)
   - **Default Enabled** - Whether enabled by default
   - **Description** - What the feature does
   - **Rollout Notes** - Dependencies and context
3. Save

### Feature Categories

- **Core** - Essential platform features
- **Products** - Product catalog features
- **Inventory** - Inventory management features
- **Procurement** - Purchasing features
- **Recipes** - Recipe management features
- **POS** - Point of sale integration
- **Finance** - Financial features
- **Analytics** - Reporting and analytics
- **Permissions** - Access control features

### Feature Key Naming Convention

Use dot notation: `<category>.<feature_name>`

Examples:
- `products.bulk_operations`
- `inventory.audit_workflows`
- `analytics.finance_dashboard`
- `procurement.ottimate_import`

---

## Module Activations

Control which modules are enabled for each subscription plan.

**Path:** BLKSHP OS Workspace → Module Activations
**Or:** `/app/module-activation`

### Understanding Module Activations

Module Activations link a module to a subscription plan and define:
- Whether the module is enabled
- Whether it's required (cannot be disabled)
- Dependencies on other modules
- Feature overrides specific to this module

### Creating a Module Activation

1. Click "New" in Module Activation list
2. Fill in required fields:
   - **Plan** - Link to Subscription Plan
   - **Module Key** - Module identifier (e.g., "products", "inventory")
   - **Module Label** - Display name
   - **Is Enabled** - Whether module is active
   - **Is Required** - Whether module can be disabled
3. Add dependencies if needed
4. Add feature overrides in JSON format (optional)
5. Save

### Module Dependencies

Specify which modules must be enabled before this one:

Example: "Recipes" module depends on "Products" and "Inventory"

```json
["products", "inventory"]
```

---

## Subscription Access Logs

Audit trail of all subscription management actions.

**Path:** BLKSHP OS Workspace → Subscription Logs
**Or:** `/app/subscription-access-log`

### Log Types

- **provision_tenant** - New tenant provisioned
- **unprovision_tenant** - Tenant deprovisioned
- **change_plan** - Subscription plan changed
- **toggle_module** - Module enabled/disabled
- **change_feature** - Feature toggle changed

### Log Fields

| Field | Description |
|-------|-------------|
| Company | Affected company |
| User | Admin who performed action |
| Action | Type of action performed |
| Details | JSON with action details |
| IP Address | Source IP of the action |
| Created | Timestamp of action |

**Logs are immutable** - they cannot be modified or deleted, ensuring audit integrity.

---

## Automation Scripts

BLKSHP OS includes automation scripts for bulk operations.

### Tenant Provisioning Script

Automate setup of new tenants with subscription plans.

#### Single Tenant Provisioning

```bash
bench execute blkshp_os.scripts.provision_tenant.provision \
  --kwargs "{'company': 'ACME Corp', 'plan': 'STANDARD', 'modules': ['products', 'inventory']}"
```

#### Bulk Provisioning

```python
from blkshp_os.scripts.provision_tenant import bulk_provision

tenants = [
    {
        "company": "ACME Corp",
        "plan": "STANDARD",
        "modules": ["products", "inventory"]
    },
    {
        "company": "Hotel XYZ",
        "plan": "PREMIUM",
        "modules": ["products", "inventory", "procurement", "recipes"]
    }
]

results = bulk_provision(tenants)
for result in results:
    print(f"{result['company']}: {result['message']}")
```

#### Unprovisioning

Remove subscription plan from a tenant:

```bash
bench execute blkshp_os.scripts.provision_tenant.unprovision \
  --kwargs "{'company': 'ACME Corp'}"
```

Remove Tenant Branding entirely:

```bash
bench execute blkshp_os.scripts.provision_tenant.unprovision \
  --kwargs "{'company': 'ACME Corp', 'remove_branding': True}"
```

---

## Permissions & Security

### Role-Based Access

**BLKSHP Operations Role**
- Full access to Subscription Management page
- Can change tenant plans
- Can toggle modules
- Can view subscription logs

**System Manager Role**
- Same as BLKSHP Operations
- Can also manage Subscription Plans
- Can manage Feature Toggles
- Can manage Module Activations

**Tenants**
- **No access** to any admin UI
- Can only view their own feature matrix via API

### Audit Logging

All administrative actions are logged to **Subscription Access Log**:
- Who performed the action
- When it was performed
- What was changed
- Why it was changed (reason field)
- Source IP address

Logs are immutable and cannot be deleted, ensuring compliance and audit trail integrity.

---

## Best Practices

### Subscription Plan Management

1. **Use semantic plan codes** - STANDARD, PREMIUM, ENTERPRISE
2. **Set one default plan** - For new tenants
3. **Document feature overrides** - Use description field
4. **Test plan changes** - Verify module dependencies

### Module Management

1. **Mark core modules as required** - Prevent accidental disabling
2. **Document dependencies** - Specify in rollout notes
3. **Test module toggles** - Ensure dependent features work
4. **Always provide a reason** - For audit purposes

### Feature Toggles

1. **Use consistent naming** - Follow `category.feature` pattern
2. **Set sensible defaults** - Based on target plan tier
3. **Document rollout notes** - Dependencies, prerequisites
4. **Communicate changes** - To affected tenants

### Audit & Compliance

1. **Always provide reasons** - When changing plans or modules
2. **Review logs regularly** - Monitor subscription changes
3. **Document major changes** - In change management system
4. **Test before production** - Use staging environment

---

## Troubleshooting

### Tenant Not Showing Expected Features

1. Check tenant's subscription plan in Manage Tenants page
2. Verify module activations for that plan
3. Check feature toggle defaults
4. Review plan's feature overrides
5. Check Subscription Access Log for recent changes

### Cannot Change Module

**Error: "Cannot disable required module"**
- Required modules are marked in Module Activation
- Only non-required modules can be toggled
- Edit Module Activation to make it non-required (use caution)

### Plan Change Not Taking Effect

1. Verify plan exists and is active
2. Check browser console for errors
3. Refresh the page
4. Check Subscription Access Log to confirm change was logged
5. Try logging out and back in

### Provisioning Script Errors

**Error: "Company does not exist"**
- Verify company name/code is correct
- Company must exist before provisioning

**Error: "Plan does not exist"**
- Verify plan code is correct and plan is active
- Create plan first if needed

**Error: "Module not found in plan"**
- Module must have an activation record for the plan
- Create Module Activation first

---

## API Integration

The admin UI can also be accessed programmatically via REST APIs.

### Change Tenant Plan

```python
import frappe

frappe.call(
    method='blkshp_os.blkshp_os.core_platform.page.subscription_management.subscription_management.change_tenant_plan',
    args={
        'company': 'ACME Corp',
        'new_plan': 'PREMIUM',
        'reason': 'Upgrade requested by customer'
    }
)
```

### Toggle Module

```python
frappe.call(
    method='blkshp_os.blkshp_os.core_platform.page.subscription_management.subscription_management.toggle_module',
    args={
        'company': 'ACME Corp',
        'module_key': 'procurement',
        'enabled': True,
        'reason': 'Customer requested procurement module'
    }
)
```

---

## Related Documentation

- [Subscription Model Architecture](/docs/00-ARCHITECTURE/06-Core-Platform.md)
- [Feature Matrix Service](/docs/CORE-PLATFORM-README.md)
- [API Reference](/docs/API-REFERENCE.md)
- [Development Guide](/docs/DEVELOPMENT-GUIDE.md)

---

## Support & Feedback

For issues or feature requests related to the Admin UI:

1. Check this documentation first
2. Review Subscription Access Logs for audit trail
3. Contact BLKSHP Engineering team
4. File an issue in the project repository

---

**Last Updated:** 2025-11-16
**Version:** 1.0
