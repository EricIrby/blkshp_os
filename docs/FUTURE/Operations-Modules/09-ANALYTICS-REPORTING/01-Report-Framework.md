# Report Framework

## Overview

The Report Framework provides the infrastructure for creating, scheduling, and delivering reports. Built on Frappe Framework's reporting capabilities with department-based filtering and multi-format export.

## Purpose

- Provide report creation infrastructure
- Support department-based filtering
- Enable report scheduling
- Support multiple export formats
- Enable report favorites and customization

## Frappe Framework Reporting

### Built-in Capabilities
- **Report Builder**: Visual report builder for custom reports
- **Query Report**: SQL-based custom reports
- **Script Report**: Python-based custom reports with complex logic
- **Report Scheduling**: Built-in scheduler for automated report delivery
- **Export Formats**: PDF, Excel, CSV export built-in
- **Permission-Based**: Reports respect user permissions and department access

## Report Filtering System

### Standard Filters
- **Department Filter**: Single or multiple departments
- **Date Range**: From date and to date
- **Company/Location**: Filter by company/store
- **Product Category**: Filter by product category
- **Vendor**: Filter by vendor
- **Custom Filters**: Report-specific filters (e.g., GL code, product type)

### Department-Based Access
- Users see only data for departments they have access to
- Consolidated reports aggregate only accessible departments
- Department filter defaults to user's accessible departments

## Report Types

### Inventory Reports (7 reports)
- Historic Inventory Summary
- Historic Inventory Details
- Last Audit Summary
- Item Audit Report
- Inventory Cost Details
- Item Report
- Individual Item History

### Cost Reports (14 reports)
- Actual vs Theoretical Summary
- Actual vs Theoretical Cost Summary
- Actual vs Theoretical Cost Details
- Actual vs Theoretical Quantity Details
- Actual vs Theoretical COGS by Ops Group
- Cost Summary
- Cost Details
- Cost Summary by Category
- Cost Summary by Subcategory
- Cost Summary by Ops Group
- Current Cost Summary
- Theoretical Costs
- Theoretical Cost vs Sales

### Procurement Reports (10 reports)
- Purchase Log
- Purchases by Item
- Purchases by Vendor
- Best Price
- Average Price Details
- CU Price Comparison
- Price Details
- Receiving Orders Details
- Consolidated Purchases by Vendor (Director)
- Consolidated Purchases by Category (Director)

### Recipe Reports (5 reports)
- Recipe Sales
- Weekly Recipe Sales
- Recipe Reprice
- Recipes with Inactive Items
- Recipe Sync Analysis (Director)

### Sales Reports (9 reports)
- Sales Summary
- Sales Details
- Sales by Item
- Sales by Hour
- POS Item Sales
- Daily Sales Report (DSR)
- Profit by Server
- Menu Engineering
- Product Mix (Director)

### And more...
- Invoice Reports (4 reports)
- Transfer Reports (2 reports)
- Depletion Reports (3 reports)
- Variance Reports (2 reports)
- Financial Reports (4 reports)
- Director Reports (1+ reports)

## Implementation Steps

### Step 1: Set Up Report Infrastructure
1. Configure Frappe reporting
2. Set up report templates
3. Configure export formats
4. Set up scheduling

### Step 2: Implement Department Filtering
1. Add department filter to all reports
2. Respect user department permissions
3. Aggregate multi-department reports
4. Default to user's accessible departments

### Step 3: Create Report Catalog
1. Create report definitions
2. Configure report parameters
3. Set up report permissions
4. Enable report favorites

## Dependencies

- **Frappe Framework**: Built-in reporting capabilities
- **Department DocType**: Department filtering
- **All Domain DocTypes**: Report data sources

## Testing Checklist

- [ ] Create reports with department filtering
- [ ] Schedule reports for delivery
- [ ] Export reports to PDF/Excel/CSV
- [ ] Test report permissions
- [ ] Enable report favorites
- [ ] Test consolidated reports
- [ ] Verify data accuracy

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 14

