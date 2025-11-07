# BLKSHP Product Platform - Development Guide

**Master Navigation Guide for Domain-Specific Implementation Documentation**

---

## Quick Navigation

- [Architecture & Foundation](#architecture--foundation)
- [Core Domains](#core-domains)
- [Supporting Domains](#supporting-domains)
- [Integration Domains](#integration-domains)
- [Development Roadmap](#development-roadmap)

---

## Architecture & Foundation

Start here for foundational understanding:

- **[00-ARCHITECTURE/](00-ARCHITECTURE/)** - Architecture, framework overview, deployment
  - Executive summary and project overview
  - Frappe Framework guide
  - Core architecture design
  - Application structure
  - Deployment and scaling

---

## Core Domains

High-priority domains required for core functionality:

### 1. Products Domain ⭐ HIGH PRIORITY
**[01-PRODUCTS/](01-PRODUCTS/)** - Unified product/item management
- **Status**: ⏳ To be extracted
- **Dependencies**: Departments
- **Functions**: 11 functions (Product Master, Categories, Purchase Units, Unit Conversion, etc.)
- **Priority**: Foundation - required by most other domains

### 2. Departments Domain ⭐ HIGH PRIORITY
**[02-DEPARTMENTS/](02-DEPARTMENTS/)** - Department segmentation and permissions
- **Status**: ⏳ To be extracted
- **Dependencies**: None (foundation)
- **Functions**: 4 functions (Department Master, Permissions, Settings, Allocations)
- **Priority**: Foundation - required by Products, Inventory, Permissions

### 3. Inventory Domain ⭐ HIGH PRIORITY
**[03-INVENTORY/](03-INVENTORY/)** - Inventory tracking, audits, theoretical inventory
- **Status**: ⏳ To be extracted
- **Dependencies**: Products, Departments, Procurement, POS, Transfers
- **Functions**: 10 functions (Balance, Theoretical, Audits, Tasks, Workflows, etc.)
- **Priority**: Core functionality - central to the platform

### 4. Permissions Domain ⭐ HIGH PRIORITY
**[11-PERMISSIONS/](11-PERMISSIONS/)** - User management, roles, permissions
- **Status**: ⏳ To be extracted
- **Dependencies**: Departments
- **Functions**: 6 functions (User Management, Roles, Permissions Matrix, etc.)
- **Priority**: Required for user access and security

---

## Supporting Domains

Medium-priority domains that enhance functionality:

### 5. Procurement Domain
**[04-PROCUREMENT/](04-PROCUREMENT/)** - Vendors, orders, invoices, Ottimate integration
- **Status**: ⏳ To be extracted
- **Dependencies**: Products, Departments
- **Functions**: 13 functions (10 current, 3 Phase 6 deferred)
- **Priority**: Medium - core functionality, but detailed workflows deferred

### 6. Recipes Domain
**[05-RECIPES/](05-RECIPES/)** - Recipe management, costing, batch production
- **Status**: ⏳ To be extracted
- **Dependencies**: Products, Departments, Inventory
- **Functions**: 12 functions (Recipe Master, Costing, Batches, Allergens, etc.)
- **Priority**: Medium - required for POS depletion calculations

### 7. POS Integration Domain
**[06-POS-INTEGRATION/](06-POS-INTEGRATION/)** - POS connectivity and depletions
- **Status**: ⏳ To be extracted
- **Dependencies**: Products, Departments, Recipes, Inventory
- **Functions**: 7 functions (Configuration, Mapping, Sales Import, Depletion Calculation)
- **Priority**: Medium - required for automatic inventory tracking

### 8. Transfers & Depletions Domain
**[08-TRANSFERS-DEPLETIONS/](08-TRANSFERS-DEPLETIONS/)** - Inventory movements and manual depletions
- **Status**: ⏳ To be extracted
- **Dependencies**: Products, Departments, Inventory
- **Functions**: 6 functions (Transfers, Workflow, Pricing, Depletions)
- **Priority**: Medium - required for inventory movement tracking

### 9. Analytics & Reporting Domain
**[09-ANALYTICS-REPORTING/](09-ANALYTICS-REPORTING/)** - Reporting, analytics, dashboards
- **Status**: ⏳ To be extracted
- **Dependencies**: All domains (consumes data from all)
- **Functions**: 9 functions (Report Framework, 8 report types)
- **Priority**: Medium - important but can be built incrementally

### 10. Accounting Domain
**[07-ACCOUNTING/](07-ACCOUNTING/)** - Accounting system integration
- **Status**: ⏳ To be extracted
- **Dependencies**: Procurement, Products, Departments
- **Functions**: 8 functions (Configuration, QuickBooks, NetSuite, GL Mapping, etc.)
- **Priority**: Medium - required for financial reporting integration

### 11. Director Domain
**[10-DIRECTOR/](10-DIRECTOR/)** - Multi-location management
- **Status**: ⏳ To be extracted
- **Dependencies**: Products, Departments, Procurement, Recipes, Analytics
- **Functions**: 8 functions (Configuration, Sync, Corporate Management, Reporting)
- **Priority**: Medium - required for multi-location operations

### 12. Budgets Domain
**[12-BUDGETS/](12-BUDGETS/)** - Budget management and tracking
- **Status**: ⏳ To be extracted
- **Dependencies**: Departments, Procurement, Director
- **Functions**: 4 functions (Setup, Tracking, Reporting, Director Budgets)
- **Priority**: Medium - important for financial control, not critical path

---

## Integration Domains

### 13. Payments Domain ⏸️ DEFERRED
**[13-PAYMENTS/](13-PAYMENTS/)** - Payment processing
- **Status**: ⏳ Deferred to Phase 6 (12+ months)
- **Dependencies**: Procurement, Accounting
- **Functions**: 5 functions (all Phase 6)
- **Priority**: Deferred - payments currently in Ottimate

### 14. External Integrations
**[99-INTEGRATIONS/](99-INTEGRATIONS/)** - FOSS tools and external APIs
- **Status**: ⏳ To be extracted
- **Dependencies**: Used by multiple domains
- **Functions**: 6 functions (OCR, Fuzzy Matching, EDI, Email, PDF, Excel)
- **Priority**: Varies by domain requirements

---

## Development Roadmap

### Phase 1: Foundation (Weeks 1-4)
1. ✅ Architecture & Framework Setup
2. ✅ Departments Domain
3. ✅ Permissions Domain (basic)
4. ✅ Products Domain (basic)

### Phase 2: Core Inventory (Weeks 5-8)
1. ✅ Products Domain (complete)
2. ✅ Inventory Domain (basic)
3. ✅ Inventory Audits (basic)

### Phase 3: Procurement & Recipes (Weeks 9-18)
1. ✅ Procurement Domain (basic - Ottimate integration)
2. ✅ Recipes Domain
3. ✅ POS Integration

### Phase 4: Transfers & Enhancements (Weeks 19-26)
1. ✅ Transfers & Depletions
2. ✅ Inventory Enhancements
3. ✅ Product Enhancements
4. ✅ Recipe Enhancements

### Phase 5: Reporting & Analytics (Weeks 27-30)
1. ✅ Analytics & Reporting
2. ✅ Accounting Integration
3. ✅ Director Module

### Phase 6: Advanced Features (Weeks 31-38)
1. ⏳ Budget Management
2. ⏳ Advanced Reporting
3. ⏳ Mobile Enhancements

### Phase 7: Deferred Features (12+ months)
1. ⏳ Payment Processing
2. ⏳ Detailed Ordering Workflows
3. ⏳ Detailed Receiving
4. ⏳ Invoice Processing (OCR, AI)

---

## Status Legend

- ✅ **Complete** - Implementation documented and ready
- 🚧 **In Progress** - Currently being developed
- ⏳ **Pending** - To be extracted/implemented
- ⏸️ **Deferred** - Deferred to later phase

---

## Dependency Graph

```
Departments (Foundation)
    ├── Products
    │   ├── Inventory
    │   ├── Procurement
    │   ├── Recipes
    │   └── POS Integration
    ├── Permissions
    └── Budgets

Inventory
    ├── Transfers & Depletions
    └── Analytics & Reporting

Procurement
    ├── Accounting
    └── Analytics & Reporting

Recipes
    └── POS Integration

Director
    └── Analytics & Reporting (Consolidated)
```

---

## Next Steps

### ✅ Extraction Complete
All major domains have been extracted. See [START-HERE.md](START-HERE.md) for fine-tuning and development priorities.

### 🎯 Fine-Tuning & Development
1. **Start Fine-Tuning**: Departments Domain (Week 1)
2. **Then**: Permissions Domain (Week 2)
3. **Then**: Products Domain (Week 3-4)
4. **Then**: Inventory Domain (Week 5-8)

See [DEVELOPMENT-PRIORITY.md](DEVELOPMENT-PRIORITY.md) for detailed roadmap.

---

## Master Documents

- **[FRAPPE_IMPLEMENTATION_PLAN.md](FRAPPE_IMPLEMENTATION_PLAN.md)** - Original comprehensive plan (to be broken down)
- **[FUNCTIONALITY_AUDIT_CHECKLIST.md](FUNCTIONALITY_AUDIT_CHECKLIST.md)** - Feature audit and coverage tracking
- **[DOMAIN_DOCUMENTATION_STRUCTURE.md](DOMAIN_DOCUMENTATION_STRUCTURE.md)** - Structure proposal
- **[START-HERE.md](START-HERE.md)** - Getting started guide
- **[DEVELOPMENT-PRIORITY.md](DEVELOPMENT-PRIORITY.md)** - Development priorities and roadmap

## Agent Context Documents

**Essential reading for all agents:**
- **[PROJECT-CONTEXT.md](PROJECT-CONTEXT.md)** ⭐ - Project-wide architecture and principles
- **[AGENT-INSTRUCTIONS.md](AGENT-INSTRUCTIONS.md)** ⭐ - How to work on the project
- **[CROSS-DOMAIN-REFERENCE.md](CROSS-DOMAIN-REFERENCE.md)** ⭐ - Domain interactions and patterns
- **[AGENT-CONTEXT-PACKAGE.md](AGENT-CONTEXT-PACKAGE.md)** - Context loading guide

---

**Last Updated**: 2025  
**Version**: 1.0

