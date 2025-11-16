# BLKSHP OS Refactoring Plan 2: Gradual Migration

**Strategy:** Hybrid architecture with incremental module-by-module migration
**Timeline:** 12-18 months (phased rollout)
**Goal:** Risk-mitigated transition with continuous delivery and revenue generation

---

## Executive Summary

This plan takes a pragmatic, low-risk approach to transforming BLKSHP OS into a modern SaaS platform. Instead of a complete rewrite, we'll build a Next.js frontend that initially consumes the existing Frappe backend APIs, then gradually migrate backend logic module-by-module to a modern stack.

**Key Benefits:**
- **Faster time to market:** Launch Next.js UI in Q1, start generating revenue
- **Lower risk:** Proven Frappe backend remains operational during transition
- **Continuous learning:** User feedback informs backend architecture decisions
- **Incremental investment:** Spread development cost over 18 months
- **Dual-system safety:** Run both systems in parallel during migration
- **Early AI value:** Launch AI features on hybrid architecture (Q2)

**Key Challenges:**
- Longer total timeline (12-18 months vs. 6-9 months)
- Maintaining two systems simultaneously (operational complexity)
- Potential technical debt from temporary integrations
- Team needs expertise in both Frappe and Next.js

---

## Migration Phases Overview

### **Phase 1 (Q1: Months 1-3)** - Next.js Frontend Foundation
- Next.js app consuming Frappe REST APIs
- Modern UI/UX with design system
- Authentication bridge (Frappe OAuth → NextAuth.js)
- Products, Departments, Inventory read-only interfaces
- **Deliverable:** Beautiful frontend replacing Frappe Desk for clients

### **Phase 2 (Q2: Months 4-6)** - AI Layer & Enhanced UI
- Invoice OCR + fuzzy matching (new Next.js API routes)
- Complete inventory management UI (write operations via Frappe)
- Analytics dashboard with visualizations
- Natural language query interface (alpha)
- **Deliverable:** AI-powered invoice processing + analytics

### **Phase 3 (Q3: Months 7-9)** - Backend Migration Begins
- PostgreSQL setup with schema-per-tenant
- Products module backend migration (Frappe → Next.js + Prisma)
- Departments module backend migration
- Dual-database sync during transition
- Demand forecasting MVP
- **Deliverable:** First modules running on new backend

### **Phase 4 (Q4: Months 10-12)** - Core Modules Migration
- Recipe module complete migration
- Procurement workflows migration
- Inventory module backend migration
- Cost optimization AI engine
- Natural language interface (beta)
- **Deliverable:** Majority of backend on new stack

### **Phase 5 (Q5-Q6: Months 13-18)** - Complete Transition
- POS integration migration
- Accounting/intercompany migration
- Advanced AI features (waste prediction, recipe optimization)
- Performance optimization
- Frappe backend sunset
- **Deliverable:** Full Next.js SaaS platform, Frappe deprecated

---

## Technology Stack Evolution

### **Phase 1-2: Hybrid Architecture**

**Frontend:**
- Next.js 14+ (App Router)
- TypeScript, Tailwind CSS, shadcn/ui
- React Query for data fetching
- Zustand for client state

**Backend (Existing):**
- Frappe Framework v15+
- MariaDB
- Existing DocTypes and business logic
- REST API endpoints

**Bridge Layer:**
- NextAuth.js wrapping Frappe OAuth2
- API proxy for CORS/rate limiting
- Response transformation layer

**AI Services (New):**
- Next.js API routes for OCR/matching
- OpenAI API integration
- BullMQ + Redis for job processing

### **Phase 3-4: Dual-Database Pattern**

**New Backend Stack:**
- PostgreSQL 15+ with schema-per-tenant
- Prisma ORM
- tRPC for type-safe APIs
- Next.js API routes

**Data Sync:**
- Dual-write pattern (write to both DBs)
- Read from new DB, fallback to Frappe
- Reconciliation jobs for consistency

**Gradual Cutover:**
- Feature flags to toggle data source
- Module-by-module migration
- Rollback capability

### **Phase 5-6: Final Architecture**

**Full Next.js Stack:**
- Next.js 14+ frontend + backend
- PostgreSQL + Prisma
- tRPC APIs
- Serverless functions
- Redis caching
- Vercel deployment

**Frappe Deprecated:**
- Data fully migrated
- Legacy system archived
- Historical data accessible via export

---

## Detailed Timeline (18 Months)

## QUARTER 1 (Months 1-3): Frontend Foundation

### **Month 1: Project Setup & Design System**

#### Week 1-2: Infrastructure
- [ ] Initialize Next.js 14 project (App Router)
- [ ] Set up Turborepo monorepo
  - `apps/web` - Next.js frontend
  - `apps/api` - Future tRPC API (placeholder)
  - `packages/ui` - shadcn/ui components
  - `packages/frappe-sdk` - Frappe API client
  - `packages/types` - Shared TypeScript types
- [ ] Configure TypeScript, ESLint, Prettier
- [ ] Set up Tailwind CSS + shadcn/ui
- [ ] Create design tokens (colors, typography, spacing)
- [ ] Deploy to Vercel (staging environment)

