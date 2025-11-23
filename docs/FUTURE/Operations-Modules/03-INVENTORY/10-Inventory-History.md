# Inventory History

## Overview

Inventory History tracks historical inventory quantities over time. This enables trend analysis, historical reporting, and inventory movement tracking.

## Purpose

- Track inventory quantities over time
- Support historical reporting
- Enable trend analysis
- Track inventory movements
- Support audit trail

## Historical Tracking

### Inventory Balance History
- Snapshot of inventory at audit close
- Tracked per Product + Department
- Includes quantity and value
- Linked to audit record

### Inventory Movement History
- Track all inventory movements
- Receipts, transfers, depletions
- Date and time tracked
- User tracked

## Implementation

### Inventory History DocType

```python
# Inventory History DocType
# Fields
- product (Link: Product, required)
- department (Link: Department, required)
- company (Link: Company, required)
- date (Date, required)
- quantity (Float)  # Quantity in primary count unit
- value (Currency)  # Total value
- audit (Link: Inventory Audit, optional)  # Link to audit if from audit
- movement_type (Select: Audit, Receipt, Transfer In, Transfer Out, Depletion, Adjustment)
- related_document (Dynamic Link)  # Link to related document
- related_document_type (Data)  # Type of related document
```

## Historical Data Sources

### Audit Closes
- Snapshot created when audit closes
- Quantity from audit counts
- Value calculated from CU prices
- Linked to audit record

### Receipts
- Quantity from invoice receipts
- Value from invoice prices
- Linked to invoice record

### Transfers
- Quantity from transfers
- Value calculated
- Linked to transfer record

### Depletions
- Quantity from depletions
- Value calculated
- Linked to depletion record

## Implementation Steps

### Step 1: Create Inventory History DocType
1. Create `Inventory History` DocType
2. Add product, department, company links
3. Add date field
4. Add quantity and value fields

### Step 2: Add Movement Tracking
1. Add movement_type field
2. Add related_document fields
3. Link to source documents

### Step 3: Implement History Creation
1. Create history on audit close
2. Create history on receipt
3. Create history on transfer
4. Create history on depletion

### Step 4: Create History Reports
1. Historical Inventory Summary Report
2. Historical Inventory Details Report
3. Inventory Trend Report
4. Inventory Movement Report

## Dependencies

- **Product DocType**: Product reference
- **Department DocType**: Department reference
- **Inventory Audit DocType**: Audit records
- **Vendor Invoice DocType**: Receipt records
- **Inventory Transfer DocType**: Transfer records
- **Depletion DocType**: Depletion records

## Usage Examples

### Historical Snapshot
```
Inventory History:
  - Product: "Coca Cola Cans"
  - Department: "Beverage"
  - Date: 2025-01-31
  - Quantity: 135 each
  - Value: $72.85
  - Movement Type: "Audit"
  - Related Document: "January 2025 Full Inventory"
```

### Historical Trend
```
Coca Cola Cans - Beverage Department:
  - 2025-01-15: 100 each ($53.96)
  - 2025-01-31: 135 each ($72.85)
  - Trend: +35 each (+35%)
```

## Testing Checklist

- [ ] Create history on audit close
- [ ] Create history on receipt
- [ ] Create history on transfer
- [ ] Create history on depletion
- [ ] Query historical data
- [ ] Generate historical reports
- [ ] Track inventory trends
- [ ] Link to source documents

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md

