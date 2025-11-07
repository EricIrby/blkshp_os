# Fuzzy Matching

## Overview

Fuzzy Matching uses string similarity algorithms (FuzzyWuzzy) to match invoice line items to products when exact matches are not found. Helps automate product matching during invoice processing.

## Purpose

- Match invoice items to products automatically
- Handle product name variations
- Reduce manual matching work
- Improve invoice processing efficiency
- Support automated product mapping

## FuzzyWuzzy Library

### Library Details
- **Library**: `fuzzywuzzy` or `rapidfuzz`
- **License**: GPL v2 (fuzzywuzzy) or MIT (rapidfuzz)
- **Features**: String similarity matching, ratio calculation
- **Integration**: Python method in Frappe

## Implementation

### Fuzzy Matching Function

```python
from fuzzywuzzy import fuzz, process

def match_invoice_item_to_product(invoice_item_name, products):
    """Match invoice item to product using fuzzy matching"""
    
    # Get best match
    best_match = process.extractOne(
        invoice_item_name,
        products,
        scorer=fuzz.token_sort_ratio
    )
    
    # Check if match score is above threshold (e.g., 80%)
    if best_match[1] >= 80:
        return best_match[0]  # Return matched product
    else:
        return None  # No good match found
```

## Matching Strategies

### Token Sort Ratio
- Compares strings after sorting tokens
- Good for word order variations
- Example: "Coca Cola Cans" matches "Cans Coca Cola"

### Token Set Ratio
- Compares token sets
- Ignores duplicates
- Good for abbreviations

### Partial Ratio
- Finds best matching substring
- Good for partial matches
- Example: "Coca Cola" matches "Coca Cola Cans 12oz"

## Implementation Steps

### Step 1: Install Fuzzy Matching Library
1. Install fuzzywuzzy or rapidfuzz
2. Install python-Levenshtein (for performance)
3. Import libraries in Frappe

### Step 2: Implement Matching Function
1. Create match_invoice_item_to_product function
2. Use fuzzy matching algorithms
3. Set similarity threshold
4. Return best match

### Step 3: Integrate with Invoice Processing
1. Use fuzzy matching during invoice import
2. Suggest matches for unmapped items
3. Allow manual override
4. Track matching accuracy

## Dependencies

- **FuzzyWuzzy/RapidFuzz Library**: String matching
- **Product DocType**: Product database
- **Vendor Invoice DocType**: Invoice processing

## Usage Examples

### Match Invoice Item
```
Invoice Item: "Coca-Cola 12oz Cans"
Products: ["Coca Cola Cans", "Pepsi Cans", ...]
Match Score: 95%
Matched Product: "Coca Cola Cans"
```

## Testing Checklist

- [ ] Match invoice items to products
- [ ] Handle name variations
- [ ] Set appropriate thresholds
- [ ] Test different matching strategies
- [ ] Handle unmapped items
- [ ] Track matching accuracy

---

**Status**: ✅ Extracted from FRAPPE_IMPLEMENTATION_PLAN.md Section 6.2

