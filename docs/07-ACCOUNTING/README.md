# Accounting Integration Domain

## Overview

The Accounting domain integrates with external accounting systems (QuickBooks, NetSuite, R365, Sage Intacct) to sync bills and GL codes.

## Key Concepts

- **Bill Sync**: Sync vendor bills to accounting systems
- **GL Code Mapping**: Map products/departments to GL codes
- **Payee Mapping**: Map vendors to payee names in accounting systems
- **Multiple Accounting Systems**: Support for various accounting platforms

## Dependencies

- **04-PROCUREMENT**: Invoice/bill data
- **01-PRODUCTS**: GL code mapping per product-department
- **02-DEPARTMENTS**: Department-level GL codes

## Implementation Priority

**MEDIUM** - Required for financial reporting integration

## Functions

1. ✅ **Accounting Configuration** - Accounting system setup
2. ✅ **QuickBooks Integration** - QuickBooks Online/Desktop
3. ✅ **NetSuite Integration** - NetSuite API integration
4. ✅ **Other Accounting Systems** - R365, Sage Intacct
5. ✅ **GL Code Mapping** - GL code assignment, mapping
6. ✅ **Payee Mapping** - Vendor-to-payee mapping
7. ✅ **Bill Sync** - Bill syncing to accounting systems
8. ✅ **Accounting Errors** - Error handling, troubleshooting

## Status

✅ **Partially Extracted** - Core functions documented:
- ✅ Accounting Configuration (01-Accounting-Configuration.md)
- ⏳ QuickBooks Integration (02-QuickBooks-Integration.md) - To be extracted
- ⏳ NetSuite Integration (03-NetSuite-Integration.md) - To be extracted
- ⏳ Other Accounting Systems (04-Other-Accounting-Systems.md) - To be extracted
- ✅ GL Code Mapping (05-GL-Code-Mapping.md)
- ⏳ Payee Mapping (06-Payee-Mapping.md) - To be extracted
- ⏳ Bill Sync (07-Bill-Sync.md) - To be extracted
- ⏳ Accounting Errors (08-Accounting-Errors.md) - To be extracted

---

**Next Steps**: Extract remaining Accounting documentation (QuickBooks, NetSuite, Bill Sync).

