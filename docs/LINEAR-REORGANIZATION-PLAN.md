# Linear Reorganization Plan

**Date:** 2025-11-16
**Purpose:** Restructure Linear to focus on Company Management MVP
**Timeline:** 1 month to demo
**Status:** Proposed - Awaiting Approval

---

## Current Linear State (Problems)

Based on our conversation and the previous Linear updates:

**Existing Projects:**
1. ✅ Phase 1 - MVP Frontend (COMPLETED) - **WRONG SCOPE** (Products/Inventory)
2. ✅ Phase 1 - Backend APIs (COMPLETED) - Mixed scope
3. 📋 Phase 2 - Full Platform Rewrite (PLANNED) - Future work, conditional
4. 🔄 Operations (blkshp_ops) - In Progress - **Not current priority**
5. 🔄 Finance (blkshp_finance) - Planned - Partially relevant
6. 🔄 Core Platform - In Progress - Relevant (Departments, Permissions done)
7. 🔄 Frontend Application (Full Platform) - Planned - Future work

**Problems:**
- Too many projects, unclear focus
- Completed MVP was wrong scope (Products/Inventory, not Company Management)
- Operations modules are future work, not current priority
- No clear project for the actual 1-month Company Management MVP

**Existing Issues:**
- BLK-60 to BLK-72: Products/Inventory MVP (completed but wrong scope)
- BLK-41 to BLK-49: Inventory operations (future work)
- BLK-37, BLK-55, BLK-36: Backend cleanup (completed)
- Various other issues scattered across projects

---

## Proposed New Linear Structure

### Clean Slate Approach

**Archive everything and start fresh with:**

1. **One focused team:** BLKSHP Engineering
2. **One active project:** Company Management MVP
3. **One clear timeline:** 1 month to demo
4. **Clear milestones:** Weekly sprints
5. **Clear issues:** Specific to Company Management features

---

## Proposed Projects

### PROJECT 1: Company Management MVP (ACTIVE)

**Status:** In Progress
**Timeline:** 2025-11-16 to 2025-12-16 (1 month)
**Priority:** Urgent
**Goal:** Working demo for management company leadership

**Description:**
Multi-entity company management platform for hospitality management companies.
Enables leadership and accounting teams to manage companies, track relationships,
automate tasks, and monitor financial close progress.

**Target Users:**
- Management Company Leadership
- Accounting and Finance Teams

**Core Features:**
1. Company/Entity Directory & Details
2. Company Relationships (Banks, Tax Entities, Insurance, Loans, Key Employees)
3. Automated Task Management (daily/weekly/monthly/quarterly/annual)
4. Review Period Tracking (month-end close)
5. Project Tracking
6. Accounting Dashboard

**Success Criteria:**
- [ ] Leadership can log in and view their companies
- [ ] Can add and manage company relationships
- [ ] Task automation working (auto-create recurring tasks)
- [ ] Can track monthly close progress
- [ ] Dashboard shows KPIs and status
- [ ] Demo-ready in 1 month

**Tech Stack:**
- Backend: Frappe Framework + MariaDB
- Frontend: Next.js 14 + TypeScript + Tailwind
- Auth: JWT via Frappe
- Deployment: Frappe backend + Vercel frontend

---

### PROJECT 2: Core Platform (ONGOING)

**Status:** Active (Background)
**Priority:** High
**Goal:** Maintain core infrastructure

**Description:**
Core platform capabilities that support all features: authentication, permissions,
departments, subscriptions, and module activation.

**Scope:**
- ✅ Departments (Complete)
- ✅ Permissions (Complete)
- ✅ Authentication (Complete)
- ✅ Subscription Plans (Complete)
- 🔄 Company Groups (In Progress - needed for MVP)
- 🔄 Intercompany Accounting (In Progress - needed for MVP)

**Issues:** Maintenance and support issues only

---

### ARCHIVED PROJECTS

Move these to "Archived" or "Paused" status:

