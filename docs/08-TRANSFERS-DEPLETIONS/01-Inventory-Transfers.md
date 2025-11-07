# Inventory Transfers

## Overview

Inventory Transfers manage physical movement of inventory between departments and between stores. Transfers represent actual physical movement of goods and affect inventory balances.

## Purpose

- Transfer inventory between departments
- Transfer inventory between stores
- Track physical movement of goods
- Update inventory balances
- Support cost tracking and allocation

## DocType Definition

### Inventory Transfer DocType

```python
# Inventory Transfer DocType
# Fields
- transfer_number (Data, unique, auto-generated)
- transfer_type (Select: Inter-Department, Inter-Store, required)
- transfer_date (Date, required)
- from_company (Link: Company, required)
- from_location (Link: Location, optional)  # For inter-store
- from_department (Link: Department, required)
- to_company (Link: Company, required)
- to_location (Link: Location, optional)  # For inter-store
- to_department (Link: Department, required)
- transfer_lines (Table: Transfer Line)
- total_transfer_value (Currency, calculated)
- status (Select: Draft, Submitted, In Transit, Acknowledged, Cancelled)
- transfer_reason (Select: Restocking, Reallocation, Temporary Loan, Damage Replacement, Other)
- notes (Text)
- requested_by (Link: User)
- requested_at (Datetime)
- submitted_by (Link: User)
- submitted_at (Datetime)
- acknowledged_by (Link: User)
- acknowledged_at (Datetime)

# Methods
def validate_transfer():
    """Validate transfer before submission"""
    pass

def submit_transfer():
    """Submit transfer (reduces from_department inventory)"""
    pass

def acknowledge_transfer():
    """Acknowledge receipt (increases to_department inventory)"""
    pass

def cancel_transfer():
    """Cancel transfer (reverses if already submitted/acknowledged)"""
    pass
```

### Transfer Line DocType (Child Table)

```python
# Transfer Line DocType (Child Table)
# Fields
- parent (Link: Inventory Transfer)
- parenttype ("Inventory Transfer")
- parentfield ("transfer_lines")
- product (Link: Product, required)
- quantity (Float, required)  # In product's primary count unit
- unit_cost (Currency, calculated)  # Cost at time of transfer
- total_value (Currency, calculated)
- from_storage_location (Link: Storage Area, optional)  # Metadata
- to_storage_location (Link: Storage Area, optional)  # Metadata
- notes (Text)
```

## Transfer Types

### Inter-Department Transfer
- Movement within same store/location
- Between departments
- Updates department inventory balances

### Inter-Store Transfer
- Movement between different stores/locations
- Between companies
- Supports multi-location operations

## Transfer Workflow

### Status Flow
```
Draft → Submitted → In Transit (optional) → Acknowledged
  ↓
Cancelled (can cancel at any stage before Acknowledged)
```

### Status Definitions
- **Draft**: Transfer created but not yet submitted
- **Submitted**: Transfer submitted, inventory reduced from source
- **In Transit**: Optional status for inter-store transfers
- **Acknowledged**: Transfer received, inventory increased at destination
- **Cancelled**: Transfer cancelled, any inventory changes reversed

## Implementation Steps

### Step 1: Create Inventory Transfer DocType
1. Create `Inventory Transfer` DocType
2. Add transfer type and date fields
3. Add from/to company, location, department fields
4. Add transfer_lines child table

### Step 2: Implement Transfer Workflow
1. Implement status transitions
2. Validate transfers before submission
3. Reduce inventory on submission
4. Increase inventory on acknowledgment

### Step 3: Add Cost Tracking
1. Calculate unit costs at transfer time
2. Calculate total transfer value
3. Track cost allocation

## Dependencies

- **Company DocType**: Company reference (Frappe built-in)
- **Department DocType**: Department assignments
- **Product DocType**: Product references
- **Storage Area DocType**: Storage locations (metadata)

## Testing Checklist

- [ ] Create inter-department transfer
- [ ] Create inter-store transfer
- [ ] Submit transfer
- [ ] Acknowledge transfer
- [ ] Cancel transfer
- [ ] Verify inventory updates
- [ ] Calculate transfer costs
- [ ] Track transfer history

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 16

