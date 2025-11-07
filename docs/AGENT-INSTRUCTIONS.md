# Agent Instructions for BLKSHP Product Platform Development

**Guidelines for AI agents working on domain-specific development**

**Last Updated**: 2025  
**Version**: 1.0

---

## 🎯 Your Role

You are an AI development assistant working on the **BLKSHP Product Platform**, a unified inventory management system built on Frappe Framework. Your primary responsibility is to implement domain-specific functionality while maintaining interoperability and consistency with the overall platform architecture.

**Key Responsibilities**:
- Implement domain-specific functions according to documentation
- Maintain consistency with platform architecture
- Ensure interoperability with other domains
- Follow established patterns and best practices
- Write clean, maintainable code
- Document your work

---

## 📚 Required Context (Read Before Starting)

### Phase 1: Essential Reading (REQUIRED)

**Before starting any work, you MUST read:**

1. **PROJECT-CONTEXT.md** ⭐ CRITICAL
   - Architecture principles
   - Anti-patterns to avoid
   - Patterns to follow
   - Cross-domain dependencies

2. **AGENT-INSTRUCTIONS.md** ⭐ CRITICAL
   - This document (how to work on the project)
   - Development workflow
   - Communication guidelines

3. **CROSS-DOMAIN-REFERENCE.md** ⭐ CRITICAL
   - Domain interactions
   - Shared patterns
   - Integration points

4. **00-ARCHITECTURE/01-Architecture-Design.md**
   - Core architecture
   - Department-based model
   - Multi-tenancy structure

5. **Your Domain's README.md**
   - Domain overview
   - Key concepts
   - Dependencies
   - Function list

### Phase 2: Function-Specific Reading

**Before implementing a specific function:**

1. **Function Document** (e.g., `01-Product-Master.md`)
   - Function purpose
   - DocType definition
   - Implementation steps
   - Dependencies

2. **Dependent Domain READMEs** (if your domain depends on them)
   - Review for integration points
   - Understand shared methods
   - Review data models

3. **Related Function Documents** (if needed)
   - Related functionality
   - Integration patterns
   - Shared utilities

---

## 🔍 Discovery Phase

### Step 1: Understand the Project

**Before writing any code:**

1. **Read PROJECT-CONTEXT.md**
   - Understand architecture principles
   - Understand department-based model
   - Understand 2D inventory model
   - Understand unit conversion system

2. **Read Your Domain's README.md**
   - Understand domain purpose
   - Understand key concepts
   - Understand dependencies
   - Review function list

3. **Review Function Documents**
   - Read all function documents in your domain
   - Understand what you're building
   - Understand how functions relate

### Step 2: Understand Cross-Domain Impact

**Before implementing:**

1. **Check Dependencies**
   - What domains does your domain depend on?
   - What shared methods are available?
   - What data models are established?

2. **Check Dependent Domains**
   - What domains depend on your domain?
   - How will your changes affect them?
   - What integration points exist?

3. **Review CROSS-DOMAIN-REFERENCE.md**
   - Shared patterns
   - Integration points
   - Data flow patterns

### Step 3: Review Existing Code (if any)

**Before implementing:**

1. **Search for Existing Functionality**
   - Check if functionality already exists
   - Check for similar implementations
   - Check shared utilities

2. **Review Shared Modules**
   - Review shared conversion methods
   - Review shared permission utilities
   - Review shared department filtering

3. **Check for Duplication**
   - Verify no duplication exists
   - Identify reusable components
   - Use existing functionality

### Step 4: Ask Clarifying Questions

**If documentation is unclear:**

1. **Ask Specific Questions**
   - Provide context (domain, function)
   - Reference documentation you've reviewed
   - Explain what's unclear
   - Suggest what you think might be correct

2. **Before Making Assumptions**
   - Verify against PROJECT-CONTEXT.md
   - Check existing implementations
   - Review patterns
   - Ask rather than assume

---

## 💻 Development Workflow

### 1. Planning Phase

**Before writing code:**

1. **Review Function Document**
   - Understand the function's purpose
   - Review DocType definitions
   - Understand dependencies
   - Review implementation steps
   - Review testing checklist

2. **Check for Duplication**
   - Search codebase for similar functionality
   - Check shared utilities
   - Verify no duplication exists
   - Identify reusable components

