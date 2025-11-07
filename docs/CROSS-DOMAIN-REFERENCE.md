# Cross-Domain Reference Guide

**Quick reference for cross-domain integration and interoperability**

**Purpose**: Help developers understand how domains interact and what to consider when working on a specific domain.

**Last Updated**: 2025  
**Version**: 1.0

---

## 🔗 Domain Interaction Map

### Departments → All Domains

**Departments is the foundation for everything.**

**Used By:**
- **Products**: Product-to-department allocations (many-to-many)
- **Inventory**: Department-based inventory tracking (2D model)
- **Permissions**: Department-based access control
- **Procurement**: Department-based ordering and invoicing
- **Recipes**: Recipe-to-department assignments
- **POS Integration**: Department-aware sales and depletions
- **Transfers**: Department-based transfers (from/to)
- **Depletions**: Department-based depletion tracking
- **Budgets**: Department-based budgets
- **Reporting**: Department-based report filtering

**Key Integration Points:**
- All DocTypes that need department filtering include `department` field
- All queries filter by user's accessible departments
- All reports support department filtering
- Permissions respect department assignments
- Inventory tracked per Product + Department

**Shared Pattern**:
```python
# Always include department in relevant DocTypes
department (Link: Department, required)

# Always filter by accessible departments
departments = get_user_accessible_departments(user)
filters['department'] = ['in', departments]
```

---

### Products → Multiple Domains

**Products are the foundation for inventory, procurement, and recipes.**

**Used By:**
- **Inventory**: Product + Department inventory tracking
- **Procurement**: Products ordered and received
- **Recipes**: Products used as ingredients
- **POS Integration**: Products sold (via recipes)
- **Transfers**: Products transferred
- **Depletions**: Products depleted
- **Reporting**: Product-based reports

**Key Integration Points:**
- Product unit conversion methods used everywhere
- Product primary count unit used for all inventory
- Product purchase units used in procurement
- Product departments used for filtering
- Product properties affect behavior (generic, non-inventory, prep item)

**Shared Methods** (Used by All Domains):
```python
# Product conversion methods (CRITICAL - use these, don't create your own)
product.convert_to_primary_unit(from_unit, quantity)
product.convert_from_primary_unit(to_unit, quantity)
product.convert_between_units(from_unit, to_unit, quantity)

# Product department methods
product.get_departments()
product.assign_to_department(department)
```

**Impact on Development:**
- ✅ DO: Use Product's conversion methods
- ✅ DO: Store all quantities in product's primary count unit
- ✅ DO: Use Product's department methods
- ❌ DO NOT: Create custom conversion methods
- ❌ DO NOT: Store converted quantities
- ❌ DO NOT: Duplicate product department logic

---

### Inventory → Transfers, Depletions, POS

**Inventory depends on Products and Departments.**

**Used By:**
- **Transfers**: Inventory moved between departments/stores
- **Depletions**: Inventory consumed/wasted
- **POS Integration**: Inventory depleted from sales
- **Theoretical Inventory**: Calculates expected inventory
- **Audits**: Physical inventory counts
- **Reporting**: Inventory reports

**Key Integration Points:**
- 2D model (Product + Department) used everywhere
- Storage is metadata only (not in calculations)
- All quantities in primary count unit
- Theoretical inventory includes all transactions
- Inventory balance updated by all transactions

**Shared Functions** (Used by Multiple Domains):
```python
# Theoretical inventory calculation (used by audits, reports, transfers)
calculate_theoretical_inventory(product, company, department, as_on_date)

# Inventory balance (used by all inventory operations)
get_inventory_balance(product, department, company)
update_inventory_balance(product, department, company, quantity_change)
```

**Impact on Development:**
- ✅ DO: Use Product + Department for all inventory operations
- ✅ DO: Use primary count units
- ✅ DO: Update inventory balance on transactions
- ✅ DO: Include storage as metadata (not in calculations)
- ❌ DO NOT: Create storage-based inventory
- ❌ DO NOT: Mix departments in calculations
- ❌ DO NOT: Store converted quantities

---

### Recipes → POS Integration

**Recipes drive POS depletion calculations.**

