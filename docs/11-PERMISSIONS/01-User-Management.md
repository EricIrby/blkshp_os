# User Management

## Overview

User management in BLKSHP uses Frappe's built-in User DocType with extensions for department-based access control and team accounts.

## Purpose

- Manage user accounts and authentication
- Assign users to departments
- Assign roles to users
- Support team accounts
- Enable SSO integration

## Key Concepts

### User Accounts
- Standard user accounts with email/password authentication
- Support for team accounts (shared credentials)
- Integration with SSO providers (Okta)

### Department Assignments
- Users assigned to departments via Department Permission child table
- Each assignment has granular permissions
- Users can belong to multiple departments

### Role Assignments
- Users assigned to roles
- Roles define permission sets
- Users can have multiple roles
- User-level permission overrides supported

## Implementation Steps

### Step 1: Extend User DocType
1. Add department_permissions child table
2. Add custom fields if needed
3. Configure team account support

### Step 2: Implement Department Permissions
1. Create Department Permission child table
2. Add to User DocType
3. Implement permission checking logic

### Step 3: Add Team Account Support
1. Add team account flag
2. Implement team account management
3. Add validation rules

### Step 4: SSO Integration
1. Configure SSO provider (Okta)
2. Implement SSO authentication
3. Map SSO groups to roles/departments

## Dependencies

- **Frappe User DocType**: Base user management (Frappe built-in)
- **Department DocType**: For department assignments
- **Role System**: For role assignments (see Role Definitions)

## Testing Checklist

- [ ] Create user account
- [ ] Assign user to departments
- [ ] Assign roles to user
- [ ] Test user-level permission overrides
- [ ] Test team account creation
- [ ] Test SSO authentication
- [ ] Verify department filtering works

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 12

