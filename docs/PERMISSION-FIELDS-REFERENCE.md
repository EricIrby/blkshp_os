# Permission Fields Reference

## Department Permission Fields

The `Department Permission` child table (attached to User DocType) has the following permission flags:

### Available Permission Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `department` | Link | Link to Department DocType | Required |
| `is_active` | Check | Whether this permission is active | 1 |
| `can_read` | Check | Can view/read department data | 0 |
| `can_write` | Check | Can edit department data | 0 |
| `can_create` | Check | Can create new records for department | 0 |
| `can_delete` | Check | Can delete department records | 0 |
| `can_submit` | Check | Can submit documents for department | 0 |
| `can_cancel` | Check | Can cancel submitted documents | 0 |
| `can_approve` | Check | Can approve documents/transactions | 0 |
| `valid_from` | Date | Permission effective start date | Optional |
| `valid_upto` | Date | Permission expiration date | Optional |
| `notes` | Small Text | Additional notes about the permission | Optional |

### Usage Example

```python
# Creating a user with department permissions
user = frappe.get_doc({
    "doctype": "User",
    "email": "buyer@example.com",
    "first_name": "Test",
    "last_name": "Buyer"
})

# Add department permission
user.append("department_permissions", {
    "department": "KITCHEN",
    "can_read": 1,
    "can_write": 1,
    "can_create": 1,
    "can_approve": 1,
    "is_active": 1
})

user.insert()
```

---

## Role Permission Fields

The `Role Permission` child table (attached to Role DocType) has the following fields:

### Available Permission Fields

| Field | Type | Description | Default |
|-------|------|-------------|---------|
| `permission_code` | Data | Unique permission code (e.g., "orders.view") | Required |
| `permission_name` | Data | Human-readable permission name | Auto-populated |
| `is_granted` | Check | Whether permission is granted | 1 |
| `permission_category` | Data | Category (Orders, Invoices, etc.) | Auto-populated |
| `description` | Small Text | Permission description | Auto-populated |
| `department_restricted` | Check | If permission is department-specific | Auto-populated |

### Usage Example

```python
# Creating a custom role with permissions
role = frappe.get_doc({
    "doctype": "Role",
    "role_name": "Custom Buyer",
    "is_custom_role": 1,
    "role_description": "Custom buyer role with limited permissions"
})

# Add permissions
role.append("custom_permissions", {
    "permission_code": "orders.view",
    "is_granted": 1
})

role.append("custom_permissions", {
    "permission_code": "orders.create",
    "is_granted": 1
})

role.insert()
```

---

## Common Permission Patterns

### Read-Only Access

```python
{
    "department": "KITCHEN",
    "can_read": 1,
    "is_active": 1
}
```

### Standard User Access

```python
{
    "department": "KITCHEN",
    "can_read": 1,
    "can_write": 1,
    "can_create": 1,
    "is_active": 1
}
```

### Manager Access

```python
{
    "department": "KITCHEN",
    "can_read": 1,
    "can_write": 1,
    "can_create": 1,
    "can_delete": 1,
    "can_submit": 1,
    "can_approve": 1,
    "is_active": 1
}
```

### Full Access

```python
{
    "department": "KITCHEN",
    "can_read": 1,
    "can_write": 1,
    "can_create": 1,
    "can_delete": 1,
    "can_submit": 1,
    "can_cancel": 1,
    "can_approve": 1,
    "is_active": 1
}
```

### Temporary Access (with expiration)

```python
{
    "department": "KITCHEN",
    "can_read": 1,
    "can_write": 1,
    "is_active": 1,
    "valid_from": "2025-01-01",
    "valid_upto": "2025-12-31"
}
```

---

## Permission Hierarchy

### Department Permissions (User-Level)

Department permissions control **which departments** a user can access and **what actions** they can perform within those departments.

**Scope:** Department-specific data access

**Example Use Cases:**
- Buyer can only order for Kitchen and Bar departments
- Inventory taker can only audit Kitchen department
- Manager can access all departments with full permissions

### Role Permissions (Role-Level)

Role permissions control **what features/functions** a user can access across the application.

**Scope:** Application-wide feature access

**Example Use Cases:**
- "orders.create" - Can create purchase orders
- "audits.do" - Can perform inventory audits
- "reports.view_cost" - Can view cost reports

### Combined Access Control

Both permission types work together:

1. **Role Permission** determines if user can access a feature (e.g., "orders.create")
2. **Department Permission** determines which departments they can use that feature for

**Example:**
- User has role permission "orders.create" ✓
- User has department permission for "KITCHEN" with `can_create: 1` ✓
- **Result:** User can create orders for Kitchen department

---

## Important Notes

### ❌ Invalid Fields

These fields **DO NOT EXIST** and will cause errors:

- ~~`can_order`~~ - Use `can_create` instead
- ~~`can_audit`~~ - Use role permission "audits.do" instead
- ~~`can_transfer`~~ - Use role permission "transfers.create" instead
- ~~`can_receive`~~ - Use role permission "receiving.create" instead
- ~~`can_view_cost`~~ - Use role permission "reports.view_cost" instead

### ✅ Correct Approach

**Don't:** Try to add domain-specific permissions to Department Permission
```python
# WRONG - these fields don't exist
{
    "department": "KITCHEN",
    "can_order": 1,      # ❌ Invalid
    "can_audit": 1,      # ❌ Invalid
    "can_transfer": 1    # ❌ Invalid
}
```

**Do:** Use generic CRUD permissions + role-based permissions
```python
# CORRECT - use standard CRUD permissions
{
    "department": "KITCHEN",
    "can_read": 1,       # ✓ Valid
    "can_write": 1,      # ✓ Valid
    "can_create": 1,     # ✓ Valid
    "can_approve": 1     # ✓ Valid
}

# Then assign role with specific permissions
user.append("roles", {"role": "Buyer"})  # Has "orders.create" permission
```

---

## Validation Rules

### Department Permission Validation

1. **Department is required** - Must link to an existing, active department
2. **At least one permission** - Must select at least one permission flag
3. **Company alignment** - Department's company must match user's company (if set)
4. **No duplicates** - Cannot assign same department twice to same user
5. **Date validation** - `valid_upto` must be after `valid_from`

### Role Permission Validation

1. **Permission code is required** - Must be a valid code from the registry
2. **Auto-population** - Name, category, and description are auto-filled
3. **Valid permission** - Code must exist in `permissions.constants.ALL_PERMISSIONS`

---

## API Reference

### Check Department Permission

```python
from blkshp_os.permissions.service import has_department_permission

# Check if user can create in Kitchen department
can_create = has_department_permission(
    user="buyer@example.com",
    department="KITCHEN",
    permission="can_create"
)
```

### Get Accessible Departments

```python
from blkshp_os.permissions.service import get_accessible_departments

# Get all departments user can read
departments = get_accessible_departments(
    user="buyer@example.com",
    permission="can_read"
)
```

### Check Role Permission

```python
from blkshp_os.permissions.roles import has_permission

# Check if user has permission to create orders
can_create_orders = has_permission(
    user="buyer@example.com",
    permission_code="orders.create"
)
```

---

## See Also

- **Permission Registry**: `blkshp_os/permissions/constants.py`
- **Permission Service**: `blkshp_os/permissions/service.py`
- **Role Service**: `blkshp_os/permissions/roles.py`
- **API Documentation**: `docs/API-REFERENCE.md`
- **Implementation Summary**: `docs/11-PERMISSIONS/IMPLEMENTATION-SUMMARY.md`

