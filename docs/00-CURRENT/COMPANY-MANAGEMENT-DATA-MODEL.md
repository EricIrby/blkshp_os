# Company Management Data Model Design
**Issue:** BLK-73 (Design-001)
**Date:** 2025-11-16
**Status:** Design Complete
**Author:** Development Team

---

## Table of Contents
1. [Overview](#overview)
2. [DocType Schemas](#doctype-schemas)
   - [Company DocType](#1-company-doctype-enhanced)
   - [Banking Institution](#2-banking-institution-doctype)
   - [Company Bank Relationship](#3-company-bank-relationship-doctype)
   - [Bank Account](#4-bank-account-doctype)
   - [Tax Authority](#5-tax-authority-doctype)
   - [Company Tax Authority Relationship](#6-company-tax-authority-relationship-doctype)
   - [Tax Obligation](#7-tax-obligation-doctype)
   - [Insurance Broker](#8-insurance-broker-doctype)
   - [Insurance Carrier](#9-insurance-carrier-doctype)
   - [Premium Finance Provider](#10-premium-finance-provider-doctype)
   - [Insurance Policy](#11-insurance-policy-doctype)
   - [Loan Relationship](#12-loan-relationship-doctype)
   - [Key Employee Relationship](#13-key-employee-relationship-doctype)
   - [Task Type](#14-task-type-doctype)
   - [Review Period](#15-review-period-doctype)
   - [Project](#16-project-doctype)
   - [Platform Feature](#17-platform-feature-doctype)
   - [Subscription Plan](#18-subscription-plan-doctype)
3. [Feature Registry](#feature-registry)
4. [Entity Relationships](#entity-relationships)
5. [Validation Rules](#validation-rules)
6. [Security Considerations](#security-considerations)
7. [Implementation Notes](#implementation-notes)

---

## Overview

This document defines the complete data model for the Company Management MVP. All schemas follow Frappe Framework v15+ conventions and best practices.

**Data Model Scope:**
- **18 Main DocTypes** (Company, Banking Institution, Company Bank Relationship, Bank Account, Tax Authority, Company Tax Authority Relationship, Tax Obligation, Insurance Broker, Insurance Carrier, Premium Finance Provider, Insurance Policy, Loan Relationship, Key Employee Relationship, Task Type, Review Period, Project, Platform Feature, Subscription Plan)
- **24 Child Tables** (for addresses, contacts, documents, phone numbers, emails, websites, company features, covered entities, covered locations, filing documents, loan amortization schedules, plan features, dependencies, milestones, and tasks)
- **Total: 42 DocTypes** designed with normalized database structure following 3rd normal form and feature-based subscription architecture

**Normalized Architecture:**
The data model follows a consistent three-tier pattern for shared entities:
1. **Master Entities** (Banking Institution, Tax Authority, Insurance Broker, Insurance Carrier, Premium Finance Provider) - Shared across companies
2. **Junction Entities** (Company Bank Relationship, Company Tax Authority Relationship) - Link companies to master entities
3. **Specific Records** (Bank Account, Tax Obligation, Insurance Policy) - Company-specific instances

**Feature-Based Subscription Architecture:**
The platform implements a flexible feature-based subscription system that allows granular control over functionality:

**Core Concept:**
- Individual features can be enabled/disabled per company
- Features can be bundled into subscription plans OR configured à la carte
- Supports both pre-built plans AND custom feature combinations
- "Build your own" flexibility with optional pre-packaged convenience

**Feature Categories:**

**Basic Features (Free/Included):**
- Core data entry and storage
- Basic task automation (recurrence-based)
- Standard reporting
- Manual workflows
- Basic CRUD operations

**Premium Features (Paid Add-ons):**
- Detailed child tables (e.g., Loan Amortization Schedules)
- Auto-calculations (balances, interest, projections)
- Payment variance analysis
- Advanced automation
- Predictive alerts

**Enterprise Features (High-tier):**
- General Ledger (GL) integration
- Auto-drafted journal entries
- Multi-entity consolidation
- Advanced reporting and analytics
- Custom integrations

**Implementation Pattern:**
- Each feature has a unique `feature_code` (e.g., `loan_amortization_schedules`)
- Server-side: Check `has_feature(company, feature_code)` before executing feature logic
- Frontend: Conditionally render based on enabled features
- API: Filter data and endpoints based on feature access
- Company DocType tracks enabled features via:
  - `subscription_plan` (optional Link to pre-built plan)
  - `Company Feature` child table (granular feature tracking)

**Subscription Plans (Optional Bundles):**
Plans are pre-configured bundles of features (e.g., "Starter", "Professional", "Enterprise")
- Companies can subscribe to a plan (gets all plan features)
- OR companies can enable individual features custom
- OR mix both (plan + additional à la carte features)

**This pattern applies to: ALL modules (Company Management, Inventory, Procurement, Recipes, POS, Accounting, Analytics, and future modules)**

**Detailed feature codes and feature-specific functionality are documented in each DocType section below.**

### Key Principles
- **Master-Detail Pattern:** Company is the master, relationships are details
- **Data Integrity:** All relationships link to Company via `Link` field type
- **Security:** Sensitive fields (EIN, account numbers) use encryption
- **Validation:** Field-level and document-level validation rules
- **Audit Trail:** All DocTypes enable `track_changes` and `track_seen`
- **Extensibility:** Designed to support future multi-location features

---

## DocType Schemas

### 1. Company DocType (Enhanced)

**Module:** Director
**DocType Name:** Company
**Naming:** `field:company_code`
**Features:** Feature-001

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company_name` | Data | Company Name | Yes | No | - | Display name of company |
| `company_code` | Data | Company Code | Yes | Yes | - | Unique identifier (e.g., "ACM", "GHD") |
| `legal_name` | Data | Legal Name | Yes | No | - | Full legal entity name |
| `dba_name` | Data | DBA Name | No | No | - | "Doing Business As" name |
| `ein` | Password | EIN/Tax ID | Yes | Yes | - | Encrypted federal tax ID |
| `is_active` | Check | Is Active | No | No | 1 | Active status |
| `subscription_plan` | Link | Subscription Plan | No | No | - | Link to Subscription Plan (optional - for pre-built plans) |
| `entity_type` | Select | Entity Type | Yes | No | - | LLC, Corporation, Partnership, Sole Proprietorship, Other |
| `formation_date` | Date | Formation Date | No | No | - | Date entity was formed |
| `state_of_formation` | Data | State of Formation | No | No | - | State where entity was formed |
| `fiscal_year_start` | Data | Fiscal Year Start | No | No | "January" | Month when fiscal year starts |
| `default_currency` | Link | Default Currency | Yes | No | "USD" | Link to Currency |
| **Section: Ownership** |
| `parent_company` | Link | Parent Company | No | No | - | Link to Company (self-link) |
| `ownership_structure` | Small Text | Ownership Structure | No | No | - | Description of ownership |
| **Section: Additional** |
| `description` | Small Text | Description | No | No | - | General notes/description |

#### Child Tables

**Company Address** (Child Table: `Company Address`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `address_type` | Select | Address Type | Yes | - | Billing, Physical, Mailing, Shipping, Corporate, Branch, Other |
| `address_label` | Data | Address Label | No | - | Custom label (e.g., "Headquarters", "Warehouse 1") |
| `street` | Data | Street | Yes | - | Street address |
| `suite_unit` | Data | Suite/Unit | No | - | Suite, unit, or apartment number |
| `city` | Data | City | Yes | - | City |
| `state` | Data | State | Yes | - | State or province |
| `zip_code` | Data | ZIP Code | Yes | - | Postal/ZIP code |
| `country` | Link | Country | Yes | "United States" | Link to Country |
| `is_primary` | Check | Is Primary | No | 0 | Mark as primary address |

**Company Phone** (Child Table: `Company Phone`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `phone_type` | Select | Phone Type | Yes | - | Office, Mobile, Fax, Toll-Free, Direct, Other |
| `phone_label` | Data | Phone Label | No | - | Custom label (e.g., "Main Office", "Accounting Dept") |
| `phone_number` | Data | Phone Number | Yes | - | Phone number |
| `extension` | Data | Extension | No | - | Phone extension |
| `is_primary` | Check | Is Primary | No | 0 | Mark as primary phone |

**Company Email** (Child Table: `Company Email`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `email_type` | Select | Email Type | Yes | - | Primary, Accounting, Support, Billing, Sales, HR, Other |
| `email_label` | Data | Email Label | No | - | Custom label (e.g., "AP Team", "Controller") |
| `email_address` | Data | Email Address | Yes | - | Email address |
| `is_primary` | Check | Is Primary | No | 0 | Mark as primary email |

**Company Website** (Child Table: `Company Website`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `website_type` | Select | Website Type | Yes | - | Main Website, Customer Portal, Vendor Portal, Internal, Documentation, Other |
| `website_label` | Data | Website Label | No | - | Custom label (e.g., "Corporate Site", "Online Ordering") |
| `url` | Data | URL | Yes | - | Website URL |
| `is_primary` | Check | Is Primary | No | 0 | Mark as primary website |

**Company Feature** (Child Table: `Company Feature`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `feature_code` | Link | Feature Code | Yes | - | Link to Platform Feature |
| `is_enabled` | Check | Is Enabled | No | 1 | Whether this feature is currently enabled |
| `enabled_date` | Date | Enabled Date | No | - | Date when feature was enabled |
| `disabled_date` | Date | Disabled Date | No | - | Date when feature was disabled (if applicable) |
| `source` | Select | Source | Yes | "Plan" | Plan (from subscription_plan), Custom (manually added), Trial (temporary trial) |
| `trial_end_date` | Date | Trial End Date | No | - | If source=Trial, when trial ends |
| `notes` | Small Text | Notes | No | - | Notes about this feature enablement |

#### Validation Rules
1. `ein` must be 9 digits (format: XX-XXXXXXX)
2. `company_code` must be 2-5 uppercase alphanumeric characters
3. `fiscal_year_start` must be valid month name
4. If `parent_company` is set, prevent circular references
5. **Company Address child table:**
   - At least one address with `is_primary` = 1 required
   - Only one address can have `is_primary` = 1
   - `email_address` must be valid email format
   - `zip_code` format validation based on country
6. **Company Phone child table:**
   - At least one phone with `is_primary` = 1 recommended
   - Only one phone can have `is_primary` = 1
   - Phone number format validation (flexible for international)
7. **Company Email child table:**
   - At least one email with `is_primary` = 1 required
   - Only one email can have `is_primary` = 1
   - `email_address` must match email regex pattern
8. **Company Website child table:**
   - Only one website can have `is_primary` = 1
   - `url` must be valid URL format (http:// or https://)

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Read, Write, Create
- **Accountant:** Read only

#### Settings
```json
{
  "autoname": "field:company_code",
  "quick_entry": 1,
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "company_name,legal_name,company_code",
  "title_field": "company_name",
  "sort_field": "company_name",
  "sort_order": "ASC"
}
```

---

### 2. Banking Institution DocType

**Module:** Director
**DocType Name:** Banking Institution
**Naming:** Auto-generated
**Features:** Feature-002
**Note:** Shared master data - multiple companies can have relationships with the same banking institution

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `institution_name` | Data | Institution Name | Yes | Yes | - | Official name of banking institution |
| `institution_type` | Select | Institution Type | Yes | No | - | Commercial Bank, Credit Union, Investment Bank, Online Bank, Other |
| `swift_code` | Data | SWIFT/BIC Code | No | No | - | International bank identifier |
| `website` | Data | Website | No | No | - | Institution website URL |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Banking Institution Address** (Child Table: `Banking Institution Address`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `branch_name` | Data | Branch Name | Yes | - | Branch name or label (e.g., "Downtown Branch", "Main Office") |
| `branch_number` | Data | Branch Number | No | - | Official branch number/code |
| `street` | Data | Street | Yes | - | Street address |
| `suite_unit` | Data | Suite/Unit | No | - | Suite or unit number |
| `city` | Data | City | Yes | - | City |
| `state` | Data | State | Yes | - | State or province |
| `zip_code` | Data | ZIP Code | Yes | - | Postal/ZIP code |
| `country` | Link | Country | Yes | "United States" | Link to Country |
| `phone` | Data | Phone | No | - | Branch phone number |
| `is_headquarters` | Check | Is Headquarters | No | 0 | Mark as headquarters/main office |
| `notes` | Small Text | Notes | No | - | Additional notes |

**Banking Institution Contact** (Child Table: `Banking Institution Contact`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `contact_name` | Data | Contact Name | Yes | - | Full name of contact |
| `title` | Data | Title | No | - | Job title or role |
| `department` | Data | Department | No | - | Department (e.g., Commercial Lending, Treasury) |
| `branch_name` | Data | Branch Name | No | - | Which branch this contact works at (free text or reference to Banking Institution Address.branch_name) |
| `email` | Data | Email | No | - | Contact email address |
| `phone` | Data | Phone | No | - | Contact phone number |
| `extension` | Data | Extension | No | - | Phone extension |
| `is_primary` | Check | Is Primary | No | 0 | Mark as primary contact for entire institution |
| `notes` | Small Text | Notes | No | - | Additional notes |

#### Validation Rules
1. `institution_name` must be unique
2. `website` must be valid URL format if provided
3. **Banking Institution Address child table:**
   - At least one address with `is_headquarters` = 1 recommended
   - Only one address can have `is_headquarters` = 1
4. **Banking Institution Contact child table:**
   - Contact `email` must be valid email format if provided
   - Only one contact can have `is_primary` = 1
   - `branch_name` should match an existing Banking Institution Address.branch_name if provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Create

#### Settings
```json
{
  "autoname": "format:BANK-INST-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "institution_name,institution_type",
  "title_field": "institution_name",
  "sort_field": "institution_name",
  "sort_order": "ASC"
}
```

---

### 3. Company Bank Relationship DocType

**Module:** Director
**DocType Name:** Company Bank Relationship
**Naming:** Auto-generated
**Features:** Feature-002
**Note:** Links a Company to a Banking Institution; accounts are stored in separate Bank Account DocType

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company` | Link | Company | Yes | No | - | Link to Company |
| `banking_institution` | Link | Banking Institution | Yes | No | - | Link to Banking Institution |
| `relationship_start_date` | Date | Relationship Start Date | No | No | - | When relationship began |
| `relationship_end_date` | Date | Relationship End Date | No | No | - | When relationship ended (if applicable) |
| `relationship_status` | Select | Relationship Status | Yes | No | "Active" | Active, Inactive, Closed |
| `primary_contact` | Link | Primary Contact | No | No | - | Link to Banking Institution Contact (from institution's contact child table) |
| `relationship_type` | Select | Relationship Type | No | No | - | Checking/Savings, Lending, Treasury, Investment, Full Service, Other |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes about relationship |

#### Child Tables
None (Accounts are stored in separate Bank Account DocType)

#### Validation Rules
1. Combination of `company` + `banking_institution` should be unique
2. `relationship_end_date` must be >= `relationship_start_date` if provided
3. `relationship_status` should be "Closed" if `relationship_end_date` is set

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read only

#### Settings
```json
{
  "autoname": "format:CBR-{company}-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "company,banking_institution",
  "title_field": "banking_institution",
  "sort_field": "company",
  "sort_order": "ASC"
}
```

---

### 4. Bank Account DocType

**Module:** Director
**DocType Name:** Bank Account
**Naming:** Auto-generated
**Features:** Feature-002
**Note:** Individual bank accounts linked to Company Bank Relationship

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company_bank_relationship` | Link | Company Bank Relationship | Yes | No | - | Link to Company Bank Relationship |
| `account_label` | Data | Account Label | Yes | No | - | Custom label (e.g., "Operating Account", "Payroll Account") |
| `account_id` | Data | Account ID | No | No | - | Internal account identifier |
| `account_type` | Select | Account Type | Yes | No | - | Checking, Savings, Money Market, CD, Other |
| `account_number` | Password | Account Number | Yes | No | - | Encrypted account number (last 4 visible) |
| `routing_number` | Data | Routing Number | No | No | - | Bank routing number (9 digits) |
| `account_status` | Select | Account Status | Yes | No | "Active" | Active, Closed, Dormant, Frozen |
| **Section: Dates & Balance** |
| `opening_date` | Date | Opening Date | No | No | - | Date account was opened |
| `closing_date` | Date | Closing Date | No | No | - | Date account was closed |
| `current_balance` | Currency | Current Balance | No | No | 0.00 | Current account balance |
| `last_reconciled_date` | Date | Last Reconciled Date | No | No | - | Date of last reconciliation |
| **Section: Additional** |
| `online_banking_url` | Data | Online Banking URL | No | No | - | Direct URL to account login |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Bank Account Document** (Child Table: `Bank Account Document`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `document_name` | Data | Document Name | Yes | - | Name/description of document |
| `document_type` | Select | Document Type | Yes | - | Account Opening, Statement, Agreement, Debit Card, Check Image, Wire Confirmation, Other |
| `document_date` | Date | Document Date | No | - | Date of document |
| `file_attachment` | Attach | File Attachment | No | - | Uploaded file |
| `external_url` | Data | External URL | No | - | Link to external document (if not uploaded) |
| `notes` | Small Text | Notes | No | - | Additional notes |

#### Validation Rules
1. `account_number` must be encrypted
2. `routing_number` must be 9 digits if provided
3. `closing_date` must be >= `opening_date` if provided
4. `account_status` must be "Closed" if `closing_date` is set
5. `online_banking_url` must be valid URL if provided
6. In Bank Account Document child table: either `file_attachment` or `external_url` should be provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read only

#### Settings
```json
{
  "autoname": "format:ACCT-{company_bank_relationship}-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "account_label,account_id,account_type",
  "title_field": "account_label",
  "sort_field": "opening_date",
  "sort_order": "DESC"
}
```

---

### 5. Tax Authority DocType

**Module:** Director
**DocType Name:** Tax Authority
**Naming:** Auto-generated
**Features:** Feature-003
**Note:** Shared master data - multiple companies can have relationships with the same tax authority

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `authority_name` | Data | Authority Name | Yes | Yes | - | Official name (e.g., "Internal Revenue Service", "California FTB", "Los Angeles County") |
| `authority_short_name` | Data | Short Name | No | No | - | Common abbreviation (e.g., "IRS", "FTB") |
| `authority_type` | Select | Authority Type | Yes | No | - | Income Tax, Sales Tax, Payroll Tax, Property Tax, Excise Tax, Other |
| `jurisdiction_level` | Select | Jurisdiction Level | Yes | No | - | Federal, State, County, City, District, Other |
| `jurisdiction_name` | Data | Jurisdiction Name | No | No | - | State, county, or city name if applicable |
| `website` | Data | Website | No | No | - | Authority website URL |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Tax Authority Address** (Child Table: `Tax Authority Address`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `office_name` | Data | Office Name | Yes | - | Office name or label (e.g., "Main Office", "Regional Office") |
| `street` | Data | Street | Yes | - | Street address |
| `suite_unit` | Data | Suite/Unit | No | - | Suite or unit number |
| `city` | Data | City | Yes | - | City |
| `state` | Data | State | Yes | - | State or province |
| `zip_code` | Data | ZIP Code | Yes | - | Postal/ZIP code |
| `country` | Link | Country | Yes | "United States" | Link to Country |
| `phone` | Data | Phone | No | - | Office phone number |
| `is_primary` | Check | Is Primary | No | 0 | Mark as primary office |
| `notes` | Small Text | Notes | No | - | Additional notes |

**Tax Authority Contact** (Child Table: `Tax Authority Contact`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `contact_name` | Data | Contact Name | Yes | - | Full name of contact |
| `title` | Data | Title | No | - | Job title or role |
| `department` | Data | Department | No | - | Department |
| `office_name` | Data | Office Name | No | - | Which office this contact works at |
| `email` | Data | Email | No | - | Contact email address |
| `phone` | Data | Phone | No | - | Contact phone number |
| `extension` | Data | Extension | No | - | Phone extension |
| `is_primary` | Check | Is Primary | No | 0 | Mark as primary contact |
| `notes` | Small Text | Notes | No | - | Additional notes |

#### Validation Rules
1. `authority_name` must be unique
2. `website` must be valid URL format if provided
3. **Tax Authority Address child table:**
   - Only one address can have `is_primary` = 1
4. **Tax Authority Contact child table:**
   - Contact `email` must be valid email format if provided
   - Only one contact can have `is_primary` = 1

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Create

#### Settings
```json
{
  "autoname": "format:TAX-AUTH-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "authority_name,authority_short_name,jurisdiction_name",
  "title_field": "authority_name",
  "sort_field": "authority_name",
  "sort_order": "ASC"
}
```

---

### 6. Company Tax Authority Relationship DocType

**Module:** Director
**DocType Name:** Company Tax Authority Relationship
**Naming:** Auto-generated
**Features:** Feature-003
**Note:** Links a Company to a Tax Authority; obligations are stored in separate Tax Obligation DocType

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company` | Link | Company | Yes | No | - | Link to Company |
| `tax_authority` | Link | Tax Authority | Yes | No | - | Link to Tax Authority |
| `relationship_start_date` | Date | Relationship Start Date | No | No | - | When relationship/registration began |
| `relationship_end_date` | Date | Relationship End Date | No | No | - | When relationship ended (if applicable) |
| `relationship_status` | Select | Relationship Status | Yes | No | "Active" | Active, Inactive, Closed |
| `primary_contact` | Link | Primary Contact | No | No | - | Link to Tax Authority Contact |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes about relationship |

#### Child Tables
None (Obligations are stored in separate Tax Obligation DocType)

#### Validation Rules
1. Combination of `company` + `tax_authority` should be unique
2. `relationship_end_date` must be >= `relationship_start_date` if provided
3. `relationship_status` should be "Closed" if `relationship_end_date` is set

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read only

#### Settings
```json
{
  "autoname": "format:CTAR-{company}-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "company,tax_authority",
  "title_field": "tax_authority",
  "sort_field": "company",
  "sort_order": "ASC"
}
```

---

### 7. Tax Obligation DocType

**Module:** Director
**DocType Name:** Tax Obligation
**Naming:** Auto-generated
**Features:** Feature-003
**Note:** Individual tax filing obligations linked to Company Tax Authority Relationship

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company_tax_authority_relationship` | Link | Company Tax Authority Relationship | Yes | No | - | Link to Company Tax Authority Relationship |
| `obligation_name` | Data | Obligation Name | Yes | No | - | Name/description (e.g., "Federal Income Tax", "Monthly Sales Tax") |
| `tax_id` | Data | Tax ID | No | No | - | Tax ID for this specific obligation (if different from EIN) |
| `obligation_type` | Select | Obligation Type | Yes | No | - | Income Tax Return, Sales Tax, Payroll Tax, Property Tax, Estimated Tax, Information Return, Other |
| **Section: Filing Requirements** |
| `filing_frequency` | Select | Filing Frequency | Yes | No | - | Monthly, Quarterly, Annual, Semi-Annual, As Needed, Other |
| `filing_form` | Data | Filing Form | No | No | - | Form number (e.g., "1120", "Form 100", "DE-9") |
| `due_date_pattern` | Data | Due Date Pattern | No | No | - | Pattern description (e.g., "15th of following month", "April 15") |
| `next_due_date` | Date | Next Due Date | No | No | - | Next filing due date |
| **Section: Responsible Party** |
| `responsible_party_name` | Data | Responsible Party Name | No | No | - | Person responsible for filing |
| `responsible_party_email` | Data | Responsible Party Email | No | No | - | Email of responsible party |
| **Section: Status** |
| `obligation_status` | Select | Obligation Status | Yes | No | "Active" | Active, Inactive, Closed |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Tax Filing Document** (Child Table: `Tax Filing Document`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `document_name` | Data | Document Name | Yes | - | Name/description of document |
| `document_type` | Select | Document Type | Yes | - | Tax Return, Payment Confirmation, Extension, Notice, Correspondence, Other |
| `tax_period` | Data | Tax Period | No | - | Period covered (e.g., "Q1 2025", "2024 Annual") |
| `filing_date` | Date | Filing Date | No | - | Date filed |
| `due_date` | Date | Due Date | No | - | Original due date |
| `file_attachment` | Attach | File Attachment | No | - | Uploaded file |
| `external_url` | Data | External URL | No | - | Link to external document |
| `notes` | Small Text | Notes | No | - | Additional notes |

#### Validation Rules
1. `responsible_party_email` must be valid email format if provided
2. `next_due_date` should be >= today's date if obligation is Active
3. In Tax Filing Document child table: either `file_attachment` or `external_url` should be provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Write

#### Settings
```json
{
  "autoname": "format:TAX-OBL-{company_tax_authority_relationship}-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "obligation_name,tax_id,filing_form",
  "title_field": "obligation_name",
  "sort_field": "next_due_date",
  "sort_order": "ASC"
}
```

---

### 8. Insurance Broker DocType

**Module:** Director
**DocType Name:** Insurance Broker
**Naming:** Auto-generated
**Features:** Feature-004
**Note:** Shared master data - multiple policies can use the same broker

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `broker_name` | Data | Broker Name | Yes | Yes | - | Official broker/agency name |
| `broker_type` | Select | Broker Type | No | No | - | Independent Agent, Captive Agent, Direct Writer, Wholesaler, MGA, Other |
| `license_number` | Data | License Number | No | No | - | State license number |
| `website` | Data | Website | No | No | - | Broker website URL |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Insurance Broker Address** (Child Table: `Insurance Broker Address`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `office_name` | Data | Office Name | Yes | - | Office name (e.g., "Main Office", "Regional Office") |
| `street` | Data | Street | Yes | - | Street address |
| `suite_unit` | Data | Suite/Unit | No | - | Suite or unit number |
| `city` | Data | City | Yes | - | City |
| `state` | Data | State | Yes | - | State |
| `zip_code` | Data | ZIP Code | Yes | - | ZIP code |
| `country` | Link | Country | Yes | "United States" | Link to Country |
| `phone` | Data | Phone | No | - | Office phone |
| `is_primary` | Check | Is Primary | No | 0 | Primary office |

**Insurance Broker Contact** (Child Table: `Insurance Broker Contact`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `contact_name` | Data | Contact Name | Yes | - | Full name |
| `title` | Data | Title | No | - | Job title |
| `office_name` | Data | Office Name | No | - | Which office |
| `email` | Data | Email | No | - | Email address |
| `phone` | Data | Phone | No | - | Phone number |
| `extension` | Data | Extension | No | - | Extension |
| `is_primary` | Check | Is Primary | No | 0 | Primary contact |

#### Validation Rules
1. `broker_name` must be unique
2. `website` must be valid URL format if provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Create

#### Settings
```json
{
  "autoname": "format:INS-BROKER-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "broker_name",
  "title_field": "broker_name",
  "sort_field": "broker_name",
  "sort_order": "ASC"
}
```

---

### 9. Insurance Carrier DocType

**Module:** Director
**DocType Name:** Insurance Carrier
**Naming:** Auto-generated
**Features:** Feature-004
**Note:** Shared master data - multiple policies can use the same carrier

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `carrier_name` | Data | Carrier Name | Yes | Yes | - | Official carrier/insurer name |
| `carrier_type` | Select | Carrier Type | No | No | - | Standard Carrier, Surplus Lines, Captive, Self-Insured, Other |
| `am_best_rating` | Data | AM Best Rating | No | No | - | Financial strength rating |
| `naic_number` | Data | NAIC Number | No | No | - | National Association of Insurance Commissioners number |
| `website` | Data | Website | No | No | - | Carrier website URL |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Insurance Carrier Address** (Child Table: `Insurance Carrier Address`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `office_name` | Data | Office Name | Yes | - | Office name |
| `street` | Data | Street | Yes | - | Street address |
| `suite_unit` | Data | Suite/Unit | No | - | Suite or unit |
| `city` | Data | City | Yes | - | City |
| `state` | Data | State | Yes | - | State |
| `zip_code` | Data | ZIP Code | Yes | - | ZIP code |
| `country` | Link | Country | Yes | "United States" | Link to Country |
| `phone` | Data | Phone | No | - | Office phone |
| `is_primary` | Check | Is Primary | No | 0 | Primary office |

**Insurance Carrier Contact** (Child Table: `Insurance Carrier Contact`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `contact_name` | Data | Contact Name | Yes | - | Full name |
| `title` | Data | Title | No | - | Job title |
| `office_name` | Data | Office Name | No | - | Which office |
| `email` | Data | Email | No | - | Email address |
| `phone` | Data | Phone | No | - | Phone number |
| `extension` | Data | Extension | No | - | Extension |
| `is_primary` | Check | Is Primary | No | 0 | Primary contact |

#### Validation Rules
1. `carrier_name` must be unique
2. `website` must be valid URL format if provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Create

#### Settings
```json
{
  "autoname": "format:INS-CARRIER-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "carrier_name,am_best_rating",
  "title_field": "carrier_name",
  "sort_field": "carrier_name",
  "sort_order": "ASC"
}
```

---

### 10. Premium Finance Provider DocType

**Module:** Director
**DocType Name:** Premium Finance Provider
**Naming:** Auto-generated
**Features:** Feature-004
**Note:** Shared master data - used when insurance premiums are financed

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `provider_name` | Data | Provider Name | Yes | Yes | - | Finance company name |
| `website` | Data | Website | No | No | - | Provider website URL |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Premium Finance Provider Contact** (Child Table: `Premium Finance Provider Contact`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `contact_name` | Data | Contact Name | Yes | - | Full name |
| `title` | Data | Title | No | - | Job title |
| `email` | Data | Email | No | - | Email address |
| `phone` | Data | Phone | No | - | Phone number |
| `extension` | Data | Extension | No | - | Extension |
| `is_primary` | Check | Is Primary | No | 0 | Primary contact |

#### Validation Rules
1. `provider_name` must be unique
2. `website` must be valid URL format if provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Create

#### Settings
```json
{
  "autoname": "format:FIN-PROV-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "provider_name",
  "title_field": "provider_name",
  "sort_field": "provider_name",
  "sort_order": "ASC"
}
```

---

### 11. Insurance Policy DocType

**Module:** Director
**DocType Name:** Insurance Policy
**Naming:** Auto-generated
**Features:** Feature-004
**Note:** Policies can cover multiple companies and locations

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `policy_name` | Data | Policy Name | Yes | No | - | Internal policy name/label |
| `policy_number` | Data | Policy Number | Yes | Yes | - | Official policy number |
| `insurance_broker` | Link | Insurance Broker | Yes | No | - | Link to Insurance Broker |
| `insurance_carrier` | Link | Insurance Carrier | Yes | No | - | Link to Insurance Carrier |
| `premium_finance_provider` | Link | Premium Finance Provider | No | No | - | Link to Premium Finance Provider (if financed) |
| **Section: Coverage** |
| `coverage_type` | Select | Coverage Type | Yes | No | - | General Liability, Property, Workers Comp, Umbrella, Cyber, D&O, E&O, Auto, Health, Life, Other |
| `coverage_amount` | Currency | Coverage Amount | No | No | 0.00 | Total coverage limit |
| `deductible` | Currency | Deductible | No | No | 0.00 | Policy deductible |
| **Section: Premium** |
| `annual_premium` | Currency | Annual Premium | Yes | No | 0.00 | Total annual premium |
| `payment_frequency` | Select | Payment Frequency | No | No | "Annual" | Annual, Semi-Annual, Quarterly, Monthly |
| `is_financed` | Check | Is Financed | No | No | 0 | Whether premium is financed |
| `finance_down_payment` | Currency | Down Payment | No | No | 0.00 | Down payment if financed |
| `finance_payment_amount` | Currency | Finance Payment | No | No | 0.00 | Installment amount if financed |
| **Section: Dates** |
| `effective_date` | Date | Effective Date | Yes | No | - | Policy start date |
| `expiration_date` | Date | Expiration Date | Yes | No | - | Policy end date |
| `renewal_date` | Date | Renewal Date | No | No | - | Next renewal date |
| `auto_renew` | Check | Auto-Renew | No | No | 0 | Auto-renewal enabled |
| **Section: Status** |
| `policy_status` | Select | Policy Status | Yes | No | "Active" | Active, Expired, Cancelled, Pending Renewal, In Force |
| `cancellation_date` | Date | Cancellation Date | No | No | - | Date policy was cancelled |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Policy Covered Entity** (Child Table: `Policy Covered Entity`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `company` | Link | Company | Yes | - | Link to Company covered by this policy |
| `coverage_notes` | Small Text | Coverage Notes | No | - | Specific coverage notes for this entity |

**Policy Covered Location** (Child Table: `Policy Covered Location`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `location_name` | Data | Location Name | Yes | - | Name/label for location (e.g., "Downtown Hotel", "Warehouse 1") |
| `company` | Link | Company | No | - | Which company owns/operates this location |
| `street` | Data | Street | Yes | - | Street address |
| `city` | Data | City | Yes | - | City |
| `state` | Data | State | Yes | - | State |
| `zip_code` | Data | ZIP Code | Yes | - | ZIP code |
| `property_value` | Currency | Property Value | No | 0.00 | Insured property value at this location |
| `coverage_notes` | Small Text | Coverage Notes | No | - | Specific coverage for this location |

**Policy Document** (Child Table: `Policy Document`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `document_name` | Data | Document Name | Yes | - | Name/description |
| `document_type` | Select | Document Type | Yes | - | Policy, Certificate of Insurance, Endorsement, Binder, Declaration Page, Renewal Notice, Cancellation Notice, Other |
| `document_date` | Date | Document Date | No | - | Date of document |
| `file_attachment` | Attach | File Attachment | No | - | Uploaded file |
| `external_url` | Data | External URL | No | - | Link to external document |
| `notes` | Small Text | Notes | No | - | Additional notes |

#### Validation Rules
1. `policy_number` must be unique
2. `expiration_date` must be >= `effective_date`
3. `renewal_date` should be <= `expiration_date` if provided
4. `policy_status` should be "Expired" if `expiration_date` is in the past
5. `coverage_amount`, `deductible`, `annual_premium` must be >= 0
6. If `is_financed` = 1, `premium_finance_provider` is required
7. At least one covered entity or covered location should be specified

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Write

#### Settings
```json
{
  "autoname": "field:policy_number",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "policy_name,policy_number,coverage_type",
  "title_field": "policy_name",
  "sort_field": "expiration_date",
  "sort_order": "DESC"
}
```

---

### 12. Loan Relationship DocType

**Module:** Director
**DocType Name:** Loan Relationship
**Naming:** Auto-generated
**Features:** Feature-005
**Note:** Loans are tied to banking relationships. The lender is the Banking Institution linked via Company Bank Relationship.

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company_bank_relationship` | Link | Company Bank Relationship | Yes | No | - | Link to Company Bank Relationship (identifies both company and banking institution) |
| `loan_number` | Password | Loan Number | No | No | - | Encrypted loan account number |
| `loan_type` | Select | Loan Type | Yes | No | - | Term Loan, Line of Credit, Mortgage, SBA 7(a), SBA 504, Equipment Financing, Real Estate, Working Capital, Equipment Loan, Other |
| **Section: Loan Terms** |
| `original_principal` | Currency | Original Principal | Yes | No | 0.00 | Original loan principal amount |
| `interest_rate` | Float | Interest Rate (%) | Yes | No | 0.00 | Annual interest rate percentage |
| `loan_term_months` | Int | Loan Term (months) | Yes | No | 0 | Total loan term in months |
| `payment_frequency` | Select | Payment Frequency | Yes | No | "Monthly" | Monthly, Quarterly, Semi-Annual, Annual, Other |
| `payment_amount` | Currency | Payment Amount | No | No | 0.00 | Regular payment amount |
| **Section: Dates & Status** |
| `origination_date` | Date | Origination Date | Yes | No | - | Date loan was originated |
| `maturity_date` | Date | Maturity Date | Yes | No | - | Date loan matures/ends |
| `next_payment_date` | Date | Next Payment Date | No | No | - | Date of next payment due (auto-calculated from amortization schedule) |
| `current_balance` | Currency | Current Balance | No | No | 0.00 | Current outstanding balance (auto-calculated from amortization schedule) |
| `accrued_interest` | Currency | Accrued Interest | No | No | 0.00 | Accrued interest to date (auto-calculated) |
| `loan_status` | Select | Loan Status | Yes | No | "Active" | Active, Paid Off, In Default, Refinanced, Closed |
| **Section: Security** |
| `collateral_description` | Small Text | Collateral Description | No | No | - | Description of loan collateral |
| `guarantors` | Small Text | Guarantors | No | No | - | Names of personal guarantors |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes about the loan |

#### Child Tables

**Loan Amortization Schedule** (Child Table: `Loan Amortization Schedule`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `payment_number` | Int | Payment # | Yes | - | Sequential payment number (1, 2, 3...) |
| `scheduled_payment_date` | Date | Scheduled Date | Yes | - | Scheduled payment date |
| `scheduled_payment_amount` | Currency | Scheduled Payment | Yes | 0.00 | Scheduled total payment amount |
| `principal_portion` | Currency | Principal Portion | Yes | 0.00 | Principal portion of payment |
| `interest_portion` | Currency | Interest Portion | Yes | 0.00 | Interest portion of payment |
| `remaining_balance` | Currency | Remaining Balance | Yes | 0.00 | Remaining balance after this payment |
| **Section: Actual Payment Tracking** |
| `is_paid` | Check | Is Paid | No | 0 | Whether payment has been made |
| `actual_payment_date` | Date | Actual Payment Date | No | - | Date payment was actually made |
| `actual_payment_amount` | Currency | Actual Payment Amount | No | 0.00 | Actual amount paid |
| `variance` | Currency | Variance | No | 0.00 | Difference between scheduled and actual payment (read-only, auto-calculated) |

#### Validation Rules
1. `company_bank_relationship` must be valid and active
2. `maturity_date` must be >= `origination_date`
3. `interest_rate` must be between 0 and 100
4. `loan_term_months` must be > 0
5. `current_balance` must be >= 0 and <= `original_principal`
6. `loan_number` must be encrypted (Password field type)
7. `payment_amount` and `original_principal` must be > 0
8. `next_payment_date` should be >= today's date if loan is Active
9. **Loan Amortization Schedule child table:**
   - `payment_number` must be sequential (1, 2, 3...)
   - `scheduled_payment_date` must be chronological
   - `remaining_balance` for last payment must be 0.00
   - Sum of all `principal_portion` must equal `original_principal`
   - If `is_paid` = 1, then `actual_payment_date` is required
   - `variance` = `actual_payment_amount` - `scheduled_payment_amount` (auto-calculated)

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read only

#### Settings
```json
{
  "autoname": "format:LOAN-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "loan_number,loan_type",
  "title_field": "loan_type",
  "sort_field": "origination_date",
  "sort_order": "DESC"
}
```

#### Server-Side Automation
The Loan Amortization Schedule enables automated loan management:
1. **Auto-calculate current_balance:** Sum of unpaid principal portions
2. **Auto-calculate next_payment_date:** Earliest unpaid scheduled_payment_date where is_paid = 0
3. **Auto-calculate accrued_interest:** Based on current_balance, interest_rate, and days since last payment
4. **Alert upcoming payments:** Notify when next_payment_date < 7 days
5. **Track payment variance:** Auto-calculate variance field when actual payment recorded
6. **Update loan_status:** Auto-update to "Paid Off" when all payments marked is_paid = 1 and remaining_balance = 0

#### Feature Codes and Functionality

This DocType supports granular feature-based enablement. Features are enabled per company via the Company Feature child table.

**Basic Features (Free/Included):**

**`loan_basic_entry`** - Core Loan Data Entry
- All main Loan Relationship fields
- Manual entry of `current_balance`, `next_payment_date`
- Basic loan information storage
- Manual status updates
- View loan list and details

**`loan_task_automation`** - Payment Reminder Tasks
- Auto-create recurring tasks based on `payment_frequency`
- Task creation triggered by `next_payment_date`
- Basic task assignment and notifications
- Payment reminder workflow
- Implementation: Uses Task Type with recurrence pattern

**Premium Features (Paid Add-ons):**

**`loan_amortization_schedules`** ($25/mo) - Full Amortization Tracking
- **Enables:** Loan Amortization Schedule child table
- Full amortization schedule with all payment details
- Track scheduled vs actual payments
- Record payment dates and amounts
- View complete payment history
- Implementation: Renders child table in UI, stores amortization data

**`loan_auto_calculations`** ($15/mo) - Automated Balance Calculations
- **Requires:** `loan_amortization_schedules`
- Auto-calculate `current_balance` from amortization schedule
- Auto-calculate `next_payment_date` from unpaid payments
- Auto-calculate `accrued_interest` based on actual days
- Auto-update fields on payment recording
- Implementation: Server-side calculations in `Loan Relationship.py`

**`loan_payment_variance`** ($20/mo) - Payment Variance Analysis
- **Requires:** `loan_amortization_schedules`
- Auto-calculate variance between scheduled and actual payments
- Variance reporting and alerts
- Track payment timing and amount differences
- Variance trend analysis
- Implementation: Calculates `variance` field in amortization schedule

**`loan_advanced_reporting`** ($30/mo) - Advanced Loan Reports
- Amortization schedule reports (PDF/Excel)
- Interest expense projections
- Principal paydown analysis
- Payment variance analysis reports
- Custom loan reports
- Implementation: Report generator with loan data

**Enterprise Features (High-tier):**

**`loan_gl_integration`** ($50/mo) - General Ledger Integration
- **Requires:** `gl_integration_full`, `loan_amortization_schedules`
- Auto-draft journal entries for loan transactions:
  - Loan disbursement (DR Cash, CR Loan Payable)
  - Monthly interest accrual (DR Interest Expense, CR Interest Payable)
  - Loan payments (DR Loan Payable + Interest Payable, CR Cash)
  - Principal vs interest allocation per payment
- GL code mapping based on loan type and company settings
- Multi-entity GL posting for consolidated companies
- GL account reconciliation
- Implementation: Creates Journal Entry DocTypes linked to loan transactions

**`loan_bank_reconciliation`** ($30/mo) - Bank Transaction Reconciliation
- **Requires:** `banking_reconciliation`, `loan_amortization_schedules`
- Auto-match bank transactions to loan payments
- Reconciliation workflow
- Identify missing or duplicate payments
- Implementation: Links bank transactions to amortization schedule payments

**Implementation Notes:**
- Server-side: `if has_feature(company, "loan_amortization_schedules"):`
- Frontend: Conditionally render child table and auto-calculated fields
- API: Return filtered data based on enabled features
- All basic features work independently
- Premium features have clear dependencies

---

### 13. Key Employee Relationship DocType

**Module:** Director
**DocType Name:** Key Employee Relationship
**Naming:** Auto-generated
**Features:** Feature-006

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company` | Link | Company | Yes | No | - | Link to Company |
| `employee_name` | Data | Employee Name | Yes | No | - | Full name of employee |
| `role_title` | Data | Role/Title | Yes | No | - | Job title or role |
| `department` | Data | Department | No | No | - | Department name |
| **Section: Contact Information** |
| `email` | Data | Email | Yes | No | - | Employee email address |
| `phone_work` | Data | Work Phone | No | No | - | Work phone number |
| `phone_mobile` | Data | Mobile Phone | No | No | - | Mobile phone number |
| **Section: Employment** |
| `start_date` | Date | Start Date | Yes | No | - | Employment start date |
| `end_date` | Date | End Date | No | No | - | Employment end date (if applicable) |
| `status` | Select | Status | Yes | No | "Active" | Active, Inactive, On Leave |
| `responsibilities` | Long Text | Responsibilities | No | No | - | Description of key responsibilities |
| **Section: Emergency Contact** |
| `emergency_contact_name` | Data | Emergency Contact Name | No | No | - | Name of emergency contact |
| `emergency_contact_phone` | Data | Emergency Contact Phone | No | No | - | Emergency contact phone |
| **Section: Additional** |
| `notes` | Small Text | Notes | No | No | - | Additional notes |

#### Child Tables
None

#### Validation Rules
1. `email` must be valid email format
2. `end_date` must be >= `start_date` if provided
3. `status` should be "Inactive" if `end_date` is set and in the past
4. `phone_work` and `phone_mobile` should be valid phone format if provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read only

#### Settings
```json
{
  "autoname": "format:EMP-{company}-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "employee_name,role_title,department",
  "title_field": "employee_name",
  "sort_field": "employee_name",
  "sort_order": "ASC"
}
```

---

### 14. Task Type DocType

**Module:** Director
**DocType Name:** Task Type
**Naming:** `field:task_name`
**Features:** Feature-007

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `task_name` | Data | Task Name | Yes | Yes | - | Unique task identifier |
| `description` | Long Text | Description | No | No | - | Detailed task description |
| `category` | Select | Category | Yes | No | - | Accounting, Finance, Operations, Compliance, HR, Other |
| `priority` | Select | Priority | Yes | No | "Medium" | Urgent, High, Medium, Low |
| `status` | Select | Status | Yes | No | "Active" | Active, Inactive |
| **Section: Recurrence** |
| `recurrence_pattern` | Select | Recurrence Pattern | Yes | No | - | Daily, Weekly, Bi-weekly, Monthly, Quarterly, Annual, On-Demand |
| `day_of_week` | Select | Day of Week | No | No | - | Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday (for Weekly/Bi-weekly) |
| `day_of_month` | Int | Day of Month | No | No | - | 1-31 (for Monthly) |
| `month` | Select | Month | No | No | - | January-December (for Annual) |
| `quarter` | Select | Quarter | No | No | - | Q1, Q2, Q3, Q4 (for Quarterly) |
| **Section: Assignment** |
| `assigned_role` | Link | Assigned Role | No | No | - | Link to Role |
| `estimated_time` | Float | Estimated Time (hours) | No | No | 0.0 | Estimated completion time |
| `instructions` | Long Text | Instructions | No | No | - | Step-by-step instructions (Markdown) |
| **Section: Metadata** |
| `created_by` | Link | Created By | No | No | - | Link to User (auto-filled) |
| `modified_by` | Link | Modified By | No | No | - | Link to User (auto-filled) |

#### Child Tables

**Task Dependencies** (Child Table: `Task Type Dependency`)
| Field Name | Field Type | Label | Required | Description |
|------------|-----------|-------|----------|-------------|
| `prerequisite_task` | Link | Prerequisite Task | Yes | Link to Task Type that must complete first |
| `dependency_type` | Select | Dependency Type | Yes | Finish-to-Start, Start-to-Start, Finish-to-Finish |

#### Validation Rules
1. `day_of_week` required if `recurrence_pattern` is Weekly or Bi-weekly
2. `day_of_month` required if `recurrence_pattern` is Monthly (1-31)
3. `month` required if `recurrence_pattern` is Annual
4. `quarter` required if `recurrence_pattern` is Quarterly
5. `estimated_time` must be > 0 if provided
6. Prevent circular dependencies in Task Dependencies child table
7. `task_name` must be unique

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Create

#### Settings
```json
{
  "autoname": "field:task_name",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "task_name,category",
  "title_field": "task_name",
  "sort_field": "task_name",
  "sort_order": "ASC"
}
```

---

### 15. Review Period DocType

**Module:** Director
**DocType Name:** Review Period
**Naming:** Auto-generated
**Features:** Feature-008

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `company` | Link | Company | Yes | No | - | Link to Company |
| `period_name` | Data | Period Name | Yes | No | - | E.g., "November 2025" |
| **Section: Period Details** |
| `period_start_date` | Date | Period Start Date | Yes | No | - | Start of review period |
| `period_end_date` | Date | Period End Date | Yes | No | - | End of review period |
| `target_close_date` | Date | Target Close Date | Yes | No | - | Target date to close period |
| `actual_close_date` | Date | Actual Close Date | No | No | - | Actual date period was closed |
| **Section: Status & Assignment** |
| `status` | Select | Status | Yes | No | "Open" | Open, In Progress, Controller Review, Executive Review, Closed |
| `assigned_controller` | Link | Assigned Controller | No | No | - | Link to User (Controller role) |
| `assigned_executive` | Link | Assigned Executive | No | No | - | Link to User (Executive role) |
| **Section: Issues** |
| `outstanding_issues` | Long Text | Outstanding Issues | No | No | - | List of unresolved issues |
| `blockers` | Long Text | Blockers | No | No | - | Items blocking completion |
| **Section: Additional** |
| `notes` | Long Text | Notes | No | No | - | Additional notes |
| **Section: Metadata** |
| `created_by` | Link | Created By | No | No | - | Link to User (auto-filled) |
| `modified_by` | Link | Modified By | No | No | - | Link to User (auto-filled) |

#### Child Tables

**Tasks** (Child Table: `Review Period Task`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `task_type` | Link | Task Type | Yes | - | Link to Task Type |
| `task_name` | Data | Task Name | Yes | - | Name of task |
| `assigned_to` | Link | Assigned To | No | - | Link to User |
| `due_date` | Date | Due Date | Yes | - | Task due date |
| `completed_date` | Date | Completed Date | No | - | Date task was completed |
| `status` | Select | Status | Yes | "Not Started" | Not Started, In Progress, Completed |
| `notes` | Small Text | Notes | No | - | Task-specific notes |

#### Validation Rules
1. `period_end_date` must be >= `period_start_date`
2. `target_close_date` should be >= `period_end_date`
3. `actual_close_date` should be >= `target_close_date` if provided
4. `status` must be "Closed" if `actual_close_date` is set
5. Cannot close period unless all tasks are "Completed"
6. `completed_date` must be <= today's date if provided
7. Task `status` must be "Completed" if `completed_date` is set

#### Server Scripts
- **Calculate completion percentage:** Count completed tasks / total tasks
- **Workflow transitions:** Enforce status progression (Open → In Progress → Controller Review → Executive Review → Closed)
- **Notifications:** Send emails when status changes or tasks are overdue

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Write (assigned tasks only)

#### Settings
```json
{
  "autoname": "format:RP-{company}-{YYYY}-{MM}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "period_name,company",
  "title_field": "period_name",
  "sort_field": "period_start_date",
  "sort_order": "DESC"
}
```

---

### 16. Project DocType

**Module:** Director
**DocType Name:** Project
**Naming:** Auto-generated
**Features:** Feature-015 (Referenced in roadmap)

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `project_name` | Data | Project Name | Yes | No | - | Name of project |
| `company` | Link | Company | Yes | No | - | Link to Company |
| `description` | Long Text | Description | No | No | - | Project description |
| **Section: Dates** |
| `start_date` | Date | Start Date | No | No | - | Project start date |
| `end_date` | Date | End Date | No | No | - | Project end date |
| `expected_completion` | Date | Expected Completion | No | No | - | Expected completion date |
| **Section: Assignment** |
| `project_manager` | Link | Project Manager | No | No | - | Link to User |
| `team_members` | Small Text | Team Members | No | No | - | Comma-separated team members |
| **Section: Status** |
| `status` | Select | Status | Yes | No | "Planned" | Planned, In Progress, On Hold, Completed, Cancelled |
| `progress` | Percent | Progress (%) | No | No | 0 | Project completion percentage |
| **Section: Additional** |
| `notes` | Long Text | Notes | No | No | - | Additional notes |

#### Child Tables

**Milestones** (Child Table: `Project Milestone`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `milestone_name` | Data | Milestone Name | Yes | - | Name of milestone |
| `due_date` | Date | Due Date | Yes | - | Milestone due date |
| `completed_date` | Date | Completed Date | No | - | Date milestone was completed |
| `status` | Select | Status | Yes | "Pending" | Pending, Completed |
| `description` | Small Text | Description | No | - | Milestone description |

**Project Tasks** (Child Table: `Project Task`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `task_name` | Data | Task Name | Yes | - | Name of task |
| `assigned_to` | Link | Assigned To | No | - | Link to User |
| `due_date` | Date | Due Date | No | - | Task due date |
| `completed_date` | Date | Completed Date | No | - | Date task was completed |
| `status` | Select | Status | Yes | "Not Started" | Not Started, In Progress, Completed |
| `notes` | Small Text | Notes | No | - | Task notes |

#### Validation Rules
1. `end_date` must be >= `start_date` if both provided
2. `expected_completion` should be >= `start_date` if provided
3. `progress` must be between 0 and 100
4. `status` should be "Completed" if `progress` = 100
5. Milestone `completed_date` must be <= today's date if provided
6. Task `completed_date` must be <= today's date if provided

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Full access
- **Accountant:** Read, Write (assigned tasks only)

#### Settings
```json
{
  "autoname": "format:PRJ-{company}-{####}",
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "project_name,company",
  "title_field": "project_name",
  "sort_field": "start_date",
  "sort_order": "DESC"
}
```

---

### 17. Platform Feature DocType

**Module:** Director
**DocType Name:** Platform Feature
**Naming:** `field:feature_code`
**Features:** Design-004 (BLK-195)
**Note:** Master registry of all available platform features for subscription management

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `feature_code` | Data | Feature Code | Yes | Yes | - | Unique identifier (e.g., "loan_amortization_schedules") |
| `feature_name` | Data | Feature Name | Yes | No | - | Display name (e.g., "Loan Amortization Schedules") |
| `module` | Select | Module | Yes | No | - | Company Management, Inventory, Procurement, Recipes, POS, Accounting, Analytics, Other |
| `category` | Select | Category | Yes | No | - | Basic (free), Premium (paid add-on), Enterprise (high-tier) |
| **Section: Description** |
| `short_description` | Small Text | Short Description | Yes | No | - | Brief feature description (1-2 sentences) |
| `detailed_description` | Long Text | Detailed Description | No | No | - | Full feature documentation |
| `benefits` | Long Text | Benefits | No | No | - | Key benefits and value proposition |
| **Section: Pricing** |
| `base_price` | Currency | Base Price | No | No | 0.00 | Monthly price per feature (if sold individually) |
| `is_billable` | Check | Is Billable | No | No | 1 | Whether this feature has a cost |
| **Section: Dependencies** |
| `requires_feature` | Link | Requires Feature | No | No | - | Link to Platform Feature (prerequisite) |
| `enables_features` | Small Text | Enables Features | No | No | - | Comma-separated list of features this unlocks |
| **Section: Status** |
| `is_active` | Check | Is Active | No | No | 1 | Whether feature is currently available |
| `release_date` | Date | Release Date | No | No | - | When feature was/will be released |
| `deprecation_date` | Date | Deprecation Date | No | No | - | When feature will be deprecated (if applicable) |
| **Section: Additional** |
| `documentation_url` | Data | Documentation URL | No | No | - | Link to feature documentation |
| `notes` | Small Text | Notes | No | No | - | Internal notes about this feature |

#### Child Tables
None

#### Validation Rules
1. `feature_code` must be lowercase with underscores (e.g., "loan_amortization_schedules")
2. `feature_code` must be unique across all features
3. `base_price` must be >= 0
4. `deprecation_date` must be > `release_date` if both provided
5. If `category` = "Basic", then `is_billable` should be 0
6. `requires_feature` cannot reference self (no circular dependencies)

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Read only
- **All Users:** Read (for feature discovery)

#### Settings
```json
{
  "autoname": "field:feature_code",
  "quick_entry": 0,
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "feature_name,feature_code,module",
  "title_field": "feature_name",
  "sort_field": "module",
  "sort_order": "ASC"
}
```

---

### 18. Subscription Plan DocType

**Module:** Director
**DocType Name:** Subscription Plan
**Naming:** `field:plan_code`
**Features:** Design-004 (BLK-195)
**Note:** Pre-configured bundles of features for subscription offerings (optional - supports both plans and à la carte)

#### Fields

| Field Name | Field Type | Label | Required | Unique | Default | Description |
|------------|-----------|-------|----------|--------|---------|-------------|
| `plan_code` | Data | Plan Code | Yes | Yes | - | Unique identifier (e.g., "starter", "professional", "enterprise") |
| `plan_name` | Data | Plan Name | Yes | No | - | Display name (e.g., "Professional Plan") |
| `marketing_name` | Data | Marketing Name | No | No | - | Public-facing name (e.g., "Professional - For Growing Businesses") |
| **Section: Description** |
| `short_description` | Small Text | Short Description | Yes | No | - | Brief plan description |
| `detailed_description` | Long Text | Detailed Description | No | No | - | Full plan details and features |
| `target_customer` | Small Text | Target Customer | No | No | - | Who this plan is best for |
| **Section: Pricing** |
| `monthly_price` | Currency | Monthly Price | Yes | No | 0.00 | Total monthly price |
| `annual_price` | Currency | Annual Price | No | No | 0.00 | Total annual price (if different) |
| `setup_fee` | Currency | Setup Fee | No | No | 0.00 | One-time setup fee |
| `billing_frequency` | Select | Billing Frequency | Yes | No | "Monthly" | Monthly, Quarterly, Annual |
| **Section: Limits** |
| `max_companies` | Int | Max Companies | No | No | 0 | Maximum companies (0 = unlimited) |
| `max_users` | Int | Max Users | No | No | 0 | Maximum users (0 = unlimited) |
| `max_locations` | Int | Max Locations | No | No | 0 | Maximum locations per company (0 = unlimited) |
| **Section: Status** |
| `is_active` | Check | Is Active | No | No | 1 | Whether plan is currently offered |
| `is_public` | Check | Is Public | No | No | 1 | Whether plan is publicly visible |
| `launch_date` | Date | Launch Date | No | No | - | When plan was/will be launched |
| **Section: Additional** |
| `terms_and_conditions` | Long Text | Terms & Conditions | No | No | - | Plan-specific T&Cs |
| `notes` | Small Text | Notes | No | No | - | Internal notes |

#### Child Tables

**Plan Feature** (Child Table: `Plan Feature`)
| Field Name | Field Type | Label | Required | Default | Description |
|------------|-----------|-------|----------|---------|-------------|
| `feature_code` | Link | Feature Code | Yes | - | Link to Platform Feature |
| `is_included` | Check | Is Included | No | 1 | Whether feature is included in this plan |
| `quantity_limit` | Int | Quantity Limit | No | 0 | Limit for metered features (0 = unlimited) |
| `notes` | Small Text | Notes | No | - | Notes about feature inclusion |

#### Validation Rules
1. `plan_code` must be lowercase with underscores or hyphens
2. `plan_code` must be unique across all plans
3. `monthly_price` and `annual_price` must be >= 0
4. `annual_price` should be <= (`monthly_price` * 12) if both provided
5. `max_companies`, `max_users`, `max_locations` must be >= 0
6. **Plan Feature child table:**
   - Each `feature_code` can only appear once per plan
   - All features in plan must be active Platform Features

#### Permissions
- **System Manager:** Full access
- **Accounting Manager:** Read, Write, Create
- **All Users:** Read (for public plans only)

#### Settings
```json
{
  "autoname": "field:plan_code",
  "quick_entry": 0,
  "track_changes": 1,
  "track_seen": 1,
  "search_fields": "plan_name,plan_code",
  "title_field": "plan_name",
  "sort_field": "monthly_price",
  "sort_order": "ASC"
}
```

---

## Feature Registry

### Company Management Module Features

This section documents all available features for the Company Management module with their feature codes, pricing, and dependencies.

#### Basic Features (Free/Included)

| Feature Code | Feature Name | Description | Category | Price |
|--------------|--------------|-------------|----------|-------|
| `company_basic_entry` | Company Management | Create and manage company master data | Basic | Free |
| `banking_basic_entry` | Basic Banking Tracking | Track bank accounts and relationships | Basic | Free |
| `tax_basic_entry` | Basic Tax Tracking | Track tax authorities and obligations | Basic | Free |
| `insurance_basic_entry` | Basic Insurance Tracking | Track insurance policies and renewals | Basic | Free |
| `loan_basic_entry` | Basic Loan Tracking | Track loans with manual balance entry | Basic | Free |
| `task_basic_automation` | Task Automation | Recurrence-based task creation | Basic | Free |
| `employee_basic_tracking` | Employee Relationships | Track key employee relationships | Basic | Free |
| `project_basic_tracking` | Project Management | Basic project and milestone tracking | Basic | Free |

#### Premium Features (Paid Add-ons)

| Feature Code | Feature Name | Description | Requires | Category | Price/mo |
|--------------|--------------|-------------|----------|----------|----------|
| `loan_amortization_schedules` | Loan Amortization | Full amortization schedule tracking | - | Premium | $25 |
| `loan_auto_calculations` | Loan Auto-Calculations | Auto-calculate balances and interest | `loan_amortization_schedules` | Premium | $15 |
| `loan_payment_variance` | Loan Payment Variance | Track and analyze payment variances | `loan_amortization_schedules` | Premium | $20 |
| `loan_advanced_reporting` | Loan Advanced Reports | Detailed loan reports and analytics | - | Premium | $30 |
| `loan_bank_reconciliation` | Loan-Bank Reconciliation | Auto-match payments to bank transactions | `banking_reconciliation`, `loan_amortization_schedules` | Premium | $30 |
| `banking_reconciliation` | Bank Reconciliation | Reconcile bank accounts with transactions | - | Premium | $30 |
| `tax_auto_filings` | Tax Filing Automation | Automated tax filing reminders and tracking | - | Premium | $15 |
| `insurance_certificate_tracking` | Insurance Certificates | Certificate of insurance management | - | Premium | $20 |
| `advanced_reporting` | Advanced Reporting | Custom reports and analytics across modules | - | Premium | $40 |

#### Enterprise Features (High-tier)

| Feature Code | Feature Name | Description | Requires | Category | Price/mo |
|--------------|--------------|-------------|----------|----------|----------|
| `loan_gl_integration` | Loan GL Integration | Auto-draft journal entries for loans | `gl_integration_full`, `loan_amortization_schedules` | Enterprise | $50 |
| `gl_integration_full` | Full GL Integration | Complete general ledger integration | - | Enterprise | $100 |
| `multi_entity_consolidation` | Multi-Entity Consolidation | Consolidated financial reporting | `gl_integration_full` | Enterprise | $100 |

### Feature Dependencies Graph

```
gl_integration_full (Enterprise - $100)
├── loan_gl_integration (Enterprise - $50)
│   └── loan_amortization_schedules (Premium - $25)
│       ├── loan_auto_calculations (Premium - $15)
│       ├── loan_payment_variance (Premium - $20)
│       └── loan_bank_reconciliation (Premium - $30)
│           └── banking_reconciliation (Premium - $30)
└── multi_entity_consolidation (Enterprise - $100)

Advanced Features (independent):
- tax_auto_filings (Premium - $15)
- insurance_certificate_tracking (Premium - $20)
- advanced_reporting (Premium - $40)
- loan_advanced_reporting (Premium - $30)
```

### Example Subscription Plans

#### Starter Plan - $99/month
**Target:** Single entity, basic tracking needs
**Included Features:**
- All Basic features (company, banking, tax, insurance, loan, task, employee, project)
- Total value: Core functionality

#### Professional Plan - $299/month
**Target:** Single entity with detailed tracking and automation
**Included Features:**
- All Starter features
- `loan_amortization_schedules` ($25)
- `loan_auto_calculations` ($15)
- `loan_payment_variance` ($20)
- `banking_reconciliation` ($30)
- `tax_auto_filings` ($15)
- `advanced_reporting` ($40)
- **Total add-on value:** $145/mo
- **Plan savings:** $46/mo (24% discount)

#### Enterprise Plan - $599/month
**Target:** Multi-entity operations with full accounting integration
**Included Features:**
- All Professional features
- `loan_gl_integration` ($50)
- `gl_integration_full` ($100)
- `multi_entity_consolidation` ($100)
- `insurance_certificate_tracking` ($20)
- `loan_advanced_reporting` ($30)
- `loan_bank_reconciliation` ($30)
- **Total add-on value:** $475/mo (on top of Professional)
- **Plan savings:** $320/mo (40% discount)

#### Custom Plan - Variable Pricing
**Target:** Clients with specific feature needs
**Approach:** À la carte feature selection
**Example Configuration:**
- All Basic features: Free
- `loan_amortization_schedules`: $25/mo
- `advanced_reporting`: $40/mo
- **Total:** $65/mo

### Future Module Features

The following modules will follow the same feature-based pattern:

**Inventory Management Module:**
- `inventory_basic_entry` (Basic - Free)
- `inventory_audit_tracking` (Premium - TBD)
- `inventory_variance_analysis` (Premium - TBD)
- `inventory_gl_integration` (Enterprise - TBD)

**Procurement Module:**
- `procurement_basic_entry` (Basic - Free)
- `invoice_ocr_processing` (Premium - TBD)
- `purchase_approval_workflows` (Premium - TBD)
- `vendor_performance_analytics` (Premium - TBD)

**Recipe Costing Module:**
- `recipe_basic_entry` (Basic - Free)
- `recipe_costing_automation` (Premium - TBD)
- `recipe_variance_analysis` (Premium - TBD)
- `recipe_batch_management` (Premium - TBD)

**POS Integration Module:**
- `pos_sales_import` (Basic - Free)
- `pos_auto_depletion` (Premium - TBD)
- `pos_variance_tracking` (Premium - TBD)
- `pos_gl_integration` (Enterprise - TBD)

*Detailed feature definitions will be added as modules are designed*

---

## Entity Relationships

### Entity Relationship Diagram

```
┌─────────────────┐
│    Company      │ (Master)
│  (Director)     │
└────────┬────────┘
         │
         │ 1:N
         ├────────────────┐
         │                │
         ▼                ▼
┌─────────────────┐  ┌─────────────────┐
│ Bank            │  │ Tax Entity      │
│ Relationship    │  │ Relationship    │
└─────────────────┘  └─────────────────┘
         │
         │ 1:N
         ├────────────────┬────────────────┬────────────────┐
         │                │                │                │
         ▼                ▼                ▼                ▼
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Insurance       │  │ Loan            │  │ Key Employee    │  │ Review Period   │
│ Relationship    │  │ Relationship    │  │ Relationship    │  │                 │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └────────┬────────┘
                                                                         │
                                                                         │ 1:N
                                                                         ▼
                                                                ┌─────────────────┐
                                                                │ Review Period   │
                                                                │ Task (Child)    │
                                                                └────────┬────────┘
                                                                         │
                                                                         │ N:1
                                                                         ▼
┌─────────────────┐                                            ┌─────────────────┐
│ Project         │                                            │ Task Type       │
└────────┬────────┘                                            │ (Master)        │
         │                                                     └────────┬────────┘
         │ 1:N                                                          │
         ├────────────────┬────────────────┐                           │ 1:N
         │                │                │                            │
         ▼                ▼                ▼                            ▼
┌─────────────────┐  ┌─────────────────┐  │                   ┌─────────────────┐
│ Project         │  │ Project Task    │  │                   │ Task Type       │
│ Milestone       │  │ (Child)         │  │                   │ Dependency      │
│ (Child)         │  └─────────────────┘  │                   │ (Child)         │
└─────────────────┘                       │                   └─────────────────┘
                                          │
                                          ▼
                                    Link to Company
```

### Relationship Summary

| Parent DocType | Child DocType | Relationship Type | Link Field |
|---------------|---------------|-------------------|------------|
| Company | Bank Relationship | One-to-Many | `company` |
| Company | Tax Entity Relationship | One-to-Many | `company` |
| Company | Insurance Relationship | One-to-Many | `company` |
| Company | Loan Relationship | One-to-Many | `company` |
| Company | Key Employee Relationship | One-to-Many | `company` |
| Company | Review Period | One-to-Many | `company` |
| Company | Project | One-to-Many | `company` |
| Company | Company | One-to-Many (Self) | `parent_company` |
| Review Period | Review Period Task | One-to-Many (Child Table) | Parent doc |
| Task Type | Task Type Dependency | One-to-Many (Child Table) | Parent doc |
| Task Type | Review Period Task | One-to-Many | `task_type` |
| Project | Project Milestone | One-to-Many (Child Table) | Parent doc |
| Project | Project Task | One-to-Many (Child Table) | Parent doc |

---

## Validation Rules

### Cross-Document Validation

1. **Company Hierarchy:**
   - Prevent circular references in `parent_company`
   - Maximum depth of 3 levels in company hierarchy

2. **Date Consistency:**
   - End dates must be >= start dates across all DocTypes
   - `actual_close_date` (Review Period) should trigger status = "Closed"
   - Insurance `expiration_date` in past should trigger status = "Expired"

3. **Task Dependencies:**
   - Prevent circular dependencies in Task Type Dependency table
   - Enforce dependency completion before dependent task can be marked complete

4. **Review Period Closure:**
   - All tasks must be "Completed" before period can be set to "Closed"
   - Controller must review before Executive
   - Executive must review before Closed

### Field-Level Validation

1. **Email Fields:**
   - All email fields must match pattern: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`

2. **Phone Fields:**
   - Optional format: `(XXX) XXX-XXXX` or `XXX-XXX-XXXX` or `XXXXXXXXXX`

3. **Numeric Fields:**
   - Currency fields: Must be >= 0 (except balance fields which can be negative)
   - Percentage fields: Must be between 0 and 100
   - Interest rate: Must be between 0 and 100

4. **Encrypted Fields:**
   - `ein` (Company): Format XX-XXXXXXX (9 digits)
   - `account_number` (Bank, Loan): Minimum 4 characters

5. **URL Fields:**
   - Must match pattern: `^https?://[^\s]+$`

---

## Security Considerations

### Encryption

**Fields Requiring Encryption:**
- `Company.ein` - Federal Tax ID
- `Bank Relationship.account_number` - Bank account number
- `Loan Relationship.account_number` - Loan account number

**Implementation:**
- Use Frappe's built-in `Password` field type (AES-256 encryption)
- Encryption keys managed by Frappe Framework
- Encrypted at rest and in transit

### Permissions

**Role-Based Access Control:**

| Role | Company | Relationships | Tasks | Review Periods | Projects |
|------|---------|---------------|-------|----------------|----------|
| System Manager | Full | Full | Full | Full | Full |
| Accounting Manager | Full | Full | Full | Full | Full |
| Accountant | Read | Read | Read/Write (assigned) | Read/Write (assigned) | Read/Write (assigned) |
| Controller | Read | Read | Read | Read/Write | Read |
| Executive | Read | Read | Read | Read/Write | Read |

**Document-Level Permissions:**
- Company-level access: Users can only access companies they're assigned to
- Relationship access: Inherits from parent Company permissions
- Task assignment: Users can edit tasks assigned to them
- Review period: Controllers and Executives can update status

### Data Protection

1. **PII (Personally Identifiable Information):**
   - EIN, account numbers encrypted
   - Employee contact info restricted to authorized roles
   - Audit trail for all changes to sensitive fields

2. **Access Logging:**
   - Enable `track_changes` on all DocTypes
   - Enable `track_seen` for compliance tracking
   - Log all access to encrypted fields

3. **Export Restrictions:**
   - Encrypted fields should not be exportable
   - Bulk export requires System Manager role
   - Export logs maintained for audit

---

## Implementation Notes

### Module Organization

All DocTypes should be created in the **Director** module:
```
blkshp_os/
├── blkshp_os/
│   ├── director/
│   │   ├── doctype/
│   │   │   ├── company/
│   │   │   ├── company_address/                    # Child Table
│   │   │   ├── company_phone/                      # Child Table
│   │   │   ├── company_email/                      # Child Table
│   │   │   ├── company_website/                    # Child Table
│   │   │   ├── banking_institution/
│   │   │   ├── banking_institution_address/            # Child Table
│   │   │   ├── banking_institution_contact/            # Child Table
│   │   │   ├── company_bank_relationship/
│   │   │   ├── bank_account/
│   │   │   ├── bank_account_document/                  # Child Table
│   │   │   ├── tax_authority/
│   │   │   ├── tax_authority_address/                  # Child Table
│   │   │   ├── tax_authority_contact/                  # Child Table
│   │   │   ├── company_tax_authority_relationship/
│   │   │   ├── tax_obligation/
│   │   │   ├── tax_filing_document/                    # Child Table
│   │   │   ├── insurance_broker/
│   │   │   ├── insurance_broker_address/               # Child Table
│   │   │   ├── insurance_broker_contact/               # Child Table
│   │   │   ├── insurance_carrier/
│   │   │   ├── insurance_carrier_address/              # Child Table
│   │   │   ├── insurance_carrier_contact/              # Child Table
│   │   │   ├── premium_finance_provider/
│   │   │   ├── premium_finance_provider_contact/       # Child Table
│   │   │   ├── insurance_policy/
│   │   │   ├── policy_covered_entity/                  # Child Table
│   │   │   ├── policy_covered_location/                # Child Table
│   │   │   ├── policy_document/                        # Child Table
│   │   │   ├── loan_relationship/
│   │   │   ├── loan_amortization_schedule/             # Child Table
│   │   │   ├── key_employee_relationship/
│   │   │   ├── task_type/
│   │   │   ├── task_type_dependency/                   # Child Table
│   │   │   ├── review_period/
│   │   │   ├── review_period_task/                     # Child Table
│   │   │   ├── project/
│   │   │   ├── project_milestone/                      # Child Table
│   │   │   └── project_task/                           # Child Table
```

### Implementation Order

Follow this sequence to respect dependencies:

1. **Week 1 - Core Master DocTypes:**
   - Company (enhance existing) with child tables:
     - Company Address
     - Company Phone
     - Company Email
     - Company Website
   - Task Type (with Task Type Dependency child table)

2. **Week 2 - Banking DocTypes:**
   - Banking Institution (master) with child tables:
     - Banking Institution Address
     - Banking Institution Contact
   - Company Bank Relationship
   - Bank Account (with Bank Account Document child table)

3. **Week 2 - Tax DocTypes:**
   - Tax Authority (master) with child tables:
     - Tax Authority Address
     - Tax Authority Contact
   - Company Tax Authority Relationship
   - Tax Obligation (with Tax Filing Document child table)

4. **Week 2-3 - Insurance DocTypes:**
   - Insurance Broker (master) with child tables:
     - Insurance Broker Address
     - Insurance Broker Contact
   - Insurance Carrier (master) with child tables:
     - Insurance Carrier Address
     - Insurance Carrier Contact
   - Premium Finance Provider (master) with child table:
     - Premium Finance Provider Contact
   - Insurance Policy with child tables:
     - Policy Covered Entity
     - Policy Covered Location
     - Policy Document

5. **Week 3 - Other Relationship DocTypes:**
   - Loan Relationship
   - Key Employee Relationship

6. **Week 3 - Complex DocTypes:**
   - Review Period (with Review Period Task child table)
   - Project (with Project Milestone and Project Task child tables)

### Frappe Bench Commands

```bash
# Create new DocType via Frappe Desk
bench --site [sitename] frappe --create-doctype

# Export DocType to JSON
bench --site [sitename] export-doc "DocType" "Company"

# Migrate database after changes
bench --site [sitename] migrate

# Clear cache
bench --site [sitename] clear-cache
```

### Database Indexing

**Recommended Indexes:**
- `Company.company_code` (unique index - auto-created by autoname)
- `Company.ein` (unique index)
- `Company Bank Relationship.company` (foreign key index)
- `Company Bank Relationship.banking_institution` (foreign key index)
- `Bank Account.company_bank_relationship` (foreign key index)
- `Company Tax Authority Relationship.company` (foreign key index)
- `Company Tax Authority Relationship.tax_authority` (foreign key index)
- `Tax Obligation.company_tax_authority_relationship` (foreign key index)
- `Tax Obligation.next_due_date` (for alert queries)
- `Insurance Policy.expiration_date` (for alert queries)
- `Insurance Policy.insurance_broker` (foreign key index)
- `Insurance Policy.insurance_carrier` (foreign key index)
- `Loan Relationship.company_bank_relationship` (foreign key index)
- `Loan Relationship.next_payment_date` (for alert queries)
- `Loan Relationship.loan_status` (for dashboard queries)
- `Key Employee Relationship.company` (foreign key index)
- `Review Period.company` (foreign key index)
- `Review Period.status` (for dashboard queries)
- `Project.company` (foreign key index)
- `Project.status` (for dashboard queries)

Frappe automatically creates indexes for:
- Primary keys (name field)
- Link fields (foreign keys)
- Unique fields

### Server-Side Scripts

**Required Server Scripts:**

1. **Company.py:**
   - Validate EIN format (XX-XXXXXXX)
   - Prevent circular parent_company references
   - Auto-generate company_code if not provided
   - Validate child tables:
     - Ensure at least one primary address exists
     - Ensure at least one primary email exists
     - Ensure only one primary per child table type
     - Validate email format in Company Email child table
     - Validate URL format in Company Website child table
     - Validate phone number format in Company Phone child table

2. **Bank Account.py:**
   - Validate routing number (9 digits)
   - Auto-update status to "Closed" if closing_date is set
   - Validate account_number encryption

3. **Tax Obligation.py:**
   - Validate responsible_party_email format
   - Auto-calculate next_due_date based on filing_frequency
   - Alert when next_due_date < 30 days

4. **Insurance Policy.py:**
   - Auto-update policy_status to "Expired" if expiration_date < today
   - Alert when expiration_date < 30 days
   - Validate at least one covered entity or covered location exists
   - Validate premium_finance_provider required if is_financed = 1

5. **Loan Relationship.py:**
   - Validate company_bank_relationship exists and is active
   - Validate interest_rate (0-100)
   - Validate loan_term_months > 0
   - Auto-calculate current_balance from amortization schedule (sum of unpaid principal portions)
   - Auto-calculate next_payment_date from amortization schedule (earliest unpaid scheduled_payment_date)
   - Auto-calculate accrued_interest based on current_balance, interest_rate, and days since last payment
   - Validate Loan Amortization Schedule child table:
     - payment_number must be sequential
     - scheduled_payment_date must be chronological
     - Sum of principal_portion must equal original_principal
     - Last payment remaining_balance must be 0.00
     - If is_paid = 1, require actual_payment_date
     - Auto-calculate variance = actual_payment_amount - scheduled_payment_amount
   - Auto-update loan_status to "Paid Off" when all payments paid and balance = 0
   - Alert when next_payment_date < 7 days
   - Alert when payment overdue (next_payment_date < today and not paid)

6. **Review Period.py:**
   - Calculate completion percentage from tasks
   - Enforce workflow (status transitions)
   - Validate all tasks completed before closing
   - Send notifications on status changes

6. **Task Type.py:**
   - Prevent circular dependencies
   - Validate recurrence pattern fields

### API Endpoints

All API endpoints documented separately in Feature-009. Endpoints should follow this structure:

```python
# /api/company_management.py

@frappe.whitelist()
def get_company_details(company_id):
    """Get company with all relationships"""
    pass

@frappe.whitelist()
def list_companies(filters=None, limit=20, offset=0):
    """List companies with pagination"""
    pass

# Additional endpoints per Feature-009
```

### Data Migration

**Existing Company DocType:**
- Current fields: `company_name`, `company_code`, `is_active`, `default_currency`, `description`
- Migration strategy:
  1. Add new fields to existing DocType (Feature-001)
  2. Populate `legal_name` from `company_name` for existing records
  3. No data loss - all existing companies preserved
  4. Set defaults for new required fields

---

## Acceptance Criteria Checklist

- [x] All 18 main DocTypes defined with complete field specifications
- [x] All 24 child tables designed
- [x] Data types specified for all fields
- [x] Validation rules documented for each DocType
- [x] Entity relationships mapped with ERD
- [x] Security requirements identified (encryption, permissions)
- [x] Implementation order defined (6 phases)
- [x] Database indexing strategy documented
- [x] Server-side validation requirements specified
- [x] Child table structures defined
- [x] Naming conventions specified
- [x] Migration strategy for existing Company DocType
- [x] Permission model documented

---

## Frontend Integration Notes

### Company Profile Page Structure

The Company Detail Page (Feature-011) will organize data using a tabbed interface:

**Page Route:** `/companies/[id]`

**Tab Structure:**
1. **General Tab** - Company DocType core information
   - Company name, legal name, DBA
   - Entity type, formation details
   - EIN, fiscal year
   - Status and ownership structure
   - All addresses (from Company Address child table)
   - All phone numbers (from Company Phone child table)
   - All emails (from Company Email child table)
   - All websites (from Company Website child table)
   - **Quick Links Section:**
     - "View Tasks" → Navigate to `/tasks?company=[id]` (Task Management module filtered by company)
     - "View Projects" → Navigate to `/projects?company=[id]` (Project Management module filtered by company)
     - "View Review Periods" → Navigate to `/review-periods?company=[id]` (Review Periods filtered by company)

2. **Banking Tab** - Financial accounts
   - Banking relationships (Company Bank Relationship)
   - Bank accounts per relationship (Bank Account)
   - Loans (Loan Relationship)
   - Account balances, statuses
   - Payment schedules
   - Quick actions: Add Banking Relationship, Add Bank Account, Add Loan

3. **Tax Tab** - Tax compliance
   - Tax authority relationships (Company Tax Authority Relationship)
   - Tax obligations per authority (Tax Obligation)
   - Filing frequencies and due dates
   - Jurisdictions
   - Responsible parties
   - Quick actions: Add Tax Authority, Add Tax Obligation

4. **Insurance Tab** - Insurance policies
   - All policies (Insurance Policy)
   - Broker, carrier, and finance provider details
   - Covered entities and locations per policy
   - Coverage details, premiums
   - Expiration tracking and alerts
   - Certificate downloads
   - Quick actions: Add Insurance Broker, Add Insurance Carrier, Add Insurance Policy

5. **People Tab** - Key employees
   - All key employees (Key Employee Relationship)
   - Roles, departments
   - Contact information
   - Emergency contacts
   - Quick actions: Add Key Employee

**Implementation Details:**
- Full UI/UX design in **Design-003 (Frontend Architecture) - BLK-75**
- API endpoints to fetch tab data in **Design-002 (API Endpoint Design) - BLK-74**
- Component hierarchy and state management in **Design-003**

---

## Next Steps

1. **Review & Approval:** Get this design reviewed and approved (BLK-73)
2. **Subscription Tier Architecture Document:** Create dedicated architectural document (Design-004) defining:
   - Detailed tier feature matrix for all modules
   - Subscription tier management and upgrades/downgrades
   - Feature-gating implementation patterns (backend, frontend, API)
   - GL integration architecture for Advanced tier
   - Permission model per tier
   - Billing and subscription management
3. **API Design:** Move to Design-002 (API Endpoint Design) - BLK-74
4. **Frontend Design:** Move to Design-003 (Frontend Architecture) - BLK-75
5. **Implementation:** Begin Feature-001 (Enhanced Company DocType)

---

**Document Version:** 1.6
**Last Updated:** 2025-11-17
**Status:** Complete - Ready for Review

**Revision History:**
- v1.0 (2025-11-16): Initial design with fixed address/contact fields
- v1.1 (2025-11-17): Updated Company DocType to use child tables for addresses, phones, emails, and websites for unlimited flexibility
- v1.2 (2025-11-17): Restructured banking from 1 DocType to 3 (Banking Institution, Company Bank Relationship, Bank Account) and added Banking Institution Address child table for multi-branch support
- v1.3 (2025-11-17): Major refactoring - normalized Tax (3 DocTypes: Tax Authority, Company Tax Authority Relationship, Tax Obligation) and Insurance (5 DocTypes: Insurance Broker, Insurance Carrier, Premium Finance Provider, Insurance Policy) following same pattern as Banking. Insurance supports multiple brokers, carriers, finance providers, and can cover multiple entities/locations per policy. Total: 16 main DocTypes + 21 child tables = 37 DocTypes
- v1.4 (2025-11-17): Restructured Loan Relationship to link to Banking Institution via Company Bank Relationship (following same pattern as Bank Account). Added Loan Amortization Schedule child table to enable automated loan management including auto-calculation of current balance, next payment date, and accrued interest. Renamed fields for consistency (original_principal, loan_term_months). Total: 16 main DocTypes + 22 child tables = 38 DocTypes
- v1.5 (2025-11-17): Added Subscription Tier Architecture - two-tier model (Basic/Advanced) that applies across ALL modules. Added `subscription_tier` field to Company DocType. Documented tier-specific features for Loan Relationship including Basic (task automation only) vs Advanced (amortization schedules, auto-calculations, GL integration, drafted journals). This architectural pattern will be applied to all modules going forward.
- v1.6 (2025-11-17): **MAJOR ARCHITECTURAL CHANGE** - Replaced static subscription tiers with flexible feature-based subscription system. Removed `subscription_tier` field, added `subscription_plan` link and `Company Feature` child table. Created 2 new DocTypes: Platform Feature (feature registry) and Subscription Plan (optional bundles). Supports both pre-built plans AND custom à la carte feature selection. Added comprehensive Feature Registry documenting all 22 Company Management features with codes, pricing, and dependencies. Created Linear issue BLK-195 for detailed feature architecture design. This enables granular control and flexible pricing models. Total: 18 main DocTypes + 24 child tables = 42 DocTypes
