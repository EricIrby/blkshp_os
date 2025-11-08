# BLKSHP OS API Reference

## Overview

This document provides comprehensive documentation for the BLKSHP OS REST API endpoints.

## Authentication

All API endpoints require authentication. Use Frappe's standard authentication mechanisms:
- Session-based authentication (cookies)
- Token-based authentication (API key/secret)

## Base URL

```
/api/method/blkshp_os.api.<module>.<function>
```

---

## Department API

### Get Accessible Departments

Get list of departments accessible to the current user.

**Endpoint:** `/api/method/blkshp_os.api.departments.get_accessible_departments`

**Method:** `GET` or `POST`

**Parameters:**
- `permission_flag` (string, optional): Permission level to check. Default: `"can_read"`
  - Valid values: `can_read`, `can_write`, `can_create`, `can_delete`, `can_submit`, `can_cancel`, `can_approve`

**Response:**
```json
[
  {
    "name": "DEPT-001",
    "department_name": "Kitchen",
    "department_code": "KITCHEN",
    "department_type": "Food",
    "company": "Test Company",
    "is_active": 1,
    "parent_department": null
  }
]
```

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.get_accessible_departments \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"permission_flag": "can_read"}'
```

---

### Get Department Details

Get comprehensive department details including products and users.

**Endpoint:** `/api/method/blkshp_os.api.departments.get_department_details`

**Method:** `GET` or `POST`

**Parameters:**
- `department` (string, required): Department name/ID

**Response:**
```json
{
  "department": {
    "name": "DEPT-001",
    "department_name": "Kitchen",
    "department_code": "KITCHEN",
    "department_type": "Food",
    "company": "Test Company",
    "is_active": 1,
    "parent_department": null,
    "default_storage_area": "Main Storage",
    "default_gl_code": "5000",
    "settings": "{\"eoq_enabled\": true}"
  },
  "products": [
    {
      "product": "PROD-001",
      "is_primary": 1
    }
  ],
  "users": [
    {
      "user": "user@example.com",
      "can_read": 1,
      "can_write": 1,
      "can_create": 0,
      "can_delete": 0,
      "can_submit": 0,
      "can_cancel": 0,
      "can_approve": 0
    }
  ],
  "product_count": 1,
  "user_count": 1
}
```

**Permissions Required:** `can_read` on the department

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.get_department_details \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"department": "DEPT-001"}'
```

---

### Get Department Hierarchy

Get department hierarchy tree structure.

**Endpoint:** `/api/method/blkshp_os.api.departments.get_department_hierarchy`

**Method:** `GET` or `POST`

**Parameters:**
- `department` (string, optional): Root department. If not provided, returns all top-level departments.

**Response:**
```json
[
  {
    "name": "DEPT-001",
    "department_name": "Kitchen",
    "department_code": "KITCHEN",
    "department_type": "Food",
    "parent_department": null,
    "is_active": 1,
    "has_children": true,
    "children": [
      {
        "name": "DEPT-002",
        "department_name": "Prep Kitchen",
        "department_code": "PREP",
        "department_type": "Kitchen",
        "parent_department": "DEPT-001",
        "is_active": 1,
        "has_children": false
      }
    ]
  }
]
```

**Permissions Required:** `can_read` on departments

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.get_department_hierarchy \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json"
```

---

### Get Department Settings

Get department settings (all or specific key).

**Endpoint:** `/api/method/blkshp_os.api.departments.get_department_settings`

**Method:** `GET` or `POST`

**Parameters:**
- `department` (string, required): Department name/ID
- `setting_key` (string, optional): Specific setting key. If not provided, returns all settings.

**Response (all settings):**
```json
{
  "eoq_enabled": true,
  "eoq_calculation_method": "wilson",
  "default_ordering_day": "Monday",
  "minimum_order_amount": 100.0,
  "require_order_approval": false
}
```

**Response (specific key):**
```json
"Monday"
```

**Permissions Required:** `can_read` on the department

**Example:**
```bash
# Get all settings
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.get_department_settings \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"department": "DEPT-001"}'

