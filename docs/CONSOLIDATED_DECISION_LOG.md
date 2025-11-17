# Consolidated Decision Journal

> Combines determinations from `PRODUCT_PLATFORM_DECISION_LOG.md`, `ACCOUNTING_OPERATIONS_PLATFORM_DECISION_LOG.md`, and `INTERCOMPANY_ACCOUNTING_FUNCTIONALITY_DECISION_LOG.md`. The **Source** column lists originating documents so future updates can trace lineage.

## Platform & Architecture
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Reserve Frappe Desk UI for internal BLKSHP operations and administration | Consolidation Decision | Desk not intuitive for end users; need polished client experience | Keeps internal tooling on native Desk while client-facing workflows move to dedicated front end | Requires parallel SPA/front-end project and hardened API surface | Frappe Desk, internal Ops tooling | 2025-11-10 |
| Maintain strict separation between BLKSHP administrative tooling and tenant-facing access | Consolidation Decision | Clients request plan/feature changes through BLKSHP operations | Protects subscription integrity and keeps sensitive controls with internal staff | Admin UIs/scripts gated to BLKSHP roles; tenant APIs expose read-only feature state | Subscription fixtures, admin tooling roadmap | 2025-11-10 |
| Deliver client-facing experience via dedicated front-end consuming Frappe/ERPNext APIs | Consolidation Decision | Hospitality customers need intuitive UI across modules | Allows custom UX, branding, and guided flows while reusing backend services | Necessitates API contracts, authentication gateway, and feature gating aligned with subscription model | Public API layer, auth service, front-end app | 2025-11-10 |
| Adopt Next.js + TypeScript + Tailwind SPA for external UI, backed by Frappe/ERPNext REST endpoints | Consolidation Decision | Need rapid MVP and modern UX while leveraging existing backend | Next.js provides SSR/SSG, strong tooling, and easy deployment; Tailwind accelerates UI build | Requires REST contract layer in Frappe, token-based auth, and CI/CD for SPA | Next.js app repo, Frappe API endpoints, OAuth/session handling | 2025-11-10 |
| **Approved Two-Phase Strategy: Quick MVP → Full Platform Rewrite (FastAPI + Next.js)** | Strategic Decision | Internal validation before major investment; clean architecture without gradual migration complexity | Phase 1 (2-3 months): Minimal MVP on Frappe+Next.js for internal company demo and adoption decision. Phase 2 (4-6 months with team, 10-12 months solo): Complete rewrite to FastAPI backend + Next.js frontend with modern stack (PostgreSQL, Clerk, custom RBAC, AI features). Clean break from Frappe after validation reduces technical debt vs gradual migration. ~40% of Python business logic portable from Frappe to FastAPI | MVP code throwaway except Next.js UI; two development cycles; total 6-9 months (MVP) + 4-12 months (platform) = 10-21 months depending on resources; but cleaner final architecture and clear go/no-go decision point | See DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md; Phase 1 MVP active; Phase 2 conditional on company adoption decision | 2025-11-16 |
| Adopt unified stack of Frappe Press + Bench + Framework + ERPNext for consolidated solution | Consolidation Decision | Align all domains on common hosted/runtime platform | Press provides managed SaaS footprint; Bench/ERPNext underpin existing automation | All modules must remain compatible with ERPNext core and Press deployment constraints | Frappe Press platform, ERPNext core | 2025-11-10 |
| Organize backend by domain modules with shared API layer | Product Platform | Maintain clear service boundaries | Mirrors business pillars and keeps cross-domain contracts explicit | Consolidation must map modules across apps | Domain module structure, API namespace | 2025-11-08 |
| Fork ERPNext source for intercompany automation (not standalone app) | Intercompany | Deep modifications to transaction DocTypes | Monolithic fork eases testing and allows system-generated entries | Upgrades harder; SaaS packaging bundles modified ERPNext | ERPNext fork repo, merge strategy | 2025-01-09 |
| Migrate legacy standalone DocTypes into ERPNext-aligned consolidated core | Consolidation Decision | Product app previously avoided ERPNext dependency | Harmonises data models across domains and leverages ERPNext functionality | Requires mapping existing masters into ERPNext equivalents and preserving business rules | Migration scripts, ERPNext DocTypes | 2025-11-10 |
| Adopt Frappe v15+ bench with multiple Frappe apps in single bench (`property_directory`, `accounting_operations`, etc.) | Accounting Ops | Property accounting ERP baseline stack | Multi-app bench separates concerns and release cadence | Requires dependency coordination and versioning per app | Bench, Python 3.10+, MariaDB 10.6+, Redis 6.2+ | 2025-10-28 |
| Retain Nginx → Gunicorn → Supervisor runtime topology | Accounting Ops | Production deployment topology | Matches bench defaults and provides TLS/process supervision | Ops maintains Nginx certs and Supervisor programs | Bench Procfile, Nginx config | 2025-10-28 |
| Use Redis 6.2+ for caching, queues, and sessions | Accounting Ops | Scheduler + cache requirements | Aligns with bench scheduler and job queue | Adds Redis operational dependency | Redis service, bench scheduler | 2025-10-28 |
| Default to per-tenant sites on Frappe Press (one bench/site per customer) for MVP and early rollout | Consolidation Decision | Need isolation, low cost, rapid provisioning | One-site-per-customer keeps data air-gapped, simplifies rollback, matches Press workflows | Provisioning scripts must automate Press site creation and plan management | Frappe Press automation, bench provisioner | 2025-11-10 |
| Document migration path to shared multi-site benches if cost optimisation required | Consolidation Decision | Future scaling option | Provides roadmap for consolidating smaller tenants once automation stable | Requires tooling to migrate sites without downtime | Migration playbooks, backup/restore scripts | 2025-11-10 |

