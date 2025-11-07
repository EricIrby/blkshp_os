# Transfer Workflow

## Overview

Transfer Workflow defines the lifecycle of inventory transfers from creation through acknowledgment. Ensures proper tracking and inventory balance updates.

## Purpose

- Define transfer lifecycle stages
- Control transfer state transitions
- Ensure inventory balance accuracy
- Support transfer tracking
- Enable transfer cancellation

## Workflow States

### Draft
- Transfer created
- Products and quantities added
- Not yet submitted
- Can be modified freely

### Submitted
- Transfer submitted
- Inventory reduced from source department
- Transfer value calculated
- Ready for acknowledgment

### In Transit (Optional)
- For inter-store transfers
- Goods in transit
- Inventory reduced from source
- Not yet received at destination

### Acknowledged
- Transfer received
- Inventory increased at destination
- Transfer complete
- Theoretical inventory updated

### Cancelled
- Transfer cancelled
- Any inventory changes reversed
- Transfer cannot be completed

## State Transitions

### Normal Flow
```
Draft → Submitted → In Transit (optional) → Acknowledged
```

### Cancellation Flow
```
Draft → Cancelled
Submitted → Cancelled (reverses inventory reduction)
In Transit → Cancelled (reverses inventory reduction)
```

## Implementation Steps

### Step 1: Create Workflow
1. Create workflow in Frappe
2. Define states (Draft, Submitted, In Transit, Acknowledged, Cancelled)
3. Define transitions between states
4. Set permissions per state

### Step 2: Implement State Actions
1. Reduce inventory on Submitted
2. Increase inventory on Acknowledged
3. Reverse changes on Cancelled
4. Update theoretical inventory

### Step 3: Add Validation
1. Validate sufficient inventory
2. Validate product availability
3. Validate department assignments
4. Block invalid transitions

## Dependencies

- **Inventory Transfer DocType**: Transfer records
- **Inventory Balance DocType**: Inventory updates

## Usage Examples

### Inter-Department Transfer
```
1. Create transfer (Draft)
2. Add products and quantities
3. Submit transfer (Submitted)
   - Inventory reduced from Kitchen
4. Acknowledge transfer (Acknowledged)
   - Inventory increased in Bar
```

### Inter-Store Transfer
```
1. Create transfer (Draft)
2. Add products and quantities
3. Submit transfer (Submitted)
   - Inventory reduced from Store 1
4. Mark in transit (In Transit)
5. Acknowledge receipt (Acknowledged)
   - Inventory increased in Store 2
```

## Testing Checklist

- [ ] Create transfer (Draft)
- [ ] Submit transfer (Submitted)
- [ ] Mark in transit (In Transit)
- [ ] Acknowledge transfer (Acknowledged)
- [ ] Cancel transfer (Cancelled)
- [ ] Verify inventory updates
- [ ] Verify state transitions
- [ ] Test validation rules

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 16.3