1. **Phase 1 - MVP Frontend** → ARCHIVE
   - Reason: Wrong scope (Products/Inventory)
   - Status: Complete but not useful for current demo

2. **Phase 2 - Full Platform Rewrite** → ARCHIVE
   - Reason: Future work, conditional on company approval
   - Status: Planned, not current

3. **Operations (blkshp_ops)** → PAUSE
   - Reason: Inventory/operations not needed for 1-month demo
   - Status: Can resume after Company Management MVP

4. **Finance (blkshp_finance)** → MERGE into Company Management MVP
   - Keep intercompany accounting work
   - Archive other finance features for later

5. **Frontend Application (Full Platform)** → ARCHIVE
   - Reason: Future work
   - Status: Superseded by Company Management MVP

---

## Proposed Milestones

### MILESTONE 1: Planning & Design (Week 1)
**Dates:** 2025-11-16 to 2025-11-22
**Goal:** Complete planning and design

**Issues:**
- Define complete data model (DocTypes)
- Design API endpoints
- Design frontend pages
- Create demo walkthrough script

---

### MILESTONE 2: Backend Foundation (Week 2)
**Dates:** 2025-11-23 to 2025-11-29
**Goal:** Core DocTypes and APIs working

**Issues:**
- Company Master DocType
- Company Relationships DocTypes (Banks, Tax, Insurance, Loans, Employees)
- Task Type DocType
- Review Period DocType
- Project DocType
- Core API endpoints

---

### MILESTONE 3: Task Automation & Frontend (Week 3)
**Dates:** 2025-11-30 to 2025-12-06
**Goal:** Task automation working, frontend pages built

**Issues:**
- Task automation scheduler
- Next.js pages (Company Directory, Relationships, Tasks, Projects)
- Dashboard with KPIs
- Navigation and layout

---

### MILESTONE 4: Integration & Polish (Week 4)
**Dates:** 2025-12-07 to 2025-12-13
**Goal:** Everything integrated, bug fixes, demo prep

**Issues:**
- End-to-end testing
- Bug fixes
- Demo data seeding
- Demo rehearsal
- Final polish

---

### MILESTONE 5: Demo Day (Week 4 end)
**Date:** 2025-12-14 to 2025-12-16
**Goal:** Present to leadership

**Issues:**
- Demo preparation
- Demo delivery
- Gather feedback
- Document next steps

---

## Proposed Labels

**Priority Labels:**
- `urgent` - Must have for demo
- `high` - Important for demo
- `medium` - Nice to have
- `low` - Future enhancement

**Type Labels:**
- `backend` - Backend/API work
- `frontend` - Next.js frontend
- `design` - Planning/design work
- `bug` - Bug fix
- `docs` - Documentation

**Domain Labels:**
- `company-management` - Company/entity features
- `relationships` - Company relationships
- `tasks` - Task automation
- `reviews` - Review periods
- `projects` - Project tracking
- `dashboard` - Dashboard/reporting
- `auth` - Authentication
- `permissions` - Permissions

**Status Labels:**
- `blocked` - Blocked by dependency
- `in-review` - In code review
- `ready-to-test` - Ready for testing
- `demo-critical` - Critical for demo

---

## Sample Issues for Company Management MVP

### Epic: Company Management MVP

#### Planning & Design (Milestone 1)

**BLK-100: Define Company Management Data Model**
- Priority: Urgent
- Labels: design, backend, company-management
- Description: Design complete DocType schema for Company, Relationships, Tasks, Reviews, Projects
- Estimate: 1 day
- Acceptance Criteria:
  - [ ] Company DocType defined with all fields
  - [ ] All relationship DocTypes defined
  - [ ] Task Type and Review Period DocTypes defined
  - [ ] Project DocType defined
  - [ ] Relationships documented

