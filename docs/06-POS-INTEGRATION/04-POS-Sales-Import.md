# POS Sales Import

## Overview

POS Sales Import handles importing sales data from POS systems via API polling or manual file import. Sales data is then processed to create inventory depletions.

## Purpose

- Import sales data from POS systems
- Support automatic API polling
- Support manual file import
- Process sales to create depletions
- Track sales by department and instance

## POS Sale DocType

```python
# POS Sale DocType
# Fields
- sale_number (Data, unique, auto-generated)
- pos_instance (Link: POS Instance, required)
- pos_system (Select: Toast, Square, Clover, Resy, Custom)
- pos_transaction_id (Data, required)
- sale_date (Date, required)
- sale_time (Time, required)
- company (Link: Company, required)
- department (Link: Department, required)
- sale_lines (Table: POS Sale Line)
- total_amount (Currency, calculated)
- total_items (Int, calculated)
- server (Link: User, optional)
- table_number (Data, optional)
- payment_method (Select: Cash, Card, Mobile, Other)
- status (Select: Imported, Processed, Error)
- import_source (Select: API Poll, Manual Import, Manual Repoll)
- imported_at (Datetime)
- processed_at (Datetime)
- depletion_created (Check)
- poll_batch_id (Data, optional)
```

## Import Methods

### Automatic API Polling
- Scheduled polling based on instance frequency
- Polls sales data since last poll
- Creates POS Sale records automatically
- Processes depletions if enabled

### Manual File Import
- Upload CSV/Excel file with sales data
- Map columns to POS Sale fields
- Validate and import sales
- Process depletions after import

### Manual Repoll
- Manually trigger API poll
- Specify date range
- Overwrite existing sales if needed
- Useful for corrections

## Implementation Steps

### Step 1: Create POS Sale DocType
1. Create `POS Sale` DocType
2. Add POS instance link
3. Add transaction fields
4. Add sale_lines child table

### Step 2: Implement API Polling
1. Create polling scheduler
2. Poll sales from POS API
3. Create POS Sale records
4. Track poll status

### Step 3: Implement File Import
1. Support CSV/Excel import
2. Validate file format
3. Map columns
4. Create POS Sale records

## Dependencies

- **POS Instance DocType**: Instance reference
- **POS Sale Line DocType**: Sale line items
- **Department DocType**: Department assignment

## Testing Checklist

- [ ] Import sales via API polling
- [ ] Import sales via file upload
- [ ] Manual repoll functionality
- [ ] Validate sales data
- [ ] Create POS Sale records
- [ ] Process sales to depletions
- [ ] Track import status
- [ ] Handle import errors

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 20.3

