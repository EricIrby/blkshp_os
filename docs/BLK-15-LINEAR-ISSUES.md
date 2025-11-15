# BLK-15 Linear Issues - Creation Guide

**Parent Issue:** [BLK-15](https://linear.app/blkshp/issue/BLK-15)
**Total Issues:** 12 (BLK-41 through BLK-52)
**Total Effort:** 4 weeks

---

## Issue BLK-41: Create Stock Ledger Entry DocType

**Title:** Create Stock Ledger Entry DocType

**Description:**
```
Implement transaction-level inventory audit trail following ERPNext patterns.

## Goal
Create a new DocType to record every inventory movement as an immutable transaction, enabling complete audit trail and running balance calculations.

## Tasks
- [ ] Create Stock Ledger Entry DocType JSON
  - Fields: item_code, product, warehouse, department, company
  - Fields: actual_qty, qty_after_transaction, posting_date, posting_time
  - Fields: voucher_type, voucher_no, voucher_detail_no
  - Set document_type = "Transaction", is_submittable = 1
- [ ] Create Stock Ledger Entry Python controller
  - Validation: prevent editing after submit
  - Auto-set: posting_datetime from date + time
  - Index: (product, department, posting_datetime)
- [ ] Implement running balance calculation
  - Server-side method to calculate qty_after_transaction
  - Get previous balance from last ledger entry
  - Add actual_qty to get new balance
- [ ] Add permission checks
  - Only System Manager can create directly
  - Typically created by other DocTypes (Inventory Audit, etc.)
- [ ] Write unit tests
  - Test running balance calculation
  - Test immutability after submit
  - Test query performance

## Acceptance Criteria
- ✅ Stock Ledger Entry DocType exists and is submittable
- ✅ Running balance calculates correctly
- ✅ Entries are immutable after submit
- ✅ Tests pass with >90% coverage

## Technical Notes
- Pattern follows ERPNext Stock Ledger Entry design
- Immutable ledger model ensures audit integrity
- Running balance cached for performance

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
- ERPNext Pattern: https://github.com/frappe/erpnext/blob/version-15/erpnext/stock/doctype/stock_ledger_entry/stock_ledger_entry.json
```

**Labels:** Phase 1, Backend, DocType
**Estimate:** 3 days
**Priority:** High
**Parent:** BLK-15

---

## Issue BLK-42: Integrate Stock Ledger with Inventory Audit

**Title:** Integrate Stock Ledger with Inventory Audit

**Description:**
```
Generate Stock Ledger Entries when Inventory Audits are completed.

## Goal
Automatically create Stock Ledger Entry transactions when an Inventory Audit is finalized, ensuring all inventory adjustments are recorded in the ledger.

## Tasks
- [ ] Update Inventory Audit controller
  - Add `generate_stock_ledger_entries()` method
  - Call on audit completion (after variance calculation)
  - Create one entry per audit line with variance
- [ ] Implement entry generation logic
  - For each audit line with variance:
    - actual_qty = variance (audit qty - system qty)
    - posting_date = audit completion date
    - voucher_type = "Inventory Audit"
    - voucher_no = audit.name
    - product, department from audit line
- [ ] Add validation
  - Prevent audit completion if ledger generation fails
  - Show error messages for invalid states
- [ ] Update Inventory Balance from ledger
  - Recalculate from Stock Ledger Entries
  - Ensure consistency between balance and ledger
- [ ] Write integration tests
  - Test ledger entry generation on audit completion
  - Test balance updates match ledger
  - Test audit with no variances (no entries created)

## Acceptance Criteria
- ✅ Audit completion generates correct ledger entries
- ✅ Inventory Balance matches Stock Ledger running balance
- ✅ Tests cover all audit scenarios

## Technical Notes
- Only create entries for lines with variances (audit qty ≠ system qty)
- Maintain transactional integrity - rollback on error
- Existing Inventory Balance continues to work unchanged

## Dependencies
- Requires: BLK-41 (Stock Ledger Entry DocType)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
```

**Labels:** Phase 1, Backend, Integration
**Estimate:** 2 days
**Priority:** High
**Parent:** BLK-15
**Blockers:** BLK-41

---

## Issue BLK-43: Add Valuation Fields to Product DocType

**Title:** Add Valuation Fields to Product DocType

**Description:**
```
Add cost tracking and valuation method fields to Product.

## Goal
Enable cost tracking at the product level to support COGS calculation and inventory valuation.

## Tasks
- [ ] Update Product DocType JSON
  - Add section_break: "Valuation"
  - Add valuation_rate (Currency, precision=2)
  - Add valuation_method (Select: "Moving Average", "FIFO", "Manual")
  - Add default_incoming_rate (Currency, for purchases)
- [ ] Update Product controller
  - Add validation for valuation fields
  - Set default valuation_method = "Moving Average"
- [ ] Add migration script
  - Set default valuation_method for existing products
  - Initialize valuation_rate = 0.00
- [ ] Update Product form UI
  - Show valuation section
  - Add help text for valuation_method
- [ ] Write tests
  - Test default values
  - Test validation

## Acceptance Criteria
- ✅ Valuation fields exist on Product
- ✅ Migration script runs successfully
- ✅ Existing products updated without errors

## Technical Notes
- Fields are optional to maintain backwards compatibility
- Moving Average is default as it's simplest and most common
- valuation_rate will be auto-updated by Stock Ledger transactions

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
- ERPNext Item valuation: https://github.com/frappe/erpnext/blob/version-15/erpnext/stock/doctype/item/item.json
```

**Labels:** Phase 1, Backend, DocType, Migration
**Estimate:** 1 day
**Priority:** High
**Parent:** BLK-15

---

## Issue BLK-44: Implement Moving Average Costing

**Title:** Implement Moving Average Costing

**Description:**
```
Calculate product cost using moving average method from stock transactions.

## Goal
Automatically calculate and maintain accurate product costs using the moving average method, enabling accurate COGS reporting and inventory valuation.

## Tasks
- [ ] Create costing service module
  - `blkshp_os/inventory/costing.py`
  - `calculate_moving_average(product, department, incoming_qty, incoming_rate)`
  - `get_current_stock_value(product, department)`
- [ ] Implement Moving Average algorithm
  ```python
  new_rate = (current_value + incoming_value) / (current_qty + incoming_qty)
  ```
  - Get current qty and rate from Inventory Balance
  - Calculate new weighted average rate
  - Update Product.valuation_rate
- [ ] Add cost fields to Stock Ledger Entry
  - incoming_rate (Currency) - cost per unit for receipts
  - outgoing_rate (Currency) - cost per unit for issues
  - valuation_rate (Currency) - weighted average after transaction
  - stock_value (Currency) - total value (qty × rate)
  - stock_value_difference (Currency) - change in total value
- [ ] Integrate with Stock Ledger Entry creation
  - Calculate rates when entry is submitted
  - Update Product.valuation_rate
  - Store values in ledger entry
- [ ] Create COGS calculation utility
  - `calculate_cogs(department, from_date, to_date)`
  - Sum stock_value_difference for outgoing entries
  - Filter by department and date range
- [ ] Write comprehensive tests
  - Test moving average calculation
  - Test with multiple transactions
  - Test COGS calculation
  - Test edge cases (zero quantity, negative variance)

## Acceptance Criteria
- ✅ Moving average calculates correctly
- ✅ Product valuation_rate updates on transactions
- ✅ COGS calculation accurate
- ✅ Tests achieve >95% coverage

## Technical Notes
- Moving average formula: (old_value + new_value) / (old_qty + new_qty)
- Only incoming transactions update valuation_rate
- Outgoing transactions use current valuation_rate
- Handle edge cases: division by zero, negative stock

## Dependencies
- Requires: BLK-41 (Stock Ledger Entry DocType)
- Requires: BLK-43 (Valuation fields on Product)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
- ERPNext Costing: https://docs.erpnext.com/docs/user/manual/en/stock/articles/item-valuation-fifo-and-moving-average
```

**Labels:** Phase 1, Backend, Costing, Critical
**Estimate:** 3 days
**Priority:** High
**Parent:** BLK-15
**Blockers:** BLK-41, BLK-43

---

## Issue BLK-45: Create Stock Ledger Reports

**Title:** Create Stock Ledger Reports

**Description:**
```
Build reports and queries for Stock Ledger data.

## Goal
Provide visibility into inventory transactions, stock balances, and COGS through reports and dashboards.

## Tasks
- [ ] Create Stock Ledger report
  - List view with filters: product, department, date range
  - Show: posting_date, product, qty, rate, value, balance
  - Export to Excel
- [ ] Create COGS report
  - Group by: department, product category
  - Time period selection
  - Comparison to previous period
- [ ] Add Stock Ledger queries
  - `get_stock_balance(product, department, as_of_date)`
  - `get_stock_value(product, department, as_of_date)`
  - `get_stock_movements(product, department, from_date, to_date)`
- [ ] Create dashboard widget
  - Show total stock value by department
  - Show recent movements
- [ ] Write query tests
  - Test balance queries
  - Test date filtering
  - Test performance with 10k+ entries

## Acceptance Criteria
- ✅ Stock Ledger report displays correctly
- ✅ COGS report calculates accurately
- ✅ Queries perform well (<100ms for typical use)

## Technical Notes
- Use indexed queries for performance
- Cache dashboard widgets (5 minute TTL)
- Support Excel export for all reports

## Dependencies
- Requires: BLK-41 (Stock Ledger Entry DocType)
- Requires: BLK-44 (Costing implementation)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
```

**Labels:** Phase 1, Frontend, Reports
**Estimate:** 1 day
**Priority:** Medium
**Parent:** BLK-15
**Blockers:** BLK-41, BLK-44

---

## Issue BLK-46: Create Batch Number DocType

**Title:** Create Batch Number DocType

**Description:**
```
Implement batch tracking for perishable items.

## Goal
Enable batch/lot number tracking with expiration dates for food safety and traceability.

## Tasks
- [ ] Create Batch Number DocType JSON
  - batch_id (Data, unique, required)
  - product (Link to Product, required)
  - department (Link to Department, required)
  - manufacturing_date (Date, optional)
  - expiration_date (Date, optional)
  - quantity (Float, read-only) - calculated from ledger
  - status (Select: Active, Expired, Consumed)
- [ ] Create Batch Number controller
  - Auto-generate batch_id if not provided
  - Validation: expiration_date > manufacturing_date
  - Auto-update status based on expiration_date
  - Calculate quantity from Stock Ledger Entries
- [ ] Add batch naming series
  - Format: {product_code}-{YYYY}-{####}
  - Example: "TOMATO-2025-0001"
- [ ] Add permissions
  - Department-restricted
  - Read-only quantity field
- [ ] Write unit tests
  - Test batch creation
  - Test expiration status
  - Test quantity calculation

## Acceptance Criteria
- ✅ Batch Number DocType created
- ✅ Auto-naming works correctly
- ✅ Expiration status updates automatically
- ✅ Tests pass

## Technical Notes
- Batch numbers are immutable once created
- Quantity is calculated from Stock Ledger Entries (read-only)
- Status auto-updates daily via scheduled job
- Critical for food safety compliance and recalls

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
- ERPNext Batch: https://docs.erpnext.com/docs/user/manual/en/stock/batch
```

**Labels:** Phase 2, Backend, DocType, Food Safety
**Estimate:** 2 days
**Priority:** High
**Parent:** BLK-15

---

## Issue BLK-47: Add Batch Support to Stock Ledger

**Title:** Add Batch Support to Stock Ledger

**Description:**
```
Link Stock Ledger Entries to Batch Numbers.

## Goal
Track inventory movements at the batch level to maintain accurate batch quantities and enable batch-level reporting.

## Tasks
- [ ] Update Stock Ledger Entry
  - Add batch_number (Link to Batch Number, optional)
  - Add validation: require batch if product.has_batch_no = 1
- [ ] Update batch quantity calculation
  - Sum actual_qty from Stock Ledger Entries
  - Group by (product, department, batch_number)
  - Update Batch Number.quantity field
- [ ] Add batch filtering to queries
  - `get_stock_balance_by_batch(product, department)`
  - `get_expiring_batches(department, within_days=30)`
- [ ] Create batch ledger report
  - Show movements per batch
  - Highlight expiring batches
- [ ] Write integration tests
  - Test batch quantity calculation
  - Test batch filtering
  - Test expiration queries

## Acceptance Criteria
- ✅ Stock Ledger supports batch tracking
- ✅ Batch quantities calculate correctly
- ✅ Expiration queries work

## Technical Notes
- Batch tracking is optional per product (has_batch_no flag)
- Multiple batches can exist for same product/department
- FIFO logic: consume oldest batches first (by manufacturing_date)

## Dependencies
- Requires: BLK-41 (Stock Ledger Entry DocType)
- Requires: BLK-46 (Batch Number DocType)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
```

**Labels:** Phase 2, Backend, Integration
**Estimate:** 2 days
**Priority:** High
**Parent:** BLK-15
**Blockers:** BLK-41, BLK-46

---

## Issue BLK-48: Integrate Batches with Inventory Audit

**Title:** Integrate Batches with Inventory Audit

**Description:**
```
Enable batch selection during inventory audits.

## Goal
Allow users to count inventory by batch number and receive expiration warnings during audits.

## Tasks
- [ ] Update Inventory Audit Line
  - Add batch_number (Link to Batch Number, optional)
  - Show expiration_date from batch (read-only)
  - Add expiration warning indicator
- [ ] Update Inventory Audit UI
  - Show batch dropdown for products with has_batch_no = 1
  - Display expiration date and status
  - Highlight expired batches in red
- [ ] Update ledger entry generation
  - Pass batch_number to Stock Ledger Entry
  - Create separate entries per batch
- [ ] Add expiration alerts
  - Show warning if counting expired batch
  - Option to exclude expired batches from audit
- [ ] Write integration tests
  - Test batch selection in audit
  - Test ledger generation with batches
  - Test expiration warnings

## Acceptance Criteria
- ✅ Audit supports batch entry
- ✅ Expiration warnings display correctly
- ✅ Stock Ledger Entries link to batches

## Technical Notes
- Batch selection required if product.has_batch_no = 1
- Expired batch warning is non-blocking (can still count)
- Generate separate ledger entry per batch

## Dependencies
- Requires: BLK-42 (Stock Ledger integration with Audit)
- Requires: BLK-46 (Batch Number DocType)
- Requires: BLK-47 (Batch support in Stock Ledger)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
```

**Labels:** Phase 2, Backend, Frontend, Integration
**Estimate:** 2 days
**Priority:** High
**Parent:** BLK-15
**Blockers:** BLK-42, BLK-46, BLK-47

---

## Issue BLK-49: Add has_batch_no Flag to Product

**Title:** Add has_batch_no Flag to Product

**Description:**
```
Enable per-product batch tracking control.

## Goal
Allow enabling/disabling batch tracking per product, with automatic settings for food items.

## Tasks
- [ ] Update Product DocType
  - Add has_batch_no (Check, default=0) in Valuation section
  - Add batch_naming_series (Data, optional)
  - Add shelf_life_in_days (Int, optional)
- [ ] Add validation
  - If has_batch_no = 1, shelf_life_in_days should be set
  - Show warning if no shelf_life for perishable items
- [ ] Create migration script
  - Auto-set has_batch_no = 1 for Food/Beverage products
  - Set default shelf_life based on product_type
- [ ] Update form UI
  - Show batch fields when has_batch_no = 1
  - Help text explaining batch tracking
- [ ] Write tests
  - Test validation
  - Test migration

## Acceptance Criteria
- ✅ has_batch_no flag exists
- ✅ Validation works correctly
- ✅ Migration script runs successfully

## Technical Notes
- Batch tracking is optional and per-product
- Recommended for all Food/Beverage items
- shelf_life_in_days used for expiration calculation

## Suggested Defaults:
- Food: has_batch_no = 1, shelf_life_in_days = 30
- Beverage: has_batch_no = 1, shelf_life_in_days = 365
- Supply/Equipment: has_batch_no = 0

## Dependencies
- Requires: BLK-46 (Batch Number DocType)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
```

**Labels:** Phase 2, Backend, DocType, Migration
**Estimate:** 1 day
**Priority:** Medium
**Parent:** BLK-15
**Blockers:** BLK-46

---

## Issue BLK-50: Add ERPNext-Compatible Fields to Product

**Title:** Add ERPNext-Compatible Fields to Product

**Description:**
```
Add optional ERPNext Item field mappings to Product.

## Goal
Enable ERPNext compatibility by adding optional Item-compatible fields that auto-sync from Product fields.

## Tasks
- [ ] Update Product DocType
  - Add section_break: "ERPNext Compatibility" (collapsed by default)
  - Add item_code (Data, read-only) - maps to product_code
  - Add item_name (Data, read-only) - maps to product_name
  - Add stock_uom (Link to UOM, optional)
  - Add item_group (Link to Item Group, optional)
- [ ] Add auto-sync logic
  - On Product save, set item_code = product_code
  - On Product save, set item_name = product_name
  - Fields are read-only, updated automatically
- [ ] Update form UI
  - Collapse ERPNext section by default
  - Add help text: "For ERPNext integration only"
- [ ] Write tests
  - Test auto-sync
  - Test read-only enforcement

## Acceptance Criteria
- ✅ ERPNext fields exist and auto-sync
- ✅ Fields are read-only
- ✅ No impact on existing workflows

## Technical Notes
- These fields are purely for compatibility
- Hidden by default, no impact on BLKSHP workflows
- Enables ERPNext modules to reference BLKSHP Products as Items

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
- Analysis: `docs/ERPNEXT-V15-ALIGNMENT-ANALYSIS.md`
```

**Labels:** Phase 3, Backend, DocType, Integration
**Estimate:** 1 day
**Priority:** Low
**Parent:** BLK-15

---

## Issue BLK-51: Create ERPNext Item Import Utility

**Title:** Create ERPNext Item Import Utility

**Description:**
```
Build utility to import ERPNext Item data as BLKSHP Products.

## Goal
Enable migration from ERPNext by providing a tool to import Item data as Products with proper field mapping.

## Tasks
- [ ] Create import utility module
  - `blkshp_os/integrations/erpnext_import.py`
  - `import_items_from_erpnext(item_list, company, department)`
- [ ] Implement field mapping
  ```python
  Product.product_code = Item.item_code
  Product.product_name = Item.item_name
  Product.company = {specified company}
  Product.primary_count_unit = map_uom(Item.stock_uom)
  Product.category = map_item_group(Item.item_group)
  Product.valuation_rate = Item.valuation_rate
  Product.has_batch_no = Item.has_batch_no
  ```
- [ ] Create UOM mapping table
  - Map ERPNext UOMs to BLKSHP count units
  - Configurable via DocType or JSON config
- [ ] Add import validation
  - Check for duplicate product_codes
  - Validate required fields
  - Report errors without halting
- [ ] Create import log
  - Track success/failure per item
  - Show field mapping results
  - Export to CSV
- [ ] Build simple UI
  - Upload CSV or select from ERPNext database
  - Preview mappings before import
  - Show import progress
- [ ] Write comprehensive tests
  - Test successful import
  - Test duplicate handling
  - Test UOM mapping
  - Test error handling

## Acceptance Criteria
- ✅ Utility imports ERPNext Items successfully
- ✅ Field mapping works correctly
- ✅ Import errors are logged and reported
- ✅ Tests cover all scenarios

## Technical Notes
- One-way import (ERPNext → BLKSHP)
- Best-effort UOM mapping (may require manual review)
- Skip items that can't be mapped

## Supported Mappings:
- Item → Product (1:1)
- Item Group → Product Category
- UOM → primary_count_unit
- Valuation Rate → valuation_rate
- Batch tracking flag → has_batch_no

## Dependencies
- Requires: BLK-50 (ERPNext-compatible fields)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
```

**Labels:** Phase 3, Backend, Integration, Migration
**Estimate:** 3 days
**Priority:** Medium
**Parent:** BLK-15
**Blockers:** BLK-50

---

## Issue BLK-52: Create ERPNext Alignment Documentation

**Title:** Create ERPNext Alignment Documentation

**Description:**
```
Document field mappings, migration paths, and integration patterns.

## Goal
Provide comprehensive documentation for ERPNext users migrating to or integrating with BLKSHP OS.

## Tasks
- [ ] Create field mapping reference
  - Table: ERPNext Item ↔ BLKSHP Product
  - Table: ERPNext Stock Ledger Entry ↔ BLKSHP Stock Ledger Entry
  - Table: ERPNext Warehouse ↔ BLKSHP Department
- [ ] Write migration guide
  - Step-by-step ERPNext → BLKSHP migration
  - Data export from ERPNext
  - Import into BLKSHP
  - Validation checklist
- [ ] Document API compatibility
  - Which ERPNext APIs are compatible
  - Which require adaptation
  - Custom API mappings
- [ ] Create integration examples
  - Example: Sync items from ERPNext daily
  - Example: Send stock movements to ERPNext
  - Example: Use BLKSHP as inventory module for ERPNext
- [ ] Add to main documentation
  - Link from README
  - Add to docs site
  - Include in user manual

## Deliverables
- `docs/ERPNEXT-FIELD-MAPPING.md`
- `docs/ERPNEXT-MIGRATION-GUIDE.md`
- `docs/ERPNEXT-INTEGRATION-EXAMPLES.md`

## Acceptance Criteria
- ✅ All mapping tables complete
- ✅ Migration guide validated by test import
- ✅ Examples tested and working

## Technical Notes
- Include both conceptual differences and practical mappings
- Highlight BLKSHP advantages (multi-department, hospitality features)
- Provide troubleshooting section

## Key Differences to Document:
1. Product vs Item naming
2. Department vs Warehouse model
3. Stock Ledger Entry compatibility
4. Batch tracking differences
5. Valuation method implementation

## Dependencies
- Requires: BLK-51 (Import utility for validation)

## References
- Implementation Plan: `docs/BLK-15-IMPLEMENTATION-PLAN.md`
- Analysis: `docs/ERPNEXT-V15-ALIGNMENT-ANALYSIS.md`
```

**Labels:** Phase 3, Documentation
**Estimate:** 2 days
**Priority:** Low
**Parent:** BLK-15
**Blockers:** BLK-51

---

## Summary Statistics

**Total Issues:** 12
**Total Effort:** ~20 days (4 weeks)

**By Phase:**
- Phase 1 (Stock Ledger & Valuation): 5 issues, 10 days
- Phase 2 (Batch Tracking): 4 issues, 7 days
- Phase 3 (ERPNext Compatibility): 3 issues, 6 days

**By Priority:**
- High: 9 issues
- Medium: 2 issues
- Low: 2 issues

**By Type:**
- Backend: 9 issues
- Frontend: 2 issues
- Documentation: 1 issue

---

## Creation Instructions

To create these issues in Linear:

1. Go to https://linear.app/blkshp
2. For each issue above:
   - Click "+ New Issue"
   - Copy the **Title**
   - Copy the **Description** (markdown formatted)
   - Set **Labels** as specified
   - Set **Estimate** (use story points or days)
   - Set **Priority**
   - Link to parent issue: BLK-15
   - Add **Blockers** if specified
3. Create in order (BLK-41 first, then BLK-42, etc.)

---

**Document Author:** Claude Code (AI Assistant)
**Status:** Ready for Linear issue creation
**Reference:** `docs/BLK-15-IMPLEMENTATION-PLAN.md`
