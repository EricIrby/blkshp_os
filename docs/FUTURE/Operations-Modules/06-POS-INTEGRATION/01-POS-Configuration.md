# POS Configuration

## Overview

POS Configuration sets up POS system connections with instance-based management. Each location can have multiple POS instances (e.g., Restaurant Toast, Retail Toast) mapped to different departments.

## Purpose

- Configure POS system connections
- Support multiple POS instances per location
- Map POS instances to departments
- Configure API authentication
- Set up automatic polling schedules

## DocType Definition

### POS Instance DocType

```python
# POS Instance DocType
# Fields
- instance_name (Data, required)  # Name for this POS instance (e.g., "Restaurant Toast")
- pos_system (Select: Toast, Square, Clover, Resy, Custom, required)
- company (Link: Company, required)
- location (Link: Location, optional)  # If multi-location
- department (Link: Department, required)  # Primary department for this instance
- api_endpoint (Data, optional)  # API endpoint URL
- api_key (Password, optional)  # API authentication key
- api_secret (Password, optional)  # API secret (if required)
- authentication_type (Select: API Key, OAuth, Basic Auth, Custom)
- polling_enabled (Check, default=1)  # Enable automatic polling
- polling_frequency (Select: Every 15 minutes, Every 30 minutes, Hourly, Every 2 hours, Daily)
- last_poll_date (Datetime)  # Last successful poll
- last_poll_status (Select: Success, Error, In Progress)
- last_poll_error (Text)  # Error message if last poll failed
- next_poll_date (Datetime, calculated)  # Next scheduled poll
- status (Select: Active, Inactive, Error)
- notes (Text)

# Methods
def poll_sales_data():
    """Poll sales data from POS API"""
    pass

def test_connection():
    """Test API connection"""
    pass

def calculate_next_poll():
    """Calculate next poll date based on frequency"""
    pass
```

## Key Features

### Multiple Instances
- Each location can have multiple POS instances
- Example: Restaurant Toast and Retail Toast at same location
- Each instance mapped to different department
- Independent configuration per instance

### Department Mapping
- Each instance mapped to primary department
- Sales from instance assigned to department
- Supports department-specific reporting

### API Configuration
- Stores API credentials and endpoints
- Supports multiple authentication types
- Test connection functionality
- Secure credential storage

### Automatic Polling
- Configurable polling frequency
- Automatic sales data import
- Poll history tracking
- Error handling and retry logic

## Implementation Steps

### Step 1: Create POS Instance DocType
1. Create `POS Instance` DocType
2. Add basic fields (name, system, company, department)
3. Add API configuration fields
4. Add polling configuration fields

### Step 2: Implement API Connection
1. Implement test_connection() method
2. Support multiple authentication types
3. Handle API errors gracefully
4. Store credentials securely

### Step 3: Implement Polling
1. Implement poll_sales_data() method
2. Calculate next poll date
3. Track poll status and errors
4. Support manual polling

## Dependencies

- **Company DocType**: Company reference (Frappe built-in)
- **Department DocType**: Department mapping
- **Location DocType**: Location reference (if multi-location)

## Usage Examples

### Multiple Instance Setup
```
Location: Hotel ABC
├── POS Instance: "Restaurant Toast"
│   ├── Department: Restaurant Department
│   ├── API Endpoint: https://api.toasttab.com/restaurant-123
│   └── Polling: Every 30 minutes
└── POS Instance: "Retail Toast"
    ├── Department: Retail Department
    ├── API Endpoint: https://api.toasttab.com/retail-456
    └── Polling: Hourly
```

### API Configuration
```
POS Instance: "Restaurant Toast"
├── API Endpoint: https://api.toasttab.com/v1
├── API Key: [encrypted]
├── API Secret: [encrypted]
├── Authentication Type: API Key
└── Connection Status: Connected
```

## Testing Checklist

- [ ] Create POS instance
- [ ] Configure API credentials
- [ ] Test API connection
- [ ] Configure polling frequency
- [ ] Enable automatic polling
- [ ] Verify poll execution
- [ ] Test manual polling
- [ ] Handle API errors
- [ ] Track poll history

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 20.2

