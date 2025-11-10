# Consolidated Development Timeline

## Phase 0 – Foundations (Day 0-2)
- [ ] Align bench environment on ERPNext v15 with Frappe Press-compatible dependencies
  - Update `pyproject.toml`, `package.json`, and `requirements.txt`
  - Verify app install order and site configuration
- [ ] Capture existing product platform code quality status
  - Run existing tests, linting, and document gaps
  - Create refactor backlog (naming, deprecated DocTypes, etc.)
- [ ] Provision automation scripts
  - `scripts/bootstrap_site.py` to install apps, apply fixtures, assign subscription plans
  - Document usage in `docs/DEVELOPMENT-GUIDE.md`

## Phase 1 – Core Consolidation (Week 1)
- [ ] Core app (`blkshp_core`)
  - Implement/validate DocTypes: `Subscription Plan`, `Feature Toggle`, `Module Activation`, `Tenant Branding`
  - Enhance `UserPermissionMixin` for company + department + functional checks with tests
  - Build feature flag utilities + `/api/method/blkshp_core.get_feature_matrix`
- [ ] Products & Inventory alignment (`blkshp_ops`)
  - Import existing DocTypes; reconcile with ERPNext models (Products, Departments, Inventory Balance)
  - Ensure conversion utilities are in shared service with tests
  - Expose REST endpoints for Products, Inventory overview, audits
- [ ] Finance & Intercompany (`blkshp_finance`)
  - Ensure intercompany doc events, settlement DocType, and approval flows run on ERPNext v15
  - Provide API endpoints for balances, pending approvals, settlements
- [ ] API authentication
  - Configure OAuth2/JWT for SPA
  - Build login/profile endpoints (`/api/method/blkshp_core.login`, `.../profile`)

## Phase 2 – MVP Readiness (Week 2)
- [ ] Feature gating + subscription enforcement
  - Hook module activation checks into DocType events and REST endpoints
  - Build Desk admin UI for plan management and feature overrides
- [ ] Multi-tenancy scripts
  - Automate per-tenant site creation on Press (one site per customer)
  - Seed demo data for MVP (companies, departments, products, sample intercompany transactions)
- [ ] Front-end integration contracts
  - Finalize REST response schemas; document in `docs/API-REFERENCE.md`
  - Add CORS and rate limiting rules for SPA origin
- [ ] Testing & QA baseline
  - Expand unit/integration tests for critical flows (product CRUD, intercompany JE, audit close)
  - Set up GitHub Actions for lint/test

## Phase 3 – Demo & Feedback Loop (Week 3)
- [ ] Deploy MVP bench to staging Press site
  - Install apps, apply fixtures, verify subscription gating
  - Connect SPA MVP to staging APIs
- [ ] Conduct demo walkthrough scenarios
  - Product creation and department assignment
  - Inventory audit variance report
  - Intercompany transaction + approval + settlement
- [ ] Gather feedback, capture change requests, update backlog

## Phase 4 – Production Hardening (Weeks 4+)
- [ ] Security enhancements (HTTPS certificates, rate limiting, audit logging review)
- [ ] Observability (Sentry, uptime monitors, log aggregation)
- [ ] Documentation and training materials for ops team
- [ ] Plan next release wave (Recipes, POS, analytics, etc.)

## Tracking & Reporting
- Maintain task status in project management tool (Linear/Jira) synced with this timeline
- Update `docs/CHANGELOG.md` per milestone
- Review progress weekly; adjust estimates based on feedback and discovery

