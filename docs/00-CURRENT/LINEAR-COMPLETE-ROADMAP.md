# The Pass - Complete Linear Roadmap

**Product Name:** The Pass
**Current Focus:** Company Management MVP
**Timeline:** MVP (1 month) → Full Platform (6-12 months)
**Date Created:** 2025-11-16

---

## Overview

This document provides the **complete roadmap** from MVP to final product release, organized as Linear projects, milestones, and issues with clear dependencies.

### Roadmap Phases

1. **Phase 1: Company Management MVP** (1 month) - Active NOW
2. **Phase 2: Operations Modules** (3-6 months) - After MVP approval
3. **Phase 3: Platform Enhancement** (3-6 months) - Advanced features
4. **Phase 4: Scale & Optimize** (Ongoing) - Production readiness

---

## Issue Naming Convention

**Format:** `[Type]-[Number]: Brief Description`

**Types:**
- `Feature` - New feature development
- `Bug` - Bug fixes
- `Enhancement` - Improvements to existing features
- `Integration` - Third-party integrations
- `Refactor` - Code refactoring
- `Docs` - Documentation
- `Test` - Testing tasks
- `Deploy` - Deployment tasks
- `Design` - Design/planning tasks

**Examples:**
- `Feature-001: Company Directory Page`
- `Bug-042: Fix date picker timezone issue`
- `Integration-015: QuickBooks API connection`
- `Enhancement-023: Add bulk edit to tasks`

---

## Labels System

### Priority Labels
- `🔴 urgent` - Critical for current milestone
- `🟠 high` - Important, should be done soon
- `🟡 medium` - Standard priority
- `⚪ low` - Nice to have

### Type Labels
- `backend` - Backend/API work
- `frontend` - Frontend UI work
- `full-stack` - Both backend and frontend
- `database` - Database schema/migrations
- `infrastructure` - DevOps/deployment

### Domain Labels
- `company-mgmt` - Company management features
- `relationships` - Company relationships
- `tasks` - Task automation
- `reviews` - Review periods
- `projects` - Project tracking
- `finance` - Finance/accounting
- `inventory` - Inventory management
- `recipes` - Recipe costing
- `procurement` - Procurement
- `pos` - POS integration
- `analytics` - Analytics/reporting

### Status Labels
- `blocked` - Blocked by dependency
- `in-review` - In code review
- `ready-test` - Ready for testing
- `demo-critical` - Must have for demo

---

# PHASE 1: COMPANY MANAGEMENT MVP

**Timeline:** 2025-11-16 to 2025-12-16 (4 weeks)
**Goal:** Working demo for leadership
**Status:** ACTIVE

---

## PROJECT 1: Company Management MVP

### Project Details
- **Timeline:** 4 weeks
- **Team:** Solo developer (18 hrs/week)
- **Success Criteria:**
  - [ ] Leadership can manage companies and relationships
  - [ ] Task automation working
  - [ ] Monthly close tracking functional
  - [ ] Dashboard shows real KPIs
  - [ ] Demo ready by Dec 14-16

---

## Milestone 1.1: Planning & Design

**Dates:** 2025-11-16 to 2025-11-22 (Week 1)
**Goal:** Complete system design

### Design-001: Company Management Data Model
- **Type:** Design
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, company-mgmt, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-11-16
- **Target Date:** 2025-11-16
- **Dependencies:** None
- **Description:** Design complete DocType schema for all Company Management features
- **Deliverables:**
  - [ ] Company DocType schema
  - [ ] All Relationship DocTypes (Banks, Tax, Insurance, Loans, Employees)
  - [ ] Task Type DocType schema
  - [ ] Review Period DocType schema
  - [ ] Project DocType schema
  - [ ] Field specifications with validation rules
  - [ ] Relationship diagrams
- **Acceptance Criteria:**
  - All DocTypes defined with complete field lists
  - Data types specified
  - Validation rules documented
  - Relationships mapped
  - Schema reviewed and approved

**Blocks:** Feature-001, Feature-002, Feature-003, Feature-004, Feature-005, Feature-006, Feature-007, Feature-008

---

### Design-002: API Endpoint Design
- **Type:** Design
- **Priority:** 🔴 Urgent
- **Labels:** backend, company-mgmt, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-11-17
- **Target Date:** 2025-11-17
- **Dependencies:** Design-001
- **Description:** Design all REST API endpoints for Company Management
- **Deliverables:**
  - [ ] Company CRUD endpoints
  - [ ] Relationships CRUD endpoints
  - [ ] Task automation endpoints
  - [ ] Review Period endpoints
  - [ ] Project endpoints
  - [ ] Dashboard KPI endpoints
  - [ ] Request/response schemas
  - [ ] Permission requirements
- **Acceptance Criteria:**
  - All endpoints documented
  - Request/response formats defined
  - Permission model specified
  - Error handling documented

**Blocks:** Feature-009

---

### Design-003: Frontend Architecture
- **Type:** Design
- **Priority:** 🔴 Urgent
- **Labels:** frontend, company-mgmt, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-11-18
- **Target Date:** 2025-11-18
- **Dependencies:** Design-002
- **Description:** Design Next.js frontend structure, pages, and components
- **Deliverables:**
  - [ ] Page structure and routes
  - [ ] Component hierarchy
  - [ ] Navigation flow
  - [ ] State management approach
  - [ ] Data fetching strategy
  - [ ] Form handling approach
  - [ ] Wireframes for key pages
- **Acceptance Criteria:**
  - All pages identified
  - Component structure defined
  - Data flow documented
  - Design reviewed and approved

**Blocks:** Feature-010, Feature-011, Feature-012, Feature-013, Feature-014, Feature-015, Feature-016

---

