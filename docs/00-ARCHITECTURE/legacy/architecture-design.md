# Architecture Design

> **Legacy Reference:** Retained for historical design notes. For current architecture, see `00-ARCHITECTURE/01-App-Structure.md`.

## Multi-Tenancy Structure

Frappe's native Company hierarchy maps to BLKSHP's Director/Store structure, with **Department-based segmentation** instead of separate platforms:

```
Director (Company)
├── Store 1 (Company)
│   ├── Food & Beverage (Department)
│   ├── Beverage (Department)
│   ├── Supplies (Department)
│   └── Kitchen (Department)
├── Store 2 (Company)
│   └── [Same Department Structure]
└── Store 3 (Company)
    └── [Same Department Structure]
```

### Implementation

- Use Frappe's `Company` DocType for Director and Stores
- Use custom `Department` DocType for segmentation (Food, Beverage, Supplies, etc.)
- All products, items, and inventory managed in single unified system
- Departments enable:
  - Product allocations (assign products to specific departments)
  - Inter-department transfers
  - Department-specific permissions and access control
  - Department-level reporting and analytics
  - Department-specific inventory tracking

## Module Breakdown

**Core Modules:**

1. **Products** - Unified product/item management (all types in one system)
2. **Departments** - Department management, allocations, permissions
3. **Inventory** - Inventory tracking, audits, theoretical inventory (department-aware)
4. **Procurement** - Vendors, orders, invoices (department-aware)
5. **Recipes** - Recipe management and costing
6. **POS Integration** - POS connectivity and depletions
7. **Accounting** - Accounting integration and bill sync
8. **Analytics** - Reporting and dashboards (department-filtered)
9. **Director** - Multi-location management
10. **Payments** - Payment processing

## Department-Based Architecture

### Key Principles

- **Single Product Master**: All products (food, beverage, supplies) in one unified system
- **Department Segmentation**: Products assigned to departments for organization
- **Flexible Allocation**: Products can belong to multiple departments
- **Department Transfers**: Move inventory between departments seamlessly
- **Permission-Based Access**: Users can have access to specific departments
- **Department Reporting**: All reports filterable by department

### Benefits

- **Simplified Management**: One product master instead of multiple platforms
- **Flexible Organization**: Products can belong to multiple departments
- **Granular Permissions**: Users only see departments they have access to
- **Unified Reporting**: All reports work across departments
- **Seamless Transfers**: Move inventory between departments easily

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 3

