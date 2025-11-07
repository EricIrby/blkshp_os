# Product Categories

## Overview

Product Categories provide a hierarchical organization system for products. Categories and subcategories help organize products for reporting, filtering, and management.

## Purpose

- Organize products hierarchically
- Enable category-based filtering and reporting
- Support category-specific configurations
- Enable bulk category operations

## DocType Definition

### Product Category DocType

```python
# Fields
- category_name (Data, required)
- category_code (Data, unique)
- parent_category (Link: Product Category)  # For subcategories
- category_type (Select: Food, Beverage, Supply, Equipment, Other)
- description (Text)
- is_active (Check)
- gl_code (Link: Account)  # Default GL code for category
- image (Attach Image)
```

## Key Features

### Hierarchical Structure
- Categories can have parent categories (subcategories)
- Supports multi-level hierarchy
- Enables category-based organization

### Category Types
- Categories can be typed (Food, Beverage, Supply, Equipment)
- Type helps with organization and filtering
- Can have default settings per type

### GL Code Mapping
- Categories can have default GL codes
- GL codes can be overridden at product level
- Supports department-specific GL codes

## Implementation Steps

### Step 1: Create Product Category DocType
1. Create `Product Category` DocType
2. Add category_name field (required)
3. Add category_code field (unique)
4. Add parent_category link (for hierarchy)

### Step 2: Add Category Properties
1. Add category_type field
2. Add description field
3. Add is_active checkbox
4. Add gl_code field

### Step 3: Add to Product DocType
1. Add category link to Product DocType
2. Add subcategory link to Product DocType
3. Add validation for category compatibility

### Step 4: Implement Category Methods
1. Implement get_products(category) method
2. Implement get_subcategories(category) method
3. Add category hierarchy validation

## Dependencies

- **Product DocType**: Products reference categories
- **Account DocType**: For GL code mapping (from Accounting/ERPNext)

## Usage Examples

### Category Hierarchy
```
Food
├── Produce
│   ├── Fresh Vegetables
│   └── Fresh Fruits
├── Meat & Seafood
│   ├── Beef
│   ├── Pork
│   └── Seafood
└── Dairy
    ├── Cheese
    └── Milk

Beverage
├── Beer
├── Wine
└── Spirits

Supplies
├── Cleaning Supplies
└── Paper Products
```

### Product Assignment
```
Product: "Romaine Lettuce"
├── Category: "Produce"
└── Subcategory: "Fresh Vegetables"

Product: "Ribeye Steak"
├── Category: "Meat & Seafood"
└── Subcategory: "Beef"
```

## Testing Checklist

- [ ] Create category with valid data
- [ ] Verify category code uniqueness
- [ ] Test parent category relationship
- [ ] Test category hierarchy
- [ ] Verify products can be assigned to categories
- [ ] Test category-based filtering
- [ ] Test category deactivation
- [ ] Verify GL code mapping

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md

