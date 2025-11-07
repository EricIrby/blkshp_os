# BLKSHP Product Platform - Project-Wide Context

**This document provides essential project-wide context for all domain-specific development work.**

**Last Updated**: 2025  
**Version**: 1.0

---

## 🎯 Project Overview

**BLKSHP Product Platform** is a unified inventory management and cost control platform built on Frappe Framework. Unlike Craftable's multi-platform approach (Foodager/Bevager/House), BLKSHP uses a single unified platform with **department-based segmentation** for flexible product management, allocations, transfers, and permissions.

**Key Differentiator**: Single unified system instead of separate platforms, using departments to organize and segment functionality.

---

## 🏗️ Core Architecture Principles

### 1. Unified Platform (Not Separate Platforms)

**Key Principle**: All products (food, beverage, supplies, equipment) managed in one unified system.

- **Single Product Master**: One `Product` DocType for all product types
- **Department Segmentation**: Products assigned to departments (many-to-many)
- **No Platform Separation**: Unlike Craftable's Foodager/Bevager/House approach
- **Product Type Field**: Use `product_type` field (Food, Beverage, Supply, Equipment) to distinguish, but same DocType

**Impact on Development**:
- ✅ DO: Create one `Product` DocType for all product types
- ✅ DO: Use `product_type` field to distinguish types
- ✅ DO: Use departments to organize products
- ❌ DO NOT: Create separate DocTypes for food vs beverage vs supplies
- ❌ DO NOT: Create separate inventory systems per product type
- ❌ DO NOT: Build functionality that only works for one product type

---

### 2. Department-Based Architecture

**Key Principle**: Departments enable flexible organization without separate platforms.

**Department Structure**:
```
Company (Store)
├── Food & Beverage (Department)
├── Beverage (Department)
├── Supplies (Department)
└── Kitchen (Department)
```

**How Departments Work**:
- Products can belong to **multiple departments** (many-to-many)
- Users have access to **specific departments** (permission-based)
- Inventory tracked per **Product + Department** (2D model)
- Reports **filterable by department**
- Permissions are **department-based**

**Impact on Development**:
- ✅ DO: Always include `department` field in relevant DocTypes
- ✅ DO: Support department filtering in all queries
- ✅ DO: Respect department permissions
- ✅ DO: Enable department-based reporting
- ❌ DO NOT: Create functionality that ignores departments
- ❌ DO NOT: Build reports that don't filter by department
- ❌ DO NOT: Bypass department permissions

---

### 3. 2D Inventory Model (Product + Department)

**Key Principle**: Inventory tracked by Product + Department combination, NOT by storage location.

**Inventory Model**:
- **Product**: The item (e.g., "Coca Cola Cans")
- **Department**: Where it's used (e.g., "Beverage")
- **Storage Location**: Metadata only (where it's stored, but doesn't create separate inventory)

**Formula**:
```
Inventory Balance = Product + Department
Storage = Metadata (helps organize counting, but not part of inventory calculation)
```

**Critical Understanding**:
- Storage areas help organize where products are stored
- Storage areas help organize counting tasks
- Storage areas appear in audit lines
- Storage areas do NOT create separate inventory buckets
- All inventory calculations use Product + Department only

**Impact on Development**:
- ✅ DO: Track inventory by Product + Department only
- ✅ DO: Include storage as metadata in audit lines
- ✅ DO: Use storage to organize counting tasks
- ❌ DO NOT: Create separate inventory balances per storage location
- ❌ DO NOT: Include storage in theoretical inventory calculations
- ❌ DO NOT: Calculate inventory per storage location

---

### 4. Hub-and-Spoke Unit Conversion

**Key Principle**: All unit conversions flow through the product's primary count unit (hub).

**Conversion Flow**:
```
Any Unit → Primary Unit (Hub) → Any Other Unit
```

**Example**:
- Product: "Coca Cola Cans"
- Primary Unit: "each" (1 can)
- Purchase Unit: "case" = 24 each
- Volume: "gallon" = 128 fl_oz = 10.67 each (via 12 fl_oz per can)

**Storage Rule**: All counts stored in primary count unit, conversions done on-the-fly for display/entry.

