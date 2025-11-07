# BLKSHP Product Platform - Comprehensive Functionality Audit Checklist

**Purpose:** Verify that all functionality from Craftable has been captured in the FRAPPE_IMPLEMENTATION_PLAN.md

**Date:** 2025  
**Status:** Complete - Ready for Review  
**Source:** Craftable Documentation Directory (276 files reviewed)

---

## 1. CORE INVENTORY MANAGEMENT

### 1.1 Product Management
- [x] Unified Product Master (single product for all types) - **COVERED**
- [x] Product Categories and Subcategories - **COVERED**
- [x] Product Tags - **COVERED**
- [x] Product Images - **COVERED**
- [x] Product Properties:
  - [x] Generic Items - **COVERED**
  - [x] Non-Inventory Items - **COVERED**
  - [x] Prep Items - **COVERED**
  - [ ] Linked Items - **NEEDS VERIFICATION**
  - [ ] Duplicate Items Detection - **NEEDS DETAIL**
- [x] Product-to-Department Assignments (many-to-many) - **COVERED**
- [x] Department-Specific Par Levels - **COVERED**
- [x] Department-Specific Order Quantities - **COVERED**
- [x] Default Department Assignment - **COVERED**
- [x] Storage Area Assignments - **COVERED**
- [x] Vendor Associations - **COVERED**
- [x] Purchase Unit Definitions - **COVERED**
- [x] Count Unit System (Primary + Volume + Weight conversions) - **COVERED**
- [x] Unit Conversion System (hub-and-spoke model) - **COVERED**
- [x] Secondary Count Units - **COVERED**
- [x] GL Code Mapping (per product-department) - **COVERED**
- [x] Active/Inactive Status - **COVERED**
- [ ] Item History Tracking - **NEEDS DETAIL**
- [ ] Item Notes - **NEEDS DETAIL**
- [ ] Item ID Management - **NEEDS DETAIL**
- [ ] Item CU Price Override - **NEEDS DETAIL**
- [ ] Item Export to Excel - **NEEDS DETAIL**
- [ ] Item Loader (Bulk Import) - **NEEDS DETAIL**
- [ ] Express Loader - **NEEDS DETAIL**
- [ ] Item Manager Interface - **NEEDS DETAIL**
- [ ] Item Requests - **NEEDS DETAIL**
- [ ] Multiple SKUs per Item - **NEEDS DETAIL**
- [ ] Substitute Items - **NEEDS DETAIL**
- [ ] Item Bins - **NEEDS DETAIL**
- [ ] Item Labels (Print) - **NEEDS DETAIL**
- [ ] Each Label Setting - **NEEDS DETAIL**
- [ ] Catch Weight for Purchase Units - **NEEDS DETAIL**
- [ ] Weight Capture for Purchase Units - **NEEDS DETAIL**
- [ ] Minimum Order Amount/CU Quantity - **NEEDS DETAIL**
- [ ] Contract Price Violations - **NEEDS DETAIL**
- [ ] Promo Threshold - **NEEDS DETAIL**

### 1.2 Inventory Tracking
- [x] 2D Inventory Model (Product + Department) - **COVERED**
- [x] Theoretical Inventory Calculation (per department) - **COVERED**
- [x] Inventory Balance Tracking (Product + Department) - **COVERED**
- [x] Storage Location Tracking (metadata only) - **COVERED**
- [x] Inventory Transfers (inter-department, inter-store) - **COVERED**
- [x] Depletion Tracking (sold, spilled, manual, per department) - **COVERED**
- [x] Variance Calculation (per department) - **COVERED**
- [x] Historical Inventory Tracking - **COVERED**
- [ ] Negative Transfer Control - **NEEDS DETAIL**
- [ ] Transfer Price Updates - **NEEDS DETAIL**

### 1.3 Inventory Auditing
- [x] Task-Based Audit System - **COVERED**
- [x] Audit Scope Definition (departments, storages, categories) - **COVERED**
- [x] Counting Task Creation (auto-generated from scope) - **COVERED**
- [x] Multi-User Concurrent Counting - **COVERED**
- [x] Department-Based Task Assignment - **COVERED**
- [x] Storage-First Counting Workflow - **COVERED**
- [x] Count Unit Selection (any available unit) - **COVERED**
- [x] Count Storage (converted to primary unit) - **COVERED**
- [x] Audit Line Recording - **COVERED**
- [x] Audit Status Workflow (Setup → Ready → In Progress → Review → Closed → Locked) - **COVERED**
- [x] Audit Closing Process - **COVERED**
- [x] Variance Reporting (per department) - **COVERED**
- [x] Partial Audits (by category/department) - **COVERED**
- [x] Full Audits - **COVERED**
- [x] Audit History and Reporting - **COVERED**
- [ ] Flagging Audit Items for Recount - **NEEDS DETAIL**
- [ ] Unsaved Counts Management - **NEEDS DETAIL**
- [ ] Audit Deletion - **NEEDS DETAIL**
- [ ] Reopening Closed Audits - **NEEDS DETAIL**
- [ ] Opening Locked Audits - **NEEDS DETAIL**
- [ ] Updating Closed Audits - **NEEDS DETAIL**
- [ ] Correcting Previous Audits - **NEEDS DETAIL**
- [ ] Updating Item CU Price on Closed Audit - **NEEDS DETAIL**
- [ ] Audit Comparison Report - **NEEDS DETAIL**
- [ ] Days to Lock Audits (Director Configuration) - **NEEDS DETAIL**

---

## 2. PROCUREMENT & ORDERING

### 2.1 Vendor Management
- [x] Vendor Master - **COVERED**
- [x] Vendor Contact Information - **COVERED**
- [x] Vendor Payment Terms - **COVERED**
- [ ] Vendor Catalogs - **DEFERRED** (Not needed at this time - catalog integrations removed)
- [x] Vendor-Specific Purchase Units - **COVERED**
- [x] Vendor SKU Mapping - **COVERED**
- [x] Vendor Item Mapping - **COVERED** (Section 22.4)
- [x] Preferred Vendor Assignment - **COVERED**
- [x] Vendor Pricing (contract prices) - **COVERED**
- [x] Corporate Vendor Management (Director-level) - **COVERED**
- [x] Store-Level Vendor Sync - **COVERED**
- [x] Mixed Vendors - **COVERED** (Section 22.11)
- [x] Vendor Sales Rep Details - **COVERED** (Section 22.3.1 - Multiple contact types)
- [x] Vendor Accounting Details (Bill Item Name, Payment Method) - **COVERED** (Section 22.2)
- [x] Vendor Accounting Contacts - **COVERED** (Section 22.3.2)
- [x] Vendor Leadership Contacts - **COVERED** (Section 22.3.3)
- [x] Vendor Other Contacts - **COVERED** (Section 22.3.4)
- [x] Vendor Mapping (External Systems) - **COVERED** (Section 22.10)
- [x] Vendor Vacation Settings - **COVERED** (Section 22.6)
- [x] Vendor Tags - **COVERED** (Section 22.7)
- [x] Vendor Ordering Rules (Minimums, Cutoffs, Schedules) - **COVERED** (Section 22.5)
- [x] Removing/Inactivating Vendors - **COVERED** (Section 22.8)
- [ ] Vendor Portal - **REMOVED** (Not needed - vendor portal removed)
- [ ] Craftables Vendor Integrations - **DEFERRED** (Future enhancement)

