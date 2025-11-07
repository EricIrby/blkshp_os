# Inventory Audits

## Overview

Inventory Audits are physical counts of inventory with a task-based assignment system. Audits go through a workflow from Setup → Ready → In Progress → Review → Closed → Locked.

## Purpose

- Conduct physical inventory counts
- Organize counts by department and storage
- Support full and partial audits
- Track audit progress and completion
- Calculate variances and close audit period

## DocType Definition

### Inventory Audit DocType

```python
# Fields
- audit_name (Data, required)
- audit_type (Select: Full, Partial)
- audit_date (Date, required)
- company (Link: Company, required)
- status (Select: Setup, Ready, In Progress, Review, Closed, Locked)

# Audit Scope (for reference/reporting)
- audit_departments (Table: Audit Department)  # Which departments in scope
- audit_storage_locations (Table: Audit Storage Location)  # Which storages in scope
- audit_categories (Table: Audit Category)  # Which categories (if partial)

# Counting Tasks (Department + Storage + Category assignments)
- counting_tasks (Table: Counting Task)

# Audit Results
- audit_lines (Table: Audit Line)  # All counts from all users
- total_products_counted (Int, calculated)
- total_value (Currency, calculated)
- closed_by (Link: User)
- closed_at (Datetime)

# Closing Data
- pos_sales_date_from (Date)
- pos_sales_date_to (Date)
```

### Methods

```python
def create_counting_tasks():
    """Auto-create counting tasks from audit scope"""
    # Group storages by department
    # Create task for each department-storage combination
    # Assign categories if partial audit
    pass

def close_audit():
    """Close audit and calculate variances"""
    # Pull POS sales for each department
    # Calculate theoretical inventory per department
    # Compare to actual counts
    # Flag high variances
    # Close period
    pass

def calculate_variance():
    """Compare actual vs theoretical per department"""
    pass
```

## Audit Workflow

### Status Flow

```
Setup → Ready → In Progress → Review → Closed → Locked
```

**Setup:**
- Audit created
- Scope defined (departments, storages, categories)
- Counting tasks not yet created

**Ready:**
- Counting tasks created
- Tasks assigned to departments/users
- Ready for counting to begin

**In Progress:**
- Counting has begun
- Users are entering counts
- Some tasks may be complete

**Review:**
- All counting complete
- Reviewing counts for accuracy
- Making corrections if needed

**Closed:**
- Audit finalized
- Variances calculated
- Inventory balances updated
- Period closed

**Locked:**
- Audit locked (after X days)
- Cannot be modified
- Used for historical reporting

## Audit Types

### Full Audit
- Count all products in all departments
- All storage locations
- Complete inventory snapshot

### Partial Audit
- Count specific categories
- Count specific departments
- Count specific storage locations
- Useful for cycle counting

## Implementation Steps

### Step 1: Create Inventory Audit DocType
1. Create `Inventory Audit` DocType
2. Add core fields (name, type, date, company, status)
3. Add scope tables (departments, storages, categories)
4. Add counting_tasks table

### Step 2: Add Audit Results
1. Add audit_lines table
2. Add calculated fields (total_products_counted, total_value)
3. Add closing fields (closed_by, closed_at)

### Step 3: Implement Methods
1. Implement create_counting_tasks()
2. Implement close_audit()
3. Implement calculate_variance()

### Step 4: Implement Workflow
1. Create workflow states
2. Add transitions between states
3. Add validations for state changes
4. Add permissions per state

## Dependencies

- **Company DocType**: Company reference (Frappe built-in)
- **Department DocType**: Department assignments
- **Storage Area DocType**: Storage locations
- **Product Category DocType**: Category filtering
- **Counting Task DocType**: Task assignments
- **Audit Line DocType**: Count entries

## Usage Examples

### Full Audit Setup
```
Audit:
  - Name: "January 2025 Full Inventory"
  - Type: "Full"
  - Date: 2025-01-31
  - Company: "Store 1"
  - Status: "Setup"
  
  Departments: All departments
  Storage Locations: All storage locations
  Categories: All categories
```

### Partial Audit Setup
```
Audit:
  - Name: "January 2025 Beverage Count"
  - Type: "Partial"
  - Date: 2025-01-15
  - Company: "Store 1"
  - Status: "Setup"
  
  Departments: Beverage, Bar
  Storage Locations: Bar Cooler, Wine Cellar
  Categories: Beer, Wine, Spirits
```

### Audit Closing
```
1. Set status to "Review"
2. Review all counts
3. Make corrections if needed
4. Set status to "Closed"
5. Calculate variances
6. Update inventory balances
7. Lock audit (after X days)
```

## Testing Checklist

- [ ] Create full audit
- [ ] Create partial audit
- [ ] Define audit scope
- [ ] Create counting tasks
- [ ] Update audit status
- [ ] Enter audit lines
- [ ] Calculate totals
- [ ] Close audit
- [ ] Calculate variances
- [ ] Lock audit
- [ ] Verify inventory balance updates

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

