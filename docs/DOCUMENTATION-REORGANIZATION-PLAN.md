# Documentation Reorganization Plan

**Date:** 2025-11-16
**Purpose:** Clean up and reorganize documentation to focus on Company Management MVP
**Status:** Proposed - Awaiting Approval

---

## Current Situation

**Problem:**
- Documentation is cluttered with outdated plans (Products/Inventory MVP, Phase 2 rewrites)
- Multiple conflicting strategy documents
- Unclear what's relevant vs. future work
- Hard to find current priorities

**Solution:**
- Archive outdated/future documentation
- Create clear structure focused on Company Management MVP
- Move operations modules (Products, Inventory, etc.) to "future work" folder
- Keep only essential, current documentation at root level

---

## Proposed New Structure

```
docs/
├── README.md                          # Main entry point - UPDATED for Company Management MVP
├── QUICK-START.md                     # NEW - How to get started with current project
├── COMPANY-MANAGEMENT-MVP.md          # NEW - MVP scope and requirements
│
├── 00-CURRENT/                        # NEW - Current active work
│   ├── 01-SCOPE.md                    # MVP scope and timeline
│   ├── 02-ARCHITECTURE.md             # Current architecture decisions
│   ├── 03-DATA-MODEL.md               # DocTypes and relationships
│   ├── 04-API-DESIGN.md               # API endpoints
│   ├── 05-FRONTEND-DESIGN.md          # Next.js structure
│   └── 06-DEMO-PLAN.md                # 1-month demo preparation
│
├── 01-CORE-PLATFORM/                  # Core infrastructure (current)
│   ├── Authentication.md
│   ├── Permissions.md
│   ├── Departments.md
│   └── Subscriptions.md
│
├── 02-COMPANY-MANAGEMENT/             # NEW - Company Management domain
│   ├── README.md
│   ├── 01-Company-Master.md
│   ├── 02-Company-Relationships.md
│   ├── 03-Task-Automation.md
│   ├── 04-Review-Periods.md
│   ├── 05-Project-Tracking.md
│   └── 06-Dashboard.md
│
├── 03-FINANCE/                        # Finance & Accounting (current)
│   ├── README.md
│   ├── Intercompany-Accounting.md
│   ├── Company-Groups.md
│   └── Settlements.md
│
├── API/                               # API Documentation
│   ├── Authentication.md
│   ├── Finance.md
│   ├── Company-Management.md          # NEW
│   └── Reference.md
│
├── GUIDES/                            # Development guides
│   ├── Development-Guide.md
│   ├── Testing-Guide.md
│   ├── Git-Workflow.md
│   └── Deployment.md
│
├── ARCHIVE/                           # OLD/OUTDATED - Move here
│   ├── old-mvp-plans/
│   │   ├── LINEAR-MVP-ISSUES.md
│   │   ├── LINEAR-QUICK-START.md
│   │   ├── LINEAR-RESTRUCTURING-PLAN.md
│   │   └── LINEAR-Q1-NEXT-JS-ISSUES.md
│   ├── phase-2-plans/
│   │   ├── DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md
│   │   ├── FRAPPE-TO-FASTAPI-PORTING-GUIDE.md
│   │   ├── REFACTORING-PLAN-1-FULL-NEXTJS.md
│   │   └── REFACTORING-PLAN-2-GRADUAL-MIGRATION.md
│   ├── old-architecture/
│   │   ├── 00-ARCHITECTURE/legacy/
│   │   └── CONSOLIDATION-PRD.md
│   └── old-decision-logs/
│       └── DECISION_LOG.md
│
└── FUTURE/                            # Future work - Not current priority
    ├── Operations-Modules/
    │   ├── 01-PRODUCTS/
    │   ├── 03-INVENTORY/
    │   ├── 04-PROCUREMENT/
    │   ├── 05-RECIPES/
    │   ├── 06-POS-INTEGRATION/
    │   ├── 08-TRANSFERS-DEPLETIONS/
    │   ├── 09-ANALYTICS-REPORTING/
    │   ├── 10-DIRECTOR/
    │   ├── 12-BUDGETS/
    │   ├── 13-PAYMENTS/
    │   └── 99-INTEGRATIONS/
    └── README.md                      # Explains future roadmap
```