## Data Model & Domain Design
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Use Departments as foundational segmentation across all domains | Product Platform | Replace fragmented Craftable segmentation | Unifies reporting, permissions, inventory logic | Every DocType stores `department`; consolidation must map | Department DocType, permission service | 2025-11-08 |
| Allow many-to-many product ↔ department allocations via `Product Department` child table | Product Platform | Shared items across departments | Prevents duplicate product masters and supports par levels | Inventory/procurement expect multi-department support | Product DocType, child table | 2025-11-08 |
| Maintain catalog of 70+ atomic permissions grouped into roles | Product Platform | Least privilege operations | Granular permissions support department CRUD distinctions | Consolidation must align other RBAC models | Permission registry, role fixtures | 2025-11-08 |
| Extend Frappe User DocType via mixin plus department permission child table | Product Platform | Enforce permissions at DocType level | Integrates with Frappe permission engine automatically | Alternate user stores must load mixin | `UserPermissionMixin`, custom fields | 2025-11-08 |
| Layer company/department access with granular functional permissions for every action | Consolidation Decision | Need unified access control across modules | Combines ERPNext company permissions, department mixin, and atomic function rights for least privilege | All services must verify both structural access and functional permission | User Permission DocType, department child table, permission registry | 2025-11-10 |
| Single Product DocType for all item types with hub-and-spoke unit conversion | Product Platform | Avoid duplicated catalogs and conversion drift | Shared conversion methods maintain consistent math | Downstream services must call shared helpers | Product conversion service | 2025-11-08 |
| Track inventory as Product + Department unique tuple; storage areas as metadata | Product Platform | Align with department-centric operations | Simplifies math and reporting | Migration from bin-level systems needs aggregation | Inventory Balance DocType unique index | 2025-11-08 |
| Maintain consolidated core module for shared masters (Company, Department, Product, Vendor, Feature Flag, etc.) gated by module activation | Consolidation Decision | Shared data must exist once while supporting optional modules | Keeps canonical masters central and only surfaces when dependent module is enabled | Module activation DocType must toggle fixtures, workspace, permissions | Core app (`blkshp_core`), activation scripts | 2025-11-10 |
| Shared COA across companies with per-company nicknames | Intercompany | Consolidated reporting across company group | Avoids account mapping while giving local naming flexibility | Companies must agree on COA template | COA replication scripts | 2025-01-09 |
| Add `line_item_company` to all child tables and mirror as Accounting Dimension | Intercompany | Need line-level allocations & reporting | Child field + dimension provides UI control + reporting filters | Requires synchronization validation | Custom fields, Accounting Dimension config | 2025-01-09 |
| Use two consolidated intercompany accounts per company (Due From/To) with party dimension granularity | Intercompany | Track company-pair balances without account explosion | Party field provides counterpart detail while keeping COA manageable | Depends on accurate party tagging | GL Entry party enforcement | 2025-01-09 |
| Introduce `Company Group` DocType for accounting rules distinct from Parent Company | Intercompany | Support multiple isolated groups and shared settings | Keeps org hierarchy separate from accounting automation | Onboarding adds group setup step | Company Group master | 2025-01-09 |
| Model Region → Property → Legal Entity hierarchy | Accounting Ops | Hospitality portfolio structure | Matches business reality and supports reporting | Downstream automation hinges on hierarchy integrity | Region/Property/Legal Entity DocTypes | 2025-10-28 |
| Require human-readable unique codes for key masters | Accounting Ops | Simplify automation and reporting | Prevents ambiguous references during integrations | Imports must enforce uniqueness | Unique constraints, validation scripts | 2025-10-28 |
| Store Property role assignments in dedicated DocType | Accounting Ops | Track staffing & automation assignments | Supports history and non-user role mapping | Requires data hygiene for downstream ACLs | Property Role Assignment DocType | 2025-10-28 |
| Define Task Type masters with recurrence & dependencies metadata | Accounting Ops | Standardize operational tasks | Enables recurring generation and governance | Changes ripple to all properties | Task Type DocType | 2025-10-28 |
| Mask/encrypt sensitive fields (EINs, bank accounts, balances) | Accounting Ops | Data protection obligations | Prevents accidental disclosure and supports compliance | Requires encryption service and key management | EncryptionService, security plumbing | 2025-10-28 |

