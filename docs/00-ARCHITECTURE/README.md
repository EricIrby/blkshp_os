# Architecture & Foundation Documentation

This directory contains foundational architecture documentation for BLKSHP OS.

**Last Updated:** November 8, 2025

---

## Documents

### Core Architecture

- **01-App-Structure.md** ⭐ **START HERE** - Current Desk-only application structure
  - Complete file structure and organization
  - Module and DocType patterns
  - Development workflow
  - Best practices for current architecture

- **02-Frappe-Framework.md** (formerly 03) - Frappe Framework guide
  - Framework overview and concepts
  - DocType system
  - API patterns
  - Best practices

- **03-Deployment.md** (formerly 04) - Deployment and scaling
  - Production deployment
  - Scaling strategies
  - Infrastructure requirements
  - Performance optimization

- **04-Separate-Frontend.md** - Future SPA architecture reference
  - ⚠️ Not currently implemented
  - Vue/React/Vite architecture
  - When to use separate frontend
  - Migration path from Desk-only
  - Preserved for future reference

### Legacy/Reference

- **00-Overview.md** - Historical: Executive summary (consolidated into docs/README.md)
- **01-Architecture-Design.md** - Historical: Core architecture (reference)
- **02-Application-Structure.md** - Historical: Old structure (superseded by 01-App-Structure.md)

---

## Reading Order

### For New Developers

1. **01-App-Structure.md** - Understand current application structure
2. **02-Frappe-Framework.md** - Learn Frappe framework
3. **03-Deployment.md** - Understand deployment (when ready)
4. **docs/README.md** (parent) - Project overview and setup

### For Architecture Decisions

1. **01-App-Structure.md** - Current implementation
2. **01-Architecture-Design.md** - Core design principles
3. **04-Separate-Frontend.md** - Future SPA considerations (if needed)

### For Future SPA Migration

1. **01-App-Structure.md** - Current structure (baseline)
2. **04-Separate-Frontend.md** - SPA architecture guide
3. **02-Frappe-Framework.md** - API integration patterns

---

## Purpose

These documents provide the architectural foundation for BLKSHP OS development. They should be consulted:

- **Before starting** any new domain implementation
- **When making** architectural decisions
- **For understanding** module organization patterns
- **When planning** future enhancements

---

## Key Concepts

### Current Architecture: Desk-Only

BLKSHP OS uses a **traditional Frappe Desk application** architecture:

- ✅ Built-in Frappe UI for all functionality
- ✅ Rapid development with DocType system
- ✅ Proven patterns for business operations
- ✅ Backend and frontend in one framework
- ✅ Can migrate to SPA later if needed

### Domain-Based Organization

Code is organized by business domain:
- `departments/` - Department management
- `permissions/` - User permissions and roles
- `products/` - Product management (future)
- `inventory/` - Inventory tracking (future)
- etc.

### When to Consult These Docs

**01-App-Structure.md:**
- Creating new domains
- Adding DocTypes
- Organizing code
- Understanding file structure

**02-Frappe-Framework.md:**
- Learning Frappe concepts
- API development
- DocType development
- Best practices

**03-Deployment.md:**
- Deploying to production
- Scaling the application
- Infrastructure planning

**04-Separate-Frontend.md:**
- Considering SPA frontend
- Customer-facing portals
- Mobile-first requirements
- Migration planning

---

## Status

**Current Implementation:**
- ✅ Desk-only architecture (01-App-Structure.md)
- ✅ Departments domain complete
- ✅ Permissions domain complete
- ⏳ Products domain next

**Documentation:**
- ✅ Current structure documented
- ✅ Frappe guide complete
- ✅ Deployment guide complete
- ✅ Future SPA guide preserved

---

**For main documentation:** See `docs/README.md` (parent directory)  
**For development guide:** See `docs/DEVELOPMENT-GUIDE.md`  
**For domain docs:** See domain-specific folders (01-PRODUCTS/, 02-DEPARTMENTS/, etc.)

