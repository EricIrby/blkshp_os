# BLKSHP Product Platform - Development Guide

**Master Navigation Guide for Domain-Specific Implementation Documentation**

---

## Quick Navigation

- [Architecture & Foundation](#architecture--foundation)
- [Core Domains](#core-domains)
- [Supporting Domains](#supporting-domains)
- [Integration Domains](#integration-domains)
- [Development Roadmap](#development-roadmap)
- [Local Bench Commands](#local-bench-commands)

---

## Architecture & Foundation
-### Local Bench Commands

When running Frappe CLI operations (migrate, tests, exports, etc.), change into the bench directory and invoke the virtualenv-managed binary:

```bash
cd /Users/Eric/Development/BLKSHP/BLKSHP-DEV
../venv/bin/bench --site blkshp.local migrate
```

Using the global `bench` executable outside this directory will not detect the BLKSHP bench or its sites.

---


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

**Last Updated**: November 8, 2025  
**Version**: 1.1

---

## Development Priorities & Fine-Tuning

### Recommended Starting Point

Based on dependencies and development phases, here's the recommended order for development and fine-tuning:

### Phase 1: Foundation (Start Here) ⭐

#### 1. Departments Domain (WEEK 1) ✅ COMPLETE

**Why Start Here:**
- Zero dependencies (foundation domain)
- Required by all other domains
- Simple, well-defined scope
- Enables product allocations and permissions

**Status:** ✅ Complete - Implementation documented in `02-DEPARTMENTS/IMPLEMENTATION-SUMMARY.md`

#### 2. Permissions Domain (WEEK 1-2) ✅ COMPLETE

**Why Second:**
- Depends on Departments (built)
- Required for user access control
- Needed before any real development work
- Enables secure development

**Status:** ✅ Complete - Implementation documented in `11-PERMISSIONS/IMPLEMENTATION-SUMMARY.md`

#### 3. Products Domain (WEEK 2-4) ⏳ NEXT PRIORITY

**Why Third:**
- Depends on Departments (built)
- Foundation for Inventory, Procurement, Recipes
- Most complex foundation domain
- Needs thorough fine-tuning before use

**Fine-Tuning Tasks:**

1. **Review `01-Product-Master.md`** - Enhance with:
   - Complete field validation rules
   - Complete method implementations
   - Error handling scenarios
   - Data migration considerations
   - Index optimization strategies

2. **Review `04-Unit-Conversion-System.md`** - Enhance with:
   - Complete conversion algorithm implementation
   - Edge case handling
   - Performance optimization
   - Conversion accuracy testing

3. **Review `08-Bulk-Operations.md`** - Enhance with:
   - Complete import/export implementation
   - Error handling and recovery
   - Validation rules
   - Progress tracking UI

4. **Create missing function documents:**
   - `05-Product-Departments.md` - Reference Departments domain
   - `06-Product-Storage.md` - Storage assignments

5. **Add implementation details:**
   - Database indexes
   - API endpoints
   - Client-side scripts
   - Server-side scripts
   - Print formats
   - Workflows (if needed)

**Development Tasks:**
1. Create Product DocType
2. Implement unit conversion system
3. Create Purchase Unit DocType
4. Implement bulk import/export
5. Test product creation and unit conversions

### Phase 2: Core Functionality (WEEK 5-8)

#### 4. Inventory Domain (WEEK 5-8)

**Why Fourth:**
- Depends on Products and Departments (both built)
- Core functionality of the platform
- Most complex domain
- Needs Products working correctly first

**Fine-Tuning Tasks:**

1. **Review `02-Theoretical-Inventory.md`** - Enhance with:
   - Complete SQL query optimizations
   - Caching strategies
   - Performance benchmarks
   - Edge case handling

2. **Review `03-Inventory-Audits.md`** - Enhance with:
   - Complete workflow state machine
   - Complete task generation algorithm
   - Mobile UI specifications
   - Offline counting support

3. **Review `05-Audit-Lines.md`** - Enhance with:
   - Complete unit conversion integration
   - Count validation rules
   - Data entry optimization
   - Barcode scanning integration

4. **Add implementation details:**
   - Background job processing
   - Real-time updates
   - Notification system
   - Mobile app specifications

#### 5. Procurement Domain (WEEK 5-8)

**Why Fifth:**
- Can be developed in parallel with Inventory
- Depends on Products and Departments (both built)
- Required for invoice receipt integration
- Ottimate integration needed

**Fine-Tuning Tasks:**

1. **Review `01-Vendor-Master.md`** - Complete vendor management
2. **Review `02-Purchase-Orders.md`** - Ottimate integration details
3. **Review `03-Invoice-Receipt.md`** - Complete invoice processing
4. **Create `04-Ottimate-Integration.md`** - Integration specifications

#### 6. Recipes Domain (WEEK 7-10)

**Why Sixth:**
- Depends on Products and Inventory
- Required for POS depletion calculations
- Complex domain with costing calculations
- Can be developed alongside Inventory enhancements

**Fine-Tuning Tasks:**

1. **Review `01-Recipe-Master.md`** - Complete recipe structure
2. **Review `02-Recipe-Costing.md`** - Cost calculation algorithms
3. **Review `03-Recipe-Batches.md`** - Batch production workflows
4. **Review `04-POS-Item-Mapping.md`** - POS integration requirements

### Phase 3: Integration (WEEK 11-14)

#### 7. POS Integration (WEEK 11-12)

**Why Seventh:**
- Depends on Products, Recipes, Inventory
- Critical for automatic depletion tracking
- Requires all foundation domains working

**Development Priority:** High - enables automatic inventory tracking

#### 8. Transfers & Depletions (WEEK 13-14)

**Why Eighth:**
- Depends on Products, Departments, Inventory
- Completes inventory movement tracking
- Required for complete inventory picture

**Development Priority:** High - completes core functionality

### Phase 4: Reporting & Advanced (WEEK 15+)

#### 9. Analytics & Reporting

**Development Priority:** Medium - can be built incrementally

#### 10. Accounting Integration

**Development Priority:** Medium - required for financial reporting

#### 11. Director (Multi-Location)

**Development Priority:** Medium - required for multi-location operations

#### 12. Budgets

**Development Priority:** Medium - important for financial control

### Phase 5: Deferred (12+ months)

- Payment Processing
- Detailed Ordering Workflows
- Detailed Receiving
- Invoice Processing (OCR, AI)

---

## Development Checklist

### Before Starting Development

- [ ] Read `docs/README.md` (main entry point)
- [ ] Read `AGENT-INSTRUCTIONS.md` (if AI agent)
- [ ] Read `CROSS-DOMAIN-REFERENCE.md` (integration patterns)
- [ ] Read domain-specific README
- [ ] Read function documentation
- [ ] Understand dependencies
- [ ] Check for existing implementations
- [ ] Review architecture documentation (`00-ARCHITECTURE/`)

### During Development

**Code Quality:**
- [ ] Follow established patterns
- [ ] Use shared utilities (no duplication)
- [ ] Write clean, maintainable code
- [ ] Add code comments for complex logic
- [ ] Follow Frappe best practices
- [ ] Use type hints where appropriate

**DocType & Module Structure:**
- [ ] For every DocType created, add the Python controller file (even if empty) inside `doctype/<doctype>/<doctype>.py`
- [ ] Ensure `__init__.py` exists in each new module directory
- [ ] Keep DocType JSON definitions in sync by exporting via `bench export-doc`
- [ ] Update fixtures if new fixtures are required

**Architecture Compliance:**
- [ ] Support department filtering in all queries
- [ ] Respect department permissions
- [ ] Use primary count units for storage
- [ ] Follow 2D inventory model (Product + Department)
- [ ] Use Product's conversion methods (don't duplicate)
- [ ] Include storage as metadata only

**Validation & Error Handling:**
- [ ] Add validation rules for all fields
- [ ] Implement proper error handling
- [ ] Handle edge cases gracefully
- [ ] Provide clear error messages
- [ ] Log errors appropriately

**Testing:**
- [ ] Write unit tests for business logic
- [ ] Write integration tests for workflows
- [ ] Test API endpoints
- [ ] Test permission checks
- [ ] Test with different user roles
- [ ] Test department filtering

**Documentation:**
- [ ] Update implementation summary
- [ ] Document API endpoints
- [ ] Add inline code comments
- [ ] Update README if needed
- [ ] Add usage examples

### Before Committing

**Code Review:**
- [ ] Test functionality manually
- [ ] Run automated tests
- [ ] Check for linter errors
- [ ] Verify no console errors
- [ ] Check integration points
- [ ] Review code changes

**Git Practices:**
- [ ] Clear commit message
- [ ] Follow commit message format
- [ ] Atomic commits (one logical change)
- [ ] No debug code left in
- [ ] No commented-out code
- [ ] No unnecessary changes

**Documentation:**
- [ ] Update documentation if needed
- [ ] Add/update tests
- [ ] Update IMPLEMENTATION-SUMMARY.md
- [ ] Update API-REFERENCE.md if needed

### Before Merging to Main

**Quality Assurance:**
- [ ] All tests pass
- [ ] Code reviewed (if working with team)
- [ ] Documentation updated
- [ ] No merge conflicts
- [ ] Integration tested
- [ ] Performance acceptable
- [ ] Error handling complete
- [ ] No TODO comments left unresolved

**Deployment Readiness:**
- [ ] Migrations tested
- [ ] Fixtures updated if needed
- [ ] No breaking changes (or documented)
- [ ] Backwards compatibility maintained
- [ ] Database indexes added if needed

**Communication:**
- [ ] PR description complete
- [ ] Breaking changes highlighted
- [ ] Migration notes provided
- [ ] API changes documented

---

## Quick Reference

### Essential Documents

**Getting Started:**
- `docs/README.md` - Main entry point (START HERE)
- `TESTING-GUIDE.md` - Testing practices
- `API-REFERENCE.md` - API documentation

**Architecture:**
- `00-ARCHITECTURE/01-App-Structure.md` - Current structure
- `00-ARCHITECTURE/02-Frappe-Framework.md` - Frappe guide
- `CROSS-DOMAIN-REFERENCE.md` - Integration patterns

**Development:**
- This file (`DEVELOPMENT-GUIDE.md`) - Complete roadmap
- Domain `README.md` files - Domain overviews
- Function documents - Detailed implementations

### Common Patterns

**Department Filtering:**
```python
def get_accessible_departments(user):
    """Get departments user has access to"""
    departments = frappe.get_all(
        'Department Permission',
        filters={'parent': user, 'can_read': 1},
        fields=['department']
    )
    return [d.department for d in departments]
```

**Unit Conversion:**
```python
# Always use Product's methods
product = frappe.get_doc('Product', product_name)
quantity_in_primary = product.convert_to_primary_unit(from_unit, quantity)
```

**Permission Checking:**
```python
if not has_department_permission(user, department, 'can_read'):
    frappe.throw(_("No access to department"))
```

---

## FAQ

**Q: Which domain should I start with?**  
A: Start with Products domain (next priority after Departments & Permissions).

**Q: How do I know if a domain is complete?**  
A: Check for `IMPLEMENTATION-SUMMARY.md` in the domain folder.

**Q: Where do I find API endpoints?**  
A: Check `API-REFERENCE.md` and domain-specific implementation summaries.

**Q: How do I test my changes?**  
A: See `TESTING-GUIDE.md` for comprehensive testing instructions.

**Q: What if I need to add a separate frontend?**  
A: See `00-ARCHITECTURE/04-Separate-Frontend.md` for SPA architecture guide.

---

**Last Updated**: November 8, 2025  
**Version**: 1.1

