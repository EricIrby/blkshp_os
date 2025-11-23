# Recipe Master

## Overview

The Recipe DocType stores the authoritative definition for menu items, prep items, and beverage builds. Each recipe keeps a list of ingredients, calculates the extended cost for every row, and rolls the totals into `total_cost` and `cost_per_unit`. Subrecipes are supported by referencing other `Recipe` documents as ingredients.

## Key Fields

- `recipe_name` – Display name of the recipe (title field)
- `recipe_code` – Unique code generated automatically (`RECIPE-.#####`)
- `recipe_type` – Food, Beverage, or Prep
- `company` – Auto-populated from the owning department (enforced)
- `department` – Owning department (required)
- `yield_quantity` / `yield_unit` – Expected output of the recipe
- `ingredients` – Child table (`Recipe Ingredient`)
- `allergens` – Manual allergen tags (`Recipe Allergen`)
- `inherited_allergens` – Read-only allergen list propagated from subrecipes
- `total_cost` – Sum of ingredient costs
- `cost_per_unit` – `total_cost / yield_quantity`

### Recipe Ingredient Child Table

- `ingredient_type` – `Product` or `Recipe`
- `product` – Link to `Product` when `ingredient_type` is `Product`
- `subrecipe` – Link to `Recipe` when `ingredient_type` is `Recipe`
- `quantity` / `unit` – Quantity used and the unit entered by the user
- `cost_per_unit` – Required for product ingredients; optional for subrecipes
- `cost_total` – Calculated row cost (read-only)
- `base_quantity` – Quantity normalized to the product's primary count unit

### Recipe Allergen Child Tables

- `Recipe Allergen` – Manual allergen selections added by the author
- `Recipe Inherited Allergen` – Read-only list of allergens inherited from nested subrecipes (with source recipe references)

## Behaviour

- Cost calculations run during `validate`
- Recipe company is enforced to match the owning department's company
- Product and subrecipe ingredients must belong to the same department/company as the recipe
- Product ingredient quantities are converted to the product's primary count unit
- Subrecipe costs use the referenced recipe's `cost_per_unit`
- Saving a subrecipe automatically recalculates any parent recipes that reference it
- Allergens propagate automatically from subrecipes; duplicates are rejected
- Recipe yield must be greater than zero

## Testing Checklist

- [x] Cost calculation for product ingredients
- [x] Cost calculation for subrecipe ingredients
- [x] Parent recipes refresh when a subrecipe changes
- [x] Department/company alignment validation
- [x] Allergen propagation from subrecipes

---

**Status**: ✅ Implemented in code and covered by automated tests.