### Design-004: Demo Walkthrough Script
- **Type:** Design
- **Priority:** 🟠 High
- **Labels:** demo-critical
- **Estimate:** 0.5 day
- **Start Date:** 2025-11-19
- **Target Date:** 2025-11-19
- **Dependencies:** Design-003
- **Description:** Create complete demo script for leadership presentation
- **Deliverables:**
  - [ ] Demo storyline
  - [ ] Key talking points
  - [ ] Demo data requirements
  - [ ] Screenshots/mockups
  - [ ] Success metrics
  - [ ] Q&A preparation
- **Acceptance Criteria:**
  - Complete demo script written
  - Talking points clear
  - Demo flow logical
  - Timing appropriate (10-15 min)

---

## Milestone 1.2: Backend Foundation

**Dates:** 2025-11-20 to 2025-11-29 (Week 2)
**Goal:** Core DocTypes and APIs functional

> **Note:** This milestone has been updated to reflect the normalized three-tier data architecture and task management system per Design-001 updates (2025-11-23). New DocTypes added: Property, Property Company Relationship, Task Default Template. Each relationship DocType now includes Task Setting child tables.

### Feature-NEW: Property DocType (BLK-196)
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, company-mgmt, demo-critical
- **Estimate:** 1 day
- **Target Date:** 2025-11-24
- **Dependencies:** Design-001
- **Description:** Create Property DocType for operational units (hotels, restaurants, venues). Properties are where work happens, distinct from Companies (legal entities).
- **Key Fields:** property_name, property_code, property_type, property_status, management dates
- **Child Tables:** Property Address, Property Phone, Property Email, Property Contact, Property Department, Property Task Setting
- **Acceptance Criteria:**
  - Property can be created with all fields
  - Department heads link to Key Employee Relationship
  - Task settings configurable per property

**Blocks:** Property Company Relationship, Key Employee updates

---

### Feature-NEW: Property Company Relationship DocType (BLK-197)
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, relationships, demo-critical
- **Estimate:** 0.5 day
- **Target Date:** 2025-11-24
- **Dependencies:** Design-001, Property DocType
- **Description:** Junction table linking Properties (operational units) to Companies (legal entities)
- **Key Fields:** property (Link), company (Link), entity_role (free text), relationship dates
- **Acceptance Criteria:**
  - Can link multiple companies to one property
  - Entity role describes company function (e.g., "Operating LP", "Liquor License Holder")
  - Visible from both Property and Company views

**Blocked By:** Property DocType
**Blocks:** Key Employee updates

---

### Feature-001: Enhanced Company DocType (BLK-122)
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, company-mgmt, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-11-20
- **Target Date:** 2025-11-20
- **Dependencies:** Design-001
- **Description:** Enhance Company DocType with all required fields
- **Fields to Add:**
  - Legal name, DBA name
  - EIN/Tax ID (encrypted)
  - Billing address (street, city, state, zip, country)
  - Physical address (street, city, state, zip, country)
  - Mailing address (street, city, state, zip, country)
  - Phone number (primary, secondary)
  - Email (primary, accounting, support)
  - Website URL
  - Status (Active, Inactive, Pending)
  - Entity type (LLC, Corporation, Partnership, Sole Proprietorship)
  - Formation date
  - State of formation
  - Ownership structure
  - Parent company (self-link)
  - Notes/description
- **Deliverables:**
  - [ ] All fields added to Company DocType
  - [ ] Validation rules implemented
  - [ ] Encryption for sensitive fields (EIN)
  - [ ] Can create/edit via Frappe Desk
  - [ ] Unit tests passing
- **Acceptance Criteria:**
  - All fields functional
  - Validation working correctly
  - Encryption working
  - Tests cover all fields

**Blocked By:** Design-001
**Blocks:** Feature-002, Feature-003, Feature-004, Feature-005, Feature-006

---

### Feature-002: Bank Relationship DocType
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, relationships, demo-critical
- **Estimate:** 0.5 day
- **Start Date:** 2025-11-21
- **Target Date:** 2025-11-21
- **Dependencies:** Design-001, Feature-001
- **Description:** Create DocType to track banking relationships
- **Fields:**
  - Company (Link to Company)
  - Bank name
  - Account type (Checking, Savings, Money Market, Loan, Credit Line)
  - Account number (encrypted)
  - Routing number
  - Account status (Active, Closed, Dormant)
  - Opening date
  - Closing date
  - Current balance
  - Primary contact name
  - Primary contact phone
  - Primary contact email
  - Online banking URL
  - Notes
- **Deliverables:**
  - [ ] DocType created
  - [ ] Linked to Company
  - [ ] Encryption for account number
  - [ ] Can CRUD via Frappe Desk
  - [ ] Unit tests
- **Acceptance Criteria:**
  - DocType functional
  - Company linkage working
  - Encryption working
  - CRUD operations work

**Blocked By:** Design-001, Feature-001
**Blocks:** Feature-009

---

### Feature-003: Tax Entity Relationship DocType
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, relationships, demo-critical
- **Estimate:** 0.5 day
- **Start Date:** 2025-11-21
- **Target Date:** 2025-11-21
- **Dependencies:** Design-001, Feature-001
- **Description:** Create DocType for tax entity relationships
- **Fields:**
  - Company (Link to Company)
  - Tax entity type (Federal, State, Local, Sales Tax, Payroll Tax)
  - Tax ID/EIN
  - Jurisdiction (state, county, city)
  - Filing frequency (Monthly, Quarterly, Annual)
  - Due dates (comma-separated or child table)
  - Responsible party name
  - Responsible party email
  - Notes
- **Deliverables:**
  - [ ] DocType created
  - [ ] Linked to Company
  - [ ] Can CRUD via Frappe Desk
  - [ ] Unit tests
- **Acceptance Criteria:**
  - DocType functional
  - Company linkage working
  - All fields working

**Blocked By:** Design-001, Feature-001
**Blocks:** Feature-009

---