#### Week 3-4: Frappe Integration Layer
- [ ] Build Frappe API client (TypeScript SDK)
  - Products API wrapper
  - Departments API wrapper
  - Inventory API wrapper
  - Authentication helpers
- [ ] Implement API response caching (React Query)
- [ ] Create error handling and loading states
- [ ] Set up API proxy for CORS
- [ ] Document Frappe API patterns

**Deliverables:**
- Next.js app deployed to staging
- Frappe API integration tested
- Design system components library

---

### **Month 2: Authentication & Navigation**

#### Week 5-6: Authentication Bridge
- [ ] Set up NextAuth.js v5
- [ ] Integrate Frappe OAuth2 provider
  - Token exchange flow
  - Session management
  - Refresh token handling
- [ ] Build login/logout UI
- [ ] Implement session persistence
- [ ] Create protected route middleware
- [ ] Build user profile page

#### Week 7-8: Core Navigation & Dashboard
- [ ] Design and build navigation components
  - Top navigation bar
  - Sidebar with module links
  - Breadcrumbs
  - Mobile responsive menu
- [ ] Create dashboard layout
- [ ] Build department selector (multi-department users)
- [ ] Implement permission-based menu rendering
- [ ] Create home dashboard with KPI widgets (reading from Frappe)

**Deliverables:**
- Full authentication flow working
- Responsive navigation system
- Dashboard with real Frappe data

---

### **Month 3: Products & Departments UI**

#### Week 9-10: Products Module UI
- [ ] Build product list view
  - Server-side search and filters
  - Pagination
  - Category filtering
  - Department filtering
- [ ] Create product detail view
  - Product information display
  - Unit conversion calculator
  - Department allocations
  - Purchase units table
  - Storage areas
- [ ] Build product creation/edit forms
  - Multi-step wizard
  - Unit conversion setup
  - Department assignment
  - Batch tracking configuration
- [ ] Implement product search with autocomplete

#### Week 11-12: Departments Module UI
- [ ] Build department list view with hierarchy
- [ ] Create department detail view
  - Department info and settings
  - Product allocations
  - User permissions
- [ ] Build department management forms
- [ ] Implement department hierarchy visualization (tree view)
- [ ] Create department selector component (reusable)

**Deliverables:**
- Complete products management interface
- Department management interface
- Users can perform CRUD operations via Frappe backend
- **Q1 Launch:** Beta customers can use Next.js UI instead of Frappe Desk

---

## QUARTER 2 (Months 4-6): AI Features & Inventory UI

### **Month 4: Inventory Management UI**

#### Week 13-14: Inventory Balance & Audit List Views
- [ ] Build inventory balance dashboard
  - Product inventory grid (by department)
  - Low stock alerts
  - Batch expiration warnings
  - Search and filters
- [ ] Create inventory audit list view
  - Audit status indicators
  - Variance summary
  - Filter by date, department, status
- [ ] Build stock ledger view
  - Transaction history
  - Running balance display
  - Drill-down to voucher details

#### Week 15-16: Inventory Audit Workflow UI
- [ ] Build audit creation wizard
  - Department/category/product selection
  - Storage area filtering
  - Counting task generation
- [ ] Create counting task interface
  - Mobile-friendly design
  - Barcode scanning integration (future)
  - Quantity input with unit conversion
  - Real-time progress tracking
- [ ] Build variance review interface
  - Variance visualization (charts)
  - Line-by-line approval
  - Notes and adjustments
- [ ] Implement audit closing workflow
  - Confirmation dialog
  - Stock ledger preview
  - Balance update summary

**Deliverables:**
- Complete inventory management UI
- End-to-end audit workflow functional
- All operations still using Frappe backend

---

### **Month 5: AI Integration (Invoice OCR)**

#### Week 17-18: Invoice Upload & OCR Pipeline
- [ ] Set up file upload system (Vercel Blob or S3)
- [ ] Build invoice upload UI
  - Drag-and-drop interface
  - Multi-file upload
  - Upload progress indicators
- [ ] Create OCR processing service (Next.js API route)
  - OpenAI Vision API integration
  - Tesseract.js fallback
  - Structured data extraction
- [ ] Set up BullMQ + Redis for job queue
- [ ] Build job processing worker
- [ ] Create processing status dashboard

#### Week 19-20: Fuzzy Matching & Review UI
- [ ] Implement fuzzy matching service
  - RapidFuzz integration
  - Product similarity scoring
  - Vendor-based matching boost
  - Confidence thresholds
- [ ] Build invoice review interface
  - OCR extracted data display
  - Side-by-side image + data view
  - Product matching suggestions
  - Manual override controls
- [ ] Create auto-match approval flow
  - High-confidence auto-approve (>85%)
  - Low-confidence review queue
  - Batch approval actions
- [ ] Implement learning feedback loop
  - User corrections stored
  - Matching algorithm improvements

