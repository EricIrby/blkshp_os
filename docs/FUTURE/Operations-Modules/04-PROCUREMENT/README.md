# Procurement Domain

## Overview

The Procurement domain manages vendors, purchase orders, receiving, and invoice processing. Note: Detailed ordering and invoice processing workflows are deferred to Phase 6 (after Ottimate contract ends).

## Key Concepts

- **Vendor Master**: Comprehensive vendor management with contact details
- **Ottimate Integration**: Flatfile import for receiving data (current implementation)
- **Invoice Structure**: Basic invoice DocType with department allocation
- **Phase 6 Deferred**: Detailed ordering, receiving, and invoice processing workflows

## Dependencies

- **01-PRODUCTS**: Product definitions for vendor mappings
- **02-DEPARTMENTS**: Department allocations for invoice lines

## Implementation Priority

**MEDIUM** - Core functionality, but detailed workflows deferred

## Functions

### Current Implementation (Phase 1-4)

1. ✅ **Vendor Master** - Vendor DocType, CRUD operations
2. ✅ **Vendor Contacts** - Contact management (sales, accounting, leadership)
3. ✅ **Vendor Pricing** - Contract prices, pricing rules
4. ✅ **Vendor Ordering Rules** - Minimums, cutoffs, schedules, vacation settings
5. ✅ **Vendor Mapping** - Vendor-to-product mapping, SKU mapping
6. ✅ **Purchase Orders** - PO DocType (basic structure)
7. ✅ **Receiving** - Receiving workflow (basic structure)
8. ✅ **Invoice Structure** - Invoice DocType, line items
9. ✅ **Invoice Line Allocation** - Department allocation, line splitting
10. ✅ **Ottimate Integration** - Flatfile import, item mapping

### Phase 6 Deferred (12+ months)

11. ⏳ **Detailed Ordering Workflows** - Quick orders, recurring orders, approval workflows
12. ⏳ **Detailed Receiving** - Partial receiving, inspection, quality control
13. ⏳ **Invoice Processing** - OCR, AI processing, matching, reconciliation

## Status

⏳ **To be extracted from FRAPPE_IMPLEMENTATION_PLAN.md**

---

**Next Steps**: Extract Vendor Master and Ottimate Integration first, as they're needed for current operations.