### 2.2 Purchase Orders
- [x] Purchase Order Creation - **COVERED** (Basic structure)
- [x] Purchase Order Items - **COVERED** (Basic structure)
- [x] Order-to-Par Functionality - **COVERED** (Basic structure)
- [x] Department-Specific Ordering - **COVERED**
- [x] Order Approval Workflows - **COVERED** (Basic structure)
- [x] Order Status Tracking - **COVERED** (Basic structure)
- [x] Order Guides (saved templates) - **COVERED** (Basic structure)
- [x] Order History - **COVERED**
- [x] Order Log Report - **COVERED**
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Quick Orders - Ordering workflows moved to later phase after Ottimate contract
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Recurring Orders - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Orders with Budgets - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Non-Inventory Ordering - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Ordering Options - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Ordering Through Bill Hold - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Ordering from Vendor Catalog - Ordering workflows moved to later phase (catalog integrations removed)
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Ordering Freehand Items - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Multi-User Order Approval - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Order Notifications (Email/Text) - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Order PDF with Logo - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Adding Non-Inventory Items to Orders - Ordering workflows moved to later phase
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Order Non-Mapped Items from Vendor Catalog - Ordering workflows moved to later phase
- **Note**: Purchase orders are currently managed in Ottimate or manually. Detailed ordering workflows will be built in BLKSHP after Ottimate contract ends (12+ months).

### 2.3 Receiving Workflow
- [x] Receiving Orders - **COVERED** (Basic structure)
- [x] Delivery Receipts - **COVERED**
- [x] Mark Order Received - **COVERED**
- [x] Receive Order Button - **COVERED**
- [x] Receiving Orders Details Report - **COVERED**
- [x] Ottimate Integration - **COVERED** (Section 15)
  - [x] Flatfile import from Ottimate - **COVERED**
  - [x] Receiving activity update from Ottimate data - **COVERED**
  - [x] Inventory update based on Ottimate receiving - **COVERED**
  - [x] Persistent item mapping system - **COVERED**
  - [x] Review workflow for unmapped items - **COVERED**
  - [x] Note: Invoices and A/P managed in Ottimate (not in this system) - **COVERED**
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Detailed Receiving Workflow - Moved to later phase after Ottimate contract
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Partial Receiving - Moved to later phase after Ottimate contract
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Receiving Inspection - Moved to later phase (Optional)
- [ ] **DEFERRED TO LATER PHASE** (12+ months): Receiving Quality Control - Moved to later phase (Optional)
- [ ] **DEFERRED**: 3-Way Matching (PO, Delivery Receipt, Invoice) - **FUTURE PHASE**
- [ ] **DEFERRED**: Reconciliation Rules - **FUTURE PHASE**
- [ ] **DEFERRED**: Threshold % for Variance - **FUTURE PHASE**
- [ ] **DEFERRED**: Linking Delivery Receipts to Invoices - **FUTURE PHASE**

### 2.4 Invoice Processing
- [x] Basic Invoice Structure - **COVERED** (Basic DocType structure exists)
- [x] Invoice Line-Level Department Allocation - **COVERED**
- [x] Invoice Line Splitting (across departments) - **COVERED**
- [x] GL Code Assignment (per product-department) - **COVERED**
- [x] Storage Location Assignment (metadata) - **COVERED**
- [ ] **DEFERRED TO LATER PHASE** (12+ months): All invoice processing workflows moved to later phase after Ottimate contract
  - [ ] Invoice OCR Processing (Tesseract, EasyOCR, InvoiceNet)
  - [ ] Invoice AI Processing
  - [ ] AI-Powered Invoice Matching
  - [ ] Invoice Line Extraction
  - [ ] Product Matching (FuzzyWuzzy)
  - [ ] Invoice Reconciliation
  - [ ] Invoice Redlining (quantity/price adjustments)
  - [ ] Invoice Approval Workflow
  - [ ] Invoice Status Tracking
  - [ ] Invoice-to-Purchase Order Linking
  - [ ] Electronic Invoicing
  - [ ] E-Invoice Mapping
  - [ ] Updating Electronic Invoice Lines
  - [ ] Invoice Image Upload
  - [ ] Image Vault
  - [ ] Email Invoice Submission
  - [ ] EDI Feed Processing
  - [ ] Invoice Notifications (Processing, Unmapped, etc.)
  - [ ] Price Review Flag (20% threshold)
  - [ ] Short Pay Invoices
  - [ ] Merging Invoices
  - [ ] Creating Invoices from Orders
  - [ ] Creating Vendor Invoices Manually
  - [ ] Separating Invoice Between Departments
  - [ ] Viewing Vendor Invoice History
  - [ ] Invoice Summary Report
  - [ ] Invoice Log Report
  - [ ] Raw Invoice Log Report
  - [ ] Auditing Your Bill Hold
- **Note**: Invoices and A/P are currently managed in Ottimate. Invoice processing workflows will be built in BLKSHP after Ottimate contract ends (12+ months).

---

## 3. RECIPE MANAGEMENT

### 3.1 Recipe Creation
- [x] Recipe Master - **COVERED**
- [x] Menu List Grouping - **COVERED**
- [x] Recipe Ingredients (with unit selection) - **COVERED**
- [x] Ingredient Quantity Conversion (to primary units) - **COVERED**
- [x] Subrecipe Support - **COVERED**
- [x] Recipe Cost Calculation (automatic, in primary units) - **COVERED**
- [x] Cost Per Serving Calculation - **COVERED**
- [x] Cost Percentage Calculation - **COVERED**
- [x] Serving Count - **COVERED**
- [x] Serving Price - **COVERED**
- [x] Target Cost Percentage - **COVERED**
- [x] Recipe Instructions - **COVERED**
- [x] Prep Time - **COVERED**
- [x] Shelf Life - **COVERED**
- [x] Storage Temperature - **COVERED**
- [x] Recipe Images - **COVERED**
- [x] Recipe-to-Department Assignment - **COVERED**
- [x] Modifier Recipe Support - **COVERED**
- [x] Prep Item Support - **COVERED**
- [x] Batch Tracking - **COVERED**
- [x] Throw Away Items - **COVERED**
- [x] Base Items - **COVERED**
- [x] Unlinked Items - **COVERED**
- [x] Volume & Weight Calculations - **COVERED**
- [x] Size Override - **COVERED**
- [x] Recipe Allergens - **COVERED** (Section 25.2)
- [x] Inherited Allergens - **COVERED** (Section 25.2)
- [x] Recipe Line Swap - **COVERED** (Section 25.3)
- [x] Understanding Yields - **COVERED** (Section 18)
- [x] Recipe Printing - **COVERED** (Section 25.4)
- [x] Menu List Printing - **COVERED** (Section 25.5.2)
- [x] Creating/Editing Menu Lists - **COVERED** (Section 25.5)

