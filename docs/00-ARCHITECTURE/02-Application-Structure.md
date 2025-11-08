# Application Structure

## Frappe App Layout

The `blkshp_os` repository follows the standard Frappe pattern. The Desk workspace ships inside the `blkshp_os` module (`blkshp_os/blkshp_os/workspace`) so Frappe can auto-discover it during `bench migrate`.

```
blkshp_os/
├── blkshp_os/
│   ├── __init__.py
│   ├── accounting/
│   ├── analytics/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── departments.py
│   │   └── roles.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── desktop.py          # Desk tile configuration
│   ├── departments/
│   ├── permissions/
│   ├── public/
│   │   └── js/
│   ├── scripts/
│   ├── modules.txt             # Registered Frappe modules
│   └── hooks.py                # Application hooks
├── blkshp_os/
│   └── workspace/
│       ├── __init__.py
│       └── blkshp_os/
│           └── blkshp_os.json  # Custom workspace definition
├── docs/
├── fixtures/
├── pyproject.toml
├── README.md
└── scripts/
```

## Core DocTypes Required

### Products Module
- `Product` - Unified product/item master (replaces separate Food/Bev/Supplies items)
- `Product Department` - Product-to-department allocation (many-to-many)
- `Purchase Unit` - Vendor-specific purchase units
- `Product Category` - Category hierarchy (unified)
- `Product Tag` - Custom tags
- `Product Storage` - Storage area assignments

### Departments Module
- `Department` - Department master (Food, Beverage, Supplies, Kitchen, etc.)
- `Department Permission` - User access to departments
- `Department Settings` - Department-specific configurations

### Inventory Module
- `Inventory Audit` - Physical counts with task-based assignments
- `Counting Task` - Department + Storage + Category assignments for counting
- `Audit Line` - Individual count entries
- `Inventory Balance` - Product + Department inventory tracking (2D model)
- `Theoretical Inventory` - Calculated inventory (virtual, department-aware)
- `Storage Area` - Storage locations with default department assignment

### Procurement Module
- `Hospitality Vendor` - Extended vendor master
- `Purchase Order` - Orders to vendors
- `Purchase Order Item` - Order line items
- `Vendor Invoice` - Invoices from vendors
- `Invoice Line` - Invoice line items
- `Invoice Image` - OCR processing queue
- `Vendor Catalog` - Electronic catalogs
- `Order Guide` - Saved ordering templates

### Recipe Module
- `Menu List` - Recipe groupings
- `Recipe` - Recipe master
- `Recipe Ingredient` - Recipe line items
- `Modifier Recipe` - POS modifier recipes
- `Prep Item` - Manufactured items
- `Batch` - Production batches

### POS Integration Module
- `POS System` - POS system connections
- `POS Item Mapping` - Recipe-to-POS mapping
- `POS Modifier Mapping` - Modifier mappings
- `POS Sales Data` - Imported sales transactions
- `POS Depletion` - Calculated depletions

### Accounting Module
- `Accounting System` - Accounting connections
- `Bill` - Synced bills (extends ERPNext Bill)
- `GL Mapping` - Category-to-GL mappings
- `Payee Mapping` - Vendor-to-payee mappings

### Analytics Module
- `Analytics Dashboard` - Dashboard configuration
- `Logbook` - Daily operations log
- `Logbook Note` - Daily notes
- `Logbook Task` - Daily tasks
- `Scheduled Report` - Automated reports

### Director Module
- `Store Sync` - Store synchronization jobs
- `Sync History` - Sync audit trail
- `Corporate Vendor` - Director-level vendors
- `Corporate Item` - Director-level items
- `Corporate Recipe` - Director-level recipes

### Transfer & Depletion Module
- `Inventory Transfer` - Inter-store/Inter-department transfers (physical moves)
- `Transfer Line` - Transfer items
- `Depletion` - Manual depletions (department-aware)
- `Depletion Line` - Depletion items

### Payments Module
- `Bank Account` - Payment accounts
- `Check Run` - Batch payments
- `Payment` - Individual payments
- `Credit Tracker` - Credit memo tracking

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 4