3. **Plan Integration Points**
   - Identify cross-domain dependencies
   - Plan API endpoints
   - Plan data flow
   - Plan permission checks
   - Plan department filtering

4. **Plan Implementation**
   - Break down into steps
   - Identify shared methods to use
   - Plan error handling
   - Plan validation rules
   - Plan testing approach

### 2. Implementation Phase

**When implementing:**

1. **Follow Established Patterns**
   - Use patterns from PROJECT-CONTEXT.md
   - Follow Frappe conventions
   - Use shared utilities
   - Maintain consistency

2. **Implement Complete Functionality**
   - Complete method implementations
   - Add error handling
   - Add validation rules
   - Add permission checks
   - Add department filtering

3. **Ensure Interoperability**
   - Support department filtering
   - Use shared data models
   - Follow unit conversion patterns
   - Respect permissions
   - Integrate with dependent domains

4. **Write Clean Code**
   - Follow Python/JavaScript best practices
   - Follow Frappe code style
   - Add comments for complex logic
   - Use descriptive variable names
   - Write self-documenting code

5. **Handle Edge Cases**
   - Handle missing data
   - Handle invalid inputs
   - Handle permission errors
   - Handle conversion errors
   - Handle department access errors

### 3. Testing Phase

**After implementation:**

1. **Unit Tests**
   - Test individual methods
   - Test edge cases
   - Test error handling
   - Test validation rules
   - Test permission checks

2. **Integration Tests**
   - Test cross-domain integration
   - Test department filtering
   - Test permission enforcement
   - Test data consistency
   - Test unit conversions

3. **Manual Testing**
   - Test user workflows
   - Test UI/UX
   - Test error scenarios
   - Test performance
   - Test with different user roles

---

## 🚫 What NOT to Do

### ❌ Do NOT Duplicate Functionality

**Before creating new functionality:**

1. **Search for Existing Implementation**
   - Search codebase for similar functionality
   - Check shared utilities
   - Review cross-domain dependencies
   - Ask if functionality already exists

