# Department Settings

## Overview

Department Settings configure default values and department-level configurations that apply to products, inventory, and operations within a department. These settings serve as defaults that can be overridden at the product-department level.

## Purpose

- Set department-level default storage areas
- Set department-level default GL codes
- Configure department-specific operational settings
- Provide extensible configuration via JSON settings field
- Establish defaults for products assigned to the department

## DocType Definition

### Department Settings (Fields on Department DocType)

Department Settings are stored as fields directly on the `Department` DocType:

```python
# Department-Level Default Settings
- default_storage_area (Link: Storage Area)  # Default storage for department
- default_gl_code (Link: Account)  # Default GL code for department
- settings (JSON)  # Extensible department-specific settings
```

### Settings JSON Structure

The `settings` JSON field can contain extensible department-specific configuration:

```json
{
  "eoq_enabled": true,
  "eoq_calculation_method": "standard",
  "reorder_point_buffer": 0.2,
  "default_ordering_day": "monday",
  "allow_inter_department_transfers": true,
  "require_approval_for_transfers": false,
  "inventory_count_frequency": "monthly",
  "minimum_order_amount": 0.00,
  "budget_alert_threshold": 0.90,
  "custom_settings": {}
}
```

## Key Features

### Default Storage Area

- **Purpose**: Sets the default storage area for products in this department
- **Usage**: Used when assigning products to departments if no specific storage is set
- **Override**: Can be overridden at product-department level (Product Department child table)
- **Impact**: Helps organize inventory counting and storage location tracking

### Default GL Code

- **Purpose**: Sets the default general ledger code for products in this department
- **Usage**: Used for accounting integration when no product-department-specific GL code is set
- **Override**: Can be overridden at product-department level or product level
- **Impact**: Affects financial reporting and accounting system sync

### Settings JSON Field

- **Purpose**: Extensible configuration for department-specific behavior
- **Usage**: Stores additional settings not covered by standard fields
- **Examples**: EOQ settings, reorder points, ordering schedules, transfer policies
- **Extensibility**: Can be extended without schema changes

### Hierarchy of Settings

Settings follow a hierarchy with more specific settings overriding general ones:

```
1. Product-Department Level (Product Department child table)
   - Most specific, overrides all defaults
   - par_level, order_quantity, default_storage_area per product-department

2. Department Level (Department Settings)
   - Default values for department
   - default_storage_area, default_gl_code

3. Product Level (Product DocType)
   - Product-wide defaults
   - Preferred vendor, preferred purchase unit
```

## Implementation Steps

### Step 1: Add Settings Fields to Department DocType

1. Add `default_storage_area` field (Link: Storage Area)
   - Optional field
   - Filters by company
   - Shows only active storage areas

2. Add `default_gl_code` field (Link: Account)
   - Optional field
   - Filters by company
   - Shows only active accounts

3. Add `settings` field (JSON)
   - Long text field with JSON format
   - Validate JSON syntax on save
   - Provide UI for common settings

### Step 2: Implement Default Value Logic

1. Create method to get default storage area for department
2. Create method to get default GL code for department
3. Apply defaults when creating product-department allocations
4. Allow overrides at product-department level

### Step 3: Add Settings UI Components

1. Add section to Department form for settings
2. Create settings form with common fields
3. Store settings in JSON format
4. Provide JSON editor for advanced settings

### Step 4: Implement Settings Helpers

1. Create helper methods to read settings JSON
2. Create validation for settings values
3. Provide default values for missing settings
4. Document available settings options

## Settings Options

### EOQ (Economic Order Quantity) Settings

```json
{
  "eoq_enabled": true,
  "eoq_calculation_method": "standard",
  "eoq_safety_stock_factor": 1.5
}
```

- **eoq_enabled**: Enable EOQ calculations for this department
- **eoq_calculation_method**: Method for EOQ calculation (standard, modified, custom)
- **eoq_safety_stock_factor**: Multiplier for safety stock in EOQ calculations

### Reorder Point Settings

```json
{
  "reorder_point_buffer": 0.2,
  "reorder_point_method": "par_level_based"
}
```

- **reorder_point_buffer**: Percentage buffer above par level for reorder point
- **reorder_point_method**: How to calculate reorder point (par_level_based, usage_based, custom)

### Ordering Settings

```json
{
  "default_ordering_day": "monday",
  "minimum_order_amount": 500.00,
  "require_order_approval": false
}
```

- **default_ordering_day**: Default day of week for ordering
- **minimum_order_amount**: Minimum order amount for department
- **require_order_approval**: Require approval for orders

### Transfer Settings

```json
{
  "allow_inter_department_transfers": true,
  "require_approval_for_transfers": false,
  "transfer_approval_roles": ["Manager"]
}
```