### Feature-004: Insurance Relationship DocType
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, relationships, demo-critical
- **Estimate:** 0.5 day
- **Start Date:** 2025-11-22
- **Target Date:** 2025-11-22
- **Dependencies:** Design-001, Feature-001
- **Description:** Create DocType for insurance policies
- **Fields:**
  - Company (Link to Company)
  - Insurance type (General Liability, Property, Workers Comp, Umbrella, Cyber, D&O, E&O, Auto, Health, Life, Other)
  - Provider name
  - Policy number
  - Coverage amount
  - Deductible
  - Annual premium
  - Effective date
  - Expiration date
  - Renewal date
  - Auto-renew (checkbox)
  - Agent name
  - Agent phone
  - Agent email
  - Status (Active, Expired, Cancelled, Pending)
  - Certificate of insurance (file attachment)
  - Notes
- **Deliverables:**
  - [ ] DocType created
  - [ ] Linked to Company
  - [ ] File attachment working
  - [ ] Can CRUD via Frappe Desk
  - [ ] Unit tests
- **Acceptance Criteria:**
  - DocType functional
  - Company linkage working
  - File uploads working
  - All fields working

**Blocked By:** Design-001, Feature-001
**Blocks:** Feature-009

---

### Feature-005: Loan Relationship DocType
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, relationships, demo-critical
- **Estimate:** 0.5 day
- **Start Date:** 2025-11-22
- **Target Date:** 2025-11-22
- **Dependencies:** Design-001, Feature-001
- **Description:** Create DocType for loan tracking
- **Fields:**
  - Company (Link to Company)
  - Lender name
  - Loan type (Term Loan, Line of Credit, Mortgage, SBA 7(a), SBA 504, Equipment Financing, Other)
  - Loan amount
  - Interest rate (%)
  - Term length (months)
  - Monthly payment
  - Origination date
  - Maturity date
  - Current balance
  - Account number (encrypted)
  - Loan status (Active, Paid Off, In Default, Refinanced)
  - Collateral description
  - Guarantors (Text or child table)
  - Payment frequency (Monthly, Quarterly, etc.)
  - Last payment date
  - Next payment date
  - Notes
- **Deliverables:**
  - [ ] DocType created
  - [ ] Linked to Company
  - [ ] Encryption for account number
  - [ ] Can CRUD via Frappe Desk
  - [ ] Unit tests
- **Acceptance Criteria:**
  - DocType functional
  - Company linkage working
  - Encryption working
  - All fields working

**Blocked By:** Design-001, Feature-001
**Blocks:** Feature-009

---

### Feature-006: Key Employee Relationship DocType
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, relationships, demo-critical
- **Estimate:** 0.5 day
- **Start Date:** 2025-11-23
- **Target Date:** 2025-11-23
- **Dependencies:** Design-001, Feature-001
- **Description:** Create DocType for key employee tracking
- **Fields:**
  - Company (Link to Company)
  - Employee name
  - Role/Title
  - Email
  - Phone (work, mobile)
  - Start date
  - End date
  - Status (Active, Inactive, On Leave)
  - Department
  - Responsibilities (Long Text)
  - Emergency contact name
  - Emergency contact phone
  - Notes
- **Deliverables:**
  - [ ] DocType created
  - [ ] Linked to Company
  - [ ] Can CRUD via Frappe Desk
  - [ ] Unit tests
- **Acceptance Criteria:**
  - DocType functional
  - Company linkage working
  - All fields working

**Blocked By:** Design-001, Feature-001
**Blocks:** Feature-009

---

### Feature-007: Task Type DocType - Knowledge Base (BLK-128)
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, tasks, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-11-24
- **Target Date:** 2025-11-26
- **Dependencies:** Design-001
- **Description:** Create Task Type DocType as a **knowledge base** for task definitions. This is NOT for scheduling - it contains instructions, checklists, and requirements. Actual scheduling is handled by Task Default Templates and Task Settings on relationship DocTypes.
- **Key Fields:**
  - task_code (unique), task_name, category, description
  - instructions, checklist, resources (knowledge base content)
  - requires_documentation, documentation_type, documentation_instructions
  - default_priority, default_estimated_time, default_assigned_role
  - is_active
- **Child Table:** Task Type Checklist Item (item, is_required, order)
- **Architecture Change:** Scheduling fields REMOVED - now handled by Task Settings on each DocType
- **Deliverables:**
  - [ ] DocType created (knowledge base only)
  - [ ] Checklist items child table
  - [ ] Instructions render as Markdown
  - [ ] No scheduling/recurrence fields
  - [ ] Unit tests
- **Acceptance Criteria:**
  - Task Type serves as knowledge base
  - No scheduling/recurrence fields
  - Linked from Task Default Templates and Task Settings

**Blocked By:** Design-001
**Blocks:** Task Default Template, Feature-008, Feature-017

---

### Feature-NEW: Task Default Template DocType (BLK-198)
- **Type:** Feature
- **Priority:** 🟠 High
- **Labels:** backend, database, tasks, demo-critical
- **Estimate:** 1 day
- **Target Date:** 2025-11-27
- **Dependencies:** Design-001, Feature-007 (Task Type)
- **Description:** Create Task Default Template DocType - defines auto-apply rules for task settings when specific record types are created.
- **Key Fields:**
  - template_name
  - applies_to_doctype (Bank Account, Tax Obligation, Insurance Policy, Loan Relationship, Company, Property)
  - subtype_field, subtype_value (for filtering by account_type, obligation_type, etc.)
  - task_type (Link)
  - default_recurrence, default_day_of_week, default_day_of_month
  - default_due_offset_days, trigger_field
  - default_assigned_role, requires_documentation
  - is_active
- **Example Templates:**
  - "Checking Account - Bank Reconciliation" → When Bank Account (Checking) created, add monthly Bank Reconciliation task
  - "Sales Tax - Tax Filing" → When Tax Obligation (Sales Tax) created, add monthly Tax Filing task
