# BLKSHP OS Application Structure (Desk-Only)

**Current Architecture:** Frappe Desk-Only Application  
**Last Updated:** November 8, 2025

---

## Table of Contents

1. [Overview](#overview)
2. [Complete File Structure](#complete-file-structure)
3. [Directory Explanations](#directory-explanations)
4. [Module Organization](#module-organization)
5. [DocType Patterns](#doctype-patterns)
6. [Development Workflow](#development-workflow)
7. [When to Add Separate Frontend](#when-to-add-separate-frontend)

---

## Overview

BLKSHP OS is a **traditional Frappe Desk application** that leverages Frappe's built-in UI framework for all functionality. This approach:

- ✅ Provides rapid development using Frappe's DocType system
- ✅ Offers proven UI patterns for business operations
- ✅ Enables backend and frontend development in one framework
- ✅ Supports future migration to separate frontend if needed

### Architecture Components

- **Frappe Desk UI** - Built-in forms, lists, reports
- **Python Backend** - DocTypes, API endpoints, business logic
- **Client Scripts** - JavaScript enhancements for forms (.js files)
- **Server Scripts** - Python automation and workflows
- **REST API** - Auto-generated + custom whitelisted methods
- **First-Class DocTypes** - Every business entity lives under `blkshp_os` (no reliance on ERPNext or other apps)

### Access Points

- **Frappe Desk**: `http://yoursite.com/app` - Main UI
- **DocType Forms**: `http://yoursite.com/app/department/DEPT-001`
- **Lists**: `http://yoursite.com/app/list/Department`
- **Reports**: `http://yoursite.com/app/query-report/Inventory Balance`
- **API**: `http://yoursite.com/api/method/blkshp_os.api.departments.get_accessible_departments`

---

## Complete File Structure

```
blkshp_os/                              # Root directory
├── MANIFEST.in                         # Python package manifest
├── README.md                           # App documentation
├── license.txt                         # License file
├── pyproject.toml                      # Modern Python package config
│
├── blkshp_os/                          # Main Python package
│   ├── __init__.py                     # Package initialization (version)
│   ├── hooks.py                        # ⭐ CRITICAL: App configuration
│   ├── modules.txt                     # List of modules
│   ├── patches.txt                     # Database migration patches
│   │
│   ├── config/                         # Desk configuration
│   │   ├── __init__.py
│   │   └── desktop.py                  # Workspace tiles
│   │
│   ├── api/                            # ⭐ Whitelisted API endpoints
│   │   ├── __init__.py
│   │   ├── departments.py              # Department APIs
│   │   ├── roles.py                    # Role/Permission APIs
│   │   └── test_departments_api.py     # API tests
│   │
│   ├── departments/                    # ⭐ Departments domain module
│   │   ├── __init__.py
│   │   │
│   │   └── doctype/                    # Domain DocTypes
│   │       ├── __init__.py
│   │       │
│   │       ├── department/             # Department Master DocType
│   │       │   ├── __init__.py
│   │       │   ├── department.py       # Python controller
│   │       │   ├── department.json     # DocType metadata
│   │       │   ├── department.js       # Client-side form script
│   │       │   └── test_department.py  # Unit tests
│   │       │
│   │       └── product_department/     # Product Department Child Table
│   │           ├── __init__.py
│   │           ├── product_department.py
│   │           ├── product_department.json
│   │           └── test_product_department.py
│   │
│   ├── permissions/                    # ⭐ Permissions domain module
│   │   ├── __init__.py
│   │   ├── constants.py                # Permission registry (70+ permissions)
│   │   ├── service.py                  # Department permission service
│   │   ├── user.py                     # User permission mixin
│   │   ├── query.py                    # Permission queries
│   │   ├── roles.py                    # Role management service
│   │   ├── test_permissions_service.py
│   │   ├── test_roles.py
│   │   │
│   │   └── doctype/                    # Domain DocTypes
│   │       ├── __init__.py
│   │       │
│   │       ├── department_permission/  # Department Permission Child Table
│   │       │   ├── __init__.py
│   │       │   ├── department_permission.py
│   │       │   ├── department_permission.json
│   │       │   └── test_department_permission.py
│   │       │
│   │       └── role_permission/        # Role Permission Child Table
│   │           ├── __init__.py
│   │           ├── role_permission.py
│   │           ├── role_permission.json
│   │           └── test_role_permission.py
│   │
│   ├── products/                       # Products domain (future)
│   │   └── __init__.py
│   ├── inventory/                      # Inventory domain (future)
│   │   └── __init__.py
│   ├── procurement/                    # Procurement domain (future)
│   │   └── __init__.py
│   ├── recipes/                        # Recipes domain (future)
│   │   └── __init__.py
│   ├── pos_integration/                # POS Integration (future)
│   │   └── __init__.py
│   ├── accounting/                     # Accounting (future)
│   │   └── __init__.py
│   ├── transfers_depletions/           # Transfers & Depletions (future)
│   │   └── __init__.py
│   ├── analytics/                      # Analytics (future)
│   │   └── __init__.py
│   ├── budgets/                        # Budgets (future)
│   │   └── __init__.py
│   ├── payments/                       # Payments (future)
│   │   └── __init__.py
│   ├── director/                       # Multi-location (future)
│   │   └── __init__.py
│   │
│   ├── blkshp_os/                      # ⭐ Default module (workspace)
│   │   ├── __init__.py
│   │   │
│   │   └── workspace/                  # Custom workspaces
│   │       ├── __init__.py
│   │       └── blkshp_os/
│   │           └── blkshp_os.json      # BLKSHP OS workspace definition
│   │
│   ├── public/                         # Static assets (served by nginx)
│   │   ├── css/
│   │   │   └── blkshp_os.css           # Custom styles (optional)
│   │   │
│   │   ├── js/
│   │   │   ├── role.js                 # Role form enhancements
│   │   │   └── user.js                 # User form enhancements
│   │   │
│   │   └── images/
│   │       └── favicon.ico             # App icon
│   │
│   ├── templates/                      # Jinja templates
│   │   ├── __init__.py
│   │   ├── includes/                   # Reusable template parts
│   │   ├── pages/                      # Full page templates
│   │   └── emails/                     # Email templates (optional)
│   │
│   └── scripts/                        # Utility scripts
│       ├── __init__.py
│       └── sync_doctypes.py            # DocType sync script
│
├── docs/                               # Documentation
│   ├── README.md                       # Main documentation entry
│   ├── 00-ARCHITECTURE/                # Architecture documentation
│   ├── 01-PRODUCTS/                    # Domain documentation
│   ├── 02-DEPARTMENTS/
│   ├── 03-INVENTORY/
│   ├── [other domains]/
│   └── [other docs]/
│
├── fixtures/                           # Fixtures (exported data)
│   ├── custom_field.json               # Custom fields
│   └── standard_roles.json             # Standard roles
│
├── scripts/                            # Standalone scripts
│   ├── __init__.py
│   ├── setup_test_data.py              # Test data setup
│   ├── test.sh                         # Testing script
│   └── README.md
│
└── [other root files]/
```

---

## Directory Explanations

### Root Level Files

#### `pyproject.toml`

Modern Python package configuration (replaces setup.py).

```toml
[project]
name = "blkshp_os"
authors = [
    { name = "BLKSHP Advisory", email = "blkshp-os@blkshp.co"}
]
description = "A business operating system for hospitality companies"
requires-python = ">=3.10"
readme = "README.md"
dynamic = ["version"]

[build-system]
requires = ["flit_core >=3.4,<4"]
build-backend = "flit_core.buildapi"
```

#### `MANIFEST.in`

Specifies which non-Python files to include in the package.

```
include MANIFEST.in
include *.txt
include *.md
include *.toml
recursive-include blkshp_os *.css
recursive-include blkshp_os *.html
recursive-include blkshp_os *.ico
recursive-include blkshp_os *.js
recursive-include blkshp_os *.json
recursive-include blkshp_os *.md
recursive-include blkshp_os *.png
recursive-include blkshp_os *.py
recursive-include blkshp_os *.svg
recursive-exclude blkshp_os *.pyc
```

### Backend Python Package (`blkshp_os/`)

This directory contains all Frappe backend code.

#### `hooks.py` ⭐ CRITICAL

The most important configuration file - defines app behavior, routing, and integration points.

```python
app_name = "blkshp_os"
app_title = "BLKSHP OS"
app_publisher = "BLKSHP Advisory"
app_description = "A business operating system for hospitality companies"
app_license = "mit"
app_version = "0.0.1"

# Fixtures (exported data)
fixtures = [
    {
        "dt": "Custom Field",
        "filters": [["name", "in", [
            "User-department_permissions",
            "User-is_team_account",
            "Role-custom_permissions",
            "Role-is_custom_role",
            "Role-role_description"
        ]]],
    }
]

# Permission query filters
permission_query_conditions = {
    "Department": "blkshp_os.permissions.query.department_permission_query",
}

# Extend DocType classes
extend_doctype_class = {
    "User": "blkshp_os.permissions.user.UserPermissionMixin",
}

# Client scripts for standard DocTypes
doctype_js = {
    "User": "public/js/user.js",
    "Role": "public/js/role.js"
}
```

#### `modules.txt`

Lists all modules in your app (one per line). Each module groups related DocTypes.

```
BLKSHP OS
Departments
Products
Inventory
Procurement
Recipes
POS Integration
Transfers and Depletions
Analytics
Accounting
Budgets
Payments
Director
Permissions
```

#### `config/desktop.py`

Defines workspace tiles shown in Frappe Desk.

```python
from frappe import _

def get_data():
    return [
        {
            "module_name": "BLKSHP OS",
            "category": "Modules",
            "label": _("BLKSHP OS"),
            "color": "blue",
            "icon": "octicon octicon-package",
            "type": "module",
            "description": _("Inventory management and cost control")
        }
    ]
```

### Domain Modules

Each domain (Departments, Products, Inventory, etc.) is organized as a Python module with:

**Module Structure:**
```
domain_name/
├── __init__.py                # Module initialization
├── [service files]            # Shared services (e.g., service.py, query.py)
└── doctype/                   # DocTypes for this domain
    ├── __init__.py
    ├── doctype_1/
    │   ├── __init__.py
    │   ├── doctype_1.py       # Python controller
    │   ├── doctype_1.json     # DocType metadata
    │   ├── doctype_1.js       # Client script (optional)
    │   └── test_doctype_1.py  # Unit tests (optional)
    └── doctype_2/
        └── [same pattern]
```

**Example: Departments Domain**
```
departments/
├── __init__.py
└── doctype/
    ├── department/             # Master DocType
    └── product_department/     # Child Table
```

**Example: Permissions Domain (with services)**
```
permissions/
├── __init__.py
├── constants.py                # Shared: Permission registry
├── service.py                  # Shared: Permission service
├── user.py                     # Shared: User mixin
├── query.py                    # Shared: Permission queries
├── roles.py                    # Shared: Role management
└── doctype/
    ├── department_permission/  # Child Table
    └── role_permission/        # Child Table
```

---

## Module Organization

### Domain Modules vs. Frappe Modules

**Domain Modules** (Python packages):
- Organize code by business domain
- Located at `blkshp_os/domain_name/`
- Contain DocTypes, services, and tests
- Examples: `departments/`, `permissions/`, `products/`
- Must include the full DocType stack (JSON, controller, tests). BLKSHP OS does **not** depend on DocTypes shipped by ERPNext/Helpdesk/etc.; if the platform needs `Company`, `Vendor`, or similar masters they must be defined inside this app (e.g. `director/doctype/company`).

**Frappe Modules** (metadata):
- Organize DocTypes in Frappe UI
- Listed in `modules.txt`
- Shown in Desk navigation
- Examples: "Departments", "Products", "Inventory"

**Relationship:**
- One domain module can span multiple Frappe modules
- One Frappe module can contain DocTypes from multiple domains
- Generally: 1 domain module = 1 Frappe module

### Standard Patterns

**Pattern 1: Simple Domain**
```
departments/                    # Domain module
├── __init__.py
└── doctype/
    ├── department/             # Frappe module: "Departments"
    └── product_department/     # Frappe module: "Departments"
```

**Pattern 2: Domain with Shared Services**
```
permissions/                    # Domain module
├── __init__.py
├── service.py                  # Shared across domain
├── query.py                    # Shared across domain
└── doctype/
    ├── department_permission/  # Frappe module: "Permissions"
    └── role_permission/        # Frappe module: "Permissions"
```

**Pattern 3: Cross-Domain Shared**
```
api/                            # Shared API layer
├── __init__.py
├── departments.py              # Department domain APIs
└── roles.py                    # Permissions domain APIs
```

---

## DocType Patterns

### DocType Directory Structure

Each DocType lives in its own directory:

```
doctype_name/
├── __init__.py                 # Makes it a Python package
├── doctype_name.py             # Python controller (business logic)
├── doctype_name.json           # Metadata (fields, permissions, etc.)
├── doctype_name.js             # Client-side form scripts (optional)
└── test_doctype_name.py        # Unit tests (optional)
```

> **Important:** Always create the controller (`doctype_name.py`) and export the JSON. Stubs are acceptable, but the files must exist so installations that only include BLKSHP OS can migrate without pulling in other apps.

### Python Controller (`doctype_name.py`)

```python
import frappe
from frappe import _
from frappe.model.document import Document

class Department(Document):
    """Department Master DocType"""
    
    def validate(self):
        """Validation before save"""
        self._validate_department_code()
        self._validate_company()
    
    def _validate_department_code(self):
        """Ensure department code is unique per company"""
        if frappe.db.exists("Department", {
            "department_code": self.department_code,
            "company": self.company,
            "name": ("!=", self.name)
        }):
            frappe.throw(_("Department code already exists for this company"))
    
    def _validate_company(self):
        """Validate company exists"""
        if not frappe.db.exists("Company", self.company):
            frappe.throw(_("Company {0} does not exist").format(self.company))
```

### DocType Metadata (`.json`)

Generated by Frappe - defines fields, permissions, behavior:

```json
{
  "autoname": "field:department_code",
  "document_type": "Master",
  "module": "Departments",
  "fields": [
    {
      "fieldname": "department_name",
      "fieldtype": "Data",
      "label": "Department Name",
      "reqd": 1
    }
  ],
  "permissions": [...]
}
```

### Client Script (`.js`)

Enhances form behavior client-side:

```javascript
frappe.ui.form.on('Department', {
    refresh: function(frm) {
        if (!frm.is_new()) {
            frm.add_custom_button(__('View Products'), function() {
                frappe.set_route('List', 'Product', {
                    'departments.department': frm.doc.name
                });
            });
        }
    },
    
    department_code: function(frm) {
        // Auto-uppercase
        if (frm.doc.department_code) {
            frm.set_value('department_code', 
                         frm.doc.department_code.toUpperCase());
        }
    }
});
```

---

## Development Workflow

### Creating a New Domain

**Step 1: Create Domain Module**

```bash
cd blkshp_os/
mkdir new_domain
cd new_domain
touch __init__.py
mkdir doctype
cd doctype
touch __init__.py
```

**Step 2: Add to modules.txt**

```
# blkshp_os/modules.txt
BLKSHP OS
Departments
New Domain    # Add this line
```

**Step 3: Create DocTypes via Desk**

1. Go to Desk → Customize → DocType → New
2. Set Module = "New Domain"
3. Define fields
4. Save

**Step 4: Export DocType**

```bash
bench --site mysite.local export-doc "New DocType" "New DocType Name"
```

**Step 5: Create Python Controller**

```bash
cd blkshp_os/new_domain/doctype/new_doctype/
# Edit new_doctype.py with business logic
```

**Step 6: Add Tests**

```bash
# Create test_new_doctype.py
```

**Step 7: Run Tests**

```bash
bench --site mysite.local run-tests --app blkshp_os --module blkshp_os.new_domain
```

### Making Changes

**Backend Changes:**
```bash
# Edit Python files
# Run migrations
bench --site mysite.local migrate

# Clear cache
bench --site mysite.local clear-cache

# Restart
bench restart
```

**Client Script Changes:**
```bash
# Edit .js files in public/js/ or doctype directories

# Build assets
bench build --app blkshp_os

# Clear cache
bench --site mysite.local clear-cache
```

**DocType Metadata Changes:**
```bash
# Make changes in Desk UI
# Export to JSON
bench --site mysite.local export-doc "DocType" "DocType Name"

# Or sync from JSON
bench --site mysite.local migrate
```

---

## When to Add Separate Frontend

### Current Architecture is Ideal For:

- ✅ Business operations and back-office functions
- ✅ Internal user applications
- ✅ Admin panels and management tools
- ✅ Data entry and reporting
- ✅ Workflow-heavy applications
- ✅ Rapid development and iteration

### Consider Separate Frontend When:

- Customer-facing portals required
- Mobile-first experience needed
- Modern SPA performance critical
- Highly customized UI/UX required
- External user access (non-employees)
- Complex interactive visualizations
- Real-time collaborative features

### Migration Path

If you need to add a separate frontend in the future:

1. **Keep Current Backend** - All DocTypes and API endpoints remain
2. **Add Frontend Directory** - Add `frontend/` with Vue/React/etc.
3. **Build Process** - Configure Vite to build to `www/` directory
4. **Routing** - Add `website_route_rules` in `hooks.py`
5. **API Integration** - Frontend calls existing API endpoints

**See:** `04-Separate-Frontend.md` for complete SPA architecture guide

---

## Best Practices

### Code Organization

✅ **DO:**
- Group related DocTypes in domain modules
- Create shared services at module root
- Use descriptive module and DocType names
- Follow Frappe naming conventions
- Keep Python controllers focused

❌ **DON'T:**
- Mix unrelated functionality in one module
- Duplicate code across modules
- Create overly complex inheritance hierarchies
- Bypass Frappe's built-in features

### API Design

✅ **DO:**
- Use `@frappe.whitelist()` for public APIs
- Validate all inputs
- Return consistent response formats
- Handle errors gracefully
- Document API endpoints

❌ **DON'T:**
- Expose internal methods
- Skip permission checks
- Return raw database results
- Ignore error cases
- Forget CSRF protection

### Testing

✅ **DO:**
- Write unit tests for business logic
- Test validation rules
- Test API endpoints
- Test permission checks
- Use fixtures for test data

❌ **DON'T:**
- Skip writing tests
- Test only happy paths
- Ignore edge cases
- Commit broken tests
- Test implementation details

---

## Quick Reference

### Important Files

| File | Purpose |
|------|---------|
| `hooks.py` | App configuration, routing, hooks |
| `modules.txt` | Module list for Desk UI |
| `config/desktop.py` | Workspace tiles |
| `pyproject.toml` | Python package config |
| `fixtures/*.json` | Exported custom fields, roles |

### Common Commands

```bash
# Install app
bench --site mysite install-app blkshp_os

# Run migrations
bench --site mysite migrate

# Clear cache
bench --site mysite clear-cache

# Build assets
bench build --app blkshp_os

# Run tests
bench --site mysite run-tests --app blkshp_os

# Export DocType
bench --site mysite export-doc "DocType" "DocType Name"
```

### Directory Patterns

```
# Master DocType in domain module
blkshp_os/domain/doctype/master_name/

# Child Table in domain module
blkshp_os/domain/doctype/child_name/

# Shared services
blkshp_os/domain/service.py

# API endpoints
blkshp_os/api/domain_name.py

# Client scripts (global)
blkshp_os/public/js/doctype_name.js
```

---

## Summary

BLKSHP OS uses a **Frappe Desk-only architecture** with:

- ✅ Domain-based module organization
- ✅ DocTypes for all data models
- ✅ Python controllers for business logic
- ✅ Client scripts for form enhancements
- ✅ Centralized API layer
- ✅ Comprehensive test coverage
- ✅ Clear separation of concerns

This architecture provides a solid foundation for rapid development while maintaining flexibility for future enhancements, including potential migration to a separate frontend if requirements change.

---

**For separate frontend architecture (future reference):** See `04-Separate-Frontend.md`  
**For domain-specific structures:** See domain `README.md` files  
**For deployment guide:** See `03-Deployment.md`

**Last Updated:** November 8, 2025

