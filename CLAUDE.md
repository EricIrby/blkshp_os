# The Pass - Project Memory & Conventions

> **Project:** The Pass (formerly BLKSHP OS)
> **Description:** Multi-Entity Hospitality Management Platform
> **Last Updated:** 2025-11-17

---

## Project Overview

**The Pass** (formerly BLKSHP OS) is a multi-entity hospitality management platform built on Frappe Framework v15+ with a Next.js 14 frontend. The platform serves management company leadership and accounting teams managing multiple hospitality entities (hotels, restaurants, venues).

### Tech Stack

- **Backend:** Frappe Framework v15+ (Python)
- **Frontend:** Next.js 14 (TypeScript/React)
- **Database:** MariaDB/MySQL (via Frappe ORM)
- **Deployment:** Production on DigitalOcean/GCP/AWS
- **Version Control:** Git + GitHub
- **Project Management:** Linear (team: BLKSHP)

---

## Critical Architectural Decisions

### 1. Feature-Based Subscription Architecture (Nov 2025)

**Decision:** Use flexible feature flags instead of static subscription tiers.

**Why:** Enables custom-built feature sets per client with granular pricing based on activated/deactivated features, while still supporting optional pre-built subscription plans for convenience.

**Implementation:**
- Each platform capability is an individual feature with unique code (e.g., `loan_amortization_schedules`)
- Features tracked per company via `Company Feature` child table
- Optional subscription plans via `Subscription Plan` DocType that bundle features
- Server-side pattern: `if has_feature(company, "feature_code"):`
- Frontend: Conditional rendering based on enabled features
- API: Feature-gating at endpoint level

**Key DocTypes:**
- `Platform Feature` - Feature registry with codes, pricing, dependencies
- `Subscription Plan` - Pre-built feature bundles (optional)
- `Company Feature` (child table) - Enabled features per company
- `Plan Feature` (child table) - Features included in plans

**Feature Categories:**
- **Basic** (free/included) - Core CRUD operations, basic automation
- **Premium** (paid add-ons) - Advanced features, analytics, automation
- **Enterprise** (high-tier) - GL integration, consolidation, auto-drafted journals

### 2. Normalized Database Architecture

**Pattern:** Three-tier structure for shared entities:

1. **Master Entities** (e.g., Banking Institution, Tax Authority, Insurance Broker) - Shared across companies
2. **Junction Entities** (e.g., Company Bank Relationship, Company Tax Authority Relationship) - Links
3. **Specific Records** (e.g., Bank Account, Tax Obligation, Insurance Policy) - Company-specific instances

**Why:** Prevents data duplication, supports multi-entity operations, enables shared vendor/institution management.

**Examples:**
- **Banking:** Institution (master) → Company Relationship (junction) → Bank Account (specific)
- **Tax:** Authority (master) → Company Relationship (junction) → Tax Obligation (specific)
- **Insurance:** Broker + Carrier + Finance Provider (masters) → Insurance Policy (specific with covered entities/locations)

### 3. Loan Management Integration

**Decision:** Loans link to Banking Institution via Company Bank Relationship (not standalone).

**Why:** Loans typically come from existing banking partners. Keeps institution data consistent and avoids duplication.

**Key Features:**
- `Loan Amortization Schedule` child table for detailed payment tracking
- Auto-calculated fields: `current_balance`, `next_payment_date`, `accrued_interest`
- Supports both basic tracking (manual entry) and advanced (auto-calculations + GL integration)
- Feature-gated: Amortization features only available with appropriate feature flags

### 4. Child Tables for Multi-Valued Attributes

**Pattern:** Use child tables instead of fixed fields for unlimited entries with custom labels.

**Applied to:**
- Company: addresses, phones, emails, websites, features
- Banking Institution: addresses (branches), contacts
- Tax Authority: addresses, contacts
- Insurance entities: addresses, contacts
- Loans: amortization schedules
- Projects: milestones, tasks
- Review Periods: tasks
- Task Types: dependencies
- Subscription Plans: features

**Benefits:** Unlimited entries, custom labels, `is_primary` flags, better data normalization.

---

## Development Conventions

### DocType Naming

- **Main DocTypes:** PascalCase with spaces (e.g., `Banking Institution`, `Tax Authority`)
- **Child Tables:** Parent name + descriptor (e.g., `Company Address`, `Loan Amortization Schedule`)
- **Feature Codes:** lowercase_with_underscores (e.g., `loan_amortization_schedules`)
- **Plan Codes:** lowercase-with-hyphens (e.g., `professional`, `enterprise`)

### Field Naming