### 3.2 Recipe Costing
- [x] Automatic Cost Calculation from Ingredients - **COVERED**
- [x] Unit Conversion in Recipe Costing - **COVERED**
- [x] Subrecipe Costing - **COVERED**
- [x] Cost Updates (when ingredient prices change) - **COVERED**
- [x] Historical Cost Tracking - **COVERED**
- [x] Recipe Reprice Report - **COVERED** (Section 25.6)

### 3.3 Pours
- [x] Creating Pours - **COVERED**
- [x] Updating Pours - **COVERED**
- [x] Setting Pours - **COVERED** (Section 25.7)

### 3.4 Prep Items & Batches
- [x] Creating Prep Items - **COVERED**
- [x] Creating Batches - **COVERED**
- [x] Adding to Batches - **COVERED**
- [x] Production Preps - **COVERED**
- [x] Counting Prep Items and Batches - **COVERED** (Section 25.8)
- [ ] Creating Batches at Commissary - **NEEDS DETAIL**
- [ ] Batches Transferring as Depletions - **NEEDS DETAIL**

---

## 4. POS INTEGRATION

### 4.1 POS System Connection
- [x] POS System Configuration - **COVERED**
- [x] POS API Integration (Toast, Square, etc.) - **COVERED**
- [x] POS Sales Data Import - **COVERED**
- [x] POS Sales Date Range Filtering - **COVERED**
- [x] Department-Specific POS Tracking - **COVERED**
- [ ] Manual POS Tickets - **NEEDS DETAIL**
- [ ] Re-authorizing Lightspeed - **NEEDS DETAIL**

### 4.2 POS Item Mapping
- [x] Recipe-to-POS Item Mapping - **COVERED**
- [x] Modifier-to-POS Modifier Mapping - **COVERED**
- [x] Department Assignment in Mapping - **COVERED**
- [x] POS Item Mapping Status (Active/Inactive) - **COVERED**
- [ ] Wine Vintages POS Item Mapping - **NEEDS DETAIL**
- [ ] Viewing Recipes/Modifiers Linked to Individual Items - **NEEDS DETAIL**

### 4.3 POS Depletion Calculation
- [x] Automatic Depletion from POS Sales - **COVERED**
- [x] Recipe-Based Depletion Calculation - **COVERED**
- [x] Modifier Adjustment Handling - **COVERED**
- [x] Department-Aware Depletion - **COVERED**
- [x] Unit Conversion in Depletions (to primary units) - **COVERED**
- [x] Depletion Date Tracking - **COVERED**
- [x] Depletion Source Tracking (POS, manual, etc.) - **COVERED**
- [ ] Rerunning POS Depletions After Closing Audit - **NEEDS DETAIL**
- [ ] Allocating Salary Data to Staff for Toast POS - **NEEDS DETAIL**
- [ ] Theoretical Inventory from Your POS - **NEEDS DETAIL**

---

## 5. ACCOUNTING INTEGRATION

### 5.1 Accounting System Connection
- [x] Accounting System Configuration - **COVERED**
- [x] QuickBooks Online Integration - **COVERED**
- [x] QuickBooks Desktop Integration (Web Connector) - **COVERED**
- [x] NetSuite Integration - **COVERED**
- [x] R365 Accounting Integration - **NEEDS DETAIL**
- [x] Sage Intacct API Integration - **NEEDS DETAIL**
- [x] Bill Sync Functionality - **COVERED**
- [x] GL Code Mapping - **COVERED**
- [x] Payee Mapping (Vendor-to-Payee) - **COVERED**
- [x] Accounting Sync Status Tracking - **COVERED**
- [ ] Adding New Payees to Books (QuickBooks Online) - **NEEDS DETAIL**
- [ ] Adding New Payees to Books (QuickBooks Desktop Web Connector) - **NEEDS DETAIL**
- [ ] Failed No Account QuickBooks Desktop Web Connector - **NEEDS DETAIL**
- [ ] Failed No Payee QuickBooks Desktop - **NEEDS DETAIL**
- [ ] QuickBooks Online Responded with Error Current Period Closed - **NEEDS DETAIL**
- [ ] Resolving Error QBWC1039 in QuickBooks Desktop Web Connector - **NEEDS DETAIL**
- [ ] Create Backup of QuickBooks Desktop Company File - **NEEDS DETAIL**
- [ ] Downloading QuickBooks Desktop Web Connector - **NEEDS DETAIL**
- [ ] Classes in Books - **NEEDS DETAIL**
- [ ] Credits, Charges, Taxes (with Books) - **NEEDS DETAIL**
- [ ] Credits, Charges, Taxes (without Books) - **NEEDS DETAIL**
- [ ] Syncing Bills - **NEEDS DETAIL**

### 5.2 Financial Management
- [x] GL Code Assignment (per product-department) - **COVERED**
- [x] Bill Creation from Invoices - **COVERED**
- [x] Expense Recognition (on inventory receipt) - **COVERED**
- [x] Cost Tracking (per product-department) - **COVERED**
- [x] Financial Reporting Integration - **COVERED**
- [ ] Creating General Ledger Accounts - **NEEDS DETAIL**
- [ ] Map to GL - **NEEDS DETAIL**
- [ ] Mass Map - **NEEDS DETAIL**
- [ ] Tax Mappings - **NEEDS DETAIL**
- [ ] GL Distribution Report - **NEEDS DETAIL**
- [ ] GL Summary Report - **NEEDS DETAIL**
- [ ] Alcohol by Volume (ABV) Tax - **NEEDS DETAIL**

---

## 6. PAYMENTS & FINANCIAL OPERATIONS

### 6.1 Payment Processing
- [x] **DEFERRED**: Bank Account Management - **COVERED**
- [x] **DEFERRED**: Check Run (Batch Payments) - **COVERED**
- [x] **DEFERRED**: Individual Payment Processing - **COVERED**
- [x] **DEFERRED**: Credit Tracker - **COVERED**
- [x] **DEFERRED**: Payment Status Tracking - **COVERED**
- [ ] **DEFERRED**: Payments Setup - **NEEDS DETAIL**
- [ ] **DEFERRED**: Setting Up Bank Accounts for Payments - **NEEDS DETAIL**
- [ ] **DEFERRED**: Setting Up ACH Payments - **NEEDS DETAIL**
- [ ] **DEFERRED**: Setting Up Vendor for Payments - **NEEDS DETAIL**
- [ ] **DEFERRED**: Performing Check Run (Authorization Required) - **NEEDS DETAIL**
- [ ] **DEFERRED**: Performing Check Run (No Authorization Required) - **NEEDS DETAIL**
- [ ] **DEFERRED**: Depositing or Printing E-Check - **NEEDS DETAIL**
- [ ] **DEFERRED**: Payment Statuses and Costs - **NEEDS DETAIL**
- [ ] **DEFERRED**: Payment Sync - **NEEDS DETAIL**
- [ ] **DEFERRED**: Payments Disabled - What to Do - **NEEDS DETAIL**
- [ ] **DEFERRED**: Marking Bills Paid - **NEEDS DETAIL**
- [ ] **DEFERRED**: Creating Credit Manually - **NEEDS DETAIL**
- [ ] **DEFERRED**: Processing Credit via Electronic Invoice - **NEEDS DETAIL**
- [ ] **DEFERRED**: Processing Credit and Adjusting Inventory When Bill Sent to Accounting - **NEEDS DETAIL**
- [ ] **DEFERRED**: Credit Trackers - **NEEDS DETAIL**
- [ ] **DEFERRED**: Adding/Updating Credit Card on File - **NEEDS DETAIL**

