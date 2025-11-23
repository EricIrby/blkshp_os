# Purchase Units

## Overview

Purchase Units define vendor-specific purchase units for products. Each purchase unit specifies how the vendor packages the product and how it converts to the product's primary count unit.

## Purpose

- Define vendor-specific packaging (e.g., "24x1each" case)
- Convert purchase quantities to primary count units
- Calculate cost per primary unit
- Support multiple vendors per product
- Track contract prices and pricing

## DocType Definition

### Fields

```python
# Core Fields
- product (Link: Product, required)
- vendor (Link: Vendor, required)
- pack_size_description (Data, required)  # e.g., "24x1each"
- vendor_sku (Data)
- price (Currency)
- contract_price (Currency)
- conversion_to_primary_cu (Float, required)  # Converts to product's primary count unit
- minimum_order_qty (Float)
- is_preferred (Check)
- active (Check)
```

### Methods

```python
def calculate_primary_quantity(pu_quantity, conversion_factor):
    """Convert PU quantity to product's primary count unit"""
    return pu_quantity * conversion_factor

def get_cost_per_primary_unit(pu_price, conversion_factor):
    """Calculate cost per primary unit"""
    return pu_price / conversion_factor
```

## Example

```
Purchase Unit: "Coca Cola Cans - Case"
├── Product: Coca Cola Cans
├── Vendor: Sysco
├── Pack Size: "24x1each"
├── Price: $12.95
└── Conversion to Primary: 24 each per case
    └── Cost per each: $12.95 / 24 = $0.5396 per can
    └── Cost per fl_oz: $0.5396 / 12 = $0.045 per fl_oz
    └── Cost per gallon: $0.045 * 128 = $5.76 per gallon
    └── Cost per gram: $0.5396 / 360 = $0.0015 per gram
    └── Cost per lb: $0.0015 * 453.592 = $0.68 per lb
```

## Key Features

### Vendor-Specific Packaging
- Each vendor can have different packaging
- Pack size description describes the packaging
- Vendor SKU tracks vendor's item identifier

### Price Tracking
- **Price**: Current price from vendor
- **Contract Price**: Contracted price (for violation tracking)
- Both prices tracked for comparison

### Conversion to Primary Unit
- All purchase units convert to product's primary count unit
- Enables consistent inventory tracking
- Supports cost calculations across units

### Preferred Purchase Unit
- Mark one purchase unit as preferred per vendor
- Used for default ordering
- Product can have preferred vendor and preferred purchase unit

## Implementation Steps

### Step 1: Create Purchase Unit DocType
1. Create `Purchase Unit` DocType
2. Add product and vendor links (required)
3. Add pack size description field
4. Add conversion factor field (required)

### Step 2: Add Pricing Fields
1. Add price field
2. Add contract_price field
3. Add minimum_order_qty field
4. Add is_preferred checkbox

### Step 3: Implement Conversion Methods
1. Implement calculate_primary_quantity method
2. Implement get_cost_per_primary_unit method
3. Add validation for conversion_factor > 0

### Step 4: Add to Product DocType
1. Add purchase_units table to Product DocType
2. Link to preferred_purchase_unit field
3. Add validation for preferred purchase unit

## Dependencies

- **Product DocType**: Required parent
- **Vendor DocType**: Required vendor link (from Procurement domain)

## Usage Examples

### Single Purchase Unit
```
Product: "Coca Cola Cans"
Purchase Units:
  - Vendor: "Sysco"
    Pack Size: "24x1each"
    Conversion: 24 each
    Price: $12.95
    Preferred: Yes
```

### Multiple Purchase Units
```
Product: "Chicken Breast"
Purchase Units:
  - Vendor: "Sysco"
    Pack Size: "40 lb case"
    Conversion: 40 lb
    Price: $89.95
    Preferred: Yes
  - Vendor: "US Foods"
    Pack Size: "40 lb case"
    Conversion: 40 lb
    Price: $87.50
    Preferred: No
```

## Testing Checklist

- [ ] Create purchase unit with valid data
- [ ] Verify conversion to primary unit works
- [ ] Test cost per primary unit calculation
- [ ] Test multiple purchase units per product
- [ ] Test preferred purchase unit selection
- [ ] Verify contract price tracking
- [ ] Test minimum order quantity validation

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

