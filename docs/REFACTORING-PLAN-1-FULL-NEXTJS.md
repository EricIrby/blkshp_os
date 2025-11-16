# BLKSHP OS Refactoring Plan 1: Full Next.js Replacement

**Strategy:** Complete rewrite with modern Next.js stack
**Timeline:** 6-9 months
**Goal:** Feature-complete SaaS product with all AI capabilities before launch

---

## Executive Summary

This plan involves a complete architectural transformation from Frappe Framework to a modern Next.js-based SaaS platform. We'll rebuild all functionality from scratch using industry-standard tools, implement comprehensive AI features, and launch with a polished, production-ready product.

**Key Benefits:**
- Full control over data model and business logic
- Modern developer experience (TypeScript, React Server Components)
- Superior performance and scalability
- Built-in AI integration from day one
- Lower long-term infrastructure costs
- Better mobile/offline support

**Key Risks:**
- Longer time to market (6-9 months vs. 3-4 months)
- Higher upfront development cost
- Need to rebuild proven Frappe functionality
- Potential feature gaps during migration

---

## Technology Stack

### Frontend
- **Framework:** Next.js 14+ (App Router, React Server Components)
- **Language:** TypeScript 5+
- **Styling:** Tailwind CSS 3+ with shadcn/ui components
- **State Management:** Zustand + React Query (TanStack Query)
- **Forms:** React Hook Form + Zod validation
- **Charts:** Recharts or Tremor
- **Tables:** TanStack Table

### Backend
- **API Layer:** Next.js API Routes + tRPC (type-safe API)
- **Compute:** Serverless functions (Vercel Edge Functions / AWS Lambda)
- **Database:** PostgreSQL 15+ (Neon, Supabase, or Railway)
- **ORM:** Prisma 5+ (type-safe queries, migrations, multi-schema)
- **Caching:** Redis (Upstash for serverless)
- **Queue:** BullMQ + Redis for background jobs
- **Search:** Typesense or Meilisearch (full-text search)

### Authentication & Authorization
- **Auth:** NextAuth.js v5 (Auth.js)
- **Session:** JWT + database sessions
- **RBAC:** Custom role-based access control
- **MFA:** TOTP support (optional)

### AI/ML Stack
- **LLM:** OpenAI API (GPT-4 Turbo)
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector DB:** Pinecone or Supabase pgvector
- **Orchestration:** LangChain.js
- **Framework:** Vercel AI SDK
- **OCR:** Tesseract.js + OpenAI Vision API
- **ML Models:** TensorFlow.js or Python microservices (forecasting)

### Infrastructure
- **Hosting:** Vercel (frontend/edge) + Railway/Render (background workers)
- **CDN:** Vercel Edge Network
- **File Storage:** Vercel Blob or AWS S3
- **Monitoring:** Sentry (errors) + Vercel Analytics + PostHog (product analytics)
- **Logging:** Axiom or Baselime
- **Email:** Resend or SendGrid

### Development Tools
- **Monorepo:** Turborepo
- **Package Manager:** pnpm
- **Linting:** ESLint + Prettier
- **Testing:** Vitest (unit) + Playwright (E2E)
- **CI/CD:** GitHub Actions
- **Code Quality:** Husky pre-commit hooks

---

## Multi-Tenancy Architecture

### Schema-per-Tenant (Recommended)

**Design:**
```typescript
// Database URL with dynamic schema
const getDatabaseUrl = (tenantId: string) => {
  return `postgresql://user:pass@host/dbname?schema=tenant_${tenantId}`
}

// Prisma client factory
export function getPrismaClient(tenantId: string) {
  return new PrismaClient({
    datasources: {
      db: { url: getDatabaseUrl(tenantId) }
    }
  })
}

// Middleware for automatic tenant isolation
export async function withTenant<T>(
  tenantId: string,
  fn: (prisma: PrismaClient) => Promise<T>
): Promise<T> {
  const prisma = getPrismaClient(tenantId)
  try {
    return await fn(prisma)
  } finally {
    await prisma.$disconnect()
  }
}
```

**Schema Structure:**
- **Public schema:** Tenant registry, global settings, admin tables
- **Per-tenant schemas:** `tenant_001`, `tenant_002`, etc.
- Each tenant schema contains: products, inventory, recipes, users, etc.

**Benefits:**
- Strong data isolation (compliance/security)
- Easy per-customer backup/restore
- Simple data export for customer portability
- Better than database-per-tenant cost efficiency
- PostgreSQL Row-Level Security (RLS) as additional safeguard

**Schema Provisioning:**
```typescript
// On new tenant signup
async function provisionTenant(tenantId: string, companyName: string) {
  // 1. Create schema
  await prisma.$executeRaw`CREATE SCHEMA tenant_${tenantId}`

  // 2. Run migrations on new schema
  await runMigrations(tenantId)

  // 3. Seed initial data
  await seedTenantData(tenantId, companyName)

  // 4. Register in tenant registry
  await prisma.tenant.create({
    data: { id: tenantId, name: companyName, status: 'active' }
  })
}
```

---

## Data Model (Prisma Schema)

### Core Entities

```prisma
// Multi-tenant base
model Tenant {
  id            String   @id
  name          String
  subdomain     String   @unique
  customDomain  String?  @unique
  status        String   @default("active")
  plan          String   @default("foundation")
  createdAt     DateTime @default(now())
  updatedAt     DateTime @updatedAt
}

