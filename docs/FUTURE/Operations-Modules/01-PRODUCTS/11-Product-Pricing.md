# Product Pricing

## Overview

Product Pricing manages pricing information for products, including contract prices, promotional thresholds, and price violation tracking. This enables cost control and price monitoring.

## Purpose

- Track contract prices from vendors
- Monitor price violations
- Manage promotional pricing thresholds
- Calculate cost per unit
- Support price analysis and reporting

## Contract Price Tracking

### Purchase Unit Pricing
- Contract price per purchase unit
- Current price per purchase unit
- Price history tracking
- Price violation detection

### Price Violation Detection
When invoice price exceeds contract price:
- Create price violation record
- Calculate variance amount and percentage
- Flag for review
- Generate violation reports

## Promotional Threshold Management

### Promo Threshold DocType

```python
# Promo Threshold DocType
# Fields
- threshold_name (Data, required)
- vendor (Link: Vendor, required)
- product (Link: Product, optional)  # Product-specific or all products
- category (Link: Product Category, optional)  # Category-specific
- threshold_type (Select: Quantity, Amount, Both, required)
- quantity_threshold (Float)  # Minimum quantity for promo price
- amount_threshold (Currency)  # Minimum order amount for promo price
- promo_price (Currency, required)  # Promotional price
- regular_price (Currency)  # Regular price (for comparison)
- discount_percent (Float, calculated)  # Discount percentage
- effective_from (Date, required)
- effective_to (Date, required)
- is_active (Check, default=1)
- auto_apply (Check)  # Auto-apply when threshold met
```

### Threshold Types
- **Quantity**: Minimum quantity required
- **Amount**: Minimum order amount required
- **Both**: Both quantity and amount required

### Promo Application
- Check thresholds when ordering
- Auto-apply promo pricing when threshold met
- Calculate savings from promo
- Track promo usage

## Contract Price Violation Tracking

### Contract Price Violation DocType

```python
# Contract Price Violation DocType
# Fields
- violation_date (Date, required)
- company (Link: Company, required)
- vendor (Link: Vendor, required)
- product (Link: Product, required)
- purchase_unit (Link: Purchase Unit, required)
- invoice_number (Data, required)
- contract_price (Currency, required)
- invoice_price (Currency, required)
- quantity (Float, required)
- variance_amount (Currency, calculated)  # invoice_price - contract_price
- variance_percent (Float, calculated)  # (variance_amount / contract_price) * 100
- status (Select: New, Reviewed, Resolved, Ignored)
- reviewed_by (Link: User)
- reviewed_at (Datetime)
- resolution_notes (Text)
```

### Automatic Violation Detection
When importing from Ottimate or processing invoices:
1. Check contract price for purchase unit
2. Compare invoice price to contract price
3. Create violation if invoice price > contract price
4. Calculate variance amount and percentage
5. Flag for review

## Cost Per Unit Calculation

### Cost Calculations
- Cost per primary unit
- Cost per volume unit
- Cost per weight unit
- Cost per purchase unit

### Example
```
Purchase: 1 case = $12.95 = 24 each
├── Cost per each: $12.95 / 24 = $0.5396
├── Cost per fl_oz: $0.5396 / 12 = $0.045
├── Cost per gallon: $0.045 * 128 = $5.76
├── Cost per gram: $0.5396 / 360 = $0.0015
└── Cost per lb: $0.0015 * 453.592 = $0.68
```

## Implementation Steps

### Step 1: Add Pricing Fields to Purchase Unit
1. Add contract_price field
2. Add price field (current price)
3. Add price history tracking

### Step 2: Create Contract Price Violation DocType
1. Create `Contract Price Violation` DocType
2. Add violation tracking fields
3. Add status and resolution fields

### Step 3: Create Promo Threshold DocType
1. Create `Promo Threshold` DocType
2. Add threshold configuration fields
3. Add promo price fields

### Step 4: Implement Violation Detection
1. Implement violation checking logic
2. Auto-create violations on invoice import
3. Calculate variance amounts
4. Generate violation reports

### Step 5: Implement Promo Checking
1. Implement threshold checking logic
2. Auto-apply promo pricing
3. Calculate promo savings
4. Track promo usage

## Dependencies

- **Product DocType**: For product references
- **Purchase Unit DocType**: For pricing information
- **Vendor DocType**: For vendor references
- **Vendor Invoice DocType**: For price violation detection

## Usage Examples

### Contract Price Violation
```
Violation:
  - Vendor: "Sysco"
  - Product: "Coca Cola Cans"
  - Contract Price: $12.95
  - Invoice Price: $13.50
  - Variance: $0.55 (4.25%)
  - Status: "New"
```

### Promo Threshold
```
Promo Threshold:
  - Vendor: "Sysco"
  - Product: "Chicken Breast"
  - Threshold Type: "Quantity"
  - Quantity Threshold: 100 lb
  - Promo Price: $2.50/lb
  - Regular Price: $2.75/lb
  - Discount: 9.09%
```

## Testing Checklist

- [ ] Track contract prices
- [ ] Detect price violations
- [ ] Calculate variance amounts
- [ ] Create promo thresholds
- [ ] Check promo thresholds
- [ ] Auto-apply promo pricing
- [ ] Calculate cost per unit
- [ ] Generate violation reports
- [ ] Track price history

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Sections 23.9, 23.10

