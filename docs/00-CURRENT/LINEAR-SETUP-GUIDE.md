# Linear Setup Guide - Quick Actions

**Purpose:** Step-by-step guide to set up Linear based on the complete roadmap
**Time Required:** 2-3 hours
**Reference:** LINEAR-COMPLETE-ROADMAP.md

---

## STEP 1: Archive Old Projects (15 min)

### Projects to Archive

1. **Phase 1 - MVP Frontend**
   - Status: Mark as "Completed"
   - Archive: Yes
   - Note: "Completed but wrong scope (Products/Inventory)"

2. **Phase 2 - Full Platform Rewrite**
   - Status: Mark as "Canceled"
   - Archive: Yes
   - Note: "Future work - FastAPI rewrite conditional on MVP approval"

3. **Operations (blkshp_ops)**
   - Status: Mark as "Paused"
   - Note: "Inventory/operations work - deferred to Phase 2"

4. **Frontend Application (Full Platform)**
   - Status: Mark as "Canceled"
   - Archive: Yes
   - Note: "Superseded by Company Management MVP"

### How to Archive
1. Go to each project
2. Click "..." menu → "Edit Project"
3. Change status
4. Click "Archive" if applicable
5. Add note in description

---

## STEP 2: Review Existing Issues (30 min)

### Issues to Archive/Reassign

**Check these issue ranges:**
- BLK-1 to BLK-100 (all existing issues)

**For each issue, decide:**
- ✅ **Keep** - Relevant to Company Management MVP or Core Platform
- 🗄️ **Archive** - Products/Inventory work (wrong scope)
- ⏸️ **Pause** - Operations modules (Phase 2)

**Likely Archives:**
- BLK-60 to BLK-72 (Products/Inventory MVP - completed but wrong scope)
- BLK-41 to BLK-49 (Inventory/operations - Phase 2 work)

**Likely Keeps:**
- BLK-37 (Fix Frappe app structure) - Keep if relevant
- BLK-36 (Run Black and Ruff) - Keep if relevant
- Any Core Platform issues (Departments, Permissions, Auth)

**How to Archive:**
1. Open issue
2. Change status to "Canceled" or "Done (Archived)"
3. Add label: `archived`
4. Add comment: "Archived - [reason]"

---

## STEP 3: Create Labels (15 min)

### Priority Labels
- 🔴 `urgent` - #DC2626
- 🟠 `high` - #EA580C
- 🟡 `medium` - #CA8A04
- ⚪ `low` - #6B7280

### Type Labels
- `backend` - #EF4444
- `frontend` - #3B82F6
- `full-stack` - #8B5CF6
- `database` - #10B981
- `infrastructure` - #6366F1

### Domain Labels
- `company-mgmt` - #F59E0B
- `relationships` - #EC4899
- `tasks` - #14B8A6
- `reviews` - #8B5CF6
- `projects` - #06B6D4
- `finance` - #10B981
- `inventory` - #84CC16
- `recipes` - #F97316
- `procurement` - #6366F1
- `pos` - #8B5CF6
- `analytics` - #0EA5E9

### Status Labels
- `blocked` - #DC2626
- `in-review` - #F59E0B
- `ready-test` - #10B981
- `demo-critical` - #DC2626

### How to Create:
1. Go to Team Settings → Labels
2. Click "New Label"
3. Add name and color
4. Save

---

## STEP 4: Create Projects (15 min)

### Project 1: Company Management MVP (ACTIVE)

**Details:**
- **Name:** Company Management MVP
- **Status:** In Progress
- **State:** Started
- **Priority:** Urgent
- **Lead:** Eric
- **Start Date:** 2025-11-16
- **Target Date:** 2025-12-16
- **Description:**
```
Multi-entity hospitality company management platform for management company leadership and accounting teams.

**Goal:** Working demo by Dec 14-16

**Features:**
- Company/Entity Directory & Management
- Company Relationships (Banks, Tax, Insurance, Loans, Employees)
- Automated Task Management (recurring tasks)
- Review Period Tracking (month-end close)
- Project Tracking
- Accounting Dashboard

**Success Criteria:**
- Leadership can manage companies and relationships
- Task automation working
- Monthly close tracking functional
- Dashboard shows real KPIs
- Demo ready by Dec 14-16
```

**Icon:** 🏢

---

### Project 2: Core Platform (BACKGROUND)

