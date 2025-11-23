# BLKSHP OS Development Strategy: MVP to Full Platform

**Status:** ✅ **ACTIVE STRATEGY** (2025-11-16)
**Approach:** Quick MVP validation → Immediate full platform rewrite
**Timeline:** 2-3 months MVP + 6-9 months full platform = 8-12 months total

---

## Executive Summary

This strategy takes a **validation-first** approach: build a minimal viable product on Frappe + Next.js to validate the concept internally, then immediately transition to building a production-grade platform on modern infrastructure.

### Two-Phase Strategy

**Phase 1: Minimal MVP (2-3 months)**
- Purpose: Internal validation and proof of concept
- Stack: Frappe backend + Next.js frontend
- Goal: Present working product to company for internal adoption decision
- Scope: Core features only (Products, Inventory, Basic Auth)

**Phase 2: Full Platform (6-9 months after MVP approval)**
- Purpose: Production-ready SaaS platform
- Stack: FastAPI + Next.js + PostgreSQL + Modern DevOps
- Goal: Scalable, AI-native, multi-tenant hospitality platform
- Scope: Complete feature set with AI, analytics, and advanced workflows

---

## Why This Approach?

### Advantages Over Gradual Migration

**✅ Faster Internal Validation (2-3 months vs 3 months)**
- Bare minimum features only
- No polish required for internal demo
- Quick go/no-go decision

**✅ Clean Architecture (No Technical Debt)**
- No gradual migration complexity
- No dual-write patterns
- No Frappe dependencies in final product

**✅ Modern Stack from Day 1 (Phase 2)**
- Built for AI/ML from ground up
- PGVector for embeddings
- FastAPI async performance
- Clerk for modern auth

**✅ Clear Decision Point**
- MVP proves concept internally
- Company commits before full investment
- Avoid building full platform if not needed

### Trade-offs

**❌ MVP Code is Throwaway**
- Next.js frontend can be reused (with modifications)
- Frappe backend work is discarded
- ~2-3 months of Frappe work won't carry forward

**❌ Longer Total Timeline**
- 2-3 months MVP + 6-9 months platform = 8-12 months
- vs. Gradual Migration: 18 months
- But much cleaner architecture at end

**❌ Two Development Cycles**
- Build MVP features twice (once on Frappe, once on FastAPI)
- Learning curve for FastAPI stack
- More context switching

---

## Phase 1: Minimal MVP (2-3 Months)

### Goal
**Present working product to company leadership for internal adoption decision**

### Success Criteria
- [ ] Leadership can log in and see their products/inventory
- [ ] Demonstrates core value proposition
- [ ] Works on mobile (basic responsiveness)
- [ ] Decision made: Adopt internally (YES/NO)

### Scope: Absolute Minimum

**Must Have:**
1. **Authentication**
   - Login/logout with Frappe JWT
   - User profile display

2. **Products Module**
   - List products with search
   - View product details
   - Create/edit products (basic form)
   - No: Multi-step wizard, no advanced features

3. **Inventory Module**
   - View current inventory balances
   - Filter by department
   - No: Audit workflows, no stock ledger

4. **Dashboard**
   - Welcome message
   - Product count
   - Low stock alerts
   - No: Charts, no advanced analytics

**Explicitly Out of Scope (Use Frappe Desk):**
- ❌ Inventory audits (use Frappe Desk)
- ❌ Department management (use Frappe Desk)
- ❌ Finance/intercompany (use Frappe Desk)
- ❌ Recipes (not needed for MVP)
- ❌ Procurement (not needed for MVP)
- ❌ AI features (Phase 2)
- ❌ Advanced reporting (Phase 2)

### Technology Stack (Phase 1 MVP)

**Frontend:**
- Next.js 14 (App Router)
- TypeScript
- Tailwind CSS
- shadcn/ui components
- React Query
- NextAuth.js (temporary - will switch to Clerk in Phase 2)