**BLK-101: Design Company Management API Endpoints**
- Priority: Urgent
- Labels: design, backend
- Description: Design REST API endpoints for Company Management features
- Estimate: 1 day
- Acceptance Criteria:
  - [ ] Company CRUD endpoints designed
  - [ ] Relationships CRUD endpoints designed
  - [ ] Task automation endpoints designed
  - [ ] Review Period endpoints designed
  - [ ] Project endpoints designed
  - [ ] Dashboard KPI endpoints designed

**BLK-102: Design Next.js Frontend Structure**
- Priority: Urgent
- Labels: design, frontend
- Description: Design page structure, navigation, and components
- Estimate: 1 day
- Acceptance Criteria:
  - [ ] Page structure defined
  - [ ] Component hierarchy designed
  - [ ] Navigation flow mapped
  - [ ] Data flow documented

**BLK-103: Create Demo Walkthrough Script**
- Priority: High
- Labels: design, demo-critical
- Description: Write complete demo script for leadership presentation
- Estimate: 0.5 day
- Acceptance Criteria:
  - [ ] Demo storyline defined
  - [ ] Key talking points listed
  - [ ] Demo flow documented
  - [ ] Success metrics identified

---

#### Backend Foundation (Milestone 2)

**BLK-110: Enhance Company Master DocType**
- Priority: Urgent
- Labels: backend, company-management, demo-critical
- Description: Expand Company DocType with all required fields
- Estimate: 1 day
- Fields to add:
  - Legal name, DBA name
  - EIN/Tax ID
  - Address (billing, physical)
  - Phone, email, website
  - Status (active, inactive)
  - Formation date
  - Entity type
  - Ownership structure
- Acceptance Criteria:
  - [ ] All fields added
  - [ ] Validation working
  - [ ] Can create/edit companies via Frappe Desk
  - [ ] Tests passing

**BLK-111: Bank Relationship DocType**
- Priority: Urgent
- Labels: backend, relationships, demo-critical
- Description: Create DocType to track company banking relationships
- Estimate: 0.5 day
- Fields:
  - Company (link)
  - Bank name
  - Account type (checking, savings, loan, credit)
  - Account number (encrypted)
  - Routing number
  - Account status
  - Primary contact
  - Notes
- Acceptance Criteria:
  - [ ] DocType created
  - [ ] Linked to Company
  - [ ] Encryption working for sensitive fields
  - [ ] Can CRUD via Frappe Desk

**BLK-112: Tax Entity Relationship DocType**
- Priority: Urgent
- Labels: backend, relationships, demo-critical
- Estimate: 0.5 day
- Fields:
  - Company (link)
  - Tax entity type (Federal, State, Local)
  - Tax ID
  - Jurisdiction
  - Filing frequency
  - Due dates
  - Responsible party
  - Notes

**BLK-113: Insurance Relationship DocType**
- Priority: Urgent
- Labels: backend, relationships, demo-critical
- Estimate: 0.5 day
- Fields:
  - Company (link)
  - Insurance type (General Liability, Property, Workers Comp, etc.)
  - Provider name
  - Policy number
  - Coverage amount
  - Premium
  - Effective date
  - Expiration date
  - Renewal date
  - Agent contact
  - Status

**BLK-114: Loan Relationship DocType**
- Priority: Urgent
- Labels: backend, relationships, demo-critical
- Estimate: 0.5 day
- Fields:
  - Company (link)
  - Lender name
  - Loan type (Term, Line of Credit, Mortgage, SBA, etc.)
  - Loan amount
  - Interest rate
  - Term length
  - Monthly payment
  - Origination date
  - Maturity date
  - Account number
  - Loan status
  - Collateral
  - Guarantors

**BLK-115: Key Employee Relationship DocType**
- Priority: Urgent
- Labels: backend, relationships, demo-critical
- Estimate: 0.5 day
- Fields:
  - Company (link)
  - Employee name
  - Role/Title
  - Email
  - Phone
  - Start date
  - Status (active, inactive)
  - Responsibilities
  - Notes

