# Agent Context Package

**Essential documents to include in agent context for domain-specific development**

**Last Updated**: 2025  
**Version**: 1.0

---

## 📦 Required Context Package

When starting work on a specific domain, include these documents in the agent's context to ensure understanding of project-wide architecture, patterns, and integration points.

---

## 🎯 Core Context (ALWAYS INCLUDE)

### 1. Project-Wide Context (REQUIRED)
**File**: `PROJECT-CONTEXT.md`
- Architecture principles
- Anti-patterns to avoid
- Patterns to follow
- Cross-domain dependencies
- Common pitfalls

**Why**: Provides essential architecture context that applies to all domains.

---

### 2. Agent Instructions (REQUIRED)
**File**: `AGENT-INSTRUCTIONS.md`
- How to work on the project
- Development workflow
- Communication guidelines
- Code review checklist
- Testing requirements

**Why**: Ensures agents follow consistent processes and communication patterns.

---

### 3. Cross-Domain Reference (REQUIRED)
**File**: `CROSS-DOMAIN-REFERENCE.md`
- Domain interactions
- Shared patterns
- Integration points
- Data flow patterns
- Quick reference

**Why**: Helps agents understand how domains integrate and avoid duplication.

---

### 4. Architecture Foundation (REQUIRED)
**Files**: 
- `00-ARCHITECTURE/01-Architecture-Design.md`
- `00-ARCHITECTURE/02-Application-Structure.md`
- `00-ARCHITECTURE/03-Frappe-Framework-Guide.md`

**Why**: Provides foundational architecture understanding.

---

## 📋 Domain-Specific Context Package

### For Departments Domain Development

**Core Context** (Always Include):
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md
4. 00-ARCHITECTURE/01-Architecture-Design.md
5. 00-ARCHITECTURE/02-Application-Structure.md

**Domain-Specific**:
6. 02-DEPARTMENTS/README.md
7. 02-DEPARTMENTS/01-Department-Master.md
8. 02-DEPARTMENTS/02-Department-Permissions.md
9. 02-DEPARTMENTS/04-Department-Allocations.md

**Dependencies**: None (foundation domain)

**Why This Package**: Departments is the foundation - no dependencies, but everything depends on it. Agents need to understand the critical role departments play.

---

### For Products Domain Development

**Core Context** (Always Include):
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md
4. 00-ARCHITECTURE/01-Architecture-Design.md
5. 00-ARCHITECTURE/02-Application-Structure.md

**Domain-Specific**:
6. 01-PRODUCTS/README.md
7. 01-PRODUCTS/01-Product-Master.md
8. 01-PRODUCTS/04-Unit-Conversion-System.md ⭐ CRITICAL
9. Function documents you're implementing

**Dependencies** (Review):
10. 02-DEPARTMENTS/README.md (dependency)
11. 02-DEPARTMENTS/04-Department-Allocations.md (for product-department relationship)

**Why This Package**: Products depends on Departments. Unit conversion is critical and used by ALL domains.

---

### For Inventory Domain Development

**Core Context** (Always Include):
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md
4. 00-ARCHITECTURE/01-Architecture-Design.md
5. 00-ARCHITECTURE/02-Application-Structure.md

**Domain-Specific**:
6. 03-INVENTORY/README.md
7. 03-INVENTORY/01-Inventory-Balance.md
8. 03-INVENTORY/02-Theoretical-Inventory.md ⭐ CRITICAL
9. Function documents you're implementing

**Dependencies** (Review):
10. 02-DEPARTMENTS/README.md (dependency)
11. 01-PRODUCTS/README.md (dependency)
12. 01-PRODUCTS/04-Unit-Conversion-System.md ⭐ CRITICAL (unit conversions)

**Why This Package**: Inventory depends on Products and Departments. 2D model and unit conversions are critical.

---

### For POS Integration Domain Development

**Core Context** (Always Include):
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md
4. 00-ARCHITECTURE/01-Architecture-Design.md

**Domain-Specific**:
5. 06-POS-INTEGRATION/README.md
6. Function documents you're implementing

**Dependencies** (Review):
7. 01-PRODUCTS/README.md (dependency)
8. 02-DEPARTMENTS/README.md (dependency)
9. 05-RECIPES/README.md ⭐ CRITICAL (for depletion calculations)
10. 03-INVENTORY/README.md (for inventory updates)
11. 01-PRODUCTS/04-Unit-Conversion-System.md (for unit conversions)

