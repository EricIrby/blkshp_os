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

## Core Platform API

### Get Feature Matrix

Retrieve subscription plan metadata, module availability, and feature toggles for the authenticated tenant user. Feature administration remains a BLKSHP Operations responsibility and the response is read-only.

**Endpoint:** `/api/method/blkshp_os.api.core_platform.get_feature_matrix`

**Method:** `GET` or `POST`

**Parameters:**
- `refresh` (int, optional): When set to `1`, bypasses cached plan data before building the matrix. Defaults to `0` (use cached data when available).

**Response:**
```json
{
  "plan_code": "FOUNDATION",
  "plan": {
    "code": "FOUNDATION",
    "label": "Foundation Plan",
    "is_active": true,
    "is_default": true,
    "billing_currency": "USD"
  },
  "modules": [
    {
      "key": "core",
      "label": "Core",
      "is_enabled": true,
      "is_required": true,
      "depends_on": [],
      "feature_overrides": {},
      "user_has_access": true
    }
  ],
  "enabled_modules": ["core", "inventory"],
  "user_accessible_modules": ["core", "inventory"],
  "feature_states": {
    "core.workspace.access": true
  },
  "user_feature_access": {
    "core.workspace.access": true
  },
  "administration": {
    "managed_by": "BLKSHP Operations",
    "message": "Feature toggles are administered solely by BLKSHP Operations."
  },
  "generated_at": "2025-11-11 12:34:56.000000",
  "user": {
    "id": "matrix.user@example.com",
    "company": "Matrix Test Company",
    "roles": ["Employee"]
  }
}
```

**Example:**
```bash
curl -X GET https://your-site.com/api/method/blkshp_os.api.core_platform.get_feature_matrix \
  -H "Authorization: token api_key:api_secret"
```

---

### Get Profile

Return a read-only profile summary for the current user, including company assignment, department permissions, subscription snapshot, and permission catalog.

**Endpoint:** `/api/method/blkshp_os.api.core_platform.get_profile`

**Method:** `GET` or `POST`

**Parameters:**
- `refresh` (int, optional): When set to `1`, bypasses cached plan data prior to assembling the profile. Defaults to `0`.

**Response:**
```json
{
  "user": {
    "id": "matrix.user@example.com",
    "full_name": "Matrix User",
    "email": "matrix.user@example.com",
    "enabled": true,
    "roles": ["Employee"]
  },
  "company": "Matrix Test Company",
  "departments": [
    {
      "department": "MATRIX",
      "can_read": 1,
      "can_write": 0
    }
  ],
  "permissions": {
    "by_category": {
      "inventory": [{"permission_code": "inventory.audit.run"}],
      "system": []
    },
    "total": 12
  },
  "subscription": {
    "plan_code": "FOUNDATION",
    "plan": {
      "code": "FOUNDATION",
      "label": "Foundation Plan"
    },
    "modules": [
      {
        "key": "core",
        "label": "Core",
        "is_enabled": true,
        "user_has_access": true
      }
    ],
    "user_feature_access": {
      "core.workspace.access": true
    },
    "administration": {
      "managed_by": "BLKSHP Operations",
      "message": "Feature toggles are administered solely by BLKSHP Operations."
    }
  },
  "generated_at": "2025-11-11 12:34:56.000000"
}
```

**Example:**
```bash
curl -X GET https://your-site.com/api/method/blkshp_os.api.core_platform.get_profile \
  -H "Authorization: token api_key:api_secret"
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

## Recipe API

### Get Recipe Details

Fetch a recipe document including costing, department alignment, and allergen metadata.

**Endpoint:** `/api/resource/Recipe/<recipe_name>`

**Method:** `GET`

**Response (excerpt):**
```json
{
  "name": "RECIPE-00001",
  "recipe_name": "House Salsa",
  "department": "KITCHEN-TC1",
  "company": "Test Company",
  "yield_quantity": 4,
  "ingredients": [
    {
      "ingredient_type": "Product",
      "product": "PROD-00001",
      "quantity": 2,
      "unit": "each",
      "cost_per_unit": 1.5,
      "cost_total": 3.0
    }
  ],
  "allergens": [
    {
      "allergen": "Shellfish",
      "notes": null
    }
  ],
  "inherited_allergens": [
    {
      "allergen": "Gluten",
      "source_recipes": "RECIPE-00042"
    }
  ],
  "total_cost": 5.25,
  "cost_per_unit": 1.3125
}
```

**Notes:**
- `company` is enforced to match the owning department.
- `allergens` lists manual tags, while `inherited_allergens` captures allergens propagated from subrecipes alongside their sources.
- Use standard Frappe authentication headers (`Authorization: token api_key:api_secret`) to access the resource.

**Example:**
```bash
curl -X GET https://your-site.com/api/resource/Recipe/RECIPE-00001 \
  -H "Authorization: token api_key:api_secret"
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

