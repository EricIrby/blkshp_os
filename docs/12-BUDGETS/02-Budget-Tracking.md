# Budget Tracking

## Overview

Budget Tracking monitors budget utilization by tracking committed amounts (from orders) and spent amounts (from receiving activity) against budgeted amounts.

## Purpose

- Track budget commitments from orders
- Track budget spending from receiving
- Calculate budget utilization
- Generate budget alerts
- Support budget vs actual reporting

## Tracking Components

### Committed Amounts
- From purchase orders
- Budget committed when order placed
- Tracked per GL code
- Reversed if order cancelled

### Spent Amounts
- From receiving activity
- Budget spent when goods received
- Tracked per GL code
- From Ottimate import or manual receiving

### Remaining Amounts
- Budget - Committed - Spent
- Available budget remaining
- Calculated per GL code
- Real-time updates

### Utilization Percent
- (Committed + Spent) / Budget * 100
- Percentage of budget used
- Alerts when approaching limits
- Tracked per GL code

## Implementation

### Budget Tracking DocType

```python
# Budget Tracking DocType (Auto-generated)
# Fields
- budget (Link: Budget, required)
- budget_line (Link: Budget Line)
- transaction_type (Select: Order, Receiving, Adjustment)
- transaction_reference (Dynamic Link)
- department (Link: Department, required)
- gl_code (Link: Account, required)
- amount (Currency, required)
- transaction_date (Date, required)
- is_committed (Check)
- is_spent (Check)
- created_at (Datetime)
```

## Implementation Steps

### Step 1: Create Budget Tracking DocType
1. Create `Budget Tracking` DocType
2. Add budget and budget_line links
3. Add transaction tracking fields
4. Add amount and date fields

### Step 2: Implement Order Tracking
1. Create tracking record when order placed
2. Update committed_amount on budget line
3. Reverse if order cancelled

### Step 3: Implement Receiving Tracking
1. Create tracking record when goods received
2. Update spent_amount on budget line
3. Support Ottimate import

### Step 4: Implement Budget Alerts
1. Check utilization percent
2. Generate alerts when approaching limits
3. Notify budget owners

## Dependencies

- **Budget DocType**: Budget reference
- **Purchase Order DocType**: Order commitments
- **Receiving DocType**: Spending tracking

## Usage Examples

### Budget Utilization
```
Budget: "Kitchen - January 2025"
  - Total Budget: $29,000
  - Committed: $15,000 (from orders)
  - Spent: $12,000 (from receiving)
  - Remaining: $2,000
  - Utilization: 93.1%
```

### Budget Alert
```
Alert: Budget 90% Utilized
  - Budget: "Kitchen - January 2025"
  - GL Code: "Food Cost"
  - Utilization: 92%
  - Remaining: $1,320
```

## Testing Checklist

- [ ] Track order commitments
- [ ] Track receiving spending
- [ ] Calculate remaining amounts
- [ ] Calculate utilization percent
- [ ] Generate budget alerts
- [ ] Reverse cancelled orders
- [ ] Support Ottimate import

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 13

