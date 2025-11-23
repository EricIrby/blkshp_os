# Company Management Data Model

**Issue:** BLK-73 (Design-001)
**Status:** In Progress
**Due:** 2025-11-16
**Last Updated:** 2025-11-16

---

## Overview

This document defines the complete DocType schema for all Company Management features in The Pass. These DocTypes form the foundation of the multi-entity hospitality management platform.

---

## 1. Enhanced Company DocType

**DocType Name:** `Company`
**Module:** `Director`
**Naming:** Auto-generated from Company Name

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `company_name` | Data | Company Name | Yes | Legal or operating name |
| `company_code` | Data | Company Code | Yes | Short code (auto-generated) |
| `legal_name` | Data | Legal Name | No | Full legal entity name |
| `dba` | Data | DBA | No | "Doing Business As" name |
| `ein` | Data | EIN | No | Employer Identification Number |
| `entity_type` | Select | Entity Type | No | LLC, Corporation, Partnership, etc. |
| `formation_date` | Date | Formation Date | No | Date entity was formed |
| `fiscal_year_start` | Select | Fiscal Year Start | No | Month fiscal year starts |

### Status & Settings

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_active` | Check | Active | Yes | Company is active |
| `status` | Select | Status | Yes | Active, Inactive, Pending, Closed |
| `default_currency` | Link | Default Currency | Yes | Link to Currency |

### Contact Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `primary_phone` | Data | Primary Phone | No | Main phone number |
| `primary_email` | Data | Primary Email | No | Main email address |
| `website` | Data | Website | No | Company website URL |

### Addresses (Child Table)

**Child DocType Name:** `Company Address`

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `address_type` | Select | Address Type | Yes | Legal, Mailing, Physical, Billing |
| `address_line1` | Data | Address Line 1 | Yes | Street address |
| `address_line2` | Data | Address Line 2 | No | Suite, unit, etc. |
| `city` | Data | City | Yes | City |
| `state` | Data | State/Province | Yes | State or province |
| `postal_code` | Data | Postal Code | Yes | ZIP or postal code |
| `country` | Link | Country | Yes | Link to Country |
| `is_primary` | Check | Is Primary | No | Primary address flag |

### Financial Settings

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `accounting_method` | Select | Accounting Method | No | Cash, Accrual |
| `tax_id` | Data | Tax ID | No | State tax ID |
| `cost_center` | Link | Cost Center | No | Link to Cost Center |
| `company_group` | Link | Company Group | No | Link to Company Group |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `description` | Text Editor | Description | No | Company description |
| `notes` | Text Editor | Notes | No | Internal notes |

### Standard Fields
- `owner`
- `creation`
- `modified`
- `modified_by`

### Permissions
- Read: All users with Company access
- Write: Company Administrators
- Create: System Administrators
- Delete: System Administrators

---

## 2. Bank Relationship DocType

**DocType Name:** `Company Bank`
**Module:** `Company Management`
**Naming:** Auto-generated (BANK-YYYY-XXXXX)

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `company` | Link | Company | Yes | Link to Company |
| `bank_name` | Data | Bank Name | Yes | Name of bank |
| `account_type` | Select | Account Type | Yes | Checking, Savings, Money Market, Line of Credit |
| `account_number` | Password | Account Number | Yes | Encrypted account number |
| `routing_number` | Data | Routing Number | No | Bank routing number |
| `account_nickname` | Data | Account Nickname | No | Friendly name for account |

### Account Details

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `opening_date` | Date | Opening Date | No | Date account was opened |
| `current_balance` | Currency | Current Balance | No | Current account balance |
| `available_balance` | Currency | Available Balance | No | Available funds |
| `credit_limit` | Currency | Credit Limit | No | Credit limit (for LOC) |
| `interest_rate` | Percent | Interest Rate | No | Interest rate |

### Contact Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `bank_phone` | Data | Bank Phone | No | Bank contact phone |
| `bank_email` | Data | Bank Email | No | Bank contact email |
| `branch_address` | Small Text | Branch Address | No | Branch location |
| `account_manager` | Data | Account Manager | No | Name of account manager |
| `manager_phone` | Data | Manager Phone | No | Account manager phone |
| `manager_email` | Data | Manager Email | No | Account manager email |

### Online Banking

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `online_banking_url` | Data | Online Banking URL | No | Bank's website |
| `username` | Password | Username | No | Encrypted username |
| `has_online_access` | Check | Has Online Access | No | Online banking enabled |

### Status

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_active` | Check | Active | Yes | Account is active |
| `status` | Select | Status | Yes | Active, Inactive, Closed |
| `closed_date` | Date | Closed Date | No | Date account was closed |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `notes` | Text Editor | Notes | No | Internal notes |

