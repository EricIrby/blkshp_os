# Depletion Types

## Overview

Depletion Types categorize different reasons for inventory consumption. Each type has specific use cases and accounting treatment.

## Purpose

- Categorize depletion reasons
- Support different accounting treatments
- Enable reporting and analysis
- Track depletion patterns
- Support cost allocation

## Depletion Type Categories

### Sold (POS)
- Automatic depletion from POS sales
- Calculated from recipe usage
- Primary depletion type
- Source: POS Sale

### Spilled
- Physical spillage or breakage
- Accidental loss
- Recorded when discovered
- Source: Manual Entry

### Wasted
- Spoiled, expired, or unusable inventory
- Quality issues
- Recorded when discovered
- Source: Manual Entry

### Manual
- Manual consumption for other reasons
- General use
- Various purposes
- Source: Manual Entry

### Theft/Loss
- Theft or unexplained loss
- Security issues
- Requires investigation
- Source: Manual Entry

### Comp/Complimentary
- Given away for free
- Promotional items
- Customer service
- Source: Manual Entry

## Accounting Treatment

### GL Code Assignment
- Each depletion type can have default GL code
- Can be overridden per depletion line
- Supports cost allocation

### Cost Impact
- All depletion types reduce inventory
- Affect COGS calculations
- Impact variance analysis

## Implementation Steps

### Step 1: Define Depletion Types
1. Create depletion type options
2. Define default GL codes per type
3. Set up accounting treatment

### Step 2: Implement Type Selection
1. Add depletion_type field to Depletion DocType
2. Auto-assign GL codes based on type
3. Support type-specific workflows

### Step 3: Add Reporting
1. Report depletions by type
2. Analyze depletion patterns
3. Track type-specific costs

## Dependencies

- **Depletion DocType**: Depletion records
- **Account DocType**: GL code mapping

## Usage Examples

### Waste Analysis
```
Waste Depletions Report:
  - Department: Kitchen
  - Period: January 2025
  - Total Waste: $450.00
  - Top Items: Lettuce, Tomatoes, Dairy
```

### Spillage Tracking
```
Spillage Depletions:
  - Department: Bar
  - Period: January 2025
  - Total Spillage: $125.00
  - Items: Wine, Spirits, Beer
```

## Testing Checklist

- [ ] Create depletion with each type
- [ ] Verify GL code assignment
- [ ] Test type-specific workflows
- [ ] Generate type-specific reports
- [ ] Analyze depletion patterns

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 17

