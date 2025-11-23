# Consolidated Development Timeline

## Phase 0 – Foundations (Day 0-2) ✅ COMPLETE
- [x] Align bench environment on ERPNext v15 with Frappe Press-compatible dependencies
  - Update `pyproject.toml`, `package.json`, and `requirements.txt`
  - Verify app install order and site configuration
- [x] Capture existing product platform code quality status
  - Run existing tests, linting, and document gaps
  - Create refactor backlog (naming, deprecated DocTypes, etc.)
- [x] Provision automation scripts
  - `scripts/bootstrap_site.py` to install apps, apply fixtures, assign subscription plans
  - Document usage in `docs/DEVELOPMENT-GUIDE.md`

## Phase 1 – Core Consolidation (Week 1) ✅ COMPLETE (2025-11-16)
- [x] Core app (`blkshp_os`)
  - [x] Implement/validate DocTypes: `Subscription Plan`, `Feature Toggle`, `Module Activation`, `Tenant Branding`
  - [x] Reorganized core_platform module structure
  - [x] Built feature enforcement system with comprehensive documentation
  - [x] Delivered BLKSHP admin tooling for plan + module management
- [x] Products & Inventory alignment
  - [x] Consolidated Products, Departments, Inventory Balance DocTypes
  - [x] Implemented unit conversion utilities with tests
  - [x] Exposed 17 REST endpoints for Products and Inventory (see `docs/API-INVENTORY.md`)
- [x] Finance & Intercompany
  - [x] Implemented intercompany transaction automation
  - [x] Exposed 7 REST endpoints for balances, approvals, settlements (see `docs/API-FINANCE.md`)
- [x] API authentication
  - [x] Implemented JWT-based authentication for SPAs
  - [x] Built 6 authentication endpoints (login, refresh, profile, verify, token_info, logout)
  - [x] Comprehensive documentation in `docs/API-AUTHENTICATION.md`

**Phase 1 Deliverables:**
- 30 REST API endpoints across Inventory (17), Finance (7), Auth (6)
- Complete API documentation (3 comprehensive guides)
- JWT authentication system ready for Next.js consumption
- Backend ready for frontend integration

---

## Phase 2 – Minimal MVP for Internal Demo (2-3 Months) 🎯 CURRENT PHASE

**Strategy:** Build MINIMAL Next.js frontend for internal company validation only

**Purpose:** Prove concept to company leadership for adoption decision
**Scope:** Absolute minimum features (Products + Inventory view + Basic Auth)
**Decision Point:** End of Month 2-3 → Company decides to adopt internally or not

**Reference:** See `docs/DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md` for full two-phase strategy

### Month 1: Bare Bones Setup (Weeks 1-4)
- [ ] Initialize Next.js 14 project (basic setup, no Turborepo for MVP)
- [ ] Configure TypeScript, Tailwind CSS, shadcn/ui (minimal)
- [ ] Build basic Frappe API client (auth + products + inventory endpoints only)
- [ ] NextAuth.js with Frappe JWT (simple, not production-grade)
- [ ] Deploy to Vercel staging

**Deliverables:** Can log in, can call Frappe APIs

### Month 2: Core Features (Weeks 5-8)
- [ ] Products list with basic search (simple table, no fancy filters)
- [ ] Product detail view (read-only)
- [ ] Product create/edit form (single-step, no wizard)
- [ ] Inventory balance view (simple table with department filter)
- [ ] Basic navigation (top bar + sidebar skeleton)
- [ ] Dashboard with basic KPIs (product count, low stock)

**Deliverables:** Can manage products, can view inventory

### Month 3: Polish for Demo (Weeks 9-12) - OPTIONAL
- [ ] Bug fixes and error handling
- [ ] Mobile responsiveness (basic)
- [ ] Loading states and error messages
- [ ] Internal demo preparation
- [ ] **DECISION:** Company adopts internally? YES/NO

**Deliverables:** 🎯 **Internal demo complete, decision made**

### Out of Scope for MVP (Use Frappe Desk)
- ❌ Department management (use Frappe Desk)
- ❌ Inventory audits (use Frappe Desk)
- ❌ Finance/intercompany (use Frappe Desk)
- ❌ Advanced reporting (later)
- ❌ AI features (Phase 3)
- ❌ Mobile apps (Phase 3)

---

## Phase 3 – Full Platform Rewrite (4-6 Months with Team, 10-12 Months Solo)

**Conditional:** Only if company adopts internally after MVP

**Strategy:** Build production-grade platform on FastAPI + Next.js + PostgreSQL

**Stack:**
- FastAPI backend (async Python)
- PostgreSQL with PGVector
- Custom RBAC system
- Clerk authentication
- Complete feature set
- AI capabilities
- Modern DevOps

**Timeline:**
- Q1 (Months 1-3): Foundation (FastAPI, PostgreSQL, Clerk, RBAC, core APIs)
- Q2 (Months 4-6): Features (Products, Inventory, Procurement, Recipes, AI Invoice OCR)
- Q3 (Months 7-9): Advanced (Analytics, Demand Forecasting, NL Queries, Beta Launch)

**Reference:** See `docs/DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md` for detailed Phase 3 plan
**Porting Guide:** See `docs/FRAPPE-TO-FASTAPI-PORTING-GUIDE.md` for migration guidance

---

## Legacy Phases (Superseded by Next.js Strategy)

The following phases have been superseded by the Next.js frontend strategy. Original backend-focused work remains for reference:

### Phase 3 (Legacy) – Demo & Feedback Loop
- Deploy MVP to staging
- Conduct demo scenarios
- Gather feedback

### Phase 4 (Legacy) – Production Hardening
- Security enhancements
- Observability (Sentry, monitoring)
- Documentation and training

## Tracking & Reporting
- Maintain task status in project management tool (Linear/Jira) synced with this timeline
- Update `docs/CHANGELOG.md` per milestone
- Review progress weekly; adjust estimates based on feedback and discovery

