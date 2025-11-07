# Department Master

## Overview

The Department DocType is the foundation for department-based segmentation. Departments enable flexible product management, permissions, and reporting without requiring separate platforms.

## Purpose

- Organize products, inventory, and operations by department
- Enable department-based access control
- Support department-specific settings (par levels, GL codes, storage areas)
- Enable inter-department transfers and reporting

## DocType Definition

### Fields

```python
# Core Fields
- department_name (Data, required)
- department_code (Data, unique)
- department_type (Select: Food, Beverage, Supplies, Kitchen, Bar, etc.)
- parent_department (Link: Department)  # For sub-departments
- company (Link: Company, required)
- is_active (Check)
- default_storage_area (Link: Storage Area)
- default_gl_code (Link: Account)
- settings (JSON)  # Department-specific settings
```

### Methods

```python
def get_products(department):
    """Get all products assigned to department"""
    pass

def get_users(department):
    """Get all users with access to department"""
    pass
```

## Implementation Steps

### Step 1: Create DocType
1. Create `Department` DocType in Frappe
2. Add core fields (name, code, type)
3. Add company link (required for multi-tenancy)
4. Add parent department link (for sub-departments)

### Step 2: Add Department Settings
1. Add default storage area field
2. Add default GL code field
3. Add settings JSON field for extensibility
4. Add is_active checkbox

### Step 3: Implement Methods
1. Implement `get_products()` method
2. Implement `get_users()` method
3. Add validation rules (unique code per company)

### Step 4: Set Permissions
1. Set role-based permissions
2. Configure department-level access control
3. Set field-level permissions if needed

## Dependencies

- **Frappe Company DocType**: Required for multi-tenancy
- **Storage Area DocType**: For default storage assignment (from Inventory domain)
- **Account DocType**: For default GL code (from Accounting/ERPNext)

## Testing Checklist

- [ ] Create department with valid data
- [ ] Verify department code uniqueness per company
- [ ] Test parent department relationship
- [ ] Verify products can be assigned to department
- [ ] Verify users can be assigned to department
- [ ] Test department deactivation
- [ ] Verify permissions work correctly

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

