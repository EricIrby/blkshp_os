# Linear Issues: MVP Next.js Frontend (Minimal)

**Epic:** Minimal MVP for Internal Company Demo
**Timeline:** 2025-11-16 to 2026-01-16 (2 months, Month 3 optional polish)
**Goal:** MINIMAL working product to present to company for adoption decision

**IMPORTANT:** This is NOT a full product. This is a proof-of-concept for internal validation only.
**Strategy:** See `docs/DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md`

---

## EPIC: Minimal MVP for Internal Demo

**Description:**
Build the BARE MINIMUM Next.js frontend to demonstrate the concept to company leadership. This is NOT a customer-ready product. This is purely for internal validation to decide whether to proceed with full platform development.

**Minimal Scope:**
- Login/logout (basic)
- Products list + create/edit (simple forms)
- Inventory balance view (read-only table)
- Basic dashboard (product count, low stock)
- Works on desktop (mobile nice-to-have)

**Success Criteria (Internal Demo):**
- [ ] Leadership can log in
- [ ] Can view and manage products
- [ ] Can view inventory balances
- [ ] Demonstrates value proposition
- [ ] **DECISION:** Company adopts internally? (YES/NO)

**NOT in Scope:**
- ❌ Polish UX (good enough for demo)
- ❌ Department management (use Frappe Desk)
- ❌ Inventory audits (use Frappe Desk)
- ❌ Mobile apps
- ❌ AI features
- ❌ Advanced reporting

**Dependencies:**
- ✅ Frappe backend APIs (30 endpoints available)
- ✅ JWT authentication
- ✅ API documentation

**Next Steps After MVP:**
- If YES → Proceed to Phase 3 (FastAPI full platform rewrite)
- If NO → Continue using Frappe Desk

**Links:**
- Strategy: `docs/DEVELOPMENT-STRATEGY-MVP-TO-PLATFORM.md`
- Timeline: `docs/PROJECT-TIMELINE.md`
- Porting Guide (Phase 3): `docs/FRAPPE-TO-FASTAPI-PORTING-GUIDE.md`

---

## MONTH 1: Bare Bones Setup (Weeks 1-4)

**Goal:** Get Next.js running with basic Frappe API integration

### Week 1-2: Project Initialization

#### BLK-MVP-01: Initialize Next.js 14 Project (MINIMAL)
**Priority:** Critical
**Estimate:** 1 day
**Labels:** `mvp`, `setup`, `month-1`

**Description:**
Basic Next.js setup - NO Turborepo (keep it simple for MVP)

**Acceptance Criteria:**
- [ ] Next.js 14 with App Router
- [ ] TypeScript + Tailwind CSS
- [ ] Basic folder structure
- [ ] Dev server runs

**Technical Notes:**
```bash
npx create-next-app@latest blkshp-mvp --typescript --tailwind --app
```

**SKIP for MVP:**
- ❌ No Turborepo (single app is fine)
- ❌ No monorepo complexity
- ❌ No separate packages

---

#### BLK-MVP-02: Configure Tooling (MINIMAL)
**Priority:** High
**Estimate:** 0.5 days
**Labels:** `mvp`, `setup`, `month-1`

**Description:**
Minimal dev tooling

**Acceptance Criteria:**
- [ ] ESLint configured
- [ ] Prettier configured
- [ ] Basic shadcn/ui setup (just install, use as needed)

**SKIP for MVP:**
- ❌ No pre-commit hooks (overkill for MVP)
- ❌ No extensive linting rules

---

#### BLK-52: Configure Development Tooling
**Priority:** High
**Estimate:** 1 day
**Labels:** `frontend`, `tooling`, `q1-month-1`
**Depends on:** BLK-51

**Description:**
Set up ESLint, Prettier, and development tooling for code quality.

**Acceptance Criteria:**
- [ ] ESLint configured with Next.js rules
- [ ] Prettier configured with consistent formatting
- [ ] Pre-commit hooks with Husky
- [ ] VS Code workspace settings
- [ ] `.editorconfig` for consistent editor settings
- [ ] npm scripts for linting and formatting

---

#### BLK-53: Set Up Tailwind CSS + shadcn/ui
**Priority:** Critical
**Estimate:** 2 days
**Labels:** `frontend`, `ui`, `design-system`, `q1-month-1`
**Depends on:** BLK-51

