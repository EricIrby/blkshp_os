# Permissions Matrix

## Overview

BLKSHP implements a comprehensive permission system with 50+ permissions organized into functional categories. This document provides an overview of all available permissions.

## Permission System Principles

### Key Principles
- **Flexible Role System**: Standard/default roles are provided as templates, but users can create unlimited custom roles with any permission combination
- **User-Level Overrides**: Individual users can have permissions overridden at the user level, independent of their role assignments
- **Department-Based Access**: Users can be assigned to specific departments or multiple departments
- **Permission-Based Control**: Permissions are organized by functional areas (Orders, Inventory, Recipes, etc.) and can be mixed and matched
- **Granular Control**: Field-level and document-level permissions for sensitive operations
- **Hierarchical Structure**: Director-level permissions for multi-location management
- **Account Owner**: Full admin privileges, cannot be restricted

### Permission Categories

The permission system includes the following categories:

1. **Orders Permissions** (11 permissions)
2. **Invoices Permissions** (13 permissions)
3. **Audits Permissions** (8 permissions)
4. **Depletions Permissions** (4 permissions)
5. **Transfers Permissions** (4 permissions)
6. **Reports Permissions** (4 permissions)
7. **POS Permissions** (2 permissions)
8. **Items Permissions** (7 permissions)
9. **Vendors Permissions** (6 permissions)
10. **Recipes Permissions** (3 permissions)
11. **Preps Permissions** (3 permissions)
12. **Modifier Permissions** (2 permissions)
13. **Item Tags Permissions** (4 permissions)
14. **Store Settings Permissions** (3 permissions)
15. **Item Manager Permissions** (4 permissions)
16. **Dashboard Trends Permissions** (3 permissions)
17. **Director Reviews Permissions** (4 permissions)
18. **Markets Permissions** (3 permissions)
19. **Menu Lists Permissions** (3 permissions)
20. **Director Operations Permissions** (8 permissions)
21. **Director Dashboard Trends** (3 permissions)

**Total: 50+ permissions**

## Department Restrictions

Most permissions support department restrictions:
- **Department-Restricted**: Permission only applies to assigned departments
- **Global**: Permission applies across all departments (e.g., View Reports)

## Detailed Permission Lists

For detailed permission definitions, see:
- [Orders Permissions](orders-permissions.md) - Order creation, editing, receiving
- [Invoices Permissions](invoices-permissions.md) - Invoice processing, approval
- [Audits Permissions](audits-permissions.md) - Audit opening, counting, closing
- [Items Permissions](items-permissions.md) - Product management, editing
- [Vendors Permissions](vendors-permissions.md) - Vendor management
- [Recipes Permissions](recipes-permissions.md) - Recipe creation, editing
- [Director Permissions](director-permissions.md) - Director-level operations

## Implementation Notes

### Permission Types
- **Document Permissions**: Read, Write, Create, Delete, Submit, Cancel
- **Field Permissions**: Read, Write per field
- **Custom Permissions**: Application-specific permissions (e.g., "Open Audit", "Place Order")

### Permission Checking
- Permissions checked at document level
- Department filtering applied automatically
- More restrictive permission applies (role OR department)

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 12.3

**Note**: Detailed permission definitions are in Section 12.3 of the master plan. Individual permission category documents can be created as needed.

