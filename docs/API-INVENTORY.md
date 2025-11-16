# Inventory API Reference

## Overview

The Inventory API provides REST endpoints for querying and managing inventory data including balances, stock movements, batch numbers, and inventory audits.

All endpoints are permission-aware and respect department-based access controls. System roles (BLKSHP Operations, System Manager, Administrator) bypass permission checks.

**Base Path:** `/api/method/blkshp_os.api.inventory.`

---

## Inventory Balance Endpoints

### List Inventory Balances

Get a paginated list of inventory balances with optional filters.

**Endpoint:** `list_inventory_balances`

**Method:** GET

**Parameters:**
- `product` (string, optional): Filter by product code
- `department` (string, optional): Filter by department
- `company` (string, optional): Filter by company
- `limit` (integer, optional): Maximum results (default: 100)
- `offset` (integer, optional): Pagination offset (default: 0)

**Response:**
```json
{
  "balances": [
    {
      "name": "TOMATO-KITCHEN-ACME",
      "product": "TOMATO",
      "department": "KITCHEN",
      "company": "ACME",
      "quantity": 150.5,
      "last_updated": "2025-11-16 10:30:00",
      "last_audit_date": "2025-11-15"
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0
}
```

---

### Get Inventory Balance

Get a specific inventory balance for a product/department/company combination.

**Endpoint:** `get_inventory_balance`

**Method:** GET

**Parameters:**
- `product` (string, required): Product code
- `department` (string, required): Department name
- `company` (string, required): Company name

**Response:**
```json
{
  "product": "TOMATO",
  "department": "KITCHEN",
  "company": "ACME",
  "quantity": 150.5,
  "last_updated": "2025-11-16 10:30:00",
  "last_audit_date": "2025-11-15"
}
```

---

## Stock Ledger Query Endpoints

### Query Stock Balance

Query current stock balance from Stock Ledger Entries.

**Endpoint:** `query_stock_balance`

**Method:** GET

**Parameters:**
- `product` (string, required): Product code
- `department` (string, required): Department name
- `company` (string, required): Company name
- `as_of_date` (string, optional): Date to query balance as of (ISO format: YYYY-MM-DD)

**Response:**
```json
{
  "product": "TOMATO",
  "department": "KITCHEN",
  "company": "ACME",
  "balance": 150.5,
  "as_of_date": "2025-11-16"
}
```

---

### Query Stock Value

Query current stock value from Stock Ledger Entries.

**Endpoint:** `query_stock_value`

**Method:** GET

**Parameters:**
- `product` (string, required): Product code
- `department` (string, required): Department name
- `company` (string, required): Company name
- `as_of_date` (string, optional): Date to query value as of (ISO format)

**Response:**
```json
{
  "product": "TOMATO",
  "department": "KITCHEN",
  "company": "ACME",
  "value": 452.50,
  "as_of_date": "2025-11-16"
}
```

---

### Query Stock Movements

Query stock movements for a product/department within a date range.

**Endpoint:** `query_stock_movements`

**Method:** GET

**Parameters:**
- `product` (string, required): Product code
- `department` (string, required): Department name
- `company` (string, required): Company name
- `from_date` (string, required): Start date (ISO format)
- `to_date` (string, required): End date (ISO format)

**Response:**
```json
{
  "product": "TOMATO",
  "department": "KITCHEN",
  "company": "ACME",
  "from_date": "2025-11-01",
  "to_date": "2025-11-16",
  "movements": [
    {
      "posting_date": "2025-11-15",
      "voucher_type": "Inventory Audit",
      "voucher_no": "AUDIT-001",
      "actual_qty": 50.0,
      "qty_after_transaction": 150.5
    }
  ]
}
```

---

## Batch Number Endpoints

### List Batches

Get a paginated list of batch numbers with optional filters.

**Endpoint:** `list_batches`

**Method:** GET

**Parameters:**
- `product` (string, optional): Filter by product code
- `department` (string, optional): Filter by department
- `company` (string, optional): Filter by company
- `active_only` (boolean, optional): Only non-expired batches (default: true)
- `limit` (integer, optional): Maximum results (default: 100)
- `offset` (integer, optional): Pagination offset (default: 0)

