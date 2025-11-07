# Audit Enhancements

## Overview

Audit Enhancements provide advanced workflow management for inventory audits, including recount flags, unsaved count recovery, audit corrections, reopening capabilities, and locking configuration.

## Purpose

- Flag items for recount during or after counting
- Recover unsaved counts (browser crash, network issues)
- Delete audits with proper authorization
- Reopen closed audits for corrections
- Open locked audits with authorization workflow
- Update closed audits with change tracking
- Correct previous audits with audit trail
- Update item CU prices on closed audits
- Configure audit locking periods (Director-level)

## Key Features

### Flagging Items for Recount
- Flag items during counting for uncertainty/discrepancies
- Record recount reason
- Track who flagged and when
- Record recount value
- Approve/reject recounts

### Unsaved Count Recovery
- Track counts entered but not saved
- Recover counts after browser crash/network issues
- Prevent data loss
- Show unsaved counts to users

### Audit Deletion
- Delete audits with proper authorization
- Require admin/account owner permission
- Log deletion for audit trail
- Prevent deletion of closed/locked audits

### Reopening Closed Audits
- Reopen closed audits for corrections
- Require authorization
- Track reopening in audit trail
- Allow corrections while maintaining history

### Opening Locked Audits
- Open locked audits with authorization workflow
- Director-level authorization
- Track opening in audit trail
- Allow corrections to historical audits

### Updating Closed Audits
- Update closed audit counts
- Track all changes in audit trail
- Require authorization for updates
- Maintain data integrity

### Correcting Previous Audits
- Correct errors in previous audits
- Create audit trail of corrections
- Update inventory balances retroactively
- Maintain historical accuracy

### Updating CU Prices
- Update item CU prices on closed audits
- Recalculate audit values
- Track price changes
- Maintain audit integrity

### Audit Locking Configuration
- Director-level configuration
- Set days to lock audits after closing
- Automatic locking after period
- Authorization required to open locked audits

## Implementation Steps

### Step 1: Add Recount Fields to Audit Line
1. Add needs_recount checkbox
2. Add recount_reason field
3. Add recount_count fields
4. Add final_count fields

### Step 2: Create Unsaved Count DocType
1. Create `Unsaved Count` DocType
2. Add recovery fields
3. Implement recovery methods

### Step 3: Implement Audit Deletion
1. Add deletion authorization check
2. Log deletion in audit trail
3. Prevent deletion of closed/locked audits

### Step 4: Implement Reopening
1. Add reopen authorization check
2. Track reopening in audit trail
3. Allow corrections

### Step 5: Implement Locking
1. Add locking configuration (Director-level)
2. Implement automatic locking
3. Add authorization for opening locked audits

## Dependencies

- **Inventory Audit DocType**: Audit records
- **Audit Line DocType**: Count entries
- **Director Configuration**: Locking configuration

## Usage Examples

### Flag Item for Recount
```
1. User flags item during counting
2. Enter recount reason
3. Supervisor recounts item
4. Approve/reject recount
5. Set final count
```

### Recover Unsaved Count
```
1. User enters count but doesn't save
2. Browser crashes
3. System saves unsaved count
4. User returns and recovers count
5. Count added to audit
```

### Reopen Closed Audit
```
1. Audit is closed
2. Request to reopen (authorization required)
3. Make corrections
4. Close audit again
```

## Testing Checklist

- [ ] Flag items for recount
- [ ] Record recount values
- [ ] Approve/reject recounts
- [ ] Recover unsaved counts
- [ ] Delete audits (with authorization)
- [ ] Reopen closed audits
- [ ] Open locked audits (with authorization)
- [ ] Update closed audits
- [ ] Correct previous audits
- [ ] Update CU prices on closed audits
- [ ] Configure audit locking periods

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 24

