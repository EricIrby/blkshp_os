# BLKSHP OS Development Guide

_Last updated: 2025-11-10_

This guide provides the day-to-day workflow, tooling expectations, and references required to work on the consolidated BLKSHP OS codebase.

## 1. Quick Start Checklist

1. **Clone bench & apps** – see `docs/README.md` for installation details.
2. **Install dependencies** – ensure Python 3.10+, Node 18 LTS, Yarn/NPM as preferred.
3. **Install app** – follow the bench app installation order (see section 1.1 below).
4. **Sync documentation** – review:
   - `docs/CONSOLIDATED_DECISION_LOG.md`
   - `docs/PROJECT-TIMELINE.md`
   - Relevant domain docs under `docs/`
5. **Connect to Linear** – issues live in the [BLKSHP Linear workspace](https://linear.app/blkshp/). Link Cursor → Linear for in-editor access.
6. **Create feature branch** – use Linear issue identifier, e.g. `feature/blk-17-inventory-audit-api`.
7. **Run local bench** – `bench start` (backend) + `npm run dev` (frontend once scaffolded).

### 1.1 Bench App Installation Order

When setting up a new bench or site, install apps in the following order:

```bash
# 1. Frappe Framework (installed by default with bench init)
# 2. ERPNext (if not already installed)
bench get-app erpnext --branch version-15

# 3. BLKSHP OS (this app)
bench get-app https://github.com/your-org/blkshp_os --branch main

# Install on site in the same order
bench --site mysite.local install-app erpnext
bench --site mysite.local install-app blkshp_os
```

**Important Notes:**
- BLKSHP OS has no `required_apps` specified in `hooks.py`, but it extends ERPNext/Frappe core DocTypes (User, Role)
- Always install ERPNext before BLKSHP OS to ensure core DocTypes exist
- The app is compatible with ERPNext v15 and Frappe v15+

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

### 5.1 ERPNext v15 & Frappe Press Compatibility

**Compatibility Status:** ✅ Fully compatible with ERPNext v15 and Frappe Press

BLKSHP OS has been audited for ERPNext v15 compatibility (see BLK-5). Key findings:

**Dependencies:**
- Python 3.10+ required (compatible with ERPNext v15)
- No external Python dependencies beyond Frappe/ERPNext
- No custom frontend build pipeline (uses Frappe's built-in asset bundling)
- No Node.js dependencies (no package.json)

**Build & Update:**
- `bench build --app blkshp_os` - Compiles JS/CSS assets using Frappe's bundler
- `bench --site <site> migrate` - Runs database migrations
- `bench update --patch` - Updates app and applies patches
- All standard bench commands are supported

**Frappe Press Deployment:**
- Pure Python/JS app with no custom build requirements
- Uses standard Frappe fixtures mechanism for Custom Fields and Roles
- No special server configuration needed
- Compatible with Press's standard deployment pipeline

**App Structure:**
- Follows Frappe v15 app structure conventions
- Uses modern hook patterns (e.g., `extend_doctype_class`)
- No deprecated APIs or patterns
- Frontend assets: minimal client scripts for User and Role forms only

**Configuration Files:**
- `pyproject.toml` - Uses flit_core build backend (standard for Frappe apps)
- `hooks.py` - Standard v15 hooks, no deprecated patterns
- `modules.txt` - Defines 14 modules for the app
- `patches.txt` - Empty (ready for future database patches)
- No `requirements.txt` needed (dependencies managed by bench)

**Testing:**
```bash
# Verify build works
bench build --app blkshp_os

# Run migrations
bench --site <site> migrate

# Run app tests
bench --site <site> run-tests --app blkshp_os

# Update app (includes patches)
bench update --patch
```

### 5.2 Site Provisioning

**Audience:** BLKSHP Operations staff only

The `scripts/bootstrap_site.py` script automates the creation and configuration of tenant sites for BLKSHP OS. This tool streamlines the provisioning process by handling site creation, app installation, subscription plan configuration, and initial setup in a single command.

**Prerequisites:**
- Active Frappe bench environment (for local provisioning)
- BLKSHP Operations credentials
- For Frappe Press: `FC_API_KEY` and `FC_API_SECRET` environment variables

**Basic Usage:**

```bash
# Create a local site with FOUNDATION plan
python scripts/bootstrap_site.py --site demo.local --plan FOUNDATION

# Create site with custom admin password
python scripts/bootstrap_site.py --site tenant1.local --plan FOUNDATION --admin-password secure123

# Enable specific modules beyond the plan's defaults
python scripts/bootstrap_site.py --site tenant1.local --plan FOUNDATION \
    --enable-module inventory --enable-module procurement
```

**Available Options:**

| Option | Required | Description |
|--------|----------|-------------|
| `--site` | Yes | Site name (e.g., `demo.local` or `tenant.frappe.cloud`) |
| `--plan` | Yes | Subscription plan code (e.g., `FOUNDATION`, `PROFESSIONAL`) |
| `--enable-module` | No | Enable specific module (can be specified multiple times) |
| `--admin-password` | No | Administrator password (default: `admin`) |
| `--press` | No | Provision on Frappe Press instead of local bench |
| `--press-team` | No | Frappe Press team name (required if `--press` is used) |

**What the Script Does:**

1. **Site Creation**: Creates new Frappe site with specified name
2. **App Installation**: Installs `blkshp_os` and required dependencies
3. **Migrations**: Runs all database migrations to set up schema
4. **Role Setup**: Creates and configures BLKSHP Operations role
5. **Plan Configuration**: Applies subscription plan and validates plan exists
6. **Module Overrides**: Enables additional modules if specified
7. **Summary Report**: Provides next steps and access information

**Frappe Press Integration:**

Frappe Press provisioning is planned for Phase 2 but not yet implemented. When using `--press`, the script will display instructions for manual Press provisioning. Contact BLKSHP DevOps for Press deployment support.

**Security Notes:**

- This tool is restricted to BLKSHP Operations staff only
- All provisioning actions are audit-logged
- Clients cannot request direct provisioning; they must contact BLKSHP support
- Default passwords should be changed immediately after provisioning

**Troubleshooting:**

```bash
# Verify bench environment
bench --version

# Check if site already exists
bench --site <site> version

# Manually verify plan exists
bench --site <site> console
>>> frappe.get_all("Subscription Plan", pluck="plan_code")
```

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
