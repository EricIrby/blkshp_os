# ERPNext v15 Alignment Analysis - Product & Inventory DocTypes

**Date:** 2025-11-14
**Issue:** [BLK-15](https://linear.app/blkshp/issue/BLK-15)
**Status:** ANALYSIS COMPLETE

---

## Executive Summary

Analyzed BLKSHP OS Product and Inventory DocTypes against ERPNext v15 standards to identify alignment opportunities. Our current implementation is **highly specialized for hospitality operations** and differs significantly from ERPNext's generic retail/manufacturing model.

**Key Finding:** Full alignment would require major breaking changes. **Recommended approach:** Maintain hospitality-specific design while adding strategic ERPNext compatibility layers.

---

## Part 1: Product vs Item DocType Comparison

### ERPNext v15 Item DocType

**Core Purpose:** Generic item master for retail, manufacturing, and services
**Key Features:**
- Stock management (stock_uom, is_stock_item)
- Batch and serial number tracking
- Valuation methods (FIFO, Moving Average, LIFO)
- Manufacturing integration (BOM support)
- Multi-UOM with conversion factors
- Shelf life and expiration tracking
- Safety stock and min order quantities

**Field Structure:**
```
item_code (Data, unique)
item_name (Data)
item_group (Link to Item Group)
stock_uom (Link to UOM)
is_stock_item (Check)
has_batch_no (Check)
has_serial_no (Check)
valuation_rate (Currency)
valuation_method (Select: FIFO/Moving Average/LIFO)
opening_stock (Float)
shelf_life_in_days (Int)
min_order_qty (Float)
safety_stock (Float)
```

### BLKSHP Product DocType

**Core Purpose:** Hospitality product master with department-based inventory
**Key Features:**
- Multi-department allocation (department-specific inventory)
- Flexible unit conversions (volume, weight, count)
- Prep item tracking (recipe ingredients vs finished goods)
- Generic item support (category-level ordering)
- Purchase unit management (vendor-specific packaging)
- Storage location tracking (bin locations)

**Field Structure:**
```
product_code (Data, unique)
product_name (Data)
product_type (Select: Food/Beverage/Supply/Equipment/Other)
company (Link to Company)
primary_count_unit (Select)
volume_conversion_unit (Select)
volume_conversion_factor (Float)
weight_conversion_unit (Select)
weight_conversion_factor (Float)
is_generic (Check)
is_non_inventory (Check)
is_prep_item (Check)
preferred_vendor (Link)
departments (Table: Product Department)
purchase_units (Table: Product Purchase Unit)
storage_areas (Table: Product Storage Area)
```

### Comparison Analysis

| Feature | ERPNext Item | BLKSHP Product | Alignment |
|---------|--------------|----------------|-----------|
| **Unique Identifier** | item_code | product_code | ✅ Compatible |
| **Display Name** | item_name | product_name | ✅ Compatible |
| **Classification** | item_group (hierarchical) | category + subcategory + type | ⚠️ Different approach |
| **Stock Tracking** | is_stock_item | Implied (inverse of is_non_inventory) | ⚠️ Logic reversed |
| **Base UOM** | stock_uom (link) | primary_count_unit (select) | ❌ Incompatible |
| **Batch/Serial** | has_batch_no, has_serial_no | Not implemented | ❌ Missing |
| **Valuation** | valuation_rate, valuation_method | Not in Product (in Inventory Balance) | ❌ Different location |
| **Multi-Department** | Not supported | Core feature (departments table) | ✅ BLKSHP Advantage |
| **Purchase Units** | UOM Conversion table | purchase_units table | ⚠️ Similar concept, different structure |
| **Prep Items** | Manufacturing (BOM) | is_prep_item flag | ⚠️ Different approach |
| **Generic Items** | Variant system | is_generic flag | ⚠️ Different approach |

---

## Part 2: Inventory Balance vs Stock Ledger Entry

### ERPNext Stock Ledger Entry

**Core Purpose:** Transaction-level inventory audit trail
**Pattern:** Ledger model - every stock movement creates an entry

**Key Fields:**
```
item_code (Link)
warehouse (Link)
actual_qty (Float) - change in quantity
qty_after_transaction (Float) - running balance
posting_date (Date)
posting_time (Time)
voucher_type (Data) - originating document type
voucher_no (Data) - originating document number
incoming_rate (Currency)
outgoing_rate (Currency)
valuation_rate (Currency)
stock_value (Currency)
stock_value_difference (Currency)
serial_and_batch_bundle (Link)
```

**Pattern:**
- Immutable transaction log
- Running balance calculation
- FIFO/LIFO queue management
- Linked to source documents (Purchase Receipt, Delivery Note, etc.)

### BLKSHP Inventory Balance

**Core Purpose:** Current on-hand inventory by product/department
**Pattern:** Balance model - single record per product/department

**Key Fields:**
```
product (Link)
department (Link)
company (Link)
quantity (Float) - current on-hand
last_updated (Datetime)
last_audit_date (Date)
```

**Pattern:**
- Mutable current state
- Updated by Inventory Audit completion
- No transaction history
- No valuation tracking

### Critical Differences

| Aspect | ERPNext SLE | BLKSHP Inventory Balance | Impact |
|--------|-------------|--------------------------|--------|
| **Model** | Transaction ledger | Current balance | ❌ Fundamentally different |
| **History** | Complete audit trail | No history | ❌ Missing audit capability |
| **Valuation** | FIFO/LIFO queue | Not tracked | ❌ Missing cost tracking |
| **Updates** | Immutable append-only | Mutable updates | ❌ Different integrity model |
| **Source Links** | voucher_type, voucher_no | Not tracked | ❌ Missing provenance |
| **Multi-Location** | Warehouse field | Department field | ⚠️ Similar concept |

---

## Part 3: Gap Analysis

### Critical Gaps

#### 1. Missing Stock Ledger / Transaction History ❌

**Current State:**
- Inventory Balance only tracks current quantity
- No transaction history or audit trail
- Inventory Audit updates balances in-place

**ERPNext Standard:**
- Stock Ledger Entry records every movement
- Immutable transaction log
- Running balance calculated from transactions

**Impact:**
- Cannot reconstruct historical inventory levels
- Limited forensic audit capabilities
- No automatic COGS calculation from movements

**Required:**
- New DocType: Inventory Transaction or Stock Ledger Entry
- Migration strategy for historical data
- Update Inventory Audit to generate transactions

---

#### 2. Missing Valuation & Costing ❌

**Current State:**
- No valuation_rate on Product
- No cost tracking in Inventory Balance
- No FIFO/LIFO queue management

**ERPNext Standard:**
- Valuation method per item
- Cost tracking per transaction
- Stock value calculated automatically

**Impact:**
- Cannot calculate accurate COGS
- No automatic financial integration
- Manual cost tracking required

**Required:**
- Add valuation fields to Product or new DocType
- Implement FIFO/Moving Average calculation
- Integration with accounting (GL entries)

---

#### 3. Missing Batch & Serial Number Support ❌

**Current State:**
- No batch tracking
- No serial number support
- No expiration date management

**ERPNext Standard:**
- Batch Number DocType
- Serial Number DocType
- Serial and Batch Bundle for transactions

**Impact:**
- Cannot track lot numbers for recalls
- No expiration management (food safety issue)
- Limited traceability

**Required:**
- Batch Number DocType
- Expiration date tracking
- Integration with Inventory Audit

---

#### 4. Incompatible UOM System ⚠️

**Current State:**
- primary_count_unit is Select field (hardcoded options)
- Conversion factors stored on Product
- Limited to volume/weight conversions

**ERPNext Standard:**
- UOM DocType (extensible)
- UOM Conversion Factor DocType (item-specific)
- Multi-level UOM conversions

**Impact:**
- Cannot add custom units without code changes
- Less flexible than ERPNext standard
- Harder to integrate with ERPNext modules

**Required:**
- Migrate to UOM DocType pattern
- Create UOM Conversion Factor child table
- Update all unit references

---

### Strengths of Current Implementation ✅

#### 1. Multi-Department Inventory ✅

**BLKSHP Advantage:**
- Department-specific inventory tracking
- Department-level permissions
- Inter-department transfers (planned in BLK-40)

**ERPNext Limitation:**
- Only supports single warehouse per transaction
- No native department-based segmentation

**Decision:** **Keep BLKSHP design** - this is a core differentiator

---

#### 2. Hospitality-Specific Features ✅

**BLKSHP Advantages:**
- Prep item tracking (is_prep_item)
- Generic item support (is_generic)
- Product type classification (Food/Beverage/Supply)
- Purchase unit flexibility

**ERPNext:**
- Generic retail/manufacturing focus
- No hospitality-specific features

**Decision:** **Keep BLKSHP design** - these are essential for hospitality

---

#### 3. Flexible Unit Conversions ✅

**BLKSHP Approach:**
- Volume and weight conversions on Product
- Purchase units with vendor-specific packaging
- Count unit flexibility (each, case, lb, bottle, etc.)

**ERPNext:**
- More rigid UOM system
- Less intuitive for hospitality use cases

**Decision:** **Keep BLKSHP design** but consider UOM compatibility layer

---

## Part 4: Alignment Strategy

### Option 1: Full ERPNext Alignment (NOT RECOMMENDED)

**Changes Required:**
- Rename Product → Item
- Migrate to UOM DocType
- Implement Stock Ledger Entry
- Remove department-based inventory
- Remove hospitality-specific fields

**Pros:**
- ✅ Full ERPNext module compatibility
- ✅ Standard reporting and integrations

**Cons:**
- ❌ Breaks existing installations
- ❌ Loses hospitality-specific features
- ❌ Major migration effort (4-6 weeks)
- ❌ Worse UX for hospitality users

**Verdict:** ❌ **NOT RECOMMENDED** - loses core value proposition

---

### Option 2: Hybrid Approach - Compatibility Layer (RECOMMENDED)

**Strategy:** Keep BLKSHP design, add ERPNext-compatible fields and integrations

**Phase 1: Non-Breaking Enhancements**
1. Add optional ERPNext-compatible fields to Product:
   ```python
   item_code (Data, read-only) = product_code
   item_name (Data, read-only) = product_name
   stock_uom (Link to UOM, optional)
   valuation_rate (Currency, optional)
   has_batch_no (Check, default: 0)
   ```

2. Create Stock Ledger Entry DocType:
   - Parallel to Inventory Balance
   - Generated automatically from Inventory Audits
   - Links to Product (not ERPNext Item)

3. Add Batch Number DocType:
   - Links to Product
   - Expiration date support
   - Manufacturing date

**Phase 2: Integration Points**
4. Create ERPNext Item → BLKSHP Product sync utility:
   - Import ERPNext Items as Products
   - Map UOM → primary_count_unit
   - One-way or two-way sync option

5. Stock Entry integration:
   - Map Stock Entry to Inventory Audit
   - Generate Stock Ledger Entries
   - Support Material Transfer

**Pros:**
- ✅ Maintains BLKSHP advantages
- ✅ No breaking changes
- ✅ Adds ERPNext compatibility when needed
- ✅ Incremental implementation (2-3 weeks)

**Cons:**
- ⚠️ Dual model complexity
- ⚠️ Requires sync management
- ⚠️ Not "pure" ERPNext

**Verdict:** ✅ **RECOMMENDED** - best balance of compatibility and value

---

### Option 3: Minimal Alignment - Documentation Only

**Strategy:** Document differences, provide migration guides, no code changes

**Deliverables:**
- Mapping document: Product ↔ Item
- Migration guide for ERPNext users
- API compatibility notes

**Pros:**
- ✅ Zero code changes
- ✅ Fastest to implement (1-2 days)

**Cons:**
- ❌ No actual compatibility
- ❌ Manual migration required
- ❌ No ERPNext module integration

**Verdict:** ⚠️ **NOT SUFFICIENT** - doesn't solve the problem

---

## Part 5: Recommended Implementation Plan

### ✅ DECISION: Hybrid Approach (Option 2)

**Rationale:**
1. Preserves hospitality-specific advantages
2. Adds strategic ERPNext compatibility
3. Enables gradual migration path
4. Supports both BLKSHP-only and ERPNext-integrated deployments

---

### Phase 1: Foundation - Stock Ledger & Valuation (2 weeks)

#### Week 1: Stock Ledger Entry DocType
**Tasks:**
- [ ] Create Stock Ledger Entry DocType
  - Fields: item_code, warehouse/department, actual_qty, qty_after_transaction, posting_date, voucher_type, voucher_no
  - Link to Product (not ERPNext Item)
  - Immutable pattern (no edit after submit)
- [ ] Update Inventory Audit to generate Stock Ledger Entries
  - On audit completion, create entries for all variances
  - Link back to Inventory Audit (voucher_type = "Inventory Audit")
- [ ] Add running balance calculation
  - Server script to calculate qty_after_transaction
  - Validation to prevent negative stock (optional setting)

**Deliverables:**
- Stock Ledger Entry DocType
- Inventory Audit integration
- Unit tests for ledger logic

---

#### Week 2: Valuation & Costing
**Tasks:**
- [ ] Add valuation fields to Product
  - valuation_rate (Currency, optional)
  - valuation_method (Select: Moving Average, FIFO, Manual)
- [ ] Add cost tracking to Stock Ledger Entry
  - incoming_rate, outgoing_rate
  - valuation_rate (calculated)
  - stock_value, stock_value_difference
- [ ] Implement Moving Average costing
  - Calculate on each incoming transaction
  - Update valuation_rate on Product
- [ ] Create COGS calculation utility
  - Calculate cost of goods sold from ledger entries
  - Report by department and time period

**Deliverables:**
- Valuation fields on Product
- Moving Average costing logic
- COGS reporting

---

### Phase 2: Batch Tracking & Expiration (1 week)

**Tasks:**
- [ ] Create Batch Number DocType
  - batch_id (auto-generated or manual)
  - product (Link to Product)
  - manufacturing_date (Date, optional)
  - expiration_date (Date, optional)
  - quantity (Float, read-only - calculated from ledger)
  - department (Link to Department)
- [ ] Add batch support to Stock Ledger Entry
  - batch_number (Link to Batch Number)
  - Split entries by batch when needed
- [ ] Update Inventory Audit to support batch entry
  - Batch selection on audit lines
  - Expiration date warnings
- [ ] Add has_batch_no flag to Product
  - Enable batch tracking per product
  - Validation: require batch on transactions if enabled

**Deliverables:**
- Batch Number DocType
- Batch tracking in Stock Ledger
- Expiration management

---

### Phase 3: ERPNext Compatibility Layer (1 week)

**Tasks:**
- [ ] Add ERPNext-compatible fields to Product (optional)
  - item_code (Data, hidden, read-only) = product_code
  - item_name (Data, hidden, read-only) = product_name
  - stock_uom (Link to UOM, optional)
  - item_group (Link to Item Group, optional)
- [ ] Create ERPNext Item sync utility
  - Import ERPNext Items as BLKSHP Products
  - Map Item Group → Product Category
  - Map UOM → primary_count_unit (best-effort)
  - One-way sync on import
- [ ] Document field mappings
  - Create mapping reference guide
  - Include migration examples
  - API compatibility notes

**Deliverables:**
- ERPNext-compatible fields (optional)
- Item import utility
- Migration documentation

---

## Part 6: Migration Impact Assessment

### Database Changes

**New DocTypes:**
- Stock Ledger Entry (new table)
- Batch Number (new table)

**Modified DocTypes:**
- Product: Add 5-8 optional fields
- Inventory Audit: Add batch support

**Data Migration:**
- No historical data migration required (Stock Ledger starts fresh)
- Existing Inventory Balances unchanged
- Future audits generate ledger entries

**Breaking Changes:**
- ✅ None - all changes are additive

---

### API Impact

**New APIs:**
- `get_stock_ledger_entries(product, department, from_date, to_date)`
- `calculate_cogs(department, period)`
- `get_batch_numbers(product, department, include_expired=False)`

**Modified APIs:**
- Inventory Audit submission now generates Stock Ledger Entries
- No breaking changes to existing APIs

---

### Performance Considerations

**Stock Ledger Entry Volume:**
- Assumption: 500 products × 5 departments × 12 audits/year = 30,000 entries/year
- Mitigation: Index on (product, department, posting_date)
- Archival: Summarize entries older than 2 years

**Query Optimization:**
- Running balance calculation cached in qty_after_transaction
- COGS calculation uses indexed queries
- Batch expiration checks use date index

---

## Part 7: Success Metrics

### Phase 1 Success Criteria
- [ ] Stock Ledger Entry captures all inventory movements
- [ ] Running balance matches Inventory Balance after audit
- [ ] COGS calculated automatically from ledger
- [ ] Valuation rate updates on purchases

### Phase 2 Success Criteria
- [ ] Batch numbers tracked for perishable items
- [ ] Expiration warnings displayed in audits
- [ ] FIFO cost calculation available (optional)

### Phase 3 Success Criteria
- [ ] ERPNext Item data importable without errors
- [ ] Field mapping documented and tested
- [ ] Migration guide validated by test user

---

## Part 8: Decision Log

### Decisions Made

1. ✅ **Maintain BLKSHP-specific design** - Do not rename Product → Item
2. ✅ **Add Stock Ledger Entry** - Parallel to Inventory Balance for audit trail
3. ✅ **Implement valuation tracking** - Add cost fields to Product and ledger
4. ✅ **Support batch tracking** - Essential for food safety and expiration
5. ✅ **Create compatibility layer** - Optional ERPNext field mapping
6. ⚠️ **Defer UOM migration** - Keep select-based units, add UOM link as optional
7. ⚠️ **Defer serial numbers** - Not critical for hospitality (focus on batches)

### Decisions Deferred

1. Full UOM DocType migration - evaluate in Phase 3+ based on feedback
2. Serial number support - not a priority for hospitality operations
3. ERPNext Manufacturing integration - outside current scope
4. LIFO costing - start with Moving Average, add FIFO/LIFO if needed

---

## Part 9: References

**ERPNext Documentation:**
- [Stock Module Overview](https://docs.erpnext.com/docs/user/manual/en/stock)
- [Stock Entry](https://docs.erpnext.com/docs/user/manual/en/stock-entry)
- [Serial and Batch Bundle (v15)](https://frappe.io/blog/product-updates/v15-erpnext-updates)

**ERPNext Source Code:**
- [Item DocType](https://github.com/frappe/erpnext/blob/version-15/erpnext/stock/doctype/item/item.json)
- [Stock Ledger Entry](https://github.com/frappe/erpnext/blob/version-15/erpnext/stock/doctype/stock_ledger_entry/stock_ledger_entry.json)

**BLKSHP OS Current Implementation:**
- `blkshp_os/products/doctype/product/product.json`
- `blkshp_os/inventory/doctype/inventory_balance/inventory_balance.json`
- `blkshp_os/inventory/doctype/inventory_audit/inventory_audit.py`

**Related Issues:**
- BLK-15 (this analysis)
- BLK-14 (Operations audit - revealed current state)
- BLK-40 (Transfers & Depletions - needs Stock Ledger Entry)

---

## Part 10: Next Steps

### Immediate Actions
1. ✅ **Review this analysis** - Share with team for feedback
2. 🔄 **Create Linear issues** - Break down implementation into issues
3. 🔄 **Update PROJECT-TIMELINE.md** - Add to Phase 2 scope
4. 🔄 **Prioritize phases** - Confirm order and timing

### Phase 1 Preparation
5. 📋 **Design Stock Ledger Entry schema** - Finalize field list
6. 📋 **Design valuation calculation** - Moving Average algorithm
7. 📋 **Plan Inventory Audit migration** - Generate ledger entries on completion

### Documentation
8. 📝 **Create Stock Ledger Entry specification** - Detailed DocType design
9. 📝 **Create Batch Number specification** - Detailed DocType design
10. 📝 **Update CONSOLIDATED_DECISION_LOG.md** - Record decisions

---

**Analysis Author:** Claude Code (AI Assistant)
**Review Required:** Product Owner / Technical Lead
**Estimated Effort:** 4 weeks (3 phases)
**Risk Level:** Medium (additive changes, no breaking modifications)

**Status:** ✅ ANALYSIS COMPLETE - READY FOR REVIEW
