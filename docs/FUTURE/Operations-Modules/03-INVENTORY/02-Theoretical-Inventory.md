# Theoretical Inventory

## Overview

Theoretical Inventory calculates expected inventory quantities based on the last audit plus all transactions (receipts, transfers, depletions) since then. Uses a 2D model (Product + Department) with storage as metadata only.

## Purpose

- Calculate expected inventory quantities
- Compare with actual counts to find variances
- Support variance analysis and reporting
- Enable inventory tracking between audits
- Support audit closing process

## Calculation Formula

```
Theoretical Inventory = 
    Starting Inventory (from last audit)
    + Received (from invoices, allocated to department)
    + Transferred In (to department)
    - Transferred Out (from department)
    - Depleted (sold, spilled, manual, in department)
```

## Implementation

### Calculate Theoretical Inventory Function

```python
@frappe.whitelist()
def calculate_theoretical_inventory(product, company, department, as_on_date):
    """
    Calculate theoretical inventory for Product + Department (2D model)
    Storage location is metadata only - not part of calculation
    """
    
    # Get last audit date for this company
    last_audit = frappe.get_last_doc('Inventory Audit', {
        'company': company,
        'status': 'Closed'
    })
    
    # Check if this department was in last audit
    audit_dept = frappe.get_value('Audit Department', {
        'parent': last_audit.name,
        'department': department
    })
    
    if not last_audit or not audit_dept:
        return 0
    
    # Starting inventory from last audit (sum across all storages for this department)
    # All counts stored in primary count unit
    starting_qty = sum_audit_counts(last_audit, product, department)
    
    # Received from invoices (after last audit) - allocated to this department
    received_qty = sum_invoice_receipts(product, department, company, 
                                        last_audit.audit_date, as_on_date)
    
    # Transferred in (to this department)
    transferred_in_qty = sum_transfers_in(product, department, company,
                                          last_audit.audit_date, as_on_date)
    
    # Transferred out (from this department)
    transferred_out_qty = sum_transfers_out(product, department, company,
                                            last_audit.audit_date, as_on_date)
    
    # Depleted (sold, spilled, manual) in this department
    depleted_qty = sum_depletions(product, department, company,
                                  last_audit.audit_date, as_on_date)
    
    # Calculate theoretical (Product + Department - 2D model)
    theoretical = (
        starting_qty +
        received_qty +
        transferred_in_qty -
        transferred_out_qty -
        depleted_qty
    )
    
    return theoretical
```

## Calculation Components

### Starting Inventory
- Sum of all audit line counts for product + department
- From last closed audit
- All counts in primary count unit
- Summed across all storage locations (storage is metadata only)

### Received (From Invoices)
- Invoice lines allocated to department
- Check both direct department assignment and split lines
- Convert purchase unit quantities to primary count unit
- Only approved invoices
- Between last audit date and as_on_date

### Transferred In
- Transfers to this department
- Only acknowledged transfers
- Between last audit date and as_on_date

### Transferred Out
- Transfers from this department
- Only acknowledged transfers
- Between last audit date and as_on_date

### Depleted
- Manual depletions in this department
- POS-driven automatic depletions
- All depletion types (sold, spilled, wasted, manual)
- Between last audit date and as_on_date

## Key Features

### 2D Model
- Calculated per Product + Department combination
- Storage location not included in calculation
- Consistent with inventory balance model

### Department-Aware
- All transactions are department-specific
- Theoretical calculated per department
- Supports inter-department transfers

### Unit Conversion
- All quantities converted to primary count unit
- Consistent unit handling
- Accurate calculations

## Implementation Steps

### Step 1: Create Calculation Function
1. Create calculate_theoretical_inventory function
2. Get last audit for company
3. Verify department was in audit

### Step 2: Implement Component Calculations
1. Implement starting inventory calculation
2. Implement received calculation (invoices)
3. Implement transferred in/out calculations
4. Implement depleted calculation

### Step 3: Add Batch Production Support
1. Add batch production to theoretical calculation
2. Track batches produced
3. Include batch production in starting inventory

### Step 4: Create Caching
1. Cache theoretical calculations
2. Invalidate cache on transactions
3. Optimize performance

## Dependencies

- **Inventory Audit DocType**: For starting inventory
- **Vendor Invoice DocType**: For received quantities
- **Inventory Transfer DocType**: For transfer quantities
- **Depletion DocType**: For depletion quantities
- **Product DocType**: For unit conversions

## Usage Examples

### Calculate Theoretical for Audit
```
Product: "Coca Cola Cans"
Department: "Beverage"
As On Date: 2025-01-31

Calculation:
  Starting (from audit 2025-01-15): 100 each
  + Received (invoices): 240 each
  + Transferred In: 0 each
  - Transferred Out: 20 each
  - Depleted (POS): 180 each
  
  Theoretical: 140 each
```

### Compare with Actual Count
```
Audit Count: 135 each
Theoretical: 140 each
Variance: -5 each (-3.6%)
```

## Testing Checklist

- [ ] Calculate theoretical with starting inventory
- [ ] Include invoice receipts
- [ ] Include transfers in
- [ ] Include transfers out
- [ ] Include depletions
- [ ] Handle missing last audit
- [ ] Handle department not in audit
- [ ] Verify unit conversions
- [ ] Compare with actual counts
- [ ] Calculate variance

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 8.1