# Get specific setting
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.get_department_settings \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"department": "DEPT-001", "setting_key": "default_ordering_day"}'
```

---

### Update Department Settings

Update department settings.

**Endpoint:** `/api/method/blkshp_os.api.departments.update_department_settings`

**Method:** `POST`

**Parameters:**
- `department` (string, required): Department name/ID
- `settings` (object, required): Dictionary of settings to update

**Request Body:**
```json
{
  "department": "DEPT-001",
  "settings": {
    "eoq_enabled": true,
    "minimum_order_amount": 150.0,
    "default_ordering_day": "Tuesday"
  }
}
```

**Response:**
```json
{
  "eoq_enabled": true,
  "eoq_calculation_method": "wilson",
  "minimum_order_amount": 150.0,
  "default_ordering_day": "Tuesday",
  "require_order_approval": false
}
```

**Permissions Required:** `can_write` on the department

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.update_department_settings \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "department": "DEPT-001",
    "settings": {
      "eoq_enabled": true,
      "minimum_order_amount": 150.0
    }
  }'
```

---

### Assign Products to Department

Bulk assign products to a department.

**Endpoint:** `/api/method/blkshp_os.api.departments.assign_products_to_department`

**Method:** `POST`

**Parameters:**
- `department` (string, required): Department name/ID
- `products` (array, required): List of product names/IDs
- `is_primary` (boolean, optional): Mark as primary department. Default: `false`
- `par_level` (float, optional): Default par level for all products
- `order_quantity` (float, optional): Default order quantity for all products

**Request Body:**
```json
{
  "department": "DEPT-001",
  "products": ["PROD-001", "PROD-002", "PROD-003"],
  "is_primary": true,
  "par_level": 50.0,
  "order_quantity": 100.0
}
```

**Response:**
```json
{
  "success": ["PROD-001", "PROD-002"],
  "failed": [
    {
      "product": "PROD-003",
      "reason": "Already assigned to department"
    }
  ],
  "total": 3
}
```

**Permissions Required:** `can_write` on the department

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.assign_products_to_department \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "department": "DEPT-001",
    "products": ["PROD-001", "PROD-002"],
    "is_primary": true,
    "par_level": 50.0
  }'
```

---

### Get Department Statistics

Get statistics for a department.

**Endpoint:** `/api/method/blkshp_os.api.departments.get_department_statistics`

**Method:** `GET` or `POST`

**Parameters:**
- `department` (string, required): Department name/ID

**Response:**
```json
{
  "department": "DEPT-001",
  "product_count": 45,
  "user_count": 12,
  "inventory_value": 15234.50,
  "child_department_count": 3
}
```

**Permissions Required:** `can_read` on the department

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.departments.get_department_statistics \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"department": "DEPT-001"}'
```

---

## Permission Flags

The following permission flags are used throughout the API:

- `can_read`: View department data
- `can_write`: Modify department data
- `can_create`: Create new records in department
- `can_delete`: Delete records in department
- `can_submit`: Submit documents in department
- `can_cancel`: Cancel documents in department
- `can_approve`: Approve documents in department

---

## Error Responses

All API endpoints may return the following error responses:

### 403 Forbidden
```json
{
  "exc_type": "PermissionError",
  "exception": "You do not have permission to view this department"
}
```

### 404 Not Found
```json
{
  "exc_type": "DoesNotExistError",
  "exception": "Department DEPT-001 does not exist"
}
```

### 400 Bad Request
```json
{
  "exc_type": "ValidationError",
  "exception": "Department is required"
}
```

### 500 Internal Server Error
```json
{
  "exc_type": "Exception",
  "exception": "An unexpected error occurred"
}
```

---

## Rate Limiting

API requests are subject to Frappe's standard rate limiting policies. Consult your system administrator for specific limits.

---

## Changelog

### Version 1.0.0 (2025-11-08)
- Initial release
- Department API endpoints
- Permission-based access control
- Department hierarchy support
- Settings management
- Product assignment
- Statistics and reporting

