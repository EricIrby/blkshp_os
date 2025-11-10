# BLKSHP OS Development Guide

_Last updated: 2025-11-10_

This guide provides the day-to-day workflow, tooling expectations, and references required to work on the consolidated BLKSHP OS codebase.

## 1. Quick Start Checklist

1. **Clone bench & apps** – see `docs/README.md` for installation details.
2. **Install dependencies** – ensure Python 3.10+, Node 18 LTS, Yarn/NPM as preferred.
3. **Sync documentation** – review:
   - `docs/CONSOLIDATED_DECISION_LOG.md`
   - `docs/PROJECT-TIMELINE.md`
   - Relevant domain docs under `docs/`
4. **Connect to Linear** – issues live in the [BLKSHP Linear workspace](https://linear.app/blkshp/). Link Cursor → Linear for in-editor access.
5. **Create feature branch** – use Linear issue identifier, e.g. `feature/blk-17-inventory-audit-api`.
6. **Run local bench** – `bench start` (backend) + `npm run dev` (frontend once scaffolded).

## 2. Tooling & Workflow

| Area | Tooling | Notes |
| --- | --- | --- |
| Issue Tracking | Linear | Projects by module (`Core Platform`, `Operations`, `Finance`, `Frontend`). Milestones mirror phases. |
| Source Control | GitHub (`blkshp_os`) | Feature branches follow `feature/blk-XX-*`. Include issue ID in commits & PR titles. |
| Code Editor | Cursor | Linear integration keeps issues visible; use MCP tools for context. |
| Bench | ERPNext v15 / Frappe Press | Local bench for dev; Press per-tenant scripts in Phase 2. |
| Frontend | Next.js, TypeScript, Tailwind | Repo under `frontend/` (Phase 1 scaffolding). |

### Standard Flow

1. **Pick issue from Linear** (move to `To Do`).
2. **Create branch** named with issue ID.
3. **Develop & test** (see section 4).
4. **Open Draft PR** – Linear moves issue to `In Progress` automatically.
5. **Request review** – final PR moves issue to `In Review`.
6. **Merge** – Linear marks issue `Done`; delete branch when ready.

## 3. Phase Overview

Phases are tracked in `docs/PROJECT-TIMELINE.md` and Linear milestones:

- **Phase 0 – Foundations**: Bench compatibility, provisioning scripts, baseline audits.
- **Phase 1 – Core Consolidation**: Subscription core (`blkshp_core`), Product/Inventory alignment, intercompany hooks.
- **Phase 2 – MVP Readiness**: Feature enforcement, demo data, frontend MVP.
- **Phase 3 – Demo & Feedback**: Staging deployment, scripted demo walkthroughs.
- **Phase 4 – Hardening**: Security, observability, documentation refresh.

## 4. Development Standards

### 4.1 Backend (Frappe/ERPNext)
- Follow domain folder structure (`blkshp_core`, `blkshp_ops`, `blkshp_finance`).
- Use shared utilities (permissions mixin, feature toggles, conversion services).
- Always enforce department + company filters; no raw SQL without guards.
- Feature gates checked server-side even if hidden in UI.
- Export DocType changes using `bench export-fixtures` where applicable.

### 4.2 Frontend (Next.js)
- Organize features under `frontend/src/modules/*` per domain.
- Hydrate feature matrix & profile on login; guard routes using hooks.
- Use React Query for all API calls; handle error and loading states.
- Maintain TypeScript types in `frontend/src/types`. Generate from OpenAPI if available.

### 4.3 Testing
- Backend unit tests via `bench run-tests --app <app>`.
- Integration tests for critical workflows (inventory audits, intercompany settlements).
- Frontend unit tests (Vitest) and E2E (Playwright) for MVP flows.
- CI pipelines (`.github/workflows/`) must run lint + tests before merge.

### 4.4 Documentation
- Update the relevant domain README/implementation summary for changes.
- Add new endpoints to `docs/API-REFERENCE.md`.
- Record significant decisions in `docs/CONSOLIDATED_DECISION_LOG.md` via PR note.
- Keep `docs/PROJECT-TIMELINE.md` progress boxes accurate as milestones complete.

## 5. Deployment & Environments

- **Local Bench:** default for development & testing.
- **Staging Press Site:** provisioned per Phase 3 using automation in `scripts/bootstrap_site.py` and Press tools.
- **Production Press Sites:** one Press site per customer, configured via Module Activation + Subscription Plan DocTypes.
- **Frontend Deployments:** Vercel recommended; Press static hosting supported if needed.

## 6. Branching & PR Conventions

- Branch: `feature/blk-XX-description`
- Commit: `BLK-XX: Summary of change`
- PR title: `BLK-XX: <short description>`
- PR template should include checklist for tests, docs, feature flags.

## 7. Essential Commands

```bash
# Run migrations/tests for specific app
bench --site <site> migrate
bench --site <site> run-tests --app blkshp_core

# Export fixtures after DocType updates
bench --site <site> export-fixtures

# Frontend
cd frontend
npm install
npm run dev
```

## 8. Support & References

- **Decision Log:** `docs/CONSOLIDATED_DECISION_LOG.md`
- **Project Timeline:** `docs/PROJECT-TIMELINE.md`
- **Architecture:** `docs/00-ARCHITECTURE/`
- **Testing Guide:** `docs/TESTING-GUIDE.md`
- **Linear Projects:** `Core Platform`, `Operations (blkshp_ops)`, `Finance`, `Frontend Application`

## 9. Onboarding Notes

- Review `AGENT-INSTRUCTIONS.md` if using AI-assisted development.
- Load context package via `docs/AGENT-CONTEXT-PACKAGE.md` for automated tooling.
- Use Cursor’s Linear integration to keep issue state synchronized while coding.

---

By following this guide alongside the decision log and timeline, you can pick up any task in `blkshp_os` with full context and deliver consistent, production-ready changes.
