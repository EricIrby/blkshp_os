# BLK-15 Implementation Plan: ERPNext v15 Alignment

**Issue:** [BLK-15](https://linear.app/blkshp/issue/BLK-15)
**Status:** READY FOR IMPLEMENTATION
**Total Effort:** 4 weeks (3 phases)
**Dependencies:** None (can start immediately)

---

## Overview

Based on the comprehensive alignment analysis in `docs/ERPNEXT-V15-ALIGNMENT-ANALYSIS.md`, this implementation plan breaks down the hybrid approach into actionable tasks.

**Strategy:** Maintain BLKSHP's hospitality-specific design while adding strategic ERPNext compatibility layers.

---

## Phase 1: Stock Ledger & Valuation (2 weeks)

### Goal
Implement transaction-based inventory tracking and cost valuation

### Sub-Issues to Create

#### BLK-41: Create Stock Ledger Entry DocType (3 days)

**Description:**
Implement transaction-level inventory audit trail following ERPNext patterns.

**Tasks:**
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

**Acceptance Criteria:**
- Stock Ledger Entry DocType exists and is submittable
- Running balance calculates correctly
- Entries are immutable after submit
- Tests pass with >90% coverage

**Estimated Effort:** 3 days

---

#### BLK-42: Integrate Stock Ledger with Inventory Audit (2 days)

**Description:**
Generate Stock Ledger Entries when Inventory Audits are completed.

**Tasks:**
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

**Acceptance Criteria:**
- Audit completion generates correct ledger entries
- Inventory Balance matches Stock Ledger running balance
- Tests cover all audit scenarios

**Estimated Effort:** 2 days

---

#### BLK-43: Add Valuation Fields to Product DocType (1 day)

**Description:**
Add cost tracking and valuation method fields to Product.

**Tasks:**
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

**Acceptance Criteria:**
- Valuation fields exist on Product
- Migration script runs successfully
- Existing products updated without errors

**Estimated Effort:** 1 day

---

#### BLK-44: Implement Moving Average Costing (3 days)

**Description:**
Calculate product cost using moving average method from stock transactions.

**Tasks:**
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

**Acceptance Criteria:**
- Moving average calculates correctly
- Product valuation_rate updates on transactions
- COGS calculation accurate
- Tests achieve >95% coverage

**Estimated Effort:** 3 days

---

#### BLK-45: Create Stock Ledger Reports (1 day)

**Description:**
Build reports and queries for Stock Ledger data.

**Tasks:**
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

**Acceptance Criteria:**
- Stock Ledger report displays correctly
- COGS report calculates accurately
- Queries perform well (<100ms for typical use)

**Estimated Effort:** 1 day

---

## Phase 2: Batch Tracking & Expiration (1 week)

### Goal
Enable batch number tracking and expiration date management for food safety.

### Sub-Issues to Create

#### BLK-46: Create Batch Number DocType (2 days)

**Description:**
Implement batch tracking for perishable items.

**Tasks:**
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

**Acceptance Criteria:**
- Batch Number DocType created
- Auto-naming works correctly
- Expiration status updates automatically
- Tests pass

**Estimated Effort:** 2 days

---

#### BLK-47: Add Batch Support to Stock Ledger (2 days)

**Description:**
Link Stock Ledger Entries to Batch Numbers.

**Tasks:**
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

**Acceptance Criteria:**
- Stock Ledger supports batch tracking
- Batch quantities calculate correctly
- Expiration queries work

**Estimated Effort:** 2 days

---

#### BLK-48: Integrate Batches with Inventory Audit (2 days)

**Description:**
Enable batch selection during inventory audits.

**Tasks:**
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

**Acceptance Criteria:**
- Audit supports batch entry
- Expiration warnings display correctly
- Stock Ledger Entries link to batches

**Estimated Effort:** 2 days

---

#### BLK-49: Add has_batch_no Flag to Product (1 day)

**Description:**
Enable per-product batch tracking control.

**Tasks:**
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

**Acceptance Criteria:**
- has_batch_no flag exists
- Validation works correctly
- Migration script runs successfully

**Estimated Effort:** 1 day

---

## Phase 3: ERPNext Compatibility Layer (1 week)

### Goal
Enable ERPNext Item data import and field mapping for integration scenarios.

### Sub-Issues to Create

#### BLK-50: Add ERPNext-Compatible Fields to Product (1 day)

**Description:**
Add optional ERPNext Item field mappings to Product.

**Tasks:**
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

**Acceptance Criteria:**
- ERPNext fields exist and auto-sync
- Fields are read-only
- No impact on existing workflows

**Estimated Effort:** 1 day

---

#### BLK-51: Create ERPNext Item Import Utility (3 days)

**Description:**
Build utility to import ERPNext Item data as BLKSHP Products.

**Tasks:**
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

**Acceptance Criteria:**
- Utility imports ERPNext Items successfully
- Field mapping works correctly
- Import errors are logged and reported
- Tests cover all scenarios

**Estimated Effort:** 3 days

---

#### BLK-52: Create ERPNext Alignment Documentation (2 days)

**Description:**
Document field mappings, migration paths, and integration patterns.

**Tasks:**
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

**Deliverables:**
- `docs/ERPNEXT-FIELD-MAPPING.md`
- `docs/ERPNEXT-MIGRATION-GUIDE.md`
- `docs/ERPNEXT-INTEGRATION-EXAMPLES.md`

**Acceptance Criteria:**
- All mapping tables complete
- Migration guide validated by test import
- Examples tested and working

**Estimated Effort:** 2 days

---

#### BLK-53: Optional - Create UOM DocType (Deferred)

**Description:**
Replace Select field with UOM DocType for extensibility.

**Status:** DEFERRED to Phase 4+ (not critical for BLK-15)

**Rationale:**
- Current Select-based units work well for hospitality
- UOM DocType adds complexity without immediate value
- Can be added later if needed for ERPNext integration

**If Implemented Later:**
- Create UOM DocType (Name, Symbol, Type)
- Create UOM Conversion Factor child table on Product
- Migrate primary_count_unit Select → Link to UOM
- Update all unit references
- Estimated: 3-4 days

---

## Testing Strategy

### Unit Tests
- All new DocTypes: controller validation, calculations
- Costing logic: moving average, COGS
- Batch tracking: quantity calculation, expiration
- Import utility: field mapping, error handling

**Coverage Target:** >90% for all new code

### Integration Tests
- Inventory Audit → Stock Ledger Entry generation
- Stock Ledger Entry → Inventory Balance updates
- Batch tracking through full audit workflow
- ERPNext Item import end-to-end

**Coverage Target:** All major workflows tested

### Performance Tests
- Stock Ledger queries with 10k+ entries
- Running balance calculation performance
- Batch quantity aggregation performance
- Import of 1000+ items

**Performance Targets:**
- Stock balance query: <100ms
- COGS calculation (1 year): <500ms
- Item import (1000 items): <60 seconds

### Manual Testing
- Inventory Audit with batch tracking
- COGS report accuracy
- ERPNext Item import UI flow
- Expiration alerts and warnings

---

## Deployment Plan

### Phase 1 Deployment (Week 2)
- Deploy to staging environment
- Run migration scripts
- Validate Stock Ledger generation from audits
- Test COGS calculations with real data

### Phase 2 Deployment (Week 3)
- Deploy Batch Number support
- Migrate test products to use batches
- Validate expiration tracking
- Test batch selection in audits

### Phase 3 Deployment (Week 4)
- Deploy ERPNext compatibility layer
- Test Item import with sample data
- Validate field mappings
- Release documentation

### Production Rollout
- Week 5: Production deployment
- Monitor Stock Ledger generation
- Track performance metrics
- Gather user feedback

---

## Rollback Plan

**If Issues Found:**
1. Stock Ledger Entry is additive - can be disabled
2. Batch tracking is optional (has_batch_no flag)
3. ERPNext fields are optional and hidden
4. No data loss - all features are additive

**Rollback Steps:**
1. Disable Stock Ledger generation in Inventory Audit
2. Set has_batch_no = 0 for all products
3. Hide ERPNext compatibility section
4. Existing Inventory Balance continues to work

**Risk Level:** LOW - all changes are non-breaking

---

## Success Metrics

### Phase 1 Metrics
- [ ] 100% of Inventory Audits generate Stock Ledger Entries
- [ ] Inventory Balance matches Stock Ledger within 0.01%
- [ ] COGS calculation matches manual calculation
- [ ] Stock Ledger queries perform <100ms

### Phase 2 Metrics
- [ ] Batch tracking enabled for 80%+ of Food/Beverage products
- [ ] Expiration alerts prevent counting expired items
- [ ] Batch quantity calculations accurate within 0.01%

### Phase 3 Metrics
- [ ] Successfully import 100+ ERPNext Items
- [ ] Field mapping accuracy >95%
- [ ] Documentation validated by external user

### Overall Success
- [ ] All phases deployed to production
- [ ] No breaking changes to existing features
- [ ] User adoption >80% within 30 days
- [ ] Zero critical bugs in production

---

## Timeline Summary

| Week | Phase | Issues | Effort |
|------|-------|--------|--------|
| 1 | Phase 1.1 | BLK-41, BLK-42, BLK-43 | Stock Ledger + Audit Integration |
| 2 | Phase 1.2 | BLK-44, BLK-45 | Costing + Reports |
| 3 | Phase 2 | BLK-46, BLK-47, BLK-48, BLK-49 | Batch Tracking |
| 4 | Phase 3 | BLK-50, BLK-51, BLK-52 | ERPNext Compatibility |

**Total Duration:** 4 weeks
**Total Issues:** 12 (BLK-41 through BLK-52)
**Risk:** Medium (moderate complexity, clear scope)

---

## Dependencies

**Required Before Starting:**
- ✅ BLK-36 (Code cleanup) - DONE
- ✅ BLK-14 (Operations audit) - DONE
- ⚠️ BLK-40 (Transfers/Depletions) - Can proceed in parallel

**Blockers:**
- None identified

**Nice to Have:**
- BLK-38 (Inventory Audit test coverage) - improves confidence
- BLK-39 (Recipe allergen tests) - unrelated but valuable

---

## Open Questions

1. **UOM Migration Timeline**
   - Q: When should we migrate to UOM DocType?
   - A: Deferred to Phase 4+, evaluate based on ERPNext integration needs

2. **Serial Number Support**
   - Q: Do we need serial number tracking?
   - A: Not for current hospitality use cases, defer indefinitely

3. **FIFO vs Moving Average**
   - Q: Should we support FIFO costing?
   - A: Start with Moving Average, add FIFO in Phase 4+ if requested

4. **Backwards Compatibility**
   - Q: How to handle existing Inventory Balances?
   - A: No migration needed - Stock Ledger starts fresh, balances continue

---

**Plan Author:** Claude Code (AI Assistant)
**Status:** ✅ READY FOR REVIEW AND ISSUE CREATION
**Next Step:** Create Linear issues BLK-41 through BLK-52