**AI Service Architecture:**
```typescript
// Next.js API route (not Frappe)
// POST /api/ai/process-invoice
export async function POST(req: Request) {
  const formData = await req.formData()
  const file = formData.get('file') as File

  // Upload to storage
  const blob = await uploadToStorage(file)

  // Queue OCR job
  const job = await invoiceQueue.add('ocr-invoice', {
    blobUrl: blob.url,
    tenantId: getCurrentTenant(),
    userId: getCurrentUser()
  })

  return Response.json({ jobId: job.id })
}

// Background worker processes OCR
// Creates draft invoice in Frappe via API
```

**Deliverables:**
- Invoice OCR system operational
- 85%+ auto-match rate
- Invoice processing time reduced by 80%
- **First AI feature live!**

---

### **Month 6: Analytics Dashboard & NL Interface (Alpha)**

#### Week 21-22: Analytics Dashboard
- [ ] Build analytics framework
  - Data aggregation utilities
  - Chart components (Recharts)
  - Date range selectors
  - Department filters
- [ ] Create inventory analytics
  - Inventory turnover metrics
  - Variance trends
  - Top movers (fast/slow)
  - Stockout frequency
- [ ] Build cost analytics
  - COGS by department
  - Recipe cost trends
  - Vendor price comparison
  - Cost variance analysis
- [ ] Implement procurement analytics
  - Purchase order volumes
  - Vendor performance
  - Lead time tracking

#### Week 23-24: Natural Language Interface (Alpha)
- [ ] Set up LangChain.js + OpenAI
- [ ] Implement basic query agent
  - Query inventory tool
  - Query reports tool
  - Date range parsing
- [ ] Build chat UI component
  - Streaming responses
  - Message history
  - Code/table rendering
- [ ] Create example prompts library
- [ ] Implement permission-aware queries
- [ ] Add usage tracking and rate limiting

**Example Queries (Alpha):**
- "Show me inventory variances this week"
- "What are my top 10 products by value?"
- "List all expired batches"
- "Show me purchase orders pending approval"

**Deliverables:**
- Comprehensive analytics dashboard
- Natural language query interface (alpha)
- Users getting AI-powered insights
- **Q2 Complete:** Revenue-generating SaaS with AI features

---

## QUARTER 3 (Months 7-9): Backend Migration Begins

### **Month 7: PostgreSQL & Multi-Tenancy Setup**

#### Week 25-26: Database Infrastructure
- [ ] Set up PostgreSQL 15+ (Neon, Supabase, or Railway)
- [ ] Design schema-per-tenant architecture
- [ ] Create Prisma schema
  - Core entities (Product, Department, etc.)
  - Multi-schema support
  - Indexes and constraints
- [ ] Build tenant provisioning system
  - Schema creation automation
  - Migration execution per schema
  - Seed data generation
- [ ] Set up tenant registry (public schema)
- [ ] Implement tenant resolution middleware

#### Week 27-28: Data Migration Framework
- [ ] Build ETL framework
  - Frappe API data extraction
  - Data transformation layer
  - Prisma bulk insert utilities
  - Validation and reconciliation
- [ ] Create migration CLI tool
- [ ] Implement dual-write pattern
  - Write to Frappe (primary) + Postgres (sync)
  - Conflict resolution strategy
  - Rollback mechanisms
- [ ] Build reconciliation jobs
  - Daily data consistency checks
  - Drift detection and alerts
  - Auto-correction for simple cases

**Deliverables:**
- PostgreSQL infrastructure ready
- Migration tooling operational
- Dual-write pattern tested

---

### **Month 8: Products Module Migration**

#### Week 29-30: Products Backend Migration
- [ ] Migrate Product data from Frappe to Postgres
  - Run ETL for all existing products
  - Validate data integrity
  - Reconcile discrepancies
- [ ] Build Products API (tRPC routes)
  - CRUD operations
  - Search and filtering
  - Unit conversion services
  - Department allocation
- [ ] Implement dual-database read strategy
  - Feature flag: `products.useNewBackend`
  - Read from Postgres, fallback to Frappe
  - Performance comparison logging
- [ ] Test with pilot customers (internal/beta)
- [ ] Monitor performance and errors
- [ ] Gradually increase traffic to new backend (10% → 50% → 100%)

#### Week 31-32: Products Write Operations
- [ ] Migrate write operations to new backend
  - Create/update/delete products
  - Dual-write to both databases
  - Verify synchronization
- [ ] Build admin UI for backend toggle
- [ ] Create rollback procedures
- [ ] Performance optimization
  - Query analysis
  - Index optimization
  - Caching strategy
- [ ] **Cutover:** Products module 100% on new backend

**Deliverables:**
- Products module fully migrated
- Frappe products marked read-only (fallback only)
- Performance metrics showing <200ms avg response time

---

### **Month 9: Departments & Demand Forecasting**

#### Week 33-34: Departments Backend Migration
- [ ] Migrate Department data to Postgres
- [ ] Build Departments API (tRPC)
  - CRUD operations
  - Hierarchy queries
  - Settings management
  - Permission queries
- [ ] Implement department permission system (new backend)
- [ ] Dual-write pattern for departments
- [ ] Gradual cutover (same strategy as Products)
- [ ] **Cutover:** Departments module 100% on new backend