**Used By:**
- **POS Integration**: Recipe ingredients used to calculate depletions
- **Inventory**: Batch production affects inventory
- **Costing**: Recipe costs calculated from ingredients
- **Reporting**: Recipe reports and analysis

**Key Integration Points:**
- Recipe-to-POS item mapping required
- Recipe ingredients determine POS depletions
- Recipe department assignment affects depletion department
- Recipe unit conversions used in depletion calculations
- Recipe costing uses product prices

**Shared Methods**:
```python
# Recipe costing (used by reports, POS)
recipe.calculate_cost()
recipe.get_cost_per_serving()

# Recipe depletions (used by POS)
recipe.calculate_ingredient_depletions(quantity_sold, department)
```

**Impact on Development:**
- ✅ DO: Use recipe ingredients for depletion calculations
- ✅ DO: Convert ingredient quantities to primary units
- ✅ DO: Use recipe department for depletion department
- ❌ DO NOT: Calculate depletions without recipes
- ❌ DO NOT: Ignore recipe unit conversions
- ❌ DO NOT: Mix recipe departments

---

### Procurement → Inventory, Accounting

**Procurement affects inventory and accounting.**

**Used By:**
- **Inventory**: Receipts increase inventory (department-allocated)
- **Accounting**: Bills synced to accounting systems
- **Theoretical Inventory**: Receipts included in calculations
- **Budgeting**: Purchase orders commit budgets, receipts spend budgets

**Key Integration Points:**
- Invoice receipts update inventory (department-allocated)
- Purchase units used for ordering
- GL codes assigned per product-department
- Ottimate integration imports receiving data
- Invoice line splitting across departments

**Impact on Development:**
- ✅ DO: Allocate invoice lines to departments
- ✅ DO: Convert purchase units to primary units
- ✅ DO: Update inventory on receipt
- ✅ DO: Assign GL codes per product-department
- ❌ DO NOT: Ignore department allocation
- ❌ DO NOT: Skip unit conversion
- ❌ DO NOT: Bypass inventory updates

---

## 📐 Shared Data Models

### Product + Department Pattern

**Used By**: Inventory, Procurement, Recipes, POS, Transfers, Depletions

**Pattern**:
```python
# Always include both Product and Department
product (Link: Product, required)
department (Link: Department, required)
company (Link: Company, required)  # For multi-tenancy

# Storage is optional metadata
storage_location (Link: Storage Area, optional)  # Metadata only
```

**Examples**:
- **Inventory Balance**: Product + Department (storage not included)
- **Theoretical Inventory**: Product + Department (storage not in calculation)
- **Invoice Line Allocation**: Product + Department (from invoice line split)
- **Transfer**: Product + Department (from/to departments)
- **Depletion**: Product + Department (depleted from department)
- **POS Depletion**: Product + Department (from recipe, via POS sale)

**Key Rule**: Storage location is metadata for organization, NOT part of inventory calculation.

---

### Unit Conversion Pattern

**Used By**: Products, Inventory, Recipes, POS, Procurement

**Pattern**:
```python
# Always use Product's conversion methods
product = frappe.get_doc('Product', product_name)

# Convert to primary unit for storage
quantity_in_primary = product.convert_to_primary_unit(from_unit, quantity)

# Store in primary unit
doc.quantity = quantity_in_primary

# Convert from primary unit for display
display_quantity = product.convert_from_primary_unit(to_unit, quantity_in_primary)

# Convert between units via primary
converted_quantity = product.convert_between_units(from_unit, to_unit, quantity)
```

**Key Rules**:
- Always store quantities in primary count unit
- Always use Product's conversion methods (don't create your own)
- Always convert on-the-fly for display/entry
- Never store converted quantities

**Examples**:
- **Audit Lines**: Count in any unit, store in primary unit
- **Invoice Lines**: Purchase unit → primary unit for inventory
- **Recipe Ingredients**: Any unit → primary unit for costing
- **POS Depletions**: Recipe units → primary units for inventory

---

### Department Filtering Pattern

**Used By**: All domains with department-based data

