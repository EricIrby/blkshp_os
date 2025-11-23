# The Pass - Company Management Platform

**Multi-entity hospitality company management and accounting automation**

**Product Name:** The Pass
**Current Focus:** Company Management MVP
**Timeline:** 1 month to demo (Nov 16 - Dec 16, 2025)
**Last Updated:** November 16, 2025

---

## 🎯 What is The Pass?

The Pass is a **multi-entity management platform** for hospitality management companies operating multiple properties/entities. It provides company/entity management, relationship tracking, task automation, and financial oversight for management company leadership and accounting teams.

### Current Priority: Company Management MVP

**Goal:** Working demo for internal leadership by December 14-16, 2025

**Target Users:**
- Multi-entity management company leadership
- Accounting and finance teams

**Core Features (MVP):**
1. **Company/Entity Directory & Management** - Centralized company information
2. **Company Relationships** - Banks, Tax Entities, Insurance, Loans, Key Employees
3. **Automated Task Management** - Recurring tasks (daily/weekly/monthly/quarterly/annual)
4. **Review Period Tracking** - Month-end close workflow and progress
5. **Project Tracking** - Accounting projects and milestones
6. **Accounting Dashboard** - KPIs, alerts, and insights for leadership

---

## 🚀 Quick Start

### For Development

**Prerequisites:**
- Frappe Bench installed
- A test site created
- Terminal access

**Setup:**
```bash
cd /path/to/frappe-bench

# Install the app
bench --site mysite.local install-app blkshp_os

# Run migrations
bench --site mysite.local migrate

# Start server
bench start
```

**Access:** `http://localhost:8000`

---

## 📚 Documentation

### Getting Started

**START HERE:** 👇
- **[00-CURRENT/REORGANIZATION-COMPLETE.md](00-CURRENT/REORGANIZATION-COMPLETE.md)** - What's been done, what's next
- **[00-CURRENT/LINEAR-COMPLETE-ROADMAP.md](00-CURRENT/LINEAR-COMPLETE-ROADMAP.md)** - Complete roadmap (MVP → Final Product)
- **[00-CURRENT/LINEAR-SETUP-GUIDE.md](00-CURRENT/LINEAR-SETUP-GUIDE.md)** - How to set up Linear for project tracking

### Core Documentation
- **[GUIDES/Development-Guide.md](GUIDES/Development-Guide.md)** - Development workflow
- **[GUIDES/Testing-Guide.md](GUIDES/Testing-Guide.md)** - Testing practices
- **[GUIDES/Git-Workflow.md](GUIDES/Git-Workflow.md)** - Git practices
- **[CONSOLIDATED_DECISION_LOG.md](CONSOLIDATED_DECISION_LOG.md)** - Decision history

### Current Work (Active MVP Development)
- **[00-CURRENT/](00-CURRENT/)** - Active MVP planning and tracking
- **[02-COMPANY-MANAGEMENT/](02-COMPANY-MANAGEMENT/)** - Company Management domain (to be created)
- **[03-FINANCE/](03-FINANCE/)** - Finance & Intercompany Accounting

### Core Platform (Completed)
- **[02-DEPARTMENTS/](02-DEPARTMENTS/)** - Department management (✅ Complete)
- **[11-PERMISSIONS/](11-PERMISSIONS/)** - Permissions system (✅ Complete)
- **[00-ARCHITECTURE/](00-ARCHITECTURE/)** - Architecture documentation

### API Documentation
- **[API/Authentication.md](API/Authentication.md)** - JWT authentication
- **[API/Finance.md](API/Finance.md)** - Finance & intercompany APIs
- **[API/Inventory.md](API/Inventory.md)** - Inventory APIs
- **[API/Reference.md](API/Reference.md)** - Complete API reference

### Future Work (Post-MVP)
- **[FUTURE/Operations-Modules/](FUTURE/)** - Inventory, recipes, procurement, etc. (Phase 2+)

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- Frappe Framework v15+
- Python 3.10+
- MariaDB 10.6+
- JWT Authentication

**Frontend:**
- Next.js 14 with App Router
- TypeScript
- Tailwind CSS
- React Query (TanStack Query)

**Infrastructure:**
- Frappe Bench
- Nginx
- Redis 6.2+

### Current Status

**Completed (✅):**
- Departments domain
- Permissions system (70+ granular permissions)
- JWT authentication
- Intercompany accounting
- Company Groups
- Subscription management

**In Progress (🔄):**
- Company Management MVP (4 weeks)
- Task automation
- Review period tracking

**Planned (📋):**
- Operations modules (inventory, recipes, etc.) - Phase 2
- Multi-location management - Phase 3
- Advanced analytics - Phase 3

---

## 📅 Timeline

### Phase 1: Company Management MVP (ACTIVE)
**Timeline:** Nov 16 - Dec 16, 2025 (4 weeks)

**Weekly Breakdown:**
- **Week 1 (Nov 16-22):** Planning & Design
- **Week 2 (Nov 23-29):** Backend Foundation (DocTypes & APIs)
- **Week 3 (Nov 30-Dec 6):** Task Automation & Frontend
- **Week 4 (Dec 7-13):** Testing, Polish, Demo Prep
- **Demo Day:** Dec 14-16, 2025