// Products (per tenant schema)
model Product {
  id                    String   @id @default(cuid())
  productCode           String   @unique
  productName           String
  productType           String   // Food, Beverage, Supply, Equipment, Other
  primaryCountUnit      String   // each, case, lb, kg, oz, etc.

  // Unit conversions
  volumeConversionUnit  String?
  volumeConversionFactor Float?
  weightConversionUnit  String?
  weightConversionFactor Float?

  // Valuation
  valuationRate         Float    @default(0)
  valuationMethod       String   @default("Moving Average")
  defaultIncomingRate   Float?

  // Batch tracking
  hasBatchNo            Boolean  @default(false)
  shelfLifeInDays       Int?

  // Properties
  isGeneric             Boolean  @default(false)
  isNonInventory        Boolean  @default(false)
  isPrepItem            Boolean  @default(false)

  category              ProductCategory? @relation(fields: [categoryId], references: [id])
  categoryId            String?

  departments           ProductDepartment[]
  inventoryBalances     InventoryBalance[]
  stockLedgerEntries    StockLedgerEntry[]
  batches               BatchNumber[]

  createdAt             DateTime @default(now())
  updatedAt             DateTime @updatedAt

  @@index([productCode])
  @@index([productType])
  @@index([categoryId])
}

// Departments
model Department {
  id                String   @id @default(cuid())
  departmentCode    String   @unique
  departmentName    String
  departmentType    String?
  company           String
  parentDepartment  Department? @relation("DepartmentHierarchy", fields: [parentId], references: [id])
  parentId          String?
  children          Department[] @relation("DepartmentHierarchy")
  isActive          Boolean  @default(true)
  settings          Json?    // Flexible settings storage

  products          ProductDepartment[]
  inventoryBalances InventoryBalance[]
  stockLedgerEntries StockLedgerEntry[]

  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt

  @@index([departmentCode])
  @@index([company])
}

// Inventory Balance (Product + Department unique)
model InventoryBalance {
  id                String   @id @default(cuid())
  product           Product  @relation(fields: [productId], references: [id])
  productId         String
  department        Department @relation(fields: [departmentId], references: [id])
  departmentId      String
  company           String
  quantity          Float    @default(0) // In primary count unit
  lastAuditDate     DateTime?
  lastTransactionDate DateTime?

  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt

  @@unique([productId, departmentId, company])
  @@index([departmentId])
  @@index([productId])
}

// Stock Ledger Entry (immutable audit trail)
model StockLedgerEntry {
  id                    String   @id @default(cuid())
  product               Product  @relation(fields: [productId], references: [id])
  productId             String
  department            Department @relation(fields: [departmentId], references: [id])
  departmentId          String
  company               String
  batch                 BatchNumber? @relation(fields: [batchId], references: [id])
  batchId               String?

  // Transaction details
  actualQty             Float    // Change in quantity
  qtyAfterTransaction   Float    // Running balance
  postingDate           DateTime
  postingTime           DateTime @default(now())
  voucherType           String   // "Inventory Audit", "Purchase Receipt", etc.
  voucherNo             String

  // Valuation
  incomingRate          Float?
  outgoingRate          Float?
  valuationRate         Float
  stockValue            Float
  stockValueDifference  Float

  createdAt             DateTime @default(now())

  @@index([productId, departmentId, postingDate])
  @@index([voucherType, voucherNo])
  @@index([batchId])
}

// Batch Number
model BatchNumber {
  id                  String   @id @default(cuid())
  batchId             String   @unique // Auto-generated
  product             Product  @relation(fields: [productId], references: [id])
  productId           String
  department          Department @relation(fields: [departmentId], references: [id])
  departmentId        String
  manufacturingDate   DateTime?
  expirationDate      DateTime?
  quantity            Float    @default(0) // Calculated from ledger
  status              String   @default("Active") // Active, Expired, Consumed

  stockLedgerEntries  StockLedgerEntry[]

  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt

  @@index([productId, departmentId])
  @@index([expirationDate])
  @@index([status])
}

// Recipe
model Recipe {
  id              String   @id @default(cuid())
  recipeName      String
  department      Department @relation(fields: [departmentId], references: [id])
  departmentId    String
  company         String
  yieldQuantity   Float
  yieldUnit       String
  totalCost       Float    @default(0)
  costPerUnit     Float    @default(0)

  ingredients     RecipeIngredient[]
  allergens       RecipeAllergen[]
  inheritedAllergens RecipeInheritedAllergen[]
  batches         RecipeBatch[]

  createdAt       DateTime @default(now())
  updatedAt       DateTime @updatedAt

  @@index([departmentId])
}

// Users & Permissions
model User {
  id                String   @id @default(cuid())
  email             String   @unique
  name              String?
  password          String   // Hashed
  role              Role     @relation(fields: [roleId], references: [id])
  roleId            String
  isActive          Boolean  @default(true)

  departmentPermissions DepartmentPermission[]

  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt
}

model Role {
  id          String   @id @default(cuid())
  roleCode    String   @unique
  roleName    String
  description String?
  isCustom    Boolean  @default(false)

  permissions RolePermission[]
  users       User[]

  createdAt   DateTime @default(now())
  updatedAt   DateTime @updatedAt
}