**Backend:**
- Frappe Framework v15+ (existing)
- MariaDB (existing)
- 30 REST API endpoints (already built)

**Deployment:**
- Vercel (Next.js frontend)
- Frappe Press (Frappe backend - existing)

**Timeline:** 2-3 months at 18 hours/week

---

## Phase 2: Full Platform (6-9 Months After MVP Approval)

### Goal
**Build production-ready, AI-native, multi-tenant SaaS platform**

### Success Criteria
- [ ] 100+ concurrent users supported
- [ ] Multi-tenant with data isolation
- [ ] AI features operational (invoice OCR, demand forecasting)
- [ ] Complete RBAC system
- [ ] Mobile apps (React Native - optional)
- [ ] First paying external customers

### Complete Technology Stack

#### Backend - FastAPI

**Core Framework:**
- **FastAPI** - Modern async Python framework
- **Python 3.11+** - Latest Python with performance improvements
- **Uvicorn** - ASGI server
- **SQLAlchemy 2.0** - Modern ORM with async support
- **Pydantic v2** - Data validation and settings

**Database:**
- **PostgreSQL 16+** - Primary database
- **PGVector** - Vector embeddings for AI/semantic search
- **PostgreSQL Full-Text Search** - Built-in search
- **Schema-per-tenant** - Multi-tenancy strategy

**Caching & Queue:**
- **Valkey** - Redis fork (drop-in replacement)
- **BullMQ** - Robust queue system for complex workflows

**Storage:**
- **MinIO** - S3-compatible object storage
- **Local filesystem** - Development/small deployments

#### Frontend - Next.js

**Core Framework:**
- **Next.js 14+** - React framework with App Router
- **TypeScript** - Type safety
- **React 18** - Latest React with concurrent features

**UI & Styling:**
- **Tailwind CSS** - Utility-first CSS
- **shadcn/ui** - Component library
- **Radix UI** - Headless components
- **Framer Motion** - Animations

**State Management:**
- **React Query (TanStack Query)** - Server state
- **Zustand** - Client state
- **React Hook Form** - Form management
- **Zod** - Schema validation

**API Layer:**
- **tRPC** - Type-safe API calls (optional)
- **Axios** - HTTP client (alternative)
- **SWR** - Alternative to React Query (if preferred)

#### Authentication & Authorization

**Authentication:**
- **Clerk** - Modern auth platform
  - Social logins (Google, Microsoft, Apple)
  - MFA/2FA built-in
  - User management UI
  - Session management
  - Passwordless options

**Authorization:**
- **Custom RBAC System**
  - Role-based access control
  - Permission-based access control
  - Department/company-level access
  - Resource-level permissions
  - Policy engine for complex rules

**RBAC Architecture:**
```
User → Roles → Permissions → Resources
     → Companies → Departments → Products/Inventory
```

#### AI & Machine Learning

**LLM APIs:**
- **OpenAI GPT-4** - Primary LLM for chat, reasoning
- **Anthropic Claude** - Alternative LLM, document analysis
- **Google Gemini** - Multi-modal capabilities

**Vector Database:**
- **PGVector** - PostgreSQL extension for embeddings
- Semantic search over products, recipes, documents
- RAG (Retrieval Augmented Generation) for AI chat

**AI Features:**
- Invoice OCR (OpenAI Vision API)
- Fuzzy product matching (RapidFuzz + embeddings)
- Demand forecasting (Prophet + custom models)
- Natural language queries (LangChain)
- Recipe optimization
- Waste prediction

#### DevOps & Infrastructure

**Reverse Proxy:**
- **Caddy** - Modern reverse proxy with automatic HTTPS
- Alternative: Nginx (if needed)

**Process Management:**
- **PM2** - Process manager for Node.js services
- **Systemd** - System-level process management
- **Docker** - Containerization (optional)

**Monitoring:**
- **Grafana** - Dashboards and visualization
- **Prometheus** - Metrics collection
- **NetData** - Real-time performance monitoring
- **Uptime Kuma** - Uptime monitoring