#### Week 35-36: Demand Forecasting AI (MVP)
- [ ] Build Python microservice (FastAPI)
- [ ] Implement Prophet time series model
- [ ] Create forecasting API endpoint
- [ ] Integrate with Next.js frontend
- [ ] Build forecast visualization UI
  - Historical data + predictions
  - Confidence intervals
  - Recommended par levels
- [ ] Add forecast-based ordering suggestions

**Deliverables:**
- Departments module migrated
- Demand forecasting AI operational
- Users seeing ML-powered par level recommendations
- **Q3 Complete:** Core data models on new backend + 2 AI features live

---

## QUARTER 4 (Months 10-12): Recipe, Procurement, Inventory Migration

### **Month 10: Recipe Module Migration**

#### Week 37-38: Recipe Backend Migration
- [ ] Migrate Recipe data to Postgres
  - Recipes
  - Recipe ingredients (products + sub-recipes)
  - Allergens and inheritance
  - Recipe batches
- [ ] Build Recipes API (tRPC)
  - CRUD operations
  - Nested recipe support
  - Cost calculation service
  - Allergen inheritance logic
- [ ] Migrate recipe costing logic
- [ ] Dual-write and gradual cutover
- [ ] **Cutover:** Recipes 100% on new backend

#### Week 39-40: Recipe AI Enhancements
- [ ] Build recipe cost trend analysis
- [ ] Implement ingredient substitution suggestions
  - Based on cost
  - Based on availability
  - Allergen-safe alternatives
- [ ] Create recipe optimization dashboard
- [ ] Add "recipe cost spike" alerts

**Deliverables:**
- Recipe module fully migrated
- AI-powered recipe cost insights

---

### **Month 11: Procurement Module Migration**

#### Week 41-42: Procurement Backend Migration
- [ ] Migrate Vendor data to Postgres
- [ ] Build Purchase Order system (new backend)
  - PO creation and approval
  - Receiving workflow
  - Invoice matching
- [ ] Implement vendor management API
- [ ] Build procurement workflows
- [ ] Integrate invoice OCR (already built in Q2)
  - Auto-create POs from invoices
  - Match invoices to existing POs
- [ ] Dual-write and cutover

#### Week 43-44: Cost Optimization AI Engine
- [ ] Build vendor price comparison engine
- [ ] Implement cost variance detection
  - Unusual price spike alerts
  - Historical price trend analysis
- [ ] Create vendor performance scoring
  - Price competitiveness
  - On-time delivery
  - Quality ratings
- [ ] Build cost optimization recommendations
  - Vendor switching suggestions
  - Bulk ordering opportunities
  - Contract renegotiation alerts

**Deliverables:**
- Procurement module migrated
- Cost optimization AI delivering vendor insights
- Users saving money through AI recommendations

---

### **Month 12: Inventory Module Migration**

#### Week 45-46: Inventory Backend Migration
- [ ] Migrate Inventory Balance data
- [ ] Migrate Stock Ledger Entry (complete history)
- [ ] Migrate Batch Number data
- [ ] Build Inventory API (tRPC)
  - Balance queries
  - Stock ledger entries
  - Audit workflows
- [ ] Implement inventory valuation logic
  - Moving average costing
  - FIFO support
  - Manual valuation
- [ ] Dual-write and cutover

#### Week 47-48: Natural Language Interface (Beta)
- [ ] Expand LangChain agent tools
  - Create purchase order tool
  - Run inventory audit tool
  - Generate reports tool
  - Update product tool
- [ ] Implement permission-aware function execution
- [ ] Build conversational context management
- [ ] Create onboarding tutorial
- [ ] Add voice input support (optional)
- [ ] Beta release to all customers

**Advanced NL Capabilities (Beta):**
```
User: "Create a PO for all vegetables under par from Sysco"
AI: [Calculates theoretical inventory, identifies 12 products under par,
     filters by category=Vegetable and vendor_preference=Sysco,
     drafts PO for $1,245.50]
    "I've created PO #PO-2025-042 for 12 vegetable items from Sysco
     totaling $1,245.50. Would you like to review before submitting?"

User: "Yes, show me"
AI: [Displays PO line items in table]

User: "Remove the tomatoes and submit"
AI: [Removes tomato line items, recalculates total]
    "Updated PO total is $1,087.20. Submitting now..."
    [Creates PO in system]
    "✅ PO #PO-2025-042 submitted successfully."
```

**Deliverables:**
- Inventory module fully migrated
- Natural language interface (beta) with action capabilities
- **Q4 Complete:** All core modules on new backend, advanced AI operational

---

## QUARTER 5-6 (Months 13-18): Complete Transition & Advanced Features

### **Month 13-14: POS Integration Migration**

#### Weeks 49-52: POS Module
- [ ] Design POS integration architecture (new backend)
- [ ] Build POS configuration system
- [ ] Implement sales import service
  - Polling-based import
  - File-based import (CSV, JSON)
  - API-based import (webhooks)
