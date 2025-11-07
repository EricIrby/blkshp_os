# POS Item Mapping

## Overview

POS Item Mapping maps POS system items to BLKSHP recipes. Mappings are instance-specific, allowing the same POS item to map to different recipes per department/instance.

## Purpose

- Map POS items to recipes
- Support instance-specific mappings
- Enable automatic recipe lookup
- Track mapping usage
- Support bulk mapping operations

## DocType Definition

### POS Item Mapping DocType

```python
# POS Item Mapping DocType
# Fields
- pos_item_id (Data, required)  # Item ID from POS system
- pos_item_name (Data, required)  # Item name from POS
- pos_instance (Link: POS Instance, required)  # POS instance (replaces pos_system)
- pos_system (Select: Toast, Square, Clover, Resy, Custom)  # Derived from instance
- blkshp_recipe (Link: Recipe, required)  # Mapped recipe
- department (Link: Department, required)  # Department where item is sold
- is_active (Check, default=1)
- mapping_created_at (Datetime)
- mapping_created_by (Link: User)
- last_sale_date (Datetime)  # Last time this mapping was used
- usage_count (Int, default=0)  # How many times mapping used

# Methods
def update_usage():
    """Update usage statistics when mapping is used"""
    pass
```

## Key Features

### Instance-Based Mapping
- Mappings tied to specific POS instance
- Same POS item ID can map differently per instance
- Supports multiple departments per location

### Persistent Mapping
- Once mapped, POS items automatically use recipe
- No need to remap for each sale
- Mappings saved for future use

### Department-Specific
- Same POS item can map to different recipes by department
- Department auto-filled from instance (can override)
- Supports department-specific reporting

### Usage Tracking
- Tracks how often each mapping is used
- Last sale date tracking
- Helps identify unused mappings

### Auto-Mapping
- Suggests mappings based on name similarity
- Fuzzy matching for item names
- Bulk mapping support

## Implementation Steps

### Step 1: Create POS Item Mapping DocType
1. Create `POS Item Mapping` DocType
2. Add POS item fields (id, name)
3. Add pos_instance link (required)
4. Add blkshp_recipe link (required)

### Step 2: Add Mapping Fields
1. Add department field (required)
2. Add is_active checkbox
3. Add usage tracking fields
4. Add created/created_by fields

### Step 3: Implement Auto-Mapping
1. Implement name similarity matching
2. Suggest recipes based on name
3. Support fuzzy matching
4. Bulk mapping interface

### Step 4: Implement Usage Tracking
1. Update usage_count on sale
2. Update last_sale_date
3. Track mapping effectiveness

## Dependencies

- **POS Instance DocType**: Instance reference
- **Recipe DocType**: Recipe mapping (from Recipes domain)
- **Department DocType**: Department assignment

## Usage Examples

### Single Mapping
```
POS Item Mapping:
  - POS Item ID: "TOAST-12345"
  - POS Item Name: "Grilled Chicken"
  - POS Instance: "Restaurant Toast"
  - BLKSHP Recipe: "Grilled Chicken Recipe"
  - Department: "Kitchen"
  - Usage Count: 245
  - Last Sale Date: 2025-01-31
```

### Instance-Specific Mapping
```
Same POS Item, Different Instances:
  - POS Item ID: "TOAST-12345"
  
  Instance: "Restaurant Toast"
    - Recipe: "Grilled Chicken Recipe"
    - Department: "Kitchen"
  
  Instance: "Catering Toast"
    - Recipe: "Catering Chicken Recipe"
    - Department: "Catering"
```

## Testing Checklist

- [ ] Create POS item mapping
- [ ] Map POS item to recipe
- [ ] Test instance-specific mappings
- [ ] Test auto-mapping suggestions
- [ ] Bulk mapping operations
- [ ] Update usage tracking
- [ ] Query mappings by instance
- [ ] Query mappings by department
- [ ] Test inactive mappings

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 20.2