### 6.2 Payment Approval
- [ ] **DEFERRED**: Payment Approval Workflow Documentation - **FUTURE PHASE** (Payments handled in Ottimate)
- [ ] **DEFERRED**: Multi-Level Approval Routing - **FUTURE PHASE** (Payments handled in Ottimate)
- [ ] **DEFERRED**: Payment Hold/Release Process - **FUTURE PHASE** (Payments handled in Ottimate)
- [ ] **DEFERRED**: Payment Scheduling - **FUTURE PHASE** (Payments handled in Ottimate)

---

## 7. TRANSFERS & DEPLETIONS

### 7.1 Inventory Transfers
- [x] Inter-Department Transfers - **COVERED**
- [x] Inter-Store Transfers - **COVERED**
- [x] Transfer Line Items - **COVERED**
- [x] Transfer Status Tracking (Draft → Submitted → Acknowledged) - **COVERED**
- [x] Transfer Date Tracking - **COVERED**
- [x] Transfer Impact on Theoretical Inventory - **COVERED**
- [x] Transfer Approval Workflow - **COVERED**
- [ ] Transferring Into The Negative - **NEEDS DETAIL**
- [ ] Transfer Price Updates - **NEEDS DETAIL**
- [ ] Director Transfers (Instant) - **NEEDS DETAIL**
- [ ] Transferring Items with Recipes - **NEEDS DETAIL**
- [ ] Transfer Rejection - **NEEDS DETAIL**
- [ ] Reverting Transfer Acknowledgment - **NEEDS DETAIL**
- [ ] Transfer Log Report - **NEEDS DETAIL**
- [ ] Transfer Summary Report - **NEEDS DETAIL**
- [ ] AI Item Suggestions for Transfers - **NEEDS DETAIL**

### 7.2 Manual Depletions
- [x] Depletion Creation - **COVERED**
- [x] Depletion Line Items - **COVERED**
- [x] Depletion Types (Sold, Spilled, Wasted, Manual) - **COVERED**
- [x] Department-Aware Depletions - **COVERED**
- [x] Depletion Date Tracking - **COVERED**
- [x] Depletion Source Tracking - **COVERED**
- [ ] Managing Depletions - **NEEDS DETAIL**
- [ ] Depletion Details Report - **NEEDS DETAIL**
- [ ] Depletion Summary Report - **NEEDS DETAIL**

---

## 8. REPORTING & ANALYTICS

### 8.1 Reporting System
- [x] Analytics Dashboard - **COVERED**
- [x] Department-Filterable Reports - **COVERED**
- [x] Location-Level Reports - **COVERED**
- [x] Multi-Location Consolidated Reports - **COVERED**
- [x] Scheduled Reports - **COVERED**
- [x] Custom Report Builder (mentioned in improvements) - **COVERED**
- [x] Report Export (PDF, Excel, CSV - mentioned in improvements) - **COVERED**
- [ ] Favorite Reports - **NEEDS DETAIL**
- [ ] View Favorite Reports Only - **NEEDS DETAIL**
- [ ] Analytics Heartbeat - **NEEDS DETAIL**
- [ ] Analytics Overview - **NEEDS DETAIL**
- [ ] Analytic Reports Deep Dive - **NEEDS DETAIL**

### 8.2 Report Types (50+ Reports Identified) - **PHASE 2 - NEXT PRIORITY**
- [x] Inventory Reports:
  - [x] Historic Inventory Summary Report - **COVERED**
  - [ ] Historic Inventory Details Report - **NEEDS DETAIL**
  - [ ] Last Audit Summary Report - **NEEDS DETAIL**
  - [ ] Item Audit Report - **NEEDS DETAIL**
  - [ ] Inventory Cost Details Report - **NEEDS DETAIL**
  - [ ] Item Report - **NEEDS DETAIL**
  - [ ] Viewing Individual Item History - **NEEDS DETAIL**

- [x] Cost Reports:
  - [x] Actual vs Theoretical Summary Report - **COVERED**
  - [ ] Actual vs Theoretical Cost Summary Report - **NEEDS DETAIL**
  - [ ] Actual vs Theoretical Cost Details Report - **NEEDS DETAIL**
  - [ ] Actual vs Theoretical Quantity Details Report - **NEEDS DETAIL**
  - [ ] Actual vs Theoretical COGS by Ops Group Report - **NEEDS DETAIL**
  - [ ] Cost Summary Report - **NEEDS DETAIL**
  - [ ] Cost Details Report - **NEEDS DETAIL**
  - [ ] Cost Summary by Category Report - **NEEDS DETAIL**
  - [ ] Cost Summary by Subcategory Report - **NEEDS DETAIL**
  - [ ] Cost Summary by Ops Group - **NEEDS DETAIL**
  - [ ] Current Cost Summary Report - **NEEDS DETAIL**
  - [ ] Theoretical Costs Report - **NEEDS DETAIL**
  - [ ] Theoretical Cost vs Sales - **NEEDS DETAIL**

- [ ] Procurement Reports:
  - [ ] Purchase Log Report - **NEEDS DETAIL**
  - [ ] Purchases by Item Report - **NEEDS DETAIL**
  - [ ] Purchases by Vendor Report - **NEEDS DETAIL**
  - [ ] Best Price Report - **NEEDS DETAIL**
  - [ ] Average Price Details Report - **NEEDS DETAIL**
  - [ ] CU Price Comparison Report - **NEEDS DETAIL**
  - [ ] Price Details Report - **NEEDS DETAIL**
  - [ ] Receiving Orders Details Report - **NEEDS DETAIL**
  - [ ] Consolidated Purchases by Vendor Report (Director) - **NEEDS DETAIL**
  - [ ] Consolidated Purchases by Category Report (Director) - **NEEDS DETAIL**

- [ ] Recipe Reports:
  - [ ] Recipe Sales Report - **NEEDS DETAIL**
  - [ ] Weekly Recipe Sales Report - **NEEDS DETAIL**
  - [ ] Recipe Reprice Report - **NEEDS DETAIL**
  - [ ] Recipes with Inactive Items Report - **NEEDS DETAIL**
  - [ ] Recipe Sync Analysis Report (Director) - **NEEDS DETAIL**

- [ ] Sales Reports:
  - [ ] Sales Summary Report - **NEEDS DETAIL**
  - [ ] Sales Details Report - **NEEDS DETAIL**
  - [ ] Sales by Item Report - **NEEDS DETAIL**
  - [ ] Sales by Hour Report - **NEEDS DETAIL**
  - [ ] POS Item Sales Report - **NEEDS DETAIL**
  - [ ] Daily Sales Report (DSR) Setup - **NEEDS DETAIL**
  - [ ] Profit by Server Report - **NEEDS DETAIL**
  - [ ] Menu Engineering Report - **NEEDS DETAIL**
  - [ ] Product Mix Report (Director) - **NEEDS DETAIL**