**BLK-116: Task Type DocType**
- Priority: Urgent
- Labels: backend, tasks, demo-critical
- Description: Create master DocType for task templates
- Estimate: 1 day
- Fields:
  - Task name
  - Description
  - Recurrence (Daily, Weekly, Bi-weekly, Monthly, Quarterly, Annual)
  - Day of week (for weekly)
  - Day of month (for monthly)
  - Month (for quarterly/annual)
  - Dependencies (other task types)
  - Assigned role
  - Estimated time
  - Instructions
- Acceptance Criteria:
  - [ ] DocType created
  - [ ] Recurrence patterns working
  - [ ] Dependencies can be set
  - [ ] Can create task templates

**BLK-117: Review Period DocType**
- Priority: Urgent
- Labels: backend, reviews, demo-critical
- Description: Create DocType to track month-end close periods
- Estimate: 1 day
- Fields:
  - Company (link)
  - Period (Month YYYY)
  - Start date
  - Target close date
  - Actual close date
  - Status (Open, In Progress, Controller Review, Executive Review, Closed)
  - Assigned controller
  - Assigned executive
  - Tasks (child table - links to Task instances)
  - Issues/blockers
  - Notes
- Acceptance Criteria:
  - [ ] DocType created
  - [ ] Status workflow working
  - [ ] Linked to tasks
  - [ ] Can track progress

**BLK-118: Project DocType**
- Priority: High
- Labels: backend, projects
- Description: Create DocType for tracking accounting projects
- Estimate: 1 day
- Fields:
  - Company (link)
  - Project name
  - Description
  - Project type (Audit, Reconciliation, Analysis, Implementation, etc.)
  - Status (Planned, In Progress, On Hold, Completed, Cancelled)
  - Priority
  - Start date
  - Due date
  - Completion date
  - Assigned to (user)
  - Tasks (child table)
  - Milestones
  - Notes
- Acceptance Criteria:
  - [ ] DocType created
  - [ ] Status workflow working
  - [ ] Can create and track projects

**BLK-119: Company Management API Endpoints**
- Priority: Urgent
- Labels: backend, demo-critical
- Description: Create REST API endpoints for Company Management
- Estimate: 2 days
- Endpoints:
  - `get_company_details` - Get company with all relationships
  - `list_companies` - List companies with filters
  - `get_company_relationships` - Get all relationships for a company
  - `get_company_tasks` - Get active tasks for company
  - `get_company_review_periods` - Get review periods for company
  - `get_company_projects` - Get projects for company
  - `get_dashboard_kpis` - Get KPIs for dashboard
- Acceptance Criteria:
  - [ ] All endpoints implemented
  - [ ] Permission checks working
  - [ ] Tests passing
  - [ ] API documentation updated

---

#### Task Automation & Frontend (Milestone 3)

**BLK-120: Task Automation Scheduler**
- Priority: Urgent
- Labels: backend, tasks, demo-critical
- Description: Build scheduler to auto-create recurring tasks
- Estimate: 2 days
- Features:
  - Daily scheduler (runs at 12:01 AM)
  - Reads Task Type masters
  - Creates Task instances based on recurrence
  - Assigns to correct users/roles
  - Links to Review Periods (for monthly tasks)
  - Handles dependencies
- Acceptance Criteria:
  - [ ] Scheduler working
  - [ ] Tasks auto-created correctly
  - [ ] Recurrence patterns working
  - [ ] Dependencies enforced
  - [ ] Tests passing

**BLK-121: Company Directory Page**
- Priority: Urgent
- Labels: frontend, company-management, demo-critical
- Description: Build Next.js page to list and search companies
- Estimate: 1 day
- Features:
  - Table of companies
  - Search by name
  - Filter by status
  - Click to view details
- Acceptance Criteria:
  - [ ] Page renders
  - [ ] Data loads from API
  - [ ] Search working
  - [ ] Navigation working

