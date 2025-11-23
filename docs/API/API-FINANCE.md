# Finance & Intercompany API Reference

## Overview

The Finance API provides REST endpoints for querying and managing intercompany transactions, balances, and settlements.

All endpoints are permission-aware and respect company-based access controls. System roles (BLKSHP Operations, System Manager, Administrator, Accounts Manager) bypass permission checks.

**Base Path:** `/api/method/blkshp_os.api.finance.`

---

## Intercompany Balance Endpoints

### Get Intercompany Balance

Get the balance between two specific companies.

**Endpoint:** `get_intercompany_balance`

**Method:** GET

**Parameters:**
- `source_company` (string, required): Source company code
- `target_company` (string, required): Target company code
- `as_of_date` (string, optional): Date to query balance as of (ISO format: YYYY-MM-DD)

**Response:**
```json
{
  "source_company": "ACME",
  "target_company": "HOTEL-1",
  "balance": 15000.50,
  "as_of_date": "2025-11-16",
  "currency": "USD"
}
```

**Notes:**
- Positive balance means source company owes target company
- Negative balance means target company owes source company
- Companies must be in the same Company Group

---

### List Intercompany Balances

Get a list of all intercompany balances for a company or group.

**Endpoint:** `list_intercompany_balances`

**Method:** GET

**Parameters:**
- `company` (string, optional): Filter balances for this company
- `company_group` (string, optional): Get all balances within this group

**Response:**
```json
{
  "balances": [
    {
      "source_company": "ACME",
      "target_company": "HOTEL-1",
      "balance": 15000.50,
      "currency": "USD"
    },
    {
      "source_company": "ACME",
      "target_company": "HOTEL-2",
      "balance": -5000.00,
      "currency": "USD"
    }
  ],
  "total": 2
}
```

**Notes:**
- Must specify either `company` or `company_group`
- Only returns non-zero balances

---

## Settlement Endpoints

### List Settlements

Get a paginated list of intercompany settlements.

**Endpoint:** `list_settlements`

**Method:** GET

**Parameters:**
- `company` (string, optional): Filter settlements involving this company (as source or target)
- `status` (string, optional): Filter by status (Draft, Settled, Cancelled)
- `limit` (integer, optional): Maximum results (default: 50)
- `offset` (integer, optional): Pagination offset (default: 0)

**Response:**
```json
{
  "settlements": [
    {
      "name": "SETTLE-2025-0001",
      "source_company": "HOTEL-1",
      "target_company": "ACME",
      "settlement_amount": 10000.00,
      "settlement_currency": "USD",
      "settlement_date": "2025-11-15",
      "status": "Settled",
      "submitted_by": "user@example.com"
    }
  ],
  "total": 1,
  "limit": 50,
  "offset": 0
}
```

---

### Get Settlement

Get specific settlement details.

**Endpoint:** `get_settlement`

**Method:** GET

**Parameters:**
- `settlement_name` (string, required): Settlement document name

**Response:**
```json
{
  "name": "SETTLE-2025-0001",
  "source_company": "HOTEL-1",
  "target_company": "ACME",
  "settlement_amount": 10000.00,
  "settlement_currency": "USD",
  "settlement_date": "2025-11-15",
  "status": "Settled",
  "description": "Monthly intercompany settlement",
  "payment_method": "Bank Transfer",
  "reference_number": "TXN-12345",
  "submitted_by": "user@example.com",
  "submitted_at": "2025-11-15 14:30:00"
}
```

---

### Create Settlement

Create a new intercompany settlement.

**Endpoint:** `create_settlement`

**Method:** POST

**Request Body:**
```json
{
  "source_company": "HOTEL-1",
  "target_company": "ACME",
  "settlement_amount": 10000.00,
  "settlement_currency": "USD",
  "description": "Monthly intercompany settlement",
  "payment_method": "Bank Transfer",
  "reference_number": "TXN-12345"
}
```

**Response:**
```json
{
  "name": "SETTLE-2025-0002",
  "source_company": "HOTEL-1",
  "target_company": "ACME",
  "settlement_amount": 10000.00,
  "status": "Draft"
}
```

**Required Fields:**
- `source_company` - Company making the payment
- `target_company` - Company receiving the payment
- `settlement_amount` - Amount to settle (must be > 0)
- `settlement_currency` - Currency code (e.g., "USD")

**Optional Fields:**
- `description` - Settlement description
- `payment_method` - Method of payment (Bank Transfer, Check, ACH, Wire, Cash, Other)
- `reference_number` - External reference number (e.g., transaction ID)
- `notes` - Internal notes

**Validation:**
- Companies must be different
- Companies must be in the same Company Group
- Settlement amount must be greater than zero
- User must have write permission for both companies

---

### Submit Settlement

Submit an intercompany settlement for approval.

**Endpoint:** `submit_settlement`

**Method:** POST

**Parameters:**
- `settlement_name` (string, required): Settlement document name

**Response:**
```json
{
  "name": "SETTLE-2025-0002",
  "status": "Settled",
  "settlement_date": "2025-11-16",
  "submitted_by": "user@example.com"
}
```

**Dual Approval Requirement:**
- User must have submit permission for **both** source and target companies
- This ensures proper segregation of duties for intercompany fund transfers
- System roles (System Manager, Administrator, Accounts Manager) bypass this requirement

---

## Permission Model

All finance/intercompany API endpoints respect company-based permissions:

