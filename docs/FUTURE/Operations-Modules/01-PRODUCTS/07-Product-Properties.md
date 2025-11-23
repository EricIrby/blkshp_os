# Product Properties

## Overview

Product Properties define special characteristics of products, such as whether they are generic items, non-inventory items, or prep items. These properties affect how products are managed, tracked, and used in the system.

## Purpose

- Identify generic items (interchangeable products)
- Identify non-inventory items (not tracked in inventory)
- Identify prep items (manufactured/prepared items)
- Support linked items (related products)
- Enable special handling for different product types

## Product Property Types

### Generic Items

Generic items are products that are interchangeable with other products. For example, "Chicken Breast - Generic" can be used in recipes instead of specific vendor items.

**Characteristics:**
- Can be used as substitutes
- Not typically purchased directly
- Used in recipes and cost calculations
- Can have multiple vendor-specific variants

**Use Cases:**
- Recipe costing with generic ingredients
- Menu planning with generic products
- Cost analysis with generic items

### Non-Inventory Items

Non-inventory items are products that are not tracked in inventory. These items are typically:
- Services (e.g., delivery fees)
- Consumables (e.g., cleaning supplies that are expensed)
- Equipment (e.g., kitchen equipment)
- Retail products (e.g., merchandise for sale)

**Characteristics:**
- Not counted in audits
- Not included in inventory reports
- Can be ordered but not tracked
- Expensed rather than inventoried

**Use Cases:**
- Ordering non-inventory supplies
- Tracking expenses for non-inventory items
- Reporting on non-inventory purchases

### Prep Items

Prep items are products that are manufactured or prepared from other products (ingredients). They are created through batch production.

**Characteristics:**
- Created from recipes
- Produced in batches
- Tracked in inventory
- Consume ingredients when produced
- Have yield (recipe output quantity)

**Use Cases:**
- Batch production tracking
- Prep item inventory management
- Recipe costing for prep items
- Inventory audits of prep items

### Linked Items

Linked items are products that are related to other products. They can be:
- Substitutes (alternative products)
- Related products (complementary items)
- Variants (size, flavor variants)

**Characteristics:**
- Linked to parent product
- Can be used as substitutes
- Share some properties with parent
- Can have independent pricing

## DocType Definition

### Product DocType Properties

```python
# Product Properties Fields
- is_generic (Check)  # Generic item flag
- is_non_inventory (Check)  # Non-inventory item flag
- is_prep_item (Check)  # Prep item flag
- linked_product (Link: Product)  # Linked/parent product
- substitute_items (Table: Substitute Item)  # Substitute products
```

### Substitute Item DocType (Child Table)

```python
# Substitute Item
- parent (Link: Product)
- substitute_product (Link: Product, required)
- priority (Int)  # Priority for substitution
- is_preferred (Check)  # Preferred substitute
```

## Implementation Steps

### Step 1: Add Property Flags
1. Add is_generic checkbox to Product DocType
2. Add is_non_inventory checkbox to Product DocType
3. Add is_prep_item checkbox to Product DocType
4. Add linked_product link to Product DocType

### Step 2: Add Substitute Items
1. Create `Substitute Item` child table DocType
2. Add to Product DocType
3. Add priority and is_preferred fields

### Step 3: Implement Validation
1. Validate property combinations (e.g., can't be generic and prep item)
2. Validate linked product relationships
3. Validate substitute item relationships

### Step 4: Update Related Systems
1. Update inventory tracking to skip non-inventory items
2. Update audit system to handle prep items
3. Update recipe system to support generic items
4. Update ordering system to handle non-inventory items

## Dependencies

- **Product DocType**: Base DocType for properties
- **Recipe DocType**: For prep items (from Recipes domain)
- **Batch DocType**: For prep item production (from Recipes domain)

## Usage Examples

### Generic Item
```
Product: "Chicken Breast - Generic"
├── is_generic: Yes
├── Used in recipes
└── Can be substituted with vendor-specific items

Recipe: "Grilled Chicken"
└── Ingredient: "Chicken Breast - Generic"
    └── Can use any vendor's chicken breast
```

### Non-Inventory Item
```
Product: "Delivery Fee"
├── is_non_inventory: Yes
├── Not counted in audits
├── Not included in inventory reports
└── Expensed when ordered
```

### Prep Item
```
Product: "Pizza Dough"
├── is_prep_item: Yes
├── Created from recipe
├── Produced in batches
└── Consumes ingredients (flour, yeast, water)

Recipe: "Pizza Dough Recipe"
└── Ingredients: Flour, Yeast, Water, Salt
    └── Yield: 5 lb dough
```

### Linked Items
```
Product: "Coca Cola - 12oz Can"
├── linked_product: None
└── substitute_items:
    - Coca Cola - 20oz Bottle
    - Pepsi - 12oz Can
    - Sprite - 12oz Can
```

## Testing Checklist

- [ ] Create generic item
- [ ] Create non-inventory item
- [ ] Create prep item
- [ ] Test property combinations
- [ ] Test linked product relationships
- [ ] Test substitute items
- [ ] Verify non-inventory items excluded from audits
- [ ] Verify prep items included in audits
- [ ] Test generic items in recipes

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md