- **Deliverables:**
  - [ ] DocType created
  - [ ] Server-side hook to apply templates on record creation
  - [ ] Validation rules
  - [ ] Unit tests
- **Acceptance Criteria:**
  - Templates auto-apply when matching records are created
  - Subtype filtering works (e.g., only Checking accounts)
  - Settings can be overridden after creation

**Blocked By:** Feature-007 (Task Type)
**Blocks:** Feature-017 (Task Automation)

---

### Feature-008: Review Period DocType
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, database, reviews, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-11-25
- **Target Date:** 2025-11-25
- **Dependencies:** Design-001, Feature-007
- **Description:** Create DocType to track month-end close periods
- **Fields:**
  - Company (Link to Company)
  - Period name (e.g., "November 2025")
  - Period start date
  - Period end date
  - Target close date
  - Actual close date
  - Status (Open, In Progress, Controller Review, Executive Review, Closed)
  - Assigned controller (Link to User)
  - Assigned executive (Link to User)
  - Tasks (Child Table - Task instances)
    - Task Type (Link)
    - Task name
    - Assigned to (Link to User)
    - Due date
    - Completed date
    - Status (Not Started, In Progress, Completed)
    - Notes
  - Outstanding issues (Long Text)
  - Blockers (Long Text)
  - Notes (Long Text)
  - Created by
  - Modified by
- **Deliverables:**
  - [ ] DocType created
  - [ ] Status workflow configured
  - [ ] Tasks child table working
  - [ ] Linked to Company and Task Types
  - [ ] Can track progress
  - [ ] Unit tests
- **Acceptance Criteria:**
  - DocType functional
  - Workflow transitions working
  - Tasks can be added
  - Progress calculated correctly

**Blocked By:** Design-001, Feature-007
**Blocks:** Feature-009, Feature-017

---

### Feature-009: Company Management API Endpoints
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, company-mgmt, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-11-26
- **Target Date:** 2025-11-27
- **Dependencies:** Design-002, Feature-001, Feature-002, Feature-003, Feature-004, Feature-005, Feature-006, Feature-008
- **Description:** Create REST API endpoints for Company Management
- **Endpoints to Create:**
  - `get_company_details(company_id)` - Get company with all relationships
  - `list_companies(filters, limit, offset)` - List companies with pagination
  - `get_company_relationships(company_id, relationship_type)` - Get specific relationships
  - `get_company_banks(company_id)` - Get all bank relationships
  - `get_company_tax_entities(company_id)` - Get all tax entities
  - `get_company_insurance(company_id)` - Get all insurance policies
  - `get_company_loans(company_id)` - Get all loans
  - `get_company_employees(company_id)` - Get all key employees
  - `get_company_tasks(company_id, status)` - Get active/completed tasks
  - `get_company_review_periods(company_id, limit)` - Get review periods
  - `get_dashboard_kpis(company_id)` - Get KPIs for dashboard
  - `create_relationship(relationship_type, data)` - Generic relationship creator
  - `update_relationship(relationship_type, id, data)` - Generic relationship updater
- **Deliverables:**
  - [ ] All endpoints implemented in `/api/company_management.py`
  - [ ] Permission checks (company-level access)
  - [ ] Request validation
  - [ ] Response formatting
  - [ ] Error handling
  - [ ] Unit tests for all endpoints
  - [ ] API documentation updated
- **Acceptance Criteria:**
  - All endpoints working
  - Permissions enforced
  - Tests passing (100%)
  - Documentation complete

**Blocked By:** Design-002, Feature-001, Feature-002, Feature-003, Feature-004, Feature-005, Feature-006, Feature-008
**Blocks:** Feature-010, Feature-011, Feature-012, Feature-013, Feature-014, Feature-015, Feature-016

---

## Milestone 1.3: Task Automation & Frontend

**Dates:** 2025-11-30 to 2025-12-06 (Week 3)
**Goal:** Automation working, frontend pages built

### Feature-017: Task Automation Scheduler
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** backend, tasks, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-11-28
- **Target Date:** 2025-11-29
- **Dependencies:** Feature-007, Feature-008
- **Description:** Build scheduler to auto-create recurring tasks
- **Features:**
  - Daily scheduler (runs at 12:01 AM via Frappe cron)
  - Reads all active Task Type masters
  - Creates Task instances based on recurrence patterns
  - Assigns to correct users/roles
  - Links to Review Periods (for monthly close tasks)
  - Handles task dependencies (wait for prerequisite tasks)
  - Sends email notifications for new tasks
  - Logs all task creation
- **Deliverables:**
  - [ ] Scheduler function in `/tasks/automation.py`
  - [ ] Cron job configured in hooks.py
  - [ ] Recurrence logic for all patterns
  - [ ] Dependency checking
  - [ ] Email notification templates
  - [ ] Logging system
  - [ ] Unit tests
  - [ ] Integration tests
- **Acceptance Criteria:**
  - Scheduler runs daily
  - Tasks created correctly for all recurrence patterns
  - Dependencies enforced
  - Notifications sent
  - No duplicate task creation
  - Tests passing

**Blocked By:** Feature-007, Feature-008
**Blocks:** Feature-013

---

### Feature-010: Company Directory Page
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** frontend, company-mgmt, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-11-30
- **Target Date:** 2025-11-30
- **Dependencies:** Design-003, Feature-009
- **Description:** Build Next.js page to list and search companies
- **Page:** `/companies`
- **Features:**
  - Table of companies (name, status, entity type, city, state)
  - Search by name
  - Filter by status (Active, Inactive)
  - Filter by entity type
  - Sort by columns
  - Click row to view details
  - "Add Company" button
  - Loading skeletons
  - Empty state
- **Components:**
  - CompaniesTable
  - CompanyRow
  - SearchBar
  - FilterDropdowns
  - AddCompanyButton
