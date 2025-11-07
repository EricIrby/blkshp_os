# Excel Import/Export

## Overview

Excel Import/Export provides functionality for importing and exporting data in Excel and CSV formats. Used for bulk operations, data migration, and reporting.

## Purpose

- Import data from Excel/CSV files
- Export data to Excel/CSV files
- Support bulk operations
- Enable data migration
- Support reporting exports

## Libraries Used

### pandas
- **Library**: `pandas`
- **License**: BSD
- **Features**: Data manipulation, Excel/CSV reading/writing
- **Integration**: Python library

### openpyxl
- **Library**: `openpyxl`
- **License**: MIT
- **Features**: Excel file reading/writing
- **Integration**: Python library

## Import Functionality

### Supported Formats
- Excel (.xlsx, .xls)
- CSV (.csv)
- Tab-delimited files

### Import Features
- Column mapping
- Data validation
- Error handling
- Bulk import
- Progress tracking

## Export Functionality

### Supported Formats
- Excel (.xlsx)
- CSV (.csv)
- PDF (via report export)

### Export Features
- Custom column selection
- Filtering and sorting
- Multiple sheet support (Excel)
- Formatting options

## Implementation Steps

### Step 1: Install Libraries
1. Install pandas
2. Install openpyxl
3. Import in Frappe

### Step 2: Implement Import
1. Read Excel/CSV files
2. Validate data
3. Map columns
4. Import records

### Step 3: Implement Export
1. Query data
2. Format data
3. Write to Excel/CSV
4. Support filtering

## Dependencies

- **pandas**: Data manipulation
- **openpyxl**: Excel file handling
- **Domain DocTypes**: Data sources

## Usage Examples

### Import Products
```
1. Prepare Excel file with product data
2. Upload file
3. Map columns to Product fields
4. Validate data
5. Import products
```

### Export Inventory Report
```
1. Generate inventory report
2. Select export format (Excel/CSV)
3. Apply filters
4. Export file
```

## Testing Checklist

- [ ] Import from Excel
- [ ] Import from CSV
- [ ] Export to Excel
- [ ] Export to CSV
- [ ] Handle import errors
- [ ] Validate data
- [ ] Test column mapping

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 6.7