**Details:**
- **Name:** Core Platform
- **Status:** In Progress
- **State:** Started
- **Priority:** High
- **Lead:** Eric
- **Description:**
```
Core infrastructure supporting all features: authentication, permissions, departments, subscriptions.

**Completed:**
- ✅ Departments
- ✅ Permissions (70+ granular permissions)
- ✅ Authentication (JWT)
- ✅ Subscription Plans

**In Progress:**
- Company Groups
- Intercompany Accounting
```

**Icon:** ⚙️

---

### Future Projects (Create as Planned)

Create these projects but mark as "Planned":

**Project 3: Inventory Management**
- Status: Planned
- Start: 2026-01-01 (tentative)
- Description: "Property-level inventory tracking and audits. Starts after MVP approval."

**Project 4: Procurement**
- Status: Planned
- Start: 2026-04-01 (tentative)
- Description: "Vendor management and purchasing. Depends on Inventory."

**Project 5: Recipe Costing**
- Status: Planned
- Start: 2026-04-01 (tentative)
- Description: "Recipe management and costing. Depends on Inventory."

**Project 6: POS Integration**
- Status: Planned
- Start: 2026-07-01 (tentative)
- Description: "POS system integration and depletion. Depends on Inventory and Recipes."

**Project 7: Multi-Location**
- Status: Planned
- Start: 2026-10-01 (tentative)
- Description: "Corporate master data and multi-location management."

**Project 8: Analytics**
- Status: Planned
- Start: 2027-01-01 (tentative)
- Description: "Advanced reporting and analytics."

---

## STEP 5: Create Milestones (20 min)

### For Project 1: Company Management MVP

**Milestone 1.1: Planning & Design**
- Project: Company Management MVP
- Start: 2025-11-16
- Target: 2025-11-22
- Description: "Complete system design - data model, API design, frontend architecture"

**Milestone 1.2: Backend Foundation**
- Project: Company Management MVP
- Start: 2025-11-20
- Target: 2025-11-29
- Description: "Core DocTypes and APIs functional"

**Milestone 1.3: Task Automation & Frontend**
- Project: Company Management MVP
- Start: 2025-11-30
- Target: 2025-12-06
- Description: "Task automation working, all frontend pages built"

**Milestone 1.4: Integration, Testing & Polish**
- Project: Company Management MVP
- Start: 2025-12-08
- Target: 2025-12-13
- Description: "E2E testing, bug fixes, demo preparation"

**Milestone 1.5: Demo Day**
- Project: Company Management MVP
- Start: 2025-12-14
- Target: 2025-12-16
- Description: "Present to leadership"

---

## STEP 6: Create Week 1 Issues (45 min)

### Design-001: Company Management Data Model

**Create Issue:**
- **Title:** `Design-001: Company Management Data Model`
- **Type:** Design (if available, or use label)
- **Project:** Company Management MVP
- **Milestone:** 1.1 Planning & Design
- **Priority:** 🔴 Urgent
- **Labels:** `backend`, `database`, `company-mgmt`, `demo-critical`
- **Assignee:** Eric
- **Estimate:** 1 day (8 points if using story points)
- **Start Date:** 2025-11-16
- **Due Date:** 2025-11-16
- **Dependencies:** None
- **Description:**
```
Design complete DocType schema for all Company Management features.

**Deliverables:**
- [ ] Company DocType schema (all fields, types, validation)
- [ ] Bank Relationship DocType schema
- [ ] Tax Entity Relationship DocType schema
- [ ] Insurance Relationship DocType schema
- [ ] Loan Relationship DocType schema
- [ ] Key Employee Relationship DocType schema
- [ ] Task Type DocType schema
- [ ] Review Period DocType schema
- [ ] Project DocType schema
- [ ] Entity relationship diagram
- [ ] Field specifications document

**Acceptance Criteria:**
- All DocTypes defined with complete field lists
- Data types specified (Data, Link, Int, Float, Date, etc.)
- Validation rules documented
- Relationships (Links) mapped
- Schema reviewed and approved

**Blocks:**
- Feature-001: Enhanced Company DocType
- Feature-002: Bank Relationship DocType
- Feature-003: Tax Entity Relationship DocType
- Feature-004: Insurance Relationship DocType
- Feature-005: Loan Relationship DocType
- Feature-006: Key Employee Relationship DocType
- Feature-007: Task Type DocType
- Feature-008: Review Period DocType
```