**Impact on Development**:
- ✅ DO: Always store quantities in primary count unit
- ✅ DO: Convert at display/entry time using Product's methods
- ✅ DO: Use Product's `convert_to_primary_unit()` and `convert_from_primary_unit()` methods
- ❌ DO NOT: Store converted quantities (always recalculate)
- ❌ DO NOT: Create custom conversion methods (use Product's methods)
- ❌ DO NOT: Hard-code conversion factors

---

### 5. Theoretical Inventory Calculation

**Key Principle**: Theoretical inventory calculated from last audit plus all transactions.

**Formula**:
```
Theoretical Inventory = 
    Starting Inventory (from last audit)
    + Received (from invoices, allocated to department)
    + Transferred In (to department)
    - Transferred Out (from department)
    - Depleted (sold, spilled, manual, in department)
```

**Key Points**:
- Calculated per **Product + Department** (2D model)
- Storage location is **NOT included** in calculation
- All quantities in **primary count unit**
- Includes batch production if applicable
- Department-aware (all transactions are department-specific)

**Impact on Development**:
- ✅ DO: Calculate theoretical per Product + Department
- ✅ DO: Include all transaction types (receipts, transfers, depletions)
- ✅ DO: Use primary count units
- ✅ DO: Include batch production
- ❌ DO NOT: Include storage location in calculation
- ❌ DO NOT: Mix departments in calculations
- ❌ DO NOT: Store calculated theoretical (recalculate on demand)

---

## 🔗 Cross-Domain Dependencies

### Dependency Chain

```
Departments (Foundation - No Dependencies)
    ├── Products (requires Departments)
    │   ├── Inventory (requires Products, Departments)
    │   ├── Procurement (requires Products, Departments)
    │   └── Recipes (requires Products, Departments)
    ├── Permissions (requires Departments)
    └── Everything Else (requires Departments)

Products (Foundation for Many)
    ├── Inventory (tracks Products)
    ├── Procurement (orders Products)
    ├── Recipes (uses Products as ingredients)
    └── POS Integration (sells Products via Recipes)

Inventory (Core Functionality)
    ├── Transfers (moves Inventory)
    ├── Depletions (consumes Inventory)
    └── POS Integration (depletes Inventory)

Recipes (Drives POS Depletions)
    └── POS Integration (calculates depletions from Recipes)
```

### Critical Dependencies

**Departments → Everything**
- All domains depend on Departments
- Department assignments required for products, inventory, permissions
- Do NOT create functionality that bypasses departments
- Always include department in data models

**Products → Inventory, Procurement, Recipes**
- Products are the foundation for inventory tracking
- Products required for procurement (ordering)
- Products used as recipe ingredients
- Product unit conversion methods used everywhere

**Recipes → POS Integration**
- POS depletions calculated from recipe ingredients
- Recipe-to-POS item mapping required
- Department-aware recipe usage
- Recipe unit conversions used in depletion calculations

---

## 🚫 Anti-Patterns to Avoid

### ❌ DO NOT Create Separate Platforms

**Wrong Approach**:
- Creating separate "Food Items" and "Beverage Items" DocTypes
- Creating separate inventory systems per product type
- Separating functionality by product type
- Building product-type-specific features

**Right Approach**:
- Single `Product` DocType for all types
- Use `product_type` field to distinguish
- Use departments to organize
- All functionality works across all product types

---

### ❌ DO NOT Create Storage-Based Inventory

**Wrong Approach**:
- Tracking inventory per storage location
- Creating separate inventory balances per storage
- Including storage in theoretical inventory calculations
- Calculating inventory per storage area

**Right Approach**:
- Inventory tracked by Product + Department only
- Storage is metadata for organization
- Storage helps with counting tasks but not calculations
- Storage appears in audit lines but doesn't affect inventory math

---

### ❌ DO NOT Store Converted Quantities

**Wrong Approach**:
- Storing both "each" and "gallon" quantities
- Duplicating quantities in different units
- Hard-coding unit conversions
- Creating custom conversion tables

**Right Approach**:
- Store all quantities in primary count unit
- Convert on-the-fly for display/entry
- Use Product's conversion methods
- Recalculate conversions as needed

---

### ❌ DO NOT Bypass Departments

**Wrong Approach**:
- Creating functionality that ignores departments
- Building reports that don't filter by department
- Ignoring department permissions
- Creating department-agnostic features

**Right Approach**:
- Always include department in data models
- Support department filtering in all queries
- Respect department permissions
- Enable department-based reporting

---

### ❌ DO NOT Duplicate Functionality

**Wrong Approach**:
- Creating separate conversion methods in each domain
- Duplicating permission checking logic
- Recreating department filtering in each module
- Building domain-specific utilities that already exist

**Right Approach**:
- Use shared Product conversion methods
- Use Frappe's built-in permission system
- Create reusable department filtering utilities
- Leverage shared functions and modules

---

## ✅ Patterns to Follow

### ✅ Use Frappe Framework Features

**Leverage Built-ins**:
- Use Frappe's DocType system (don't create raw SQL tables)
- Use Frappe's permission system (don't create custom permission logic)
- Use Frappe's workflow engine (don't reinvent state machines)
- Use Frappe's API framework (don't create custom REST APIs)
- Use Frappe's print formats (don't create custom PDF generators)
- Use Frappe's email integration (don't create custom email systems)