- **Deliverables:**
  - [ ] Page component created
  - [ ] Table component
  - [ ] Search functionality
  - [ ] Filters working
  - [ ] Navigation to details
  - [ ] Loading states
  - [ ] Empty state
  - [ ] Responsive design
- **Acceptance Criteria:**
  - Page renders correctly
  - Data loads from API
  - Search works
  - Filters work
  - Navigation works
  - Mobile responsive

**Blocked By:** Design-003, Feature-009
**Blocks:** None

---

### Feature-011: Company Detail Page
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** frontend, company-mgmt, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-12-01
- **Target Date:** 2025-12-02
- **Dependencies:** Design-003, Feature-009
- **Description:** Build page showing company details and all relationships
- **Page:** `/companies/[id]`
- **Sections:**
  - Company Information (header with key details)
  - Overview Tab (summary, status, key metrics)
  - Relationships Tabs:
    - Banks
    - Tax Entities
    - Insurance
    - Loans
    - Key Employees
  - Edit button (navigates to edit page)
- **Components:**
  - CompanyHeader
  - CompanyOverview
  - RelationshipTabs
  - BanksList
  - TaxEntitiesList
  - InsuranceList
  - LoansList
  - EmployeesList
  - EditButton
- **Deliverables:**
  - [ ] Page component
  - [ ] All tab components
  - [ ] Data fetching from API
  - [ ] Loading states
  - [ ] Empty states for tabs
  - [ ] Navigation to edit
  - [ ] Responsive design
- **Acceptance Criteria:**
  - Page renders
  - All tabs functional
  - Data displays correctly
  - Can navigate to edit
  - Mobile responsive

**Blocked By:** Design-003, Feature-009
**Blocks:** Feature-012

---

### Feature-012: Company Relationship Management
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** frontend, full-stack, relationships, demo-critical
- **Estimate:** 3 days
- **Start Date:** 2025-12-03
- **Target Date:** 2025-12-05
- **Dependencies:** Design-003, Feature-009, Feature-011
- **Description:** Build forms to add/edit all relationship types
- **Pages:**
  - `/companies/[id]/relationships/bank/new`
  - `/companies/[id]/relationships/bank/[rel_id]/edit`
  - (Same for tax, insurance, loans, employees)
- **Forms:**
  - Bank relationship form (all fields from Feature-002)
  - Tax entity form (all fields from Feature-003)
  - Insurance form (all fields from Feature-004)
  - Loan form (all fields from Feature-005)
  - Employee form (all fields from Feature-006)
- **Features:**
  - Form validation (Zod schemas)
  - Encrypted field handling
  - File upload (insurance certificates)
  - Auto-save drafts
  - Success/error notifications
  - Cancel/back navigation
- **Components:**
  - BankRelationshipForm
  - TaxEntityForm
  - InsuranceForm
  - LoanForm
  - EmployeeForm
  - RelationshipFormLayout
  - FormField components
- **Deliverables:**
  - [ ] All form components
  - [ ] Validation working
  - [ ] Can create relationships
  - [ ] Can edit relationships
  - [ ] File uploads working
  - [ ] Success/error handling
  - [ ] Responsive design
- **Acceptance Criteria:**
  - All forms functional
  - Validation working
  - CRUD operations work
  - File uploads work
  - Mobile responsive

**Blocked By:** Design-003, Feature-009, Feature-011
**Blocks:** None

---

### Feature-013: Tasks Page
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** frontend, tasks, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-12-04
- **Target Date:** 2025-12-05
- **Dependencies:** Design-003, Feature-009, Feature-017
- **Description:** Build page to view and manage tasks
- **Page:** `/tasks`
- **Features:**
  - Task list grouped by company
  - Filter by:
    - Status (Not Started, In Progress, Completed)
    - Company
    - Due date range
    - Assigned to
  - Sort by due date, priority, company
  - Mark tasks complete (checkbox)
  - Task detail modal
  - View task instructions
  - Add notes to tasks
- **Components:**
  - TasksList
  - TaskCard
  - TaskFilters
  - TaskDetailModal
  - TaskNotesEditor
  - CompletionCheckbox
- **Deliverables:**
  - [ ] Page component
  - [ ] Task list rendering
  - [ ] Filters working
  - [ ] Can mark complete
  - [ ] Detail modal
  - [ ] Notes functionality
  - [ ] Loading/empty states
  - [ ] Responsive design
- **Acceptance Criteria:**
  - Page renders
  - Tasks load from API
  - Filters work
  - Can complete tasks
  - Detail view works
  - Mobile responsive

**Blocked By:** Design-003, Feature-009, Feature-017
**Blocks:** None

---

### Feature-014: Review Periods Page
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** frontend, reviews, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-12-04
- **Target Date:** 2025-12-05
- **Dependencies:** Design-003, Feature-009
- **Description:** Build page to track monthly close progress
- **Page:** `/review-periods`
- **Features:**
  - List of review periods by company
  - Filter by company, status, period
  - Progress indicators (% tasks complete)
  - Status badges
  - Task completion checklist
  - Update status (Controller Review → Executive Review → Closed)
  - Add blockers/notes
  - Expand/collapse details
- **Components:**
  - ReviewPeriodsList
  - ReviewPeriodCard
  - ProgressBar
  - StatusBadge
  - TaskChecklist
  - StatusUpdateButton
  - BlockersEditor
- **Deliverables:**
  - [ ] Page component
  - [ ] List rendering
  - [ ] Progress calculation
  - [ ] Status updates
  - [ ] Blockers/notes
  - [ ] Loading/empty states
  - [ ] Responsive design
- **Acceptance Criteria:**
  - Page renders
  - Progress shown correctly
  - Can update status
  - Blockers saveable
  - Mobile responsive

**Blocked By:** Design-003, Feature-009
**Blocks:** None

---

