# Subscription Enforcement - Quick Start Guide

## Installation

The enforcement system is automatically available once the app is installed. The `Subscription Access Log` DocType will be created on first use.

## 5-Minute Quick Start

### 1. Protect an API Endpoint

```python
import frappe
from blkshp_os.core_platform.enforcement import require_module_access

@frappe.whitelist()
@require_module_access("inventory")
def my_inventory_api():
    return {"status": "success"}
```

### 2. Protect a DocType Method

```python
from blkshp_os.core_platform.enforcement import require_module_access

class MyDocType(Document):
    def validate(self):
        require_module_access("inventory", context={
            "doctype": self.doctype,
            "name": self.name
        })
```

### 3. Add to hooks.py

```python
from functools import partial
from blkshp_os.core_platform.enforcement import enforce_module_access_for_doctype

doc_events = {
    "Stock Entry": {
        "before_insert": partial(
            enforce_module_access_for_doctype,
            module_key="inventory"
        ),
    },
}
```

### 4. Feature-Level Protection

```python
from blkshp_os.core_platform.enforcement import require_feature_access

@frappe.whitelist()
@require_feature_access("analytics.finance_dashboard")
def get_dashboard():
    return {"data": "..."}
```

### 5. View Access Logs

```python
from blkshp_os.core_platform.enforcement import get_access_log_summary

# Get all denied access attempts
logs = get_access_log_summary(action="Denied", limit=100)

# Get logs for specific user
user_logs = get_access_log_summary(user="tenant@example.com")
```

## Common Patterns

### API Protection (Decorator Style)

```python
@frappe.whitelist()
@require_module_access("procurement")
def create_purchase_order():
    pass
```

### Multiple Requirements

```python
@frappe.whitelist()
@require_module_access("procurement")
@require_feature_access("procurement.ottimate_import")
def import_data():
    pass
```

### DocType Controller (Function Call Style)

```python
def validate(self):
    require_module_access("inventory", context={"doctype": self.doctype})
```

### Conditional Enforcement

```python
def process_items(items):
    require_module_access("products")

    if len(items) > 10:
        require_feature_access("products.bulk_operations")
```

## Important Notes

1. **Bypass Roles**: Administrator, System Manager, BLKSHP Operations bypass enforcement
2. **All Access is Logged**: Both denials and bypasses are logged
3. **HTTP 403**: Blocked access returns HTTP 403 status
4. **Context is Optional**: But recommended for better audit trails
5. **Log Retention**: Logs are automatically cleared after 90 days

## Testing Your Implementation

```python
# Test that tenant user is blocked
with patch("blkshp_os.permissions.service.user_has_module_access") as mock:
    mock.return_value = False
    with self.assertRaises(SubscriptionAccessDenied):
        my_protected_function()

# Test that admin can access
with patch("blkshp_os.permissions.service._user_bypasses_subscription_gates") as mock:
    mock.return_value = True
    result = my_protected_function()  # Should not raise
```

## Troubleshooting

**Q: My enforcement isn't triggering**
A: Check that the function/hook is actually being called. Add logging to verify.

**Q: Admin users are being blocked**
A: Verify the user has one of: Administrator, System Manager, or BLKSHP Operations roles.

**Q: Logs aren't being created**
A: Ensure `log_denial=True` (it's the default). Check that Subscription Access Log DocType exists.

## More Information

- Full documentation: `ENFORCEMENT_README.md`
- Examples: `enforcement_examples.py`
- Tests: `tests/test_enforcement.py`