## Workflow, Automation & UX
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Daily scheduler at 12:01 AM creates review periods and recurring tasks | Accounting Ops | Automate month-end task creation | Predictable timeline for finance teams | Scheduler failure stalls compliance tasks | Bench scheduler, task generation script | 2025-10-28 |
| Task lifecycle: To-Do → Complete → Reviewed → Corrections Needed → Closed | Accounting Ops | Enforce controller oversight | Ensures accountability and audit trail | Requires training and workflow controls | Task workflow config | 2025-10-28 |
| Auto-create monthly review periods | Accounting Ops | Keep close containers consistent | Guarantees executive reporting context | Scheduler downtime must be monitored | Review Period DocType | 2025-10-28 |
| Enforce task dependencies blocking downstream work | Accounting Ops | Prevent premature activities | Maintains workflow integrity | UI must surface blockers | Dependency tables, status checks | 2025-10-28 |
| Trigger exec review tasks after controller closures | Accounting Ops | Final approval layer | Provides leadership oversight | Extends close timeline, requires staffing | Review Period workflow | 2025-10-28 |
| Intercompany automation runs synchronously on submit, copying all line metadata | Intercompany | Ensure atomic automation | Keeps source + JEs in same transaction and preserves context | Submit latency increases; fail fast semantics | Doc events, IntercompanyManager mapping | 2025-01-09 |
| Use source posting date for generated JEs | Intercompany | Period integrity | Keeps reconciliations aligned | Backdated submissions propagate | Posting date propagation | 2025-01-09 |
| Create separate JE pairs per source→target company and ignore same-company lines | Intercompany | Mixed-company transactions | Facilitates reconciliation and settlement | More documents per submit | Grouping logic | 2025-01-09 |
| Require reversals instead of cancellation once intercompany JEs exist | Intercompany | Preserve audit trail | Prevents orphaned entries across companies | Users need reversal training | `before_cancel` hook, guidance | 2025-01-09 |
| Warn user on first intercompany line change; add badges + “View Intercompany JEs” button | Intercompany | UX awareness | Educates without alert fatigue and surfaces status | Requires form scripting and status fields | Client scripts, intercompany status | 2025-01-09 |
| Default `line_item_company` to parent company | Intercompany | Reduce data entry | Ensures field always populated | Depends on warning to catch overrides | Form scripts | 2025-01-09 |
| Build dedicated intercompany dashboard & reconciliation report | Intercompany | Finance visibility | Centralises balances, approvals, discrepancies | Requires balance APIs and caching | Dashboard page, balance services | 2025-01-09 |
| Define module dependency matrix so provisioning enforces prerequisites (e.g., Recipes requires Products + Inventory) | Consolidation Decision | Maintain integrity when enabling modules | Prevents activating modules without required foundations | Provisioning tooling must consult dependency matrix | Module dependency registry | 2025-11-10 |