### Permissions
- Read: Company Viewers, Accountants
- Write: Company Editors, Accountants
- Create: Company Administrators
- Delete: System Administrators

---

## 3. Tax Entity Relationship DocType

**DocType Name:** `Company Tax Entity`
**Module:** `Company Management`
**Naming:** Auto-generated (TAX-YYYY-XXXXX)

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `company` | Link | Company | Yes | Link to Company |
| `tax_type` | Select | Tax Type | Yes | Federal, State, Local, Sales Tax, Payroll |
| `tax_authority` | Data | Tax Authority | Yes | IRS, State DOR, etc. |
| `tax_id` | Data | Tax ID | No | Tax identification number |
| `filing_frequency` | Select | Filing Frequency | Yes | Monthly, Quarterly, Annual |

### Filing Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `filing_method` | Select | Filing Method | No | Electronic, Paper, Third Party |
| `filing_deadline` | Data | Filing Deadline | No | Day of month/quarter |
| `next_filing_date` | Date | Next Filing Date | No | Next deadline |
| `last_filing_date` | Date | Last Filing Date | No | Most recent filing |

### Contact Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `authority_phone` | Data | Authority Phone | No | Contact phone |
| `authority_email` | Data | Authority Email | No | Contact email |
| `authority_website` | Data | Authority Website | No | Filing portal URL |
| `account_number` | Data | Account Number | No | Account with authority |

### Login Credentials

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `portal_username` | Password | Portal Username | No | Encrypted username |
| `has_portal_access` | Check | Has Portal Access | No | Online portal enabled |

### Status

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_active` | Check | Active | Yes | Tax entity is active |
| `registration_date` | Date | Registration Date | No | Date registered |
| `exemption_status` | Data | Exemption Status | No | Any exemptions |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `notes` | Text Editor | Notes | No | Internal notes |

### Permissions
- Read: Company Viewers, Accountants
- Write: Accountants
- Create: Company Administrators
- Delete: System Administrators

---

## 4. Insurance Relationship DocType

**DocType Name:** `Company Insurance`
**Module:** `Company Management`
**Naming:** Auto-generated (INS-YYYY-XXXXX)

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `company` | Link | Company | Yes | Link to Company |
| `insurance_type` | Select | Insurance Type | Yes | General Liability, Property, Workers Comp, etc. |
| `insurance_carrier` | Data | Insurance Carrier | Yes | Name of insurance company |
| `policy_number` | Data | Policy Number | Yes | Policy number |
| `policy_holder` | Data | Policy Holder | No | Name on policy |

### Coverage Details

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `coverage_amount` | Currency | Coverage Amount | No | Total coverage |
| `deductible` | Currency | Deductible | No | Deductible amount |
| `premium_amount` | Currency | Premium Amount | No | Annual/monthly premium |
| `premium_frequency` | Select | Premium Frequency | No | Monthly, Quarterly, Annual |

### Dates

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `effective_date` | Date | Effective Date | Yes | Coverage start date |
| `expiration_date` | Date | Expiration Date | Yes | Coverage end date |
| `renewal_date` | Date | Renewal Date | No | Next renewal date |
| `last_review_date` | Date | Last Review Date | No | Last policy review |

### Contact Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `agent_name` | Data | Agent Name | No | Insurance agent name |
| `agent_phone` | Data | Agent Phone | No | Agent contact phone |
| `agent_email` | Data | Agent Email | No | Agent contact email |
| `carrier_phone` | Data | Carrier Phone | No | Carrier customer service |
| `claims_phone` | Data | Claims Phone | No | Claims department phone |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `coverage_details` | Text Editor | Coverage Details | No | Detailed coverage info |
| `exclusions` | Text Editor | Exclusions | No | Coverage exclusions |
| `notes` | Text Editor | Notes | No | Internal notes |

### Status

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_active` | Check | Active | Yes | Policy is active |
| `auto_renew` | Check | Auto Renew | No | Auto-renewal enabled |

### Permissions
- Read: Company Viewers, Accountants
- Write: Company Editors, Accountants
- Create: Company Administrators
- Delete: System Administrators

---

## 5. Loan Relationship DocType

**DocType Name:** `Company Loan`
**Module:** `Company Management`
**Naming:** Auto-generated (LOAN-YYYY-XXXXX)

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `company` | Link | Company | Yes | Link to Company |
| `loan_type` | Select | Loan Type | Yes | Term Loan, Line of Credit, Mortgage, Equipment, SBA |
| `lender_name` | Data | Lender Name | Yes | Name of lender |
| `loan_number` | Data | Loan Number | No | Loan account number |
| `purpose` | Select | Purpose | No | Working Capital, Equipment, Real Estate, etc. |