### Feature-015: Projects Page
- **Type:** Feature
- **Priority:** 🟠 High
- **Labels:** frontend, projects
- **Estimate:** 2 days
- **Start Date:** 2025-12-06
- **Target Date:** 2025-12-07
- **Dependencies:** Design-003, Feature-009
- **Description:** Build page to manage accounting projects
- **Page:** `/projects`
- **Features:**
  - Project list
  - Filter by company, status, assignee
  - Create project form
  - Edit project
  - Project detail view
  - Add/complete milestones
  - Add/complete tasks
  - Project status updates
- **Components:**
  - ProjectsList
  - ProjectCard
  - CreateProjectModal
  - ProjectDetailView
  - MilestonesList
  - ProjectTasksList
- **Deliverables:**
  - [ ] Page component
  - [ ] List rendering
  - [ ] Create form
  - [ ] Detail view
  - [ ] Milestones/tasks
  - [ ] Status updates
  - [ ] Responsive design
- **Acceptance Criteria:**
  - Page renders
  - Can create projects
  - Can view/edit
  - Milestones/tasks work
  - Mobile responsive

**Blocked By:** Design-003, Feature-009
**Blocks:** None

---

### Feature-016: Dashboard Page
- **Type:** Feature
- **Priority:** 🔴 Urgent
- **Labels:** frontend, full-stack, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-12-06
- **Target Date:** 2025-12-07
- **Dependencies:** Design-003, Feature-009
- **Description:** Build leadership dashboard with KPIs and charts
- **Page:** `/dashboard` (home page)
- **Widgets:**
  - Active companies count
  - Open tasks by company (bar chart)
  - Review periods status (kanban board or status grid)
  - Projects in progress (list)
  - Upcoming deadlines (calendar/list)
  - Alerts/warnings (overdue tasks, expiring insurance, etc.)
  - Quick actions (add company, add task, etc.)
- **Charts:**
  - Tasks by status (pie chart)
  - Review periods by status (bar chart)
  - Tasks over time (line chart)
- **Components:**
  - DashboardLayout
  - KPICard
  - TasksChart
  - ReviewPeriodsGrid
  - ProjectsList
  - UpcomingDeadlines
  - AlertsPanel
  - QuickActions
- **Deliverables:**
  - [ ] Dashboard page
  - [ ] All KPI widgets
  - [ ] Charts with real data
  - [ ] Real-time updates
  - [ ] Loading states
  - [ ] Responsive design
- **Acceptance Criteria:**
  - Dashboard renders
  - All widgets functional
  - Charts accurate
  - Real data displayed
  - Mobile responsive

**Blocked By:** Design-003, Feature-009
**Blocks:** None

---

## Milestone 1.4: Integration, Testing & Polish

**Dates:** 2025-12-08 to 2025-12-13 (Week 4)
**Goal:** Everything polished and demo-ready

### Test-001: End-to-End Testing
- **Type:** Test
- **Priority:** 🔴 Urgent
- **Labels:** full-stack, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-12-08
- **Target Date:** 2025-12-09
- **Dependencies:** Feature-010, Feature-011, Feature-012, Feature-013, Feature-014, Feature-015, Feature-016
- **Description:** Test complete user workflows end-to-end
- **Test Scenarios:**
  1. **Company Setup Flow:**
     - Create new company
     - Add bank relationship
     - Add tax entity
     - Add insurance policy
     - Add loan
     - Add key employee
     - View company detail page
     - Verify dashboard updates
  2. **Task Automation Flow:**
     - Create Task Type with monthly recurrence
     - Wait for scheduler (or trigger manually)
     - Verify task created
     - Assign to user
     - Mark complete
     - Verify review period updates
  3. **Monthly Close Flow:**
     - View review period
     - Complete tasks
     - Update status to Controller Review
     - Add blockers
     - Update status to Executive Review
     - Close period
     - Verify dashboard reflects closed period
  4. **Project Management Flow:**
     - Create project
     - Add milestones
     - Add tasks
     - Update status
     - Complete project
- **Deliverables:**
  - [ ] Test plan document
  - [ ] Automated E2E tests (Playwright)
  - [ ] Manual test checklist
  - [ ] Bug tracking sheet
  - [ ] All critical bugs fixed
- **Acceptance Criteria:**
  - All workflows tested
  - No critical bugs
  - Data integrity maintained
  - Tests documented

**Blocked By:** Feature-010, Feature-011, Feature-012, Feature-013, Feature-014, Feature-015, Feature-016
**Blocks:** Docs-001

---

### Bug-001: Bug Fixes & Polish
- **Type:** Bug
- **Priority:** 🔴 Urgent
- **Labels:** full-stack, demo-critical
- **Estimate:** 2 days
- **Start Date:** 2025-12-10
- **Target Date:** 2025-12-11
- **Dependencies:** Test-001
- **Description:** Fix all bugs found during E2E testing
- **Categories:**
  - UI/UX issues
  - Data validation errors
  - API errors
  - Permission issues
  - Performance problems
  - Mobile responsiveness
  - Browser compatibility
- **Deliverables:**
  - [ ] All critical bugs fixed
  - [ ] All high priority bugs fixed
  - [ ] Medium bugs triaged (fix or defer)
  - [ ] UI polished
  - [ ] Performance optimized
  - [ ] Cross-browser tested
- **Acceptance Criteria:**
  - Zero critical bugs
  - Zero high priority bugs
  - UX smooth
  - Performance acceptable (<2s page loads)

**Blocked By:** Test-001
**Blocks:** Docs-001

---