- [ ] Build POS item → recipe mapping
- [ ] Implement automated depletion calculation
  - Recipe-based ingredient depletion
  - Department allocation
  - Stock ledger entry generation
- [ ] Create POS sales dashboard
- [ ] Build recipe-to-sales analysis

#### Weeks 53-56: Accounting Foundation
- [ ] Migrate Account data (Chart of Accounts)
- [ ] Build Journal Entry system
- [ ] Implement GL posting logic
- [ ] Create accounting reports foundation

**Deliverables:**
- POS integration operational
- Sales data driving automated depletions

---

### **Month 15-16: Intercompany & Advanced AI**

#### Weeks 57-60: Intercompany Automation
- [ ] Migrate Company and Company Group data
- [ ] Build intercompany transaction engine
  - Automatic JE generation
  - Dual-posting on submit
  - Intercompany account consolidation
- [ ] Implement settlement tracking
- [ ] Create intercompany reconciliation reports

#### Weeks 61-64: Advanced AI Features
- [ ] **Waste Prediction AI**
  - Predict batch expirations likely to waste
  - Suggest promotional menu items to deplete
  - Optimize ordering to reduce waste
- [ ] **Recipe Optimization AI**
  - Suggest recipe modifications for cost savings
  - Portion size optimization
  - Seasonal ingredient substitutions
- [ ] **Smart Alerts System**
  - Anomaly detection (unusual usage, price spikes)
  - Predictive stockout warnings
  - Margin erosion alerts

**Deliverables:**
- Intercompany transactions automated
- Advanced AI features reducing waste and costs

---

### **Month 17-18: Production Hardening & Frappe Sunset**

#### Weeks 65-68: Production Optimization
- [ ] Performance optimization
  - Database query tuning
  - API response time optimization
  - Frontend bundle size reduction
  - CDN configuration
- [ ] Security hardening
  - Penetration testing
  - OWASP compliance review
  - Secrets rotation
  - Audit log review
- [ ] Scalability improvements
  - Connection pooling
  - Caching strategy refinement
  - Rate limiting tuning

#### Weeks 69-72: Frappe Sunset & Final Cutover
- [ ] Migrate remaining edge cases
- [ ] Final data reconciliation
- [ ] Shut down dual-write system
- [ ] Archive Frappe data (compliance retention)
- [ ] **Turn off Frappe backend** 🎉
- [ ] Monitor for issues
- [ ] Document lessons learned
- [ ] Celebrate! 🚀

**Deliverables:**
- Full Next.js SaaS platform operational
- Frappe system deprecated
- All customers migrated successfully
- **Mission Complete!**

---

## Hybrid Architecture Patterns

### **Dual-Write Pattern (Months 7-17)**

```typescript
// During migration, write to both databases
async function createProduct(data: ProductInput) {
  const tenantId = getCurrentTenant()

  // Write to new backend (Prisma)
  const prismaProduct = await withTenant(tenantId, async (prisma) => {
    return await prisma.product.create({ data })
  })

  // Write to old backend (Frappe) - keep in sync
  try {
    await frappeClient.createDoc('Product', {
      product_code: data.productCode,
      product_name: data.productName,
      // ... map fields
    })
  } catch (error) {
    // Log sync failure but don't fail request
    logger.error('Frappe sync failed', { error, productId: prismaProduct.id })
    // Queue retry job
    await syncQueue.add('sync-product', { productId: prismaProduct.id })
  }

  return prismaProduct
}
```

### **Feature Flag Strategy**

```typescript
// Gradual cutover with feature flags
async function getProduct(productId: string) {
  const tenantId = getCurrentTenant()

  // Check feature flag
  const useNewBackend = await featureFlag.isEnabled(
    tenantId,
    'products.useNewBackend'
  )

  if (useNewBackend) {
    // Read from Prisma
    return await prisma.product.findUnique({ where: { id: productId } })
  } else {
    // Read from Frappe (legacy)
    return await frappeClient.getDoc('Product', productId)
  }
}

// Gradual rollout: 0% → 10% → 25% → 50% → 100%
// Percentage-based rollout
const rolloutPercentage = await featureFlag.getRolloutPercentage(
  'products.useNewBackend'
)
const useNewBackend = hashTenantId(tenantId) % 100 < rolloutPercentage
```

### **Data Reconciliation Jobs**

```typescript
// Daily reconciliation job
async function reconcileProducts() {
  const tenants = await getAllActiveTenants()

  for (const tenant of tenants) {
    // Fetch from both sources
    const prismaProducts = await getPrismaProducts(tenant.id)
    const frappeProducts = await getFrappeProducts(tenant.id)

    // Compare counts
    if (prismaProducts.length !== frappeProducts.length) {
      await alertOps({
        type: 'data_drift',
        tenant: tenant.id,
        message: `Product count mismatch: Prisma=${prismaProducts.length}, Frappe=${frappeProducts.length}`
      })
    }

    // Spot check random samples
    const samples = sampleRandom(prismaProducts, 100)
    for (const prismaProduct of samples) {
      const frappeProduct = frappeProducts.find(
        f => f.product_code === prismaProduct.productCode
      )

      if (!frappeProduct) {
        await alertOps({
          type: 'missing_product',
          tenant: tenant.id,
          productId: prismaProduct.id
        })
        continue
      }

      // Check critical fields match
      if (prismaProduct.productName !== frappeProduct.product_name) {
        await alertOps({
          type: 'field_mismatch',
          tenant: tenant.id,
          productId: prismaProduct.id,
          field: 'productName'
        })
      }
    }
  }
}

// Run daily at 2 AM
cron.schedule('0 2 * * *', reconcileProducts)
```