### Phase 2: Operations Modules (PLANNED)
**Timeline:** Jan-Jun 2026 (conditional on Phase 1 approval)
- Inventory management
- Procurement
- Recipe costing
- POS integration

### Phase 3: Platform Enhancement (PLANNED)
**Timeline:** Jul-Dec 2026
- Multi-location (Director)
- Advanced analytics
- Budgeting

### Phase 4: Scale & Optimize (ONGOING)
**Timeline:** 2027+
- Performance optimization
- Mobile apps
- AI features
- Advanced integrations

---

## 🎯 MVP Scope

### Must Have (Demo Critical)

✅ **Company Management:**
- Company directory (list, search, filter)
- Company details (legal info, addresses, contacts)
- Company status tracking

✅ **Relationships:**
- Banks (account info, encrypted fields)
- Tax Entities (federal, state, local)
- Insurance (policies, coverage, renewals)
- Loans (lenders, amounts, terms)
- Key Employees (contacts, roles)

✅ **Task Automation:**
- Task templates (recurrence patterns)
- Automatic task creation (daily scheduler)
- Task assignment by role
- Task dependencies

✅ **Review Periods (Month-End Close):**
- Review period tracking per company
- Status workflow (Open → In Progress → Controller Review → Executive Review → Closed)
- Task completion tracking
- Progress indicators

✅ **Dashboard:**
- Active companies count
- Open tasks by company
- Review periods status
- Projects in progress
- Upcoming deadlines

### Out of Scope (Phase 2)

❌ Inventory management
❌ Recipe costing
❌ POS integration
❌ Procurement/ordering
❌ Advanced analytics
❌ Multi-location
❌ Budgeting
❌ Payment processing

---

## 🔗 Key Resources

### Internal
- **Linear Project:** Company Management MVP
- **Repository:** `apps/blkshp_os`
- **Frontend Repository:** `thepass-frontend` (Next.js)

### External
- **Frappe Documentation:** https://docs.frappe.io/
- **ERPNext Documentation:** https://docs.erpnext.com/

---

## 🚦 Current Status

**Phase:** Phase 1 - Company Management MVP
**Week:** Week 1 - Planning & Design
**Current Task:** Set up Linear and begin Design-001 (Data Model)

**Next Steps:**
1. Review complete roadmap ([00-CURRENT/LINEAR-COMPLETE-ROADMAP.md](00-CURRENT/LINEAR-COMPLETE-ROADMAP.md))
2. Set up Linear ([00-CURRENT/LINEAR-SETUP-GUIDE.md](00-CURRENT/LINEAR-SETUP-GUIDE.md))
3. Start Design-001: Company Management Data Model
4. Complete Week 1 planning (4 design issues)

---

## 📊 Success Metrics

### Week 1 (Planning)
- [ ] Linear organized and structured
- [ ] All 4 design issues completed
- [ ] Complete data model documented
- [ ] API endpoints designed
- [ ] Frontend architecture designed
- [ ] Demo script written

### Phase 1 (MVP - 4 weeks)
- [ ] All features implemented
- [ ] Company Management working end-to-end
- [ ] Task automation functional
- [ ] Dashboard showing real data
- [ ] Demo delivered successfully
- [ ] **Leadership approval received**

---

## 🆘 Need Help?

**Documentation Issues:**
- Check [00-CURRENT/REORGANIZATION-COMPLETE.md](00-CURRENT/REORGANIZATION-COMPLETE.md) for status
- Check [CONSOLIDATED_DECISION_LOG.md](CONSOLIDATED_DECISION_LOG.md) for decision history

**Development Issues:**
- Check [GUIDES/Development-Guide.md](GUIDES/Development-Guide.md)
- Check domain-specific README files (e.g., [02-DEPARTMENTS/README.md](02-DEPARTMENTS/README.md))

**Architecture Questions:**
- Check [00-ARCHITECTURE/](00-ARCHITECTURE/) documentation

---

## 📝 Notes

### Recent Changes (2025-11-16)

**Documentation Reorganized:**
- Moved outdated MVP plans to `ARCHIVE/old-mvp-plans/`
- Moved Phase 2 rewrite plans to `ARCHIVE/phase-2-plans/`
- Moved operations modules to `FUTURE/Operations-Modules/`
- Created `00-CURRENT/` for active work
- Created comprehensive roadmap and Linear setup guide

**Focus Shifted:**
- FROM: Products/Inventory MVP
- TO: Company Management MVP
- Reason: Aligned with actual user needs (management company leadership & accounting teams)

### Product Vision

**The Pass** is being built in phases:

1. **Company Management** (Current) - For management company leadership and accounting teams
2. **Operations Modules** (Phase 2) - For property-level operations (inventory, recipes, etc.)
3. **Platform Enhancement** (Phase 3) - Multi-location, advanced features
4. **Scale & Optimize** (Phase 4) - Production readiness, mobile, AI

Each phase builds on the previous, creating a comprehensive hospitality management platform.

---

**Let's build! 🚀**

*For the complete roadmap and detailed planning, see [00-CURRENT/](00-CURRENT/)*
