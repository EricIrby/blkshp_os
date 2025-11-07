# Product History

## Overview

Product History provides complete audit trail tracking for all changes to products. This enables tracking of product modifications, price changes, department assignments, and other important changes over time.

## Purpose

- Track all changes to products
- Provide complete audit trail
- Support compliance and auditing
- Enable change analysis and reporting
- Link changes to related documents

## DocType Definition

### Product History DocType

```python
# Product History DocType
# Fields
- product (Link: Product, required)
- change_type (Select: Created, Updated, Deleted, Activated, Deactivated, 
               Department Added, Department Removed, Price Changed, 
               Unit Changed, Category Changed, Vendor Changed)
- field_name (Data)  # Which field changed
- old_value (Text)  # Previous value
- new_value (Text)  # New value
- changed_by (Link: User, required)
- changed_at (Datetime, required)
- change_reason (Text)  # Optional reason for change
- company (Link: Company)  # For multi-company tracking
- related_document (Dynamic Link)  # Link to related document (Invoice, Transfer, etc.)
- related_document_type (Data)  # Type of related document
```

## Change Types

### Product Lifecycle Changes
- **Created**: Product created
- **Updated**: Product field updated
- **Deleted**: Product deleted
- **Activated**: Product activated
- **Deactivated**: Product deactivated

### Assignment Changes
- **Department Added**: Product assigned to department
- **Department Removed**: Product removed from department
- **Category Changed**: Product category changed
- **Vendor Changed**: Preferred vendor changed

### Data Changes
- **Price Changed**: Price updated (purchase unit price, contract price)
- **Unit Changed**: Count unit or conversion factors changed
- **Property Changed**: Product properties changed (generic, non-inventory, prep item)

## Implementation Steps

### Step 1: Create Product History DocType
1. Create `Product History` DocType
2. Add product link (required)
3. Add change_type field
4. Add field_name, old_value, new_value fields
5. Add changed_by and changed_at fields

### Step 2: Implement History Tracking
1. Create history entry on product creation
2. Create history entry on product update
3. Create history entry on product deletion
4. Track field-level changes

### Step 3: Add Related Document Links
1. Add related_document and related_document_type fields
2. Link changes to invoices, transfers, audits, etc.
3. Provide context for changes

### Step 4: Create History View
1. Create Product History list view
2. Filter by product, change type, date range
3. Show change details
4. Export history to Excel/CSV

## Dependencies

- **Product DocType**: Source of changes
- **User DocType**: For changed_by tracking

## Usage Examples

### Product Creation
```
Product History Entry:
  - Product: "Coca Cola Cans"
  - Change Type: "Created"
  - Changed By: "John Doe"
  - Changed At: "2025-01-15 10:00:00"
```

### Price Change
```
Product History Entry:
  - Product: "Coca Cola Cans"
  - Change Type: "Price Changed"
  - Field Name: "contract_price"
  - Old Value: "$12.95"
  - New Value: "$13.50"
  - Changed By: "Jane Smith"
  - Changed At: "2025-01-20 14:30:00"
  - Related Document: "Vendor Invoice INV-001"
  - Related Document Type: "Vendor Invoice"
```

### Department Assignment
```
Product History Entry:
  - Product: "Chicken Breast"
  - Change Type: "Department Added"
  - Field Name: "departments"
  - Old Value: ""
  - New Value: "Kitchen"
  - Changed By: "Mike Johnson"
  - Changed At: "2025-01-25 09:15:00"
```

## Testing Checklist

- [ ] Track product creation
- [ ] Track product updates
- [ ] Track product deletion
- [ ] Track field-level changes
- [ ] Track department assignments
- [ ] Track price changes
- [ ] Track category changes
- [ ] Link changes to related documents
- [ ] View product history
- [ ] Export product history

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 23.3