---

## AI Implementation Strategy

### **Phase 2 (Q2): Invoice OCR on Hybrid Stack**

**Architecture:**
```
[Next.js Frontend]
       ↓ (upload invoice)
[Next.js API Route] ← OpenAI Vision API
       ↓ (OCR extracted data)
[BullMQ Worker] ← Fuzzy matching service
       ↓ (matched products)
[Frappe API] ← Create draft invoice
       ↓
[Frappe Database]
```

**Benefits:**
- AI services don't need full backend migration
- Can launch AI features early (Q2)
- Frappe handles invoice/product data integrity

---

### **Phase 3-4 (Q3-Q4): Demand Forecasting & Cost Optimization**

**Architecture:**
```
[PostgreSQL] → Historical sales data
       ↓
[Python FastAPI Service] ← Prophet ML model
       ↓ (forecast predictions)
[Next.js API] → [tRPC Routes]
       ↓
[Next.js Frontend] → Forecast visualizations
```

**Migration Timing:**
- Launch after Products & Inventory migrated (Month 9)
- Needs historical sales data in Postgres
- Python service independent of Frappe

---

### **Phase 5 (Q5-Q6): Natural Language Interface**

**Full Capabilities After Complete Migration:**
```typescript
const tools = [
  {
    name: "query_inventory",
    function: async (params) => {
      // Queries new Prisma database
      return await prisma.inventoryBalance.findMany({
        where: {
          department: params.department,
          quantity: { lt: params.minQuantity }
        },
        include: { product: true }
      })
    }
  },
  {
    name: "create_purchase_order",
    function: async (params) => {
      // Creates PO in new system
      return await prisma.purchaseOrder.create({
        data: {
          vendor: params.vendor,
          lines: params.products.map(p => ({
            productId: p.productId,
            quantity: p.quantity
          }))
        }
      })
    }
  }
  // ... more tools
]
```

**Progressive Enhancement:**
- **Month 6 (Alpha):** Read-only queries (calls Frappe APIs)
- **Month 12 (Beta):** Full CRUD actions (calls new backend)
- **Month 18 (Production):** Advanced multi-step workflows

---

## Migration Risk Mitigation

### **Rollback Procedures**

```typescript
// Every migrated module has rollback capability
async function rollbackProductsMigration(tenantId: string) {
  // Step 1: Disable new backend via feature flag
  await featureFlag.disable(tenantId, 'products.useNewBackend')

  // Step 2: Verify Frappe data is current
  const frappeProducts = await frappeClient.getDocList('Product')
  logger.info(`Frappe has ${frappeProducts.length} products`)

  // Step 3: Resume dual-write if needed
  await enableDualWrite(tenantId, 'products')

  // Step 4: Alert ops team
  await alertOps({
    type: 'rollback',
    module: 'products',
    tenant: tenantId,
    message: 'Products module rolled back to Frappe'
  })

  logger.info(`✅ Products rollback complete for tenant ${tenantId}`)
}
```

### **Data Validation Framework**

```typescript
// Automated validation runs after each migration
async function validateProductMigration(tenantId: string) {
  const issues: ValidationIssue[] = []

  // Check 1: Count match
  const prismaCount = await prisma.product.count({ where: { tenantId } })
  const frappeCount = await frappeClient.getDocCount('Product')

  if (prismaCount !== frappeCount) {
    issues.push({
      severity: 'high',
      message: `Count mismatch: Prisma=${prismaCount}, Frappe=${frappeCount}`
    })
  }

  // Check 2: Sample data integrity
  const samples = await prisma.product.findMany({ take: 100 })
  for (const sample of samples) {
    const frappeDoc = await frappeClient.getDoc('Product', sample.productCode)

    if (sample.productName !== frappeDoc.product_name) {
      issues.push({
        severity: 'high',
        productId: sample.id,
        message: `Name mismatch: "${sample.productName}" vs "${frappeDoc.product_name}"`
      })
    }

    if (Math.abs(sample.valuationRate - frappeDoc.valuation_rate) > 0.01) {
      issues.push({
        severity: 'medium',
        productId: sample.id,
        message: `Valuation rate drift: ${sample.valuationRate} vs ${frappeDoc.valuation_rate}`
      })
    }
  }

  // Check 3: Relationship integrity
  const productsWithDepts = await prisma.product.findMany({
    include: { departments: true }
  })
  for (const product of productsWithDepts) {
    if (product.departments.length === 0) {
      issues.push({
        severity: 'low',
        productId: product.id,
        message: `Product has no department allocations`
      })
    }
  }

  return {
    isValid: issues.filter(i => i.severity === 'high').length === 0,
    issues
  }
}
```