### Loan Terms

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `original_amount` | Currency | Original Amount | Yes | Original loan amount |
| `current_balance` | Currency | Current Balance | No | Current outstanding balance |
| `interest_rate` | Percent | Interest Rate | Yes | Annual interest rate |
| `term_months` | Int | Term (Months) | No | Loan term in months |
| `payment_amount` | Currency | Payment Amount | No | Regular payment amount |
| `payment_frequency` | Select | Payment Frequency | No | Monthly, Quarterly, Annual |

### Important Dates

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `origination_date` | Date | Origination Date | Yes | Loan start date |
| `maturity_date` | Date | Maturity Date | No | Loan end date |
| `first_payment_date` | Date | First Payment Date | No | First payment due date |
| `next_payment_date` | Date | Next Payment Date | No | Next payment due date |

### Contact Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `loan_officer` | Data | Loan Officer | No | Loan officer name |
| `officer_phone` | Data | Officer Phone | No | Loan officer phone |
| `officer_email` | Data | Officer Email | No | Loan officer email |
| `lender_phone` | Data | Lender Phone | No | Lender customer service |
| `lender_website` | Data | Lender Website | No | Lender website URL |

### Collateral & Guarantees

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `collateral` | Text Editor | Collateral | No | Description of collateral |
| `personal_guarantee` | Check | Personal Guarantee | No | Personal guarantee required |
| `guarantor` | Data | Guarantor | No | Name of guarantor |

### Status

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_active` | Check | Active | Yes | Loan is active |
| `status` | Select | Status | Yes | Active, Paid Off, Defaulted |
| `payoff_date` | Date | Payoff Date | No | Date loan was paid off |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `notes` | Text Editor | Notes | No | Internal notes |

### Permissions
- Read: Company Viewers, Accountants
- Write: Company Editors, Accountants
- Create: Company Administrators
- Delete: System Administrators

---

## 6. Key Employee Relationship DocType

**DocType Name:** `Company Key Employee`
**Module:** `Company Management`
**Naming:** Auto-generated (EMP-YYYY-XXXXX)

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `company` | Link | Company | Yes | Link to Company |
| `employee_name` | Data | Employee Name | Yes | Full name |
| `role` | Select | Role | Yes | Owner, CEO, CFO, Controller, Manager, etc. |
| `title` | Data | Title | No | Official job title |
| `department` | Link | Department | No | Link to Department |

### Contact Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `work_email` | Data | Work Email | No | Work email address |
| `work_phone` | Data | Work Phone | No | Work phone number |
| `mobile_phone` | Data | Mobile Phone | No | Mobile phone number |
| `personal_email` | Data | Personal Email | No | Personal email address |

### Employment Details

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `start_date` | Date | Start Date | No | Employment start date |
| `end_date` | Date | End Date | No | Employment end date |
| `employment_status` | Select | Employment Status | Yes | Active, On Leave, Terminated |
| `employment_type` | Select | Employment Type | No | Full-time, Part-time, Contractor |

### Responsibilities

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `responsibilities` | Text Editor | Responsibilities | No | Key responsibilities |
| `signatory_authority` | Check | Signatory Authority | No | Can sign on behalf of company |
| `financial_access` | Check | Financial Access | No | Has access to financials |

### Emergency Contact

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `emergency_contact_name` | Data | Emergency Contact Name | No | Emergency contact |
| `emergency_contact_phone` | Data | Emergency Contact Phone | No | Emergency phone |
| `emergency_relationship` | Data | Emergency Relationship | No | Relationship |

### Status

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_active` | Check | Active | Yes | Employee is active |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `notes` | Text Editor | Notes | No | Internal notes |

### Permissions
- Read: Company Viewers, Accountants
- Write: Company Administrators
- Create: Company Administrators
- Delete: System Administrators

---

## 7. Task Type DocType

**DocType Name:** `Task Type`
**Module:** `Company Management`
**Naming:** Prompt/Auto-generated

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `task_name` | Data | Task Name | Yes | Name of task template |
| `task_description` | Text Editor | Description | No | Detailed task description |
| `category` | Select | Category | Yes | Accounting, Compliance, Operations, HR |
| `assigned_role` | Link | Assigned Role | Yes | Link to Role (who performs task) |

