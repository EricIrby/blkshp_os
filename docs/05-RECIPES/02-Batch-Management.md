# Recipe Batch Management

## Overview

`Recipe Batch` records each production run of a recipe and automatically applies the corresponding inventory movements. When a batch is submitted, raw ingredient balances are reduced and the finished good (recipe output product) is increased.

## Key Fields

- `recipe` – Recipe being produced (must be a prep item with an output product)
- `batch_date` – Production date (defaults to today)
- `department` / `company` – Derived from the recipe if not supplied
- `produced_quantity` / `produced_unit` – Yield produced by this batch
- `ingredients` – Child table mirroring the recipe's ingredients with actual usage entry

### Recipe Batch Ingredient Child Table

- `ingredient_type` – `Product` or `Recipe`
- `product` / `subrecipe` – Source reference depending on type
- `quantity_used` / `unit` – Actual quantity consumed (defaults to scaled recipe quantity)
- `base_quantity_used` – Quantity converted to the product's primary unit (read-only)
- `expected_base_quantity` – Target usage based on recipe scaling (read-only)
- `variance` – Difference between actual and expected quantities

## Behaviour

- Ingredient rows auto-populate from the recipe each time the batch is validated
- Expected usage is calculated by scaling recipe ingredient quantities to the batch's produced quantity
- Variance is kept in primary units for simple reporting
- On submission:
  - Product ingredients reduce `Inventory Balance` quantities
  - Subrecipe ingredients consume the subrecipe's output product
  - The recipe's output product receives the produced quantity

## Testing Checklist

- [x] Batch submission adjusts inventory balances for raw ingredients
- [x] Output product quantity increases by the produced yield
- [x] Overriding ingredient usage tracks variance and uses actual quantities for adjustments

---

**Status**: ✅ Implemented with automated tests.


