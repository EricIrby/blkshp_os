# PRODUCT REQUIREMENTS DOCUMENT (PRD)
# BLKSHP OS - Hospitality Business Operating System

**Version:** 1.0
**Date:** November 13, 2025
**Status:** Active Development (Phase 2)

---

## EXECUTIVE SUMMARY

**Product Name:** BLKSHP OS
**Version:** 0.0.1
**Platform:** Frappe Framework v15+ / ERPNext
**Architecture:** Frappe Desk (Backend) + Next.js SPA (Frontend, Planned)
**License:** MIT
**Target Market:** Hospitality operations (restaurants, bars, catering companies)

BLKSHP OS is a unified business operating system for hospitality operations built on the Frappe Framework. It provides comprehensive inventory management, cost control, procurement, recipes, POS integration, and multi-location management through a department-centric, API-first architecture with granular role-based permissions and subscription-based feature gating.

**Core Value Proposition:**
- **Unified Platform:** Single system for all product types (not separate platforms for food/beverage)
- **Department-Centric:** Flexible segmentation with granular permissions
- **2D Inventory Model:** Product + Department tracking (storage as metadata)
- **Hub-and-Spoke Units:** Consistent unit conversion across all domains
- **Subscription-Based:** Tiered plans with feature gating and multi-tenancy

---

## TABLE OF CONTENTS