- **Standard:** snake_case (e.g., `company_name`, `interest_rate`)
- **Encrypted fields:** Use `Password` field type (e.g., `ein`, `account_number`, `loan_number`)
- **Booleans:** Prefix with `is_` (e.g., `is_active`, `is_primary`, `is_enabled`)
- **Dates:** Suffix with `_date` (e.g., `origination_date`, `maturity_date`)

### Child Table Patterns

**Always include:**
- Primary identifier field (e.g., `address_type`, `contact_name`)
- `is_primary` checkbox (for addresses, contacts, etc.)
- Optional `notes` or `description` field for flexibility

**Common field sets:**
- **Addresses:** street, suite_unit, city, state, zip_code, country, is_primary
- **Contacts:** contact_name, title, email, phone, is_primary
- **Documents:** document_name, document_type, file_attachment, external_url

---

## Feature Implementation Patterns

### Server-side (Python)

```python
from blkshp_os.utils import has_feature

def validate(self):
    """Validation method with feature-gating"""
    company = frappe.get_doc("Company", self.company)

    if has_feature(company, "loan_amortization_schedules"):
        # Execute premium feature logic
        self.calculate_amortization_schedule()
        self.validate_amortization_totals()
    else:
        # Basic tier - manual entry only
        if self.amortization_schedule:
            frappe.throw("Amortization schedules require the loan_amortization_schedules feature")
```

### Frontend (Next.js/TypeScript)

```typescript
import { hasFeature } from '@/lib/features';

export default function LoanDetail({ loan, company }) {
  return (
    <div>
      {/* Basic information - always visible */}
      <LoanBasicInfo loan={loan} />

      {/* Premium feature - conditionally rendered */}
      {hasFeature(company, 'loan_amortization_schedules') && (
        <AmortizationScheduleTable
          data={loan.amortization_schedule}
        />
      )}

      {/* Upgrade prompt for disabled features */}
      {!hasFeature(company, 'loan_amortization_schedules') && (
        <UpgradePrompt feature="loan_amortization_schedules" />
      )}
    </div>
  );
}
```

### API Endpoint

```python
@frappe.whitelist()
def get_loan_details(loan_id):
    """API endpoint with feature-based data filtering"""
    loan = frappe.get_doc("Loan Relationship", loan_id)
    company = frappe.get_doc("Company", loan.company)

    # Basic data - always included
    data = {
        "basic_info": loan.as_dict(),
    }

    # Premium data - only if feature enabled
    if has_feature(company, "loan_amortization_schedules"):
        data["amortization_schedule"] = loan.get("amortization_schedule")

    if has_feature(company, "loan_auto_calculations"):
        data["calculated_fields"] = {
            "current_balance": loan.current_balance,
            "accrued_interest": loan.accrued_interest,
            "next_payment_date": loan.next_payment_date
        }

    return data
```

---

## Common Patterns and Best Practices

### 1. Encryption for Sensitive Data

**Always use `Password` field type for:**
- EIN/Tax IDs (`ein`)
- Bank account numbers (`account_number`)
- Loan numbers (`loan_number`)
- SSNs or personal identifiers
- Any PII or financial identifiers

**Why:** Frappe automatically encrypts Password fields using AES-256.

**Important:** Once encrypted, data cannot be queried in filters. Store display versions separately if needed (e.g., `account_number_last_4`).

### 2. Link Fields vs Data Fields

**Use Link fields when:**
- Referencing other DocTypes (e.g., `company`, `banking_institution`)
- Need Frappe's referential integrity and cascade behavior
- Want dropdown selection from existing records

**Use Data fields when:**
- Free-form text (e.g., `company_name`, `address_label`)
- Feature codes that may not exist yet
- External identifiers (e.g., routing numbers, tax IDs)

### 3. Validation in Both Places

**Server-side (Required):**
- Always validate in Python (`DocType.validate()` method)
- Runs on API calls, imports, and UI saves
- Security-critical validation MUST be server-side
- Cannot be bypassed

**Client-side (Optional but recommended):**
- Form scripts for better UX
- Instant feedback before submission
- Example: Email format, phone format, date ranges
- Can be bypassed - never rely on alone

### 4. Feature Dependencies

**Always check dependencies before enabling:**

```python
def enable_feature(company, feature_code):
    """Enable a feature with dependency checking"""
    feature = frappe.get_doc("Platform Feature", feature_code)

    # Check if required feature is enabled
    if feature.requires_feature:
        if not has_feature(company, feature.requires_feature):
            frappe.throw(
                f"This feature requires '{feature.requires_feature}' to be enabled first"
            )

    # Add to Company Feature child table
    company.append("features", {
        "feature_code": feature_code,
        "is_enabled": 1,
        "enabled_date": today(),
        "source": "Custom"
    })
    company.save()
```