model RolePermission {
  id                  String  @id @default(cuid())
  role                Role    @relation(fields: [roleId], references: [id])
  roleId              String
  permissionCode      String  // "inventory.audit.run", "orders.create", etc.
  permissionCategory  String  // "Inventory", "Orders", etc.
  departmentRestricted Boolean @default(false)

  @@unique([roleId, permissionCode])
}

model DepartmentPermission {
  id            String     @id @default(cuid())
  user          User       @relation(fields: [userId], references: [id])
  userId        String
  department    Department @relation(fields: [departmentId], references: [id])
  departmentId  String
  canRead       Boolean    @default(true)
  canWrite      Boolean    @default(false)
  canCreate     Boolean    @default(false)
  canDelete     Boolean    @default(false)
  canSubmit     Boolean    @default(false)
  canCancel     Boolean    @default(false)
  canApprove    Boolean    @default(false)

  @@unique([userId, departmentId])
}

// Subscription Plans
model SubscriptionPlan {
  id                  String  @id @default(cuid())
  planCode            String  @unique
  planName            String
  description         String?
  isDefault           Boolean @default(false)
  isActive            Boolean @default(true)
  billingFrequency    String  // Monthly, Annual
  billingCurrency     String  @default("USD")
  basePrice           Float

  moduleActivations   ModuleActivation[]

  createdAt           DateTime @default(now())
  updatedAt           DateTime @updatedAt
}

model ModuleActivation {
  id                String  @id @default(cuid())
  plan              SubscriptionPlan @relation(fields: [planId], references: [id])
  planId            String
  moduleKey         String  // "core", "inventory", "procurement", etc.
  isEnabled         Boolean @default(false)
  isRequired        Boolean @default(false)

  @@unique([planId, moduleKey])
}
```

---

## Implementation Timeline (6-9 Months)

### **Month 1-2: Foundation & Authentication**

#### Weeks 1-2: Project Setup
- [x] Initialize Next.js 14 project with App Router
- [x] Set up Turborepo monorepo structure
  - `apps/web` - Next.js frontend
  - `apps/api` - tRPC API (if separate)
  - `packages/ui` - Shared UI components (shadcn/ui)
  - `packages/database` - Prisma schema and client
  - `packages/auth` - Authentication logic
  - `packages/config` - Shared configs (ESLint, TypeScript, Tailwind)
- [x] Configure TypeScript, ESLint, Prettier
- [x] Set up Tailwind CSS + shadcn/ui design system
- [x] Initialize PostgreSQL database (Neon or Supabase)
- [x] Set up Prisma with initial schema

#### Weeks 3-4: Multi-Tenancy Infrastructure
- [x] Implement schema-per-tenant architecture
- [x] Create tenant provisioning system
- [x] Build tenant registry (public schema)
- [x] Develop tenant resolution middleware (subdomain/custom domain)
- [x] Write Prisma migrations for multi-schema support
- [x] Create seed scripts for demo data

#### Weeks 5-6: Authentication System
- [x] Set up NextAuth.js v5
- [x] Implement email/password authentication
- [x] Build role-based access control (RBAC) system
- [x] Create permission checking utilities
- [x] Develop user management UI
- [x] Build role and permission management admin UI

#### Weeks 7-8: Department & Permissions Module
- [x] Migrate Department DocType to Prisma schema
- [x] Implement department hierarchy logic
- [x] Build department CRUD APIs (tRPC routes)
- [x] Create department management UI
- [x] Implement department permission assignment
- [x] Build permission checking middleware
- [x] Write unit tests for permission system

**Deliverables:**
- Working Next.js app with authentication
- Multi-tenant infrastructure operational
- Department management complete
- Design system established

---

### **Month 3-4: Core Modules**

#### Weeks 9-10: Products Module (Part 1)
- [x] Migrate Product DocType to Prisma schema
- [x] Implement unit conversion service (hub-and-spoke pattern)
- [x] Build product CRUD APIs
- [x] Create product category system
- [x] Develop product management UI
  - Product list with search/filter
  - Product detail view
  - Product creation/edit forms
- [x] Implement product-department allocation

#### Weeks 11-12: Products Module (Part 2)
- [x] Add batch tracking support (has_batch_no flag)
- [x] Implement product valuation fields
- [x] Build purchase unit management
- [x] Create storage area metadata system
- [x] Develop product tags and substitutes
- [x] Write comprehensive product tests

#### Weeks 13-14: Inventory Module (Part 1)
- [x] Migrate Inventory Balance to Prisma
- [x] Implement Stock Ledger Entry system
- [x] Build batch number tracking
- [x] Create inventory balance APIs
- [x] Develop theoretical inventory calculation service
- [x] Implement moving average costing algorithm

#### Weeks 15-16: Inventory Module (Part 2)
- [x] Build Inventory Audit workflow
- [x] Create audit line and counting task systems
- [x] Develop variance calculation logic
- [x] Build inventory audit UI
  - Create audit wizard
  - Counting task interface
  - Variance reporting
- [x] Implement Stock Ledger reports
- [x] Create inventory dashboard widgets

**Deliverables:**
- Complete products module with unit conversions
- Inventory management system operational
- Stock ledger audit trail working
- Batch tracking functional

---

### **Month 5: AI Integration (Phase 1)**

#### Weeks 17-18: Invoice OCR Pipeline
- [x] Set up OpenAI API integration
- [x] Build image upload system (Vercel Blob)
- [x] Implement OCR preprocessing (canvas/sharp)
- [x] Create Tesseract.js + OpenAI Vision dual pipeline
- [x] Build structured data extraction
- [x] Develop invoice parsing service
- [x] Create invoice review UI (human-in-loop)

#### Weeks 19-20: Fuzzy Matching Service
- [x] Implement RapidFuzz integration
- [x] Build product matching algorithm
  - Token sort ratio (word order)
  - Token set ratio (abbreviations)
  - Partial ratio (substrings)
  - Weighted scoring
- [x] Create vendor-product mapping cache
- [x] Develop confidence scoring system
- [x] Build matching review UI
- [x] Implement learning/feedback loop

**Background Job System:**
- [x] Set up BullMQ + Redis
- [x] Create invoice processing queue
- [x] Build job progress tracking
- [x] Implement retry logic
- [x] Create admin job monitoring UI

**Deliverables:**
- Invoice OCR system processing uploaded invoices
- Automatic product matching with 85%+ accuracy
- Background job processing operational
- Admin review interface for low-confidence matches

---

### **Month 6: Recipes & Advanced Features**

#### Weeks 21-22: Recipe Module
- [x] Migrate Recipe DocTypes to Prisma
- [x] Implement nested recipe support
- [x] Build recipe costing calculation
- [x] Create allergen tracking system
- [x] Implement allergen inheritance logic
- [x] Build recipe CRUD APIs
- [x] Develop recipe management UI
  - Recipe list and search
  - Recipe builder (drag-drop ingredients)
  - Cost calculation view
  - Allergen visualization

#### Weeks 23-24: Procurement & POS Foundation
- [x] Build vendor management system
- [x] Create purchase order workflows
- [x] Implement receiving process
- [x] Build invoice-to-PO matching
- [x] Create POS integration framework
- [x] Implement recipe-based depletion calculation
- [x] Build basic procurement reports

**Subscription & Billing:**
- [x] Integrate Stripe billing
- [x] Implement subscription plan management
- [x] Build feature gating system
- [x] Create billing portal
- [x] Develop usage tracking

**Deliverables:**
- Complete recipe management with costing
- Procurement workflows operational
- POS integration foundation ready
- Stripe billing integrated

---

### **Month 7: AI Integration (Phase 2)**

#### Weeks 25-26: Demand Forecasting
- [x] Set up time series data pipeline
- [x] Implement Prophet or ARIMA models (Python microservice)
- [x] Build feature engineering (seasonality, events, weather API)
- [x] Create forecasting service API
- [x] Develop par level recommendations
- [x] Build forecast visualization UI
- [x] Implement automated reorder alerts

#### Weeks 27-28: Cost Optimization Engine
- [x] Build recipe cost trend analysis
- [x] Implement vendor price comparison
- [x] Create ingredient substitution suggestions
- [x] Develop margin erosion alerts
- [x] Build cost optimization dashboard
- [x] Implement recommendation engine
- [x] Create vendor negotiation insights

**Deliverables:**
- Demand forecasting model generating accurate predictions
- Cost optimization recommendations driving savings
- Automated alerts for unusual patterns
- AI-powered insights dashboard

---

### **Month 8: Natural Language Interface & Testing**

#### Weeks 29-30: Natural Language Interface
- [x] Set up LangChain.js + OpenAI function calling
- [x] Implement natural language query parser
- [x] Build tool/function registry
  - Query tools (search, filter, aggregate)
  - Action tools (create PO, run audit, etc.)
- [x] Create conversational agent
- [x] Develop chat UI with streaming responses
- [x] Implement context management (conversation history)
- [x] Build permission-aware function execution
- [x] Create example prompts and onboarding

**Sample Capabilities:**
```
User: "Show me inventory variances over $500 this week"
AI: [Queries inventory audits, filters by variance > $500, returns table]