**Response:**
```json
{
  "batches": [
    {
      "name": "TOMATO-2025-0001",
      "product": "TOMATO",
      "department": "KITCHEN",
      "company": "ACME",
      "manufacturing_date": "2025-11-01",
      "expiration_date": "2025-12-01",
      "quantity": 50.0
    }
  ],
  "total": 1,
  "limit": 100,
  "offset": 0
}
```

---

### Get Batch

Get specific batch number details.

**Endpoint:** `get_batch`

**Method:** GET

**Parameters:**
- `batch_number` (string, required): Batch number

**Response:**
```json
{
  "name": "TOMATO-2025-0001",
  "product": "TOMATO",
  "department": "KITCHEN",
  "company": "ACME",
  "manufacturing_date": "2025-11-01",
  "expiration_date": "2025-12-01",
  "quantity": 50.0
}
```

---

### Query Batch Balance

Query stock balance by batch number.

**Endpoint:** `query_batch_balance`

**Method:** GET

**Parameters:**
- `product` (string, required): Product code
- `department` (string, required): Department name
- `company` (string, required): Company name
- `batch_number` (string, optional): Specific batch (if omitted, returns all batches)
- `as_of_date` (string, optional): Date to query balance as of (ISO format)

**Response:**
```json
{
  "product": "TOMATO",
  "department": "KITCHEN",
  "company": "ACME",
  "batch_number": "TOMATO-2025-0001",
  "as_of_date": "2025-11-16",
  "balance": 50.0
}
```

**Response (all batches):**
```json
{
  "product": "TOMATO",
  "department": "KITCHEN",
  "company": "ACME",
  "batch_number": null,
  "as_of_date": "2025-11-16",
  "balance": {
    "TOMATO-2025-0001": 50.0,
    "TOMATO-2025-0002": 30.0
  }
}
```

---

### Query Batch Movements

Query movements for a specific batch number.

**Endpoint:** `query_batch_movements`

**Method:** GET

**Parameters:**
- `batch_number` (string, required): Batch number
- `from_date` (string, optional): Start date (ISO format)
- `to_date` (string, optional): End date (ISO format)

**Response:**
```json
{
  "batch_number": "TOMATO-2025-0001",
  "product": "TOMATO",
  "department": "KITCHEN",
  "from_date": "2025-11-01",
  "to_date": "2025-11-16",
  "movements": [
    {
      "posting_date": "2025-11-15",
      "voucher_type": "Inventory Audit",
      "voucher_no": "AUDIT-001",
      "actual_qty": 50.0
    }
  ]
}
```

---

## Inventory Audit Endpoints

### List Audits

Get a paginated list of inventory audits with optional filters.

**Endpoint:** `list_audits`

**Method:** GET

**Parameters:**
- `status` (string, optional): Filter by status (Setup, Ready, In Progress, Review, Closed, Locked)
- `department` (string, optional): Filter by department
- `company` (string, optional): Filter by company
- `limit` (integer, optional): Maximum results (default: 50)
- `offset` (integer, optional): Pagination offset (default: 0)