**Why**: Faster development, better maintainability, consistency across the platform.

---

### ✅ Follow Department Pattern

**Always Include**:
- Department field in relevant DocTypes
- Department filtering in queries
- Department permissions checks
- Department-based reporting
- Department-aware calculations

**Example Pattern**:
```python
# Always include department
filters = {
    'department': ['in', user_accessible_departments],
    # ... other filters
}
```

---

### ✅ Use Shared Methods

**Create Reusable Utilities**:
- Product unit conversion methods (in Product DocType)
- Department filtering utilities (shared module)
- Permission checking helpers (shared module)
- Theoretical inventory calculation (shared function)

**Example**:
```python
# Use Product's conversion method (don't create your own)
product = frappe.get_doc('Product', product_name)
quantity_in_primary = product.convert_to_primary_unit(from_unit, quantity)
```

---

### ✅ Maintain Data Consistency

**Ensure Consistency**:
- All quantities in primary count unit
- All inventory calculations use Product + Department
- All permissions respect departments
- All reports support department filtering
- All unit conversions use Product's methods

---

## 📐 Standard Patterns

### Department Filtering Pattern

```python
# Always filter by user's accessible departments
def get_accessible_departments(user):
    """Get departments user has access to"""
    departments = frappe.get_all(
        'Department Permission',
        filters={'parent': user, 'can_read': 1},
        fields=['department'],
        distinct=True
    )
    return [d.department for d in departments]

# Apply department filter to queries
departments = get_accessible_departments(frappe.session.user)
filters['department'] = ['in', departments]
```

---

### Unit Conversion Pattern

```python
# Always use Product's conversion methods
product = frappe.get_doc('Product', product_name)

# Convert to primary unit for storage
quantity_in_primary = product.convert_to_primary_unit(from_unit, quantity)

# Store in primary unit
doc.quantity = quantity_in_primary

# Convert from primary unit for display
display_quantity = product.convert_from_primary_unit(to_unit, quantity_in_primary)
```

---

### Permission Checking Pattern

```python
# Check department permissions
if not has_department_permission(user, department, 'read'):
    frappe.throw(_("No access to department"))

# Use Frappe's permission system
if not frappe.has_permission('Product', doc=product_doc, user=user):
    frappe.throw(_("No permission to access product"))
```

---

### Inventory Calculation Pattern

```python
# Always use Product + Department (2D model)
theoretical = calculate_theoretical_inventory(
    product=product,
    company=company,
    department=department,  # Required!
    as_on_date=date
)

# Storage location is NOT used in calculation
# Storage is metadata only for organizing counts
```

---

## 🔄 Data Flow Patterns

### Product Lifecycle

```
1. Create Product (Products Domain)
   └── Set primary count unit, conversions, properties

2. Assign to Departments (Products Domain)
   └── Create Product Department records
   └── Set par levels per department

3. Add Purchase Units (Products Domain)
   └── Create Purchase Unit records
   └── Set conversion factors

4. Create Inventory Balance (Inventory Domain)
   └── Auto-created when product assigned to department
   └── Initial quantity: 0

5. Receive Inventory (Procurement Domain)
   └── Invoice receipt updates inventory
   └── Allocated to department

6. Count in Audit (Inventory Domain)
   └── Physical count recorded
   └── Updates inventory balance

7. Sell via POS (POS Integration Domain)
   └── POS sale calculated
   └── Recipe depletions created

8. Calculate Depletion (POS Integration Domain)
   └── Recipe ingredients depleted
   └── Inventory reduced

9. Update Inventory (Inventory Domain)
   └── Inventory balance updated
   └── Theoretical inventory recalculated
```