**Description:**
Configure Tailwind CSS and initialize shadcn/ui component library.

**Acceptance Criteria:**
- [ ] Tailwind CSS v3 configured
- [ ] Design tokens defined (colors, typography, spacing)
- [ ] shadcn/ui initialized in `packages/ui`
- [ ] Base components installed (Button, Input, Card, etc.)
- [ ] Dark mode support configured
- [ ] Component library documented

**Design Tokens:**
- Primary color: BLKSHP brand blue
- Typography: Inter or similar modern sans-serif
- Spacing scale: Tailwind default (modified as needed)

---

#### BLK-54: Deploy to Vercel Staging
**Priority:** High
**Estimate:** 1 day
**Labels:** `frontend`, `deployment`, `q1-month-1`
**Depends on:** BLK-51

**Description:**
Set up Vercel deployment for staging environment.

**Acceptance Criteria:**
- [ ] Vercel project created
- [ ] Automatic deployments on git push
- [ ] Environment variables configured
- [ ] Staging URL accessible
- [ ] Preview deployments for PRs working
- [ ] Build and deploy time < 2 minutes

**Environment Variables:**
```
NEXT_PUBLIC_FRAPPE_API_URL=https://staging.blkshp.io
NEXTAUTH_URL=https://staging-web.blkshp.io
NEXTAUTH_SECRET=<secret>
```

---

### Week 3-4: Frappe Integration Layer

#### BLK-55: Build Frappe API TypeScript SDK (Core)
**Priority:** Critical
**Estimate:** 5 days
**Labels:** `frontend`, `api-client`, `q1-month-1`
**Depends on:** BLK-51

**Description:**
Create a TypeScript SDK for interacting with Frappe REST APIs with full type safety.

**Acceptance Criteria:**
- [ ] Base client class with authentication handling
- [ ] Request/response type definitions
- [ ] Error handling and retry logic
- [ ] TypeScript interfaces for all API responses
- [ ] Request interceptors for auth tokens
- [ ] Response interceptors for error handling
- [ ] Unit tests (80%+ coverage)
- [ ] API documentation

**API Coverage:**
- Authentication endpoints (6 endpoints)
- Product endpoints (subset of 17 inventory endpoints)
- Department endpoints
- Error response types

**Technical Approach:**
```typescript
// packages/frappe-sdk/src/client.ts
export class FrappeClient {
  constructor(baseURL: string, options?: ClientOptions)

  // Auth
  async login(username: string, password: string): Promise<LoginResponse>
  async refresh(refreshToken: string): Promise<RefreshResponse>
  async profile(): Promise<UserProfile>

  // Products
  async getProducts(params?: ProductQuery): Promise<Product[]>
  async getProduct(id: string): Promise<Product>
  async createProduct(data: ProductInput): Promise<Product>
  // ...
}
```

---

#### BLK-56: Implement React Query Integration
**Priority:** Critical
**Estimate:** 3 days
**Labels:** `frontend`, `state-management`, `q1-month-1`
**Depends on:** BLK-55

**Description:**
Set up React Query (TanStack Query) for data fetching, caching, and state management.

**Acceptance Criteria:**
- [ ] React Query configured with appropriate defaults
- [ ] Custom hooks for common queries
- [ ] Cache invalidation strategies defined
- [ ] Loading and error states handled
- [ ] Optimistic updates implemented
- [ ] Query key factory for consistency
- [ ] DevTools configured for development

**Custom Hooks:**
```typescript
// apps/web/lib/hooks/useProducts.ts
export function useProducts(query?: ProductQuery) {
  return useQuery({
    queryKey: ['products', query],
    queryFn: () => frappeClient.getProducts(query),
    staleTime: 5 * 60 * 1000, // 5 minutes
  })
}

export function useCreateProduct() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: (data: ProductInput) => frappeClient.createProduct(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['products'] })
    }
  })
}
```

---

#### BLK-57: Create API Error Handling System
**Priority:** High
**Estimate:** 2 days
**Labels:** `frontend`, `error-handling`, `q1-month-1`
**Depends on:** BLK-55

**Description:**
Build centralized error handling for API errors with user-friendly messages.

