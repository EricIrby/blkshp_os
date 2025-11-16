# Subscription Enforcement System

## Overview

The BLKSHP OS subscription enforcement system provides comprehensive access control based on subscription plans, module activations, and feature toggles. This system ensures that tenant users can only access modules and features included in their subscription plan, while allowing BLKSHP Operations staff to bypass restrictions (with full audit logging).

## Architecture

### Components

1. **enforcement.py** - Core enforcement logic with decorators and helpers
2. **SubscriptionAccessDenied** - Custom exception for access denial
3. **Subscription Access Log** - DocType for audit trail
4. **Integration with permissions service** - Leverages existing permission helpers

### Key Design Decisions

- **Decorator Pattern**: Enforcement can be applied as decorators or direct function calls
- **Fail-Safe Logging**: Logging failures don't break the request
- **Admin Bypass with Audit**: BLKSHP Operations/System Manager/Administrator bypass enforcement but all actions are logged
- **Context-Rich Logging**: Logs include DocType, endpoint, event, IP address, and custom context
- **HTTP 403 Status**: SubscriptionAccessDenied extends frappe.PermissionError for proper HTTP status codes

## Usage

### 1. API Endpoint Enforcement

```python
import frappe
from blkshp_os.core_platform.enforcement import require_module_access, require_feature_access

@frappe.whitelist()
@require_module_access("inventory")
def create_stock_entry(item_code, qty):
    """Create stock entry - requires inventory module."""
    # Implementation
    return {"status": "success"}

@frappe.whitelist()
@require_feature_access("analytics.finance_dashboard")
def get_dashboard_data():
    """Get dashboard data - requires specific feature."""
    return {"revenue": 10000}

# Stack multiple decorators for module + feature
@frappe.whitelist()
@require_module_access("procurement")
@require_feature_access("procurement.ottimate_import")
def import_from_ottimate():
    """Requires both procurement module AND ottimate feature."""
    return {"status": "imported"}
```

### 2. DocType Controller Enforcement

```python
from blkshp_os.core_platform.enforcement import require_module_access

class StockEntry(Document):
    def validate(self):
        """Enforce inventory module access."""
        require_module_access(
            "inventory",
            context={
                "doctype": self.doctype,
                "name": self.name,
                "event": "validate",
            }
        )
        # Continue with validation
```

### 3. DocType Event Hooks (hooks.py)

```python
from functools import partial
from blkshp_os.core_platform.enforcement import (
    enforce_module_access_for_doctype,
    enforce_feature_access_for_doctype,
)

doc_events = {
    "Stock Entry": {
        "before_insert": partial(
            enforce_module_access_for_doctype,
            module_key="inventory"
        ),
    },
    "Stock Reconciliation": {
        "before_submit": partial(
            enforce_feature_access_for_doctype,
            feature_key="inventory.audit_workflows"
        ),
    },
}
```

### 4. Background Jobs

```python
from blkshp_os.core_platform.enforcement import require_module_access

def scheduled_inventory_sync():
    """Scheduled job with enforcement."""
    companies = frappe.get_all("Company", pluck="name")

    for company in companies:
        try:
            require_module_access(
                "inventory",
                context={"job": "inventory_sync", "company": company}
            )
            # Perform sync
        except Exception as e:
            frappe.log_error(title=f"Sync Failed: {company}", message=str(e))
```

### 5. Checking Access Without Exceptions

```python
from blkshp_os.permissions import service as permission_service

def get_available_features():
    """Return features available to current user."""
    user = frappe.session.user
    features = []

    if permission_service.user_has_module_access(user, "inventory"):
        features.append("inventory")

    if permission_service.user_has_feature(user, "analytics.finance_dashboard"):
        features.append("finance_dashboard")

    return features
```

## Exception Handling

### SubscriptionAccessDenied Exception

```python
try:
    require_module_access("inventory")
except SubscriptionAccessDenied as e:
    # Exception attributes:
    # - e.module_key or e.feature_key
    # - e.user
    # - e.http_status_code (403)
    # - str(e) - User-friendly message
    frappe.log_error("Access denied", str(e))
```

## Audit Logging

### Automatic Logging

All enforcement checks are automatically logged to **Subscription Access Log**:

- **Denied Access**: Tenant user blocked from module/feature
- **Admin Bypass**: BLKSHP Operations accessed restricted resource

### Log Contents