## Security & Access Control
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Enforce 12+ character passwords and plan MFA rollout | Accounting Ops | Authentication baseline | Reduces credential risk | Increases onboarding friction | Frappe auth settings | 2025-10-28 |
| Plan secondary sensitive-data password (Phase 2) | Accounting Ops | Additional gating for masked data | Adds explicit consent before revealing sensitive values | Requires UX/password storage work | Sensitive Data Access workflow | 2025-10-28 |
| Log sensitive data views, permission denials, overrides | Accounting Ops | Audit readiness | Provides traceability for compliance | Generates monitoring overhead | Audit log DocTypes | 2025-10-28 |
| Harden production (TLS1.2+, HSTS, rate limiting, UFW) | Accounting Ops | Network security posture | Protects against eavesdropping/brute force | Ops must maintain configs | Nginx, UFW, certs | 2025-10-28 |
| Enable MariaDB encryption at rest for sensitive tables | Accounting Ops | Database security | Protects data if disks compromised | Requires key mgmt & performance review | MariaDB encryption config | 2025-10-28 |
| Company Group permissions: Read=All, Write=Accounts Manager, Create=System Manager | Intercompany | Control master data | Allows accountants to maintain membership safely | Initial setup needs admin assistance | DocType permissions | 2025-01-09 |
| Auto-generated JEs ignore permissions during creation, flagged read-only and reversal-only | Intercompany | Cross-company automation | Ensures entries created despite user roles and remain immutable | Users must reverse via source doc | IntercompanyManager, JE form overrides | 2025-01-09 |
| Settlement submission requires permissions in both companies (dual approval) | Intercompany | Fund transfer controls | Enforces segregation of duties | Adds approval latency | Settlement workflow, notifications | 2025-01-09 |
| Data isolation based on ERPNext user permissions (group ≠ access) | Intercompany | Protect intercompany data | Reuses standard permission model, enabling selective cross-company access | Requires user-permission governance | User Permission DocType | 2025-01-09 |
| Implement custom RBAC matrix aligned to accounting roles & filter access by property assignments | Accounting Ops | Data segregation | Ensures least privilege per property/region | Onboarding must map users correctly | Permission matrix, PropertyAccessControl | 2025-10-28 |
| Capture audit trails for task changes, sensitive access, role updates | Accounting Ops | Compliance logging | Provides evidence for audits | Storage growth to manage | History child tables, Security Event Logger | 2025-10-28 |

## Integrations & External Services
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Ship roles/fields via fixtures for repeatable setup | Product Platform | Environment parity | Guarantees identical permissions across benches for AI tooling | Fixture collisions need reconciliation during consolidation | Frappe fixture loader | 2025-11-08 |
| Target Ottimate integration for invoice import | Product Platform | Stakeholder expectation | Leverages existing AP tool for receiving | Consolidation must decide master system | Ottimate API, procurement DocTypes | 2025-11-08 |
| Automate Google Drive provisioning + uploads for month-end docs | Accounting Ops | Finance team workflow | Aligns with existing Drive processes | Requires API credentials & retries | Google Drive API integration | 2025-10-28 |
| Deliver notifications via SMTP templates | Accounting Ops | User communication | Provides auditability and consistency | Needs SMTP config & monitoring | EmailService helper | 2025-10-28 |
| Publish property change webhooks | Accounting Ops | Downstream sync | Real-time updates preferred over polling | Consumers must handle retries/security | Webhook service | 2025-10-28 |
| Expose health endpoint + use external uptime monitoring | Accounting Ops | Operational visibility | Enables automated detection | Requires integration with on-call alerts | Health endpoint, monitoring tools | 2025-10-28 |
| Instrument Sentry (and optional APM) | Accounting Ops | Observability | Centralises error tracking | Vendor cost, configuration overhead | Sentry DSN, optional agent | 2025-10-28 |
| Provide whitelisted APIs for intercompany balances, settlements, pending approvals | Intercompany | UI and future integration needs | Standard Frappe JSON API retains permissions | Requires Frappe session auth | API module | 2025-01-09 |
| Keep intercompany automation separate from ERPNext’s native features | Intercompany | Different business model | Clean separation avoids core conflicts | Users must learn distinction | Documentation, naming | 2025-01-09 |
| Defer banking/treasury integration to later phase while designing handoff points | Intercompany | Scope control | Focus on core features first but keep extensible | Settlements manual initially | Documented hooks | 2025-01-09 |
| Manage subscription tiers via `Subscription Plan` DocType linking module bundles and feature toggles | Consolidation Decision | Offer differentiated pricing & functionality | Enables quick enable/disable of modules or add-ons per tenant with audit trail | Admin tooling must update plans, apply fixtures, and refresh workspaces | Subscription Plan DocType, Feature Toggle hooks | 2025-11-10 |