---

### Inventory Flow

```
Last Audit → Starting Inventory (Product + Department)
+ Invoice Receipts → Received (allocated to department)
+ Transfers In → Added (to department)
- Transfers Out → Removed (from department)
- Depletions → Removed (from department)
= Theoretical Inventory (Product + Department)
```

---

### Permission Flow

```
User → Roles → Permissions (Frappe built-in)
User → Departments → Department Permissions (custom)
Combined → Effective Permissions
Applied → All Queries and Actions
```

---

## 📋 Required Reading Before Development

**All developers must read:**

1. **00-ARCHITECTURE/01-Architecture-Design.md** - Core architecture principles
2. **00-ARCHITECTURE/02-Application-Structure.md** - DocType structure and modules
3. **PROJECT-CONTEXT.md** - This document (project-wide context)
4. **AGENT-INSTRUCTIONS.md** - How to work on this project
5. **CROSS-DOMAIN-REFERENCE.md** - Domain interactions and shared patterns

**Domain-specific developers must also read:**

6. **Their Domain's README.md** - Domain overview and dependencies
7. **DEVELOPMENT-GUIDE.md** - Development roadmap and priorities
8. **Function documents** they're implementing

---

## 🎯 Development Principles

### 1. Consistency Over Speed
- Follow established patterns
- Use shared utilities
- Maintain data consistency
- Don't shortcut department/permission checks
- Prioritize long-term maintainability

### 2. Interoperability Over Isolation
- Consider cross-domain impacts
- Design for integration
- Use shared data models
- Avoid domain-specific hacks
- Think platform-wide

### 3. Frappe Best Practices
- Use DocType system (don't create raw SQL tables)
- Leverage built-in features (permissions, workflows, APIs)
- Follow Frappe conventions (naming, structure)
- Don't reinvent functionality (use Frappe's built-ins)

### 4. Department-First Thinking
- Always consider departments
- Support department filtering
- Respect department permissions
- Enable department reporting
- Think department-aware

---

## 🚨 Common Pitfalls

1. **Forgetting Department Filtering**: Always filter by user's accessible departments in queries
2. **Storing Converted Quantities**: Always store in primary unit, convert on display
3. **Ignoring Storage Metadata**: Storage is metadata, not part of inventory calculation
4. **Duplicating Conversion Logic**: Use Product's conversion methods, don't create your own
5. **Bypassing Permissions**: Always check permissions before queries/actions
6. **Creating Separate Platforms**: Use single unified system with departments
7. **Forgetting 2D Model**: Always use Product + Department for inventory, never just Product
8. **Hard-coding Values**: Use configuration, not hard-coded values
9. **Ignoring Unit Conversion**: Always use Product's conversion methods
10. **Missing Error Handling**: Always handle errors gracefully

---

## 📞 When in Doubt

1. **Check Dependencies**: Review domain README for dependencies
2. **Review Architecture**: Check 00-ARCHITECTURE/ documents
3. **Follow Patterns**: Use established patterns in this document
4. **Ask Questions**: If something seems inconsistent, ask before implementing
5. **Review Cross-Domain**: Check CROSS-DOMAIN-REFERENCE.md for integration patterns

---

## 🔍 Key Questions to Answer

Before implementing any functionality, ask:

1. **Does this follow the unified platform approach?** (single system, not separate platforms)
2. **Does this respect departments?** (department-aware, department-filtered)
3. **Does this use the 2D inventory model?** (Product + Department, not storage)
4. **Does this use primary count units?** (store in primary, convert on display)
5. **Does this avoid duplication?** (use shared methods, don't reinvent)
6. **Does this integrate well?** (works with other domains, follows patterns)

---

**Remember**: This is a unified platform with department-based segmentation. All functionality should work across all product types and respect department boundaries. Storage is metadata for organization, not part of inventory calculations. All quantities are stored in primary count units with on-the-fly conversions.


