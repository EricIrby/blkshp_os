# Unit Conversion System

## Overview

The Unit Conversion System uses a **hub-and-spoke model** where the product's primary count unit is the hub, and all conversions flow through it. This enables flexible unit selection for counting, reporting, and calculations while maintaining consistent inventory tracking.

## Purpose

- Enable flexible unit selection (count in any available unit)
- Maintain consistent inventory tracking (all stored in primary unit)
- Support volume and weight conversions
- Support purchase unit conversions
- Enable cost calculations across units

## Hub-and-Spoke Model

### Conversion Structure

```
Product: "Coca Cola Cans"
├── Primary Count Unit: "each" (1 can) - HUB
├── Purchase Unit: 1 case = 24 each (from Purchase Unit)
├── Volume Conversion: 1 each = 12 fl_oz
└── Weight Conversion: 1 each = 360 grams

Available Count Units:
- each (primary) - HUB
- fl_oz, gallon, quart, pint, ml, l (volume conversions)
- grams, lb, oz, kg (weight conversions)
```

### Conversion Flow

All conversions go through the primary unit:
- **Any Unit → Primary Unit**: Convert to primary first
- **Primary Unit → Any Unit**: Convert from primary
- **Between Units**: Convert via primary (Any → Primary → Any)

## Cost Calculation Example

```
Purchase: 1 case = $12.95 = 24 each
├── Cost per each: $12.95 / 24 = $0.5396
├── Cost per fl_oz: $0.5396 / 12 = $0.045
├── Cost per gallon: $0.045 * 128 = $5.76
├── Cost per gram: $0.5396 / 360 = $0.0015
└── Cost per lb: $0.0015 * 453.592 = $0.68
```

## Conversion Functions

### convert_to_primary_unit()

Convert any unit to primary unit (hub conversion).

```python
def convert_to_primary_unit(product, from_unit, quantity):
    """
    Convert any unit to primary unit (hub conversion)
    
    Steps:
    1. If from purchase unit, use purchase unit conversion
    2. If from volume unit, divide by volume_conversion_factor
    3. If from weight unit, divide by weight_conversion_factor
    4. Handle standard unit conversions (gallons→fl_oz, lb→oz, etc.)
    """
    pass
```

**Examples:**
- 1 case → 24 each (via purchase unit conversion)
- 12 fl_oz → 1 each (via volume conversion: 12 / 12)
- 360 grams → 1 each (via weight conversion: 360 / 360)
- 1 gallon → 128 fl_oz → 10.67 each (via standard volume conversion)

### convert_from_primary_unit()

Convert primary unit to any unit.

```python
def convert_from_primary_unit(product, to_unit, quantity):
    """
    Convert from primary unit to any unit
    
    Steps:
    1. If to volume unit, multiply by volume_conversion_factor
    2. If to weight unit, multiply by weight_conversion_factor
    3. Handle standard unit conversions
    """
    pass
```

**Examples:**
- 24 each → 1 case (via purchase unit conversion)
- 1 each → 12 fl_oz (via volume conversion: 1 * 12)
- 1 each → 360 grams (via weight conversion: 1 * 360)
- 10.67 each → 128 fl_oz → 1 gallon (via standard volume conversion)

### convert_between_units()

Convert between any two units via primary unit.

```python
def convert_between_units(product, from_unit, to_unit, quantity):
    """
    Convert between any two units via primary unit (hub-and-spoke)
    
    Steps:
    1. Convert from_unit to primary: primary_qty = convert_to_primary_unit(from_unit, quantity)
    2. Convert primary to to_unit: result = convert_from_primary_unit(to_unit, primary_qty)
    """
    primary_qty = convert_to_primary_unit(product, from_unit, quantity)
    return convert_from_primary_unit(product, to_unit, primary_qty)
```

**Examples:**
- 1 gallon → each → 128 fl_oz (via primary unit)
- 1 lb → each → 453.592 grams (via primary unit)
- 1 case → each → 12 fl_oz (via primary unit)

## Standard Unit Conversions

The system handles standard conversions automatically:

### Volume Conversions
- 1 gallon = 128 fl_oz
- 1 quart = 32 fl_oz
- 1 pint = 16 fl_oz
- 1 liter = 33.814 fl_oz
- 1 ml = 0.033814 fl_oz

### Weight Conversions
- 1 lb = 16 oz
- 1 lb = 453.592 grams
- 1 kg = 1000 grams
- 1 kg = 2.20462 lb

## Implementation Steps

### Step 1: Define Conversion Structure
1. Identify primary count unit per product
2. Define volume conversion (if applicable)
3. Define weight conversion (if applicable)
4. Define purchase unit conversions

### Step 2: Implement Conversion Methods
1. Implement convert_to_primary_unit()
2. Implement convert_from_primary_unit()
3. Implement convert_between_units()
4. Add standard unit conversion handling

### Step 3: Add Validation
1. Validate conversion factors > 0
2. Validate unit compatibility
3. Handle edge cases (zero quantities, negative quantities)

### Step 4: Integration
1. Integrate with inventory counting
2. Integrate with cost calculations
3. Integrate with reporting
4. Add UI for unit selection

## Dependencies

- **Product DocType**: Defines primary unit and conversion factors
- **Purchase Unit DocType**: Defines purchase unit conversions

## Usage Examples

### Counting in Different Units
```
Audit Count:
  - Product: "Coca Cola Cans"
  - Count Unit: "case"
  - Count: 5 cases
  - Converted to Primary: 5 * 24 = 120 each
```

### Reporting in Different Units
```
Inventory Report:
  - Product: "Coca Cola Cans"
  - Quantity: 120 each
  - Display as: 120 each, 10 cases, 1440 fl_oz, 5 gallons
```

### Cost Calculations
```
Cost Analysis:
  - Product: "Coca Cola Cans"
  - Purchase: 1 case = $12.95
  - Cost per each: $0.5396
  - Cost per fl_oz: $0.045
  - Cost per gallon: $5.76
```

## Testing Checklist

- [ ] Test conversion to primary unit
- [ ] Test conversion from primary unit
- [ ] Test conversion between units
- [ ] Test purchase unit conversions
- [ ] Test volume conversions
- [ ] Test weight conversions
- [ ] Test standard unit conversions
- [ ] Test edge cases (zero, negative)
- [ ] Verify inventory tracking uses primary unit

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 8.2