Each log entry contains:
- `timestamp` - When the access attempt occurred
- `user` - User who attempted access
- `access_type` - "Module" or "Feature"
- `access_key` - The module_key or feature_key
- `action` - "Denied" or "Bypass"
- `bypass_reason` - Role that granted bypass (if applicable)
- `context_data` - JSON with DocType, endpoint, event, etc.
- `ip_address` - User's IP address

### Viewing Logs

```python
from blkshp_os.core_platform.enforcement import get_access_log_summary

# Get all denied access attempts
denied_logs = get_access_log_summary(action="Denied", limit=100)

# Get logs for specific user
user_logs = get_access_log_summary(user="tenant@example.com")

# Get module access logs
module_logs = get_access_log_summary(access_type="Module")

# API endpoint for users to view their own logs
# GET /api/method/blkshp_os.core_platform.enforcement.get_my_access_logs
```

### Log Retention

Subscription Access Logs are automatically cleared after **90 days** (configured in hooks.py).

## Bypass Roles

The following roles bypass subscription enforcement:

1. **Administrator** - Full bypass
2. **System Manager** - Full bypass
3. **BLKSHP Operations** - Full bypass

All bypass actions are logged for compliance and audit purposes.

## Testing

Comprehensive test suite at: `blkshp_os/blkshp_os/core_platform/tests/test_enforcement.py`

Run tests:
```bash
# In a bench environment:
bench --site your-site run-tests --app blkshp_os --module core_platform.tests.test_enforcement

# Or specific test:
bench --site your-site run-tests blkshp_os.blkshp_os.core_platform.tests.test_enforcement.TestSubscriptionEnforcement.test_module_enforcement_blocks_tenant_user
```

### Test Coverage

- Module enforcement blocks tenant users
- Feature enforcement blocks tenant users
- Admin bypass with logging
- API decorator enforcement
- DocType hook enforcement
- Direct function call enforcement
- Context data logging
- Access log retrieval
- Exception attributes
- Multiple decorators stacking
- Logging enable/disable

## Integration with Existing Systems

### Permission Service

Enforcement leverages existing helpers from `blkshp_os.permissions.service`:
- `user_has_module_access(user, module_key)`
- `user_has_feature(user, feature_key)`
- `_user_bypasses_subscription_gates(user)`

### Feature Matrix Service

Subscription context comes from `blkshp_os.core_platform.services.feature_matrix`:
- `get_subscription_context()`
- Module activation states
- Feature toggle states

## Best Practices

### 1. Choose the Right Enforcement Level

- **Module-level**: For entire feature areas (inventory, procurement, analytics)
- **Feature-level**: For specific capabilities within modules (bulk_operations, audit_workflows)

### 2. Provide Context

Always include context in enforcement calls:
```python
require_module_access(
    "inventory",
    context={
        "doctype": doc.doctype,
        "name": doc.name,
        "event": "validate",
        "additional_info": "any relevant data"
    }
)
```

### 3. Use Decorators for APIs

Decorators are cleaner for API endpoints:
```python
@frappe.whitelist()
@require_module_access("inventory")
def api_method():
    pass
```

### 4. Use Direct Calls in DocType Methods

Direct calls work better in DocType controllers:
```python
def validate(self):
    require_module_access("inventory", context={"doctype": self.doctype})
```

### 5. Use Hooks for Consistent Enforcement

For system-wide enforcement, use hooks.py:
```python
doc_events = {
    "Stock Entry": {
        "before_insert": partial(enforce_module_access_for_doctype, module_key="inventory"),
    }
}
```

### 6. Handle Background Jobs Carefully

Background jobs should check per-company access and handle failures gracefully.

### 7. Build Dynamic UIs

Use `permission_service.user_has_*` methods to show/hide UI elements based on access.

## Troubleshooting

### Issue: Enforcement not triggering

**Solution**: Ensure the DocType event or API endpoint is actually being called. Check hooks.py configuration.

### Issue: Admin users being blocked

**Solution**: Verify the user has one of the bypass roles (Administrator, System Manager, BLKSHP Operations).

### Issue: Logs not being created

**Solution**: Check that `log_denial=True` in enforcement calls. Verify Subscription Access Log DocType exists.

### Issue: Tests failing

**Solution**: Ensure test users have proper roles. Mock `permission_service` functions in tests.

## Future Enhancements

Potential improvements:
1. Rate limiting on access attempts
2. Email notifications for repeated denials
3. Grace period for expired subscriptions
4. Usage analytics per module/feature
5. IP-based access restrictions
6. Time-based access windows

## Support

For questions or issues:
- Review `enforcement_examples.py` for usage patterns
- Check test suite for implementation examples
- Contact BLKSHP Operations team