---

### Design-002: API Endpoint Design

**Create Issue:**
- **Title:** `Design-002: API Endpoint Design`
- **Project:** Company Management MVP
- **Milestone:** 1.1 Planning & Design
- **Priority:** 🔴 Urgent
- **Labels:** `backend`, `company-mgmt`, `demo-critical`
- **Assignee:** Eric
- **Estimate:** 1 day
- **Start Date:** 2025-11-17
- **Due Date:** 2025-11-17
- **Dependencies:** Design-001 (MUST SET THIS!)
- **Description:**
```
Design all REST API endpoints for Company Management features.

**Endpoints to Design:**
- get_company_details(company_id)
- list_companies(filters, limit, offset)
- get_company_relationships(company_id, type)
- get_company_banks(company_id)
- get_company_tax_entities(company_id)
- get_company_insurance(company_id)
- get_company_loans(company_id)
- get_company_employees(company_id)
- get_company_tasks(company_id, status)
- get_company_review_periods(company_id)
- get_dashboard_kpis(company_id)
- create_relationship(type, data)
- update_relationship(type, id, data)

**Deliverables:**
- [ ] All endpoints documented
- [ ] Request schemas (parameters, body)
- [ ] Response schemas (success, error)
- [ ] Permission requirements specified
- [ ] Error handling documented
- [ ] API documentation updated

**Acceptance Criteria:**
- All endpoints documented
- Request/response formats defined
- Permission model clear
- Error codes defined

**Blocked By:** Design-001
**Blocks:** Feature-009 (Company Management APIs)
```

---

### Design-003: Frontend Architecture

**Create Issue:**
- **Title:** `Design-003: Frontend Architecture`
- **Project:** Company Management MVP
- **Milestone:** 1.1 Planning & Design
- **Priority:** 🔴 Urgent
- **Labels:** `frontend`, `company-mgmt`, `demo-critical`
- **Assignee:** Eric
- **Estimate:** 1 day
- **Start Date:** 2025-11-18
- **Due Date:** 2025-11-18
- **Dependencies:** Design-002
- **Description:**
```
Design Next.js frontend structure, pages, components, and data flow.

**Pages to Design:**
- /companies (directory)
- /companies/[id] (detail)
- /companies/[id]/relationships/* (relationship forms)
- /tasks (task management)
- /review-periods (monthly close tracking)
- /projects (project management)
- /dashboard (home page with KPIs)

**Deliverables:**
- [ ] Page structure and routes defined
- [ ] Component hierarchy designed
- [ ] Navigation flow mapped
- [ ] State management approach (React Query, Context)
- [ ] Data fetching strategy
- [ ] Form handling approach (React Hook Form + Zod)
- [ ] Wireframes for key pages
- [ ] Responsive design approach

**Acceptance Criteria:**
- All pages identified
- Component structure clear
- Data flow documented
- Wireframes created
- Design reviewed

**Blocked By:** Design-002
**Blocks:** Feature-010 through Feature-016 (all frontend features)
```

---

### Design-004: Demo Walkthrough Script

**Create Issue:**
- **Title:** `Design-004: Demo Walkthrough Script`
- **Project:** Company Management MVP
- **Milestone:** 1.1 Planning & Design
- **Priority:** 🟠 High
- **Labels:** `demo-critical`
- **Assignee:** Eric
- **Estimate:** 0.5 day
- **Start Date:** 2025-11-19
- **Due Date:** 2025-11-19
- **Dependencies:** Design-003
- **Description:**
```
Create complete demo script for Dec 14-16 leadership presentation.

**Deliverables:**
- [ ] Demo storyline (narrative arc)
- [ ] Key talking points for each feature
- [ ] Demo data requirements
- [ ] Screenshots or mockups
- [ ] Success metrics to highlight
- [ ] Q&A preparation (anticipated questions)
- [ ] Backup plan if tech fails

**Demo Flow:**
1. Introduction (2 min) - Problem and solution
2. Company Management (3 min) - Show directory, add company
3. Relationships (3 min) - Add bank, insurance, view relationships
4. Task Automation (2 min) - Show auto-created tasks
5. Monthly Close (2 min) - Review period workflow
6. Dashboard (2 min) - Show KPIs and insights
7. Q&A and Next Steps

**Acceptance Criteria:**
- Complete script written
- Timing appropriate (10-15 min demo)
- Talking points compelling
- Demo flow logical
- Q&A prepared

**Blocked By:** Design-003
```