**BLK-122: Company Detail Page**
- Priority: Urgent
- Labels: frontend, company-management, demo-critical
- Description: Build page showing company details and relationships
- Estimate: 2 days
- Features:
  - Company information section
  - Relationships tabs (Banks, Tax, Insurance, Loans, Employees)
  - Edit buttons
  - Add relationship buttons
- Acceptance Criteria:
  - [ ] Page renders
  - [ ] All relationships display
  - [ ] Can navigate to edit
  - [ ] Loading states working

**BLK-123: Company Relationships Management**
- Priority: Urgent
- Labels: frontend, relationships, demo-critical
- Description: Build forms to add/edit company relationships
- Estimate: 2 days
- Features:
  - Bank relationship form
  - Tax entity form
  - Insurance form
  - Loan form
  - Employee form
  - Validation
- Acceptance Criteria:
  - [ ] All forms working
  - [ ] Can create relationships
  - [ ] Can edit relationships
  - [ ] Validation working

**BLK-124: Tasks Page**
- Priority: Urgent
- Labels: frontend, tasks, demo-critical
- Description: Build page to view and manage tasks
- Estimate: 1.5 days
- Features:
  - Task list (grouped by company)
  - Filter by status, company, due date
  - Mark tasks complete
  - Task detail view
- Acceptance Criteria:
  - [ ] Page renders
  - [ ] Tasks load
  - [ ] Can complete tasks
  - [ ] Filters working

**BLK-125: Review Periods Page**
- Priority: Urgent
- Labels: frontend, reviews, demo-critical
- Description: Build page to track monthly close progress
- Estimate: 1.5 days
- Features:
  - List of review periods by company
  - Progress indicators
  - Task completion status
  - Status updates (Controller Review → Executive Review → Closed)
- Acceptance Criteria:
  - [ ] Page renders
  - [ ] Progress shown correctly
  - [ ] Can update status
  - [ ] Shows blocking issues

**BLK-126: Projects Page**
- Priority: High
- Labels: frontend, projects
- Description: Build page to manage accounting projects
- Estimate: 1.5 days
- Features:
  - Project list
  - Filter by company, status
  - Project detail view
  - Create/edit project forms
- Acceptance Criteria:
  - [ ] Page renders
  - [ ] Can create projects
  - [ ] Can view/edit projects
  - [ ] Status updates working

**BLK-127: Dashboard Page**
- Priority: Urgent
- Labels: frontend, dashboard, demo-critical
- Description: Build leadership dashboard with KPIs
- Estimate: 2 days
- Features:
  - Active companies count
  - Open tasks by company
  - Review periods status (on track, behind, blocked)
  - Projects in progress
  - Upcoming deadlines
  - Charts/visualizations
- Acceptance Criteria:
  - [ ] Dashboard renders
  - [ ] KPIs accurate
  - [ ] Charts working
  - [ ] Real-time data

---

#### Integration & Polish (Milestone 4)

**BLK-130: End-to-End Testing**
- Priority: Urgent
- Labels: backend, frontend, demo-critical
- Description: Test complete user workflows
- Estimate: 2 days
- Test Cases:
  - Create company → Add relationships → View dashboard
  - Task auto-creation → Complete tasks → Close review period
  - Create project → Track progress → Complete
- Acceptance Criteria:
  - [ ] All workflows working
  - [ ] No critical bugs
  - [ ] Data integrity maintained

**BLK-131: Bug Fixes & Polish**
- Priority: High
- Labels: bug, demo-critical
- Description: Fix bugs found during testing
- Estimate: 2 days
- Acceptance Criteria:
  - [ ] All critical bugs fixed
  - [ ] No blocking issues
  - [ ] UX polished

**BLK-132: Demo Data Seeding**
- Priority: Urgent
- Labels: demo-critical
- Description: Create realistic demo data
- Estimate: 1 day
- Data:
  - 3-5 sample companies
  - Relationships for each
  - Review periods in various states
  - Active tasks
  - Sample projects
- Acceptance Criteria:
  - [ ] Demo data script working
  - [ ] Data realistic
  - [ ] Demo storyline supported