### **Performance Monitoring**

```typescript
// Compare performance before/after migration
async function compareBackendPerformance() {
  const tenantId = 'test_tenant'

  // Benchmark Frappe backend
  const frappeStart = Date.now()
  await frappeClient.getDocList('Product', { limit: 1000 })
  const frappeDuration = Date.now() - frappeStart

  // Benchmark new backend
  const prismaStart = Date.now()
  await prisma.product.findMany({ take: 1000 })
  const prismaDuration = Date.now() - prismaStart

  logger.info(`Performance comparison:
    Frappe: ${frappeDuration}ms
    Prisma: ${prismaDuration}ms
    Improvement: ${((frappeDuration - prismaDuration) / frappeDuration * 100).toFixed(1)}%
  `)

  // Track over time
  await metrics.record('backend_performance', {
    backend: 'frappe',
    duration: frappeDuration
  })
  await metrics.record('backend_performance', {
    backend: 'prisma',
    duration: prismaDuration
  })
}
```

---

## Team & Resource Requirements

### **Phase 1-2 (Months 1-6): Frontend + AI**
- **2 Full-stack Engineers** (Next.js, React, TypeScript)
  - Frontend development
  - Frappe integration
  - AI service implementation
- **1 UI/UX Designer** (part-time)
  - Design system
  - UI mockups
  - User testing
- **1 DevOps Engineer** (part-time)
  - Vercel deployment
  - Redis/BullMQ setup
  - Monitoring

**Cost:** ~$150K (6 months, blended rate $75K/engineer/year)

---

### **Phase 3-4 (Months 7-12): Backend Migration Core**
- **3 Full-stack Engineers** (add 1 for backend focus)
  - PostgreSQL/Prisma migration
  - tRPC API development
  - Dual-write implementation
  - Data reconciliation
- **1 Backend/AI Engineer** (Python)
  - Demand forecasting model
  - Cost optimization engine
- **1 QA Engineer** (part-time)
  - Migration testing
  - Data validation
  - Regression testing
- **1 DevOps Engineer** (part-time)

**Cost:** ~$200K (6 months)

---

### **Phase 5-6 (Months 13-18): Complete Migration**
- **3 Full-stack Engineers**
  - Remaining module migrations
  - Advanced AI features
  - Production hardening
- **1 Backend/AI Engineer** (Python)
- **1 QA Engineer** (part-time)
- **1 DevOps Engineer** (half-time)

**Cost:** ~$200K (6 months)

**Total Team Cost: ~$550K over 18 months**

---

### **Infrastructure Costs**

| Service | Phase 1-2 | Phase 3-4 | Phase 5-6 | Total (18mo) |
|---------|-----------|-----------|-----------|--------------|
| Vercel (Pro) | $480 | $480 | $480 | $1,440 |
| PostgreSQL (Neon/Supabase) | $0 | $600 | $1,200 | $1,800 |
| Redis (Upstash) | $240 | $240 | $240 | $720 |
| File Storage (S3/Blob) | $60 | $120 | $180 | $360 |
| OpenAI API | $300 | $600 | $1,200 | $2,100 |
| Monitoring (Sentry, etc.) | $120 | $240 | $360 | $720 |
| Frappe Press | $1,200 | $1,200 | $600 | $3,000 |
| **Subtotal** | **$2,400** | **$3,480** | **$4,260** | **$10,140** |

**Total Infrastructure: ~$10K over 18 months**

**Total Cost (Team + Infrastructure): ~$560K**

---

## Success Metrics by Phase

### **Phase 1 (Q1) - Frontend Launch**
- **User Adoption:** 80% of beta users prefer Next.js UI over Frappe Desk
- **Performance:** Page load time < 2 seconds
- **NPS:** > 40 (baseline)

### **Phase 2 (Q2) - AI Features**
- **Invoice OCR Accuracy:** > 90% field extraction accuracy
- **Product Matching:** > 85% auto-match rate
- **Time Savings:** 80% reduction in invoice entry time
- **Revenue:** First paying customers ($10K MRR)

### **Phase 3 (Q3) - Backend Migration Begins**
- **Data Consistency:** 99.99% sync accuracy between systems
- **Performance:** New backend 30%+ faster than Frappe
- **Migration Success:** Products & Departments 100% migrated with zero data loss
- **Revenue:** $30K MRR

### **Phase 4 (Q4) - Core Complete**
- **Migration Progress:** 70% of functionality on new backend
- **AI Impact:** Demand forecasting reducing stockouts by 40%
- **Cost Savings:** Users reporting 15% cost reduction from AI insights
- **Revenue:** $50K MRR

### **Phase 5-6 (Q5-Q6) - Full Platform**
- **Frappe Sunset:** 100% of customers on new backend
- **Platform Uptime:** 99.9% availability
- **Customer Retention:** > 95% monthly retention
- **Revenue:** $100K MRR
- **NPS:** > 60

---

## Key Decision Points

### **Month 3: Go/No-Go for Backend Migration**
**Decision:** Continue with gradual migration OR stick with Frappe backend indefinitely

