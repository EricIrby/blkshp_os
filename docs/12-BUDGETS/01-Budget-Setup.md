# Budget Setup

## Overview

Budget Setup creates department-based budgets with GL code allocations. Budgets track planned spending against actual spending for cost control and financial performance management.

## Purpose

- Create department-based budgets
- Allocate budgets to GL codes
- Set budget periods (monthly, quarterly, annual)
- Track budget vs actual spending
- Support budget approval workflow

## DocType Definition

### Budget DocType

```python
# Budget DocType
# Fields
- budget_name (Data, required)
- budget_code (Data, unique)
- company (Link: Company, required)
- department (Link: Department, required)
- budget_period (Select: Monthly, Quarterly, Annual, Custom, required)
- period_start_date (Date, required)
- period_end_date (Date, required)
- fiscal_year (Link: Fiscal Year)  # Optional
- status (Select: Draft, Active, Closed, Cancelled)
- budget_lines (Table: Budget Line)  # GL code allocations
- total_budget_amount (Currency, calculated)
- total_committed (Currency, calculated)
- total_spent (Currency, calculated)
- total_remaining (Currency, calculated)
- utilization_percent (Float, calculated)
- created_by (Link: User)
- created_at (Datetime)
- approved_by (Link: User)
- approved_at (Datetime)
```

### Budget Line DocType (Child Table)

```python
# Budget Line DocType (Child Table)
# Fields
- parent (Link: Budget)
- gl_code (Link: Account, required)
- budget_amount (Currency, required)
- committed_amount (Currency, calculated)
- spent_amount (Currency, calculated)
- remaining_amount (Currency, calculated)
- utilization_percent (Float, calculated)
- notes (Text)
```

## Key Features

### Department-Based
- Each budget assigned to single department
- Allows department managers to own budgets
- Enables department-specific cost control

### GL Code Allocations
- Budgets allocated to GL codes
- Multiple GL codes per budget
- Track spending per GL code

### Budget Periods
- Monthly budgets
- Quarterly budgets
- Annual budgets
- Custom date ranges

### Budget Tracking
- Committed: From purchase orders
- Spent: From receiving activity
- Remaining: Budget - Committed - Spent
- Utilization: (Committed + Spent) / Budget

## Implementation Steps

### Step 1: Create Budget DocType
1. Create `Budget` DocType
2. Add basic fields (name, code, company, department)
3. Add period fields
4. Add budget_lines child table

### Step 2: Add Budget Tracking
1. Add committed_amount field
2. Add spent_amount field
3. Add remaining_amount field
4. Add utilization_percent field

### Step 3: Implement Budget Calculation
1. Implement calculate_budget_totals() method
2. Calculate committed from orders
3. Calculate spent from receiving
4. Calculate remaining and utilization

## Dependencies

- **Company DocType**: Company reference
- **Department DocType**: Department assignment
- **Account DocType**: GL code references
- **Purchase Order DocType**: For committed tracking
- **Receiving DocType**: For spent tracking

## Usage Examples

### Monthly Budget
```
Budget:
  - Name: "Kitchen - January 2025"
  - Department: Kitchen
  - Period: Monthly
  - Start Date: 2025-01-01
  - End Date: 2025-01-31
  
  Budget Lines:
    - Food Cost: $16,500
    - Beverage Cost: $10,000
    - Supplies: $2,500
```

## Testing Checklist

- [ ] Create budget with valid data
- [ ] Add budget lines with GL codes
- [ ] Set budget periods
- [ ] Approve budget
- [ ] Track committed amounts
- [ ] Track spent amounts
- [ ] Calculate remaining amounts
- [ ] Calculate utilization percent

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 13

