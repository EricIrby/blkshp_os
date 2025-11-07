# Inventory Balance

## Overview

Inventory Balance tracks inventory quantities using a 2D model (Product + Department). Storage locations are tracked as metadata only and do not create separate inventory buckets. All quantities are stored in the product's primary count unit.

## Purpose

- Track inventory by Product + Department combination
- Store quantities in primary count units
- Track last audit date
- Support department-based inventory management
- Enable inventory history tracking

## DocType Definition

### Inventory Balance DocType

```python
# Inventory Balance (Product + Department only - 2D)
- product (Link: Product, required)
- department (Link: Department, required)
- company (Link: Company, required)
- quantity (Float)  # Quantity in product's primary count unit
- last_updated (Datetime)
- last_audit_date (Date)
```

## Key Features

### 2D Model (Product + Department)
- Inventory tracked by Product + Department combination
- Storage location is metadata only (not part of inventory balance)
- Same product can have different quantities per department

### Primary Count Unit
- All quantities stored in product's primary count unit
- Conversions handled when displaying/entering data
- Consistent inventory tracking across all units

### Last Audit Date
- Tracks when inventory was last audited
- Used for theoretical inventory calculations
- Enables audit history tracking

## Implementation Steps

### Step 1: Create Inventory Balance DocType
1. Create `Inventory Balance` DocType
2. Add product link (required)
3. Add department link (required)
4. Add company link (required)

### Step 2: Add Quantity Fields
1. Add quantity field (Float)
2. Add last_updated field (Datetime)
3. Add last_audit_date field (Date)

### Step 3: Set Unique Constraint
1. Set unique constraint on (product, department, company)
2. Ensure one balance record per product-department combination

### Step 4: Implement Update Methods
1. Update balance on audit closing
2. Update balance on transfers
3. Update balance on depletions
4. Update last_audit_date on audit close

## Dependencies

- **Product DocType**: Product reference
- **Department DocType**: Department reference
- **Company DocType**: Company reference (Frappe built-in)

## Usage Examples

### Single Product, Multiple Departments
```
Product: "Coca Cola Cans"
Inventory Balance:
  - Department: "Beverage"
    Quantity: 120 each
    Last Audit: 2025-01-15
  - Department: "Bar"
    Quantity: 60 each
    Last Audit: 2025-01-15
```

### Inventory Update on Audit Close
```
1. Audit closes with counts
2. Sum counts by product + department
3. Update Inventory Balance
4. Set last_audit_date to audit date
```

## Testing Checklist

- [ ] Create inventory balance record
- [ ] Verify unique constraint (product + department + company)
- [ ] Update quantity on audit close
- [ ] Update quantity on transfer
- [ ] Update quantity on depletion
- [ ] Verify quantities in primary count unit
- [ ] Track last audit date
- [ ] Query inventory by department

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