## Deployment & Operations
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Follow GitFlow with protected `main`, CI on `develop` | Accounting Ops | Branch governance | Supports controlled releases and compliance review | Requires team discipline | GitHub branch rules | 2025-10-28 |
| Automate prod deploys via GitHub Actions executing remote scripts (Ansible backup) | Accounting Ops | CI/CD strategy | Reduces manual error | Secrets mgmt critical; scripts must be idempotent | GitHub Actions, deploy scripts | 2025-10-28 |
| Maintain staging bench prior to production promotion | Accounting Ops | Environment parity | Enables UAT/regression testing | Requires staging infra and refresh process | Staging bench setup | 2025-10-28 |
| Schedule daily backups with retention policy | Accounting Ops | Recovery requirements | Satisfies RPO/RTO | Must manage storage & restoration runbooks | `bench backup`, offsite storage | 2025-10-28 |
| Layer monitoring (UptimeRobot, Sentry, optional APM) with alerting | Accounting Ops | Operational monitoring | Proactive detection of failures | Requires on-call process | Monitoring services, alert routing | 2025-10-28 |
| Cache company group lookups and dashboard balances for 5 minutes | Intercompany | Reduce dashboard load | Balanced performance vs. freshness | Slight staleness risk; relies on Redis | `frappe.cache()` usage | 2025-01-09 |
| Add composite DB indexes for balance and reference queries | Intercompany | Performance | Keeps key queries under control | Schema migrations required | DB migration scripts | 2025-01-09 |

## Testing & Quality
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Use Frappe unittest framework with ≥80% coverage for intercompany core | Intercompany | Financial accuracy demands | Protects against regressions | Requires investment in tests and CI | Frappe test runner, coverage tooling | 2025-01-09 |
| Provide fixtures with sample companies (`Hotel A/B/C`) for testing | Intercompany | Reproducible scenarios | Covers multi-company edge cases | Fixtures must stay in sync with schema | Fixture scripts | 2025-01-09 |
| Aggressive validation with transactional rollback on error | Intercompany | Prevent data corruption | Fail-fast behaviour ensures integrity | Users may encounter blocking errors | Validation helpers, logging | 2025-01-09 |
| Adopt Frappe testing framework for accounting ops; ensure automation/test coverage of task engine | Accounting Ops | QA strategy | Framework integration ensures repeatable tests | Needs CI pipeline & fixture maintenance | Frappe tests, CI | 2025-10-28 |

