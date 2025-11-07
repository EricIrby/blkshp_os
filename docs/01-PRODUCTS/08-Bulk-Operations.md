# Bulk Operations

## Overview

Bulk Operations provide comprehensive import/export capabilities for products. This includes the Item Loader for bulk import and Excel/CSV export functionality.

## Purpose

- Import products in bulk from Excel/CSV files
- Export products to Excel/CSV
- Validate data during import
- Handle errors and provide detailed feedback
- Support create, update, and create-or-update operations

## Item Loader (Bulk Import)

### DocType Definition

```python
# Item Loader DocType
# Fields
- loader_name (Data, required)
- import_type (Select: Create New Items, Update Existing Items, Create or Update)
- file (Attach File, required)  # Excel or CSV file
- file_format (Select: Excel, CSV)  # Auto-detected
- company (Link: Company, required)  # For multi-company
- default_active (Check, default=1)  # Default active status for new items
- default_product_type (Select: Food, Beverage, Supply, Equipment, Other)
- default_category (Link: Product Category, optional)
- default_department (Link: Department, optional)  # Default department assignment

# Import Options
- skip_duplicates (Check)  # Skip items that already exist
- update_existing (Check)  # Update existing items if found
- validate_only (Check)  # Validate without importing
- create_departments (Check)  # Create departments if they don't exist
- create_categories (Check)  # Create categories if they don't exist
- create_vendors (Check)  # Create vendors if they don't exist

# Column Mapping
- column_mappings (Table: Column Mapping)  # Map file columns to Product fields

# Import Status
- status (Select: Draft, Validating, Validated, Importing, Completed, Failed)
- total_rows (Int, calculated)
- success_count (Int, calculated)
- error_count (Int, calculated)
- skipped_count (Int, calculated)
- validation_errors (Table: Validation Error)
- import_results (Table: Import Result)

# Processing
- started_at (Datetime)
- started_by (Link: User)
- completed_at (Datetime)
- completed_by (Link: User)
- error_log (Long Text)  # Detailed error log
```

### Column Mapping DocType (Child Table)

```python
# Column Mapping
- parent (Link: Item Loader)
- file_column (Data, required)  # Column name from file
- product_field (Select, required)  # Product field to map to
  # Options: product_name, product_code, category, subcategory, 
  #          primary_count_unit, volume_conversion_unit, weight_conversion_unit,
  #          preferred_vendor, default_department, etc.
- is_required (Check)
- default_value (Data)  # Default if column is empty
```

### Validation Error DocType (Child Table)

```python
# Validation Error
- parent (Link: Item Loader)
- row_number (Int, required)
- column_name (Data)
- error_message (Text, required)
- error_type (Select: Required Missing, Invalid Format, Duplicate, Invalid Reference)
- row_data (JSON)  # Full row data for reference
```

### Import Result DocType (Child Table)

```python
# Import Result
- parent (Link: Item Loader)
- row_number (Int, required)
- product_name (Data)
- product_code (Data)
- status (Select: Success, Error, Skipped)
- action (Select: Created, Updated, Skipped)
- product (Link: Product)  # Link to created/updated product
- error_message (Text)
- row_data (JSON)
```

## Excel/CSV File Template

### Required Columns (Minimum)
- `product_name` (required)
- `product_code` (optional, auto-generated if missing)
- `category` (optional)
- `subcategory` (optional)
- `product_type` (optional)
- `primary_count_unit` (optional, default: "each")
- `active` (optional, default: "Yes")

### Optional Columns
- `volume_conversion_unit`, `volume_conversion_factor`
- `weight_conversion_unit`, `weight_conversion_factor`
- `default_department`, `preferred_vendor`
- `par_level`, `order_quantity`
- `is_generic`, `is_non_inventory`, `is_prep_item`
- `gl_code`, `bin_location`
- `tags`, `image_url`

## Import Workflow

1. **Upload File**: User uploads Excel/CSV file
2. **Validate File**: Check file format and structure
3. **Map Columns**: Map file columns to Product fields
4. **Validate Data**: Validate each row of data
5. **Import Items**: Create/update products
6. **Generate Report**: Show import results

## Export Functionality

### Export to Excel/CSV

Export products to Excel or CSV format with:
- All product fields
- Department assignments
- Purchase units
- Categories and tags
- Filterable by department, category, product type

## Implementation Steps

### Step 1: Create Item Loader DocType
1. Create `Item Loader` DocType
2. Add file upload field
3. Add import options
4. Add status tracking fields

### Step 2: Create Child Tables
1. Create `Column Mapping` child table
2. Create `Validation Error` child table
3. Create `Import Result` child table

### Step 3: Implement Import Logic
1. Implement file parsing (Excel/CSV)
2. Implement column mapping
3. Implement data validation
4. Implement product creation/update

### Step 4: Implement Export Logic
1. Implement Excel export
2. Implement CSV export
3. Add filtering and sorting
4. Add field selection

## Dependencies

- **Product DocType**: Target for import/export
- **Product Category DocType**: For category references
- **Department DocType**: For department assignments
- **Vendor DocType**: For vendor references
- **pandas/openpyxl**: For Excel/CSV processing

## Usage Examples

### Import Products
```
1. Create Item Loader
2. Upload Excel file with product data
3. Map columns to Product fields
4. Validate data
5. Import products
6. Review import results
```

### Export Products
```
1. Select products to export
2. Choose export format (Excel/CSV)
3. Select fields to include
4. Apply filters (department, category, etc.)
5. Export file
```

## Testing Checklist

- [ ] Import products from Excel
- [ ] Import products from CSV
- [ ] Test column mapping
- [ ] Test data validation
- [ ] Test duplicate handling
- [ ] Test error reporting
- [ ] Test create/update operations
- [ ] Export products to Excel
- [ ] Export products to CSV
- [ ] Test filtering and sorting

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 23.2