**Acceptance Criteria:**
- [ ] Error boundary components
- [ ] Toast notification system for errors
- [ ] Error code to user message mapping
- [ ] Network error handling
- [ ] Authentication error handling (401/403)
- [ ] Retry logic for transient failures
- [ ] Error logging to monitoring service

---

#### BLK-58: Set Up API Proxy for CORS
**Priority:** Medium
**Estimate:** 1 day
**Labels:** `frontend`, `infrastructure`, `q1-month-1`
**Depends on:** BLK-55

**Description:**
Configure API proxy in Next.js to handle CORS issues during development.

**Acceptance Criteria:**
- [ ] Next.js rewrites configured for API routes
- [ ] CORS headers handled correctly
- [ ] Rate limiting configured
- [ ] Request/response logging
- [ ] Works in both development and production

**next.config.js:**
```javascript
module.exports = {
  async rewrites() {
    return [
      {
        source: '/api/frappe/:path*',
        destination: process.env.FRAPPE_API_URL + '/:path*'
      }
    ]
  }
}
```

---

## MONTH 2: Authentication & Navigation

### Week 5-6: Authentication Bridge

#### BLK-59: Set Up NextAuth.js v5
**Priority:** Critical
**Estimate:** 3 days
**Labels:** `frontend`, `authentication`, `q1-month-2`
**Depends on:** BLK-55

**Description:**
Configure NextAuth.js v5 (Auth.js) to integrate with Frappe JWT authentication.

**Acceptance Criteria:**
- [ ] NextAuth.js v5 installed and configured
- [ ] Custom provider for Frappe JWT
- [ ] Session handling configured
- [ ] Refresh token rotation implemented
- [ ] Session persistence (cookies)
- [ ] Type-safe session access
- [ ] Middleware for protected routes

**Custom Provider:**
```typescript
// apps/web/auth.ts
import NextAuth from "next-auth"
import Credentials from "next-auth/providers/credentials"

export const { handlers, auth, signIn, signOut } = NextAuth({
  providers: [
    Credentials({
      credentials: {
        username: { label: "Email", type: "email" },
        password: { label: "Password", type: "password" }
      },
      async authorize(credentials) {
        const response = await frappeClient.login(
          credentials.username,
          credentials.password
        )
        return {
          id: response.user.email,
          email: response.user.email,
          name: response.user.full_name,
          accessToken: response.access_token,
          refreshToken: response.refresh_token,
        }
      }
    })
  ],
  callbacks: {
    async jwt({ token, user, account }) {
      // Handle token refresh
    },
    async session({ session, token }) {
      // Attach user data to session
    }
  }
})
```

---

#### BLK-60: Build Login/Logout UI
**Priority:** Critical
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `authentication`, `q1-month-2`
**Depends on:** BLK-59

**Description:**
Create login page and logout functionality with proper UX.

**Acceptance Criteria:**
- [ ] Login page with email/password form
- [ ] Form validation with Zod
- [ ] Loading states during authentication
- [ ] Error display for failed login
- [ ] "Remember me" option
- [ ] Logout functionality
- [ ] Redirect to login for unauthenticated users
- [ ] Responsive design (mobile-friendly)

**Design:**
- Clean, centered login form
- BLKSHP branding
- "Forgot password?" link (placeholder for future)
- Auto-focus on email field

---

#### BLK-61: Implement Session Management
**Priority:** High
**Estimate:** 2 days
**Labels:** `frontend`, `authentication`, `q1-month-2`
**Depends on:** BLK-59

**Description:**
Handle session persistence, refresh tokens, and auto-logout.

**Acceptance Criteria:**
- [ ] Session persisted across page reloads
- [ ] Automatic token refresh before expiry
- [ ] Auto-logout on session expiry
- [ ] "Session expired" notification
- [ ] Concurrent tab handling
- [ ] Secure cookie configuration

---

#### BLK-62: Create Protected Route Middleware
**Priority:** Critical
**Estimate:** 2 days
**Labels:** `frontend`, `authentication`, `q1-month-2`
**Depends on:** BLK-59

**Description:**
Implement middleware to protect authenticated routes.

**Acceptance Criteria:**
- [ ] Middleware redirects unauthenticated users to login
- [ ] Public routes accessible without auth
- [ ] Redirect to original destination after login
- [ ] Loading state while checking authentication
- [ ] Type-safe route protection