**Error Tracking:**
- **GlitchTip** - Self-hosted Sentry alternative
- Error aggregation and alerting

**Analytics:**
- **PostHog** - Product analytics (self-hosted option)
- **Umami** - Privacy-focused web analytics
- Feature usage tracking
- User behavior analysis

#### Communication & Notifications

**Email:**
- **Resend** - Modern email API
- **MJML** - Responsive email templates
- Transactional emails
- Email notifications

**Notifications:**
- **Apprise** - Universal notification system
  - Slack, Discord, SMS, Push notifications
  - Email, webhooks
  - Multi-channel notification delivery

#### Business Intelligence & Reporting

**BI Platform:**
- **Apache Superset** - Modern BI platform
  - Self-service analytics
  - SQL Lab for ad-hoc queries
  - Dashboard builder
  - Charts and visualizations

**PDF Generation:**
- **Gotenberg** - PDF generation service
  - HTML to PDF
  - Reports, invoices, statements
  - Custom templates

#### Developer Tools

**Documentation:**
- **Nextra** - Next.js-based documentation
  - Developer docs
  - API reference
  - User guides

**Feature Flags:**
- **Unleash** - Feature flag platform
  - Gradual rollouts
  - A/B testing
  - Kill switches
  - Environment-specific features

**Image Processing:**
- **Pillow** - Python image library
- **ImageMagick** - Advanced image processing
  - Image resizing, optimization
  - Thumbnail generation
  - Format conversion

#### Database & ORM

**SQLAlchemy 2.0 Patterns:**
```python
# Modern async patterns
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Product(Base):
    __tablename__ = "products"
    __table_args__ = {"schema": "tenant_acme"}  # Schema per tenant

    id: Mapped[int] = mapped_column(primary_key=True)
    product_code: Mapped[str] = mapped_column(String(50), unique=True)
    product_name: Mapped[str]
    # ... fields
```

**Multi-Tenancy Strategy:**
- Schema per tenant (PostgreSQL schemas)
- Tenant resolution via middleware
- Isolated data with shared infrastructure
- Tenant-specific migrations

---

## Architecture Comparison

### Phase 1: MVP Architecture
```
[Browser] → [Next.js on Vercel] → [Frappe APIs] → [MariaDB]
                                        ↓
                                 [Frappe Desk]
                                 (for admin)
```

### Phase 2: Full Platform Architecture
```
[Browser/Mobile] → [Caddy]
                      ↓
         ┌────────────┴────────────┐
         ↓                         ↓
    [Next.js]                 [FastAPI]
         ↓                         ↓
    [Static Files]           [SQLAlchemy]
                                  ↓
                    ┌─────────────┴──────────────┐
                    ↓                            ↓
              [PostgreSQL]                   [Valkey]
              + PGVector                     (Redis)
                    ↓                            ↓
              [Full-Text Search]           [BullMQ]
                                               ↓
                                          [AI Workers]
                                               ↓
                                    [OpenAI/Claude/Gemini]

[MinIO] ← [File Storage]
[Clerk] ← [Authentication]
[Apprise] ← [Notifications]
[GlitchTip] ← [Error Tracking]
[Grafana/Prometheus] ← [Monitoring]
[PostHog] ← [Analytics]
```

---

## RBAC System Design (Phase 2)

### Custom RBAC vs. Frappe Permissions

**Why Custom RBAC?**
- Frappe's permission system is tightly coupled to DocTypes
- Need flexible, resource-level permissions
- Multi-tenancy with company/department isolation
- API-first (not DocType-driven)
- Fine-grained action permissions

### RBAC Schema Design

