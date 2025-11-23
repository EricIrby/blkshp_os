# BLKSHP OS Development Guide

_Last updated: 2025-11-15_

This guide provides the day-to-day workflow, tooling expectations, and references required to work on the consolidated BLKSHP OS codebase.

## 1. Bench Environment Structure

BLKSHP OS is developed within a **Frappe Bench environment**. Understanding this structure is essential for effective development:

```
BLKSHP-DEV/                          # Bench root (two directories up from app)
├── apps/
│   ├── frappe/                      # Frappe Framework
│   ├── erpnext/                     # ERPNext (optional but recommended)
│   └── blkshp_os/                   # BLKSHP OS app (current working directory)
│       ├── blkshp_os/               # Python package
│       ├── docs/                    # Documentation
│       ├── fixtures/                # Fixtures
│       └── scripts/                 # Utility scripts
├── sites/
│   ├── common_site_config.json      # Shared site configuration
│   └── [site-name]/                 # Individual site directories
│       ├── site_config.json         # Site-specific config
│       └── private/                 # Site private files
├── env/                             # Python virtual environment
│   └── bin/
│       ├── python                   # Python interpreter
│       └── bench                    # Bench CLI
├── config/                          # Supervisor/nginx configs
└── logs/                            # Application logs
```

**Key Paths:**
- **Current working directory:** `/Users/Eric/Development/BLKSHP/BLKSHP-DEV/apps/blkshp_os` (app code)
- **Bench root:** `../../` from current directory
- **Bench commands:** Available from any directory (uses bench context)
- **Virtual environment:** `../../env/bin/python`

## 2. Quick Start Checklist

1. **Verify bench environment** – ensure you're in the bench directory structure.
2. **Install dependencies** – ensure Python 3.10+, Node 18 LTS are available in the bench.
3. **Install app on site** – follow the bench app installation order (see section 2.1 below).
4. **Sync documentation** – review:
   - `docs/CONSOLIDATED_DECISION_LOG.md`
   - `docs/PROJECT-TIMELINE.md`
   - Relevant domain docs under `docs/`