**Criteria:**
- [ ] Next.js UI adopted by > 80% of users
- [ ] Performance meets targets (< 2s page load)
- [ ] User feedback positive (NPS > 40)
- [ ] Revenue traction ($10K+ MRR)

**If NO:** Pivot to "frontend-only" strategy, keep Frappe backend long-term

---

### **Month 9: Accelerate or Extend?**
**Decision:** Accelerate migration (more resources) OR extend timeline

**Criteria:**
- [ ] Products/Departments migration successful (99.99% accuracy)
- [ ] Performance improvements validated (30%+ faster)
- [ ] Dual-write system stable (< 0.1% sync failures)
- [ ] Revenue growth on track ($30K+ MRR)

**Options:**
- **Accelerate:** Add 2 more engineers, compress 12 months → 9 months
- **Extend:** Keep timeline, reduce risk
- **Pause:** If revenue not meeting targets, focus on growth over migration

---

### **Month 15: Frappe Sunset Date**
**Decision:** Set firm date to turn off Frappe

**Criteria:**
- [ ] All modules migrated and validated
- [ ] No critical bugs in new backend
- [ ] All customers successfully using new system
- [ ] Performance SLAs met
- [ ] Data reconciliation 100% clean

**Sunset Plan:**
- Month 16: Announce sunset to customers (2-month notice)
- Month 17: Read-only mode for Frappe
- Month 18: Turn off Frappe, archive data

---

## Advantages vs. Plan 1 (Full Rewrite)

### **Lower Risk**
- ✅ Existing Frappe backend remains operational during transition
- ✅ Rollback capability at every phase
- ✅ Revenue generation starts earlier (Q1 vs. Month 9)

### **Faster Time to Market**
- ✅ Next.js UI launched in 3 months (vs. 9 months)
- ✅ First AI feature in 6 months (vs. 7 months)
- ✅ Revenue generation during migration offsets costs

### **Continuous Learning**
- ✅ User feedback informs backend architecture decisions
- ✅ Real usage data guides optimization priorities
- ✅ A/B testing opportunities (old vs. new backend)

### **Financial Flexibility**
- ✅ Spread $560K investment over 18 months (vs. $550K in 9 months)
- ✅ Revenue partially funds development after Q2
- ✅ Can pause/adjust based on cash flow

---

## Disadvantages vs. Plan 1

### **Longer Total Timeline**
- ❌ 18 months vs. 9 months to full platform
- ❌ Frappe dependency extends to Month 17

### **Operational Complexity**
- ❌ Maintaining two systems simultaneously
- ❌ Dual-write overhead and sync management
- ❌ Team needs expertise in both Frappe and Next.js

### **Potential Technical Debt**
- ❌ Temporary integrations (Frappe API wrappers)
- ❌ Data sync logic eventually discarded
- ❌ Some rework of AI services during migration

---

## Recommended Path

### **Start with Plan 2 (Gradual Migration), with option to accelerate**

**Rationale:**
1. **De-risk the investment:** Prove market fit with Next.js UI before committing to full backend rewrite
2. **Generate revenue sooner:** Start selling in Q2 (vs. Month 9)
3. **Learn before building:** User feedback informs backend architecture
4. **Maintain flexibility:** Can pause migration if revenue stalls

**Acceleration Trigger:**
- If revenue hits $50K MRR by Month 9, add 2 engineers and compress timeline
- Target: Complete migration by Month 15 instead of Month 18

**Hybrid Approach:**
- Months 1-9: Follow Plan 2 (gradual migration)
- Month 9: Reassess based on metrics
- Months 10-15: Accelerate if metrics strong
- Months 16-18: Buffer for polish and edge cases

---

## Next Steps

1. **Assemble core team** (2 engineers + 1 designer for Phase 1)
2. **Set up development infrastructure** (repos, Vercel, staging)
3. **Begin Month 1 work** (Next.js project setup)
4. **Recruit beta customers** (5-10 for Q1 launch)
5. **Establish weekly sprint cadence**
6. **Track metrics rigorously** (inform decision points)

---

## Conclusion

The gradual migration strategy balances speed, risk, and cost. By launching a modern Next.js frontend first, we can start generating revenue and learning from users while the proven Frappe backend continues handling business logic. The phased backend migration allows us to refactor with confidence, using real production data and user feedback to guide decisions.

**Timeline Summary:**
- **Q1:** Launch Next.js UI → First customers
- **Q2:** Launch AI invoice processing → Revenue acceleration
- **Q3:** Migrate core data models → New backend foundation
- **Q4:** Migrate business logic → Majority on new stack
- **Q5-Q6:** Complete migration → Sunset Frappe → Full SaaS platform 🚀

**Investment:** $560K over 18 months
**Expected Revenue:** $100K MRR by Month 18 (breakeven in ~6 months post-launch)

This plan provides the safety of a gradual transition while maintaining the ambitious vision of a modern, AI-powered SaaS platform.

---

*Document Version: 1.0*
*Last Updated: 2025-01-15*
*Owner: BLKSHP Engineering Team*