```python
# models/rbac.py
class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]  # e.g., "Inventory Manager"
    description: Mapped[str]
    company_id: Mapped[int | None]  # Company-specific role (or global)

class Permission(Base):
    __tablename__ = "permissions"

    id: Mapped[int] = mapped_column(primary_key=True)
    resource: Mapped[str]  # e.g., "products", "inventory"
    action: Mapped[str]    # e.g., "create", "read", "update", "delete"
    scope: Mapped[str]     # e.g., "own", "department", "company", "all"

class RolePermission(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[int]
    permission_id: Mapped[int]
    conditions: Mapped[dict | None]  # JSON field for complex rules

class UserRole(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[str]  # Clerk user ID
    role_id: Mapped[int]
    company_id: Mapped[int | None]
    department_id: Mapped[int | None]

class DepartmentAccess(Base):
    __tablename__ = "department_access"

    user_id: Mapped[str]
    department_id: Mapped[int]
    access_level: Mapped[str]  # "read", "write", "admin"
```

### Permission Checking

```python
# services/rbac.py
class RBACService:
    async def check_permission(
        self,
        user_id: str,
        resource: str,
        action: str,
        resource_id: int | None = None,
        context: dict | None = None
    ) -> bool:
        """
        Check if user has permission for action on resource.

        Examples:
        - can_create_product = await rbac.check_permission(
              user_id, "products", "create"
          )
        - can_edit_product = await rbac.check_permission(
              user_id, "products", "update", resource_id=123
          )
        """
        # 1. Get user's roles (including company/department context)
        # 2. Get permissions for those roles
        # 3. Check scope (own, department, company, all)
        # 4. Evaluate conditions (if any)
        # 5. Return True/False
        pass

    async def filter_query_by_permissions(
        self,
        query: Select,
        user_id: str,
        resource: str
    ) -> Select:
        """
        Apply permission filters to SQLAlchemy query.

        Example:
        query = select(Product)
        filtered = await rbac.filter_query_by_permissions(
            query, user_id, "products"
        )
        # Returns only products user can see
        """
        pass
```

### FastAPI Dependency Injection

```python
# api/dependencies.py
from fastapi import Depends, HTTPException
from clerk_backend_api import Clerk

clerk = Clerk(bearer_auth=settings.CLERK_SECRET_KEY)

async def get_current_user(
    auth_header: str = Header(..., alias="Authorization")
) -> dict:
    """Verify Clerk session and return user."""
    token = auth_header.replace("Bearer ", "")
    session = await clerk.sessions.verify_session(token)
    return session.user

async def require_permission(
    resource: str,
    action: str
):
    """FastAPI dependency for permission checking."""
    async def permission_checker(
        user: dict = Depends(get_current_user),
        rbac: RBACService = Depends(get_rbac_service)
    ):
        has_permission = await rbac.check_permission(
            user["id"], resource, action
        )
        if not has_permission:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user
    return permission_checker

# Usage in routes
@router.post("/products")
async def create_product(
    product: ProductCreate,
    user: dict = Depends(require_permission("products", "create"))
):
    # User is already checked for permission
    pass
```

---

## Data Migration Strategy (Phase 1 → Phase 2)

### What Gets Migrated?

**Core Data:**
- ✅ Products (with all metadata)
- ✅ Departments (with hierarchy)
- ✅ Inventory balances
- ✅ Companies
- ✅ Users (→ Clerk)

**Workflow Data (Optional):**
- ❌ Frappe-specific DocTypes (not compatible)
- ❌ Audit logs (start fresh)
- ✅ Historical inventory transactions (if needed)

### Migration Approach

**Option 1: Fresh Start (Recommended)**
- Start Phase 2 with clean database
- Import master data only (products, departments)
- Current inventory balances as opening entries
- No historical transactions

**Option 2: Full Historical Migration**
- Export all Frappe data to JSON/CSV
- Transform to new schema
- Import into PostgreSQL
- Validate data integrity

**Recommended:** Option 1 (fresh start) unless historical data is critical

---

## Timeline Breakdown

### Phase 1: MVP (2-3 Months, 18 hrs/week)

**Month 1: Foundation (Weeks 1-4)**
- Next.js setup
- Frappe SDK (minimal)
- Basic auth
- Navigation skeleton