**Why This Package**: POS Integration depends on Recipes for depletion calculations, Products for conversions, and Inventory for updates.

---

### For Procurement Domain Development

**Core Context** (Always Include):
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md

**Domain-Specific**:
4. 04-PROCUREMENT/README.md
5. Function documents you're implementing

**Dependencies** (Review):
6. 01-PRODUCTS/README.md (dependency)
7. 02-DEPARTMENTS/README.md (dependency)
8. 01-PRODUCTS/04-Unit-Conversion-System.md (for unit conversions)
9. 03-INVENTORY/README.md (for inventory updates)

**Why This Package**: Procurement depends on Products (for purchase units) and Departments (for allocation).

---

### For Recipes Domain Development

**Core Context** (Always Include):
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md

**Domain-Specific**:
4. 05-RECIPES/README.md
5. Function documents you're implementing

**Dependencies** (Review):
6. 01-PRODUCTS/README.md (dependency - products as ingredients)
7. 02-DEPARTMENTS/README.md (dependency)
8. 01-PRODUCTS/04-Unit-Conversion-System.md ⭐ CRITICAL (for recipe costing)

**Why This Package**: Recipes depend on Products (ingredients) and use unit conversions for costing.

---

### For Transfers & Depletions Domain Development

**Core Context** (Always Include):
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md

**Domain-Specific**:
4. 08-TRANSFERS-DEPLETIONS/README.md
5. Function documents you're implementing

**Dependencies** (Review):
6. 01-PRODUCTS/README.md (dependency)
7. 02-DEPARTMENTS/README.md (dependency)
8. 03-INVENTORY/README.md ⭐ CRITICAL (for inventory updates)
9. 01-PRODUCTS/04-Unit-Conversion-System.md (for unit conversions)

**Why This Package**: Transfers and Depletions depend on Inventory for balance updates.

---

## 📝 Context Loading Strategy

### Phase 1: Initial Context (Start of Session)

**Load these documents first:**
1. PROJECT-CONTEXT.md (essential architecture)
2. AGENT-INSTRUCTIONS.md (how to work)
3. CROSS-DOMAIN-REFERENCE.md (integration patterns)
4. Your domain's README.md (domain overview)

**Time**: ~30 minutes to read and understand

---

### Phase 2: Function-Specific Context (During Implementation)

**Load these documents when implementing a function:**
1. Function document you're implementing
2. Dependent domain READMEs (if critical dependencies)
3. Related function documents (if integration needed)

**Time**: ~15 minutes per function

---

### Phase 3: Reference Context (As Needed)

**Load these documents when needed:**
1. Specific function documents for reference
2. Architecture documents for details
3. Development guides for priorities
4. Dependent domain function documents (for integration)

**Time**: As needed

---

## ✅ Context Verification Checklist

### Before Starting Development

**Verify agent has access to:**
- [ ] PROJECT-CONTEXT.md
- [ ] AGENT-INSTRUCTIONS.md
- [ ] CROSS-DOMAIN-REFERENCE.md
- [ ] Your domain's README.md
- [ ] Function documents you're implementing
- [ ] Dependent domain READMEs (if critical)
- [ ] Architecture documents (if needed)

### During Development

**Verify agent understands:**
- [ ] Architecture principles
- [ ] Department-based model
- [ ] 2D inventory model
- [ ] Unit conversion patterns
- [ ] Permission patterns
- [ ] Cross-domain dependencies
- [ ] Shared methods available

### After Implementation

**Verify agent has considered:**
- [ ] Cross-domain impact
- [ ] Integration points
- [ ] Shared patterns
- [ ] Data consistency
- [ ] Permission enforcement
- [ ] Department filtering
- [ ] Unit conversions

---

## 🎓 Learning Path for Agents

### Step 1: Understand the Platform (30-60 min)
1. Read PROJECT-CONTEXT.md (architecture principles)
2. Read AGENT-INSTRUCTIONS.md (how to work)
3. Review 00-ARCHITECTURE/ documents (foundation)
4. Review CROSS-DOMAIN-REFERENCE.md (integration)

### Step 2: Understand Your Domain (30 min)
1. Read your domain's README.md
2. Read all function documents in your domain
3. Understand dependencies
4. Review integration points

