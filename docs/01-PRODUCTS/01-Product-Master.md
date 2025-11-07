# Product Master

## Overview

The Product DocType is the unified product/item master that manages all products (food, beverage, supplies, equipment) in a single system. Unlike Craftable's separate platforms, BLKSHP uses one unified product master with department-based segmentation.

## Purpose

- Single source of truth for all products
- Support all product types (food, beverage, supplies, equipment)
- Enable department-based organization
- Support flexible unit conversions
- Integrate with inventory, procurement, and recipes

## DocType Definition

### Fields

```python
# Core Fields
- product_name (Data, required)
- product_code (Data, unique, auto-generated)
- category (Link: Product Category)
- subcategory (Link: Product Category)
- product_type (Select: Food, Beverage, Supply, Equipment, Other)
- departments (Table: Product Department)  # Many-to-many relationship

# Count Unit System (Hub-and-Spoke Model)
- primary_count_unit (Select: each, lb, oz, case, bottle, etc., required)
- volume_conversion_unit (Select: fl_oz, ml, l, gallon, quart, pint)  # Optional
- volume_conversion_factor (Float)  # 1 primary_unit = X volume_unit
- weight_conversion_unit (Select: lb, oz, g, kg)  # Optional
- weight_conversion_factor (Float)  # 1 primary_unit = X weight_unit

# Storage and Organization
- storage_areas (Table: Product Storage Area)
- bin_location (Data)
- default_department (Link: Department)  # Primary department
- par_levels (Table: Department Par Level)  # Par level per department
- order_quantity (Float)

# Purchase and Vendor
- preferred_vendor (Link: Vendor)
- preferred_purchase_unit (Link: Purchase Unit)

# Product Properties
- is_generic (Check)
- is_non_inventory (Check)
- is_prep_item (Check)
- tags (Table: Product Tag)
- gl_code (Link: Account)
- image (Attach Image)
- active (Check)
```

### Methods

```python
def calculate_theoretical_inventory(product, company, department, date):
    """
    Calculate theoretical inventory for product in department (2D model)
    Storage location is metadata only - not part of calculation
    All counts stored in primary count unit
    """
    # Starting inventory from last audit (sum across all storages for department)
    # + Received from invoices (allocated to this department)
    # + Transferred in (to this department)
    # - Transferred out (from this department)
    # - Depleted (sold, spilled, manual) in this department
    pass

def get_available_count_units(product):
    """Get all count units available for this product"""
    units = [self.primary_count_unit]
    
    if self.volume_conversion_unit:
        units.append(self.volume_conversion_unit)
        # Standard volume conversions available: gallon, quart, pint, ml, l
    
    if self.weight_conversion_unit:
        units.append(self.weight_conversion_unit)
        # Standard weight conversions available: lb, oz, kg
    
    return units

def convert_to_primary_unit(product, from_unit, quantity):
    """Convert any unit to primary unit (hub conversion)"""
    # If from purchase unit, use purchase unit conversion
    # If from volume unit, divide by volume_conversion_factor
    # If from weight unit, divide by weight_conversion_factor
    # Handle standard unit conversions (gallons→fl_oz, lb→oz, etc.)
    pass

def convert_from_primary_unit(product, to_unit, quantity):
    """Convert from primary unit to any unit"""
    # If to volume unit, multiply by volume_conversion_factor
    # If to weight unit, multiply by weight_conversion_factor
    # Handle standard unit conversions
    pass

def convert_between_units(product, from_unit, to_unit, quantity):
    """Convert between any two units via primary unit"""
    primary_qty = convert_to_primary_unit(product, from_unit, quantity)
    return convert_from_primary_unit(product, to_unit, primary_qty)

def get_purchase_units(product, vendor=None):
    """Get purchase units for product"""
    pass

def get_departments(product):
    """Get all departments this product belongs to"""
    pass

def assign_to_department(product, department):
    """Assign product to department"""
    pass
```

## Example Configuration

```
Product: "Coca Cola Cans"
├── Primary Count Unit: "each" (1 can)
├── Volume Conversion: 1 each = 12 fl_oz
├── Weight Conversion: 1 each = 360 grams
└── Purchase Unit: 1 case = 24 each (from Purchase Unit)

Available Count Units:
- each (primary)
- fl_oz, gallon, quart, pint, ml, l (volume)
- grams, lb, oz, kg (weight)
```

## Implementation Steps

### Step 1: Create Product DocType
1. Create `Product` DocType in Frappe
2. Add core fields (name, code, category, type)
3. Add department relationship (child table)
4. Add count unit fields

### Step 2: Add Count Unit System
1. Add primary_count_unit field (required)
2. Add volume conversion fields (optional)
3. Add weight conversion fields (optional)
4. Implement conversion methods

### Step 3: Add Storage and Organization
1. Add storage areas table
2. Add bin location field
3. Add default department field
4. Add par levels table

### Step 4: Add Product Properties
1. Add generic/non-inventory/prep item flags
2. Add tags table
3. Add GL code field
4. Add image field

### Step 5: Implement Methods
1. Implement conversion methods
2. Implement theoretical inventory calculation
3. Implement department assignment methods
4. Add validation rules

## Dependencies

- **Product Category DocType**: For category assignments
- **Department DocType**: For department assignments
- **Purchase Unit DocType**: For purchase unit definitions
- **Storage Area DocType**: For storage assignments (from Inventory domain)
- **Vendor DocType**: For preferred vendor (from Procurement domain)

## Testing Checklist

- [ ] Create product with valid data
- [ ] Verify product code auto-generation
- [ ] Test department assignments
- [ ] Test count unit conversions
- [ ] Test volume conversions
- [ ] Test weight conversions
- [ ] Verify purchase unit relationships
- [ ] Test product properties (generic, non-inventory, prep item)
- [ ] Verify theoretical inventory calculation

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