**Month 2: Core Features (Weeks 5-8)**
- Products list + basic CRUD
- Inventory balance view
- Dashboard with KPIs

**Month 3: Polish & Demo (Weeks 9-12)**
- Bug fixes
- Mobile responsiveness
- Internal demo preparation
- **Decision point: Go/No-Go for Phase 2**

**Total Effort:** ~216 hours (12 weeks × 18 hrs)

---

### Phase 2: Full Platform (4-6 Months After Approval)

**Solo developer at 18 hrs/week can complete in 10-12 months**
**With help/team: 4-6 months**

## Why Shorter Than Complete Rewrite?

**You're not starting from zero:**
- ✅ 40-50% of Python business logic can be ported
- ✅ Database schema concepts proven
- ✅ API endpoint patterns established
- ✅ Permission rules already defined
- ✅ You understand the domain deeply

**But you ARE rebuilding:**
- ❌ All Frappe-specific code (DocTypes, controllers, hooks)
- ❌ Permission system (Frappe → custom RBAC)
- ❌ ORM layer (Frappe ORM → SQLAlchemy)
- ❌ Framework patterns (monolithic → modular)

**Realistic Porting Estimate:**
- Core business logic: 30-40% directly portable
- Database queries: Need rewriting but patterns similar
- Validation rules: Can copy logic, different syntax
- APIs: Similar structure, different decorators

**Quarter 1 (Months 1-3): Foundation**
- PostgreSQL + FastAPI setup
- Clerk integration
- Custom RBAC system
- Multi-tenancy infrastructure
- Core API endpoints (Products, Inventory, Departments)
- Next.js frontend (rewrite from MVP)

**Quarter 2 (Months 4-6): Features**
- Complete Products & Inventory modules
- Audit workflows
- Procurement module
- Recipe module (if needed)
- AI: Invoice OCR + fuzzy matching

**Quarter 3 (Months 7-9): Advanced & Launch**
- AI: Demand forecasting
- AI: Natural language queries
- Analytics & reporting (Superset)
- Mobile app (React Native - optional)
- Beta customers
- Production deployment

**Total Effort:**
- With team: 4-6 months full-time
- Solo (18 hrs/week): 10-12 months
- You can port ~40% of existing Python logic, saving significant time

---

## Decision Points

### End of Month 2 (MVP)
**Question:** Is MVP showing enough promise?
- **YES:** Continue to Month 3 for polish
- **NO:** Pivot strategy or abandon

### End of Month 3 (MVP Complete)
**Question:** Should we build full platform?
- **YES:** Company adopts internally, proceed to Phase 2
- **NO:** Use Frappe Desk for now, revisit later

### End of Phase 2 Quarter 1
**Question:** Is architecture solid?
- **YES:** Continue to features
- **NO:** Refactor core before proceeding

### End of Phase 2 Quarter 2
**Question:** Ready for beta customers?
- **YES:** Launch beta program
- **NO:** Extend development timeline

---

## Risk Mitigation

### MVP Risks

**Risk:** MVP too basic, doesn't convince leadership
- **Mitigation:** Focus on core value prop (inventory visibility)
- **Mitigation:** Polished UI even if limited features

**Risk:** Frappe backend becomes blocker
- **Mitigation:** APIs are already built and tested
- **Mitigation:** Fallback to Frappe Desk for missing features

### Phase 2 Risks

**Risk:** Team lacks FastAPI expertise
- **Mitigation:** Training/learning period in Q1
- **Mitigation:** Start with simple features

**Risk:** Underestimate complexity of custom RBAC
- **Mitigation:** Design thoroughly in Q1
- **Mitigation:** Reuse patterns from existing systems

**Risk:** AI features harder than expected
- **Mitigation:** Use proven libraries (LangChain, OpenAI SDK)
- **Mitigation:** Start with simple AI features (OCR)

---

## Success Metrics

### Phase 1 (MVP)
- [ ] Internal demo completed
- [ ] Leadership decision made (adopt/not adopt)
- [ ] 3-5 internal users testing
- [ ] Core workflows functional