1. [Complete Feature Inventory](#1-complete-feature-inventory)
2. [Domain Structure](#2-domain-structure)
3. [User Personas and Workflows](#3-user-personas-and-workflows)
4. [Technical Architecture](#4-technical-architecture)
5. [Integration Points](#5-integration-points)
6. [Business Model](#6-business-model)
7. [Current State vs Roadmap](#7-current-state-vs-roadmap)
8. [Key Design Principles](#8-key-design-principles)
9. [Success Metrics](#9-success-metrics)
10. [Risks and Mitigations](#10-risks-and-mitigations)
11. [Appendices](#11-appendices)

---

## 1. COMPLETE FEATURE INVENTORY

### 1.1 Implemented Features (Production Ready)

#### **Departments Domain** ✅ COMPLETE
**DocTypes:**
- Department (Master DocType)
- Department Permission (Child table on User)
- Product Department (Child table on Product)

**Capabilities:**
- Hierarchical department management with circular reference protection
- Department code uniqueness (per company, case-insensitive)
- Active/inactive status management
- JSON-based extensible settings with type validation
- Department-to-department parent relationships
- Default storage area and GL code assignment
- Department statistics and reporting

**API Endpoints (7):**
- `get_accessible_departments` - Get departments user can access
- `get_department_details` - Full department info with products/users
- `get_department_products` - Products assigned to department
- `get_department_users` - Users with access to department
- `get_department_statistics` - Department statistics
- `check_department_access` - Permission verification
- `get_department_hierarchy` - Department tree structure

**Client Enhancements:**
- Auto-uppercase department codes
- Company alignment validation for parent departments
- Self-reference prevention
- Deactivation warnings with confirmation
- Active/inactive status indicators
- Custom buttons (View Products, View Users, View Inventory)

**Documentation:** [docs/02-DEPARTMENTS/](02-DEPARTMENTS/)

---

#### **Permissions Domain** ✅ COMPLETE
**DocTypes:**
- Role Permission (Child table on Role)

**Custom Fields (5):**
- User.department_permissions (Table)
- User.is_team_account (Check)
- Role.custom_permissions (Table)
- Role.is_custom_role (Check)
- Role.role_description (Text)

**Permission Registry (70+ Permissions across 11 Categories):**
1. **Orders** (11): view, create, edit, delete, place, edit_placed, receive, mark_received, cancel, view_costs, export
2. **Invoices** (13): view, create, edit, delete, process, approve, reject, mark_paid, view_costs, ocr_upload, ocr_review, export, accounting_export
3. **Audits** (8): view, open, do, close, delete, view_historic, update_prices, export
4. **Items** (7): view, create, edit, delete, import, export, manage_categories
5. **Vendors** (6): view, create, edit, delete, import, export
6. **Recipes** (4): view, create, edit, delete
7. **Transfers** (4): view, create, approve, cancel
8. **Depletions** (4): view, create, edit, delete
9. **Reports** (4): view, export, create_custom, view_dashboard
10. **System** (5): store_settings, manage_users, manage_roles, team_accounts, manage_integrations
11. **Director** (8): view_all_stores, manage_stores, corporate_vendors, corporate_products, corporate_recipes, store_sync, reports, manage_permissions

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
- `get_available_permissions` - List all permissions
- `get_permissions_by_category` - Filter by category
- `get_user_permissions` - User's effective permissions
- `check_permission` - Verify specific permission
- `get_role_permissions` - Role's permissions
- `create_custom_role` - Create new role
- `update_role_permissions` - Update role permissions
- `revoke_permission` - Revoke permission from role
- `get_role_summary` - Role statistics
- `get_permission_categories` - List categories
- `search_permissions` - Search permissions
- `bulk_assign_permissions` - Bulk operations
- `clone_role` - Duplicate role with permissions

**Client Enhancements:**
- Permission selector dialog with checkboxes
- Auto-populate permission details on selection
- Role Summary button with statistics
- Add Permissions button with category grouping
- Custom role indicator
- View Users button

**Documentation:** [docs/11-PERMISSIONS/](11-PERMISSIONS/)

---

#### **Core Platform (Subscription Management)** ✅ COMPLETE
**DocTypes:**
- Subscription Plan
- Module Activation
- Feature Toggle
- Tenant Branding
- Subscription Access Log

**Capabilities:**
- Subscription plan management with billing metadata
- Module activation with dependency tracking
- Feature toggle registry with dot-notation keys
- Tenant branding (colors, media, custom CSS)
- Automated access logging (90-day retention)

**Default Fixtures:**
- Foundation Plan (FOUNDATION)
- 5 Core Feature Toggles:
  - `core.workspace.access`
  - `products.bulk_operations`
  - `inventory.audit_workflows`
  - `procurement.ottimate_import`
  - `analytics.finance_dashboard`

**API Endpoints (2):**
- `get_feature_matrix` - Complete feature matrix for tenant
- `get_profile` - User profile with permissions & subscription

**Operational Model:**
- BLKSHP Operations manages plans/features (admin-only)
- Tenants consume read-only feature matrix via API
- Per-tenant sites on Frappe Press (isolation model)
- Request-based plan changes (customer → BLKSHP Operations)

---

#### **Products Domain** ✅ PARTIALLY COMPLETE
**DocTypes:**
- Product (Master DocType)
- Product Category
- Product Purchase Unit (Child table)
- Product Tag
- Product Substitute Item (Child table)
- Product Storage Area (Child table)

**Capabilities:**
- Unified product master (all product types in one system)
- Hub-and-spoke unit conversion (all quantities via primary count unit)
- Department allocations (many-to-many via Product Department)
- Purchase units with vendor-specific definitions
- Product categories with hierarchy
- Product properties (generic, non-inventory, prep items)
- Substitute item tracking
- Storage area assignments (metadata only)

**Conversion Methods:**
- `convert_to_primary_unit(from_unit, quantity)` - Convert to primary
- `convert_from_primary_unit(to_unit, quantity)` - Convert from primary
- `convert_between_units(from_unit, to_unit, quantity)` - Direct conversion

**API Endpoints (1+):**
- `convert_quantity` - Centralized conversion service

**Status:** Core functions complete, bulk operations and pricing deferred

**Documentation:** [docs/01-PRODUCTS/](01-PRODUCTS/)

---

#### **Company Domain** ✅ COMPLETE
**DocTypes:**
- Company (Master DocType in director module)

**Capabilities:**
- Multi-tenancy support
- Company-based data isolation
- Company Group support for intercompany accounting
- Company assignments for users and departments

---

### 1.2 Partially Implemented Features (In Development)

#### **Inventory Domain** 🔧 IN PROGRESS
**DocTypes:**
- Inventory Balance
- Inventory Audit
- Inventory Audit Line (Child table)
- Inventory Audit Category (Child table)
- Inventory Audit Department (Child table)
- Inventory Audit Storage Location (Child table)
- Inventory Counting Task
- Storage Area

**Key Concepts:**
- 2D Inventory Model (Product + Department, storage as metadata)
- Theoretical Inventory Calculation
- Task-based audit system (setup by manager, counting by users)
- Variance calculations per department
- Audit lifecycle: Setup → Ready → In Progress → Review → Closed → Locked

**Status:** DocTypes and documentation complete, API and workflows in progress

**Documentation:** [docs/03-INVENTORY/](03-INVENTORY/)

---

#### **Recipes Domain** 🔧 IN PROGRESS
**DocTypes:**
- Recipe
- Recipe Ingredient (Child table)
- Recipe Batch
- Recipe Batch Ingredient (Child table)
- Allergen
- Recipe Allergen (Child table)
- Recipe Inherited Allergen (Child table)

**Key Concepts:**
- Recipe costing with automatic cost calculation
- Subrecipe support (nested recipes)
- Batch management and production tracking
- Allergen tracking with inheritance from ingredients
- Department assignment for recipes

**Status:** Core DocTypes complete, menu lists and repricing deferred

**Documentation:** [docs/05-RECIPES/](05-RECIPES/)

---

#### **Procurement Domain** 🔧 IN PROGRESS
**DocTypes:**
- Vendor

**Key Concepts:**
- Vendor management with contact details
- Ottimate integration for receiving data (flatfile import)
- Invoice structure with department allocation
- Purchase unit handling
- GL code mapping per product-department

**Status:** Vendor master complete, detailed ordering/receiving/invoice workflows deferred to Phase 6

**Documentation:** [docs/04-PROCUREMENT/](04-PROCUREMENT/)

---

#### **Accounting Domain** 🔧 PLANNED
**DocTypes:**
- Account

**Key Concepts:**
- GL code mapping (products/departments → GL codes)
- Bill sync to external accounting systems
- Support for QuickBooks, NetSuite, R365, Sage Intacct
- Payee mapping (vendors → payees)
- Intercompany accounting with Company Group

**Status:** Basic structure defined, integrations planned

**Documentation:** [docs/07-ACCOUNTING/](07-ACCOUNTING/)

---

### 1.3 Planned Features (Documented but Not Implemented)

#### **POS Integration Domain** 📋 PLANNED
**Capabilities:**
- Multiple POS instances per location (Toast, Square, Lightspeed)
- Recipe-to-POS item mapping
- Automatic depletion calculation from sales
- Modifier handling for depletion adjustments
- Sales data polling and import

**Documentation:** [docs/06-POS-INTEGRATION/](06-POS-INTEGRATION/)

---

#### **Transfers & Depletions Domain** 📋 PLANNED
**Capabilities:**
- Inventory transfers between departments/stores
- Manual depletion tracking (waste, spills, comps)
- Depletion types (Sold, Waste, Spill, Comp, Transfer)
- Transfer approval workflows
- Department-to-department transfer tracking

**Documentation:** [docs/08-TRANSFERS-DEPLETIONS/](08-TRANSFERS-DEPLETIONS/)

---

#### **Analytics & Reporting Domain** 📋 PLANNED
**Capabilities:**
- Department-filtered reporting
- Inventory reports (variance, usage, theoretical)
- Financial reports (costs, margins, budgets)
- Custom report builder
- Dashboard with key metrics

**Documentation:** [docs/09-ANALYTICS-REPORTING/](09-ANALYTICS-REPORTING/)

---

#### **Budgets Domain** 📋 PLANNED
**Capabilities:**
- Department-based budget setup
- Budget tracking and alerts
- Budget commitments from purchase orders
- Budget spending from receipts
- Variance analysis

**Documentation:** [docs/12-BUDGETS/](12-BUDGETS/)

---

#### **Director Domain** 📋 PLANNED
**Capabilities:**
- Multi-location management
- Corporate master data (vendors, products, recipes)
- Store synchronization
- Market-based recipe sync
- Consolidated reporting across stores
- Director team accounts

**Documentation:** [docs/10-DIRECTOR/](10-DIRECTOR/)

---

#### **Payments Domain** 📋 PLANNED
**Capabilities:**
- Payment processing integration
- Payment tracking and reconciliation
- Payment workflows

**Documentation:** [docs/13-PAYMENTS/](13-PAYMENTS/)

---

## 2. DOMAIN STRUCTURE

### 2.1 Domain Overview

BLKSHP OS is organized into **14 domains**, each representing a distinct business capability:

| Domain | Priority | Status | Dependencies | Purpose |
|--------|----------|--------|--------------|---------|
| **Core Platform** | CRITICAL | ✅ Complete | None | Subscription plans, feature toggles, module activation, branding |
| **Departments** | CRITICAL | ✅ Complete | None | Department management, hierarchy, segmentation |
| **Permissions** | CRITICAL | ✅ Complete | Departments | Role-based + department-based access control |
| **Products** | HIGH | 🔧 In Progress | Departments | Unified product master, unit conversion, categories |
| **Inventory** | HIGH | 🔧 In Progress | Products, Departments | 2D inventory tracking, audits, theoretical inventory |
| **Procurement** | HIGH | 🔧 In Progress | Products, Departments | Vendors, ordering, receiving, invoicing |
| **Recipes** | MEDIUM | 🔧 In Progress | Products, Departments, Inventory | Recipe management, costing, batch production |
| **POS Integration** | MEDIUM | 📋 Planned | Products, Recipes, Inventory | POS connectivity, automatic depletions |
| **Transfers & Depletions** | MEDIUM | 📋 Planned | Products, Departments, Inventory | Inventory movements, waste tracking |
| **Accounting** | MEDIUM | 📋 Planned | Procurement, Products, Departments | GL code mapping, bill sync to accounting systems |
| **Analytics & Reporting** | MEDIUM | 📋 Planned | All domains | Department-filtered reports, dashboards |
| **Budgets** | LOW | 📋 Planned | Departments, Procurement | Budget setup, tracking, variance analysis |
| **Director** | LOW | 📋 Planned | Products, Procurement, Recipes, Analytics | Multi-location management, corporate masters |
| **Payments** | LOW | 📋 Planned | Procurement, Accounting | Payment processing and tracking |

---

### 2.2 Domain Descriptions

#### **Core Platform**
Central subscription management, feature gating, module activation, and tenant branding. Enforces which features are available to each tenant based on their subscription plan. BLKSHP Operations manages plans; tenants consume read-only feature matrix.

**Key DocTypes:** Subscription Plan, Module Activation, Feature Toggle, Tenant Branding

---

#### **Departments**
Foundation for all other domains. Provides department-based segmentation, user access control, and organizational structure. All data is filtered and organized by departments.

**Key DocTypes:** Department, Department Permission, Product Department

**Integration Points:** Used by ALL domains for filtering, permissions, and organization

---

#### **Permissions**
Two-layer permission system: (1) Role-based permissions (70+ granular permissions), (2) Department-based access. Users must have BOTH role permission AND department access to perform operations.

**Key DocTypes:** Role Permission

**Integration Points:** ALL domains check permissions before operations

---

#### **Products**
Unified product master for ALL product types (food, beverage, supplies, equipment). Hub-and-spoke unit conversion model ensures all quantities stored in primary count unit with on-the-fly conversion.

**Key DocTypes:** Product, Product Category, Product Purchase Unit, Product Tag

**Integration Points:** Used by Inventory, Procurement, Recipes, POS, Transfers, Reporting

---

#### **Inventory**
2D inventory model (Product + Department) with storage as metadata. Theoretical inventory calculation includes all transactions (receipts, transfers, depletions). Task-based audit system for physical counts.

**Key DocTypes:** Inventory Balance, Inventory Audit, Inventory Counting Task, Storage Area

**Integration Points:** Updated by Procurement (receipts), POS (sales), Transfers (movements), Depletions (waste)

---

#### **Procurement**
Vendor management, purchase ordering, receiving, and invoice processing. Ottimate integration for receiving data import. Department allocation of invoice lines with GL code mapping.

**Key DocTypes:** Vendor, Purchase Order (planned), Vendor Invoice (planned)

**Integration Points:** Updates Inventory (receipts), syncs to Accounting (bills), commits Budgets (orders)

---

#### **Recipes**
Recipe management with automatic cost calculation, subrecipe support, and batch production tracking. Recipe-to-POS mapping drives automatic depletion calculations.

**Key DocTypes:** Recipe, Recipe Ingredient, Recipe Batch, Allergen

**Integration Points:** Used by POS (depletions), drives Inventory (batch production), uses Products (ingredients)

---

#### **POS Integration**
Connects to multiple POS systems (Toast, Square, Lightspeed) to import sales data and calculate automatic inventory depletions based on recipe mappings.

**Key Capabilities:** Multiple POS instances, recipe-to-POS mapping, automatic depletions, modifier handling

**Integration Points:** Drives Inventory (depletions), uses Recipes (ingredient calculations)

---

#### **Transfers & Depletions**
Tracks inventory movements between departments/stores and manual depletions (waste, spills, comps). Transfer approval workflows ensure proper authorization.

**Key Capabilities:** Department-to-department transfers, depletion types, approval workflows

**Integration Points:** Updates Inventory (transfers and depletions), uses Products (unit conversions)

---

#### **Accounting**
Integrates with external accounting systems (QuickBooks, NetSuite, R365, Sage Intacct) for bill sync and GL code mapping. Supports intercompany accounting with Company Group.

**Key Capabilities:** GL code mapping, bill sync, payee mapping, multiple accounting systems

**Integration Points:** Receives bills from Procurement, uses Product/Department for GL mapping

---

#### **Analytics & Reporting**
Department-filtered reporting across all domains. Provides variance analysis, usage reports, financial reports, and custom report builder.

**Key Capabilities:** Department filtering, custom reports, dashboards, multi-store consolidation

**Integration Points:** Uses data from ALL domains for reporting

---

#### **Budgets**
Department-based budget setup and tracking. Purchase orders commit budgets, receipts spend budgets. Variance analysis and alerts for budget overruns.

**Key Capabilities:** Budget setup, tracking, commitments, spending, variance analysis

**Integration Points:** Uses Departments (budget setup), Procurement (commitments and spending)

---

#### **Director**
Multi-location management with corporate-level vendor, product, and recipe masters. Store synchronization pushes corporate data to individual locations. Consolidated reporting across all stores.

**Key Capabilities:** Corporate masters, store sync, market-based sync, consolidated reporting

**Integration Points:** Manages Products, Vendors, Recipes at corporate level; syncs to stores

---

#### **Payments**
Payment processing integration and tracking. Payment workflows and reconciliation.

**Key Capabilities:** Payment processing, tracking, reconciliation

**Integration Points:** Uses Procurement and Accounting for payment data

---

## 3. USER PERSONAS AND WORKFLOWS

### 3.1 Primary User Personas

#### **1. System Administrator**
**Role:** System Manager
**Permissions:** Full access to all features
**Department Access:** All departments

**Workflows:**
- Initial system setup and configuration
- User management and role assignment
- Department creation and hierarchy management
- Integration configuration (POS, Accounting)
- System monitoring and troubleshooting

**Tools Used:**
- Frappe Desk UI
- User management forms
- Department management
- System settings
- API configuration

---

#### **2. Inventory Taker**
**Role:** Inventory Taker
**Permissions:** audits.view, audits.do, audits.view_historic (3 permissions)
**Department Access:** Assigned departments only

**Workflows:**
- View assigned counting tasks
- Count products in assigned storage areas
- Enter counts in any available unit
- Mark tasks complete
- View audit history for reference

**Primary Operations:**
- Open Inventory Audit
- Select Counting Task
- Count products by storage area
- Enter quantities (system converts to primary unit)
- Submit counts

**Tools Used:**
- Frappe Desk (counting tasks)
- Mobile-friendly counting interface (planned)

---

#### **3. Inventory Administrator**
**Role:** Inventory Administrator
**Permissions:** Full audit management (8 permissions)
**Department Access:** Assigned departments

**Workflows:**
- Create and configure audits
- Define audit scope (departments, storages, categories)
- Generate counting tasks
- Monitor counting progress
- Review variances and flag high discrepancies
- Approve and close audits
- Update inventory balances
- Generate audit reports

**Primary Operations:**
- Create Inventory Audit
- Set audit parameters (Full/Partial, departments, categories)
- Generate Counting Tasks
- Monitor progress dashboard
- Review variance report
- Flag items for recount
- Close Audit (updates inventory balance)
- Lock Audit after approval period

**Tools Used:**
- Frappe Desk (audit management)
- Audit dashboard
- Variance reports
- Inventory balance views

---

#### **4. Recipe Builder**
**Role:** Recipe Builder
**Permissions:** recipes.view, recipes.create, recipes.edit, recipes.delete, items.view (5 permissions)
**Department Access:** Assigned departments

**Workflows:**
- Create recipes with ingredient lists
- Define serving sizes and yields
- Create subrecipes (prep items)
- Calculate recipe costs
- Manage allergens
- Create batch production records
- Adjust recipes based on actual usage

**Primary Operations:**
- Create Recipe
- Add ingredients (with unit selection)
- Define serving size
- Calculate cost per serving
- Add allergen information
- Create subrecipes for prep items
- Record batch production
- Update recipe costs when ingredient prices change

**Tools Used:**
- Frappe Desk (recipe management)
- Recipe costing calculator
- Batch production forms
- Allergen tracking

---

#### **5. Buyer**
**Role:** Buyer
**Permissions:** orders.view, orders.create, orders.place, vendors.view, items.view (7 permissions)
**Department Access:** Assigned departments

**Workflows:**
- Create purchase orders
- Select vendors and products
- Review par levels and order quantities
- Place orders with vendors
- Track order status
- Communicate with vendors
- Review contract prices

**Primary Operations:**
- View par levels by department
- Create Purchase Order
- Select vendor
- Add products (with purchase units)
- Review contract prices
- Calculate order totals
- Place Order (send to vendor)
- Track order status

**Tools Used:**
- Frappe Desk (order management)
- Par level reports
- Vendor management
- Order history

---

#### **6. Receiver**
**Role:** Receiver
**Permissions:** Full receiving and invoice processing (10 permissions)
**Department Access:** Assigned departments

**Workflows:**
- Receive purchase orders
- Verify quantities and quality
- Allocate invoice lines to departments
- Process invoices
- Import invoices from Ottimate
- Approve invoices
- Update inventory on receipt

**Primary Operations:**
- Receive Purchase Order
- Verify product quantities
- Enter received quantities
- Allocate invoice lines to departments
- Assign GL codes per product-department
- Approve Invoice
- System updates inventory balance
- System syncs bill to accounting

**Tools Used:**
- Frappe Desk (receiving and invoicing)
- Ottimate integration (invoice import)
- Department allocation forms
- GL code mapping

---

#### **7. Bartender**
**Role:** Bartender
**Permissions:** Limited operations (6 permissions)
**Department Access:** Bar department only

**Workflows:**
- View inventory levels
- Record depletions (waste, spills, comps)
- Create transfers between bar areas
- View recipes
- View POS sales

**Primary Operations:**
- View Inventory Balance (Bar)
- Create Manual Depletion (waste/spill)
- Record reason and quantity
- Create Transfer (between bar areas)
- View Recipe (for drink preparation)

**Tools Used:**
- Frappe Desk (simplified views)
- Depletion forms
- Transfer forms
- Recipe views

---

#### **8. Store Manager**
**Role:** Store Manager
**Permissions:** Comprehensive store management (21 permissions)
**Department Access:** All store departments

**Workflows:**
- Oversee all store operations
- Manage users and roles for store
- Review all reports and analytics
- Approve transfers and depletions
- Manage budgets
- Configure store settings
- Monitor POS integration
- Review vendor relationships

**Primary Operations:**
- Dashboard (all store metrics)
- User management (store users)
- Department management
- Budget tracking and variance
- Approve high-value transfers
- Review inventory variances
- Manage vendor relationships
- Configure store settings
- Generate reports

**Tools Used:**
- Frappe Desk (full access)
- Store dashboard
- Analytics reports
- Budget management
- User administration

---

#### **9. Director (Multi-Location)**
**Role:** Director
**Permissions:** Corporate-level management (17 permissions)
**Department Access:** All locations and departments

**Workflows:**
- Manage multiple locations
- Create and maintain corporate masters (vendors, products, recipes)
- Sync corporate data to stores
- Consolidated reporting across locations
- Corporate budgeting
- Performance analysis across locations
- Manage corporate teams

**Primary Operations:**
- Corporate Dashboard (all locations)
- Create/Edit Corporate Vendors
- Create/Edit Corporate Products
- Create/Edit Corporate Recipes
- Sync to Stores (push corporate masters)
- Consolidated Reports (all locations)
- Store Performance Comparison
- Corporate Budget Management
- Manage Director Team Accounts

**Tools Used:**
- Frappe Desk (Director workspace)
- Corporate master management
- Store sync dashboard
- Consolidated reports
- Multi-location analytics

---

#### **10. Accountant**
**Role:** Custom Role (defined per company)
**Permissions:** invoices.view, invoices.process, invoices.approve, invoices.accounting_export, reports.view
**Department Access:** All departments (for visibility)

**Workflows:**
- Review and approve invoices
- Verify GL code mappings
- Export bills to accounting systems
- Reconcile accounting data
- Review financial reports
- Manage payee mappings

**Primary Operations:**
- Review Pending Invoices
- Verify Department Allocations
- Check GL Code Mappings
- Approve Invoices
- Export to Accounting System (QuickBooks/NetSuite/etc.)
- Reconcile Bills
- Generate Financial Reports

**Tools Used:**
- Frappe Desk (invoice review)
- Accounting integration dashboard
- GL code mapping tools
- Export utilities
- Reconciliation reports

---

#### **11. BLKSHP Operations (Internal)**
**Role:** BLKSHP Operations (custom internal role)
**Permissions:** Full administrative access + subscription management
**Department Access:** N/A (operates at platform level)

**Workflows:**
- Provision new tenant sites
- Assign and manage subscription plans
- Enable/disable modules for tenants
- Override feature toggles
- Monitor subscription access logs
- Handle tenant support requests for plan changes
- Configure tenant branding
- Manage platform-level settings

**Primary Operations:**
- Run `scripts/bootstrap_site.py` for new tenants
- Assign Subscription Plan to tenant
- Enable/Disable Modules per tenant
- Override Feature Toggles if needed
- Review Subscription Access Logs
- Apply Tenant Branding
- Monitor platform health
- Respond to tenant upgrade requests

**Tools Used:**
- Frappe Desk (admin interface)
- Provisioning scripts
- Subscription management DocTypes
- Platform monitoring tools
- Support ticket system

**Access:** BLKSHP Operations staff only (not accessible to tenants)

---

### 3.2 Workflow Examples

#### **Workflow 1: Complete Inventory Audit**

**Participants:** Inventory Administrator, Inventory Taker(s)

**Steps:**
1. **Setup (Inventory Administrator)**
   - Create Inventory Audit
   - Set audit date and type (Full/Partial)
   - Define scope (departments: Kitchen, Bar; storage areas: all)
   - Define categories (if partial: Liquor, Wine, Beer)
   - Generate Counting Tasks (system auto-generates based on scope)
   - Assign tasks to departments
   - Status: Setup → Ready

2. **Counting (Inventory Takers)**
   - View assigned Counting Tasks
   - Select first task (e.g., "Kitchen - Walk-in Cooler")
   - Count products in storage area
   - Enter counts in any available unit (system converts to primary)
   - Mark task Complete
   - Repeat for all assigned tasks
   - Status: Ready → In Progress

3. **Review (Inventory Administrator)**
   - View audit progress dashboard
   - All tasks marked Complete
   - Calculate Theoretical Inventory for all products
   - Compare Actual (counted) vs Theoretical
   - Generate Variance Report
   - Flag high variances (>10%)
   - Investigate flagged items
   - Request recount if necessary
   - Status: In Progress → Review

4. **Close (Inventory Administrator)**
   - Approve counts
   - Close Audit
   - System updates Inventory Balance for all products
   - System sets last_audit_date
   - Generate Audit Summary Report
   - Status: Review → Closed

5. **Lock (Automatic after 30 days)**
   - Audit locked after approval period
   - No further changes allowed
   - Historical record preserved
   - Status: Closed → Locked

---

#### **Workflow 2: Purchase Order to Receipt**

**Participants:** Buyer, Receiver, System (automatic)

**Steps:**
1. **Order (Buyer)**
   - Review par levels for Kitchen department
   - Identify items below par
   - Create Purchase Order
   - Select vendor (e.g., Sysco)
   - Add products with purchase units (e.g., 2 cases of chicken breast)
   - Review contract prices
   - Calculate order total
   - Place Order (send to vendor)

2. **Receive (Receiver)**
   - Receive shipment from vendor
   - Locate Purchase Order
   - Verify product quantities
   - Enter received quantities (may differ from ordered)
   - Import invoice from Ottimate (or enter manually)

3. **Allocate (Receiver)**
   - Review invoice lines
   - Allocate each line to department(s)
   - For shared items, split line across departments (Kitchen: 70%, Catering: 30%)
   - Assign GL codes per product-department
   - System converts purchase units to primary units for inventory

4. **Approve (Receiver or Manager)**
   - Review allocations
   - Verify contract prices
   - Approve Invoice
   - System updates Inventory Balance (+quantity received, per department)
   - System creates Bill in accounting system
   - System tracks receipt in Inventory History

---

#### **Workflow 3: POS Sale to Inventory Depletion**

**Participants:** System (automatic), Recipe Builder (setup)

**Setup:**
1. **Recipe Mapping (Recipe Builder)**
   - Create Recipe for menu item (e.g., "Margarita")
   - Add ingredients (Tequila: 1.5 oz, Triple Sec: 0.5 oz, Lime Juice: 1 oz)
   - Assign to Bar department
   - Map to POS item (Toast: "Margarita", Square: "Margarita", etc.)

**Automatic Processing:**
2. **Sales Import (System, every 5 minutes)**
   - Poll Toast API for sales data
   - Identify new sales since last import
   - Create POS Sale records

3. **Depletion Calculation (System)**
   - For each sale, get mapped recipe
   - For each ingredient in recipe:
     - Calculate quantity used (1.5 oz Tequila × 1 sold)
     - Convert to ingredient's primary unit (oz → gallon)
     - Create Depletion Line

4. **Inventory Update (System)**
   - Create Depletion record (type: Sold, department: Bar)
   - Reduce Inventory Balance for each ingredient
   - Update Theoretical Inventory
   - Track in Inventory History

**Result:** Inventory automatically depleted based on POS sales, no manual entry required

---

#### **Workflow 4: Corporate Recipe Sync (Multi-Location)**

**Participants:** Director, System (automatic)

**Steps:**
1. **Create Corporate Recipe (Director)**
   - Access Director workspace
   - Create Recipe at corporate level
   - Add ingredients (from corporate product masters)
   - Define serving size and cost
   - Add allergen information
   - Mark as "Corporate Recipe"
   - Assign to Market (e.g., "West Coast")

2. **Sync to Stores (Director)**
   - Select recipes to sync
   - Select target stores (all stores in "West Coast" market)
   - Initiate Sync
   - System validates: Do target stores have all required ingredients?
   - If missing, offer to sync products first
   - Sync recipes to stores

3. **Store Receipt (Automatic)**
   - Store receives synced recipe
   - Recipe marked as "Corporate Recipe" (cannot be edited locally)
   - Store can view and use recipe
   - Store can adjust portions locally (but not base recipe)
   - Recipe costs automatically calculated using store's product prices

4. **Updates (Director)**
   - Director updates corporate recipe
   - System offers to push update to stores
   - Director confirms
   - All stores receive updated recipe
   - Store-level adjustments preserved

---

## 4. TECHNICAL ARCHITECTURE

### 4.1 Technology Stack

#### **Backend**
- **Framework:** Frappe Framework v15+
- **Platform:** ERPNext v15 (extends core DocTypes)
- **Language:** Python 3.10+
- **Database:** MariaDB 10.6+ / PostgreSQL 13+
- **Cache:** Redis 6.2+
- **Server:** Gunicorn (WSGI)
- **Proxy:** Nginx (TLS termination, static assets)
- **Scheduler:** Frappe Scheduler (cron-based)
- **Job Queue:** RQ (Redis Queue)

#### **Frontend (Current)**
- **UI:** Frappe Desk (built-in)
- **JavaScript:** Vanilla JS + jQuery (Frappe standard)
- **Client Scripts:** Custom form enhancements
- **Assets:** Bundled via Frappe's asset pipeline

#### **Frontend (Planned - Phase 2)**
- **Framework:** Next.js 14+ (TypeScript)
- **State:** React Query (API caching)
- **Styling:** Tailwind CSS
- **UI Components:** shadcn/ui
- **Forms:** React Hook Form + Zod validation
- **Build:** Vite
- **Deployment:** Vercel (recommended) or Frappe Press static hosting

#### **Infrastructure**
- **Hosting:** Frappe Press (managed SaaS)
- **Deployment Model:** One Press site per tenant (isolation)
- **Scaling:** Vertical scaling per site, horizontal scaling across sites
- **Backups:** Automated daily (offsite storage)
- **Monitoring:** Uptime Robot, Sentry, APM (optional)

---

### 4.2 Architectural Patterns

#### **1. Domain-Driven Design**
Code organized by business domain (14 domains). Each domain is self-contained with:
- DocTypes (data models)
- Controllers (business logic)
- Services (domain logic)
- APIs (whitelisted endpoints)
- Tests (unit and integration)
- Documentation (domain README and function docs)

**Example Structure:**
```
blkshp_os/
├── departments/          # Domain module
│   ├── doctype/
│   │   └── department/
│   │       ├── department.json
│   │       ├── department.py (controller)
│   │       ├── department.js (client script)
│   │       └── test_department.py
│   └── service.py       # Domain services
├── api/
│   └── departments.py   # Whitelisted APIs
```

---

#### **2. Department-Centric Architecture**
All data organized by departments. Every domain respects department boundaries:
- **Data Model:** Most DocTypes include `department` field (Link: Department)
- **Filtering:** All queries filtered by user's accessible departments
- **Permissions:** Two-layer: (1) Role permissions, (2) Department access
- **Reporting:** All reports support department filtering
- **Inventory:** Tracked per Product + Department (2D model)

**Pattern:**
```python
# Always filter by accessible departments
departments = get_user_accessible_departments(user)
filters['department'] = ['in', departments]

# Always check department permissions
if not has_department_permission(user, department, 'read'):
    frappe.throw(_("No access to department"))
```

---

#### **3. 2D Inventory Model**
Inventory uniquely identified by **Product + Department** (not by storage location).
- **Key:** `(product_id, department_id, company_id)`
- **Storage:** Metadata only (helps with counting, not in calculations)
- **Benefits:** Simplifies math, maintains visibility, aligns with operations

**Example:**
```
Product: Coca Cola Cans
├── Bar Department: 240 cans (inventory balance)
│   ├── Storage: Walk-in Cooler (metadata)
│   └── Storage: Back Bar (metadata)
└── Catering Department: 120 cans (inventory balance)
    └── Storage: Catering Storage (metadata)

TOTAL: 360 cans (sum across departments)
```

---

#### **4. Hub-and-Spoke Unit Conversion**
All conversions flow through product's primary count unit (hub).
- **Storage:** All quantities stored in primary count unit
- **Display:** Convert on-the-fly for display/entry
- **Conversions:** Always use Product's conversion methods (never create custom methods)

**Example:**
```
Product: Beer (Draft)
Primary Unit: gallon

keg (15.5 gallons) → gallon → pint (0.125 gallons)
pint → gallon → keg

Stored: 31.0 gallons
Display: 2 kegs OR 248 pints
```

**Conversion Methods (on Product):**
- `convert_to_primary_unit(from_unit, quantity)` - Converts any unit to primary
- `convert_from_primary_unit(to_unit, quantity)` - Converts primary to any unit
- `convert_between_units(from_unit, to_unit, quantity)` - Direct conversion (via primary)

---

#### **5. API-First Design**
All functionality exposed via REST APIs for frontend consumption.
- **Format:** `/api/method/blkshp_os.api.<module>.<function>`
- **Authentication:** Frappe session (cookies) or API key/secret (tokens)
- **Authorization:** Permission checks on every endpoint
- **Response:** Standard Frappe JSON format

**Example:**
```python
# blkshp_os/api/departments.py

@frappe.whitelist()
def get_accessible_departments(permission_flag='read'):
    """Get departments user can access"""
    user = frappe.session.user
    departments = get_user_accessible_departments(user, permission_flag)
    return [dept.as_dict() for dept in departments]
```

---

#### **6. Feature Gating via Subscription Plans**
Features controlled by subscription plan + module activation + feature toggles.
- **Subscription Plan:** Defines modules available to tenant (e.g., FOUNDATION)
- **Module Activation:** Links modules to plan with dependencies and feature overrides
- **Feature Toggle:** Granular feature flags (e.g., `products.bulk_operations`)
- **Enforcement:** Checked server-side (even if hidden in UI)

---

#### **7. Two-Layer Permission System**
Users must have BOTH role permission AND department access.

**Layer 1: Role-Based Permissions (70+ granular permissions)**
- Atomic permissions like `orders.create`, `audits.close`, `recipes.view`
- Assigned to roles (e.g., Buyer role has `orders.create`)
- Users inherit permissions from assigned roles
- System Manager bypasses all permission checks

**Layer 2: Department-Based Access**
- Users assigned to departments via Department Permission (child table on User)
- Granular flags: read, write, create, delete, submit, cancel, approve
- Effective date range support (valid_from, valid_upto)
- Prevents cross-department data access

---

#### **8. Theoretical Inventory Calculation**
On-demand calculation (not stored) of expected inventory based on transactions.

**Formula:**
```
Theoretical Inventory =
    Starting Inventory (from last audit)
    + Received (from invoices)
    + Transferred In (from other departments)
    - Transferred Out (to other departments)
    - Depleted (sold, spilled, wasted, etc.)
```

**Key Points:**
- Calculated per **Product + Department** (storage NOT included)
- All quantities in **primary count unit**
- Recalculated on demand (not stored)
- Used for variance analysis during audits
- Caching strategy TBD (open question in Decision Log)

---

## 5. INTEGRATION POINTS

### 5.1 External System Integrations

#### **POS Systems**
**Supported:** Toast, Square, Lightspeed
**Purpose:** Import sales data for automatic inventory depletions
**Integration Method:** REST APIs (polling or webhooks)
**Configuration:** POS Configuration DocType per system

**Data Flow:**
1. System polls POS API (e.g., every 5 minutes)
2. Import new sales since last poll
3. Map POS items to recipes
4. Calculate ingredient depletions
5. Update inventory balances
6. Log depletion history

**Mapping Required:**
- POS Item → Recipe (one-to-one or one-to-many)
- POS Modifier → Recipe Adjustment (optional)
- POS Department → BLKSHP Department

---

#### **Accounting Systems**
**Supported:** QuickBooks Online/Desktop, NetSuite, R365, Sage Intacct
**Purpose:** Sync vendor bills, map GL codes
**Integration Method:** REST APIs or file export
**Configuration:** Accounting Configuration DocType

**Data Flow:**
1. Invoice approved in BLKSHP OS
2. System maps GL codes per product-department
3. System maps vendor to payee
4. Create Bill in accounting system via API
5. Track sync status
6. Handle errors with retry logic

**Mapping Required:**
- Product + Department → GL Code
- Vendor → Payee Name
- Invoice → Bill (line-by-line sync)

---

#### **Ottimate (Procurement)**
**Purpose:** Import receiving data and invoices
**Integration Method:** Flatfile import (CSV)
**Configuration:** Ottimate import settings

**Data Flow:**
1. Export invoice data from Ottimate (CSV)
2. Import CSV via BLKSHP OS
3. Map Ottimate SKUs to BLKSHP Products
4. Create Vendor Invoices
5. Allocate to departments
6. Process as normal invoices

**Mapping Required:**
- Ottimate SKU → BLKSHP Product
- Ottimate Vendor → BLKSHP Vendor

**Status:** Current implementation (Phase 1-4). Detailed ordering/receiving workflows deferred to Phase 6 (12+ months).

---

#### **Frappe Press (Hosting)**
**Purpose:** Managed hosting and deployment
**Integration Method:** Press CLI and API
**Configuration:** Press credentials (FC_API_KEY, FC_API_SECRET)

**Features:**
- One Press site per tenant (isolation)
- Automated site provisioning via `scripts/bootstrap_site.py`
- Subscription plan assignment during provisioning
- Automated backups (daily, offsite)
- SSL certificates (automatic renewal)
- Uptime monitoring
- Log aggregation

---

## 6. BUSINESS MODEL

### 6.1 Subscription-Based SaaS Model

BLKSHP OS operates on a **subscription-based SaaS model** with tiered plans, feature gating, and per-tenant isolation.

**Key Principles:**
- One subscription plan per tenant site
- Module-based feature packaging
- Granular feature toggles for add-ons
- BLKSHP Operations controls plan assignments (not self-service)
- Request-based upgrades (customer → BLKSHP Operations)

---

### 6.2 Subscription Plans

#### **Foundation Plan** (DEFAULT)
**Plan Code:** `FOUNDATION`
**Target:** Small single-location restaurants/bars
**Billing:** TBD (likely monthly)

**Included Modules:**
- Core Platform (required)
- Products
- Inventory
- Procurement
- Analytics

**Included Features:**
- Department management (unlimited departments)
- User management with role-based permissions
- Product catalog (unlimited products)
- Inventory tracking and audits
- Vendor management
- Basic procurement (Ottimate integration)
- Basic reporting and analytics

---

#### **Professional Plan** (PLANNED)
**Plan Code:** `PROFESSIONAL`
**Target:** Medium-sized operations, multiple locations

**Included Modules:**
- All Foundation modules
- Recipes
- POS Integration
- Transfers & Depletions
- Advanced Analytics

**Included Features:**
- All Foundation features
- Recipe management with costing
- Batch production tracking
- POS integration (Toast, Square, Lightspeed)
- Automatic inventory depletions
- Inter-department transfers
- Waste/spill tracking
- Advanced reporting
- Finance dashboard

---

#### **Enterprise Plan** (PLANNED)
**Plan Code:** `ENTERPRISE`
**Target:** Multi-location hospitality groups

**Included Modules:**
- All Professional modules
- Director (multi-location management)
- Budgets
- Payments
- Custom integrations

**Included Features:**
- All Professional features
- Multi-location management
- Corporate-level masters (vendors, products, recipes)
- Store synchronization
- Consolidated reporting across locations
- Budget management and tracking
- Payment processing integration
- Custom integration support
- Dedicated account manager
- Priority support

---

### 6.3 Module Dependencies

Modules have dependencies that must be satisfied before activation.

**Dependency Matrix:**
```
core (required, no dependencies)
├── products (depends on: core)
│   ├── inventory (depends on: core, products)
│   ├── procurement (depends on: core, products)
│   └── recipes (depends on: core, products)
│       └── pos_integration (depends on: core, products, recipes, inventory)
├── analytics (depends on: core)
├── budgets (depends on: core, procurement)
└── director (depends on: core, products, inventory, procurement, recipes, analytics)
```

---

### 6.4 Monetization Strategy

#### **Pricing Tiers (Estimated)**
- **Foundation:** $200-$300/month per location
- **Professional:** $500-$700/month per location
- **Enterprise:** $1,500-$2,500/month + per-location fee

**Revenue Streams:**
1. **Subscription Fees:** Primary revenue (monthly recurring)
2. **Implementation Services:** One-time setup and training fees
3. **Custom Integrations:** Custom development for unique requirements
4. **Premium Support:** Enhanced support SLA for Enterprise customers
5. **Training Services:** On-site or virtual training sessions

---

## 7. CURRENT STATE VS ROADMAP

### 7.1 Current State (Phase 1 Complete)

#### **✅ COMPLETE - Production Ready**

**Domains:**
- Core Platform (subscription management)
- Departments (foundation)
- Permissions (role-based + department-based)

**Capabilities:**
- Subscription plan management with feature gating
- Module activation with dependencies
- Feature toggle registry
- Tenant branding support
- Department management with hierarchy
- 70+ granular permissions across 11 categories
- 8 standard role templates
- Two-layer permission system (role + department)
- User management with department access
- API endpoints for departments and permissions (20 total)
- Custom fields on User and Role
- Client scripts for enhanced forms
- Provisioning automation via `scripts/bootstrap_site.py`

---

### 7.2 Planned Roadmap

#### **Phase 0 - Foundations** ✅ COMPLETE
- Align bench environment on ERPNext v15 ✅
- Capture existing code quality status ✅
- Provision automation scripts ✅

---

#### **Phase 1 - Core Consolidation** ✅ COMPLETE
- Core Platform with subscription management ✅
- Departments domain complete ✅
- Permissions domain complete ✅
- API authentication (session-based) ✅
- Fixtures (Custom Fields, Feature Toggles, Subscription Plans) ✅

---

#### **Phase 2 - MVP Readiness** 🔧 IN PROGRESS
- Products & Inventory alignment
- Recipes domain (core features)
- Procurement domain (vendor master, Ottimate integration)
- Feature gating + subscription enforcement
- Multi-tenancy scripts (site provisioning)
- Frontend integration contracts (REST response schemas)
- Testing & QA baseline (unit/integration tests, GitHub Actions)

**Timeline:** Week 1-2 (current)

---

#### **Phase 3 - Demo & Feedback Loop** 📋 PLANNED
- Deploy MVP bench to staging Press site
- Connect SPA MVP to staging APIs
- Conduct demo walkthrough scenarios
- Gather feedback, capture change requests
- Update backlog

**Timeline:** Week 3 (planned)

---

#### **Phase 4 - Production Hardening** 📋 PLANNED
- Security enhancements (HTTPS, rate limiting, audit logging)
- Observability (Sentry, uptime monitors, log aggregation)
- Documentation and training materials
- Plan next release wave

**Timeline:** Weeks 4+ (planned)

---

#### **Phase 5 - POS Integration & Transfers** 📋 PLANNED
- POS Integration domain (Toast, Square, Lightspeed)
- Automatic depletion calculations
- Transfers & Depletions domain
- Manual depletion tracking

**Timeline:** TBD (post-MVP)

---

#### **Phase 6 - Procurement Deep Dive** 📋 PLANNED (12+ months)
- Detailed ordering workflows (quick orders, recurring orders)
- Approval workflows for purchase orders
- Detailed receiving (partial receiving, inspection, quality control)
- Invoice processing (OCR, AI processing, matching, reconciliation)
- Vendor performance tracking

**Rationale:** Deferred until after Ottimate contract ends. Current Ottimate integration handles basic needs.

**Timeline:** 12+ months (post-Ottimate contract)

---

#### **Phase 7 - Analytics & Director** 📋 PLANNED
- Analytics & Reporting domain
- Director domain (multi-location management)
- Consolidated reporting
- Budget management

**Timeline:** TBD (post-POS integration)

---

## 8. KEY DESIGN PRINCIPLES

### 8.1 Architectural Principles

1. **Unified Platform, Not Separate Platforms**
   - Single Product Master for all product types (food, beverage, supplies)
   - Department-based segmentation instead of separate applications
   - One inventory tracking system for everything
   - Unified reporting across all domains

2. **Department-Centric Architecture**
   - All data filtered by departments
   - Users assigned to specific departments
   - Permissions respect department boundaries
   - Inventory tracked per Product + Department

3. **2D Inventory Model**
   - Inventory = Product + Department (not storage location)
   - Storage locations are metadata for organization
   - Simplifies calculations, maintains visibility
   - All quantities in primary count unit

4. **Hub-and-Spoke Unit Conversion**
   - All conversions flow through product's primary count unit
   - Conversions calculated on-the-fly (not stored)
   - Consistent unit handling across all domains
   - Use Product's conversion methods (never create custom)

5. **API-First Design**
   - All functionality exposed via REST APIs
   - Frontend (SPA) consumes APIs only
   - Frappe Desk uses same APIs
   - API contracts documented and versioned

6. **Subscription-Based Feature Gating**
   - Features controlled by subscription plan + module activation + feature toggles
   - BLKSHP Operations manages plans (not self-service)
   - Enforcement server-side (even if hidden in UI)
   - Tenants consume read-only feature matrix

7. **Two-Layer Permission System**
   - Layer 1: Role-based permissions (70+ granular)
   - Layer 2: Department-based access
   - Must have BOTH to perform operations
   - More restrictive permission applies

8. **Domain-Driven Design**
   - Code organized by business domain
   - Each domain self-contained
   - Clear integration points
   - Cross-domain reference documented

---

### 8.2 Data Principles

1. **Single Source of Truth**
   - One Product Master (not duplicated across domains)
   - One Department Master
   - One Inventory Balance (per Product + Department)
   - No data duplication

2. **Quantities Always in Primary Count Unit**
   - Storage rule: All quantities stored in product's primary unit
   - Display rule: Convert on-the-fly for display/entry
   - Calculation rule: All math in primary units
   - Consistency: Prevents conversion drift

3. **Storage as Metadata Only**
   - Storage locations tracked but not in calculations
   - Helps with counting tasks
   - Simplifies inventory math
   - Aligns with 2D model

4. **Theoretical Inventory Calculated, Not Stored**
   - On-demand calculation from transactions
   - Formula: Starting + Received + Transferred In - Transferred Out - Depleted
   - Used for variance analysis
   - Caching strategy TBD

5. **Audit Trail for All Transactions**
   - Inventory History records all changes
   - Version control on DocTypes (Frappe built-in)
   - Subscription Access Logs (90-day retention)
   - Immutable records (intercompany JEs, closed audits)

---

## 9. SUCCESS METRICS

### 9.1 Adoption Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Active Tenants | 50 by Q2 2026 | Count of paying tenants with active usage |
| Departments Per Tenant | Avg 5-10 | Number of departments created per tenant |
| Users Per Tenant | Avg 10-20 | Active users (logged in within 30 days) |
| Daily Active Users | 70% of users | Users who log in daily |
| Feature Adoption (Recipes) | 60% of Professional+ | % of eligible tenants using Recipes module |
| Feature Adoption (POS) | 70% of Professional+ | % of eligible tenants using POS Integration |

---

### 9.2 Operational Efficiency Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Inventory Audit Time | <4 hours | Average time to complete full audit |
| Invoice Processing Time | <10 minutes | Average time from receipt to approval |
| Purchase Order Cycle Time | <2 days | Average time from creation to receipt |
| Recipe Costing Accuracy | <3% variance | Variance between recipe cost and actual cost |

---

### 9.3 Integration Health Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| API Latency (p95) | <200ms | 95th percentile API response time |
| API Error Rate | <0.1% | % of API calls resulting in errors |
| POS Integration Uptime | 99.5% | % of time POS data successfully imported |
| Accounting Sync Success Rate | 99% | % of bills successfully synced to accounting |
| Ottimate Import Success Rate | 95% | % of Ottimate imports completed without errors |

---

## 10. RISKS AND MITIGATIONS

### 10.1 Technical Risks

#### **Risk: Performance Degradation with Multi-Location Scale**
**Impact:** High
**Likelihood:** Medium

**Mitigation:**
- Design caching strategy for theoretical inventory
- Add composite DB indexes
- Cache company group lookups
- Monitor performance metrics
- Plan horizontal scaling

---

#### **Risk: Unit Conversion Drift**
**Impact:** Critical
**Likelihood:** Low

**Mitigation:**
- Enforce hub-and-spoke conversion
- Store all quantities in primary unit only
- Use Product's conversion methods exclusively
- Comprehensive unit tests
- Validate conversions during data entry

---

### 10.2 Business Risks

#### **Risk: Change Management Resistance**
**Impact:** High
**Likelihood:** High

**Mitigation:**
- Comprehensive training materials
- On-site or virtual training sessions
- Quick-start guides
- Dedicated customer success manager
- Gather feedback during demos
- Iterate on UX based on feedback

---

#### **Risk: Customer Acquisition Challenges**
**Impact:** High
**Likelihood:** Medium

**Mitigation:**
- Offer free trials with sample data
- Provide ROI calculators
- Showcase customer success stories
- Attend industry events
- Partner with hospitality consultants
- Offer implementation services
- Competitive pricing

---

## 11. APPENDICES

### 11.1 Glossary

| Term | Definition |
|------|------------|
| **2D Inventory Model** | Inventory uniquely identified by Product + Department (not storage location) |
| **Department** | Organizational unit within a company (Kitchen, Bar, Catering, etc.) |
| **Hub-and-Spoke Unit Conversion** | All unit conversions flow through product's primary count unit |
| **Primary Count Unit** | The base unit of measure for a product (gallon, pound, each) |
| **Theoretical Inventory** | Calculated expected inventory based on transactions |
| **Variance** | Difference between actual (counted) and theoretical inventory |
| **Department Permission** | Granular access control per department |
| **Role Permission** | Granular functional permission (70+ defined) |
| **Subscription Plan** | Commercially packaged plan (FOUNDATION, PROFESSIONAL, ENTERPRISE) |
| **Feature Toggle** | Granular feature flag (e.g., products.bulk_operations) |
| **Frappe Desk** | Built-in admin interface for Frappe Framework |
| **Next.js SPA** | Planned external frontend for tenant-facing workflows |

---

### 11.2 References

**Internal Documentation:**
- [Main Documentation](README.md)
- [Consolidated Decision Log](CONSOLIDATED_DECISION_LOG.md)
- [Project Timeline](PROJECT-TIMELINE.md)
- [Development Guide](DEVELOPMENT-GUIDE.md)
- [Testing Guide](TESTING-GUIDE.md)
- [API Reference](API-REFERENCE.md)
- [Cross-Domain Reference](CROSS-DOMAIN-REFERENCE.md)

**Domain Documentation:**
- [Products Domain](01-PRODUCTS/)
- [Departments Domain](02-DEPARTMENTS/)
- [Inventory Domain](03-INVENTORY/)
- [Procurement Domain](04-PROCUREMENT/)
- [Recipes Domain](05-RECIPES/)
- [Permissions Domain](11-PERMISSIONS/)

**External References:**
- [Frappe Framework Documentation](https://frappeframework.com/docs)
- [ERPNext Documentation](https://docs.erpnext.com/)
- [Frappe Press Documentation](https://frappecloud.com/docs)

---

### 11.3 Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-13 | AI Analysis | Initial comprehensive PRD based on codebase exploration |

---

**END OF PRD**