### Deploy-001: Demo Data Seeding
- **Type:** Deploy
- **Priority:** 🔴 Urgent
- **Labels:** backend, demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-12-11
- **Target Date:** 2025-12-11
- **Dependencies:** Test-001, Bug-001
- **Description:** Create realistic demo data for presentation
- **Demo Data:**
  - **3-5 Companies:**
    - "Acme Hospitality Group" (parent company)
    - "Grand Hotel Downtown" (subsidiary)
    - "Riverside Restaurant" (subsidiary)
    - "Lakeview Catering" (subsidiary)
    - "Sunset Bar & Grill" (subsidiary)
  - **Relationships for each:**
    - 2-3 bank accounts
    - 3-5 tax entities (federal, state, local, sales tax, payroll tax)
    - 3-5 insurance policies (various types, some expiring soon)
    - 1-2 loans with realistic terms
    - 2-5 key employees
  - **Task Types:**
    - Daily: Cash reconciliation
    - Weekly: Payroll processing
    - Monthly: Bank reconciliation, Financial close, Sales tax filing
    - Quarterly: Estimated tax payments, Board reporting
    - Annual: Tax preparation, Insurance renewals
  - **Review Periods:**
    - November 2025 (In Progress - 80% tasks complete)
    - October 2025 (Executive Review - 100% tasks complete, awaiting approval)
    - September 2025 (Closed)
  - **Projects:**
    - "Q4 2025 Tax Planning" (In Progress)
    - "Annual Audit Preparation" (Planned)
    - "Insurance Policy Review" (Completed)
  - **Active Tasks:**
    - 20-30 tasks across companies in various states
    - Some overdue (to show alerts)
    - Some due soon
- **Deliverables:**
  - [ ] Demo data script
  - [ ] Data realistic and cohesive
  - [ ] Supports demo storyline
  - [ ] Can be run repeatably
  - [ ] Cleanup script to reset
- **Acceptance Criteria:**
  - Data realistic
  - Demo flows work
  - No data errors
  - Easy to reset/reload

**Blocked By:** Test-001, Bug-001
**Blocks:** Docs-001

---

### Docs-001: Demo Preparation & Rehearsal
- **Type:** Docs
- **Priority:** 🔴 Urgent
- **Labels:** demo-critical
- **Estimate:** 1 day
- **Start Date:** 2025-12-12
- **Target Date:** 2025-12-12
- **Dependencies:** Test-001, Bug-001, Deploy-001
- **Description:** Prepare for leadership demo
- **Tasks:**
  - Finalize demo script
  - Practice walkthrough (3-5 times)
  - Prepare talking points
  - Create presentation slides (optional)
  - Prepare Q&A responses
  - Setup demo environment
  - Test demo on different devices
  - Backup plan if tech fails
- **Deliverables:**
  - [ ] Finalized demo script
  - [ ] Talking points document
  - [ ] Slides (if needed)
  - [ ] Q&A prep sheet
  - [ ] Demo environment ready
  - [ ] Backup plan documented
  - [ ] Team briefed
- **Acceptance Criteria:**
  - Demo script polished
  - Walkthrough smooth (10-15 min)
  - Talking points clear
  - Q&A prepared
  - Confidence high

**Blocked By:** Test-001, Bug-001, Deploy-001
**Blocks:** None

---

## Milestone 1.5: Demo Day

**Dates:** 2025-12-14 to 2025-12-16
**Goal:** Present to leadership and get approval

### Event: Leadership Demo
- **Date:** 2025-12-14 (or best date that week)
- **Duration:** 30-60 minutes (10-15 min demo, 15-45 min discussion)
- **Attendees:**
  - Company leadership
  - Accounting team leads
  - Decision makers
- **Agenda:**
  1. Introduction (2 min) - Context and goals
  2. Demo walkthrough (10-15 min) - Show key features
  3. Q&A (15-30 min) - Answer questions
  4. Next steps discussion (5-10 min) - Get approval or feedback

### Success Criteria
- [ ] Demo completed successfully
- [ ] Leadership impressed
- [ ] No major technical issues
- [ ] Questions answered satisfactorily
- [ ] **Decision:** Approve to continue building full platform OR provide feedback for adjustments

---

# PHASE 2: OPERATIONS MODULES

**Timeline:** 2026-01-01 to 2026-06-30 (6 months)
**Status:** PLANNED (Conditional on Phase 1 approval)
**Goal:** Build property-level operations features

---

## PROJECT 2: Inventory Management

**Status:** Placeholder
**Timeline:** 3 months
**Dependencies:** Phase 1 approval

### Milestones (Placeholder)
- 2.1: Product Catalog (4 weeks)
- 2.2: Inventory Tracking (4 weeks)
- 2.3: Audits & Counting (4 weeks)

### Sample Issues (Placeholders)
- Feature-101: Product Master DocType
- Feature-102: Inventory Balance Tracking
- Feature-103: Audit Workflow System
- Feature-104: Batch/Lot Tracking
- Feature-105: Storage Area Management

---

## PROJECT 3: Procurement

**Status:** Placeholder
**Timeline:** 2 months
**Dependencies:** Project 2 (Inventory)

### Milestones (Placeholder)
- 3.1: Vendor Management (3 weeks)
- 3.2: Purchase Orders (3 weeks)
- 3.3: Receiving & Invoicing (2 weeks)

### Sample Issues (Placeholders)
- Feature-201: Vendor Master DocType
- Feature-202: Purchase Order System
- Feature-203: Receiving Workflow
- Feature-204: Invoice Matching
- Feature-205: Ottimate Integration

---

## PROJECT 4: Recipe Costing

**Status:** Placeholder
**Timeline:** 2 months
**Dependencies:** Project 2 (Inventory)

### Milestones (Placeholder)
- 4.1: Recipe Management (3 weeks)
- 4.2: Batch Production (2 weeks)
- 4.3: Costing & Pricing (3 weeks)

### Sample Issues (Placeholders)
- Feature-301: Recipe Master DocType
- Feature-302: Recipe Ingredients System
- Feature-303: Batch Management
- Feature-304: Cost Calculation Engine
- Feature-305: Menu Pricing

---

## PROJECT 5: POS Integration

**Status:** Placeholder
**Timeline:** 2 months
**Dependencies:** Project 2 (Inventory), Project 4 (Recipes)