### Step 3: Understand Integration (30 min)
1. Review CROSS-DOMAIN-REFERENCE.md integration patterns
2. Review dependent domain READMEs
3. Review dependent domain function documents (if needed)
4. Understand shared methods

### Step 4: Start Implementation
1. Follow AGENT-INSTRUCTIONS.md workflow
2. Reference PROJECT-CONTEXT.md patterns
3. Use CROSS-DOMAIN-REFERENCE.md for integration
4. Implement one function at a time

---

## 📋 Quick Reference Cards

### Architecture Principles Card

```
UNIFIED PLATFORM
- Single Product DocType (not separate platforms)
- Department-based segmentation
- All product types in one system

2D INVENTORY MODEL
- Product + Department (not storage)
- Storage is metadata only
- All calculations use Product + Department

HUB-AND-SPOKE CONVERSION
- All conversions through primary unit
- Store in primary unit
- Convert on display/entry

DEPARTMENT-FIRST
- Always include department
- Filter by departments
- Respect permissions
```

### Integration Patterns Card

```
PRODUCT + DEPARTMENT
- Always include both
- Filter by department
- Track per combination

UNIT CONVERSION
- Use Product's methods
- Store in primary unit
- Convert on-the-fly

PERMISSIONS
- Check department access
- Check role permissions
- Use Frappe's system

DEPARTMENT FILTERING
- Get user's departments
- Filter queries
- Respect boundaries
```

---

## 🚀 Agent Onboarding Process

### Day 1: Setup & Understanding (2-3 hours)

**Morning:**
- [ ] Load PROJECT-CONTEXT.md
- [ ] Load AGENT-INSTRUCTIONS.md
- [ ] Load CROSS-DOMAIN-REFERENCE.md
- [ ] Read and understand architecture principles

**Afternoon:**
- [ ] Load domain README.md
- [ ] Load function documents
- [ ] Review dependencies
- [ ] Understand integration points

---

### Day 2: Planning (2-3 hours)

**Morning:**
- [ ] Review function document in detail
- [ ] Check for existing implementations
- [ ] Plan integration points
- [ ] Identify shared utilities

**Afternoon:**
- [ ] Plan implementation steps
- [ ] Plan testing approach
- [ ] Ask clarifying questions
- [ ] Get approval to proceed

---

### Day 3: Implementation (Variable)

- [ ] Follow established patterns
- [ ] Implement functionality
- [ ] Add error handling
- [ ] Add validation
- [ ] Test thoroughly

---

## 📊 Context Package Summary

### Minimum Required Context

**For any domain:**
1. PROJECT-CONTEXT.md
2. AGENT-INSTRUCTIONS.md
3. CROSS-DOMAIN-REFERENCE.md
4. Your domain's README.md
5. Function documents you're implementing

### Recommended Additional Context

**Based on domain:**
- Dependent domain READMEs (if critical)
- Related function documents (if needed)
- Architecture documents (if needed)
- Development guides (if needed)

---

## 🔍 Context Quality Checklist

**Before starting work, verify:**
- [ ] Agent has read PROJECT-CONTEXT.md
- [ ] Agent understands architecture principles
- [ ] Agent understands department-based model
- [ ] Agent understands 2D inventory model
- [ ] Agent understands unit conversion system
- [ ] Agent understands cross-domain dependencies
- [ ] Agent has read domain documentation
- [ ] Agent understands function requirements
- [ ] Agent has reviewed integration points

---

## 💡 Tips for Effective Context Loading

1. **Start with Core Context**: Always load PROJECT-CONTEXT.md, AGENT-INSTRUCTIONS.md, CROSS-DOMAIN-REFERENCE.md first
2. **Then Domain Context**: Load domain README and function documents
3. **Then Dependencies**: Load dependent domain READMEs if critical
4. **Reference As Needed**: Load additional context when needed during implementation
5. **Keep It Focused**: Don't overload with unnecessary context, but ensure critical context is included

---

## 📞 Context Questions

**If agent asks about:**
- Architecture: Direct to PROJECT-CONTEXT.md
- How to work: Direct to AGENT-INSTRUCTIONS.md
- Integration: Direct to CROSS-DOMAIN-REFERENCE.md
- Domain specifics: Direct to domain README.md
- Function details: Direct to function document

---

**Use this package to ensure agents have all necessary context for domain-specific development. The goal is to provide enough context for effective development while avoiding information overload.**