- **allow_inter_department_transfers**: Allow transfers to/from other departments
- **require_approval_for_transfers**: Require approval for transfers
- **transfer_approval_roles**: Roles that can approve transfers

### Inventory Settings

```json
{
  "inventory_count_frequency": "monthly",
  "require_count_approval": true,
  "variance_threshold": 0.05
}
```

- **inventory_count_frequency**: How often to perform inventory counts
- **require_count_approval**: Require approval for inventory counts
- **variance_threshold**: Variance threshold for flagging discrepancies

### Budget Settings

```json
{
  "budget_alert_threshold": 0.90,
  "budget_alert_frequency": "weekly",
  "budget_fiscal_year": "calendar"
}
```

- **budget_alert_threshold**: Percentage of budget spent before alert
- **budget_alert_frequency**: How often to check budget alerts
- **budget_fiscal_year**: Fiscal year definition (calendar, custom)

## Dependencies

- **Department DocType**: Parent DocType (from Departments domain)
- **Storage Area DocType**: For default storage assignment (from Inventory domain)
- **Account DocType**: For default GL code (from Accounting/ERPNext)

## Usage Examples

### Basic Department Settings

```
Department: "Kitchen"
Settings:
  - Default Storage Area: "Main Kitchen Storage"
  - Default GL Code: "4100 - Food Cost"
  - Settings JSON: {
      "eoq_enabled": true,
      "default_ordering_day": "monday",
      "minimum_order_amount": 500.00
    }
```

### Product Assignment with Defaults

```
Product: "Chicken Breast"
Assigned to: "Kitchen" Department

Department Settings Applied:
  - Default Storage: "Main Kitchen Storage" (from department)
  - Default GL Code: "4100 - Food Cost" (from department)

Product-Department Overrides:
  - Par Level: 20 (specific to this product in Kitchen)
  - Order Quantity: 40 (specific to this product in Kitchen)
  - Storage: "Meat Cooler" (overrides department default)
```

### Settings Hierarchy Example

```
1. Department: "Kitchen"
   - Default Storage: "Main Kitchen Storage"
   - Default GL Code: "4100 - Food Cost"

2. Product: "Chicken Breast" → Kitchen Department
   - Storage: "Meat Cooler" (overrides department default)
   - GL Code: "4100 - Food Cost" (uses department default)
   - Par Level: 20 (product-department specific)

3. Product: "Lettuce" → Kitchen Department
   - Storage: "Main Kitchen Storage" (uses department default)
   - GL Code: "4100 - Food Cost" (uses department default)
   - Par Level: 15 (product-department specific)
```

## Methods

### Get Default Storage Area

```python
def get_default_storage_area(department):
    """Get default storage area for department"""
    dept = frappe.get_doc('Department', department)
    return dept.default_storage_area
```

### Get Default GL Code

```python
def get_default_gl_code(department):
    """Get default GL code for department"""
    dept = frappe.get_doc('Department', department)
    return dept.default_gl_code
```

### Get Setting Value

```python
def get_department_setting(department, setting_key, default_value=None):
    """Get specific setting value from department settings JSON"""
    dept = frappe.get_doc('Department', department)
    settings = json.loads(dept.settings) if dept.settings else {}
    return settings.get(setting_key, default_value)
```

### Apply Defaults to Product-Department

```python
def apply_department_defaults(product, department):
    """Apply department defaults when assigning product to department"""
    dept = frappe.get_doc('Department', department)
    
    # Get or create Product Department record
    product_dept = get_or_create_product_department(product, department)
    
    # Apply defaults if not already set
    if not product_dept.default_storage_area and dept.default_storage_area:
        product_dept.default_storage_area = dept.default_storage_area
    
    product_dept.save()
```

## Testing Checklist

- [ ] Set default storage area on department
- [ ] Set default GL code on department
- [ ] Verify defaults apply when assigning products to department
- [ ] Verify product-department settings override department defaults
- [ ] Test settings JSON field with valid JSON
- [ ] Test settings JSON field with invalid JSON (should error)
- [ ] Verify settings helpers return correct values
- [ ] Test settings hierarchy (product-department > department > product)
- [ ] Test EOQ settings application
- [ ] Test reorder point settings application
- [ ] Test ordering settings application
- [ ] Test transfer settings application
- [ ] Test inventory settings application
- [ ] Test budget settings application

## Related Documentation

- **01-Department-Master.md**: Department DocType definition
- **04-Department-Allocations.md**: Product-department allocations with overrides
- **03-INVENTORY/08-Storage-Areas.md**: Storage area management
- **07-ACCOUNTING/05-GL-Code-Mapping.md**: GL code mapping

---

**Status**: ✅ Created to complete Departments domain documentation

