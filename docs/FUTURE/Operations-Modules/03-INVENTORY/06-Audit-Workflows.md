# Audit Workflows

## Overview

Audit Workflows define the lifecycle of inventory audits from setup through locking. The workflow ensures proper audit management, data integrity, and operational flexibility.

## Purpose

- Define audit lifecycle stages
- Control audit state transitions
- Ensure data integrity
- Support audit corrections
- Enable audit locking for historical records

## Workflow States

### Setup
- Audit created
- Scope defined (departments, storages, categories)
- Counting tasks not yet created
- Can be modified freely

### Ready
- Counting tasks created
- Tasks assigned to departments/users
- Ready for counting to begin
- Can still modify scope before starting

### In Progress
- Counting has begun
- Users are entering counts
- Some tasks may be complete
- Can add/modify counts
- Cannot close until all tasks complete

### Review
- All counting complete
- Reviewing counts for accuracy
- Making corrections if needed
- Flagging items for recount
- Preparing to close

### Closed
- Audit finalized
- Variances calculated
- Inventory balances updated
- Period closed
- Can be reopened for corrections (with authorization)

### Locked
- Audit locked (after X days from closing)
- Cannot be modified
- Used for historical reporting
- Can be opened with authorization workflow
- Director-level configuration for lock period

## State Transitions

### Normal Flow
```
Setup → Ready → In Progress → Review → Closed → Locked
```

### Correction Flow
```
Closed → (Reopen) → Review → Closed
Locked → (Open with Authorization) → Review → Closed → Locked
```

## Implementation Steps

### Step 1: Create Workflow
1. Create workflow in Frappe
2. Define states (Setup, Ready, In Progress, Review, Closed, Locked)
3. Define transitions between states
4. Set permissions per state

### Step 2: Implement State Validations
1. Validate state transitions
2. Check prerequisites for transitions
3. Block invalid transitions
4. Show appropriate error messages

### Step 3: Implement State Actions
1. Auto-create tasks on Ready transition
2. Calculate totals on Review transition
3. Update balances on Closed transition
4. Lock audit on Locked transition

### Step 4: Add Authorization
1. Require authorization for reopening closed audits
2. Require authorization for opening locked audits
3. Track authorization in audit record
4. Log all state changes

## Dependencies

- **Inventory Audit DocType**: Audit records
- **Counting Task DocType**: Task assignments
- **Frappe Workflow Engine**: Workflow management

## Usage Examples

### Normal Audit Flow
```
1. Create audit (Setup)
2. Define scope
3. Create tasks (Ready)
4. Start counting (In Progress)
5. Complete all tasks (Review)
6. Review and correct counts
7. Close audit (Closed)
8. Lock after X days (Locked)
```

### Audit Correction
```
1. Audit is Closed
2. Request to reopen (authorization required)
3. Make corrections (Review)
4. Close audit again (Closed)
```

## Testing Checklist

- [ ] Create audit (Setup state)
- [ ] Transition to Ready
- [ ] Transition to In Progress
- [ ] Transition to Review
- [ ] Transition to Closed
- [ ] Transition to Locked
- [ ] Reopen closed audit
- [ ] Open locked audit (with authorization)
- [ ] Verify state validations
- [ ] Verify permissions per state

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 5.1

