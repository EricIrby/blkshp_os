# Project Overview

> **Legacy Reference:** This document is preserved for historical context. Current guidance lives in `docs/README.md` and `00-ARCHITECTURE/01-App-Structure.md`.

## Executive Summary

### Project Overview

This document outlines a comprehensive plan to build the **BLKSHP Product Platform** - a unified inventory management and cost control platform using the Frappe Framework. Unlike Craftable's multi-platform approach (Foodager/Bevager/House), BLKSHP uses a single unified platform with **department-based segmentation** for flexible product management, allocations, transfers, and permissions.

### Why Frappe Framework?

Frappe Framework is ideal for this project because:

- **Metadata-Driven Architecture**: Perfect for rapid development of complex business logic
- **Built-in Multi-Tenancy**: Native support for Company/Location hierarchies
- **Role-Based Permissions**: Granular permission system out of the box
- **RESTful API**: All DocTypes automatically expose REST APIs
- **Modern UI**: Frappe Desk provides responsive, mobile-friendly interface
- **Python Backend**: Easy integration with ML/AI libraries for invoice processing
- **Extensible**: Easy to add custom apps and modules

### Key Advantages of Frappe Framework

1. **Faster Development**: Metadata-driven framework reduces boilerplate code by 70%+
2. **Built-in Features**: User management, permissions, workflows, print formats, email integration
3. **ERPNext Compatibility**: Can leverage existing ERPNext modules (Stock, Accounts, etc.)
4. **Active Community**: Large ecosystem of apps and integrations
5. **Production-Ready**: Used by thousands of companies globally
6. **Open Source**: Full control and no vendor lock-in

---

## Project Goals

- **Unified Platform**: Single system for all inventory types (food, beverage, supplies)
- **Department-Based Segmentation**: Flexible organization without separate platforms
- **Comprehensive Inventory Management**: Tracking, auditing, and theoretical inventory
- **Procurement Integration**: Vendor management and Ottimate integration
- **Recipe Management**: Costing, batch production, and POS integration
- **Multi-Location Support**: Director-level management with store synchronization
- **Reporting & Analytics**: Department-filterable reports and dashboards

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 1