**Response:**
```json
{
  "audits": [
    {
      "name": "AUDIT-001",
      "audit_name": "Monthly Inventory Count - November 2025",
      "status": "Closed",
      "company": "ACME",
      "audit_date": "2025-11-15",
      "closed_by": "user@example.com",
      "closed_at": "2025-11-15 18:30:00"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

---

### Get Audit

Get specific inventory audit details.

**Endpoint:** `get_audit`

**Method:** GET

**Parameters:**
- `audit_name` (string, required): Audit document name

**Response:**
```json
{
  "name": "AUDIT-001",
  "audit_name": "Monthly Inventory Count - November 2025",
  "status": "Closed",
  "company": "ACME",
  "audit_date": "2025-11-15",
  "closed_by": "user@example.com",
  "closed_at": "2025-11-15 18:30:00",
  "departments": [
    {"department": "KITCHEN"},
    {"department": "BAR"}
  ],
  "categories": [
    {"category": "Produce"},
    {"category": "Proteins"}
  ],
  "storage_locations": [
    {"storage_area": "Walk-in Cooler"}
  ],
  "counting_tasks_count": 12,
  "audit_lines_count": 45
}
```

---

### Create Audit

Create a new inventory audit.

**Endpoint:** `create_audit`

**Method:** POST

**Request Body:**
```json
{
  "audit_name": "Monthly Inventory Count - December 2025",
  "company": "ACME",
  "audit_date": "2025-12-15",
  "departments": [
    {"department": "KITCHEN"},
    {"department": "BAR"}
  ],
  "categories": [
    {"category": "Produce"}
  ]
}
```

**Response:**
```json
{
  "name": "AUDIT-002",
  "audit_name": "Monthly Inventory Count - December 2025",
  "status": "Setup"
}
```

---

### Update Audit Status

Update inventory audit status by performing workflow actions.

**Endpoint:** `update_audit_status`

**Method:** POST

**Parameters:**
- `audit_name` (string, required): Audit document name
- `action` (string, required): Action to perform
  - `create_tasks`: Generate counting tasks
  - `mark_in_progress`: Mark audit as in progress
  - `mark_review`: Mark audit as ready for review
  - `close`: Close the audit and generate stock ledger entries
- `user` (string, optional): User performing the action (for close action)

**Request Body:**
```json
{
  "audit_name": "AUDIT-002",
  "action": "mark_in_progress"
}
```

**Response:**
```json
{
  "name": "AUDIT-002",
  "status": "In Progress",
  "action_performed": "mark_in_progress"
}
```

---

## Permission Model

All inventory API endpoints respect department-based permissions:

1. **Department Access**: Users can only access data for departments they have permissions for
2. **System Roles Bypass**: BLKSHP Operations, System Manager, and Administrator roles bypass all restrictions
3. **Read Permissions**: Most query endpoints require `can_read` permission
4. **Write Permissions**: Create/update endpoints require `can_write` permission for affected departments

### Permission Checks

- **Inventory Balance**: Checks department permission
- **Stock Queries**: Checks department permission
- **Batch Operations**: Checks department permission of the batch's department
- **Audit Operations**: Checks if user has permission for at least one department in the audit

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request** - Invalid parameters
```json
{
  "exc_type": "ValidationError",
  "message": "Product, department, and company are required."
}
```

**403 Forbidden** - Permission denied
```json
{
  "exc_type": "PermissionError",
  "message": "You do not have permission to access this department."
}
```

**404 Not Found** - Resource not found
```json
{
  "exc_type": "DoesNotExistError",
  "message": "Inventory balance not found: TOMATO-KITCHEN-ACME"
}
```

---

## Usage Examples

### cURL

```bash
# List inventory balances
curl -X GET "http://localhost:8000/api/method/blkshp_os.api.inventory.list_inventory_balances?product=TOMATO&limit=10" \
  -H "Authorization: token <api_key>:<api_secret>"

# Get specific balance
curl -X GET "http://localhost:8000/api/method/blkshp_os.api.inventory.get_inventory_balance?product=TOMATO&department=KITCHEN&company=ACME" \
  -H "Authorization: token <api_key>:<api_secret>"

# Create audit
curl -X POST "http://localhost:8000/api/method/blkshp_os.api.inventory.create_audit" \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{
    "audit_name": "Monthly Count",
    "company": "ACME",
    "audit_date": "2025-12-01",
    "departments": [{"department": "KITCHEN"}]
  }'
```

### JavaScript (Frappe)

```javascript
// List inventory balances
frappe.call({
  method: 'blkshp_os.api.inventory.list_inventory_balances',
  args: {
    product: 'TOMATO',
    limit: 10
  },
  callback: function(r) {
    console.log(r.message.balances);
  }
});

// Query stock balance
frappe.call({
  method: 'blkshp_os.api.inventory.query_stock_balance',
  args: {
    product: 'TOMATO',
    department: 'KITCHEN',
    company: 'ACME'
  },
  callback: function(r) {
    console.log('Balance:', r.message.balance);
  }
});
```

---

## Related Documentation

- [Stock Ledger Entry](/docs/03-INVENTORY/stock-ledger-entry.md)
- [Inventory Balance](/docs/03-INVENTORY/inventory-balance.md)
- [Batch Number](/docs/03-INVENTORY/batch-number.md)
- [Inventory Audit](/docs/03-INVENTORY/inventory-audit.md)
- [API Authentication](/docs/API-AUTHENTICATION.md)
- [Permissions Model](/docs/11-PERMISSIONS/)