### Recurrence Settings

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_recurring` | Check | Is Recurring | Yes | Task recurs automatically |
| `recurrence_pattern` | Select | Recurrence Pattern | No | Daily, Weekly, Monthly, Quarterly, Annual |
| `recurrence_day` | Int | Recurrence Day | No | Day of week/month/quarter |
| `start_date` | Date | Start Date | No | When recurrence starts |
| `end_date` | Date | End Date | No | When recurrence ends |

### Task Settings

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `priority` | Select | Priority | Yes | Low, Medium, High, Urgent |
| `estimated_hours` | Float | Estimated Hours | No | Expected time to complete |
| `due_offset_days` | Int | Due Offset (Days) | No | Days from creation to due date |
| `reminder_days` | Int | Reminder (Days Before) | No | Days before due to send reminder |

### Dependencies

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `depends_on_task` | Link | Depends On Task | No | Link to prerequisite Task Type |

### Checklist (Child Table)

**Child DocType Name:** `Task Type Checklist Item`

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `item_description` | Data | Item | Yes | Checklist item text |
| `is_required` | Check | Required | No | Must be completed |

### Status

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `is_active` | Check | Active | Yes | Task type is active |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `notes` | Text Editor | Notes | No | Internal notes |

### Permissions
- Read: All users
- Write: Task Administrators
- Create: Company Administrators
- Delete: System Administrators

---

## 8. Review Period DocType

**DocType Name:** `Review Period`
**Module:** `Company Management`
**Naming:** Auto-generated (format: COMPANY-YYYYMM)

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `company` | Link | Company | Yes | Link to Company |
| `period_type` | Select | Period Type | Yes | Monthly, Quarterly, Annual |
| `period_name` | Data | Period Name | Yes | e.g., "November 2025" |
| `fiscal_year` | Int | Fiscal Year | Yes | Fiscal year |
| `fiscal_period` | Int | Fiscal Period | Yes | Period number (1-12) |

### Period Dates

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `start_date` | Date | Start Date | Yes | Period start date |
| `end_date` | Date | End Date | Yes | Period end date |
| `close_date` | Date | Close Date | No | When period was closed |

### Workflow Status

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `status` | Select | Status | Yes | Open, In Progress, Controller Review, Executive Review, Closed |
| `assigned_to` | Link | Assigned To | No | Link to User |
| `controller_approved_by` | Link | Controller Approved By | No | Link to User |
| `controller_approval_date` | Datetime | Controller Approval Date | No | Timestamp |
| `executive_approved_by` | Link | Executive Approved By | No | Link to User |
| `executive_approval_date` | Datetime | Executive Approval Date | No | Timestamp |

### Progress Tracking

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `total_tasks` | Int | Total Tasks | No | Total task count (auto-calculated) |
| `completed_tasks` | Int | Completed Tasks | No | Completed task count (auto-calculated) |
| `completion_percentage` | Percent | Completion % | No | Auto-calculated progress |

### Financial Summary (Optional)

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `total_revenue` | Currency | Total Revenue | No | Period revenue |
| `total_expenses` | Currency | Total Expenses | No | Period expenses |
| `net_income` | Currency | Net Income | No | Calculated net income |

### Review Notes

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `controller_notes` | Text Editor | Controller Notes | No | Controller comments |
| `executive_notes` | Text Editor | Executive Notes | No | Executive comments |
| `notes` | Text Editor | Notes | No | General notes |

### Permissions
- Read: Company Viewers, Accountants
- Write: Accountants, Controllers
- Create: System (auto-created)
- Delete: System Administrators

---

## 9. Project DocType

**DocType Name:** `Accounting Project`
**Module:** `Company Management`
**Naming:** Auto-generated (PROJ-YYYY-XXXXX)

### Core Fields

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `project_name` | Data | Project Name | Yes | Name of project |
| `company` | Link | Company | Yes | Link to Company |
| `project_type` | Select | Project Type | Yes | Accounting, Compliance, Audit, Implementation |
| `description` | Text Editor | Description | No | Project description |

### Timeline

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `start_date` | Date | Start Date | Yes | Project start date |
| `target_end_date` | Date | Target End Date | No | Planned completion date |
| `actual_end_date` | Date | Actual End Date | No | Actual completion date |

### Assignment

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `project_manager` | Link | Project Manager | Yes | Link to User |
| `assigned_team` | Table | Assigned Team | No | Child table of team members |

### Team Members (Child Table)

**Child DocType Name:** `Project Team Member`

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `team_member` | Link | Team Member | Yes | Link to User |
| `role` | Data | Role | No | Role on project |
| `allocation_percentage` | Percent | Allocation % | No | Time allocation |

### Progress Tracking

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `status` | Select | Status | Yes | Planning, In Progress, On Hold, Completed, Cancelled |
| `priority` | Select | Priority | Yes | Low, Medium, High, Urgent |
| `completion_percentage` | Percent | Completion % | No | Manual or calculated progress |

### Milestones (Child Table)

**Child DocType Name:** `Project Milestone`

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `milestone_name` | Data | Milestone | Yes | Milestone name |
| `target_date` | Date | Target Date | Yes | Target completion date |
| `actual_date` | Date | Actual Date | No | Actual completion date |
| `is_completed` | Check | Completed | No | Milestone completed |

### Additional Information

| Field Name | Type | Label | Required | Description |
|------------|------|-------|----------|-------------|
| `notes` | Text Editor | Notes | No | Internal notes |

### Permissions
- Read: Company Viewers, Accountants
- Write: Project Manager, Accountants
- Create: Company Administrators
- Delete: System Administrators

---

## Entity Relationship Diagram

```
Company (1) ─────────< (*) Company Bank
Company (1) ─────────< (*) Company Tax Entity
Company (1) ─────────< (*) Company Insurance
Company (1) ─────────< (*) Company Loan
Company (1) ─────────< (*) Company Key Employee
Company (1) ─────────< (*) Review Period
Company (1) ─────────< (*) Accounting Project