**Middleware:**
```typescript
// apps/web/middleware.ts
export { auth as middleware } from "@/auth"

export const config = {
  matcher: [
    '/dashboard/:path*',
    '/products/:path*',
    '/inventory/:path*',
    '/api/trpc/:path*'
  ]
}
```

---

#### BLK-63: Build User Profile Page
**Priority:** Medium
**Estimate:** 2 days
**Labels:** `frontend`, `ui`, `q1-month-2`
**Depends on:** BLK-60

**Description:**
Create user profile page showing user info and settings.

**Acceptance Criteria:**
- [ ] Display user information (name, email, image)
- [ ] Show companies and roles
- [ ] Account settings section
- [ ] Logout button
- [ ] Avatar/profile image display
- [ ] Responsive layout

---

### Week 7-8: Core Navigation & Dashboard

#### BLK-64: Design and Build Top Navigation Bar
**Priority:** Critical
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `navigation`, `q1-month-2`
**Depends on:** BLK-53

**Description:**
Create responsive top navigation bar with logo, search, and user menu.

**Acceptance Criteria:**
- [ ] BLKSHP logo linking to home
- [ ] Global search bar (placeholder for future)
- [ ] Notifications icon (placeholder)
- [ ] User menu dropdown
  - Profile link
  - Settings link
  - Logout option
- [ ] Responsive design (hamburger menu on mobile)
- [ ] Sticky header on scroll
- [ ] Accessible (ARIA labels, keyboard navigation)

---

#### BLK-65: Build Sidebar Navigation
**Priority:** Critical
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `navigation`, `q1-month-2`
**Depends on:** BLK-53

**Description:**
Create collapsible sidebar with module navigation.

**Acceptance Criteria:**
- [ ] Module sections (Products, Inventory, Reports)
- [ ] Active route highlighting
- [ ] Collapsible/expandable sections
- [ ] Icons for each module
- [ ] Collapse/expand sidebar
- [ ] Mobile drawer navigation
- [ ] Permission-based menu items
- [ ] Smooth animations

**Menu Structure:**
```
Dashboard
Products
  - Products List
  - Categories
  - Units
Inventory
  - Inventory Balance
  - Stock Ledger
  - Audits
Departments
Reports (placeholder)
Settings
```

---

#### BLK-66: Implement Breadcrumbs Component
**Priority:** Medium
**Estimate:** 1 day
**Labels:** `frontend`, `ui`, `navigation`, `q1-month-2`
**Depends on:** BLK-53

**Description:**
Build breadcrumb navigation for nested routes.

**Acceptance Criteria:**
- [ ] Automatic breadcrumb generation from routes
- [ ] Clickable breadcrumb links
- [ ] Custom breadcrumb labels
- [ ] Responsive (hide on mobile if needed)
- [ ] Accessible

---

#### BLK-67: Build Department Selector Component
**Priority:** High
**Estimate:** 2 days
**Labels:** `frontend`, `ui`, `q1-month-2`
**Depends on:** BLK-55

**Description:**
Create department selector for users with access to multiple departments.

**Acceptance Criteria:**
- [ ] Dropdown showing all accessible departments
- [ ] Current department highlighted
- [ ] Department switching updates context
- [ ] Persisted selection (localStorage)
- [ ] Loads departments from Frappe API
- [ ] Loading and error states
- [ ] "All Departments" option (if permitted)

---

#### BLK-68: Create Home Dashboard with KPI Widgets
**Priority:** High
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `dashboard`, `q1-month-2`
**Depends on:** BLK-64, BLK-65, BLK-67

**Description:**
Build dashboard page with key performance indicators pulling data from Frappe.

**Acceptance Criteria:**
- [ ] Welcome message with user name
- [ ] KPI cards showing:
  - Total products
  - Products under par
  - Recent audits
  - Pending approvals (if applicable)
- [ ] Quick actions buttons
- [ ] Recent activity feed (placeholder)
- [ ] Responsive grid layout
- [ ] Loading skeletons
- [ ] Error states

---

## MONTH 3: Products & Departments UI

### Week 9-10: Products Module UI

#### BLK-69: Build Product List View
**Priority:** Critical
**Estimate:** 4 days
**Labels:** `frontend`, `ui`, `products`, `q1-month-3`
**Depends on:** BLK-55, BLK-56

