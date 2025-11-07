# Role Definitions

## Overview

BLKSHP provides standard/default roles as templates, but all roles are customizable. Users can create unlimited custom roles with any permission combination.

## Key Principles

### Flexible Role System
- **No Hard-Coded Roles**: All roles are customizable and can be created/modified
- **Standard Roles as Templates**: Default roles provided as starting points for common use cases
- **Custom Role Creation**: Create unlimited custom roles with any permission combination
- **User-Level Permission Overrides**: Override role permissions for specific users when needed

### Role Assignment
- Users can be assigned multiple roles
- Permissions are additive (user gets all permissions from all roles)
- User-level overrides can restrict permissions
- Account Owner has full admin privileges (cannot be restricted)

## Standard Roles (Default Templates)

### Audit / Inventory Taker Only

**Purpose**: For users who only count inventory

**Recommended Permissions:**
- Open Audit
- Do Audit

**Department Assignment**: Assign to specific departments they will count

**Example Use Case**: Temporary staff hired for monthly inventory counts

---

### Audit / Inventory Administrator

**Purpose**: For users who assist with inventory counting and are responsible for opening and closing audits

**Recommended Permissions:**
- Open Audit
- Do Audit
- Close Audit
- Delete Audit
- View Historic Audits
- Update Item's Audit CU Price

**Department Assignment**: Assign to specific departments they manage

**Example Use Case**: Store managers who manage inventory counts

---

### Recipe Builder / Chef

**Purpose**: For users who need the ability to build, modify, and delete recipes

**Recommended Permissions:**
- Create Recipes
- Edit Recipes
- Delete Recipes
- View Recipes
- Create Menu Lists
- Edit Menu Lists
- Delete Menu Lists

**Department Assignment**: Assign to departments where they build recipes

**Example Use Case**: Chefs and kitchen managers

---

### Buyer / Purchasing / Order Placer

**Purpose**: For users responsible for placing purchase orders

**Recommended Permissions:**
- Create Orders
- Edit Orders
- Place Orders
- Edit Placed Orders
- Receive Orders
- View Orders
- View Vendors
- View Items

**Department Assignment**: Assign to departments they purchase for

**Example Use Case**: Purchasing managers, buyers

---

### Receiver / Head of Purchasing & Procurement

**Purpose**: For users who receive orders and manage procurement

**Recommended Permissions:**
- All Buyer permissions
- Receive Orders
- Mark Order Received
- View Invoices
- Process Invoices
- Approve Invoices

**Department Assignment**: Assign to departments they manage

**Example Use Case**: Receiving managers, procurement heads

---

### Bartender

**Purpose**: For bar staff who manage beverages and pours

**Recommended Permissions:**
- View Items (Beverage department only)
- Create Pours
- Edit Pours
- View Recipes (Beverage recipes)
- View Audits (Beverage department only)
- Do Audit (Beverage department only)

**Department Assignment**: Assign to Beverage/Bar department

**Example Use Case**: Bartenders, bar managers

---

### High-Level Roles (GM, AM, Admin, IT)

**Purpose**: For general managers, area managers, administrators, and IT staff

**Recommended Permissions:**
- Most read permissions across all departments
- Limited write permissions (as needed)
- View Reports
- Manage Team Accounts (for admins)
- Store Settings (for admins)

**Department Assignment**: All departments or as needed

**Example Use Case**: General managers, administrators

---

### Director Operations

**Purpose**: For Director-level users managing multiple locations

**Recommended Permissions:**
- All Director-level permissions
- View All Director Dashboard Trends
- View All Director Reports
- Manage Corporate Vendors
- Manage Corporate Products
- Manage Corporate Recipes
- Store Sync Operations

**Department Assignment**: All stores and departments

**Example Use Case**: Director of operations, corporate managers

---

### Account Owner

**Purpose**: Full admin with all permissions

**Recommended Permissions:**
- All permissions (cannot be restricted)
- Manage Other Directors' Permissions
- Add Store
- All system administration

**Department Assignment**: All stores and departments

**Note**: Account owner permissions cannot be restricted or overridden.

---

## Creating Custom Roles

### Steps to Create Custom Role

1. **Create Role**: Create new role in Frappe
2. **Assign Permissions**: Select permissions from permission matrix
3. **Set Department Restrictions**: Configure department restrictions if needed
4. **Assign to Users**: Assign role to users
5. **Test**: Verify permissions work as expected

### Best Practices

- **Start with Standard Roles**: Use standard roles as templates
- **Principle of Least Privilege**: Grant minimum permissions needed
- **Document Custom Roles**: Document purpose and permissions
- **Regular Review**: Review and update roles regularly
- **Test Thoroughly**: Test permissions with different user scenarios

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 12.4