User: "Create a purchase order for vegetables under par"
AI: [Calculates theoretical inventory, identifies products under par,
     filters by category, drafts PO, shows for approval]

User: "What are my top cost drivers in Q1?"
AI: [Analyzes recipe costs, aggregates by ingredient category,
     visualizes top 10 with trend arrows]
```

#### Weeks 31-32: Comprehensive Testing & QA
- [x] Write E2E tests for critical flows (Playwright)
  - User signup and onboarding
  - Product creation and department assignment
  - Inventory audit workflow
  - Invoice processing end-to-end
  - Recipe creation and costing
- [x] Expand unit test coverage (target 80%+)
- [x] Perform load testing (k6)
  - Multi-tenant performance
  - Concurrent user simulation
  - Database query optimization
- [x] Security audit
  - OWASP top 10 testing
  - SQL injection prevention
  - XSS/CSRF protection
  - Authentication security
- [x] Accessibility audit (WCAG 2.1 AA)

**Deliverables:**
- Natural language interface operational
- Comprehensive test suite passing
- Performance benchmarks established
- Security vulnerabilities addressed

---

### **Month 9: Launch Preparation**

#### Weeks 33-34: Migration & Data Tools
- [x] Build Frappe-to-Prisma ETL scripts
  - Product migration
  - Department migration
  - Inventory balance migration
  - User and permission migration
  - Recipe migration
- [x] Create data validation utilities
- [x] Build rollback mechanisms
- [x] Test migration with production-like data
- [x] Document migration procedures

#### Weeks 35-36: Production Deployment & Launch
- [x] Set up production infrastructure
  - Vercel production deployment
  - PostgreSQL production database
  - Redis production instance
  - S3 bucket configuration
- [x] Configure monitoring and alerting
  - Sentry error tracking
  - Vercel Analytics
  - PostHog product analytics
  - Uptime monitoring (Better Uptime)
- [x] Implement logging and observability
- [x] Set up backup and disaster recovery
- [x] Create runbooks for common issues
- [x] Conduct security penetration testing
- [x] Perform final load testing
- [x] Launch beta to select customers
- [x] Gather feedback and iterate
- [x] Public launch preparation
  - Marketing site
  - Documentation portal
  - Support system setup
  - Pricing page
- [x] Go live! 🚀

**Deliverables:**
- Production system deployed and monitored
- Migration tools tested with real data
- Beta customers successfully onboarded
- Public launch ready

---

## AI Implementation Deep Dive

### 1. Invoice OCR + Auto-Matching Architecture

```typescript
// Invoice processing pipeline
export async function processInvoice(file: File, tenantId: string) {
  // Step 1: Upload to storage
  const blob = await uploadToStorage(file)

  // Step 2: Queue OCR job
  const job = await invoiceQueue.add('process-invoice', {
    tenantId,
    blobUrl: blob.url,
    uploadedBy: currentUser.id
  })

  return { jobId: job.id, status: 'processing' }
}

