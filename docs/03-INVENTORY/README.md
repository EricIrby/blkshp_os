# Inventory Domain

## Overview

The Inventory domain manages inventory tracking, audits, and theoretical inventory calculations. Uses a 2D model (Product + Department) with storage as metadata.

## Key Concepts

- **2D Inventory Model**: Inventory tracked by Product + Department combination
- **Theoretical Inventory**: Calculated inventory based on receipts, depletions, transfers
- **Task-Based Audits**: Two-phase audit system (setup by manager, counting by users)
- **Storage as Metadata**: Storage areas tracked but don't create separate inventory buckets

## Dependencies

- **01-PRODUCTS**: Product definitions required
- **02-DEPARTMENTS**: Department definitions required
- **04-PROCUREMENT**: Receiving data affects inventory
- **06-POS-INTEGRATION**: POS depletions affect inventory
- **08-TRANSFERS-DEPLETIONS**: Transfers and depletions affect inventory

## Implementation Priority

**HIGH** - Core functionality domain

## Functions

1. ✅ **Inventory Balance** - 2D inventory model (Product + Department)
2. ✅ **Theoretical Inventory** - Theoretical inventory calculations
3. ✅ **Inventory Audits** - Audit DocType, status workflow
4. ✅ **Counting Tasks** - Task-based counting system
5. ✅ **Audit Lines** - Count recording, unit selection
6. ✅ **Audit Workflows** - Audit lifecycle (Setup → Ready → In Progress → Review → Closed → Locked)
7. ✅ **Audit Enhancements** - Flagging, recounts, corrections, reopening
8. ✅ **Storage Areas** - Storage location management
9. ✅ **Variance Calculations** - Variance calculation (per department)
10. ✅ **Inventory History** - Historical inventory tracking

## Status

✅ **Partially Extracted** - Core functions documented:
- ✅ Inventory Balance (01-Inventory-Balance.md)
- ✅ Theoretical Inventory (02-Theoretical-Inventory.md)
- ✅ Inventory Audits (03-Inventory-Audits.md)
- ✅ Counting Tasks (04-Counting-Tasks.md)
- ✅ Audit Lines (05-Audit-Lines.md)
- ✅ Audit Workflows (06-Audit-Workflows.md)
- ✅ Audit Enhancements (07-Audit-Enhancements.md)
- ✅ Storage Areas (08-Storage-Areas.md)
- ✅ Variance Calculations (09-Variance-Calculations.md)
- ✅ Inventory History (10-Inventory-History.md)

---

**Next Steps**: Inventory domain is complete. Ready for fine-tuning.

