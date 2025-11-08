# BLKSHP OS Documentation

**Complete documentation for BLKSHP OS - A unified inventory management and cost control platform for hospitality operations.**

**Version:** 0.0.1  
**Architecture:** Frappe Desk-Only Application  
**Last Updated:** November 8, 2025

---

## 📚 Quick Navigation

- [What is BLKSHP OS?](#what-is-blkshp-os)
- [Quick Start](#quick-start)
- [First-Time Setup](#first-time-setup)
- [Architecture Overview](#architecture-overview)
- [Development Guide](#development-guide)
- [Documentation Structure](#documentation-structure)
- [Key Concepts](#key-concepts)

---

## What is BLKSHP OS?

BLKSHP OS is a **unified inventory management and cost control platform** built on Frappe Framework for hospitality companies (restaurants, bars, catering operations).

### Key Differentiators

**Unified Platform (Not Separate Platforms):**
- Single system for all product types (food, beverage, supplies, equipment)
- Department-based segmentation instead of separate applications
- One Product Master for everything
- Unified inventory tracking and reporting

**Department-Based Architecture:**
- Products can belong to multiple departments
- Users have department-specific access
- Inventory tracked per Product + Department
- Permissions are department-aware
- Reports filterable by department

**2D Inventory Model:**
- Inventory tracked by **Product + Department** only
- Storage locations are metadata for organization (not separate inventory buckets)
- Simplifies inventory calculations while maintaining visibility

**Hub-and-Spoke Unit Conversion:**
- All quantities stored in product's primary count unit
- Conversions calculated on-the-fly for display/entry
- Consistent, reliable unit handling across all domains

---

## Quick Start

### 🚀 Get Started in 5 Minutes

**Prerequisites:**
- Frappe Bench installed
- A test site created
- Terminal access

### Option 1: Automated Setup (Recommended)

```bash
cd /path/to/frappe-bench

# Step 1: Install the app (if first time)
bench --site mysite.local install-app blkshp_os

# Step 2: Run the automated setup script
cd apps/blkshp_os
./scripts/test.sh mysite.local

# Step 3: Set passwords for test users (optional)
cd /path/to/frappe-bench
bench --site mysite.local set-password buyer@test.com
bench --site mysite.local set-password inventory@test.com
bench --site mysite.local set-password manager@test.com

# Step 4: Start the server
bench start
```

### Option 2: Manual Setup

```bash
cd /path/to/frappe-bench

# Step 1: Install the app (if first time)
bench --site mysite.local install-app blkshp_os

# Step 2: Run migrations
bench --site mysite.local migrate

# Step 3: Clear cache and build
bench --site mysite.local clear-cache
bench build --app blkshp_os

# Step 4: Create test data (optional)
bench --site mysite.local execute blkshp_os.scripts.setup_test_data.setup_all

# Step 5: Start the server
bench start
```

### Access Your Site

1. Open: `http://localhost:8000`
2. Log in as **Administrator**
3. Find the **BLKSHP OS** workspace tile in Desk
4. Start exploring!

### Quick Tests

**Test 1: View Departments**
- Go to: **Home → Departments → Department**
- You should see: Kitchen, Bar, Catering, Office, Prep Kitchen

**Test 2: Check Permissions**
- Open browser console (F12)
- Run:

```javascript
frappe.call({
    method: 'blkshp_os.api.roles.get_available_permissions',
    callback: function(r) {
        console.log('Total Permissions:', r.message.length);
    }
});
```

**Expected:** 70+ permissions

---

## First-Time Setup

### 📦 Initial Installation Guide

If this is your **first time** installing BLKSHP OS, follow these steps carefully.

### Step 1: Verify App is in Bench

```bash
cd /path/to/frappe-bench
ls apps/

# You should see:
# - frappe
# - blkshp_os
# - (other apps)
```

### Step 2: Check Your Sites

```bash
# List all sites
ls sites/

# Common site names:
# - site1.local
# - localhost
# - mysite.local
```

### Step 3: Install the App

**⚠️ MOST IMPORTANT STEP:**

```bash
# Install the app on your site
bench --site mysite.local install-app blkshp_os
```

This command:
- ✅ Installs the app on the site
- ✅ Creates all DocTypes (Department, etc.)
- ✅ Loads fixtures (custom fields)
- ✅ Sets up database schema

### Step 4: Verify Installation

```bash
# Check installed apps
bench --site mysite.local list-apps

# Expected output:
# frappe
# blkshp_os
```

### Step 5: Create Test Data (Recommended)

```bash
bench --site mysite.local execute blkshp_os.scripts.setup_test_data.setup_all
```

This creates:
- ✅ Test Restaurant company
- ✅ 5 departments (Kitchen, Bar, Catering, Office, Prep Kitchen)
- ✅ 3 test users with different roles
- ✅ Standard roles with permissions

### Step 6: Set Passwords

```bash
bench --site mysite.local set-password buyer@test.com
bench --site mysite.local set-password inventory@test.com
bench --site mysite.local set-password manager@test.com
```

### Step 7: Start Server

```bash
bench start
```

Keep this terminal open - it needs to stay running.

### Step 8: Access and Test

1. Open: `http://localhost:8000`
2. Log in as Administrator
3. Go to: **Home → Departments → Department**
4. Verify test departments are created

### Common Installation Mistakes

**❌ Running commands before install-app:**
```bash
# WRONG - app not installed yet
bench --site mysite execute blkshp_os.scripts.setup_test_data.setup_all
```

**✅ Correct order:**
```bash
# RIGHT - install first
bench --site mysite install-app blkshp_os
# Then run other commands
bench --site mysite execute blkshp_os.scripts.setup_test_data.setup_all
```

**❌ Using wrong site name:**
```bash
# Check actual site name first
ls sites/
# Then use correct name
bench --site [correct-site-name] install-app blkshp_os
```

---

## Architecture Overview

### Frappe Desk-Only Application

BLKSHP OS is a **traditional Frappe Desk application** - not a separate frontend SPA.

**Why Desk-Only:**
- ✅ Business operations focus (back-office)
- ✅ Faster development using Frappe's built-in UI
- ✅ Proven approach (ERPNext, HRMS, etc.)
- ✅ Can add separate frontend later if needed

**Key Architecture Components:**

### Application Structure

```
blkshp_os/
├── blkshp_os/                    # Main Python package
│   ├── api/                      # Whitelisted API endpoints
│   ├── departments/              # Departments domain
│   │   └── doctype/
│   ├── permissions/              # Permissions domain
│   │   └── doctype/
│   ├── products/                 # Products domain (future)
│   ├── inventory/                # Inventory domain (future)
│   ├── procurement/              # Procurement domain (future)
│   ├── [other domains]/          # Additional domains
│   ├── config/                   # Desk configuration
│   ├── public/                   # Static assets (JS, CSS)
│   ├── scripts/                  # Utility scripts
│   ├── blkshp_os/                # Workspace module
│   │   └── workspace/
│   └── hooks.py                  # App configuration
├── docs/                         # Documentation
├── fixtures/                     # Fixtures (custom fields, roles)
├── scripts/                      # Standalone scripts
└── pyproject.toml                # Python project config
```

### Domain-Based Organization

**Implemented Domains:**
- ✅ **Departments** - Department management and segmentation
- ✅ **Permissions** - User management, roles, and permissions

**Planned Domains:**
- ⏳ **Products** - Unified product/item management
- ⏳ **Inventory** - Inventory tracking and audits
- ⏳ **Procurement** - Vendors, orders, invoices
- ⏳ **Recipes** - Recipe management and costing
- ⏳ **POS Integration** - POS connectivity and depletions
- ⏳ **Transfers & Depletions** - Inventory movements
- ⏳ **Analytics** - Reporting and analytics
- ⏳ **Accounting** - Accounting integration
- ⏳ **Budgets** - Budget management
- ⏳ **Payments** - Payment processing
- ⏳ **Director** - Multi-location management

### Core Principles

**1. Unified Platform**
- Single Product Master for all product types
- Department-based segmentation (not separate platforms)
- Unified inventory and reporting

**2. Department-Based Architecture**
- Products assigned to multiple departments (many-to-many)
- Users have department-specific access
- Permissions are department-aware
- All reports support department filtering

**3. 2D Inventory Model**
- Inventory = Product + Department
- Storage is metadata only (not separate inventory)
- Simplifies calculations, maintains visibility

**4. Hub-and-Spoke Unit Conversion**
- All quantities stored in primary count unit
- Conversions calculated on-the-fly
- Consistent unit handling across system

---

## Development Guide

### 🎯 Recommended Development Path

**Start with: Departments → Permissions → Products**

This follows the dependency chain and aligns with Phase 1 development.

### Phase 1: Foundation (Weeks 1-2)

**Step 1: Departments Domain** ✅ COMPLETE
- Zero dependencies (foundation)
- Required by all other domains
- Simple scope, quick wins

**Step 2: Permissions Domain** ✅ COMPLETE
- Depends on Departments
- Required for user access and security
- Role-based and department-based permissions

**Step 3: Products Domain** ⏳ NEXT
- Depends on Departments
- Required by Inventory, Procurement, Recipes
- Most complex domain (unit conversion, etc.)

### Phase 2: Core Functionality (Weeks 3-6)

**Step 4: Inventory Domain**
- Depends on: Products, Departments
- Core functionality for inventory tracking
- Theoretical inventory calculations

**Step 5: Procurement Domain**
- Depends on: Products, Departments
- Vendor management, ordering, invoicing
- Ottimate integration

**Step 6: Recipes Domain**
- Depends on: Products, Departments, Inventory
- Recipe management and costing
- Required for POS depletion calculations

### Phase 3: Integration (Weeks 7-8)

**Step 7: POS Integration**
- Depends on: Products, Recipes, Inventory
- POS connectivity and sales import
- Automatic depletion calculations

**Step 8: Transfers & Depletions**
- Depends on: Products, Departments, Inventory
- Inventory movements between departments
- Manual depletion tracking

### Development Workflow

**For Each Domain:**

1. **Read Documentation**
   - Domain README
   - Function documents
   - Cross-domain dependencies

2. **Create DocTypes**
   - Define fields and validation
   - Implement Python controllers
   - Create child tables if needed

3. **Implement Services**
   - Core business logic
   - API endpoints
   - Permission checks

4. **Write Tests**
   - Unit tests for validation
   - Integration tests for workflows
   - API endpoint tests

5. **Create Client Scripts**
   - Form enhancements
   - User experience improvements
   - Data validation

6. **Document Implementation**
   - Update implementation summaries
   - Document API endpoints
   - Create usage examples

### Development Tools

**Testing:**
```bash
# Run all tests
bench --site mysite.local run-tests --app blkshp_os

# Run domain-specific tests
bench --site mysite.local run-tests --app blkshp_os --module blkshp_os.departments

# Run single test file
bench --site mysite.local run-tests --app blkshp_os --module blkshp_os.departments.doctype.department.test_department
```

**Development Commands:**
```bash
# Clear cache
bench --site mysite.local clear-cache

# Build assets
bench build --app blkshp_os

# Run migrations
bench --site mysite.local migrate

# Restart server
bench restart
```

**Code Quality:**
```bash
# Format code with ruff
ruff format blkshp_os/

# Lint code
ruff check blkshp_os/

# Type checking (if using mypy)
mypy blkshp_os/
```

---

## Documentation Structure

### 📁 Complete Documentation Map

**Top-Level Docs (9 Essential):**
- **README.md** (this file) - Main entry point
- **DEVELOPMENT-GUIDE.md** - Complete development roadmap
- **TESTING-GUIDE.md** - Testing practices and examples
- **API-REFERENCE.md** - API documentation
- **GIT-WORKFLOW.md** - Git practices and branching
- **FIXTURES-INFO.md** - Fixtures reference
- **PERMISSION-FIELDS-REFERENCE.md** - Permission field reference
- **AGENT-INSTRUCTIONS.md** - AI agent development guide
- **CROSS-DOMAIN-REFERENCE.md** - Integration patterns

**Architecture Documentation:**
- **00-ARCHITECTURE/** - Architecture and framework guides
  - `README.md` - Architecture overview
  - `01-App-Structure.md` - Desk-only structure guide
  - `02-Frappe-Framework.md` - Frappe framework guide
  - `03-Deployment.md` - Deployment and scaling
  - `04-Separate-Frontend.md` - Future SPA architecture (reference)

**Domain Documentation:**
- **01-PRODUCTS/** - Product management (11 functions)
- **02-DEPARTMENTS/** - Department management (4 functions) ✅
- **03-INVENTORY/** - Inventory tracking (10 functions)
- **04-PROCUREMENT/** - Procurement (13 functions)
- **05-RECIPES/** - Recipe management (12 functions)
- **06-POS-INTEGRATION/** - POS integration (7 functions)
- **07-ACCOUNTING/** - Accounting (2 functions)
- **08-TRANSFERS-DEPLETIONS/** - Inventory movements (6 functions)
- **09-ANALYTICS-REPORTING/** - Reporting (9 functions)
- **10-DIRECTOR/** - Multi-location (TBD)
- **11-PERMISSIONS/** - Permissions (6 functions) ✅
- **12-BUDGETS/** - Budget management (3 functions)
- **13-PAYMENTS/** - Payment processing (TBD)
- **99-INTEGRATIONS/** - External integrations (4 functions)

### Reading Order

**For New Developers:**
1. **docs/README.md** (this file) - Start here
2. **00-ARCHITECTURE/01-App-Structure.md** - Understand structure
3. **DEVELOPMENT-GUIDE.md** - Development workflow
4. **Domain README.md** - Specific domain overview
5. **Function Documents** - Detailed implementations

**For AI Agents:**
1. **AGENT-INSTRUCTIONS.md** - Development guidelines
2. **docs/README.md** (this file) - Project overview
3. **CROSS-DOMAIN-REFERENCE.md** - Integration patterns
4. **Domain-specific docs** - Implementation details

**For Architecture Decisions:**
1. **00-ARCHITECTURE/README.md** - Architecture overview
2. **00-ARCHITECTURE/01-App-Structure.md** - Current structure
3. **00-ARCHITECTURE/04-Separate-Frontend.md** - Future SPA (if needed)

---

## Key Concepts

### Department-Based Segmentation

**What are Departments?**
- Organizational units within a company (Kitchen, Bar, Catering, etc.)
- Products can belong to multiple departments
- Users have access to specific departments
- Inventory tracked per Product + Department

**Why Departments?**
- Flexible organization without separate platforms
- Department-specific permissions and access control
- Department-based reporting and analytics
- Support for complex organizational structures

**Example:**
```
Company: Restaurant ABC
├── Kitchen (Department)
│   ├── Users: Chef, Line Cook
│   ├── Products: Flour, Chicken, Olive Oil
│   └── Inventory: Tracked separately
├── Bar (Department)
│   ├── Users: Bartender, Bar Manager
│   ├── Products: Vodka, Tonic, Limes
│   └── Inventory: Tracked separately
└── Office (Department)
    ├── Users: Manager, Accountant
    ├── Products: Paper, Pens
    └── Inventory: Tracked separately
```

### 2D Inventory Model

**Inventory = Product + Department**

- Inventory tracked by **Product + Department** combination only
- Storage locations are **metadata** for organization
- Storage helps with counting tasks but doesn't create separate inventory

**Example:**
```
Product: Coca Cola Cans
├── Bar Department
│   ├── Inventory: 240 cans (in primary unit)
│   ├── Storage: Walk-in Cooler (metadata)
│   └── Storage: Back Bar (metadata)
└── Catering Department
    ├── Inventory: 120 cans (in primary unit)
    └── Storage: Catering Storage (metadata)
```

**NOT:**
```
❌ WRONG: Separate inventory per storage location
Product: Coca Cola Cans
├── Walk-in Cooler: 100 cans
├── Back Bar: 140 cans
└── Catering Storage: 120 cans
```

### Hub-and-Spoke Unit Conversion

**All conversions flow through primary count unit (hub).**

**Example:**
```
Product: Beer (Draft)
├── Primary Unit: gallon
├── Purchase Unit: keg = 15.5 gallons
├── Serving Unit: pint = 0.125 gallons
└── Volume: ounce = 0.0078125 gallons

Conversion Flow:
keg → gallon (÷ 15.5) → pint (× 8)
pint → gallon (÷ 0.125) → keg (× 15.5)
```

**Storage Rule:**
- All quantities stored in primary count unit
- Conversions calculated on-the-fly for display/entry
- Use Product's `convert_to_primary_unit()` and `convert_from_primary_unit()` methods

### Theoretical Inventory

**Formula:**
```
Theoretical Inventory = 
    Starting Inventory (from last audit)
    + Received (from invoices)
    + Transferred In
    - Transferred Out
    - Depleted (sold, spilled, etc.)
```

**Key Points:**
- Calculated per **Product + Department**
- Storage location **NOT included**
- All quantities in **primary count unit**
- Recalculated on demand (not stored)

---

## What's Been Built

### Completed Domains (Phase 1)

#### ✅ Departments Domain

**DocTypes Created:**
- **Department** - Master DocType for departments
- **Department Permission** - Child table for user permissions
- **Product Department** - Child table for product assignments

**API Endpoints (7):**
- `get_accessible_departments` - Get departments user can access
- `get_department_details` - Get department with products/users
- `get_department_products` - Get products assigned to department
- `get_department_users` - Get users with access to department
- `get_department_statistics` - Get department statistics
- `check_department_access` - Check if user has access
- `get_department_hierarchy` - Get department tree

**Client Scripts:**
- `department.js` - Department form enhancements
- `user.js` - User form with department permissions

**Test Coverage:**
- `test_department.py` - Department validation tests
- `test_department_permission.py` - Permission validation tests
- `test_product_department.py` - Product assignment tests
- `test_departments_api.py` - API endpoint tests

#### ✅ Permissions Domain

**DocTypes Created:**
- **Role Permission** - Child table for custom role permissions

**Custom Fields Created:**
- `User.department_permissions` - Department Permission table
- `User.is_team_account` - Team account flag
- `Role.custom_permissions` - Role Permission table
- `Role.is_custom_role` - Custom role flag
- `Role.role_description` - Role description

**Permissions Defined (70+):**
- Orders (11 permissions)
- Invoices (13 permissions)
- Audits (8 permissions)
- Items (7 permissions)
- Vendors (6 permissions)
- Recipes (4 permissions)
- Transfers (4 permissions)
- Depletions (4 permissions)
- Reports (4 permissions)
- System (5 permissions)
- Director (8 permissions)

**Standard Roles (8):**
- Inventory Taker (3 permissions)
- Inventory Administrator (8 permissions)
- Recipe Builder (5 permissions)
- Buyer (7 permissions)
- Receiver (10 permissions)
- Bartender (6 permissions)
- Store Manager (21 permissions)
- Director (17 permissions)

**API Endpoints (13):**
- `get_available_permissions` - Get all available permissions
- `get_permissions_by_category` - Get permissions by category
- `get_permission_categories` - Get all categories
- `get_user_permissions` - Get user's effective permissions
- `check_permission` - Check if user has permission
- `get_role_permissions` - Get role's permissions
- `create_custom_role` - Create new custom role
- `update_role_permissions` - Update role permissions
- `revoke_permission` - Revoke permission from role
- `clone_role` - Clone role with permissions
- `get_role_summary` - Get role summary
- `search_permissions` - Search permissions
- `bulk_assign_permissions` - Bulk assign permissions

**Services:**
- `constants.py` - Permission registry
- `service.py` - Department permission service
- `user.py` - User permission mixin
- `query.py` - Permission queries
- `roles.py` - Role management service

**Client Scripts:**
- `role.js` - Role form enhancements
- `user.js` - User form with permissions (shared with Departments)

**Test Coverage:**
- `test_role_permission.py` - Role permission tests
- `test_permissions_service.py` - Service tests
- `test_roles.py` - Role management tests

### Fixtures Created

**Custom Fields (5):**
- User → Department Permissions
- User → Is Team Account
- Role → Custom Permissions
- Role → Is Custom Role
- Role → Role Description

**Standard Roles (8):**
- All role definitions with initial permissions
- Exported to `fixtures/standard_roles.json`

---

## Next Steps

### Immediate Priorities

1. **Begin Products Domain** ⏳ NEXT
   - Most complex domain (unit conversion, etc.)
   - Required by Inventory, Procurement, Recipes
   - See: `01-PRODUCTS/README.md`

2. **Review Architecture Documentation**
   - Read: `00-ARCHITECTURE/01-App-Structure.md`
   - Understand: Desk-only architecture
   - Review: Module organization patterns

3. **Study Cross-Domain Integration**
   - Read: `CROSS-DOMAIN-REFERENCE.md`
   - Understand: How domains interact
   - Review: Shared services and utilities

### Learning Resources

**Essential Reading:**
- **DEVELOPMENT-GUIDE.md** - Complete development roadmap
- **TESTING-GUIDE.md** - Testing practices
- **API-REFERENCE.md** - API documentation
- **CROSS-DOMAIN-REFERENCE.md** - Integration patterns

**Domain Implementation:**
- **02-DEPARTMENTS/IMPLEMENTATION-SUMMARY.md** - Departments implementation
- **11-PERMISSIONS/IMPLEMENTATION-SUMMARY.md** - Permissions implementation
- **01-PRODUCTS/README.md** - Products roadmap

**Architecture Reference:**
- **00-ARCHITECTURE/** - All architecture documentation
- **GIT-WORKFLOW.md** - Git practices
- **FIXTURES-INFO.md** - Fixtures guide

---

## Support & Resources

### Getting Help

**Common Issues:**
- Check: `TESTING-GUIDE.md` - Troubleshooting section
- Review: Error logs with `bench --site mysite logs`
- Search: Implementation summaries for examples
- Check: Test files for usage patterns

**Development Questions:**
- Review: `DEVELOPMENT-GUIDE.md`
- Check: `AGENT-INSTRUCTIONS.md` (for AI agents)
- Read: Domain README files
- Review: Function documents

**Architecture Questions:**
- Read: `00-ARCHITECTURE/` documentation
- Check: `CROSS-DOMAIN-REFERENCE.md`
- Review: `PROJECT-CONTEXT.md` (in architecture docs)

### Contributing

**Before Starting:**
1. Read this README completely
2. Review `DEVELOPMENT-GUIDE.md`
3. Read domain-specific README
4. Check `GIT-WORKFLOW.md`
5. Review existing implementations

**Development Process:**
1. Create feature branch
2. Implement functionality
3. Write tests
4. Update documentation
5. Submit pull request

---

## Summary

**BLKSHP OS is:**
- ✅ Unified inventory management platform
- ✅ Frappe Desk-only application
- ✅ Department-based architecture
- ✅ 2D inventory model (Product + Department)
- ✅ Hub-and-spoke unit conversion
- ✅ Modular domain structure

**Current Status:**
- ✅ Phase 1 Complete: Departments & Permissions
- ⏳ Phase 2 Starting: Products Domain
- 📚 Well-documented architecture and patterns
- 🧪 Comprehensive test coverage
- 🚀 Ready for core functionality development

**Get Started:**
1. Follow [First-Time Setup](#first-time-setup)
2. Run [Quick Start](#quick-start)
3. Read [Development Guide](#development-guide)
4. Begin implementing!

---

**Happy Coding! 🚀**

*For detailed implementation guides, see domain-specific documentation in their respective folders.*