**Pattern**:
```python
# Get user's accessible departments
def get_user_accessible_departments(user):
    """Get departments user has access to"""
    departments = frappe.get_all(
        'Department Permission',
        filters={'parent': user, 'can_read': 1},
        fields=['department'],
        distinct=True
    )
    return [d.department for d in departments]

# Filter queries by accessible departments
departments = get_user_accessible_departments(frappe.session.user)
filters = {
    'department': ['in', departments],
    # ... other filters
}

# Check permissions before queries
if not has_department_permission(user, department, 'read'):
    frappe.throw(_("No access to department"))
```

**Key Rules**:
- Always filter by user's accessible departments
- Always check permissions before queries
- Always respect department boundaries
- Always support department filtering in reports

**Examples**:
- **Product Lists**: Filter by accessible departments
- **Inventory Reports**: Filter by accessible departments
- **Audit Lists**: Filter by accessible departments
- **Purchase Orders**: Filter by accessible departments

---

### Permission Checking Pattern

**Used By**: All domains

**Pattern**:
```python
# Use Frappe's permission system
if not frappe.has_permission('Product', doc=product_doc, user=user):
    frappe.throw(_("No permission to access product"))

# Check department permissions
if not has_department_permission(user, department, 'write'):
    frappe.throw(_("No write access to department"))

# Check role permissions
if not frappe.has_permission('Product', 'write', user=user):
    frappe.throw(_("No permission to edit products"))

# Combined check
if (frappe.has_permission('Product', 'write', user=user) and
    has_department_permission(user, department, 'write')):
    # Allow operation
    pass
```

**Key Rules**:
- Always use Frappe's built-in permission system
- Always check department permissions
- Always check role permissions
- More restrictive permission applies

---

## 🔄 Common Workflows

### Product Creation Workflow

```
1. Create Product (Products Domain)
   ├── Set primary count unit
   ├── Set volume/weight conversions
   ├── Set product properties
   └── Set default department

2. Assign to Departments (Products Domain)
   ├── Create Product Department records
   ├── Set par levels per department
   ├── Set order quantities per department
   └── Mark primary department

3. Add Purchase Units (Products Domain)
   ├── Create Purchase Unit records
   ├── Set conversion factors
   ├── Set prices
   └── Mark preferred purchase unit

4. Inventory Balance Created (Inventory Domain)
   ├── Auto-created when product assigned to department
   ├── Initial quantity: 0
   ├── Tracked per Product + Department
   └── Last audit date: null

5. Ready for Use
   ├── Can be ordered (Procurement)
   ├── Can be used in recipes (Recipes)
   ├── Can be counted in audits (Inventory)
   └── Can be sold via POS (POS Integration)
```

---

### Inventory Audit Workflow

```
1. Create Audit (Inventory Domain)
   ├── Define scope (departments, storages, categories)
   ├── Set audit date
   └── Set audit type (Full/Partial)

2. Create Counting Tasks (Inventory Domain)
   ├── Auto-generated from scope
   ├── Grouped by department + storage
   ├── Assigned to departments
   └── Categories assigned if partial

3. Count Products (Inventory Domain)
   ├── Users count in any available unit
   ├── Counts converted to primary unit
   ├── Stored as Audit Lines
   └── Linked to counting task

4. Calculate Variances (Inventory Domain)
   ├── Calculate theoretical inventory
   ├── Compare to actual counts
   ├── Flag high variances
   └── Generate variance report

5. Close Audit (Inventory Domain)
   ├── Update Inventory Balance
   ├── Set last_audit_date
   ├── Lock audit after X days
   └── Create inventory history snapshot
```

---

### POS Depletion Workflow

```
1. Import POS Sales (POS Integration)
   ├── Poll POS API or import file
   ├── Create POS Sale records
   ├── Map items to recipes
   └── Assign to departments

2. Calculate Depletions (POS Integration)
   ├── For each sale, get recipe
   ├── For each ingredient, calculate depletion
   ├── Convert to ingredient's primary unit
   └── Apply modifier adjustments

3. Create Depletion Records (Depletions Domain)
   ├── Create Depletion record
   ├── Create Depletion Lines
   ├── Set depletion type: "Sold"
   └── Link to POS Sale

4. Update Inventory (Inventory Domain)
   ├── Reduce inventory balance
   ├── Update theoretical inventory
   ├── Track depletion in history
   └── Update last transaction date
```

