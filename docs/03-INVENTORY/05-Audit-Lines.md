# Audit Lines

## Overview

Audit Lines record individual product counts during audits. Users can count in any available unit (primary, volume, weight), and counts are automatically converted to the product's primary count unit for storage.

## Purpose

- Record product counts during audits
- Support flexible unit selection (count in any unit)
- Convert counts to primary unit for storage
- Track who counted and when
- Calculate count values

## DocType Definition

### Audit Line DocType (Enhanced with Count Unit Selection)

```python
# Audit Line
- parent (Link: Inventory Audit)
- counting_task (Link: Counting Task)  # Which task this count belongs to
- product (Link: Product, required)
- storage_location (Link: Storage Area, required)  # WHERE counted (metadata)
- department (Link: Department, required)  # From task assignment
- count_unit (Select, required)  # User-selected count unit (each, fl_oz, gallon, grams, lb, etc.)
- count (Float, required)  # Count in selected unit
- count_in_primary (Float, calculated)  # Converted to product's primary count unit for storage
- cu_price (Currency)  # Price per primary count unit
- total_value (Currency, calculated)  # count_in_primary * cu_price
- counted_by (Link: User)
- counted_at (Datetime)
```

### Methods

```python
def calculate_primary_count():
    """Convert count to primary unit"""
    if self.count_unit == self.product.primary_count_unit:
        self.count_in_primary = self.count
    else:
        self.count_in_primary = self.product.convert_to_primary_unit(
            self.count_unit, 
            self.count
        )
```

## Key Features

### Flexible Unit Selection
- Count in any available unit (primary, volume, weight)
- Unit selection based on product's available units
- Supports user preference for counting

### Automatic Unit Conversion
- Counts automatically converted to primary unit
- Stored in primary unit for consistency
- Original count unit preserved for reference

### Value Calculation
- CU price from product or purchase unit
- Total value calculated (count_in_primary * cu_price)
- Supports audit value reporting

## Example

```
Audit Line:
├── Product: Coca Cola Cans
├── Count Unit: "gallon" (user selected)
├── Count: 2.5 gallons
├── Count in Primary: 26.67 each (calculated: 2.5 gal → 320 fl_oz → 26.67 each)
├── CU Price: $0.5396 per each
└── Total Value: $14.39 (26.67 * $0.5396)
```

## Conversion Flow

### User Counts in Selected Unit
1. User selects count unit (e.g., "gallon")
2. User enters count (e.g., 2.5)
3. System converts to primary unit (e.g., 26.67 each)
4. Count stored in primary unit

### Conversion Process
1. Get product's conversion factors
2. Convert from selected unit to primary unit
3. Handle standard unit conversions (gallons → fl_oz → each)
4. Store count_in_primary

## Implementation Steps

### Step 1: Create Audit Line Child Table
1. Create `Audit Line` child table DocType
2. Add parent link fields
3. Add product link (required)
4. Add department link (required)

### Step 2: Add Count Fields
1. Add count_unit field (Select, required)
2. Add count field (Float, required)
3. Add count_in_primary field (Float, calculated)
4. Populate count_unit options from product's available units

### Step 3: Add Value Fields
1. Add cu_price field (Currency)
2. Add total_value field (Currency, calculated)
3. Calculate from product or purchase unit price

### Step 4: Implement Conversion
1. Implement calculate_primary_count() method
2. Use product's convert_to_primary_unit() method
3. Handle unit conversion errors

### Step 5: Add Tracking Fields
1. Add counted_by field (Link: User)
2. Add counted_at field (Datetime)
3. Auto-populate on save

## Dependencies

- **Inventory Audit DocType**: Parent DocType
- **Counting Task DocType**: Task assignment
- **Product DocType**: Product reference and unit conversions
- **Department DocType**: Department assignment
- **Storage Area DocType**: Storage location (metadata)

## Usage Examples

### Count in Primary Unit
```
Audit Line:
  - Product: "Coca Cola Cans"
  - Count Unit: "each"
  - Count: 24
  - Count in Primary: 24 each
```

### Count in Volume Unit
```
Audit Line:
  - Product: "Coca Cola Cans"
  - Count Unit: "gallon"
  - Count: 2.5
  - Count in Primary: 26.67 each (converted)
```

### Count in Weight Unit
```
Audit Line:
  - Product: "Chicken Breast"
  - Count Unit: "lb"
  - Count: 40
  - Count in Primary: 40 lb (primary unit is lb)
```

## Testing Checklist

- [ ] Create audit line with primary unit
- [ ] Create audit line with volume unit
- [ ] Create audit line with weight unit
- [ ] Verify unit conversion to primary
- [ ] Verify count_in_primary calculation
- [ ] Verify value calculation
- [ ] Test with different count units
- [ ] Verify department assignment
- [ ] Track counted_by and counted_at

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

