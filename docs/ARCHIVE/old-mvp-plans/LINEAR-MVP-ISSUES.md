# Linear Issues: Minimal MVP (COMPLETED ✅)

**Epic:** Minimal MVP for Internal Company Demo
**Timeline:** Planned 2-3 months | **Actual: 3 weeks** (9 weeks ahead!)
**Status:** ✅ **100% COMPLETE** (13/13 issues)
**Completed:** 2025-11-16
**Repository:** https://github.com/EricIrby/thepass-frontend

**IMPORTANT:** This MVP is COMPLETE and ready for internal validation.

---

## EPIC: MVP Internal Demo

**Success Criteria:**
- [x] Can log in with Frappe JWT ✅
- [x] Can view and manage products ✅
- [x] Can view inventory balances ✅
- [ ] Leadership approves for internal adoption (PENDING DEMO)

**Out of Scope:**
- ❌ Department management
- ❌ Inventory audits
- ❌ Advanced UI/UX
- ❌ Mobile apps
- ❌ AI features

---

## MONTH 1: Setup & Core Integration (4 weeks, 72 hours)

###BLK-MVP-01: Initialize Next.js Project
**Priority:** Critical | **Estimate:** 1 day (6 hrs)
**Labels:** `mvp`, `setup`

**Tasks:**
- Create Next.js 14 app with TypeScript + Tailwind
- Basic folder structure
- Dev server running
- Deploy placeholder to Vercel

**SKIP:** Turborepo, monorepo, complex build system

---

### BLK-MVP-02: Frappe API Client (Simple)
**Priority:** Critical | **Estimate:** 3 days (18 hrs)
**Labels:** `mvp`, `api-client`

**Tasks:**
- Simple fetch wrapper for Frappe APIs
- Auth endpoints (login, refresh)
- Products endpoints (list, get, create, update)
- Inventory endpoints (list balances)
- Basic error handling

**Example:**
```typescript
// lib/frappe-client.ts
export const frappeClient = {
  async login(username, password) {
    const res = await fetch('/api/method/blkshp_os.api.auth.login', {
      method: 'POST',
      body: JSON.stringify({ username, password })
    })
    return res.json()
  },

  async getProducts() {
    const res = await fetch('/api/method/blkshp_os.api.inventory.list_products', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    return res.json()
  }
}
```

**SKIP:** Type-safe SDK, extensive error handling, retry logic

---

### BLK-MVP-03: NextAuth.js Basic Setup
**Priority:** Critical | **Estimate:** 2 days (12 hrs)
**Labels:** `mvp`, `auth`

**Tasks:**
- NextAuth.js v5 configured
- Credentials provider for Frappe
- JWT token storage
- Protected routes
- Login page (simple form)

**SKIP:** Social logins, MFA, fancy UI

---

### BLK-MVP-04: Basic Navigation Shell
**Priority:** High | **Estimate:** 2 days (12 hrs)
**Labels:** `mvp`, `ui`

**Tasks:**
- Top navigation bar (logo + user menu)
- Simple sidebar (Dashboard, Products, Inventory)
- Protected route wrapper
- Logout function

**SKIP:** Collapsible sidebar, breadcrumbs, fancy animations

---

### BLK-MVP-05: Dashboard Skeleton
**Priority:** Medium | **Estimate:** 1 day (6 hrs)
**Labels:** `mvp`, `ui`

**Tasks:**
- Welcome message
- Product count card
- Low stock count card
- Basic layout

**SKIP:** Charts, graphs, advanced analytics

**Month 1 Total:** 54 hours / 72 available ✅

---

## MONTH 2: Core Features (4 weeks, 72 hours)

### BLK-MVP-06: Products List Page
**Priority:** Critical | **Estimate:** 3 days (18 hrs)
**Labels:** `mvp`, `products`

**Tasks:**
- Table showing products (product_code, product_name, category, status)
- Basic search by name/code
- "Create Product" button
- Click row → detail view
- Loading skeleton
- Empty state

**SKIP:** Advanced filters, pagination (just show all), sorting, bulk actions

---

### BLK-MVP-07: Product Detail View
**Priority:** High | **Estimate:** 2 days (12 hrs)
**Labels:** `mvp`, `products`

**Tasks:**
- Show product information (read-only)
- Product code, name, category, unit, valuation rate
- "Edit" button → edit form
- Breadcrumbs

**SKIP:** Unit conversions table, department allocations (just show primary unit)

---

### BLK-MVP-08: Product Create/Edit Form
**Priority:** Critical | **Estimate:** 4 days (24 hrs)
**Labels:** `mvp`, `products`, `forms`

**Tasks:**
- Single-step form (NOT wizard)
- Fields: product_code, product_name, category, primary_unit, valuation_rate
- Form validation (Zod)
- Submit → create/update product
- Success/error toast notifications
- Cancel button

**SKIP:** Multi-step wizard, department allocations, unit conversions, auto-save