// Background worker
invoiceQueue.process('process-invoice', async (job) => {
  const { tenantId, blobUrl } = job.data

  // Step 1: OCR extraction
  const extractedData = await extractInvoiceData(blobUrl)
  /*
    Returns: {
      vendor: "Sysco Foods",
      invoiceNumber: "INV-12345",
      invoiceDate: "2025-01-15",
      lineItems: [
        { description: "Roma Tomatoes, 25 lb case", quantity: 3, unit: "case", price: 24.50 },
        { description: "Organic Chicken Breast, 10 lb box", quantity: 5, unit: "box", price: 45.00 }
      ]
    }
  */

  // Step 2: Fuzzy matching
  const matchedItems = await matchProductsToLineItems(
    extractedData.lineItems,
    tenantId
  )
  /*
    Returns: [
      {
        lineItem: "Roma Tomatoes, 25 lb case",
        matches: [
          { productId: "prod_123", productName: "Tomatoes, Roma", confidence: 0.95 },
          { productId: "prod_456", productName: "Tomato, Cherry", confidence: 0.42 }
        ],
        bestMatch: { productId: "prod_123", confidence: 0.95 }
      }
    ]
  */

  // Step 3: Auto-approve high-confidence, flag low-confidence
  const result = {
    autoMatched: matchedItems.filter(m => m.bestMatch.confidence > 0.85),
    needsReview: matchedItems.filter(m => m.bestMatch.confidence <= 0.85)
  }

  // Step 4: Create draft invoice
  await createDraftInvoice(tenantId, extractedData, result)

  // Step 5: Notify user
  await notifyUser(job.data.uploadedBy, {
    message: `Invoice processed: ${result.autoMatched.length} matched, ${result.needsReview.length} need review`
  })
})

// OCR extraction service
async function extractInvoiceData(imageUrl: string) {
  // Try OpenAI Vision first (more accurate for structured invoices)
  try {
    const response = await openai.chat.completions.create({
      model: "gpt-4-vision-preview",
      messages: [{
        role: "user",
        content: [
          { type: "text", text: INVOICE_EXTRACTION_PROMPT },
          { type: "image_url", image_url: { url: imageUrl } }
        ]
      }],
      response_format: { type: "json_object" }
    })

    return JSON.parse(response.choices[0].message.content)
  } catch (error) {
    // Fallback to Tesseract.js
    const { data: { text } } = await Tesseract.recognize(imageUrl, 'eng')
    return parseInvoiceText(text) // Regex-based extraction
  }
}

// Fuzzy matching service
async function matchProductsToLineItems(lineItems: LineItem[], tenantId: string) {
  const products = await getActiveProducts(tenantId)

  return lineItems.map(item => {
    const matches = products.map(product => ({
      productId: product.id,
      productName: product.productName,
      confidence: calculateMatchScore(item.description, product)
    }))
    .sort((a, b) => b.confidence - a.confidence)
    .slice(0, 5) // Top 5 matches

    return {
      lineItem: item.description,
      matches,
      bestMatch: matches[0]
    }
  })
}

function calculateMatchScore(invoiceDesc: string, product: Product): number {
  const fuzz = require('fuzzball')

  // Multi-criteria matching
  const scores = {
    name: fuzz.token_sort_ratio(invoiceDesc, product.productName) / 100,
    tokenSet: fuzz.token_set_ratio(invoiceDesc, product.productName) / 100,
    partial: fuzz.partial_ratio(invoiceDesc, product.productName) / 100,
    vendor: product.vendor === extractVendor(invoiceDesc) ? 0.2 : 0
  }

  // Weighted average
  return (
    scores.name * 0.4 +
    scores.tokenSet * 0.3 +
    scores.partial * 0.2 +
    scores.vendor * 0.1
  )
}
```

**Accuracy Targets:**
- OCR extraction: 90%+ field accuracy
- Product matching: 85%+ auto-match rate (confidence > 0.85)
- Human review time: 80% reduction vs. manual entry

---

### 2. Natural Language Interface

```typescript
// LangChain agent setup
import { ChatOpenAI } from "langchain/chat_models/openai"
import { AgentExecutor, createOpenAIFunctionsAgent } from "langchain/agents"
import { pull } from "langchain/hub"

