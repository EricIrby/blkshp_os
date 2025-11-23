# Products Domain

## Overview

The Products domain manages all product/item data in a unified system. Unlike Craftable's separate platforms (Foodager/Bevager/House), BLKSHP uses a single product master that can be assigned to multiple departments.

## Key Concepts

- **Unified Product Master**: All products (food, beverage, supplies) in one system
- **Department Allocations**: Products assigned to departments (many-to-many)
- **Purchase Units**: Vendor-specific purchase unit definitions
- **Unit Conversion**: Hub-and-spoke conversion model for count units
- **Product Properties**: Generic items, non-inventory, prep items, linked items

## Dependencies

- **02-DEPARTMENTS**: Department definitions required for product allocations
- **04-PROCUREMENT**: Vendor relationships for purchase units

## Implementation Priority

**HIGH** - Foundation domain required by most other domains

## Functions

1. ✅ **Product Master** - Unified Product DocType, CRUD operations
2. ✅ **Product Categories** - Category hierarchy, subcategories
3. ✅ **Purchase Units** - Purchase unit definitions, vendor-specific units
4. ✅ **Unit Conversion System** - Hub-and-spoke conversion model
5. ✅ **Product Departments** - Product-to-department allocations
6. ✅ **Product Storage** - Storage area assignments
7. ✅ **Product Properties** - Generic items, non-inventory, prep items
8. ✅ **Bulk Operations** - Item Loader, Express Loader, bulk import/export
9. ✅ **Product History** - Item history tracking, audit trail
10. ✅ **Product Labels** - Label printing, barcode generation
11. ✅ **Product Pricing** - CU price, contract prices, promo thresholds

## Status

✅ **Partially Extracted** - Core functions documented:
- ✅ Product Master (01-Product-Master.md)
- ✅ Product Categories (02-Product-Categories.md)
- ✅ Purchase Units (03-Purchase-Units.md)
- ✅ Unit Conversion System (04-Unit-Conversion-System.md)
- ⏳ Product Departments (05-Product-Departments.md) - See Departments domain
- ⏳ Product Storage (06-Product-Storage.md) - To be extracted
- ✅ Product Properties (07-Product-Properties.md)
- ✅ Bulk Operations (08-Bulk-Operations.md)
- ✅ Product History (09-Product-History.md)
- ✅ Product Labels (10-Product-Labels.md)
- ✅ Product Pricing (11-Product-Pricing.md)

---

**Next Steps**: Extract Product Storage documentation to complete the domain.