### Phase 2 (Full Platform)
- [ ] 100+ concurrent users supported
- [ ] <200ms average API response time
- [ ] 99.9% uptime
- [ ] First 10 external customers
- [ ] $50K+ MRR
- [ ] AI features reducing manual work by 50%+

---

## Technology Learning Path

### For You (Solo Developer, 18 hrs/week)

**Phase 1 (MVP):**
- ✅ Next.js (you'll learn quickly)
- ✅ TypeScript (gradual adoption)
- ✅ React Query (straightforward)
- ✅ shadcn/ui (copy-paste components)

**Phase 2 (Full Platform) - Priority Order:**

**Week 1-2: FastAPI Basics**
- FastAPI tutorial
- Async Python patterns
- Pydantic validation
- Simple CRUD endpoints

**Week 3-4: SQLAlchemy 2.0**
- Modern ORM patterns
- Async sessions
- Relationships
- Schema per tenant

**Week 5-6: PostgreSQL**
- PGVector extension
- Full-text search
- Indexing strategies
- Performance tuning

**Week 7-8: Clerk Integration**
- Clerk docs
- FastAPI middleware
- Session management
- RBAC design

**Week 9-12: DevOps Basics**
- Caddy setup
- PM2 process management
- Grafana dashboards
- GlitchTip error tracking

**Beyond:** Advanced features as needed

---

## Cost Estimates

### Phase 1 (MVP) - Infrastructure

| Service | Monthly Cost | Notes |
|---------|--------------|-------|
| Vercel Pro | $20 | Next.js hosting |
| Frappe Press | $50 | Existing backend |
| **Total** | **$70/mo** | 3 months = $210 |

### Phase 2 (Full Platform) - Infrastructure

| Service | Monthly Cost | Notes |
|---------|--------------|-------|
| PostgreSQL (Neon/Supabase) | $25-100 | Depends on scale |
| Valkey (Upstash/self-hosted) | $10-30 | Redis alternative |
| MinIO (self-hosted) | $0 | Or S3: $20-50 |
| Clerk | $25+ | Auth platform |
| Vercel Pro | $20 | Next.js hosting |
| VPS (Hetzner/DigitalOcean) | $40-80 | Backend hosting |
| OpenAI API | $50-200 | AI features |
| Resend | $10 | Email |
| Monitoring (self-hosted) | $0 | Grafana, Prometheus |
| **Total** | **$200-500/mo** | Scales with usage |

**Annual Cost:** ~$2,400-6,000 (Phase 2)

---

## Recommendation

### For Your Situation (Solo, 18 hrs/week, Internal Validation)

**Phase 1: Aggressive MVP (2 months)**
- Bare minimum to demo
- Ship by Month 2
- Decision by Week 10

**Phase 2 Decision: Depends on Company**
- If company adopts internally: Build full platform
- If company says no: Use Frappe Desk, revisit later

**Phase 2: Realistic Timeline (9 months with help)**
- Month 1-3: Foundation (you + Claude)
- Month 4-6: Features (consider hiring help)
- Month 7-9: Polish & launch

**Alternative: If you must go solo in Phase 2**
- 12-15 months (not 9) at 18 hrs/week
- Focus on absolute essentials
- Defer AI features to later

---

## Next Steps

**This Week:**
1. ✅ Review and approve this strategy
2. Create new Linear issues for MVP only (NOT full Q1-Q6)
3. Start BLK-50: Initialize Next.js project

**This Month:**
1. Build MVP foundation
2. Get first API calls working
3. Basic auth + navigation

**Month 2:**
1. Products CRUD
2. Inventory view
3. Internal demo prep

**Month 3:**
1. Company decision
2. If YES: Plan Phase 2 in detail
3. If NO: Maintain Frappe Desk

---

*Document Version: 1.0*
*Created: 2025-11-16*
*Status: ACTIVE STRATEGY*
*Owner: Eric / BLKSHP Engineering*