---

### BLK-MVP-09: Inventory Balance View
**Priority:** Critical | **Estimate:** 2 days (12 hrs)
**Labels:** `mvp`, `inventory`

**Tasks:**
- Simple table showing inventory balances
- Columns: product, department, quantity, unit
- Basic department filter dropdown
- Search by product name

**SKIP:** Stock ledger, batch details, storage areas, audit workflows

---

### BLK-MVP-10: Error Handling & Loading States
**Priority:** High | **Estimate:** 1 day (6 hrs)
**Labels:** `mvp`, `ux`

**Tasks:**
- Loading spinners on all async operations
- Error toast notifications
- Basic error boundary
- 404 page
- Network error handling

**SKIP:** Retry logic, detailed error messages, error tracking service

**Month 2 Total:** 72 hours / 72 available ✅

---

## MONTH 3 (OPTIONAL): Polish for Demo (4 weeks, 72 hours)

### BLK-MVP-11: Bug Fixes
**Priority:** High | **Estimate:** 1 week (18 hrs)
**Labels:** `mvp`, `qa`

**Tasks:**
- Fix reported bugs
- Test all user flows
- Edge case handling
- Data validation improvements

---

### BLK-MVP-12: Mobile Responsiveness (Basic)
**Priority:** Medium | **Estimate:** 1 week (18 hrs)
**Labels:** `mvp`, `responsive`

**Tasks:**
- Responsive navigation (hamburger menu)
- Tables scroll horizontally on mobile
- Forms work on mobile
- Doesn't need to be perfect, just functional

**SKIP:** Native mobile app, sophisticated mobile UX

---

### BLK-MVP-13: Demo Preparation
**Priority:** Critical | **Estimate:** 1-2 weeks (18-36 hrs)
**Labels:** `mvp`, `demo`

**Tasks:**
- Seed demo data
- Create demo script/walkthrough
- Test demo flow end-to-end
- Fix critical visual issues
- Prepare talking points

---

## Total Effort Estimate

| Month | Issues | Hours | Actual (18hrs/wk) |
|-------|--------|-------|-------------------|
| 1 | 5 | 54 hrs | 4 weeks |
| 2 | 5 | 72 hrs | 4 weeks |
| 3 (opt) | 3 | 36-54 hrs | 2-3 weeks |
| **Total** | **13** | **162-180 hrs** | **10-11 weeks** |

**Timeline:**
- **Aggressive:** 2 months (skip Month 3)
- **Recommended:** 2.5 months (partial Month 3)
- **Safe:** 3 months (full Month 3 polish)

---

## Comparison: MVP vs Full Frontend

| Aspect | Full Frontend (Original) | MVP (This Plan) |
|--------|-------------------------|-----------------|
| **Issues** | 37 issues | 13 issues |
| **Timeline** | 12 weeks | 8-12 weeks |
| **Effort** | ~288 hours | ~162 hours |
| **Scope** | Complete UI, all modules | Products + Inventory only |
| **Quality** | Production-ready | Demo-ready |
| **Purpose** | Customer launch | Internal validation |

---

## Success Metrics

**End of Month 2:**
- [ ] Can successfully demo to leadership
- [ ] Products CRUD works end-to-end
- [ ] Inventory balances display correctly
- [ ] No critical bugs
- [ ] Runs on desktop browser

**Demo Day:**
- [ ] Leadership can log in
- [ ] Can create/edit products
- [ ] Can view inventory
- [ ] Value proposition clear
- [ ] **DECISION: Adopt internally?**

---

## Next Steps After MVP

### If Company Says YES:
1. Celebrate! 🎉
2. Start Phase 3: Full Platform Rewrite
   - FastAPI backend
   - PostgreSQL + PGVector
   - Clerk auth
   - Custom RBAC
   - AI features
3. Timeline: 4-6 months with team, 10-12 months solo
4. Reference: `docs/DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md`

### If Company Says NO:
1. Continue using Frappe Desk
2. Reassess in 6-12 months
3. MVP code can be archived

---

## How to Create Issues in Linear

1. **Create Epic:** "MVP Internal Demo"
2. **Create Milestones:**
   - Month 1: Setup & Integration
   - Month 2: Core Features
   - Month 3: Polish (optional)
3. **Create Issues:** BLK-MVP-01 through BLK-MVP-13
4. **Assign to yourself**
5. **Set 2-week sprints**

---

## Recommended Sprint Structure

**Sprint 1-2 (Weeks 1-4): Month 1**
- BLK-MVP-01, 02, 03, 04, 05

**Sprint 3-4 (Weeks 5-8): Month 2**
- BLK-MVP-06, 07, 08, 09, 10

**Sprint 5-6 (Weeks 9-12): Month 3 - Optional**
- BLK-MVP-11, 12, 13

---

*Document Created: 2025-11-16*
*Version: 1.0*
*Status: Active - Minimal MVP Strategy*