const tools = [
  {
    name: "query_inventory",
    description: "Query inventory data with filters",
    parameters: {
      department: { type: "string", optional: true },
      product: { type: "string", optional: true },
      minVariance: { type: "number", optional: true }
    },
    function: async (params) => {
      return await queryInventory(currentTenant, params)
    }
  },
  {
    name: "create_purchase_order",
    description: "Create a purchase order for products",
    parameters: {
      products: { type: "array", items: { productId: "string", quantity: "number" } },
      vendor: { type: "string" }
    },
    function: async (params) => {
      // Check permissions
      if (!hasPermission(currentUser, 'orders.create')) {
        return { error: "No permission to create purchase orders" }
      }
      return await createPurchaseOrder(currentTenant, params)
    }
  },
  {
    name: "analyze_cost_drivers",
    description: "Analyze top cost drivers for a time period",
    parameters: {
      startDate: { type: "string" },
      endDate: { type: "string" },
      topN: { type: "number", default: 10 }
    },
    function: async (params) => {
      return await analyzeCostDrivers(currentTenant, params)
    }
  }
]

const llm = new ChatOpenAI({
  modelName: "gpt-4-turbo-preview",
  temperature: 0
})

const prompt = await pull("hwchase17/openai-functions-agent")
const agent = await createOpenAIFunctionsAgent({ llm, tools, prompt })
const agentExecutor = new AgentExecutor({ agent, tools })

// Chat endpoint
export async function POST(req: Request) {
  const { message, conversationHistory } = await req.json()

  const result = await agentExecutor.invoke({
    input: message,
    chat_history: conversationHistory
  })

  return Response.json({
    response: result.output,
    toolCalls: result.intermediateSteps
  })
}
```

**Example Interactions:**

```
User: "Show me all inventory items with variances over $500 this week"

Agent Process:
1. Calls query_inventory({ minVariance: 500, startDate: "2025-01-08" })
2. Formats results into table
3. Returns: "Here are 12 inventory items with variances over $500 this week:
   [Table with Product, Department, Theoretical, Actual, Variance]"

---

User: "Create a PO for vegetables under par from Sysco"

Agent Process:
1. Calls query_inventory({ category: "Vegetables", belowPar: true })
2. Filters by vendor preference = "Sysco"
3. Calls create_purchase_order({ products: [...], vendor: "Sysco" })
4. Returns: "Created PO #PO-2025-001 for 15 vegetable items from Sysco, total $1,245.50.
   Would you like to review before submitting?"

---

User: "What were my biggest cost increases last quarter?"

Agent Process:
1. Calls analyze_cost_drivers({ startDate: "2024-10-01", endDate: "2024-12-31" })
2. Compares to previous quarter
3. Returns: "Your top 5 cost increases in Q4 2024:
   1. Chicken Breast: +$2,340 (+18% vs Q3)
   2. Avocados: +$1,890 (+34% - seasonal)
   3. Dairy Products: +$1,560 (+12%)
   ..."
```

---

### 3. Demand Forecasting

```python
# Python microservice (FastAPI)
from prophet import Prophet
import pandas as pd

@app.post("/forecast")
async def forecast_demand(product_id: str, department_id: str, days: int = 30):
    # Fetch historical data
    sales = await get_sales_history(product_id, department_id)
    df = pd.DataFrame(sales, columns=['ds', 'y'])  # ds=date, y=quantity

    # Add regressors
    df['is_weekend'] = df['ds'].dt.dayofweek >= 5
    df['is_holiday'] = df['ds'].isin(get_holidays())
    df['temperature'] = await get_weather_data(df['ds'])

    # Fit model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    model.add_regressor('is_weekend')
    model.add_regressor('is_holiday')
    model.add_regressor('temperature')

    model.fit(df)

    # Forecast
    future = model.make_future_dataframe(periods=days)
    future['is_weekend'] = future['ds'].dt.dayofweek >= 5
    future['is_holiday'] = future['ds'].isin(get_holidays())
    future['temperature'] = await forecast_weather(future['ds'])

    forecast = model.predict(future)

    # Calculate recommended par levels
    recommended_par = forecast['yhat'].quantile(0.95)  # 95th percentile

    return {
        "forecast": forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict(),
        "recommended_par": recommended_par,
        "confidence_interval": [forecast['yhat_lower'].min(), forecast['yhat_upper'].max()]
    }
