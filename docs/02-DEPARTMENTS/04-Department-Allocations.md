# Department Allocations

## Overview

The Product Department DocType creates a many-to-many relationship between Products and Departments, allowing products to be assigned to multiple departments with department-specific settings.

## Purpose

- Assign products to one or more departments
- Set department-specific par levels
- Set department-specific order quantities
- Assign department-specific storage areas
- Mark primary department assignment

## DocType Definition

### Product Department DocType (Child Table)

```python
# Fields
- parent (Link: Product)
- parenttype (Data: "Product")
- parentfield (Data: "departments")
- department (Link: Department, required)
- is_primary (Check)  # Primary department assignment
- par_level (Float)  # Department-specific par level
- order_quantity (Float)  # Department-specific order quantity
- default_storage_area (Link: Storage Area)  # Department-specific storage
```

## Key Features

### Many-to-Many Relationship
- Products can belong to multiple departments
- Departments can have multiple products
- Maintained via child table on Product DocType

### Primary Department
- One department can be marked as primary
- Used for default assignments and reporting
- Helps with organization when product belongs to multiple departments

### Department-Specific Settings
- **Par Level**: Minimum inventory level per department
- **Order Quantity**: Suggested order quantity per department
- **Storage Area**: Default storage location per department

## Implementation Steps

### Step 1: Create Child Table DocType
1. Create `Product Department` as child table DocType
2. Add parent link fields (parent, parenttype, parentfield)
3. Add department link (required)
4. Add is_primary checkbox

### Step 2: Add Department-Specific Fields
1. Add par_level field (Float)
2. Add order_quantity field (Float)
3. Add default_storage_area field (Link to Storage Area)

### Step 3: Add to Product DocType
1. Add departments table field to Product DocType
2. Configure as child table
3. Set validation rules (at least one department, only one primary)

### Step 4: Implement Validation
1. Validate at least one department assigned
2. Validate only one primary department
3. Validate par_level and order_quantity are positive

## Dependencies

- **Product DocType**: Parent DocType (from Products domain)
- **Department DocType**: Department to assign (from Departments domain)
- **Storage Area DocType**: For default storage (from Inventory domain)

## Usage Examples

### Assign Product to Single Department
```
Product: "Coca Cola Cans"
Departments:
  - Department: "Beverage"
    Primary: Yes
    Par Level: 50
    Order Quantity: 100
```

### Assign Product to Multiple Departments
```
Product: "Chicken Breast"
Departments:
  - Department: "Kitchen"
    Primary: Yes
    Par Level: 20
    Order Quantity: 40
  - Department: "Catering"
    Primary: No
    Par Level: 10
    Order Quantity: 20
```

## Testing Checklist

- [ ] Assign product to single department
- [ ] Assign product to multiple departments
- [ ] Verify only one primary department allowed
- [ ] Test department-specific par levels
- [ ] Test department-specific order quantities
- [ ] Test department-specific storage areas
- [ ] Verify validation rules work correctly

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