1. **Company Access**: Users can only access data for companies they have permissions for
2. **System Roles Bypass**: BLKSHP Operations, System Manager, Administrator, and Accounts Manager roles bypass all restrictions
3. **Read Permissions**: Balance query endpoints require read access to at least one company
4. **Write Permissions**: Creating settlements requires write access to both companies
5. **Submit Permissions**: Submitting settlements requires submit permission for **both** companies (dual approval)

### Permission Checks

- **Intercompany Balance**: User must have read access to source or target company
- **List Balances**: If filtered by company, user must have access to that company
- **List Settlements**: If filtered by company, user must have access to that company
- **Get Settlement**: User must have access to source or target company
- **Create Settlement**: User must have write access to **both** companies
- **Submit Settlement**: User must have submit access to **both** companies (dual approval)

---

## Error Responses

All endpoints may return the following error responses:

**400 Bad Request** - Invalid parameters
```json
{
  "exc_type": "ValidationError",
  "message": "source_company is required"
}
```

**403 Forbidden** - Permission denied
```json
{
  "exc_type": "PermissionError",
  "message": "You do not have permission to view balances for these companies"
}
```

**404 Not Found** - Resource not found
```json
{
  "exc_type": "DoesNotExistError",
  "message": "Settlement SETTLE-2025-0001 not found"
}
```

---

## Usage Examples

### cURL

```bash
# Get intercompany balance
curl -X GET "http://localhost:8000/api/method/blkshp_os.api.finance.get_intercompany_balance?source_company=ACME&target_company=HOTEL-1" \
  -H "Authorization: token <api_key>:<api_secret>"

# List settlements for a company
curl -X GET "http://localhost:8000/api/method/blkshp_os.api.finance.list_settlements?company=HOTEL-1&limit=10" \
  -H "Authorization: token <api_key>:<api_secret>"

# Create settlement
curl -X POST "http://localhost:8000/api/method/blkshp_os.api.finance.create_settlement" \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{
    "source_company": "HOTEL-1",
    "target_company": "ACME",
    "settlement_amount": 10000.00,
    "settlement_currency": "USD",
    "description": "Monthly settlement",
    "payment_method": "Bank Transfer"
  }'

# Submit settlement (dual approval)
curl -X POST "http://localhost:8000/api/method/blkshp_os.api.finance.submit_settlement?settlement_name=SETTLE-2025-0001" \
  -H "Authorization: token <api_key>:<api_secret>"
```

### JavaScript (Frappe)

```javascript
// Get intercompany balance
frappe.call({
  method: 'blkshp_os.api.finance.get_intercompany_balance',
  args: {
    source_company: 'ACME',
    target_company: 'HOTEL-1'
  },
  callback: function(r) {
    console.log('Balance:', r.message.balance);
  }
});

// List all balances for a company
frappe.call({
  method: 'blkshp_os.api.finance.list_intercompany_balances',
  args: {
    company: 'ACME'
  },
  callback: function(r) {
    console.log('Balances:', r.message.balances);
  }
});

// Create settlement
frappe.call({
  method: 'blkshp_os.api.finance.create_settlement',
  args: {
    settlement_data: {
      source_company: 'HOTEL-1',
      target_company: 'ACME',
      settlement_amount: 10000.00,
      settlement_currency: 'USD',
      description: 'Monthly settlement',
      payment_method: 'Bank Transfer'
    }
  },
  callback: function(r) {
    console.log('Created settlement:', r.message.name);
  }
});

// Submit settlement
frappe.call({
  method: 'blkshp_os.api.finance.submit_settlement',
  args: {
    settlement_name: 'SETTLE-2025-0001'
  },
  callback: function(r) {
    console.log('Settlement status:', r.message.status);
  }
});
```

---

## Related Documentation

- [Company Group](/docs/07-ACCOUNTING/company-group.md)
- [Intercompany Settlement](/docs/07-ACCOUNTING/intercompany-settlement.md)
- [Intercompany Balances](/docs/07-ACCOUNTING/intercompany-balances.md)
- [API Authentication](/docs/API-AUTHENTICATION.md)
- [Permissions Model](/docs/11-PERMISSIONS/)
- [Consolidated Decision Log](/docs/CONSOLIDATED_DECISION_LOG.md) - See "Intercompany" decisions

---

## Implementation Notes

### Current Limitations

1. **Balance Calculation**: Intercompany balances currently return placeholder data. Full implementation requires:
   - "Due From" and "Due To" intercompany accounts to be set up
   - GL Entry queries to calculate actual balances
   - This will be implemented in Phase 2

2. **Journal Entry Creation**: Settlements do not yet create Journal Entries automatically. This requires:
   - Intercompany account structure configuration
   - Automated JE generation on settlement submission
   - Planned for Phase 2

3. **Multi-Currency**: Currently assumes single currency (USD). Multi-currency support deferred to Phase 2

4. **Stock Transfers**: Intercompany inventory transfers are not yet supported (Phase 2)

### Future Enhancements (Phase 2)

- Consolidated eliminations for reporting
- Multi-currency settlement support with exchange rates
- Automated Journal Entry generation
- Intercompany stock transfers
- Banking/treasury integration for settlements
- Period locking and month-end close workflows
- Approval escalation and timeout rules

---

## API Changelog

### Version 1.0 (2025-11-16)
- Initial release
- Balance query endpoints (placeholder implementation)
- Settlement management endpoints (create, list, get, submit)
- Dual approval workflow for settlements
- Company Group support