- [ ] Invoice Reports:
  - [ ] Invoice Summary Report - **NEEDS DETAIL**
  - [ ] Invoice Log Report - **NEEDS DETAIL**
  - [ ] Raw Invoice Log Report - **NEEDS DETAIL**
  - [ ] Bill Summary Report - **NEEDS DETAIL**

- [ ] Transfer Reports:
  - [ ] Transfer Log Report - **NEEDS DETAIL**
  - [ ] Transfer Summary Report - **NEEDS DETAIL**

- [ ] Depletion Reports:
  - [ ] Depletion Details Report - **NEEDS DETAIL**
  - [ ] Depletion Summary Report - **NEEDS DETAIL**
  - [ ] Consumption Details Report - **NEEDS DETAIL**

- [ ] Variance Reports:
  - [ ] Variance Details Report - **NEEDS DETAIL**
  - [ ] Comparing Audits (Audit Comparison Report) - **NEEDS DETAIL**

- [ ] Financial Reports:
  - [ ] Profit and Loss Report - **NEEDS DETAIL**
  - [ ] Prime Cost Report - **NEEDS DETAIL**
  - [ ] GL Summary Report - **NEEDS DETAIL**
  - [ ] GL Distribution Report - **NEEDS DETAIL**

- [ ] Director Reports:
  - [ ] Historic Contract Price Violations Report (Director) - **NEEDS DETAIL**

### 8.3 Analytics
- [ ] **DEFERRED**: Logbook Functionality - **COVERED**
- [ ] **DEFERRED**: Logbook Notes - **COVERED**
- [ ] **DEFERRED**: Logbook Tasks - **COVERED**
- [ ] **DEFERRED**: Sales Forecasting (mentioned in improvements) - **COVERED**
- [ ] **DEFERRED**: Predictive Analytics (mentioned in improvements) - **COVERED**
- [ ] **DEFERRED**: Logbook Overview - **NEEDS DETAIL**
- [ ] **DEFERRED**: Logbook Email - **NEEDS DETAIL**
- [ ] **DEFERRED**: Logbook How to Log a Task - **NEEDS DETAIL**
- [ ] Dashboard Sales Trends - **NEEDS DETAIL**
- [ ] Dashboard COGS Trends - **NEEDS DETAIL**
- [ ] Dashboard Inventory Trends - **NEEDS DETAIL**

---

## 9. MULTI-LOCATION MANAGEMENT (DIRECTOR MODULE)

### 9.1 Store Synchronization
- [x] Store Sync Functionality - **COVERED**
- [x] Vendor Sync (Director → Stores) - **COVERED**
- [x] Product Sync (Director → Stores) - **COVERED**
- [x] Recipe Sync (Director → Stores) - **COVERED**
- [x] Sync History Tracking - **COVERED**
- [x] Sync Audit Trail - **COVERED**
- [ ] Director Configuration and Sync Settings - **NEEDS DETAIL**
- [ ] Syncing Director Items - **NEEDS DETAIL**
- [ ] Syncing Director Menu Lists & Recipes Using Markets - **NEEDS DETAIL**
- [ ] Creating/Syncing Corporate Vendors - **NEEDS DETAIL**
- [ ] Managing Vendors at Director - **NEEDS DETAIL**
- [ ] Director Corporate Budgets - **NEEDS DETAIL**
- [ ] Director Item Purchase Unit Pricing - **NEEDS DETAIL**
- [ ] Director Managing Corporate Categories - **NEEDS DETAIL**
- [ ] Director Purchase Unit Manager (PU Manager) - **NEEDS DETAIL**
- [ ] Director Team Accounts - **NEEDS DETAIL**
- [ ] Director Out of Office - **NEEDS DETAIL**
- [ ] Director Training Overview - **NEEDS DETAIL**
- [ ] Managing Contract Price Violations at Director Level - **NEEDS DETAIL**
- [ ] Matching Commissary Price List Items or Batches at Director - **NEEDS DETAIL**

### 9.2 Consolidated Management
- [x] Corporate Vendor Management - **COVERED**
- [x] Corporate Item Management - **COVERED**
- [x] Corporate Recipe Management - **COVERED**
- [x] Consolidated Reporting - **COVERED**
- [x] Multi-Store Analytics - **COVERED**
- [ ] Subsidiaries - **NEEDS DETAIL**
- [ ] Portions (Director) - **NEEDS DETAIL**

### 9.3 Commissary Management - **FUTURE PHASE (Not Needed Right Now)**
- [ ] **DEFERRED**: Commissary Setup Overview - **FUTURE PHASE**
- [ ] **DEFERRED**: Building Your Commissary's Vendor List - **FUTURE PHASE**
- [ ] **DEFERRED**: Creating/Assigning Your Commissary as a Vendor - **FUTURE PHASE**
- [ ] **DEFERRED**: Setting Sales Rep Details for Commissary - **FUTURE PHASE**
- [ ] **DEFERRED**: Adding Items/Batches to Commissary Price List - **FUTURE PHASE**
- [ ] **DEFERRED**: Matching Commissary Price List Items or Batches at Director - **FUTURE PHASE**
- [ ] **DEFERRED**: How to Add Commissary Items and Batches to Store Recipes - **FUTURE PHASE**
- [ ] **DEFERRED**: Ordering from Your Commissary - **FUTURE PHASE**
- [ ] **DEFERRED**: Ship to Store Commissary - **FUTURE PHASE**

---

## 10. USER MANAGEMENT & PERMISSIONS

### 10.1 User Access Control
- [x] Department-Based Permissions - **COVERED**
- [x] User-to-Department Assignment - **COVERED**
- [x] Multi-Department Access - **COVERED**
- [x] Permission Restrictions (cannot modify outside access) - **COVERED**
- [x] Role-Based Access Control (RBAC) - **COVERED**
- [x] Field-Level Permissions - **COVERED**
- [x] Document-Level Permissions - **COVERED**
- [ ] Team Accounts & Permissions Guide - **NEEDS DETAIL**
- [ ] Managing Team Accounts - **NEEDS DETAIL**
- [ ] Single Sign-On with Okta - **NEEDS DETAIL**
- [ ] How to Login to Craftable - **NEEDS DETAIL**

### 10.2 User Roles (Detailed Permissions)
- [ ] Account Owner (Full Admin)
- [ ] Audit/Inventory Taker Only
- [ ] Audit/Inventory Administrator
- [ ] Recipe Builder/Chef
- [ ] Buyer/Purchasing/Order Placer
- [ ] Receiver/Head of Purchasing & Procurement
- [ ] Bartender
- [ ] High-Level Roles (GM, AM, Admin, IT)
- [ ] Director Operations Permissions
- [ ] Manage Other Directors' Permissions