---

## Files to Archive

### Outdated MVP Planning Docs
Move to `ARCHIVE/old-mvp-plans/`:
- `LINEAR-MVP-ISSUES.md` - Products/Inventory MVP (wrong scope)
- `LINEAR-QUICK-START.md` - Implementation guide for wrong MVP
- `LINEAR-RESTRUCTURING-PLAN.md` - Restructuring for wrong MVP
- `LINEAR-Q1-NEXT-JS-ISSUES.md` - Old Q1 planning
- `PROJECT-TIMELINE.md` - Outdated timeline

### Future Phase 2 Planning Docs
Move to `ARCHIVE/phase-2-plans/`:
- `DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md` - Phase 2 rewrite (future, not current)
- `FRAPPE-TO-FASTAPI-PORTING-GUIDE.md` - Migration guide (future)
- `REFACTORING-PLAN-1-FULL-NEXTJS.md` - Old refactoring plan
- `REFACTORING-PLAN-2-GRADUAL-MIGRATION.md` - Old refactoring plan

### Old Architecture & PRDs
Move to `ARCHIVE/old-architecture/`:
- `CONSOLIDATION-PRD.md` - Old PRD document
- `ERPNEXT-V15-ALIGNMENT-ANALYSIS.md` - Analysis doc
- `00-ARCHITECTURE/legacy/` - Already in legacy folder

### Old Decision Logs
Move to `ARCHIVE/old-decision-logs/`:
- `DECISION_LOG.md` - Superseded by CONSOLIDATED_DECISION_LOG.md

### Specific Issue Plans
Move to `ARCHIVE/issue-plans/`:
- `BLK-15-IMPLEMENTATION-PLAN.md`
- `BLK-15-LINEAR-ISSUES.md`

---

## Files to Move to FUTURE/

### Operations Modules (Not Current Priority)
Move to `FUTURE/Operations-Modules/`:
- `01-PRODUCTS/` - Product management (future)
- `03-INVENTORY/` - Inventory management (future)
- `04-PROCUREMENT/` - Procurement (future)
- `05-RECIPES/` - Recipe costing (future)
- `06-POS-INTEGRATION/` - POS integration (future)
- `08-TRANSFERS-DEPLETIONS/` - Transfers (future)
- `09-ANALYTICS-REPORTING/` - Analytics (future)
- `10-DIRECTOR/` - Multi-location (future)
- `12-BUDGETS/` - Budgeting (future)
- `13-PAYMENTS/` - Payments (future)
- `99-INTEGRATIONS/` - Integrations (future)

**Note:** These are valuable planning docs for future work, but not current MVP priority.

---

## Files to Keep at Root Level

### Essential Current Documentation
- `README.md` - Main entry point (WILL UPDATE)
- `CONSOLIDATED_DECISION_LOG.md` - Decision history
- `AGENT-INSTRUCTIONS.md` - AI agent guide
- `CHANGELOG.md` - Change history
- `CROSS-DOMAIN-REFERENCE.md` - Integration patterns
- `FIXTURES-INFO.md` - Fixtures reference
- `PERMISSION-FIELDS-REFERENCE.md` - Permission fields
- `FUNCTIONALITY_AUDIT_CHECKLIST.md` - QA checklist

### Core Implementation (Current)
- `02-DEPARTMENTS/` - Departments domain (complete)
- `11-PERMISSIONS/` - Permissions domain (complete)
- `00-ARCHITECTURE/` - Keep non-legacy architecture docs

### API Documentation (Current)
- `API-AUTHENTICATION.md`
- `API-FINANCE.md`
- `API-INVENTORY.md` (minimal - some inventory APIs exist)
- `API-REFERENCE.md`

### Guides
- `DEVELOPMENT-GUIDE.md`
- `TESTING-GUIDE.md`
- `GIT-WORKFLOW.md`
- `ADMIN-UI-GUIDE.md`

### Accounting Domain (Current)
- `07-ACCOUNTING/` - Keep (intercompany accounting is current work)

---

## New Files to Create

### Quick Start Guide
`QUICK-START.md` - How to get started with the Company Management MVP project