**BLK-133: Demo Rehearsal**
- Priority: Urgent
- Labels: demo-critical
- Description: Practice demo presentation
- Estimate: 0.5 day
- Acceptance Criteria:
  - [ ] Demo script finalized
  - [ ] Walkthrough smooth
  - [ ] Timing good (10-15 min)
  - [ ] Talking points clear

---

## Issue Naming Convention

**Format:** `BLK-XXX: [Component] Feature/Action Description`

**Examples:**
- `BLK-110: [Company] Enhance Company Master DocType`
- `BLK-119: [API] Company Management Endpoints`
- `BLK-121: [Frontend] Company Directory Page`
- `BLK-127: [Dashboard] Leadership Dashboard with KPIs`

**Component Tags:**
- `[Company]` - Company management
- `[Relationships]` - Company relationships
- `[Tasks]` - Task automation
- `[Reviews]` - Review periods
- `[Projects]` - Projects
- `[Dashboard]` - Dashboard
- `[API]` - Backend APIs
- `[Frontend]` - Frontend pages
- `[Auth]` - Authentication
- `[Permissions]` - Permissions

---

## Timeline Summary

| Week | Milestone | Issues | Focus |
|------|-----------|--------|-------|
| 1 (Nov 16-22) | Planning & Design | BLK-100 to BLK-103 | Design complete system |
| 2 (Nov 23-29) | Backend Foundation | BLK-110 to BLK-119 | Build DocTypes & APIs |
| 3 (Nov 30-Dec 6) | Automation & Frontend | BLK-120 to BLK-127 | Build scheduler & pages |
| 4 (Dec 7-13) | Integration & Polish | BLK-130 to BLK-133 | Test, fix, demo prep |
| 4 (Dec 14-16) | Demo Day | - | Present to leadership |

**Total:** ~30-35 issues over 4 weeks

---

## What to Do with Existing Issues

### Completed Issues (BLK-60 to BLK-72)
**Action:** Mark as "Archived" or "Completed (Archived)"
- Label: `archived`, `wrong-scope`
- Note: "Completed but not relevant for Company Management MVP"

### Inventory Issues (BLK-41 to BLK-49)
**Action:** Move to "Operations" project (Paused)
- Label: `future-work`, `operations`
- Status: Paused
- Note: "Deferred to post-MVP operations phase"

### Backend Cleanup Issues (BLK-37, BLK-55, BLK-36)
**Action:** Mark as Completed
- These are done and relevant

### Other Scattered Issues
**Action:** Review individually
- Keep if relevant to Company Management MVP
- Archive if operations/future work
- Complete if done

---

## Approval Questions

1. **Archive Strategy:** Approve archiving Phase 1 MVP Frontend and other outdated projects?
2. **Focus:** Approve single focused project "Company Management MVP"?
3. **Timeline:** Approve 1-month timeline (4 weekly milestones)?
4. **Issue Structure:** Approve proposed issue breakdown (BLK-100 to BLK-133)?
5. **Labels:** Approve proposed labeling system?
6. **Existing Issues:** Approve archiving Products/Inventory MVP issues?

---

## Next Steps After Approval

1. **Linear Cleanup:**
   - Archive outdated projects
   - Create "Company Management MVP" project
   - Create 5 milestones (Planning, Backend, Frontend, Polish, Demo)
   - Create labels

2. **Issue Creation:**
   - Create BLK-100 to BLK-103 (Planning & Design) immediately
   - Create BLK-110 to BLK-133 after planning complete

3. **Archive Old Issues:**
   - Mark BLK-60 to BLK-72 as archived
   - Move BLK-41 to BLK-49 to "Paused" status

4. **Begin Work:**
   - Start with BLK-100 (Define Data Model)
   - Daily standup to track progress
   - Weekly demo to show progress

---

**Status:** Awaiting approval to proceed
**Estimated Time to Execute:** 2-3 hours for Linear cleanup and issue creation
