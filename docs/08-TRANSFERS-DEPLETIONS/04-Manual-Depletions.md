# Manual Depletions

## Overview

Manual Depletions track inventory consumption, waste, spillage, and other losses that are not automatically calculated from POS sales. Supports various depletion types for comprehensive inventory tracking.

## Purpose

- Track manual inventory consumption
- Record waste and spillage
- Track theft and losses
- Support complimentary items
- Maintain accurate inventory balances

## DocType Definition

### Depletion DocType

```python
# Depletion DocType
# Fields
- depletion_number (Data, unique, auto-generated)
- depletion_date (Date, required)
- company (Link: Company, required)
- department (Link: Department, required)
- depletion_type (Select: Sold, Spilled, Wasted, Manual, Theft/Loss, Comp, required)
- source_type (Select: POS Sale, Manual Entry, Batch Production, Recipe Usage, required)
- source_reference (Dynamic Link)  # Link to POS Sale, Batch, etc.
- depletion_lines (Table: Depletion Line)
- total_depletion_value (Currency, calculated)
- status (Select: Draft, Posted, Cancelled)
- reason (Text)  # Reason for depletion
- approved_by (Link: User)
- approved_at (Datetime)
- posted_by (Link: User)
- posted_at (Datetime)

# Methods
def validate_depletion():
    """Validate depletion before posting"""
    pass

def post_depletion():
    """Post depletion to update inventory"""
    pass

def calculate_depletion_value():
    """Calculate total depletion value"""
    pass
```

### Depletion Line DocType (Child Table)

```python
# Depletion Line DocType (Child Table)
# Fields
- parent (Link: Depletion)
- parenttype ("Depletion")
- parentfield ("depletion_lines")
- product (Link: Product, required)
- quantity (Float, required)  # In product's primary count unit
- unit_cost (Currency, calculated)
- total_value (Currency, calculated)
- gl_code (Link: Account, required)
- storage_location (Link: Storage Area, optional)
- notes (Text)
```

## Depletion Types

### Spilled
- Physical spillage or breakage
- Accidental loss
- Recorded immediately

### Wasted
- Spoiled, expired, or unusable inventory
- Quality issues
- Recorded when discovered

### Manual
- Manual consumption for other reasons
- General use
- Various purposes

### Theft/Loss
- Theft or unexplained loss
- Security issues
- Requires investigation

### Comp/Complimentary
- Given away for free
- Promotional items
- Customer service

## Implementation Steps

### Step 1: Create Depletion DocType
1. Create `Depletion` DocType
2. Add depletion date and company fields
3. Add department and depletion_type fields
4. Add depletion_lines child table

### Step 2: Implement Depletion Workflow
1. Create depletion (Draft)
2. Add depletion lines
3. Validate depletion
4. Post depletion (reduce inventory)

### Step 3: Add Cost Calculation
1. Calculate unit costs
2. Calculate total depletion value
3. Assign GL codes

## Dependencies

- **Company DocType**: Company reference
- **Department DocType**: Department assignment
- **Product DocType**: Product references
- **Account DocType**: GL code mapping

## Usage Examples

### Waste Depletion
```
Depletion:
  - Type: Wasted
  - Department: Kitchen
  - Reason: Expired produce
  - Date: 2025-01-31
  
  Lines:
    - Lettuce: 5 lb
    - Tomatoes: 3 lb
```

### Spillage Depletion
```
Depletion:
  - Type: Spilled
  - Department: Bar
  - Reason: Broken bottle
  - Date: 2025-01-31
  
  Lines:
    - Wine: 1 bottle
```

## Testing Checklist

- [ ] Create depletion (Draft)
- [ ] Add depletion lines
- [ ] Validate depletion
- [ ] Post depletion
- [ ] Verify inventory reduction
- [ ] Calculate depletion value
- [ ] Track GL codes
- [ ] Cancel depletion

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 17

