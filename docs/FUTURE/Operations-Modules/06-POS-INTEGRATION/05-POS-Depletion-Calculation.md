# POS Depletion Calculation

## Overview

POS Depletion Calculation automatically creates inventory depletions from POS sales based on recipe usage. Calculates ingredient consumption and creates depletion records.

## Purpose

- Calculate depletions from POS sales
- Use recipe ingredients for calculations
- Support unit conversions
- Create depletion records automatically
- Update theoretical inventory

## Calculation Process

### Process Flow
1. Get POS sales for period and department
2. For each sale, get mapped recipe
3. For each recipe ingredient:
   - Calculate ingredient quantity = sale quantity × ingredient quantity
   - Convert to ingredient's primary unit
   - Create depletion line
4. Group depletions by product and department
5. Create Depletion records
6. Post depletions to inventory

## Implementation

### Calculate POS Depletions Function

```python
def calculate_pos_depletions(company, department, date_from, date_to):
    """Calculate inventory depletions from POS sales for a department"""
    
    # Get all POS sales for period and department
    sales = get_pos_sales(company, department, date_from, date_to)
    
    for sale in sales:
        # Get mapped recipe and department
        mapping = get_pos_item_mapping(sale.pos_item_id, sale.pos_instance)
        
        if not mapping or not mapping.mapped_recipe:
            continue
        
        # Use department from mapping
        dept = mapping.mapped_department or department
        
        # Get recipe
        recipe = frappe.get_doc('Recipe', mapping.mapped_recipe)
        
        # Calculate depletions for each ingredient
        for ingredient in recipe.ingredients:
            # Get product to convert ingredient quantity to primary unit
            product = frappe.get_doc('Product', ingredient.product)
            
            # Convert ingredient quantity to product's primary unit
            ingredient_qty_in_primary = product.convert_to_primary_unit(
                ingredient.unit,
                ingredient.quantity
            )
            
            # Calculate depletion (sale quantity * ingredient quantity in primary)
            depletion_qty = sale.quantity * ingredient_qty_in_primary
            
            # Apply modifier adjustments if any
            if sale.modifiers:
                depletion_qty = apply_modifier_adjustments(
                    depletion_qty,
                    sale.modifiers,
                    recipe
                )
            
            # Create depletion for specific department (in primary unit)
            create_depletion(
                product=ingredient.product,
                quantity=depletion_qty,
                company=company,
                department=dept,
                depletion_date=sale.sale_date,
                depletion_type='Sold',
                source='POS Sale',
                source_reference=sale.name
            )
```

## Key Features

### Recipe-Based Calculation
- Uses recipe ingredients for depletion calculation
- Accounts for recipe yields
- Supports subrecipes

### Unit Conversion
- Converts ingredient quantities to primary units
- Handles all unit types (volume, weight, count)
- Accurate depletion quantities

### Modifier Adjustments
- Adjusts depletions based on POS modifiers
- Accounts for add-ons and substitutions
- Accurate ingredient tracking

### Department-Aware
- Depletions created for correct department
- Uses department from mapping
- Supports multi-department operations

## Implementation Steps

### Step 1: Implement Calculation Function
1. Create calculate_pos_depletions function
2. Get POS sales for period
3. Get recipe mappings
4. Calculate ingredient depletions

### Step 2: Handle Unit Conversions
1. Convert ingredient quantities to primary units
2. Calculate depletion quantities
3. Handle all unit types

### Step 3: Create Depletion Records
1. Group depletions by product/department
2. Create Depletion records
3. Post depletions to inventory

## Dependencies

- **POS Sale DocType**: Sales data
- **POS Item Mapping DocType**: Recipe mappings
- **Recipe DocType**: Recipe ingredients
- **Product DocType**: Unit conversions
- **Depletion DocType**: Depletion records

## Usage Examples

### Single Sale Depletion
```
POS Sale:
  - Item: "Grilled Chicken"
  - Quantity: 5
  - Recipe: "Grilled Chicken Recipe"
  
Depletions Created:
  - Chicken Breast: 5 lb
  - Olive Oil: 0.25 cup
  - Salt: 0.05 lb
  - Pepper: 0.02 lb
```

## Testing Checklist

- [ ] Calculate depletions from POS sales
- [ ] Use recipe ingredients
- [ ] Convert units correctly
- [ ] Handle modifier adjustments
- [ ] Create depletion records
- [ ] Update inventory balances
- [ ] Support multiple departments
- [ ] Handle unmapped items

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 8.5, 20.3

