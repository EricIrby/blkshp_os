# Products Domain – Implementation Plan

_Last updated: 2025-11-08_

## Goal
Implement the Products foundation domain (DocTypes, services, tests, fixtures, documentation) so downstream modules (Inventory, Procurement, Recipes, POS) can rely on a unified product master with accurate unit conversion and department allocations.

---

## Phase 0 – Prerequisites
- ✅ Review domain documentation (`docs/01-PRODUCTS/*`, `CROSS-DOMAIN-REFERENCE.md`).
- ✅ Branch created: `feature/products-domain`.
- ☐ Confirm latest fixtures for departments/permissions are installed (`bench --site <site> migrate` + `setup_test_data` if needed).

---

## Phase 1 – Data Model (DocTypes) ✅
Create/verify DocTypes under `blkshp_os/products/doctype/` with JSON + Python controllers.

| DocType | Purpose | Key Fields / Tables | Notes |
|---------|---------|----------------------|-------|
| `Product` | Unified product master | Core product fields, count unit hub, product properties, department table, purchase units child, tags, par levels | Autoname via `product_code`; ensure unique code per company. |
| `Product Category` | Hierarchical categorisation | Parent/child hierarchy, type, GL code | Might live in same module even if behaviour minimal. |
| `Purchase Unit` (child) | Vendor packaging | Vendor link, conversion factor, price/contract price, preferred flag | Typically child table of Product. |
| `Product Storage Area` (child) | Storage metadata | Storage area link, default flag | Depends on Inventory doc; keep optional placeholder. |
| `Product Tag` (child) | Tags | Simple tag table or reuse Frappe Tag? Decide based on docs. |
| `Substitute Item` (child) | Product substitutes | Linked product, priority, preferred flag | Supports product properties. |
| `Promo Threshold` (standalone?) | Promotional pricing | Vendor, product/category, thresholds, promo price | Check dependency with Procurement; may defer if out-of-scope. |
| `Contract Price Violation` | Price monitoring | Invoice refs, variance calc | Likely sits in Procurement; evaluate if created later. |
| `Item Loader` | Bulk import | File handling, column mapping, status tracking | Requires background jobs + pandas/openpyxl. Might be Phase 3 if heavy. |
| `Column Mapping`, `Validation Error`, `Import Result` | Item Loader child tables | Mapping & audit | Only if loader implemented now. |

### Tasks
1. ✅ Scaffold DocType directories (`frappe` CLI or manual).
2. ✅ Define DocType JSON (fields, permissions). Respect department filters.
3. ✅ Implement Python controllers:
   - Validation (`validate`), `before_save`, `on_update`.
   - Helper methods (unit conversions, department assignment).
4. ☐ Export DocTypes to JSON via `bench export-doc` for reproducibility.

---

## Phase 2 – Server Logic & Services ✅

### Conversion Utilities
- ✅ Implement hub-and-spoke conversions within `blkshp_os/products/doctype/product/product.py`.
- ✅ Provided helper methods for count units, purchase units, and standard conversion tables.
- ✅ Validated conversion factors across volume, weight, and purchase units.

### Department Integration
- ✅ Reused `Product Department` child table from Departments domain.
- ✅ Added helper methods for department access/allocation.
- ✅ Ensured default department alignment and enforced rules for non-inventory items.

### Product Lifecycle Hooks
- Auto-generate `product_code` if missing (pattern: category prefix + sequence? confirm doc).
- Ensure `default_department` exists in departments table.
- Sync `preferred_purchase_unit` to child entries.
- Restrict editing critical fields when downstream transactions exist (placeholder for future).

### Services/APIs
✅ Created `blkshp_os/products/service.py` and `blkshp_os/api/products.py`.

**Service functions**
- `create_product(data, user)`
- `update_product(product_name, data, user)`
- `search_products(filters, user)`
- `get_product_details(product_name, include_purchase_units=True, include_departments=True)`
- `bulk_assign_departments(product_names, department, add=True)`

**Whitelisted endpoints**
- `get_product` (read)
- `list_products` (with department filter)
- `create_product` / `update_product` (role + department perms)
- `convert_quantity` (utility endpoint for UI)
- `get_purchase_units` (optionally vendor filtered)

All endpoints:
- ✅ Check Frappe DocType permissions alongside department permissions.
- ✅ Return primary unit conversions with optional target units.

---

## Phase 3 – Unit Tests
- Location: `blkshp_os/products/doctype/<doctype>/test_<doctype>.py` and service tests under `blkshp_os/products/test_services.py`.
- Cover:
  - Product validation (unique code per company, required fields).
  - Department assignment logic.
  - Conversion accuracy (including edge cases).
  - Purchase unit price + conversion calculations.
  - Product properties flags (generic, non-inventory, prep item) behaviour.
  - API tests using Frappe test client (permissions + filtering).
- Integration tests once Inventory/Procurement exist (placeholder skipped for now).

---

## Phase 4 – Fixtures & Seeds
- Update `fixtures/standard_roles.json` if new permissions (e.g., `Products Manager`) required.
- Potential fixture for default count units / categories (if documentation mandates).
- Extend `scripts/setup_test_data.py` to populate sample products with purchase units and departments.

---

## Phase 5 – Client/UI Enhancements
- `product.js` form script:
  - Enforce hub conversions UI logic.
  - Auto-fill conversion factors.
  - Provide buttons (`Assign Departments`, `View Purchase Units`, `Print Labels` placeholders).
- Possibly reuse global scripts for department filtering (check existing `user.js`).

---

## Phase 6 – Bulk Operations (Optional for MVP)
- If scope includes Item Loader now:
  - Implement file parsing using pandas/openpyxl.
  - Add background job to process imports (`enqueue`).
  - Provide status feedback via DocType and notifications.
  - Write tests mocking upload workflow.
- Otherwise, document as future enhancement in this plan.

---

## Documentation & Communication
- Update:
  - `docs/01-PRODUCTS/IMPLEMENTATION-SUMMARY.md` (create if missing).
  - API entries in `docs/API-REFERENCE.md`.
  - Cross-domain references if new shared utilities created.
- Note any deviations or outstanding questions in this plan (see below).

---

## Testing Checklist
- `bench --site <site> run-tests --module blkshp_os.products`
- Manual QA scenarios:
  - Create/edit product via Desk UI.
  - Assign/unassign departments respecting permissions.
  - Add purchase units with conversions; verify cost per primary unit.
  - Use whitelisted conversion API (simulate UI call).
  - Validate non-inventory flag excludes product from department requirement.

---

## Open Questions / Decisions Needed
1. **Autoname pattern**: Confirm product code convention (`PROD-0001` vs. category-based).
2. **Storage areas**: Inventory docs not yet implemented—should we store references now or defer?
3. **Promo/violation DocTypes**: Implement in Products or defer to Procurement domain?
4. **Bulk loader timing**: MVP now vs. later phase.
5. **Tags**: Use Frappe tags or dedicated child table?

Document answers here as they are resolved.

---

## Next Steps
1. ✅ Finalize plan (this document).
2. ☐ Scaffold DocTypes & controllers (Phase 1).
3. ☐ Implement services & conversions (Phase 2).
4. ☐ Add API endpoints (Phase 2).
5. ☐ Build test suite (Phase 3).
6. ☐ Update fixtures/scripts (Phase 4).
7. ☐ UX polish (Phase 5).
8. ☐ Decide on bulk loader scope (Phase 6).