---

## Roles & Permissions API

### Get Available Permissions

Get list of all available permissions in the system.

**Endpoint:** `/api/method/blkshp_os.api.roles.get_available_permissions`

**Method:** `GET` or `POST`

**Parameters:** None

**Response:**
```json
[
  {
    "code": "orders.view",
    "name": "View Orders",
    "description": "View purchase orders",
    "category": "Orders",
    "department_restricted": true
  }
]
```

**Example:**
```bash
curl -X GET https://your-site.com/api/method/blkshp_os.api.roles.get_available_permissions \
  -H "Authorization: token api_key:api_secret"
```

---

### Get Permissions by Category

Get permissions grouped by category or for a specific category.

**Endpoint:** `/api/method/blkshp_os.api.roles.get_permissions_by_category`

**Method:** `GET` or `POST`

**Parameters:**
- `category` (string, optional): Category name. If not provided, returns all categories.

**Response (all categories):**
```json
{
  "Orders": [
    {
      "code": "orders.view",
      "name": "View Orders",
      "description": "View purchase orders",
      "department_restricted": true
    }
  ],
  "Invoices": [...]
}
```

**Response (specific category):**
```json
[
  {
    "code": "orders.view",
    "name": "View Orders",
    "description": "View purchase orders",
    "department_restricted": true
  }
]
```

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.get_permissions_by_category \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"category": "Orders"}'
```

---

### Get User Permissions

Get all permissions for a user from all their roles.

**Endpoint:** `/api/method/blkshp_os.api.roles.get_user_permissions`

**Method:** `GET` or `POST`

**Parameters:**
- `user` (string, optional): User email. Defaults to current user.

**Response:**
```json
{
  "user": "user@example.com",
  "roles": ["Store Manager", "Buyer"],
  "permissions": {
    "orders.view": [
      {
        "role": "Store Manager",
        "permission_code": "orders.view",
        "permission_name": "View Orders",
        "permission_category": "Orders",
        "department_restricted": true
      }
    ]
  },
  "permissions_by_category": {
    "Orders": [
      {
        "code": "orders.view",
        "name": "View Orders",
        "description": "View purchase orders",
        "department_restricted": true,
        "granted_by_roles": ["Store Manager", "Buyer"]
      }
    ]
  },
  "total_permissions": 15
}
```

**Permissions Required:** System Manager (to view other users' permissions)

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.get_user_permissions \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"user": "user@example.com"}'
```

---

### Check Permission

Check if user has a specific permission.

**Endpoint:** `/api/method/blkshp_os.api.roles.check_permission`

**Method:** `GET` or `POST`

**Parameters:**
- `permission_code` (string, required): Permission code to check
- `user` (string, optional): User email. Defaults to current user.

**Response:**
```json
{
  "user": "user@example.com",
  "permission_code": "orders.view",
  "has_permission": true,
  "permission_name": "View Orders",
  "permission_category": "Orders",
  "department_restricted": true,
  "granted_by_roles": ["Store Manager", "Buyer"]
}
```

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.check_permission \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"permission_code": "orders.view"}'
```

---

### Get Role Permissions

Get all permissions for a specific role.

**Endpoint:** `/api/method/blkshp_os.api.roles.get_role_permissions`

**Method:** `GET` or `POST`

**Parameters:**
- `role` (string, required): Role name

**Response:**
```json
{
  "role": "Store Manager",
  "permissions": [
    {
      "permission_code": "orders.view",
      "permission_name": "View Orders",
      "permission_category": "Orders",
      "description": "View purchase orders",
      "department_restricted": true
    }
  ],
  "summary": {
    "role": "Store Manager",
    "description": "For general managers with broad access",
    "is_custom": true,
    "user_count": 5,
    "permission_count": 20,
    "permissions_by_category": {
      "Orders": 5,
      "Invoices": 3,
      "Audits": 4
    }
  }
}
```

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.get_role_permissions \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"role": "Store Manager"}'
```

---

### Create Custom Role

Create a new custom role with specified permissions.

**Endpoint:** `/api/method/blkshp_os.api.roles.create_custom_role`

**Method:** `POST`

**Parameters:**
- `role_name` (string, required): Name of the role
- `permissions` (array, optional): List of permission codes
- `description` (string, optional): Role description

**Request Body:**
```json
{
  "role_name": "Custom Buyer",
  "permissions": ["orders.view", "orders.create", "orders.place"],
  "description": "Custom role for buyers with limited permissions"
}
```