### Milestones (Placeholder)
- 5.1: POS Configuration (2 weeks)
- 5.2: Sales Import (3 weeks)
- 5.3: Depletion Calculation (3 weeks)

### Sample Issues (Placeholders)
- Integration-401: POS System Connector
- Feature-402: Sales Journal Import
- Feature-403: Automatic Depletion
- Feature-404: Variance Analysis
- Integration-405: Multiple POS Support

---

# PHASE 3: PLATFORM ENHANCEMENT

**Timeline:** 2026-07-01 to 2026-12-31 (6 months)
**Status:** PLANNED
**Goal:** Advanced features and multi-location

---

## PROJECT 6: Multi-Location (Director)

**Status:** Placeholder
**Timeline:** 3 months

### Milestones (Placeholder)
- 6.1: Corporate Master Data (4 weeks)
- 6.2: Store Synchronization (4 weeks)
- 6.3: Consolidated Reporting (4 weeks)

### Sample Issues (Placeholders)
- Feature-501: Corporate Product Catalog
- Feature-502: Store Sync Engine
- Feature-503: Multi-Location Dashboard
- Feature-504: Consolidated Reports

---

## PROJECT 7: Analytics & Reporting

**Status:** Placeholder
**Timeline:** 2 months

### Milestones (Placeholder)
- 7.1: Report Framework (3 weeks)
- 7.2: Standard Reports (3 weeks)
- 7.3: Custom Dashboards (2 weeks)

### Sample Issues (Placeholders)
- Feature-601: Report Builder
- Feature-602: Financial Reports
- Feature-603: Operational Reports
- Feature-604: Executive Dashboard

---

## PROJECT 8: Budgeting

**Status:** Placeholder
**Timeline:** 2 months

### Milestones (Placeholder)
- 8.1: Budget Setup (3 weeks)
- 8.2: Budget Tracking (3 weeks)
- 8.3: Variance Analysis (2 weeks)

### Sample Issues (Placeholders)
- Feature-701: Budget Master
- Feature-702: Budget vs Actual
- Feature-703: Forecasting

---

# PHASE 4: SCALE & OPTIMIZE

**Timeline:** 2027-01-01 onwards
**Status:** FUTURE
**Goal:** Production readiness and scaling

---

## PROJECT 9: Platform Optimization

**Status:** Placeholder
**Timeline:** Ongoing

### Focus Areas
- Performance optimization
- Scalability improvements
- Security hardening
- Mobile apps (React Native)
- Advanced integrations
- AI/ML features

### Sample Issues (Placeholders)
- Enhancement-801: Query Optimization
- Enhancement-802: Caching Strategy
- Enhancement-803: Mobile App (iOS)
- Enhancement-804: Mobile App (Android)
- Integration-805: QuickBooks Online
- Integration-806: NetSuite
- Feature-807: AI Invoice OCR
- Feature-808: Demand Forecasting

---

# DEPENDENCY VISUALIZATION

## Phase 1: Company Management MVP

```
Design-001 (Data Model)
├─> Feature-001 (Company DocType)
│   ├─> Feature-002 (Bank)
│   ├─> Feature-003 (Tax)
│   ├─> Feature-004 (Insurance)
│   ├─> Feature-005 (Loan)
│   └─> Feature-006 (Employee)
├─> Feature-007 (Task Type)
│   ├─> Feature-008 (Review Period)
│   └─> Feature-017 (Automation)
│       └─> Feature-013 (Tasks Page)
└─> Design-002 (API Design)
    └─> Feature-009 (APIs)
        ├─> Feature-010 (Directory Page)
        ├─> Feature-011 (Detail Page)
        │   └─> Feature-012 (Relationship Forms)
        ├─> Feature-013 (Tasks Page)
        ├─> Feature-014 (Review Periods Page)
        ├─> Feature-015 (Projects Page)
        └─> Feature-016 (Dashboard)

Design-003 (Frontend)
└─> All Frontend Features (010-016)

All Features
└─> Test-001 (E2E Testing)
    ├─> Bug-001 (Bug Fixes)
    └─> Deploy-001 (Demo Data)
        └─> Docs-001 (Demo Prep)
```

## Phase Dependencies

```
Phase 1 (Company Management MVP)
└─> Phase 2 (Operations Modules)
    ├─> Project 2 (Inventory)
    │   ├─> Project 3 (Procurement)
    │   └─> Project 4 (Recipe Costing)
    │       └─> Project 5 (POS Integration)
    └─> Phase 3 (Platform Enhancement)
        ├─> Project 6 (Multi-Location)
        ├─> Project 7 (Analytics)
        └─> Project 8 (Budgeting)
            └─> Phase 4 (Scale & Optimize)
                └─> Project 9 (Optimization)
```

---

# SUMMARY

## Total Roadmap

- **Phase 1:** 1 month (4 weeks) - 30 issues - ACTIVE NOW
- **Phase 2:** 6 months - ~100 issues - Starts after MVP approval
- **Phase 3:** 6 months - ~80 issues - Advanced features
- **Phase 4:** Ongoing - Production and scale

## Immediate Focus (Next 4 Weeks)

1. **Week 1:** Planning & Design (4 design issues)
2. **Week 2:** Backend Foundation (9 feature issues)
3. **Week 3:** Automation & Frontend (8 feature issues)
4. **Week 4:** Testing & Polish (4 test/bug/deploy issues)
5. **Demo:** Dec 14-16

## Critical Path

```
Design-001 → Feature-001 → Features 002-006 → Feature-009 → Frontend Features → Testing → Demo
```

The critical path determines the minimum timeline. Any delays in these issues delay the demo.

---

**Next Steps:**
1. Create these issues in Linear with exact specifications
2. Set up dependency chains
3. Assign start/target dates
4. Add all labels
5. Begin with Design-001 immediately

This roadmap ensures nothing is forgotten and provides a clear path from MVP to final product!