---

### Invoice Receipt Workflow

```
1. Import Invoice (Procurement Domain)
   ├── From Ottimate or manual entry
   ├── Create Vendor Invoice
   ├── Create Invoice Lines
   └── Map products

2. Allocate to Departments (Procurement Domain)
   ├── Assign invoice lines to departments
   ├── Split lines across departments if needed
   ├── Assign GL codes per product-department
   └── Convert purchase units to primary units

3. Approve Invoice (Procurement Domain)
   ├── Validate allocations
   ├── Check contract prices
   └── Mark as approved

4. Update Inventory (Inventory Domain)
   ├── Increase inventory balance
   ├── Update theoretical inventory
   ├── Track receipt in history
   └── Update last transaction date

5. Sync to Accounting (Accounting Domain)
   ├── Create Bill in accounting system
   ├── Map GL codes
   ├── Map payees
   └── Track sync status
```

---

## 🚨 Integration Checkpoints

### Before Implementing a Function

**Check:**

1. **Dependencies**
   - What other domains does this depend on?
   - What shared methods are available?
   - What data models are established?
   - What patterns should I follow?

2. **Shared Methods**
   - Are there shared methods I should use?
   - Should I create shared methods for others?
   - Are there utilities I can leverage?

3. **Data Models**
   - What data models are established?
   - Should I follow Product + Department pattern?
   - Should I use primary count units?
   - Should I include storage as metadata?

4. **Patterns**
   - What patterns should I follow?
   - Are there code examples I can reference?
   - Are there anti-patterns I should avoid?

5. **Permissions**
   - How should permissions work?
   - Should I check department permissions?
   - Should I check role permissions?

6. **Departments**
   - How should departments be handled?
   - Should I filter by departments?
   - Should I support department reporting?

---

### During Implementation

**Verify:**

1. **Unit Conversions**
   - Am I using Product's conversion methods?
   - Am I storing in primary count unit?
   - Am I converting on-the-fly for display?

2. **Department Filtering**
   - Am I filtering by departments?
   - Am I checking department permissions?
   - Am I supporting department reporting?

3. **Permissions**
   - Am I checking permissions?
   - Am I using Frappe's permission system?
   - Am I respecting department permissions?

4. **Data Consistency**
   - Am I following 2D inventory model?
   - Am I using Product + Department?
   - Am I storing in primary count unit?

5. **Storage**
   - Am I treating storage as metadata only?
   - Am I including storage in audit lines?
   - Am I NOT including storage in calculations?

6. **Quantities**
   - Am I storing in primary count unit?
   - Am I converting on-the-fly?
   - Am I using Product's conversion methods?

---

### After Implementation

**Verify:**

1. **Cross-Domain Impact**
   - Does this affect other domains?
   - Do other domains depend on this?
   - Are integration points working?

2. **Data Flow**
   - Does data flow correctly between domains?
   - Are shared methods being used?
   - Is data consistency maintained?

3. **Integration**
   - Does this integrate with dependent domains?
   - Are shared patterns followed?
   - Is interoperability maintained?

4. **Consistency**
   - Is this consistent with other domains?
   - Are patterns followed?
   - Is code style consistent?

5. **Performance**
   - Does this perform well?
   - Are queries optimized?
   - Are conversions efficient?

---

## 📋 Domain-Specific Integration Points

### Working on Products Domain

**Consider Impact On:**
- **Inventory**: Inventory balance creation, theoretical inventory
- **Procurement**: Purchase units for ordering, invoice line allocation
- **Recipes**: Products as ingredients, unit conversions
- **POS**: Products sold via recipes, depletion calculations
- **Transfers**: Products transferred, unit conversions
- **Depletions**: Products depleted, unit conversions
- **Reporting**: Product-based reports, filtering

**Key Integration:**
- Unit conversion methods (used by ALL domains)
- Department assignments (used by ALL domains)
- Purchase units (used by procurement)
- Product properties (affect behavior across domains)