### 5. Child Table Best Practices

**Creating child table entries:**
```python
# Good - using append
company.append("addresses", {
    "address_type": "Corporate",
    "street": "123 Main St",
    "city": "New York",
    "state": "NY",
    "zip_code": "10001",
    "is_primary": 1
})

# Also good - for multiple entries
for address_data in addresses_list:
    company.append("addresses", address_data)

company.save()
```

**Querying child tables:**
```python
# Get all primary addresses across all companies
primary_addresses = frappe.get_all(
    "Company Address",
    filters={"is_primary": 1},
    fields=["parent", "street", "city", "state"]
)

# Get addresses for specific company
company_addresses = frappe.get_doc("Company", company_name).addresses
```

---

## File Structure

### Documentation

```
docs/
├── 00-CURRENT/                    # Current active documentation
│   └── COMPANY-MANAGEMENT-DATA-MODEL.md
├── ARCHIVE/                       # Historical/deprecated docs
├── GUIDES/                        # Development guides
│   ├── DEVELOPMENT-GUIDE.md
│   ├── GIT-WORKFLOW.md
│   ├── TESTING-GUIDE.md
│   └── LINEAR-QUICK-START.md
├── API/                           # API documentation
│   ├── API-REFERENCE.md
│   └── API-AUTHENTICATION.md
└── README.md                      # Main project documentation
```

### Code Structure

```
blkshp_os/
├── director/                      # Company Management module
│   ├── doctype/
│   │   ├── company/
│   │   ├── banking_institution/
│   │   ├── company_bank_relationship/
│   │   ├── bank_account/
│   │   ├── tax_authority/
│   │   ├── company_tax_authority_relationship/
│   │   ├── tax_obligation/
│   │   ├── insurance_broker/
│   │   ├── insurance_carrier/
│   │   ├── premium_finance_provider/
│   │   ├── insurance_policy/
│   │   ├── loan_relationship/
│   │   ├── key_employee_relationship/
│   │   ├── task_type/
│   │   ├── review_period/
│   │   ├── project/
│   │   ├── platform_feature/
│   │   └── subscription_plan/
│   └── page/                      # Custom pages
├── utils/                         # Utility functions
│   └── features.py                # Feature checking helpers
├── hooks.py                       # Frappe hooks
└── patches/                       # Database migrations
```

---

## Testing Strategy

### Unit Tests

**Location:** `blkshp_os/director/doctype/[doctype_name]/test_[doctype_name].py`

**Pattern:**
```python
import frappe
import unittest

class TestLoanRelationship(unittest.TestCase):
    def setUp(self):
        """Create test data before each test"""
        self.company = frappe.get_doc({
            "doctype": "Company",
            "company_name": "Test Company",
            "company_code": "TEST",
            "legal_name": "Test Company LLC"
        }).insert()

    def test_feature_gating(self):
        """Test that premium features are properly gated"""
        loan = frappe.get_doc({
            "doctype": "Loan Relationship",
            "company_bank_relationship": self.bank_relationship.name,
            "loan_type": "Term Loan",
            "original_principal": 100000,
            "interest_rate": 5.0
        }).insert()

        # Should raise error without feature enabled
        with self.assertRaises(frappe.ValidationError):
            loan.append("amortization_schedule", {
                "payment_number": 1,
                "scheduled_payment_date": today(),
                "scheduled_payment_amount": 1000
            })
            loan.save()

    def tearDown(self):
        """Clean up test data after each test"""
        frappe.delete_doc("Company", self.company.name, force=1)
```

### Integration Tests

Test feature combinations, multi-entity scenarios, and GL integration.

**Example:**
```python
def test_loan_gl_integration():
    """Test that GL entries are created when feature is enabled"""
    # Enable GL integration features
    enable_feature(company, "gl_integration_full")
    enable_feature(company, "loan_gl_integration")

    # Create loan
    loan = create_test_loan(company)

    # Verify GL entries were created
    gl_entries = frappe.get_all("GL Entry",
        filters={"voucher_no": loan.name}
    )
    assert len(gl_entries) > 0
```

---

## Workflow and Process

### Git Workflow

1. **Branch naming:** `feature/blk-[issue-number]` (e.g., `feature/blk-195`)
2. **Commits:** Descriptive messages, reference Linear issue
   - Format: `feat(loans): add amortization schedule child table (BLK-73)`