### Company Management MVP Scope
`COMPANY-MANAGEMENT-MVP.md` - Complete scope document:
- User personas (Management Company Leadership, Accounting Teams)
- Core features (Company Management, Relationships, Tasks, Reviews, Projects)
- Timeline (1 month to demo)
- Success criteria

### Current Work Documentation
`00-CURRENT/` folder with:
1. `01-SCOPE.md` - MVP scope and requirements
2. `02-ARCHITECTURE.md` - Current architecture decisions
3. `03-DATA-MODEL.md` - DocTypes: Company, Relationships, Tasks, Reviews, Projects
4. `04-API-DESIGN.md` - API endpoints needed
5. `05-FRONTEND-DESIGN.md` - Next.js pages and components
6. `06-DEMO-PLAN.md` - Demo preparation and walkthrough

### Company Management Domain
`02-COMPANY-MANAGEMENT/` folder with complete domain documentation

---

## Updated README.md Structure

```markdown
# BLKSHP OS - Company Management Platform

**Multi-entity hospitality company management and accounting automation**

## What is BLKSHP OS?

BLKSHP OS is a management platform for hospitality companies operating multiple properties/entities.
It provides company/entity management, relationship tracking, task automation, and financial oversight.

**Current Focus:** Company Management MVP for internal demo (1-month timeline)

## Quick Start

See [QUICK-START.md](QUICK-START.md) for setup instructions.

## Current MVP Scope

**Target Users:**
- Multi-entity management company leadership
- Accounting and finance teams

**Core Features:**
1. Company/Entity Directory & Details
2. Company Relationships (Banks, Tax Entities, Insurance, Loans, Key Employees)
3. Automated Task Management (daily/weekly/monthly/quarterly/annual)
4. Review Period Tracking (month-end close)
5. Project Tracking
6. Accounting Dashboard

**Timeline:** 1 month to working demo

See [COMPANY-MANAGEMENT-MVP.md](COMPANY-MANAGEMENT-MVP.md) for complete scope.

## Documentation

### Getting Started
- [Quick Start](QUICK-START.md)
- [Company Management MVP Scope](COMPANY-MANAGEMENT-MVP.md)
- [Development Guide](GUIDES/Development-Guide.md)

### Current Work
- [00-CURRENT/](00-CURRENT/) - Active MVP development docs
- [02-COMPANY-MANAGEMENT/](02-COMPANY-MANAGEMENT/) - Company Management domain
- [03-FINANCE/](03-FINANCE/) - Finance & Intercompany Accounting

### API Documentation
- [Authentication API](API/Authentication.md)
- [Finance API](API/Finance.md)
- [Company Management API](API/Company-Management.md)

### Core Platform
- [Departments](01-CORE-PLATFORM/Departments.md)
- [Permissions](01-CORE-PLATFORM/Permissions.md)
- [Authentication](01-CORE-PLATFORM/Authentication.md)

### Future Work
See [FUTURE/](FUTURE/) for planned operations modules (inventory, recipes, etc.)
```

---

## Implementation Steps

### Step 1: Create Archive Structure
```bash
cd docs
mkdir -p ARCHIVE/old-mvp-plans
mkdir -p ARCHIVE/phase-2-plans
mkdir -p ARCHIVE/old-architecture
mkdir -p ARCHIVE/old-decision-logs
mkdir -p ARCHIVE/issue-plans
```

### Step 2: Create Future Structure
```bash
mkdir -p FUTURE/Operations-Modules
```

### Step 3: Move Outdated Docs
```bash
# Old MVP plans
mv LINEAR-MVP-ISSUES.md ARCHIVE/old-mvp-plans/
mv LINEAR-QUICK-START.md ARCHIVE/old-mvp-plans/
mv LINEAR-RESTRUCTURING-PLAN.md ARCHIVE/old-mvp-plans/
mv LINEAR-Q1-NEXT-JS-ISSUES.md ARCHIVE/old-mvp-plans/
mv PROJECT-TIMELINE.md ARCHIVE/old-mvp-plans/

# Phase 2 plans
mv DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md ARCHIVE/phase-2-plans/
mv FRAPPE-TO-FASTAPI-PORTING-GUIDE.md ARCHIVE/phase-2-plans/
mv REFACTORING-PLAN-1-FULL-NEXTJS.md ARCHIVE/phase-2-plans/
mv REFACTORING-PLAN-2-GRADUAL-MIGRATION.md ARCHIVE/phase-2-plans/

# Old architecture
mv CONSOLIDATION-PRD.md ARCHIVE/old-architecture/
mv ERPNEXT-V15-ALIGNMENT-ANALYSIS.md ARCHIVE/old-architecture/

# Old decision logs
mv DECISION_LOG.md ARCHIVE/old-decision-logs/

# Issue plans
mv BLK-15-IMPLEMENTATION-PLAN.md ARCHIVE/issue-plans/
mv BLK-15-LINEAR-ISSUES.md ARCHIVE/issue-plans/
```