**Shared Methods You Provide:**
```python
# These methods are used by ALL domains - make them robust
product.convert_to_primary_unit(from_unit, quantity)
product.convert_from_primary_unit(to_unit, quantity)
product.convert_between_units(from_unit, to_unit, quantity)
product.get_departments()
product.get_purchase_units(vendor=None)
```

---

### Working on Inventory Domain

**Consider Impact On:**
- **Products**: Inventory balance per product-department
- **Transfers**: Inventory moved, balance updated
- **Depletions**: Inventory consumed, balance updated
- **POS**: Inventory depleted, balance updated
- **Procurement**: Inventory received, balance updated
- **Reporting**: Inventory reports, theoretical inventory

**Key Integration:**
- 2D model (Product + Department) - CRITICAL
- Theoretical inventory calculation (used by audits, reports)
- Storage metadata handling (not in calculations)
- Inventory balance updates (from all transactions)

**Shared Functions You Provide:**
```python
# These functions are used by multiple domains
calculate_theoretical_inventory(product, company, department, as_on_date)
get_inventory_balance(product, department, company)
update_inventory_balance(product, department, company, quantity_change)
```

---

### Working on POS Integration Domain

**Consider Impact On:**
- **Recipes**: Recipe ingredients for depletion calculations
- **Inventory**: Inventory depleted from sales
- **Products**: Product usage via recipes
- **Departments**: Department-aware depletions

**Key Integration:**
- Recipe-to-POS mapping (required)
- Recipe ingredient depletions (calculated)
- Department-aware depletions (from recipe/mapping)
- Unit conversions (recipe units → primary units)

**Dependencies You Use:**
```python
# You depend on Recipes for depletion calculations
recipe.get_ingredients()
recipe.calculate_ingredient_depletions(quantity_sold)

# You depend on Products for unit conversions
product.convert_to_primary_unit(unit, quantity)

# You depend on Inventory for updates
update_inventory_balance(product, department, company, -depletion_qty)
```

---

### Working on Procurement Domain

**Consider Impact On:**
- **Products**: Purchase units, vendor mappings
- **Inventory**: Receipts update inventory
- **Accounting**: Bills synced to accounting systems
- **Budgets**: Orders commit budgets, receipts spend budgets

**Key Integration:**
- Invoice line department allocation
- Purchase unit to primary unit conversion
- Inventory balance updates on receipt
- GL code assignment per product-department

**Dependencies You Use:**
```python
# You depend on Products for purchase units
product.get_purchase_units(vendor)
purchase_unit.convert_to_primary_unit(quantity)

# You depend on Inventory for updates
update_inventory_balance(product, department, company, receipt_qty)

# You depend on Accounting for GL codes
get_gl_code(product, department)
```

---

## 🎯 Interoperability Checklist

### For Each Function You Implement

**Verify:**

- [ ] Uses established data models (Product + Department)
- [ ] Uses shared methods (unit conversion, permissions)
- [ ] Supports department filtering
- [ ] Respects department permissions
- [ ] Uses primary count units
- [ ] Follows 2D inventory model (if applicable)
- [ ] Integrates with dependent domains
- [ ] Doesn't duplicate existing functionality
- [ ] Follows established patterns
- [ ] Maintains data consistency
- [ ] Handles errors gracefully
- [ ] Includes validation rules
- [ ] Performs well
- [ ] Is maintainable

---

## 🔍 Quick Reference

### Product + Department Pattern
```python
# Always include both
product (Link: Product, required)
department (Link: Department, required)
# Storage is metadata only
storage_location (Link: Storage Area, optional)
```

### Unit Conversion Pattern
```python
# Always use Product's methods
product.convert_to_primary_unit(from_unit, quantity)
# Always store in primary unit
doc.quantity = quantity_in_primary
```

### Department Filtering Pattern
```python
# Always filter by accessible departments
departments = get_user_accessible_departments(user)
filters['department'] = ['in', departments]
```

### Permission Checking Pattern
```python
# Always check permissions
frappe.has_permission('Product', doc=product_doc, user=user)
has_department_permission(user, department, 'read')
```

---

**Use this guide to ensure your implementation integrates seamlessly with other domains. When in doubt, refer to PROJECT-CONTEXT.md for architecture principles and AGENT-INSTRUCTIONS.md for development guidelines.**


