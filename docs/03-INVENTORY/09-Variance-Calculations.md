# Variance Calculations

## Overview

Variance Calculations compare actual inventory counts to theoretical inventory to identify discrepancies. Variances are calculated per Product + Department combination.

## Purpose

- Compare actual vs theoretical inventory
- Identify discrepancies and losses
- Support variance analysis and reporting
- Flag high variances for investigation
- Calculate variance amounts and percentages

## Calculation Formula

```
Variance = Actual Count - Theoretical Inventory
Variance % = (Variance / Theoretical Inventory) * 100
Variance Amount = Variance * CU Price
```

## Variance Types

### Positive Variance (Overage)
- Actual count > Theoretical inventory
- May indicate receiving errors, transfers not recorded, or other issues
- Typically less common than negative variance

### Negative Variance (Shortage)
- Actual count < Theoretical inventory
- May indicate theft, waste, spillage, or counting errors
- More common in food service operations

### Zero Variance (Match)
- Actual count = Theoretical inventory
- Perfect match (rare in practice)
- Indicates accurate tracking

## Implementation

### Calculate Variance Function

```python
def calculate_variance(audit_line):
    """Calculate variance for audit line"""
    product = audit_line.product
    department = audit_line.department
    company = audit_line.parent.company
    audit_date = audit_line.parent.audit_date
    
    # Get actual count (from audit line)
    actual_count = audit_line.count_in_primary
    
    # Get theoretical inventory
    theoretical = calculate_theoretical_inventory(
        product, company, department, audit_date
    )
    
    # Calculate variance
    variance = actual_count - theoretical
    variance_percent = (variance / theoretical * 100) if theoretical > 0 else 0
    
    # Calculate variance amount
    cu_price = audit_line.cu_price or get_cu_price(product, department)
    variance_amount = variance * cu_price
    
    return {
        'actual': actual_count,
        'theoretical': theoretical,
        'variance': variance,
        'variance_percent': variance_percent,
        'variance_amount': variance_amount
    }
```

## Variance Analysis

### High Variance Thresholds
- **Low Variance**: < 5% difference
- **Medium Variance**: 5-10% difference
- **High Variance**: > 10% difference
- **Critical Variance**: > 20% difference

### Variance Reporting
- Variance by product
- Variance by department
- Variance by category
- Total variance amount
- Variance percentage distribution

## Implementation Steps

### Step 1: Add Variance Fields to Audit Line
1. Add theoretical_inventory field
2. Add variance field
3. Add variance_percent field
4. Add variance_amount field

### Step 2: Implement Variance Calculation
1. Calculate theoretical inventory for each audit line
2. Calculate variance (actual - theoretical)
3. Calculate variance percentage
4. Calculate variance amount

### Step 3: Flag High Variances
1. Set variance thresholds
2. Flag high variances
3. Require investigation for critical variances
4. Track variance resolutions

### Step 4: Create Variance Reports
1. Variance Details Report
2. Variance Summary Report
3. High Variance Report
4. Variance by Department Report

## Dependencies

- **Inventory Audit DocType**: Audit records
- **Audit Line DocType**: Count entries
- **Theoretical Inventory Function**: Theoretical calculations
- **Product DocType**: CU price information

## Usage Examples

### Variance Calculation
```
Product: "Coca Cola Cans"
Department: "Beverage"

Actual Count: 135 each
Theoretical: 140 each
Variance: -5 each (-3.6%)
CU Price: $0.5396
Variance Amount: -$2.70
```

### High Variance Flagging
```
Product: "Premium Whiskey"
Department: "Bar"

Actual Count: 8 bottles
Theoretical: 12 bottles
Variance: -4 bottles (-33.3%)
Status: CRITICAL VARIANCE - Requires Investigation
```

## Testing Checklist

- [ ] Calculate variance for audit line
- [ ] Calculate variance percentage
- [ ] Calculate variance amount
- [ ] Flag high variances
- [ ] Generate variance reports
- [ ] Handle zero theoretical inventory
- [ ] Handle negative variances
- [ ] Handle positive variances

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

