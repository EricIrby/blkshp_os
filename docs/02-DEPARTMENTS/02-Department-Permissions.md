# Department Permissions

## Overview

Department Permissions enable user access control at the department level. Users can be assigned to specific departments with read, write, create, and delete permissions.

## Purpose

- Control user access to specific departments
- Enable granular permission management
- Support multi-department access for users
- Integrate with role-based permissions

## DocType Definition

### Department Permission DocType (Child Table)

```python
# Fields
- parent (Link: User)
- parenttype ("User")
- parentfield ("department_permissions")
- department (Link: Department, required)
- can_read (Check)
- can_write (Check)
- can_create (Check)
- can_delete (Check)
```

## Key Features

### User-Department Relationship
- Users can be assigned to multiple departments
- Each assignment has granular permissions
- Maintained via child table on User DocType

### Permission Levels
- **can_read**: View department data
- **can_write**: Modify department data
- **can_create**: Create new records in department
- **can_delete**: Delete records in department

### Integration with Roles
- Department permissions work with role-based permissions
- More restrictive permission applies (role OR department)
- Enables fine-grained access control

## Implementation Steps

### Step 1: Create Child Table DocType
1. Create `Department Permission` as child table DocType
2. Add parent link fields (parent, parenttype, parentfield)
3. Add department link (required)
4. Add permission checkboxes

### Step 2: Add to User DocType
1. Add department_permissions table field to User DocType
2. Configure as child table
3. Set validation rules

### Step 3: Implement Permission Checks
1. Create permission checking methods
2. Integrate with Frappe's permission system
3. Add department filtering to queries

### Step 4: Add UI Components
1. Add department assignment UI in user form
2. Show department permissions clearly
3. Add validation for permission combinations

## Dependencies

- **User DocType**: Parent DocType (Frappe built-in)
- **Department DocType**: Department to assign (from Departments domain)
- **Role-Based Permissions**: Integration with Permissions domain

## Usage Examples

### Single Department Access
```
User: "John Doe"
Department Permissions:
  - Department: "Kitchen"
    Read: Yes
    Write: Yes
    Create: Yes
    Delete: No
```

### Multiple Department Access
```
User: "Jane Smith"
Department Permissions:
  - Department: "Kitchen"
    Read: Yes
    Write: Yes
    Create: Yes
    Delete: No
  - Department: "Catering"
    Read: Yes
    Write: No
    Create: No
    Delete: No
```

## Testing Checklist

- [ ] Assign user to single department
- [ ] Assign user to multiple departments
- [ ] Test read permission
- [ ] Test write permission
- [ ] Test create permission
- [ ] Test delete permission
- [ ] Verify department filtering works correctly
- [ ] Test integration with role-based permissions

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 12.2

