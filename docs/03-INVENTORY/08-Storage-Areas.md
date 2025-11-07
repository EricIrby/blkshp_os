# Storage Areas

## Overview

Storage Areas define physical storage locations for inventory. Storage is tracked as metadata only and does not create separate inventory buckets. All inventory is tracked at the Product + Department level (2D model).

## Purpose

- Define physical storage locations
- Assign default departments to storage areas
- Organize counting tasks by storage
- Track where products are stored (metadata)
- Support storage-based reporting

## DocType Definition

### Storage Area DocType

```python
# Storage Area
- storage_name (Data, required)
- storage_code (Data, unique)
- company (Link: Company, required)
- default_department (Link: Department, required)  # Default department for this storage
- description (Text)
- is_active (Check)
- location_type (Select: Stockroom, Room, Vehicle, etc.)  # Optional classification
```

### Methods

```python
def get_default_department():
    """Return default department for this storage"""
    return self.default_department
```

## Key Features

### Storage as Metadata
- Storage location tracked but not part of inventory balance
- Inventory tracked at Product + Department level (2D model)
- Storage helps organize counting but doesn't affect inventory calculations

### Default Department Assignment
- Each storage has a default department
- Used for counting task assignments
- Can be overridden per product

### Storage Organization
- Organize storage by type (Stockroom, Room, Vehicle)
- Support multiple storage areas per company
- Track active/inactive storage areas

## Implementation Steps

### Step 1: Create Storage Area DocType
1. Create `Storage Area` DocType
2. Add storage_name field (required)
3. Add storage_code field (unique)
4. Add company link (required)

### Step 2: Add Department Assignment
1. Add default_department field (required)
2. Link to Department DocType
3. Implement get_default_department() method

### Step 3: Add Organization Fields
1. Add description field
2. Add is_active checkbox
3. Add location_type field (optional)

### Step 4: Integrate with Counting Tasks
1. Use storage areas in counting task creation
2. Group tasks by storage area
3. Display storage in audit lines

## Dependencies

- **Company DocType**: Company reference (Frappe built-in)
- **Department DocType**: Default department assignment

## Usage Examples

### Storage Area Setup
```
Storage Area: "Main Cooler"
├── Storage Code: "MAIN-COOLER"
├── Company: "Store 1"
├── Default Department: "Kitchen"
├── Location Type: "Stockroom"
└── Description: "Main walk-in cooler"

Storage Area: "Bar Cooler"
├── Storage Code: "BAR-COOLER"
├── Company: "Store 1"
├── Default Department: "Beverage"
├── Location Type: "Stockroom"
└── Description: "Bar beverage cooler"
```

### Storage in Counting Tasks
```
Counting Task: "Kitchen - Main Cooler"
├── Department: Kitchen
├── Storage: Main Cooler
└── Categories: All categories

Counting Task: "Beverage - Bar Cooler"
├── Department: Beverage
├── Storage: Bar Cooler
└── Categories: Beer, Wine, Spirits
```

## Testing Checklist

- [ ] Create storage area
- [ ] Verify storage code uniqueness
- [ ] Assign default department
- [ ] Test storage in counting tasks
- [ ] Verify storage in audit lines
- [ ] Test storage filtering
- [ ] Deactivate storage area
- [ ] Verify storage organization

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

