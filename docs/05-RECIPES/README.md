# Recipes Domain

## Overview

The Recipes domain manages recipe creation, costing, and batch production. Recipes drive POS depletion calculations and inventory management.

## Key Concepts

- **Recipe Costing**: Automatic cost calculation with unit conversions
- **Subrecipes**: Support for nested recipes
- **Prep Items**: Ingredients that are prepped/batched before use
- **Batch Management**: Track batch production and inventory impact
- **Department Assignment**: Recipes assigned to departments

## Dependencies

- **01-PRODUCTS**: Product/ingredient definitions required
- **02-DEPARTMENTS**: Department assignments
- **03-INVENTORY**: Batch production affects inventory

## Implementation Priority

**MEDIUM** - Required for POS depletion calculations

## Functions

1. ✅ **Recipe Master** - Recipe DocType, CRUD operations
2. ✅ **Recipe Ingredients** - Ingredient management, unit selection
3. ✅ **Recipe Costing** - Automatic cost calculation
4. ✅ **Subrecipes** - Subrecipe support, nested recipes
5. ✅ **Prep Items** - Prep item management
6. ✅ **Batch Management** - Batch production, tracking
7. ⏳ **Recipe Departments** - Recipe-to-department assignment
8. ⏳ **Recipe Allergens** - Allergen tracking, inherited allergens
9. ⏳ **Menu Lists** - Menu list grouping, management
10. ⏳ **Recipe Printing** - Recipe cards, menu list printing
11. ⏳ **Pours** - Beverage pour settings
12. ⏳ **Recipe Reprice** - Cost update tracking, reprice reports

## Status

✅ **Recipe Master + Batch Management implemented** – DocTypes, costing, and production flows shipped
⏳ **Remaining items** – Department assignment, allergens, menu lists, pours, repricing workflows

---

**Next Steps**: Finish department/allergen metadata, then plan menu lists, pours, and repricing workflows.

