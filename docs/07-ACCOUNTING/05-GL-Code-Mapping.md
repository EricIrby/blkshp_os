# GL Code Mapping

## Overview

GL Code Mapping maps products and departments to General Ledger codes for accurate financial reporting and bill syncing to accounting systems.

## Purpose

- Map products to GL codes
- Map departments to GL codes
- Support product-department specific GL codes
- Enable accurate financial reporting
- Support bill syncing to accounting systems

## GL Code Mapping Structure

### Product-Department GL Mapping
- Each product-department combination can have specific GL code
- Default GL code from product category
- Override at product-department level
- Used for invoice line allocation

### Default GL Codes
- Product category default GL code
- Department default GL code
- Company default GL codes
- Hierarchy: Product-Department > Category > Department > Company

## Implementation

### GL Mapping DocType

```python
# GL Mapping DocType
# Fields
- mapping_name (Data, required)
- company (Link: Company, required)
- product (Link: Product, optional)  # Product-specific
- department (Link: Department, optional)  # Department-specific
- category (Link: Product Category, optional)  # Category-specific
- gl_code (Link: Account, required)
- is_active (Check, default=1)

# Methods
def get_gl_code(product, department):
    """Get GL code for product-department combination"""
    # Check product-department mapping first
    # Then check category mapping
    # Then check department default
    # Then check company default
    pass
```

## Implementation Steps

### Step 1: Create GL Mapping DocType
1. Create `GL Mapping` DocType
2. Add product, department, category fields
3. Add gl_code link (to Account DocType)
4. Add priority/hierarchy logic

### Step 2: Implement GL Code Lookup
1. Implement get_gl_code() method
2. Check product-department mapping
3. Fall back to category mapping
4. Fall back to department default

### Step 3: Integrate with Invoices
1. Auto-assign GL codes on invoice lines
2. Support manual override
3. Validate GL codes
4. Use in bill syncing

## Dependencies

- **Product DocType**: Product references
- **Department DocType**: Department references
- **Product Category DocType**: Category references
- **Account DocType**: GL code references (from ERPNext/Accounting)

## Usage Examples

### Product-Department GL Mapping
```
GL Mapping:
  - Product: "Coca Cola Cans"
  - Department: "Beverage"
  - GL Code: "4100 - Beverage COGS"
```

### Category Default GL Mapping
```
GL Mapping:
  - Category: "Beverages"
  - GL Code: "4100 - Beverage COGS"
  - Applies to all products in category
```

## Testing Checklist

- [ ] Create product-department GL mapping
- [ ] Create category GL mapping
- [ ] Test GL code lookup
- [ ] Verify hierarchy (product-department > category > department)
- [ ] Auto-assign GL codes on invoices
- [ ] Support manual override
- [ ] Validate GL codes

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md

