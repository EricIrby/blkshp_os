# Accounting Configuration

## Overview

Accounting Configuration sets up connections to external accounting systems (QuickBooks, NetSuite, R365, Sage Intacct) for bill syncing and financial reporting.

## Purpose

- Configure accounting system connections
- Set up authentication credentials
- Map GL codes
- Configure bill sync settings
- Support multiple accounting systems

## DocType Definition

### Accounting System DocType

```python
# Accounting System DocType
# Fields
- system_name (Data, required)
- accounting_system (Select: QuickBooks Online, QuickBooks Desktop, NetSuite, R365, Sage Intacct, required)
- company (Link: Company, required)
- api_endpoint (Data, optional)
- api_key (Password, optional)
- api_secret (Password, optional)
- authentication_type (Select: API Key, OAuth, Basic Auth, Custom)
- refresh_token (Password, optional)  # For OAuth
- company_id (Data, optional)  # Accounting system company ID
- is_active (Check, default=1)
- last_sync_date (Datetime)
- last_sync_status (Select: Success, Error, In Progress)
- sync_frequency (Select: Real-time, Hourly, Daily, Manual)

# Methods
def test_connection():
    """Test accounting system connection"""
    pass

def sync_bills():
    """Sync bills to accounting system"""
    pass
```

## Supported Accounting Systems

### QuickBooks Online
- OAuth 2.0 authentication
- Full API coverage
- Bill syncing
- Payee mapping

### QuickBooks Desktop
- Web Connector integration
- File-based sync
- Bill syncing
- Payee mapping

### NetSuite
- SuiteTalk REST API
- Token-based authentication
- Bill syncing
- Custom field mapping

### Restaurant365 (R365)
- API integration
- Bill syncing
- GL code mapping

### Sage Intacct
- API integration
- Bill syncing
- GL code mapping

## Implementation Steps

### Step 1: Create Accounting System DocType
1. Create `Accounting System` DocType
2. Add system selection field
3. Add API configuration fields
4. Add authentication fields

### Step 2: Implement Connection Testing
1. Implement test_connection() method
2. Support multiple authentication types
3. Handle connection errors
4. Store credentials securely

### Step 3: Implement Bill Sync
1. Implement sync_bills() method
2. Map bills to accounting format
3. Handle sync errors
4. Track sync status

## Dependencies

- **Company DocType**: Company reference
- **Vendor Invoice DocType**: Bills to sync
- **Bill DocType**: Synced bills

## Usage Examples

### QuickBooks Online Setup
```
Accounting System:
  - System Name: "Store 1 QuickBooks"
  - Accounting System: QuickBooks Online
  - Company: Store 1
  - API Endpoint: https://sandbox-quickbooks.api.intuit.com
  - Authentication: OAuth 2.0
  - Status: Connected
```

## Testing Checklist

- [ ] Create accounting system connection
- [ ] Configure API credentials
- [ ] Test connection
- [ ] Configure bill sync
- [ ] Sync bills to accounting system
- [ ] Handle sync errors
- [ ] Track sync status

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 6.5