## Future Enhancements & Roadmap
| Decision | Source | Context | Rationale | Impact | Depends On | Date |
| --- | --- | --- | --- | --- | --- | --- |
| Document Okta SSO integration as roadmap item | Product Platform | Enterprise access expectation | Keeps identity work visible despite pending status | Consolidation must align with other SSO plans | Frappe OAuth hooks | 2025-11-08 |
| Phase roadmap: Products/Inventory/Procurement (P2), Recipes/POS/Transfers (P3), Analytics/Budgeting/Payments (P4) | Product Platform | Delivery sequencing | Manages scope and sets stakeholder expectations | Future consolidation must respect phase commitments | BLKSHP OS roadmap docs | 2025-11-08 |
| Phase 1 intercompany scope vs. Phase 2 (consolidated eliminations, stock transfers, multi-currency) | Intercompany | Prevent scope creep | Focus MVP while designing extension points | Later phases require additional design | Intercompany roadmap | 2025-01-09 |
| Plan consolidated statement eliminations as virtual report entries (Phase 2) | Intercompany | Future GAAP compliance | Report-level eliminations avoid GL clutter | Reporting engine must support dynamic eliminations | Consolidation engine | 2025-01-09 |
| Defer multi-currency settlements to Phase 2 using ERPNext exchange framework | Intercompany | Initial single-currency rollout | Keeps MVP manageable; design remains extensible | Requires manual FX handling later | ERPNext currency tables | 2025-01-09 |
| Treat intercompany stock transfers as Phase 2 redesign | Intercompany | Complexity of inventory valuation | Allows financial automation to launch sooner | Interim manual process needed | Inventory roadmap | 2025-01-09 |
| Sensitive data secondary password rollout timing pending (Phase 2) | Accounting Ops | Balance security vs. effort | Provides roadmap milestone | Interim relies on masking | Security roadmap | 2025-10-28 |
| Determine trigger criteria for migrating from bench multi-site to per-tenant benches | Accounting Ops | SaaS scaling | Avoid ad hoc scaling decisions | Impacts provisioning tooling | Infrastructure roadmap | 2025-10-28 |

## Open Questions
| Question | Source | Context | Options | Priority | Date | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| Define training/documentation depth for intercompany rollout | Intercompany | Complex automation adoption | Videos only / Manual + videos / Comprehensive with certification | High | 2025-01-09 | Product & Enablement |
| Map intercompany month-end close workflow | Intercompany | Reconciliation/lock process | Reconcile balances, settle (full/partial), report, lock periods | Medium | 2025-01-09 | Finance Lead |
| Decide on banking automation for settlements | Intercompany | Payment execution | Manual transfers / Banking API / Hybrid | Low | 2025-01-09 | Finance Ops |
| Plan historical intercompany balance migration | Intercompany | Go-live readiness | Opening JEs / Historical import / Start fresh | High | 2025-01-09 | Implementation Lead |
| Set approval escalation/timeout rules for intercompany | Intercompany | Prevent stuck transactions | Reminder cadence / Escalation / Auto-approve / Manual follow-up | Medium | 2025-01-09 | Finance Governance |
| Validate performance strategy if scale exceeds 25 companies | Intercompany | Future growth | Document limits / Optimise / Throttle / Async | Low | 2025-01-09 | Engineering |
| Confirm audit trail requirements (USALI, external audits) | Intercompany | Compliance | Standard logs / Enhanced logs / Immutable log / External system | High | 2025-01-09 | Compliance |
| Document error recovery runbook for failed automation | Intercompany | Support readiness | Full rollback / Manual cleanup / Automated fixer | Medium | 2025-01-09 | Engineering |
| Determine access policy for cross-company consolidated reports | Intercompany | Report security | Require all-company permission / Group-level role / CFO only / Per-company snapshots | Medium | 2025-01-09 | Finance Governance |
| Clarify USALI-specific intercompany expectations | Intercompany | Hospitality compliance | Research standard / Consult accountant / Tailor reports | Medium | 2025-01-09 | Finance SME |
| Confirm Google Drive integration MVP timing | Accounting Ops | Stretch vs. core scope | Ship in MVP / Defer to Phase 2 | Medium | 2025-10-28 | Product & Engineering |
| Decide go-live for sensitive data secondary password | Accounting Ops | Security roadmap | Phase 2 / Phase 1 / Deferred | Medium | 2025-10-28 | Security Team |
| Establish triggers for moving to per-tenant benches | Accounting Ops | Multi-tenant scaling | Property count / Compliance / Performance threshold | Medium | 2025-10-28 | Infrastructure Lead |
| Timeline for SSO/2FA adoption beyond password policy | Accounting Ops | Identity roadmap | IdP integration now / Later / Not required | Medium | 2025-10-28 | Security & IT |
| Finalize caching strategy for theoretical inventory calculations | Product Platform | Performance gap | Redis caching / Materialized tables / On-demand recalculation | High | 2025-11-08 | Engineering |
| Align Okta SSO plan across consolidated stack | Product Platform | Enterprise identity requirement | Shared SSO across projects / Project-specific / Defer | Medium | 2025-11-08 | Platform Owners |