### 10.3 Permission Categories (50+ Permissions Identified)
- [ ] Orders Permissions (15 permissions) - **NEEDS DETAIL**
- [ ] Invoices Permissions (13 permissions) - **NEEDS DETAIL**
- [ ] Keg Tracker Access - **NEEDS DETAIL**
- [ ] Audits Permissions (8 permissions) - **NEEDS DETAIL**
- [ ] Depletions Permissions (4 permissions) - **NEEDS DETAIL**
- [ ] Transfers Permissions (4 permissions) - **NEEDS DETAIL**
- [ ] Reports Permissions (4 permissions) - **NEEDS DETAIL**
- [ ] POS Permissions (2 permissions) - **NEEDS DETAIL**
- [ ] Items Permissions (7 permissions) - **NEEDS DETAIL**
- [ ] Vendors Permissions (6 permissions) - **NEEDS DETAIL**
- [ ] View Subscription Invoices - **NEEDS DETAIL**
- [ ] View Activity Log - **NEEDS DETAIL**
- [ ] Manage Team Accounts - **NEEDS DETAIL**
- [ ] Edit Budgets - **NEEDS DETAIL**
- [ ] All Menu Pricing Permissions - **NEEDS DETAIL**
- [ ] Pours Permissions (2 permissions) - **NEEDS DETAIL**
- [ ] Recipes Permissions (3 permissions) - **NEEDS DETAIL**
- [ ] Preps Permissions (3 permissions) - **NEEDS DETAIL**
- [ ] Modifier Permissions (2 permissions) - **NEEDS DETAIL**
- [ ] Item Tags Permissions (4 permissions) - **NEEDS DETAIL**
- [ ] Store Settings Permissions (3 permissions) - **NEEDS DETAIL**
- [ ] Item Manager Permissions (4 permissions) - **NEEDS DETAIL**
- [ ] Dashboard Trends Permissions (3 permissions) - **NEEDS DETAIL**
- [ ] All Director Reviews Permissions (4 permissions) - **NEEDS DETAIL**
- [ ] All Markets Permissions (3 permissions) - **NEEDS DETAIL**
- [ ] All Menu Lists Permissions (3 permissions) - **NEEDS DETAIL**
- [ ] Director Operations Permissions (8 permissions) - **NEEDS DETAIL**
- [ ] View All Director Dashboard Trends (3 permissions) - **NEEDS DETAIL**

---

## 11. BUDGET MANAGEMENT

### 11.1 Budget Setup
- [ ] Budget Definition (per department)
- [ ] Budget Period Setup
- [ ] Budget vs Actual Tracking
- [ ] Budget Reporting
- [ ] Budget Roll-Up (consolidated review)
- [ ] Using Budgets
- [ ] Creating/Editing Budgets at Store Level
- [ ] Cross-Platform Budgets
- [ ] Director Corporate Budgets
- [ ] Orders with Budgets
- [ ] Declining Budgets
- [ ] Edit Budgets Permission

---

## 12. WORKFLOWS & APPROVALS

### 12.1 Approval Workflows
- [x] Workflow Engine (Frappe built-in) - **COVERED**
- [ ] **DEFERRED**: Purchase Order Approval Workflow Details - **FUTURE PHASE** (Not needed - no A/P in system)
- [ ] **DEFERRED**: Invoice Approval Workflow Details - **FUTURE PHASE** (Not needed - A/P in Ottimate)
- [ ] **DEFERRED**: Transfer Approval Workflow Details - **FUTURE PHASE** (May be needed later)
- [ ] **DEFERRED**: Payment Approval Workflow Details - **FUTURE PHASE** (Not needed - payments in Ottimate)
- [ ] **DEFERRED**: Audit Approval Workflow Details - **FUTURE PHASE** (May be needed later)
- [ ] **DEFERRED**: Multi-User Order Approval - **FUTURE PHASE**
- [ ] **DEFERRED**: Approve/Reject Orders (Director) - **FUTURE PHASE**
- [ ] **DEFERRED**: Reject Invoices (Director) - **FUTURE PHASE**
- [ ] **DEFERRED**: Approve/Reject Bills & Credits (Director) - **FUTURE PHASE**
- [ ] **DEFERRED**: Acknowledge Price Violations (Director) - **FUTURE PHASE**
- [ ] **DEFERRED**: Multi-Level Approval Routing - **FUTURE PHASE**
- [ ] **DEFERRED**: Approval Notification System - **FUTURE PHASE**

---

## 13. ADDITIONAL FEATURES

### 13.1 Email Integration
- [x] Email Integration (Frappe built-in) - **COVERED**
- [ ] **DEFERRED**: IMAP Integration (for receiving invoices) - **COVERED**
- [ ] **DEFERRED**: Automated Invoice Email Processing Workflow - **COVERED**
- [ ] **DEFERRED**: Order Notifications (Email/Text) - **NEEDS DETAIL**
- [ ] **DEFERRED**: Invoice Notifications - **NEEDS DETAIL**
- [ ] Transfer Notifications - **NEEDS DETAIL**
- [ ] **DEFERRED**: Logbook Email - **NEEDS DETAIL**

### 13.2 Document Management
- [ ] Invoice Image Storage - **COVERED**
- [x] Product Image Storage - **COVERED**
- [x] Recipe Image Storage - **COVERED**
- [x] File Attachments - **COVERED**
- [x] Document Versioning (Frappe built-in) - **COVERED**
- [ ] **DEFERRED**: Image Vault - **NEEDS DETAIL**
- [ ] **DEFERRED**: Uploading Invoice Images for Electronic Invoicing - **NEEDS DETAIL**

### 13.3 Data Import/Export
- [x] Excel Export/Import (pandas, openpyxl) - **COVERED**
- [x] CSV Export/Import - **COVERED**
- [x] PDF Generation - **COVERED**
- [ ] Exporting Inventory Items to Excel - **NEEDS DETAIL**
- [ ] Item Loader (Bulk Import) - **NEEDS DETAIL**
- [ ] Express Loader - **NEEDS DETAIL**
- [ ] Preparing for Your Sheet Review - Loading Items into Craftable - **NEEDS DETAIL**
- [ ] Bulk Import Templates - **NEEDS DETAIL**
- [ ] Data Migration Tools - **NEEDS DETAIL**

### 13.4 Mobile Support
- [x] Mobile-Friendly Interface (Frappe responsive) - **COVERED**
- [x] Mobile Counting Interface - **COVERED**
- [ ] Progressive Web App (PWA) - mentioned in improvements - **NEEDS DETAIL**
- [ ] Offline Functionality - **NEEDS DETAIL**
- [ ] Barcode Scanning - **NEEDS DETAIL**

### 13.5 Notifications
- [x] Notification System Documentation - **COVERED** (Basic)
- [x] Email Notifications - **COVERED**
- [x] In-App Notifications - **COVERED**
- [ ] Notification Preferences - **NEEDS DETAIL**
- [ ] **DEFERRED**: Invoice Processing Notifications - **NEEDS DETAIL**
- [ ] **DEFERRED**: Order Notifications - **NEEDS DETAIL**

### 13.6 Store Settings
- [x] Update Store Settings Permission - **COVERED**
- [ ] Store Info Management - **NEEDS DETAIL**
- [x] Inventory Storages Management - **COVERED**
- [x] Item Categories Management - **COVERED**
- [ ] **DEFERRED**: Order Notifications Configuration - **NEEDS DETAIL**
- [ ] Setting Up Par Levels - **NEEDS DETAIL**
- [ ] Configuration of Pars Levels EOQ - **NEEDS DETAIL**
- [ ] Managing Pars from Item Manager - **NEEDS DETAIL**
- [ ] Setting Bins - **NEEDS DETAIL**
- [ ] **DEFERRED**: Setting Up Recurring Orders - **NEEDS DETAIL**
- [ ] **DEFERRED**: Setting Up Bill Hold - **NEEDS DETAIL**
- [ ] Setting Up Keg Tracker - **NEEDS DETAIL**
- [ ] Operations Statement Configuration - **NEEDS DETAIL**
- [ ] Ops Group Mappings - **NEEDS DETAIL**
- [ ] Days to Lock Audits (Director Configuration) - **NEEDS DETAIL**