### Step 4: Move Operations Modules to Future
```bash
mv 01-PRODUCTS FUTURE/Operations-Modules/
mv 03-INVENTORY FUTURE/Operations-Modules/
mv 04-PROCUREMENT FUTURE/Operations-Modules/
mv 05-RECIPES FUTURE/Operations-Modules/
mv 06-POS-INTEGRATION FUTURE/Operations-Modules/
mv 08-TRANSFERS-DEPLETIONS FUTURE/Operations-Modules/
mv 09-ANALYTICS-REPORTING FUTURE/Operations-Modules/
mv 10-DIRECTOR FUTURE/Operations-Modules/
mv 12-BUDGETS FUTURE/Operations-Modules/
mv 13-PAYMENTS FUTURE/Operations-Modules/
mv 99-INTEGRATIONS FUTURE/Operations-Modules/
```

### Step 5: Reorganize Current Docs
```bash
# Create new structure
mkdir -p 00-CURRENT
mkdir -p 01-CORE-PLATFORM
mkdir -p 02-COMPANY-MANAGEMENT
mkdir -p 03-FINANCE
mkdir -p API
mkdir -p GUIDES

# Move API docs
mv API-*.md API/

# Move guides
mv DEVELOPMENT-GUIDE.md GUIDES/Development-Guide.md
mv TESTING-GUIDE.md GUIDES/Testing-Guide.md
mv GIT-WORKFLOW.md GUIDES/Git-Workflow.md

# Reorganize architecture
mkdir -p 01-CORE-PLATFORM
# Keep 02-DEPARTMENTS and 11-PERMISSIONS as is for now

# Move accounting
mv 07-ACCOUNTING 03-FINANCE
```

### Step 6: Create New Documentation
- Create `QUICK-START.md`
- Create `COMPANY-MANAGEMENT-MVP.md`
- Create `00-CURRENT/` docs
- Create `02-COMPANY-MANAGEMENT/` docs
- Update `README.md`

---

## Benefits of Reorganization

### Clarity
- Easy to find what's current vs. future vs. archived
- Clear focus on Company Management MVP
- No confusion about priorities

### Maintainability
- Archived docs don't clutter searches
- Future work clearly separated
- Current work easy to navigate

### Onboarding
- New developers/AI agents can quickly understand current state
- Clear documentation hierarchy
- Obvious starting points (README, QUICK-START, MVP scope)

### Context Management
- Reduced cognitive load
- Better for AI context windows
- Easier to find relevant information

---

## Approval Needed

**Questions for Review:**

1. **Archive Strategy:** Approve moving outdated docs to ARCHIVE/?
2. **Future Work:** Approve moving operations modules to FUTURE/?
3. **New Structure:** Approve the proposed 00-CURRENT/, 02-COMPANY-MANAGEMENT/ structure?
4. **README Update:** Approve focusing README on Company Management MVP?
5. **Timing:** Execute this reorganization now, or after we define MVP scope?

**Recommendation:** Execute reorganization NOW to clean up context, THEN define MVP scope with clean slate.

---

## Next Steps After Approval

1. Execute file moves (Steps 1-5 above)
2. Create COMPANY-MANAGEMENT-MVP.md scope document
3. Create 00-CURRENT/ planning docs
4. Update README.md
5. Create 02-COMPANY-MANAGEMENT/ domain docs
6. Update Linear projects to match new structure
7. Begin MVP implementation

---

**Status:** Awaiting approval to proceed
**Estimated Time:** 1-2 hours to execute reorganization