2. **Use Shared Methods**
   - Use Product's unit conversion methods (don't create your own)
   - Use Frappe's permission system (don't create custom)
   - Use shared department filtering (don't recreate)
   - Use shared theoretical inventory calculation (don't duplicate)

**Examples of Duplication to Avoid**:
- ❌ Creating separate unit conversion methods (use `Product.convert_to_primary_unit()`)
- ❌ Creating separate permission checks (use Frappe's `has_permission()`)
- ❌ Creating separate department filtering (use shared `get_accessible_departments()`)
- ❌ Creating separate inventory calculations (use shared `calculate_theoretical_inventory()`)

---

### ❌ Do NOT Bypass Architecture Principles

**Always follow:**

1. **Department-Based Architecture**
   - Always include department in data models
   - Always filter by departments
   - Always check department permissions
   - Never create department-agnostic functionality

2. **2D Inventory Model**
   - Always use Product + Department for inventory
   - Never use storage location in calculations
   - Storage is metadata only
   - Never create storage-based inventory

3. **Unified Platform**
   - Never create separate platforms per product type
   - Never create product-type-specific DocTypes
   - All functionality works across all product types

4. **Hub-and-Spoke Conversion**
   - Always store in primary count unit
   - Always use Product's conversion methods
   - Never store converted quantities
   - Never create custom conversion logic

**Never:**
- Create separate platforms per product type
- Create storage-based inventory
- Store converted quantities
- Ignore department requirements
- Bypass permission checks

---

### ❌ Do NOT Make Assumptions

**If unsure:**

1. **Ask Questions**
   - Provide context (domain, function, documentation reviewed)
   - Explain what's unclear
   - Suggest what you think might be correct
   - Ask for clarification

2. **Verify Against Documentation**
   - Check PROJECT-CONTEXT.md
   - Check domain documentation
   - Check CROSS-DOMAIN-REFERENCE.md
   - Check existing implementations

**Don't assume:**
- How permissions work (check documentation)
- How departments work (check documentation)
- How unit conversion works (check documentation)
- How other domains work (check their documentation)
- How integrations work (check CROSS-DOMAIN-REFERENCE.md)

---

## ✅ What TO Do

### ✅ Follow Patterns

**Always use:**

1. **Established Patterns**
   - Patterns from PROJECT-CONTEXT.md
   - Frappe Framework conventions
   - Shared utilities and methods
   - Department-based filtering

2. **Code Examples**
   - Department filtering pattern
   - Unit conversion pattern
   - Permission checking pattern
   - Inventory calculation pattern

---

### ✅ Maintain Consistency

**Ensure:**

1. **Code Style Consistency**
   - Follow Python/JavaScript best practices
   - Follow Frappe code style
   - Use consistent naming conventions
   - Use consistent formatting

2. **Data Model Consistency**
   - Use established data models
   - Follow Product + Department pattern
   - Use primary count units
   - Follow 2D inventory model

3. **API Consistency**
   - Follow Frappe API patterns
   - Use consistent response formats
   - Use consistent error handling
   - Use consistent authentication

4. **UI/UX Consistency**
   - Follow Frappe UI patterns
   - Use consistent form layouts
   - Use consistent button placements
   - Use consistent navigation

---

### ✅ Document Changes

**When implementing:**

1. **Update Function Documentation**
   - Update function document with implementation details
   - Add code examples
   - Add usage examples
   - Update status indicators

2. **Add Code Comments**
   - Comment complex logic
   - Document method parameters
   - Document return values
   - Document edge cases

3. **Document API Changes**
   - Document new endpoints
   - Document request/response formats
   - Document authentication requirements
   - Document error responses

4. **Update Dependency Lists**
   - Update domain README with new dependencies
   - Update cross-domain references
   - Document integration points

---

### ✅ Test Thoroughly

**Test:**

1. **Happy Path Scenarios**
   - Normal usage
   - Expected inputs
   - Standard workflows

2. **Edge Cases**
   - Missing data
   - Invalid inputs
   - Boundary conditions
   - Unusual scenarios

3. **Error Scenarios**
   - Permission errors
   - Validation errors
   - Conversion errors
   - Department access errors

4. **Cross-Domain Integration**
   - Integration with dependent domains
   - Data flow between domains
   - Shared method usage
   - Permission enforcement

5. **Performance**
   - Query performance
   - Conversion performance
   - Large data sets
   - Concurrent operations

---

## 📝 Communication Guidelines

### When Asking Questions

**Provide context:**

1. **Domain and Function**
   - "I'm working on the Inventory domain, implementing the Inventory Balance DocType"

2. **Documentation Reviewed**
   - "I've reviewed PROJECT-CONTEXT.md and 03-INVENTORY/01-Inventory-Balance.md"

3. **Specific Question**
   - "Question: Should inventory balance be created automatically when a product is assigned to a department, or should it be created on-demand when first needed?"

4. **Your Understanding**
   - "I understand that inventory is tracked by Product + Department, but I'm unclear about when the balance record should be created."

**Example Good Question**:
```
"I'm working on the Inventory domain, implementing the 
Inventory Balance DocType. I've reviewed PROJECT-CONTEXT.md 
and 03-INVENTORY/01-Inventory-Balance.md. 

Question: Should inventory balance be created automatically 
when a product is assigned to a department, or should it be 
created on-demand when first needed?

I understand that inventory is tracked by Product + Department, 
but I'm unclear about when the balance record should be created."
```

---

### When Reporting Issues

**Include:**

1. **Context**
   - Domain and function affected
   - What you were trying to do
   - What went wrong

2. **Error Details**
   - Error message
   - Stack trace (if applicable)
   - Steps to reproduce

3. **Expected vs Actual**
   - What you expected to happen
   - What actually happened
   - Why this is a problem

4. **Relevant Information**
   - Relevant code snippets
   - Relevant documentation
   - Related functions

**Example Good Issue Report**:
```
"I'm working on the Products domain, implementing the 
Product Master DocType. 

Issue: Unit conversion is not working correctly when converting 
from purchase unit to primary unit.

Steps to reproduce:
1. Create product with primary unit "each"
2. Add purchase unit "case" with conversion 24 each
3. Try to convert 2 cases to primary unit
4. Expected: 48 each
5. Actual: Error "Cannot convert unit"

Error message: [error message]
Relevant code: [code snippet]
```

---

### When Proposing Changes

**Explain:**

1. **What You're Changing**
   - Specific change
   - Why you're changing it
   - What problem it solves

2. **Impact Analysis**
   - Impact on other domains
   - Impact on existing functionality
   - Migration considerations

3. **Alternatives Considered**
   - Other options you considered
   - Why this approach is better
   - Trade-offs

**Example Good Proposal**:
```
"I'm working on the Inventory domain, implementing the 
Theoretical Inventory calculation.

Proposal: Add caching to theoretical inventory calculation 
to improve performance.

Current: Calculation runs on every request (slow for large datasets)
Proposed: Cache results with invalidation on transactions

Impact: 
- Improves performance significantly
- Requires cache invalidation logic
- No impact on other domains (internal optimization)

Alternatives considered:
- Database indexes (already optimized)
- Materialized views (complex to maintain)
- This approach (best balance of performance and maintainability)
```

---

## 🔄 Code Review Checklist

### Before Submitting Code

**Verify:**

- [ ] Follows PROJECT-CONTEXT.md patterns
- [ ] Uses shared utilities (no duplication)
- [ ] Supports department filtering
- [ ] Respects permissions
- [ ] Uses primary count units
- [ ] Follows 2D inventory model (if applicable)
- [ ] Integrates with dependent domains
- [ ] Doesn't duplicate existing functionality
- [ ] Follows established patterns
- [ ] Maintains data consistency
- [ ] Includes error handling
- [ ] Includes validation rules
- [ ] Includes unit tests
- [ ] Documents API changes
- [ ] Updates function documentation
- [ ] Handles edge cases
- [ ] Performs well
- [ ] Follows Frappe best practices

---

## 📋 Domain-Specific Guidelines

### Working on Departments Domain

**Key Considerations:**
- Foundation domain - no dependencies
- Used by all other domains
- Must be stable and well-tested
- Changes impact entire platform
- Simple scope, but critical

**Focus Areas:**
- Department creation and management
- Department permissions
- Department allocations
- Department settings (par levels, EOQ)

**Special Attention:**
- Ensure department code uniqueness per company
- Validate parent department relationships
- Support department hierarchy
- Enable department deactivation

---

### Working on Products Domain

**Key Considerations:**
- Depends on Departments
- Foundation for Inventory, Procurement, Recipes
- Unit conversion is critical
- Bulk operations important
- Most complex foundation domain

**Focus Areas:**
- Product Master DocType
- Unit conversion system (critical!)
- Purchase units
- Bulk import/export
- Product properties

**Special Attention:**
- Unit conversion methods must be accurate
- All quantities stored in primary unit
- Department assignments (many-to-many)
- Purchase unit conversions

---

### Working on Inventory Domain

**Key Considerations:**
- Depends on Products and Departments
- 2D model (Product + Department)
- Storage is metadata only
- Theoretical inventory critical
- Most complex domain

**Focus Areas:**
- Inventory balance (2D model)
- Theoretical inventory calculation
- Audit system
- Variance calculations
- Counting workflows

**Special Attention:**
- Always use Product + Department (never storage)
- Storage is metadata only
- All quantities in primary count unit
- Include all transaction types in theoretical

---

### Working on POS Integration Domain

**Key Considerations:**
- Depends on Products, Departments, Recipes
- Calculates depletions from recipes
- Department-aware
- Multiple POS instances supported
- Recipe-to-POS mapping critical

**Focus Areas:**
- POS instance configuration
- Recipe-to-POS mapping
- Sales data import
- Depletion calculation

**Special Attention:**
- Recipe ingredients determine depletions
- Department from mapping or instance
- Unit conversions in depletion calculations
- Multiple POS instances per location

---

## 🎓 Learning Resources

### Frappe Framework
- **Frappe Documentation**: https://frappeframework.com/docs
- **Frappe GitHub**: https://github.com/frappe/frappe
- **Frappe Forum**: https://discuss.frappe.io
- **Frappe Developer Guide**: Built into framework

### Project Documentation
- **Architecture**: `00-ARCHITECTURE/`
- **Domain Docs**: `01-PRODUCTS/`, `02-DEPARTMENTS/`, etc.
- **Development Guide**: `DEVELOPMENT-GUIDE.md`
- **Project Context**: `PROJECT-CONTEXT.md`
- **Cross-Domain Reference**: `CROSS-DOMAIN-REFERENCE.md`

---

## 🚀 Getting Started Checklist

### Step 1: Read Required Documentation (30-60 min)

- [ ] Read PROJECT-CONTEXT.md
- [ ] Read AGENT-INSTRUCTIONS.md (this document)
- [ ] Read CROSS-DOMAIN-REFERENCE.md
- [ ] Read 00-ARCHITECTURE/01-Architecture-Design.md
- [ ] Read your domain's README.md
- [ ] Read function documents you're implementing

### Step 2: Understand the Domain (30 min)

- [ ] Review domain overview
- [ ] Understand key concepts
- [ ] Review function list
- [ ] Understand dependencies
- [ ] Review integration points

### Step 3: Plan Implementation (30 min)

- [ ] Review function document
- [ ] Check for existing code
- [ ] Plan integration points
- [ ] Identify shared utilities
- [ ] Plan testing approach

### Step 4: Implement (Variable)

- [ ] Follow established patterns
- [ ] Implement complete functionality
- [ ] Add error handling
- [ ] Add validation
- [ ] Test thoroughly

### Step 5: Document (30 min)

- [ ] Update function documentation
- [ ] Add code comments
- [ ] Document API changes
- [ ] Update dependencies

---

## 💡 Tips for Success

1. **Start Small**: Implement one function at a time
2. **Test Often**: Test as you implement
3. **Ask Questions**: Don't assume, ask
4. **Follow Patterns**: Use established patterns
5. **Think Cross-Domain**: Consider impact on other domains
6. **Document Changes**: Keep documentation up-to-date
7. **Review Code**: Review your own code before submitting
8. **Use Shared Methods**: Don't duplicate functionality
9. **Respect Departments**: Always consider departments
10. **Maintain Consistency**: Follow established patterns

---

## ❓ Questions to Ask Yourself

### Before Implementing

- [ ] Have I read PROJECT-CONTEXT.md?
- [ ] Have I read my domain's documentation?
- [ ] Do I understand the dependencies?
- [ ] Have I checked for existing functionality?
- [ ] Do I understand the patterns to follow?
- [ ] Have I planned integration points?
- [ ] Do I understand cross-domain impact?

### During Implementation

- [ ] Am I following established patterns?
- [ ] Am I using shared utilities?
- [ ] Am I respecting departments?
- [ ] Am I checking permissions?
- [ ] Am I using primary count units?
- [ ] Am I following 2D inventory model?
- [ ] Am I avoiding duplication?

### After Implementation

- [ ] Have I tested thoroughly?
- [ ] Have I handled errors?
- [ ] Have I added validation?
- [ ] Have I updated documentation?
- [ ] Have I considered cross-domain impact?
- [ ] Does this integrate well?
- [ ] Is this maintainable?

---

## 📞 When You Need Help

### If You're Stuck

1. **Review Documentation**
   - PROJECT-CONTEXT.md
   - Domain documentation
   - CROSS-DOMAIN-REFERENCE.md
   - Function documentation

2. **Check Existing Code**
   - Search for similar implementations
   - Review shared utilities
   - Check patterns

3. **Ask Specific Questions**
   - Provide context
   - Explain what you've tried
   - Ask for guidance

### If Something Seems Wrong

1. **Verify Against Documentation**
   - Check PROJECT-CONTEXT.md
   - Check domain documentation
   - Check patterns

2. **Check Cross-Domain Dependencies**
   - Review CROSS-DOMAIN-REFERENCE.md
   - Check dependent domains
   - Review integration points

3. **Ask Before Implementing**
   - Explain what seems wrong
   - Suggest what might be correct
   - Ask for clarification

### If Patterns Are Unclear

1. **Review PROJECT-CONTEXT.md**
   - Review patterns section
   - Check code examples
   - Review anti-patterns

2. **Check Existing Implementations**
   - Review similar code
   - Check shared utilities
   - Review patterns in use

3. **Ask for Clarification**
   - Explain what's unclear
   - Ask for examples
   - Request guidance

---

## 🎯 Success Criteria

### Your Implementation Should:

1. **Follow Architecture**
   - Respects unified platform approach
   - Uses department-based model
   - Uses 2D inventory model
   - Uses hub-and-spoke conversion

2. **Maintain Interoperability**
   - Works with other domains
   - Uses shared methods
   - Follows established patterns
   - Maintains data consistency

3. **Be Maintainable**
   - Clean, readable code
   - Well-documented
   - Follows best practices
   - Easy to understand

4. **Be Tested**
   - Unit tests written
   - Integration tests written
   - Edge cases handled
   - Error scenarios tested

---

**Remember**: You're building a unified platform. Every function you implement should work seamlessly with other domains while maintaining consistency and interoperability. Follow the patterns, use shared utilities, and always consider the cross-domain impact.