**Description:**
Create products list page with search, filters, and pagination.

**Acceptance Criteria:**
- [ ] Table/grid view of products
- [ ] Server-side search by name/code
- [ ] Filter by category
- [ ] Filter by department
- [ ] Filter by active/inactive status
- [ ] Pagination or infinite scroll
- [ ] Sort by name, code, category
- [ ] Bulk selection (for future actions)
- [ ] "Create Product" button
- [ ] Loading skeleton
- [ ] Empty state
- [ ] Responsive (card view on mobile)

**Table Columns:**
- Product Code
- Product Name
- Category
- Status (Active/Inactive)
- Primary Unit
- Actions (View, Edit, Delete)

---

#### BLK-70: Create Product Detail View
**Priority:** Critical
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `products`, `q1-month-3`
**Depends on:** BLK-69

**Description:**
Build product detail page showing all product information.

**Acceptance Criteria:**
- [ ] Product header (code, name, status)
- [ ] Product information section
  - Description
  - Category
  - Primary unit
  - Valuation rate
  - Status
- [ ] Unit conversions table
- [ ] Purchase units table
- [ ] Department allocations
  - Par levels per department
  - Storage areas
- [ ] Batch tracking settings (if enabled)
- [ ] Edit button
- [ ] Delete button (with confirmation)
- [ ] Breadcrumbs
- [ ] Loading state
- [ ] Error handling

---

#### BLK-71: Build Product Create/Edit Form
**Priority:** Critical
**Estimate:** 5 days
**Labels:** `frontend`, `ui`, `products`, `forms`, `q1-month-3`
**Depends on:** BLK-69

**Description:**
Create multi-step form for product creation and editing.

**Acceptance Criteria:**
- [ ] Multi-step wizard UI
  - Step 1: Basic information
  - Step 2: Unit conversions
  - Step 3: Department allocations
  - Step 4: Advanced settings
- [ ] Form validation with Zod
- [ ] Real-time validation feedback
- [ ] Auto-save drafts (localStorage)
- [ ] Dynamic unit conversion calculator
- [ ] Department multi-select with par levels
- [ ] Storage area selection
- [ ] Batch tracking toggle
- [ ] Form submission with loading state
- [ ] Success/error notifications
- [ ] Redirect to product detail on success
- [ ] Cancel with unsaved changes warning

**Form Fields (Step 1):**
- Product Code (auto-generated or manual)
- Product Name*
- Description
- Category*
- Primary Unit*
- Valuation Rate
- Status (Active/Inactive)

**Form Fields (Step 2):**
- Unit conversions (e.g., 1 Case = 12 Each)
- Conversion factor calculator

**Form Fields (Step 3):**
- Department selection (multi-select)
- Par levels per department
- Storage areas

---

#### BLK-72: Implement Product Search Autocomplete
**Priority:** High
**Estimate:** 2 days
**Labels:** `frontend`, `ui`, `products`, `q1-month-3`
**Depends on:** BLK-55

**Description:**
Build autocomplete search component for finding products quickly.

**Acceptance Criteria:**
- [ ] Search input with autocomplete dropdown
- [ ] Debounced API calls (300ms)
- [ ] Highlights matching text
- [ ] Keyboard navigation (up/down arrows, enter)
- [ ] Shows product code and name
- [ ] Recent searches (localStorage)
- [ ] Loading indicator
- [ ] No results message
- [ ] Reusable component

---

### Week 11-12: Departments Module UI

#### BLK-73: Build Department List View
**Priority:** High
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `departments`, `q1-month-3`
**Depends on:** BLK-55, BLK-56

**Description:**
Create departments list page with hierarchy visualization.

**Acceptance Criteria:**
- [ ] Tree view of department hierarchy
- [ ] Expand/collapse parent departments
- [ ] Search departments
- [ ] Filter by active/inactive
- [ ] "Create Department" button
- [ ] Loading skeleton
- [ ] Empty state
- [ ] Responsive design

**Display:**
- Department Code
- Department Name
- Parent Department
- Active status
- # of Products assigned
- Actions (View, Edit, Delete)

---

#### BLK-74: Create Department Detail View
**Priority:** High
**Estimate:** 2 days
**Labels:** `frontend`, `ui`, `departments`, `q1-month-3`
**Depends on:** BLK-73

