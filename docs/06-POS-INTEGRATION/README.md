# POS Integration Domain

## Overview

The POS Integration domain connects to POS systems (Toast, Square, Lightspeed) to import sales data and calculate automatic depletions.

## Key Concepts

- **Multiple POS Instances**: Support for multiple POS per location (e.g., Toast for restaurant + retail)
- **POS Item Mapping**: Map recipes to POS items for depletion calculation
- **Automatic Depletion**: Calculate inventory depletions from POS sales data
- **Modifier Handling**: Adjust depletions based on modifier selections

## Dependencies

- **01-PRODUCTS**: Product definitions
- **02-DEPARTMENTS**: Department assignments
- **05-RECIPES**: Recipe-to-POS item mapping
- **03-INVENTORY**: Depletions update inventory balances

## Implementation Priority

**MEDIUM** - Required for automatic inventory tracking

## Functions

1. ✅ **POS Configuration** - POS system setup, API keys
2. ✅ **POS Item Mapping** - Recipe-to-POS item mapping
3. ✅ **POS Modifier Mapping** - Modifier-to-POS modifier mapping
4. ✅ **POS Sales Import** - Sales data import, polling
5. ✅ **POS Depletion Calculation** - Automatic depletion from sales
6. ✅ **Multiple POS Instances** - Multiple POS per location (Toast + retail)
7. ✅ **POS API Integrations** - Toast, Square, Lightspeed APIs

## Status

✅ **Partially Extracted** - Core functions documented:
- ✅ POS Configuration (01-POS-Configuration.md)
- ✅ POS Item Mapping (02-POS-Item-Mapping.md)
- ⏳ POS Modifier Mapping (03-POS-Modifier-Mapping.md) - To be extracted
- ✅ POS Sales Import (04-POS-Sales-Import.md)
- ✅ POS Depletion Calculation (05-POS-Depletion-Calculation.md)
- ⏳ Multiple POS Instances (06-Multiple-POS-Instances.md) - Covered in Configuration
- ⏳ POS API Integrations (07-POS-API-Integrations.md) - To be extracted

---

**Next Steps**: Extract remaining POS Integration documentation (Modifier Mapping, API Integrations).

