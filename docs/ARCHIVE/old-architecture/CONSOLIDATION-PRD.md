## BLKSHP OS Consolidation PRD

### 1. Executive Summary
BLKSHP OS is a Frappe-based, desk-only application that unifies hospitality product, inventory, and cost-control workflows under a single, domain-driven architecture. The platform emphasizes department-centric access, a 2D inventory model (Product + Department), granular role permissions, and an API-first surface, making it a strong candidate for consolidation with other back-office operations platforms serving restaurants, bars, and catering teams.

### 2. Problem Statement & Goals
- **Primary Problem:** Fragmented tooling across food, beverage, and operations silos leads to duplicated item catalogs, inconsistent inventory tracking, and role-access gaps.
- **Vision:** Deliver a single-source-of-truth operating system with department-aware workflows, extensible permissions, and unified product data.
- **Goals:** Centralize masters, enforce consistent inventory math, expose comprehensive APIs for ecosystem integration, and accelerate future domain expansion.

### 3. Target Users & Personas
- **Director / Multi-Location Operations:** Requires cross-department visibility and standardized controls.
- **Store or Department Managers:** Need granular inventory, procurement, and recipe management with department-specific permissions.
- **Buyers & Receivers:** Coordinate vendor relationships, purchase units, and intake.
- **Inventory Specialists & Auditors:** Depend on theoretical vs. actual models, audit workflows, and variance tracking.
- **Developers / Integrators:** Extend via APIs, fixtures, and Frappe DocTypes to embed into broader ecosystems.

### 4. Scope & Functional Pillars
- **Phase 1 (Delivered):** Departments and Permissions domains with DocTypes, client scripts, fixtures, 70+ permissions, 20 whitelisted endpoints, and unit tests.
- **Phase 2 (In Progress):** Products, Inventory, Procurement, Recipes, POS Integration, Transfers & Depletions, Analytics, Accounting, Budgets, Payments, Director oversight.

### 5. Functional Requirements
- **Department Management:** CRUD for departments, hierarchy, product allocations, access checks, statistics, users, and permissions.
- **Role & Permission Engine:** Standard roles, custom role creation, permission registry, bulk assignment, role summaries, and permission search.
- **Products Domain (Planned):** Unified catalog spanning departments, purchase units, hub-and-spoke conversions, storage metadata, pricing, labels, bulk loaders, and audit trails.
- **Inventory & Procurement (Planned):** Theoretical inventory math, counting tasks, audits, vendor relations, ordering, invoicing, integrations (e.g., Ottimate).
- **POS & Recipe (Planned):** Sales ingestion, automatic depletion, recipe costing tied to inventory, manual depletion workflows.
- **Analytics & Director (Planned):** Department-filtered reporting, multi-location governance, budgeting, payment orchestration.

### 6. Non-Functional Requirements
- **Platform:** Frappe 14+, desk-only UI for back-office operations.
- **Performance:** Lean DocType controllers and REST endpoints; incremental domain modules reduce blast radius.
- **Security:** Department-aware permission checks with 70+ atomic permissions enforcing least privilege.
- **Extensibility:** Domain isolation, fixture-driven configuration, typed Python modules, and exhaustive documentation.

### 7. Data Model & Key Entities
- **DocTypes:** Department, Department Permission, Product Department, Role Permission (implemented); forthcoming Product, Inventory Transaction, Procurement Order, Recipe, Audit.
- **Relationships:** Many-to-many product↔department, role↔permissions, user↔department permissions; 2D inventory keyed by `(product_id, department_id)`.
- **Metadata:** Storage locations as metadata (not distinct inventory buckets), hub-based unit conversion anchored on primary count unit.

### 8. API Surface
- **Current Endpoints (20):** Seven department endpoints (access, hierarchy, products, stats) and thirteen permission endpoints (permission registry, role management, user checks, bulk operations).
- **Planned Endpoints:** Products CRUD, conversion calculators, inventory adjustments, procurement ordering, recipe costing, POS import/export, reporting dashboards.

### 9. Integrations & Dependencies
- **Framework:** Frappe Bench ecosystem (Python 3.10+, Node 18+, MariaDB/PostgreSQL).
- **External Touchpoints:** Ottimate (procurement invoices), POS systems (sales import), potential accounting packages (QuickBooks, etc.).
- **Consolidation Considerations:** Evaluate overlap in product catalog, permissions, and inventory logic across candidate systems. Identify opportunities to reuse BLKSHP’s domain modules as canonical services or map to existing masters (e.g., unify vendor + product taxonomies, leverage API-first design for interoperability).

### 10. Operational Considerations
- **Deployment:** Standard Frappe bench deployment scripts; MIT license.
- **Setup:** Install app, run fixtures/test data scripts, configure passwords, start bench; automated setup script `scripts/test.sh` streamlines provisioning.
- **Testing:** Domain-specific tests via `bench run-tests`, with coverage for DocTypes, services, and APIs; logs available through bench CLI.

### 11. Success Metrics
- **Adoption:** Percentage of departments and users managed within BLKSHP across consolidated estate.
- **Data Integrity:** Reduction in duplicate product entries; accuracy of theoretical vs. actual inventory variance.
- **Operational Efficiency:** Time-to-close inventory audits, purchase order cycle time, recipe costing accuracy.
- **Integration Health:** Number of consuming systems using BLKSHP APIs; latency/error rate across integrations.
- **Security Compliance:** Audit pass rate on permission reviews; incidents of unauthorized access.

### 12. Roadmap & Phasing
1. **Phase 2 (Near-Term):** Complete Products, Inventory, Procurement domains; deliver end-to-end inventory workflows.
2. **Phase 3:** Recipes, POS Integration, Transfers & Depletions; enable theoretical depletion and sales sync.
3. **Phase 4:** Analytics, Director multi-location, Budgeting, Payments; expand to executive reporting.
4. **Future Architecture:** Optional SPA frontend (Vue/React) per architecture guidance; maintain API parity.

### 13. Risks & Open Questions
- **Data Migration:** Effort to reconcile existing product catalogs, units, and permissions from target consolidation systems.
- **Change Management:** User retraining for department-centric operations versus legacy silos.
- **Scaling:** Ensuring DocType and permission logic remains performant with multi-location, high-volume transactions.
- **Integration Alignment:** Mapping external POS and procurement data models to the 2D inventory paradigm; handling variance in unit conversion logic.
- **Governance:** Defining ownership when multiple projects contribute to shared domain modules post-consolidation.

### 14. Consolidation Notes for AI Review
- Assess how BLKSHP’s unified product + department model can subsume or interoperate with overlapping modules in other projects (e.g., where another system already manages procurement, evaluate API contracts versus potential module reuse).
- Evaluate permission granularity compatibility—BLKSHP’s atomic permission registry may become the master authority.
- Consider doc-driven development approach; extensive documentation can bootstrap AI-assisted migration or refactoring tasks.
- Determine whether consolidation favors migrating other systems onto Frappe Bench or abstracting BLKSHP services behind shared APIs for gradual integration.

### 15. Next Steps
- Inventory candidate projects’ domain coverage, technology stacks, and data models against BLKSHP’s roadmap.
- Prioritize gap analysis on product, inventory, and procurement modules to estimate effort for consolidation or federation.
- Prototype data interchange via existing REST endpoints to validate integration feasibility before deeper merging.
- Align stakeholders on governance and deployment strategy (single bench instance versus federated deployments).

