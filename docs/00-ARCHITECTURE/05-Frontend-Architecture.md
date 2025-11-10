# Client Frontend Architecture

## Overview

BLKSHP OS exposes a dedicated client-facing experience via a Next.js (React) single-page application while retaining the Frappe Desk UI for internal BLKSHP operations.

- **Internal Users (BLKSHP team):** Continue using Frappe Desk for tenant administration, provisioning, and support workflows.
- **Client Users (Hospitality groups):** Access a tailored Next.js application that surfaces module dashboards, workflows, and analytics powered by the same ERPNext/Frappe backend.

## Tech Stack Summary

| Layer | Technology | Notes |
| --- | --- | --- |
| Frontend | Next.js 14 (React 18), TypeScript, Tailwind CSS | Hybrid SSG/SSR for performance; Tailwind for rapid UI development |
| State/Data | React Query (TanStack Query) + Context | Handles API caching, background refresh, feature flag hydration |
| Forms | React Hook Form + Zod | Schema validation shared with backend expectations |
| Testing | Vitest + Testing Library + Playwright | Unit and end-to-end coverage |
| Observability | Sentry (frontend SDK) | Mirrors backend error tracking |
| Deployment | Vercel or Frappe Press static hosting | Environment variables per tenant, CDN caching |

## Backend Integration

- **Authentication:** Utilize Frappe OAuth2 (preferred) or session tokens. SPA login flow obtains token -> stored via httpOnly cookie or secure storage.
- **API Surface:** REST endpoints exposed under `/api/method/blkshp_*` or versioned routes. GraphQL optional via `frappe_graphql`.
- **Feature Matrix:** `/api/method/blkshp_core.get_feature_matrix` returns subscription plan, enabled modules, and granular feature toggles.
- **Profile Endpoint:** Provides user, company/department access, and permissions summary for bootstrapping SPA state.
- **Permissions:** Backend remains the source of truth—SPA hides gated features but server-side enforcement always applied.

## Routing & Modules

```
/             → Executive dashboard (KPIs, alerts)
/products     → Product catalogue, filters, CRUD (feature gated)
/inventory    → Inventory summary, audits, variances
/intercompany → Approvals, settlements, historical reporting
/settings     → Profile, notifications, tenant-specific settings
```

Each route checks the hydrated feature matrix + permission scope before rendering.

## Multi-Tenancy & Theming

- Frappe Press provisions one site per tenant; SPA is served per tenant subdomain.
- Tenant branding (logo, colors) stored in `Tenant Branding` DocType and delivered via profile API.
- Optional white-labelling enables custom theme variants.

## Deployment Workflow

1. **Local Development:** `npm run dev` (Next.js) alongside local bench (`bench start`).
2. **Build:** `npm run lint && npm run test && npm run build` in CI.
3. **Deploy:** Push to main -> Vercel auto-deploy or `bench build --app blkshp_frontend` for Press static hosting.
4. **Environment Config:** `.env.local` -> staging/production secrets via platform (Vercel env vars or Press config).

## Security

- CORS configured in Nginx/Frappe to allow SPA origins.
- Rate limiting applied to public API endpoints.
- Tokens stored securely; refresh tokens (if used) handled via backend endpoints.
- Sentry instrumentation with scrubbed PII.

## Roadmap Alignment

- **Phase 1:** Repository scaffolding, auth flow design, API contract finalization.
- **Phase 2:** Implement MVP screens (Dashboard, Products, Inventory, Intercompany).
- **Phase 3:** Connect to staging API, deploy MVP build, rehearse demo scenarios.
- **Phase 4+:** PWA/offline support, advanced analytics, theming enhancements, mobile optimizations.

Refer to `docs/PROJECT-TIMELINE.md` and Linear project "Frontend Application" for task-level tracking.