3. **Pull Requests:** Link to Linear issue, include testing notes
4. **Reviews:** Required before merge to main

### Linear Workflow

**Issue Prefixes:**
- `Design-001`, `Design-002`, etc. - Design documents
- `Feature-001`, `Feature-002`, etc. - Feature implementations
- `Bug-001`, `Bug-002`, etc. - Bug fixes

**Labels:**
- `design` - Design documents
- `architecture` - Architectural decisions
- `backend` - Frappe/Python work
- `frontend` - Next.js/React work
- `documentation` - Docs updates

### Design → Implementation Flow

1. **Design Phase:** Create design document (e.g., BLK-73)
   - Define DocTypes, fields, relationships
   - Document features and pricing
   - Get approval before coding

2. **Implementation Phase:** Create feature issues
   - Feature-001: Implement DocType schemas
   - Feature-002: Implement server-side logic
   - Feature-003: Build frontend components
   - Feature-004: Write tests

3. **Review Phase:** Testing and refinement
   - Unit tests pass
   - Integration tests pass
   - Code review approved
   - Demo to stakeholders

---

## Quick Reference

### Common Frappe Commands

```bash
# Start development server
bench start

# Run tests
bench run-tests --app blkshp_os

# Run specific test
bench run-tests --app blkshp_os --doctype "Loan Relationship"

# Create new DocType
bench new-doctype

# Migrate database
bench --site [site-name] migrate

# Clear cache
bench --site [site-name] clear-cache

# Frappe console (Python REPL with Frappe context)
bench --site [site-name] console

# Install app to site
bench --site [site-name] install-app blkshp_os
```

### Helpful Frappe Patterns

```python
# Get single document
doc = frappe.get_doc("DocType Name", "document-name")

# Create new document
doc = frappe.get_doc({
    "doctype": "DocType Name",
    "field": "value"
})
doc.insert()

# Query database (returns list of dicts)
companies = frappe.get_all("Company",
    filters={"is_active": 1},
    fields=["name", "company_name", "company_code"],
    order_by="company_name asc",
    limit=20
)

# Get single value
count = frappe.db.count("Company", {"is_active": 1})

# Check if exists
exists = frappe.db.exists("Company", "ACME")

# Get value from database
company_name = frappe.db.get_value("Company", "ACME", "company_name")

# Set value in database (bypass validation)
frappe.db.set_value("Company", "ACME", "is_active", 0)

# Check feature
from blkshp_os.utils.features import has_feature
if has_feature(company, "loan_amortization_schedules"):
    # Execute premium feature logic
    pass
```

---

## Important Reminders

### For AI Assistants (Claude)

1. **Always check feature enablement** before executing premium/enterprise features
2. **Use child tables** for multi-valued attributes (addresses, contacts, etc.)
3. **Normalize shared entities** (banking institutions, tax authorities, insurance entities)
4. **Encrypt sensitive data** using Password field type
5. **Follow naming conventions** strictly (snake_case fields, PascalCase DocTypes, lowercase_underscore feature codes)
6. **Document feature dependencies** in Platform Feature registry
7. **Update version history** when making significant changes to design docs
8. **Reference Linear issues** in all commits and documentation

### For Developers

1. **Feature-first development:** Always consider which subscription tier a feature belongs to
2. **Don't hardcode tiers:** Use `has_feature()` helper, never check specific tier/plan names
3. **Test both paths:** Test basic AND premium feature paths
4. **Document pricing:** When adding features, document in Platform Feature with pricing
5. **Security-first:** Validate server-side, encrypt sensitive data, check permissions
6. **Child tables:** Use for one-to-many relationships instead of JSON fields
7. **Link fields:** Use for DocType references to maintain referential integrity

### For Product Decisions

1. **Feature granularity:** Each meaningful capability should be a separate feature
2. **Clear dependencies:** Document what features require other features
3. **Pricing strategy:** Basic (free), Premium ($15-40/mo), Enterprise ($50-100+/mo)
4. **Plan discounts:** 20-40% savings for bundled plans vs à la carte
5. **Customer flexibility:** Always support custom feature combinations
6. **Future modules:** Apply same feature-based pattern to all modules

---

## Stakeholders

**Project Owner:** Eric (eric@blkshp.co)

**Linear Team:** BLKSHP
- Team ID: `439094a9-d7dc-4816-a4de-dd0c2c47d800`

**Target Users:** Management company leadership and accounting teams

---

**End of Project Memory Document**

*This document focuses on timeless conventions, patterns, and architectural decisions. For current project status, tasks, and progress tracking, see Linear issues and session notes in `/docs/00-CURRENT/`.*
