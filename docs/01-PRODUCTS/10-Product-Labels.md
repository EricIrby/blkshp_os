# Product Labels

## Overview

Product Labels provide label printing capabilities for products. Labels can be customized with product information, barcodes, and other details for inventory management and identification.

## Purpose

- Print product labels for inventory management
- Support barcode generation and printing
- Customize label formats
- Print labels in bulk
- Support different label sizes and formats

## Label Printing Features

### Label Information
- Product name
- Product code
- Barcode (if available)
- Category
- Department
- Bin location
- Expiration date (if applicable)
- Other product details

### Label Formats
- Standard label format
- Custom label format
- Barcode-only labels
- Full product information labels

### Print Options
- Print single label
- Print labels in bulk
- Print labels for selected products
- Print labels by department
- Print labels by category

## Implementation Steps

### Step 1: Create Label Print Format
1. Create Print Format for Product labels
2. Design label layout
3. Add barcode support
4. Add customizable fields

### Step 2: Implement Barcode Generation
1. Generate barcodes for products
2. Support different barcode formats (Code128, EAN-13, etc.)
3. Store barcode data on product

### Step 3: Add Print Functionality
1. Add print button to Product form
2. Add bulk print functionality
3. Add print preview
4. Support different label sizes

### Step 4: Create Label Settings
1. Create label settings DocType
2. Configure default label format
3. Configure label size
4. Configure print options

## Dependencies

- **Product DocType**: Source of label data
- **Barcode Library**: For barcode generation (e.g., python-barcode)
- **Print Format System**: Frappe's print format system

## Usage Examples

### Print Single Label
```
1. Open Product form
2. Click "Print Label" button
3. Select label format
4. Print label
```

### Print Labels in Bulk
```
1. Select multiple products
2. Click "Print Labels" action
3. Configure print options
4. Print all labels
```

### Custom Label Format
```
Label Format:
  - Product Name (large font)
  - Product Code
  - Barcode
  - Department
  - Bin Location
```

## Testing Checklist

- [ ] Print single product label
- [ ] Print labels in bulk
- [ ] Generate barcodes
- [ ] Test different label formats
- [ ] Test label customization
- [ ] Verify label information accuracy
- [ ] Test print preview

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md