```

---

## Security Considerations

### Authentication & Authorization
- [ ] bcrypt password hashing (12+ rounds)
- [ ] JWT with short expiration (15 min access, 7 day refresh)
- [ ] HTTP-only, secure, SameSite cookies
- [ ] Rate limiting on auth endpoints (5 attempts/15 min)
- [ ] Account lockout after failed attempts
- [ ] Optional TOTP 2FA
- [ ] Permission checks on all API routes
- [ ] Department-based data isolation

### Data Protection
- [ ] PostgreSQL Row-Level Security (RLS) policies
- [ ] Encrypted fields for sensitive data (Prisma field-level encryption)
- [ ] TLS 1.3 for all connections
- [ ] Encrypted backups (AES-256)
- [ ] Secure file upload validation (file type, size, virus scanning)
- [ ] SQL injection prevention (Prisma parameterized queries)
- [ ] XSS protection (React auto-escaping + CSP headers)

### Infrastructure Security
- [ ] OWASP security headers (CSP, HSTS, X-Frame-Options)
- [ ] DDoS protection (Vercel/Cloudflare)
- [ ] API rate limiting (per tenant, per user)
- [ ] Secrets management (Vercel env vars / AWS Secrets Manager)
- [ ] Audit logging for all data mutations
- [ ] GDPR compliance (data export, right to be forgotten)
- [ ] SOC 2 Type II preparation

### AI Security
- [ ] Prompt injection prevention
- [ ] Function call authorization checks
- [ ] PII redaction in logs
- [ ] AI response content filtering
- [ ] Rate limiting on AI endpoints (cost control)

---

## Testing Strategy

### Unit Tests (Vitest)
```typescript
// Example: Unit conversion tests
describe('Product Unit Conversions', () => {
  it('converts from case to each correctly', () => {
    const product = createTestProduct({
      primaryCountUnit: 'each',
      purchaseUnits: [
        { unit: 'case', conversionFactor: 24 }
      ]
    })

    const result = convertToPrimaryUnit(product, 'case', 2)
    expect(result).toBe(48) // 2 cases * 24 each/case = 48 each
  })

  it('throws error for invalid unit conversion', () => {
    const product = createTestProduct({ primaryCountUnit: 'each' })

    expect(() => convertToPrimaryUnit(product, 'invalid', 1))
      .toThrow('No conversion found for unit: invalid')
  })
})

// Example: Permission tests
describe('Permission Checks', () => {
  it('allows department access with can_read permission', async () => {
    const user = await createUserWithPermissions({
      departments: [{ id: 'dept_1', canRead: true }]
    })

    const hasAccess = await checkDepartmentAccess(user, 'dept_1', 'read')
    expect(hasAccess).toBe(true)
  })

  it('denies department access without permission', async () => {
    const user = await createUserWithPermissions({
      departments: [{ id: 'dept_1', canRead: false }]
    })

    const hasAccess = await checkDepartmentAccess(user, 'dept_1', 'write')
    expect(hasAccess).toBe(false)
  })
})
```

**Coverage Target:** 80%+ for business logic, 100% for security functions

### Integration Tests (Vitest + Supertest)
```typescript
describe('Inventory Audit API', () => {
  it('creates audit and calculates variances correctly', async () => {
    // Setup
    const tenant = await createTestTenant()
    const product = await createTestProduct(tenant.id)
    await setInventoryBalance(tenant.id, product.id, 100)

    // Create audit
    const audit = await request(app)
      .post('/api/inventory/audits')
      .send({
        department: 'dept_kitchen',
        products: [{ productId: product.id, countedQty: 95 }]
      })
      .expect(201)

    // Verify variance
    expect(audit.body.lines[0].variance).toBe(-5)
    expect(audit.body.lines[0].variancePercent).toBe(-5)

    // Close audit and verify ledger
    await request(app)
      .post(`/api/inventory/audits/${audit.body.id}/close`)
      .expect(200)

    const ledgerEntries = await getStockLedgerEntries(product.id)
    expect(ledgerEntries).toHaveLength(1)
    expect(ledgerEntries[0].actualQty).toBe(-5)
  })
})
```

### E2E Tests (Playwright)
```typescript
test('complete invoice processing flow', async ({ page }) => {
  // Login
  await page.goto('/login')
  await page.fill('[name="email"]', 'test@example.com')
  await page.fill('[name="password"]', 'password')
  await page.click('button[type="submit"]')

  // Upload invoice
  await page.goto('/procurement/invoices/upload')
  await page.setInputFiles('input[type="file"]', 'test-invoice.pdf')
  await page.click('button:has-text("Process Invoice")')

  // Wait for processing
  await page.waitForSelector('text=Processing complete')

  // Verify auto-matched items
  const autoMatched = await page.locator('.auto-matched-item').count()
  expect(autoMatched).toBeGreaterThan(0)

  // Review low-confidence matches
  await page.click('.needs-review-item:first-child')
  await page.selectOption('select[name="product"]', { label: 'Tomatoes, Roma' })
  await page.click('button:has-text("Confirm Match")')

  // Submit invoice
  await page.click('button:has-text("Submit Invoice")')
  await expect(page.locator('text=Invoice submitted successfully')).toBeVisible()
})
```

### Load Testing (k6)
```javascript
import http from 'k6/http'
import { check, sleep } from 'k6'

export const options = {
  stages: [
    { duration: '2m', target: 100 }, // Ramp up
    { duration: '5m', target: 100 }, // Stay at 100 users
    { duration: '2m', target: 0 },   // Ramp down
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // 95% of requests < 500ms
    http_req_failed: ['rate<0.01'],   // Error rate < 1%
  },
}