### 13.7 Special Features
- [ ] Wine List Management - **NEEDS DETAIL**
- [ ] Managing Corked Wine Bottles - **NEEDS DETAIL**
- [ ] Wine Vintages POS Item Mapping - **NEEDS DETAIL**
- [x] Setting Pours - **COVERED** (Section 25.7)
- [x] Creating Pours - **COVERED**
- [ ] Understanding Promo Threshold - **NEEDS DETAIL**
- [ ] Understanding CU Price - **NEEDS DETAIL**
- [ ] Understanding Yields - **NEEDS DETAIL**
- [ ] Secondary Count Units - **NEEDS DETAIL**
- [ ] Catch Weight for Purchase Units - **NEEDS DETAIL**
- [ ] Weight Capture for Purchase Units - **NEEDS DETAIL**
- [ ] Contract Price Violations - **NEEDS DETAIL**
- [ ] Historic Contract Price Violations Report - **NEEDS DETAIL**
- [ ] Managing Contract Price Violations at Director Level - **NEEDS DETAIL**
- [ ] Viewing Individual Item History - **NEEDS DETAIL**
- [ ] Viewing Vendor Invoice History - **NEEDS DETAIL**
- [ ] What is the Activity Log - **NEEDS DETAIL**
- [ ] How to Get The Most Out of BLKSHP - **NEEDS DETAIL**
- [ ] Nutrition Function - **NEEDS DETAIL**

---

## SUMMARY STATISTICS

**Total Features Identified:** 400+  
**Features Covered in FRAPPE_IMPLEMENTATION_PLAN.md:** ~300+ (Core functionality, architecture, major systems, and Phase 4 enhancements)  
**Features Needing Detail/Verification:** ~100+ (Operational workflows, advanced reporting details, future phases)  
**Critical Gaps Identified:** 0 (All critical gaps have been addressed in Phases 1-4)  

**Implementation Status:**
- **Sections 1-11**: Core architecture and framework overview
- **Section 12**: User Roles & Permissions - COMPLETED
- **Section 13**: Budget Management - COMPLETED
- **Section 14**: Report Types - COMPLETED
- **Section 15**: Ottimate Integration - COMPLETED
- **Section 16**: Inventory Transfers - COMPLETED
- **Section 17**: Depletion Tracking - COMPLETED
- **Section 18**: Recipe Costing & Batch Management - COMPLETED
- **Section 19**: Theoretical Inventory Calculations - COMPLETED
- **Section 20**: POS Integration - COMPLETED
- **Section 21**: PMS Integration - COMPLETED (Later Phase)
- **Section 22**: Enhanced Vendor Management - COMPLETED
- **Section 23**: Product Management Enhancements - COMPLETED
- **Section 24**: Inventory Auditing Enhancements - COMPLETED
- **Section 25**: Recipe Management Enhancements - COMPLETED

**Phase 4 Complete - All Priorities Completed:**
- ✅ Product Management Enhancements (Section 23)
- ✅ Inventory Auditing Enhancements (Section 24)
- ✅ Recipe Management Enhancements (Section 25)

---

## CRITICAL GAPS REQUIRING IMMEDIATE ATTENTION

### Phase 1 (COMPLETED):

1. ✅ **User Roles & Permissions** - **COMPLETED** (Section 12)
   - Detailed role definitions and permissions matrix (50+ permissions)
   - Flexible role system with custom role creation
   - User-level permission overrides
   - Department-based access control

2. ✅ **Budget Management** - **COMPLETED** (Section 13)
   - Budget definition and setup
   - Budget vs actual tracking
   - Budget reporting and variance analysis
   - Department-level budgets

3. ✅ **Report Types** - **COMPLETED** (Section 14)
   - Catalog of 50+ report types
   - Report parameters and filters
   - Report scheduling capabilities

### Phase 2 (COMPLETED):

4. ✅ **Ottimate Integration** - **COMPLETED** (Section 15)
   - Flatfile import process from Ottimate exports
   - Persistent item mapping system
   - Review workflow for unmapped items
   - Inventory update based on receiving activity
   - Note: Invoices and A/P managed in Ottimate (not in this system)

### Phase 3 (Additional Core Features - COMPLETED):

5. ✅ **Inventory Transfers** - **COMPLETED** (Section 16)
   - Inter-department and inter-store transfers
   - Transfer status tracking and acknowledgment
   - Transfer pricing and cost allocation

6. ✅ **Depletion Tracking** - **COMPLETED** (Section 17)
   - Manual depletions (waste, spillage, consumption)
   - POS-driven automatic depletions
   - Department-based depletion tracking

7. ✅ **Recipe Costing & Batch Management** - **COMPLETED** (Section 18)
   - Dynamic recipe costing with unit conversions
   - Batch production tracking
   - Sub-recipe support
   - Inventory impact from batch production

8. ✅ **Theoretical Inventory Calculations** - **COMPLETED** (Section 19)
   - Enhanced calculations including batch production
   - Department-aware theoretical inventory
   - Real-time variance tracking

9. ✅ **POS Integration** - **COMPLETED** (Section 20)
   - API-based automatic polling
   - Multiple POS instances per location
   - POS item to recipe mapping
   - Automatic depletion from sales

10. ✅ **PMS Integration** - **COMPLETED** (Section 21 - Later Phase)
    - WebRez Pro integration for sales journal automation
    - No inventory impact (financial reporting only)

11. ✅ **Enhanced Vendor Management** - **COMPLETED** (Section 22)
    - Comprehensive vendor master with contact management
    - Ordering rules (minimums, cutoffs, schedules)
    - Vendor vacation settings
    - Vendor tags and mapping

### Phase 4 (Later Phase - After Ottimate Contract, 12+ months):

12. **Receiving Workflow** - Detailed receiving process for orders
    - Detailed receiving workflow
    - Partial receiving
    - Receiving inspection and quality control
    - Manual receiving processes

13. **Ordering Workflows** - Complete ordering system
    - Quick orders, recurring orders
    - Ordering options and workflows
    - Order approval processes
    - Order notifications

14. **Invoice Processing** - Complete invoice management
    - Invoice OCR and AI processing
    - Invoice matching and reconciliation
    - Invoice approval workflows
    - Invoice image vault and email submission

### Future Phases (Deferred):

15. ~~**Approval Workflows**~~ - REMOVED (No A/P or payment processes in system currently)
16. ~~**Payment Approval**~~ - REMOVED (Payments handled in Ottimate, later phase)
17. **Commissary Management** - DEFERRED to next phase of development
18. **Operational Workflows** - DEFERRED until after functionality and development plans are detailed

---

## RECOMMENDATIONS

### Phase 4 (COMPLETED - Current Development):

