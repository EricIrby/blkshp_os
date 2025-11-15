# Transfers & Depletions Module - Decision Document

**Date:** 2025-11-14
**Status:** DECISION NEEDED
**Related Issues:** BLK-14 (Operations Audit)

---

## Current Situation

The `transfers_depletions` module exists in `modules.txt` but contains **zero DocTypes**. Only an empty `__init__.py` file exists.

---

## Evidence of Planned Implementation

### 1. Module Registration
- ✅ Listed in `blkshp_os/modules.txt` as "Transfers Depletions"
- ✅ Directory structure created: `blkshp_os/transfers_depletions/`
- ❌ No DocTypes implemented

### 2. Permissions Defined (8 total)

**Transfer Permissions** (`blkshp_os/permissions/constants.py`):
```python
TRANSFERS_PERMISSIONS = [
    "transfers.view" - View inventory transfers
    "transfers.create" - Create inventory transfers
    "transfers.approve" - Approve transfer requests
    "transfers.edit" - Edit transfers (implied)
]
```

**Depletion Permissions**:
```python
DEPLETIONS_PERMISSIONS = [
    "depletions.view" - View manual depletions
    "depletions.create" - Create manual depletions
    "depletions.edit" - Edit depletions
    "depletions.delete" - Delete depletions
]
```

All depletion permissions are `department_restricted: True`

### 3. Department Integration Ready

`Department` DocType has transfer-related fields:
```python
allow_inter_department_transfers: bool
require_approval_for_transfers: bool
transfer_approval_roles: list[str]
```

---

## Business Requirements Analysis

### Transfers Use Case

**Scenario:** Restaurant with multiple departments
- Bar department needs lemons from Kitchen
- Kitchen creates transfer: 5 lbs lemons → Bar
- Bar manager approves transfer
- Inventory adjusted: Kitchen -5 lbs, Bar +5 lbs

**Why It Matters:**
- ✅ Accurate departmental COGS tracking
- ✅ Inventory accountability by location
- ✅ Audit trail for internal movements
- ✅ Prevents "ghost shrinkage" (movement looks like loss)

### Depletions Use Case

**Scenario:** Manual inventory adjustments
- Bottle of wine breaks in storage → Depletion (breakage)
- Manager comp's meal to VIP → Depletion (comp)
- Meat spoils before use → Depletion (spoilage)
- Staff meal at end of shift → Depletion (employee meal)

**Why It Matters:**
- ✅ Accurate inventory valuation
- ✅ Distinguish loss types (theft vs spoilage vs comp)
- ✅ Financial reporting (COGS impact by category)
- ✅ Operational insights (high spoilage = purchasing issue)

---

## Implementation Scope

### Minimal Viable Implementation

#### 1. Inventory Transfer DocType
**Fields:**
- Transfer Number (auto-generated)
- From Department (link to Department)
- To Department (link to Department)
- Transfer Date
- Status (Draft, Pending Approval, Approved, Rejected, Completed)
- Transfer Lines (child table):
  - Product (link to Product)
  - Quantity
  - Unit
  - From Storage Location (optional)
  - To Storage Location (optional)
- Notes/Reason
- Requested By (link to User)
- Approved By (link to User)
- Approval Date

**Workflow:**
1. Draft → Submit (creates Pending Approval)
2. Pending Approval → Approve (creates Completed + inventory ledger entries)
3. Pending Approval → Reject (cancels transfer)

**Inventory Impact:**
- On Approval: Decrease source department inventory, increase destination department inventory
- Creates Stock Ledger Entries for audit trail

#### 2. Inventory Depletion DocType
**Fields:**
- Depletion Number (auto-generated)
- Department (link to Department)
- Depletion Date
- Depletion Type (dropdown: Spoilage, Breakage, Theft, Comp, Employee Meal, Waste, Other)
- Status (Draft, Submitted, Cancelled)
- Depletion Lines (child table):
  - Product (link to Product)
  - Quantity
  - Unit
  - Cost Amount (calculated)
  - Storage Location (optional)
- Reason/Notes
- Created By (link to User)
- Approved By (link to User, if approval required)