---

## STEP 7: Set Up Dependencies (30 min)

**Critical:** Linear dependencies ensure clear work order.

### How to Set Dependencies

1. Open an issue
2. Click "..." menu → "Add Relation"
3. Select "Blocks" or "Blocked by"
4. Search for the issue
5. Add relation

### Dependencies to Set (Week 1)

**Design-001 blocks:**
- Feature-001, Feature-002, Feature-003, Feature-004, Feature-005, Feature-006, Feature-007, Feature-008

**Design-002 blocks:**
- Feature-009

**Design-003 blocks:**
- Feature-010, Feature-011, Feature-012, Feature-013, Feature-014, Feature-015, Feature-016

**Design-002 blocked by:**
- Design-001

**Design-003 blocked by:**
- Design-002

**Design-004 blocked by:**
- Design-003

---

## STEP 8: Create Remaining Issues (Later)

**Don't create all issues now!** Create:
- Week 1 issues (Design-001 to Design-004) - NOW
- Week 2 issues (Feature-001 to Feature-009) - After Design-001 complete
- Week 3 issues (Feature-010 to Feature-017) - After Design-002/003 complete
- Week 4 issues (Test-001, Bug-001, etc.) - During Week 3

This prevents overwhelming the backlog.

---

## STEP 9: Set Up Views (15 min)

### View 1: Current Sprint (Active View)
- Filter: Status = "In Progress" OR "Todo"
- Filter: Milestone = Current milestone
- Group by: Assignee
- Sort by: Priority, then Due Date

### View 2: This Week
- Filter: Due Date = This Week
- Group by: Priority
- Sort by: Due Date

### View 3: Blocked Issues
- Filter: Has relation "Blocked by"
- Show: What's blocking them
- Sort by: Priority

### View 4: Demo Critical
- Filter: Label = "demo-critical"
- Sort by: Due Date
- Show: Progress and status

### View 5: Roadmap (Timeline View)
- All projects
- Show milestones
- Timeline view
- Filter: Not archived

---

## QUICK START CHECKLIST

After setup, your first actions:

### Today (Nov 16):
- [ ] Archive old projects (Step 1)
- [ ] Create labels (Step 3)
- [ ] Create Company Management MVP project (Step 4)
- [ ] Create Milestone 1.1 (Step 5)
- [ ] Create Design-001 issue (Step 6)
- [ ] **START WORKING ON Design-001**

### Tomorrow (Nov 17):
- [ ] Complete Design-001
- [ ] Create Design-002 issue
- [ ] Start Design-002

### Nov 18:
- [ ] Complete Design-002
- [ ] Create Design-003 issue
- [ ] Start Design-003

### Nov 19:
- [ ] Complete Design-003
- [ ] Create Design-004 issue
- [ ] Complete Design-004

### Nov 20 (Start Week 2):
- [ ] Create Milestone 1.2
- [ ] Create Feature-001 issue
- [ ] Start building!

---

## TIPS FOR SUCCESS

### Use Dependencies Religiously
- Every issue should show what it blocks/is blocked by
- Makes prioritization automatic
- Clear what to work on next

### Update Issues Daily
- Move to "In Progress" when starting
- Add comments with progress
- Move to "Done" when complete
- Update blockers if stuck

### Keep Milestones Tight
- 1 week max per milestone
- Review progress weekly
- Adjust dates if slipping

### Use Labels for Filtering
- Filter by `demo-critical` to see must-haves
- Filter by `blocked` to see what needs unblocking
- Filter by domain to focus work

### Demo-Critical First
- Always prioritize `demo-critical` issues
- Nice-to-haves can wait
- Demo date is fixed!

---

## MAINTAINING THE ROADMAP

### Weekly Review
Every Monday:
1. Review last week's progress
2. Update milestone dates if needed
3. Create next week's issues
4. Check dependencies
5. Identify risks/blockers

### After MVP (Post-Demo)
1. Create Phase 2 milestones
2. Break down Project 2 (Inventory) issues
3. Update roadmap based on feedback
4. Continue building!

---

**Ready to start!** Begin with Step 1 (Archive old projects) and work through the checklist.

The roadmap is your guide - every issue, every dependency, every milestone is planned. Just follow the path!