5. **Connect to Linear** – issues live in the [BLKSHP Linear workspace](https://linear.app/blkshp/). Link Cursor → Linear for in-editor access.
6. **Create feature branch** – use Linear issue identifier, e.g. `feature/blk-17-inventory-audit-api`.
7. **Test locally in bench** – deploy and test changes before committing (see section 4).

### 2.1 Bench App Installation Order

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

## 3. Tooling & Workflow

| Area | Tooling | Notes |
| --- | --- | --- |
| Issue Tracking | Linear | Projects by module (`Core Platform`, `Operations`, `Finance`, `Frontend`). Milestones mirror phases. |
| Source Control | GitHub (`blkshp_os`) | Feature branches follow `feature/blk-XX-*`. Include issue ID in commits & PR titles. |
| Code Editor | Cursor | Linear integration keeps issues visible; use MCP tools for context. |
| Bench | ERPNext v15 / Frappe Press | Local bench for dev; Press per-tenant scripts in Phase 2. |
| Frontend | Next.js, TypeScript, Tailwind | Repo under `frontend/` (Phase 1 scaffolding). |

### Standard Development Workflow

The development workflow leverages the local Frappe Bench environment for testing and validation before committing changes:

1. **Pick issue from Linear** (move to `To Do`).
2. **Create feature branch** named with issue ID (e.g., `feature/blk-XX-description`).
3. **Develop changes** in the app codebase (`apps/blkshp_os/`).
4. **Deploy to local bench** (see section 5 for detailed workflow):
   - Build assets: `bench build --app blkshp_os`
   - Run migrations: `bench --site [site] migrate`
   - Clear cache: `bench --site [site] clear-cache`
5. **Test locally**:
   - Manual testing in bench UI
   - Run unit tests: `bench --site [site] run-tests --app blkshp_os`
   - Verify functionality matches requirements
6. **Commit changes** once tests pass and functionality is verified.
7. **Open Draft PR** – Linear moves issue to `In Progress` automatically.
8. **Request review** – final PR moves issue to `In Review`.
9. **Merge** – Linear marks issue `Done`; delete branch when ready.

**Key Principle:** Always test changes in the local bench environment before committing to ensure code quality and catch issues early.

## 4. Phase Overview

Phases are tracked in `docs/PROJECT-TIMELINE.md` and Linear milestones:

- **Phase 0 – Foundations**: Bench compatibility, provisioning scripts, baseline audits.
- **Phase 1 – Core Consolidation**: Subscription core (`blkshp_core`), Product/Inventory alignment, intercompany hooks.
- **Phase 2 – MVP Readiness**: Feature enforcement, demo data, frontend MVP.
- **Phase 3 – Demo & Feedback**: Staging deployment, scripted demo walkthroughs.
- **Phase 4 – Hardening**: Security, observability, documentation refresh.

## 5. Local Bench Development Workflow

Since the app is now developed within a Frappe Bench environment, you can deploy and test changes locally before committing to GitHub. This workflow ensures code quality and catches issues early.

### 5.1 Typical Development Cycle

```bash
# 1. Make code changes in apps/blkshp_os/
# (edit DocTypes, Python files, JS files, etc.)

# 2. Build assets (if you changed JS/CSS/client scripts)
bench build --app blkshp_os

# 3. Run database migrations (if you changed DocType schemas)
bench --site [your-site] migrate

# 4. Clear cache to ensure changes are reflected
bench --site [your-site] clear-cache

# 5. Restart bench (if you changed server-side Python)
bench restart

# 6. Test in browser
# Navigate to http://localhost:8000 and test your changes

# 7. Run automated tests
bench --site [your-site] run-tests --app blkshp_os

# 8. If tests pass and functionality works, commit your changes
git add .
git commit -m "BLK-XX: Description of changes"
```

### 5.2 Common Bench Commands for Development

| Command | Purpose | When to Use |
| --- | --- | --- |
| `bench build --app blkshp_os` | Compile JS/CSS assets | After changing client scripts, CSS, or JS files |
| `bench --site [site] migrate` | Run database migrations | After changing DocType schemas or adding fixtures |
| `bench --site [site] clear-cache` | Clear server cache | After changing Python code, hooks, or configuration |
| `bench restart` | Restart Frappe processes | After changing Python code (alternative to clear-cache) |
| `bench --site [site] run-tests --app blkshp_os` | Run all app tests | Before committing changes |
| `bench --site [site] console` | Python console with Frappe context | For debugging and testing code snippets |
| `bench --site [site] mariadb` | Access database directly | For debugging database issues |
| `bench --site [site] export-fixtures` | Export fixtures to JSON | After changing Custom Fields or other fixtures |

### 5.3 Testing Workflow

**Unit Tests:**
```bash
# Run all tests for the app
bench --site [site] run-tests --app blkshp_os

# Run tests for specific module
bench --site [site] run-tests --app blkshp_os --module blkshp_os.departments

# Run specific test file
bench --site [site] run-tests --app blkshp_os --module blkshp_os.departments.doctype.department.test_department
```

**Manual Testing:**
1. Start bench: `bench start`
2. Navigate to `http://localhost:8000`
3. Log in with your test credentials
4. Test the functionality manually
5. Verify all edge cases and error handling

**Integration Testing:**
- Test critical workflows end-to-end
- Verify permissions and access control
- Test department-based filtering
- Verify intercompany transactions (if applicable)

### 5.4 Working from the App Directory

Since your current working directory is the app (`apps/blkshp_os/`), bench commands work from anywhere:

```bash
# Bench commands work from the app directory
pwd
# /Users/Eric/Development/BLKSHP/BLKSHP-DEV/apps/blkshp_os

# No need to navigate to bench root
bench --site [site] migrate
bench build --app blkshp_os
```

Bench automatically detects it's within a bench directory structure and executes commands in the correct context.

### 5.5 Debugging Tips

**View Logs:**
```bash
# Tail all bench logs
bench --site [site] logs

# View specific log file
tail -f ../../logs/bench.log
```

**Enable Developer Mode:**
```bash
bench --site [site] set-config developer_mode 1
bench --site [site] clear-cache
```

Developer mode enables:
- More detailed error messages
- Automatic reloading on code changes
- Access to developer tools in UI

**Python Debugging:**
```python
# Add to your Python code for breakpoints
import frappe
frappe.log_error("Debug message", "Debug Title")

# Or use print statements (visible in bench console)
print(f"Debug: {variable}")
```

## 6. Development Standards

### 6.1 Backend (Frappe/ERPNext)
- Follow domain folder structure (`blkshp_core`, `blkshp_ops`, `blkshp_finance`).
- Use shared utilities (permissions mixin, feature toggles, conversion services).
- Always enforce department + company filters; no raw SQL without guards.
- Feature gates checked server-side even if hidden in UI.
- Export DocType changes using `bench export-fixtures` where applicable.
- **Test in local bench before committing** - ensure migrations run and tests pass.

### 6.2 Frontend (Next.js)
- Organize features under `frontend/src/modules/*` per domain.
- Hydrate feature matrix & profile on login; guard routes using hooks.
- Use React Query for all API calls; handle error and loading states.
- Maintain TypeScript types in `frontend/src/types`. Generate from OpenAPI if available.

### 6.3 Testing
- **Always test in local bench environment before committing** (see section 5.3).
- Backend unit tests via `bench --site [site] run-tests --app blkshp_os`.
- Integration tests for critical workflows (inventory audits, intercompany settlements).
- Frontend unit tests (Vitest) and E2E (Playwright) for MVP flows.
- CI pipelines (`.github/workflows/`) must run lint + tests before merge.

### 6.4 Documentation
- Update the relevant domain README/implementation summary for changes.
- Add new endpoints to `docs/API-REFERENCE.md`.
- Record significant decisions in `docs/CONSOLIDATED_DECISION_LOG.md` via PR note.
- Keep `docs/PROJECT-TIMELINE.md` progress boxes accurate as milestones complete.

## 7. Deployment & Environments

- **Local Bench:** default for development & testing.
- **Staging Press Site:** provisioned per Phase 3 using automation in `scripts/bootstrap_site.py` and Press tools.
- **Production Press Sites:** one Press site per customer, configured via Module Activation + Subscription Plan DocTypes.
- **Frontend Deployments:** Vercel recommended; Press static hosting supported if needed.

### 7.1 ERPNext v15 & Frappe Press Compatibility

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

### 7.2 Site Provisioning

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

## 8. Branching & PR Conventions

- Branch: `feature/blk-XX-description`
- Commit: `BLK-XX: Summary of change`
- PR title: `BLK-XX: <short description>`
- PR template should include checklist for tests, docs, feature flags.
- **Before creating PR:** Ensure all tests pass in local bench and changes are tested.

## 9. Essential Commands

All commands can be run from the app directory (`apps/blkshp_os/`) as bench detects the environment context.

```bash
# Development cycle (from apps/blkshp_os/ directory)
bench build --app blkshp_os          # Build JS/CSS assets
bench --site <site> migrate          # Run database migrations
bench --site <site> clear-cache      # Clear cache after Python changes
bench restart                        # Restart bench processes

# Testing
bench --site <site> run-tests --app blkshp_os                    # Run all tests
bench --site <site> run-tests --app blkshp_os --module <module>  # Run specific module tests

# Fixtures
bench --site <site> export-fixtures  # Export fixtures after DocType updates

# Debugging
bench --site <site> console          # Python console with Frappe context
bench --site <site> logs             # View application logs

# Frontend (when scaffolded)
cd frontend
npm install
npm run dev
```

**Note:** All bench commands work from the app directory - no need to navigate to bench root.

## 10. Support & References

- **Decision Log:** `docs/CONSOLIDATED_DECISION_LOG.md`
- **Project Timeline:** `docs/PROJECT-TIMELINE.md`
- **Architecture:** `docs/00-ARCHITECTURE/`
- **Testing Guide:** `docs/TESTING-GUIDE.md`
- **Linear Projects:** `Core Platform`, `Operations (blkshp_ops)`, `Finance`, `Frontend Application`

## 11. Onboarding Notes

- Review `AGENT-INSTRUCTIONS.md` if using AI-assisted development.
- Load context package via `docs/AGENT-CONTEXT-PACKAGE.md` for automated tooling.
- Use Cursor’s Linear integration to keep issue state synchronized while coding.

---

By following this guide alongside the decision log and timeline, you can pick up any task in `blkshp_os` with full context and deliver consistent, production-ready changes.