**Workflow:**
1. Draft → Submit (decreases inventory immediately)
2. Optional approval workflow for high-value items

**Inventory Impact:**
- On Submit: Decrease department inventory
- Creates Stock Ledger Entry with depletion type
- Affects departmental COGS

---

## Effort Estimation

### Phase 1: Core DocTypes (2-3 days)
- [ ] Create Inventory Transfer DocType (1 day)
- [ ] Create Inventory Depletion DocType (0.5 day)
- [ ] Implement transfer approval workflow (0.5 day)
- [ ] Add inventory ledger integration (1 day)

### Phase 2: Testing (1-2 days)
- [ ] Unit tests for both DocTypes
- [ ] Integration tests for inventory impact
- [ ] Approval workflow tests
- [ ] Department permission tests

### Phase 3: UI & Polish (1 day)
- [ ] Form customizations
- [ ] List view filters
- [ ] Reports (Transfer History, Depletion by Type)
- [ ] Permission checks in UI

**Total Effort:** 4-6 days

---

## Decision Options

### Option 1: Implement Now (RECOMMENDED)

**Pros:**
- ✅ Critical missing functionality for hospitality operations
- ✅ Infrastructure already in place (permissions, department fields)
- ✅ Relatively small scope (4-6 days)
- ✅ High business value (accurate COGS, inventory accountability)
- ✅ Completes "Operations Module" domain

**Cons:**
- ⏳ Delays other Phase 1 work by ~1 week
- 📋 Needs testing to reach production quality

**Recommendation:** Implement in Phase 2 (MVP Readiness)
- After BLK-15 (Product/Inventory alignment)
- Before production deployment
- Essential for multi-department operations

### Option 2: Defer to Phase 3+

**Pros:**
- ⏩ Focus on other Phase 1 priorities
- 📊 Gather user feedback on priority

**Cons:**
- ❌ Incomplete Operations domain
- ❌ Users must track transfers manually (error-prone)
- ❌ Inaccurate departmental COGS
- ❌ Permissions defined but unusable (confusing)

**Not Recommended** - Too important for core hospitality operations

### Option 3: Remove Module (NOT RECOMMENDED)

**Pros:**
- 🗑️ Cleans up empty module

**Cons:**
- ❌ Loses 8 defined permissions
- ❌ Department transfer fields become orphaned
- ❌ Critical feature gap remains
- ❌ Would need to re-create later anyway

**Definitely Not Recommended** - This IS needed functionality

---

## Recommendation

### ✅ DECISION: Implement in Phase 2

**Rationale:**
1. **High Business Value:** Essential for multi-department hospitality operations
2. **Foundation Ready:** Permissions and integration points already exist
3. **Reasonable Scope:** 4-6 days is manageable
4. **Completes Domain:** Makes Operations module production-ready

**Proposed Timeline:**
- **Now (Phase 1):** Continue with BLK-15 (Product/Inventory alignment)
- **Phase 2 Start:** Implement Transfers & Depletions (create BLK-40)
- **Phase 2 End:** Test and refine before MVP deployment

**Dependencies:**
- Should be done AFTER BLK-15 (Product/Inventory alignment)
- Should be done BEFORE production deployment (Phase 2 completion)

---

## Next Steps

1. ✅ **Document this decision** (this file)
2. 🔄 **Create BLK-40:** Implement Inventory Transfer & Depletion DocTypes
3. 📋 **Update PROJECT-TIMELINE.md:** Add to Phase 2 scope
4. 📝 **Update CONSOLIDATED_DECISION_LOG.md:** Record decision
5. 🗂️ **Keep module in modules.txt:** Do not remove

---

## References

- **Permissions:** `blkshp_os/permissions/constants.py` (lines ~300-350)
- **Department Fields:** `blkshp_os/departments/doctype/department/department.py`
- **Audit Finding:** `docs/OPS-MODULE-AUDIT-REPORT.md`
- **Related Issues:** BLK-14, BLK-15

---

**Decision Author:** Claude Code (AI Assistant)
**Review Required:** Product Owner / Operations Lead
**Final Decision:** PENDING APPROVAL