**Description:**
Build department detail page showing information and allocations.

**Acceptance Criteria:**
- [ ] Department header (code, name, status)
- [ ] Department information
  - Description
  - Parent department
  - Settings (if any)
- [ ] Product allocations table
  - Products assigned to this department
  - Par levels
  - Storage areas
- [ ] User permissions section (placeholder)
- [ ] Edit button
- [ ] Delete button (with confirmation)
- [ ] Breadcrumbs

---

#### BLK-75: Build Department Management Forms
**Priority:** High
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `departments`, `forms`, `q1-month-3`
**Depends on:** BLK-73

**Description:**
Create forms for creating and editing departments.

**Acceptance Criteria:**
- [ ] Create department form
- [ ] Edit department form (same component)
- [ ] Form validation
- [ ] Parent department selector (with hierarchy)
- [ ] Settings configuration
- [ ] Form submission with loading state
- [ ] Success/error notifications
- [ ] Redirect to department detail on success

**Form Fields:**
- Department Code*
- Department Name*
- Parent Department (optional)
- Description
- Status (Active/Inactive)

---

#### BLK-76: Implement Department Hierarchy Visualization
**Priority:** Medium
**Estimate:** 3 days
**Labels:** `frontend`, `ui`, `departments`, `q1-month-3`
**Depends on:** BLK-73

**Description:**
Build tree visualization component for department hierarchy.

**Acceptance Criteria:**
- [ ] Tree diagram showing department relationships
- [ ] Expand/collapse nodes
- [ ] Zoom and pan controls
- [ ] Clickable nodes navigate to department detail
- [ ] Highlight path to selected department
- [ ] Responsive (scrollable on mobile)
- [ ] Loading state
- [ ] Empty state

**Library:** React Flow or similar tree visualization library

---

#### BLK-77: Create Reusable Department Selector
**Priority:** Medium
**Estimate:** 2 days
**Labels:** `frontend`, `ui`, `components`, `q1-month-3`
**Depends on:** BLK-55

**Description:**
Build reusable department selector component used throughout the app.

**Acceptance Criteria:**
- [ ] Single-select mode
- [ ] Multi-select mode
- [ ] Search departments
- [ ] Filter by user permissions
- [ ] Hierarchical display (show parent)
- [ ] Loading state
- [ ] Error state
- [ ] Accessible

---

## Additional Tasks

### Testing & QA

#### BLK-78: Set Up End-to-End Testing with Playwright
**Priority:** High
**Estimate:** 3 days
**Labels:** `testing`, `e2e`, `q1`

**Description:**
Configure Playwright for end-to-end testing.

**Acceptance Criteria:**
- [ ] Playwright installed and configured
- [ ] Test user authentication flow
- [ ] Test product CRUD operations
- [ ] Test department CRUD operations
- [ ] CI integration (run on PR)
- [ ] Test reports generated

---

#### BLK-79: Write Component Unit Tests
**Priority:** Medium
**Estimate:** Ongoing
**Labels:** `testing`, `unit-tests`, `q1`

**Description:**
Write Jest/Vitest unit tests for critical components.

**Acceptance Criteria:**
- [ ] 80%+ code coverage target
- [ ] Test critical user flows
- [ ] Test edge cases
- [ ] Test error states
- [ ] Mock API calls

---

### Documentation

#### BLK-80: Create Frontend Development Guide
**Priority:** Medium
**Estimate:** 2 days
**Labels:** `documentation`, `q1`

**Description:**
Document how to set up and develop the Next.js frontend.

**Acceptance Criteria:**
- [ ] Setup instructions
- [ ] Development workflow
- [ ] Code style guide
- [ ] Component library usage
- [ ] API integration patterns
- [ ] Testing guide

---

### Performance & Monitoring

#### BLK-81: Set Up Performance Monitoring
**Priority:** Medium
**Estimate:** 2 days
**Labels:** `monitoring`, `performance`, `q1`

**Description:**
Configure performance monitoring and analytics.

**Acceptance Criteria:**
- [ ] Vercel Analytics configured
- [ ] Core Web Vitals tracking
- [ ] Error monitoring (Sentry)
- [ ] User analytics (PostHog or similar)
- [ ] Performance budget defined
- [ ] Alerts configured