export default function () {
  // Simulate multi-tenant load
  const tenantId = `tenant_${Math.floor(Math.random() * 10) + 1}`

  const res = http.get(`https://api.blkshpos.com/api/products?tenant=${tenantId}`, {
    headers: { Authorization: `Bearer ${__ENV.API_TOKEN}` }
  })

  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 500ms': (r) => r.timings.duration < 500,
  })

  sleep(1)
}
```

---

## Migration from Frappe

### ETL Strategy

```typescript
// Frappe to Prisma migration script
import Frappe from 'frappe-js-sdk'
import { PrismaClient } from '@prisma/client'

async function migrateProducts(tenantId: string) {
  const frappe = new Frappe('https://legacy.blkshpos.com')
  const prisma = getPrismaClient(tenantId)

  // Fetch all products from Frappe
  const frappeProducts = await frappe.getDocList('Product', {
    fields: ['*'],
    limit_page_length: 10000
  })

  // Transform and insert into Prisma
  for (const frappeProduct of frappeProducts) {
    await prisma.product.create({
      data: {
        productCode: frappeProduct.product_code,
        productName: frappeProduct.product_name,
        productType: frappeProduct.product_type,
        primaryCountUnit: frappeProduct.primary_count_unit,
        volumeConversionUnit: frappeProduct.volume_conversion_unit,
        volumeConversionFactor: frappeProduct.volume_conversion_factor,
        weightConversionUnit: frappeProduct.weight_conversion_unit,
        weightConversionFactor: frappeProduct.weight_conversion_factor,
        valuationRate: frappeProduct.valuation_rate,
        valuationMethod: frappeProduct.valuation_method,
        hasBatchNo: frappeProduct.has_batch_no,
        // ... other fields

        // Migrate child tables
        departments: {
          create: frappeProduct.departments.map(d => ({
            departmentId: findOrCreateDepartment(d.department),
            isPrimary: d.is_primary,
            parLevel: d.par_level,
            orderQuantity: d.order_quantity
          }))
        }
      }
    })
  }

  console.log(`Migrated ${frappeProducts.length} products for tenant ${tenantId}`)
}

// Validation
async function validateMigration(tenantId: string) {
  const prisma = getPrismaClient(tenantId)

  // Check counts match
  const frappeCount = await getFrappeProductCount()
  const prismaCount = await prisma.product.count()

  console.log(`Frappe products: ${frappeCount}, Prisma products: ${prismaCount}`)

  if (frappeCount !== prismaCount) {
    throw new Error('Product count mismatch!')
  }

  // Spot check random samples
  const samples = await prisma.product.findMany({ take: 10 })
  for (const sample of samples) {
    const frappeDoc = await getFrappeProduct(sample.productCode)
    assert(sample.productName === frappeDoc.product_name)
    // ... more assertions
  }

  console.log('✅ Migration validation passed')
}
```

---

## Post-Launch Roadmap

### Month 10+: Advanced Features
- [ ] Mobile app (React Native or PWA)
- [ ] Offline mode with sync
- [ ] Advanced analytics (cohort analysis, predictive alerts)
- [ ] Vendor portal (self-service invoice submission)
- [ ] Multi-location consolidated reporting
- [ ] Intercompany transaction automation
- [ ] Advanced AI: Recipe optimization, waste prediction
- [ ] White-label options for resellers

### Continuous Improvement
- [ ] A/B testing framework (Vercel Edge Config)
- [ ] Feature flags (LaunchDarkly or Statsig)
- [ ] User feedback collection (in-app surveys)
- [ ] Performance monitoring and optimization
- [ ] Security updates and penetration testing
- [ ] Compliance certifications (SOC 2, ISO 27001)

---

## Success Metrics

### Technical KPIs
- **Performance:** p95 API response time < 300ms
- **Uptime:** 99.9% availability (43 min downtime/month)
- **Error Rate:** < 0.1% of requests
- **Test Coverage:** > 80% code coverage
- **Security:** Zero critical vulnerabilities

### Product KPIs
- **AI Accuracy:**
  - Invoice OCR: > 90% field accuracy
  - Product matching: > 85% auto-match rate
  - Demand forecasting: < 15% MAPE (Mean Absolute Percentage Error)
- **User Efficiency:**
  - 80% reduction in invoice entry time
  - 50% reduction in ordering time
  - 90% reduction in variance investigation time

### Business KPIs
- **Customer Acquisition:** 50 paying customers in first 6 months
- **Retention:** > 95% monthly retention
- **NPS:** > 50
- **Revenue:** $50K MRR by end of year 1

---

## Conclusion

This full Next.js replacement strategy delivers a modern, scalable, AI-powered SaaS platform built on industry-standard technologies. While the 6-9 month timeline is aggressive, the comprehensive feature set, robust testing, and production-ready infrastructure justify the investment.

**Next Steps:**
1. Assemble development team (3-5 engineers + AI/ML specialist)
2. Set up development infrastructure (repos, CI/CD, staging environments)
3. Begin Month 1 foundation work
4. Establish weekly sprint cadence
5. Plan beta customer recruitment

**Estimated Team:**
- 2 Full-stack engineers (Next.js + TypeScript)
- 1 Backend/AI engineer (Python ML models, LangChain)
- 1 UI/UX designer
- 1 DevOps/Infrastructure engineer (part-time)
- 1 QA engineer (part-time)

**Total Budget Estimate:** $400K-$600K (salaries + infrastructure + tools)

---

*Document Version: 1.0*
*Last Updated: 2025-01-15*
*Owner: BLKSHP Engineering Team*
