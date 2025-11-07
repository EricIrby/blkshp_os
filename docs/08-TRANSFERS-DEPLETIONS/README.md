# Transfers & Depletions Domain

## Overview

The Transfers & Depletions domain manages inventory movements between departments/stores and manual depletion tracking (waste, spillage, etc.).

## Key Concepts

- **Inter-Department Transfers**: Move inventory between departments
- **Inter-Store Transfers**: Move inventory between stores
- **Transfer Workflow**: Status tracking (Draft → Submitted → Acknowledged)
- **Manual Depletions**: Track waste, spillage, consumption manually
- **Department-Aware**: All transfers and depletions are department-specific

## Dependencies

- **01-PRODUCTS**: Product definitions
- **02-DEPARTMENTS**: Source and destination departments
- **03-INVENTORY**: Transfers and depletions update inventory balances

## Implementation Priority

**MEDIUM** - Required for inventory movement tracking

## Functions

1. ✅ **Inventory Transfers** - Inter-department, inter-store transfers
2. ✅ **Transfer Workflow** - Transfer status (Draft → Submitted → Acknowledged)
3. ✅ **Transfer Pricing** - Transfer price updates, cost allocation
4. ✅ **Manual Depletions** - Manual depletion creation
5. ✅ **Depletion Types** - Sold, spilled, wasted, manual
6. ✅ **Depletion Tracking** - Department-aware depletion tracking

## Status

✅ **Partially Extracted** - Core functions documented:
- ✅ Inventory Transfers (01-Inventory-Transfers.md)
- ✅ Transfer Workflow (02-Transfer-Workflow.md)
- ⏳ Transfer Pricing (03-Transfer-Pricing.md) - To be extracted
- ✅ Manual Depletions (04-Manual-Depletions.md)
- ✅ Depletion Types (05-Depletion-Types.md)
- ✅ Depletion Tracking (06-Depletion-Tracking.md) - Covered in Manual Depletions

---

**Next Steps**: Extract Transfer Pricing documentation to complete the domain.