---

#### BLK-82: Optimize Bundle Size
**Priority:** Low
**Estimate:** 2 days
**Labels:** `performance`, `optimization`, `q1`

**Description:**
Optimize Next.js bundle size for fast load times.

**Acceptance Criteria:**
- [ ] Code splitting configured
- [ ] Dynamic imports for heavy components
- [ ] Tree shaking verified
- [ ] Bundle analyzer configured
- [ ] Image optimization configured
- [ ] Target: < 200KB initial bundle

---

## Beta Launch Preparation

#### BLK-83: Conduct Internal Testing
**Priority:** Critical
**Estimate:** 1 week
**Labels:** `qa`, `testing`, `q1-launch`

**Description:**
Comprehensive internal testing before beta launch.

**Acceptance Criteria:**
- [ ] All critical user flows tested
- [ ] Cross-browser testing (Chrome, Safari, Firefox)
- [ ] Mobile responsiveness verified
- [ ] Accessibility audit (WCAG AA)
- [ ] Performance benchmarks met
- [ ] Known issues documented

---

#### BLK-84: Beta Customer Onboarding
**Priority:** High
**Estimate:** 1 week
**Labels:** `onboarding`, `q1-launch`

**Description:**
Onboard 5-10 beta customers to the Next.js UI.

**Acceptance Criteria:**
- [ ] Beta customer accounts created
- [ ] Training materials prepared
- [ ] Onboarding calls scheduled
- [ ] Feedback collection process defined
- [ ] Support channel established (Slack/Discord)
- [ ] Usage tracking enabled

---

#### BLK-85: Production Deployment
**Priority:** Critical
**Estimate:** 2 days
**Labels:** `deployment`, `q1-launch`

**Description:**
Deploy Next.js app to production Vercel environment.

**Acceptance Criteria:**
- [ ] Production environment configured
- [ ] Environment variables set
- [ ] Custom domain configured
- [ ] SSL certificates verified
- [ ] Monitoring enabled
- [ ] Rollback plan documented
- [ ] Smoke tests passed
- [ ] Production URL accessible

---

## Success Metrics & Go/No-Go Decision (End of Q1)

After Month 3, evaluate the following metrics for the go/no-go decision on backend migration:

**Target Metrics:**
- [ ] 80%+ of beta users prefer Next.js UI over Frappe Desk
- [ ] Average page load time < 2 seconds
- [ ] NPS score > 40
- [ ] 5-10 beta customers actively using the system
- [ ] < 5 critical bugs reported
- [ ] User can complete full product/department CRUD flows

**Decision Point:**
- **GO:** Proceed with Q2 (AI features + inventory UI) and continue gradual migration
- **NO-GO:** Pivot to "frontend-only" strategy, keep Frappe backend long-term, reassess

---

## Issue Summary

**Total Issues:** 37 issues
- **Month 1:** 9 issues (BLK-50 to BLK-58)
- **Month 2:** 10 issues (BLK-59 to BLK-68)
- **Month 3:** 9 issues (BLK-69 to BLK-77)
- **Additional:** 9 issues (BLK-78 to BLK-86)

**Epic Breakdown:**
- Infrastructure & Setup: 9 issues
- Authentication: 5 issues
- Navigation: 5 issues
- Products UI: 4 issues
- Departments UI: 5 issues
- Testing & QA: 2 issues
- Documentation: 1 issue
- Performance: 2 issues
- Beta Launch: 3 issues

**Estimated Timeline:** 12 weeks (3 months)

---

## How to Create Issues in Linear

1. **Create the Epic:**
   - Title: "Next.js Frontend Foundation (Q1)"
   - Copy description from above
   - Set target date: 2026-02-16

2. **Create Issues:**
   - Copy each issue description
   - Set priority, estimate, and labels
   - Link to Epic
   - Set dependencies

3. **Organize into Projects:**
   - Create Project: "Q1 - Next.js Frontend"
   - Add all issues to project
   - Create milestones for each month

4. **Assign to Team:**
   - Assign to frontend engineers
   - Set up sprints (2-week sprints recommended)

---

*Document Created: 2025-11-16*
*Status: Ready for Linear Import*
*Owner: BLKSHP Engineering Team*