1. ✅ **COMPLETED**: Product Management Enhancements (Section 23) - Operational product management features
   - Bulk import/export (Item Loader, Express Loader)
   - Item history tracking and audit trail
   - Item notes and internal notes
   - Item ID management (multiple SKUs, barcode support)
   - Substitute items management
   - Item labels and printing
   - Catch weight and weight capture for purchase units
   - Contract price violations tracking
   - Promo threshold management
   - Item bins and storage assignments
   - Item export to Excel

2. ✅ **COMPLETED**: Inventory Auditing Enhancements (Section 24) - Advanced audit workflow features
   - Flagging audit items for recount
   - Unsaved counts management and recovery
   - Audit deletion and restoration
   - Reopening closed audits
   - Opening locked audits (with proper authorization)
   - Updating closed audits (with change tracking)
   - Correcting previous audits
   - Updating item CU price on closed audit
   - Audit comparison reporting
   - Days to lock audits (Director configuration)

3. ✅ **COMPLETED**: Recipe Management Enhancements (Section 25) - Additional recipe features
   - Recipe allergens and inherited allergens
   - Recipe line swap functionality
   - Recipe printing and menu list printing
   - Creating/editing menu lists
   - Recipe reprice reporting
   - Setting pours (beverage-specific)
   - Counting prep items and batches in audits

### Phase 5 (Future Operational Features):

4. **Accounting Integration** - External accounting system connectivity
   - QuickBooks Online/Desktop integration
   - Restaurant365 (R365) integration
   - Sage Intacct API integration
   - GL account mapping and sync
   - Bill syncing to accounting systems
   - Credits, charges, and taxes handling

5. **Mobile Features** - Enhanced mobile capabilities
   - Progressive Web App (PWA) support
   - Offline functionality
   - Barcode scanning integration
   - Mobile-optimized counting interface

6. **Notification System** - User communication features
   - Real-time notifications
   - Email notifications
   - Task assignments and alerts
   - Report scheduling and delivery

### Phase 6 (Later Phase - After Ottimate Contract, 12+ months):
7. **Receiving Workflow** - Detailed receiving process for orders
   - Detailed receiving workflows
   - Partial receiving
   - Receiving inspection and quality control
8. **Ordering Workflows** - Complete ordering system
   - All ordering features and workflows
9. **Invoice Processing** - Complete invoice management
   - All invoice processing features

### Future Phases (Deferred):
10. ~~**Approval Workflows**~~ - REMOVED (No A/P in BLKSHP)
11. ~~**Payment Approval**~~ - REMOVED (Payments in Ottimate)
12. **Commissary Management** - Next phase of development
13. **Advanced Analytics Features** - Predictive analytics, ML-based forecasting
14. **Special Features** - Wine management, nutrition tracking, etc.
15. **Troubleshooting Guides** - User documentation and help system

---

**Completed Phases:**

**Phase 1 (COMPLETED):**
1. ✅ **COMPLETED**: Reviewed and prioritized critical gaps
2. ✅ **COMPLETED**: User Roles & Permissions system (Section 12)
   - Flexible role system with custom role creation
   - User-level permission overrides
   - 50+ permissions catalog with department-based access control
3. ✅ **COMPLETED**: Budget Management system (Section 13)
   - Budget setup, tracking, and reporting
   - Department-level budgets with variance analysis
4. ✅ **COMPLETED**: Report Types catalog (Section 14)
   - 50+ report types with parameters and filters
   - Report scheduling capabilities

**Phase 2 (COMPLETED):**
5. ✅ **COMPLETED**: Ottimate Integration (Section 15)
   - Flatfile import with persistent item mapping
   - Review workflow for unmapped items
   - Inventory update based on receiving activity

**Phase 3 (COMPLETED - Additional Core Features):**
6. ✅ **COMPLETED**: Inventory Transfers (Section 16)
   - Inter-department and inter-store transfers
   - Transfer status tracking and acknowledgment
7. ✅ **COMPLETED**: Depletion Tracking (Section 17)
   - Manual and POS-driven automatic depletions
   - Department-based tracking
8. ✅ **COMPLETED**: Recipe Costing & Batch Management (Section 18)
   - Dynamic recipe costing with unit conversions
   - Batch production tracking with inventory impact
9. ✅ **COMPLETED**: Theoretical Inventory Calculations (Section 19)
   - Enhanced calculations including batch production
   - Department-aware theoretical inventory
10. ✅ **COMPLETED**: POS Integration (Section 20)
    - API-based automatic polling with multiple POS instances
    - POS item to recipe mapping
11. ✅ **COMPLETED**: PMS Integration (Section 21 - Later Phase)
    - WebRez Pro integration for sales journal automation
12. ✅ **COMPLETED**: Enhanced Vendor Management (Section 22)
    - Comprehensive vendor master with contact management
    - Ordering rules, vacation settings, tags

**Phase 4 (COMPLETED - Current Development):**
1. ✅ **COMPLETED**: Product Management Enhancements (Section 23) - Priority 1
   - Bulk import/export (Item Loader, Express Loader)
   - Item history tracking, notes, and audit trail
   - Substitute items, labels, multiple SKUs
   - Catch weight, contract price violations, promo thresholds
   - Item bins and storage assignments

2. ✅ **COMPLETED**: Inventory Auditing Enhancements (Section 24) - Priority 2
   - Flagging items for recount
   - Unsaved counts management and recovery
   - Audit corrections, reopening, and locking configuration
   - Audit comparison reporting
   - Automatic audit locking

3. ✅ **COMPLETED**: Recipe Management Enhancements (Section 25) - Priority 3
   - Allergens and inherited allergens
   - Recipe printing and menu list printing
   - Menu list creation and management
   - Recipe reprice reporting
   - Pour settings (beverage-specific)
   - Prep items and batch counting in audits

**Next Steps (Phase 5 - Future Operational Features):**

**Key Decisions Made:**
- ✅ **Architecture**: Unified platform with department-based segmentation (not separate platforms)
- ✅ **Inventory Model**: 2D model (Product + Department), storage as metadata
- ✅ **Audit System**: Task-based two-phase system (setup by manager, counting by department users)
- ✅ **A/P and Payments**: Handled in Ottimate (not in BLKSHP system)
- ✅ **Approval Workflows**: Removed (not needed without A/P)
- ✅ **Vendor Portal**: Removed (not needed)
- ✅ **Vendor Catalog Integrations**: Removed (not needed at this time)
- ✅ **Receiving, Ordering, Invoice Processing**: Deferred to Phase 6 (12+ months after Ottimate contract)
- ✅ **Ottimate Integration**: Completed - flatfile import with persistent mapping system
- ✅ **Commissary Management**: Deferred to future phase
- ✅ **Operational Workflows**: Deferred until after functionality planning
- ✅ **Role System**: Flexible, not hard-coded - standard roles as templates, custom roles allowed
- ✅ **User Permissions**: User-level overrides supported, independent of role assignments
- ✅ **POS Integration**: Multiple POS instances per location supported (e.g., Toast for restaurant and retail)
- ✅ **PMS Integration**: WebRez Pro integration planned for sales journal automation (no inventory impact)
- ✅ **Vendor Management**: Enhanced with comprehensive contact management, ordering rules, vacation settings