Task Type (1) ────────< (*) Task (generated instances)
Review Period (1) ────< (*) Task

Task Type (1) ────────< (1) Task Type (depends_on_task)

Company (1) ──────────> (1) Company Group
Company (*) ──────────> (1) Department
```

---

## Validation Rules

### Company DocType
- `company_code` must be unique
- `ein` must be unique if provided
- At least one address must be marked as primary
- `fiscal_year_start` must be 1-12

### All Relationship DocTypes
- Must have active company
- Cannot create relationships for inactive companies

### Bank Relationship
- `account_number` must be encrypted
- `routing_number` must be 9 digits if provided
- `account_type` required

### Tax Entity
- `tax_type` required
- `filing_frequency` required
- `next_filing_date` auto-calculated based on frequency

### Insurance
- `expiration_date` must be after `effective_date`
- Alert when expiration is within 60 days
- Auto-calculate `renewal_date`

### Loan
- `current_balance` cannot exceed `original_amount`
- `interest_rate` must be between 0 and 100
- `maturity_date` must be after `origination_date`
- Auto-calculate `next_payment_date` based on frequency

### Task Type
- If `is_recurring` = true, `recurrence_pattern` required
- `due_offset_days` must be positive

### Review Period
- `end_date` must be after `start_date`
- Cannot have overlapping periods for same company
- Auto-generate naming: `{company_code}-{YYYYMM}`
- Status workflow must follow sequence

### Project
- `target_end_date` must be after `start_date`
- At least one team member required
- Project manager must be assigned

---

## Auto-Generation Rules

### Naming Patterns
- **Company:** Prompt (user enters name)
- **Company Bank:** `BANK-{YYYY}-{#####}`
- **Company Tax Entity:** `TAX-{YYYY}-{#####}`
- **Company Insurance:** `INS-{YYYY}-{#####}`
- **Company Loan:** `LOAN-{YYYY}-{#####}`
- **Company Key Employee:** `EMP-{YYYY}-{#####}`
- **Task Type:** Prompt
- **Review Period:** `{company_code}-{YYYYMM}`
- **Accounting Project:** `PROJ-{YYYY}-{#####}`

### Auto-Calculated Fields
- **Review Period:**
  - `total_tasks` = Count of linked tasks
  - `completed_tasks` = Count of completed tasks
  - `completion_percentage` = (completed / total) * 100

- **Accounting Project:**
  - `completion_percentage` = Average of milestone completion

---

## Implementation Notes

### Phase 1: Core DocTypes
1. Enhanced Company DocType
2. All 5 Relationship DocTypes (Bank, Tax, Insurance, Loan, Employee)

### Phase 2: Task & Review System
3. Task Type DocType
4. Review Period DocType

### Phase 3: Project Tracking
5. Accounting Project DocType

### Migration Considerations
- Existing Company DocType will be enhanced (not replaced)
- Add new fields via migration script
- Preserve existing data

### Security Considerations
- Encrypted fields:
  - Bank account numbers
  - Bank login credentials
  - Tax portal credentials
- Field-level permissions for sensitive data
- Audit trail for all changes

---

## Next Steps

After this data model is approved:
1. Create Design-002: API Endpoint Design
2. Implement DocTypes in Frappe (Feature-001 through Feature-008)
3. Create seed data for testing
4. Build API endpoints

---

**Status:** ✅ Complete - Ready for Review
**Blocked Issues:** Feature-001 through Feature-008
**Next Issue:** Design-002 (API Endpoint Design)