**Response:**
```json
{
  "role": "Custom Buyer",
  "message": "Role Custom Buyer created successfully",
  "permissions_count": 3
}
```

**Permissions Required:** System Manager

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.create_custom_role \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "role_name": "Custom Buyer",
    "permissions": ["orders.view", "orders.create"],
    "description": "Custom buyer role"
  }'
```

---

### Update Role Permissions

Update permissions for an existing role.

**Endpoint:** `/api/method/blkshp_os.api.roles.update_role_permissions`

**Method:** `POST`

**Parameters:**
- `role` (string, required): Role name
- `permissions` (array, required): List of permission codes
- `replace` (boolean, optional): If true, replace all permissions. Default: false

**Request Body:**
```json
{
  "role": "Custom Buyer",
  "permissions": ["orders.edit", "orders.delete"],
  "replace": false
}
```

**Response:**
```json
{
  "role": "Custom Buyer",
  "message": "Role permissions updated successfully",
  "permissions_count": 5
}
```

**Permissions Required:** System Manager

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.update_role_permissions \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Custom Buyer",
    "permissions": ["orders.edit"],
    "replace": false
  }'
```

---

### Revoke Permission

Revoke a specific permission from a role.

**Endpoint:** `/api/method/blkshp_os.api.roles.revoke_permission`

**Method:** `POST`

**Parameters:**
- `role` (string, required): Role name
- `permission_code` (string, required): Permission code to revoke

**Request Body:**
```json
{
  "role": "Custom Buyer",
  "permission_code": "orders.delete"
}
```

**Response:**
```json
{
  "role": "Custom Buyer",
  "permission_code": "orders.delete",
  "message": "Permission revoked successfully",
  "permissions_count": 4
}
```

**Permissions Required:** System Manager

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.revoke_permission \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "role": "Custom Buyer",
    "permission_code": "orders.delete"
  }'
```

---

### Clone Role

Clone an existing role with all its permissions.

**Endpoint:** `/api/method/blkshp_os.api.roles.clone_role`

**Method:** `POST`

**Parameters:**
- `source_role` (string, required): Role to clone from
- `new_role_name` (string, required): Name for the new role
- `description` (string, optional): Description for the new role

**Request Body:**
```json
{
  "source_role": "Store Manager",
  "new_role_name": "Assistant Manager",
  "description": "Assistant manager with similar permissions"
}
```

**Response:**
```json
{
  "role": "Assistant Manager",
  "source_role": "Store Manager",
  "message": "Role Assistant Manager cloned from Store Manager",
  "permissions_count": 20
}
```

**Permissions Required:** System Manager

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.clone_role \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "source_role": "Store Manager",
    "new_role_name": "Assistant Manager"
  }'
```

---

### Search Permissions

Search permissions by name, description, or code.

**Endpoint:** `/api/method/blkshp_os.api.roles.search_permissions`

**Method:** `GET` or `POST`

**Parameters:**
- `query` (string, required): Search query

**Response:**
```json
[
  {
    "code": "orders.view",
    "name": "View Orders",
    "description": "View purchase orders",
    "category": "Orders",
    "department_restricted": true
  }
]
```

**Example:**
```bash
curl -X POST https://your-site.com/api/method/blkshp_os.api.roles.search_permissions \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"query": "order"}'
```

---

## Permission Categories

The following permission categories are available:

- **Orders** - Purchase order management
- **Invoices** - Invoice processing and approval
- **Audits** - Inventory audits and counting
- **Items** - Product/item management
- **Vendors** - Vendor management
- **Recipes** - Recipe creation and management
- **Transfers** - Inventory transfers between departments
- **Depletions** - Manual depletion tracking
- **Reports** - Reporting and analytics
- **System** - System settings and administration
- **Director** - Director-level multi-location operations

---

## Standard Roles

The following standard roles are provided as templates:

- **Inventory Taker** - Basic inventory counting
- **Inventory Administrator** - Full inventory management
- **Recipe Builder** - Recipe creation and management
- **Buyer** - Purchase order placement
- **Receiver** - Order receiving and invoice processing
- **Bartender** - Bar operations (beverage department)
- **Store Manager** - General store management
- **Director** - Multi-location corporate management

---

## Changelog

### Version 1.1.0 (2025-11-08)
- Added Roles & Permissions API
- 70+ granular permissions across 11 categories
- Custom role creation and management
- Role cloning and bulk operations
- Permission search functionality
- Standard role templates

### Version 1.0.0 (2025-11-08)
- Initial release
- Department API endpoints
- Permission-based access control
- Department hierarchy support
- Settings management
- Product assignment
- Statistics and reporting

