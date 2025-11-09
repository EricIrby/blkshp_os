# BLKSHP OS – Change Log

## 2025-11-09

- Enforced Department autoname consistency by generating names from `department_code` and company code, and removed conflicting JSON format strings.
- Added doc events that validate `Department Permission` and `Role Permission` child rows (and their parent `User`/`Role` documents) so custom fields and registry lookups stay in sync.
- Hardened test fixtures (`department`, `product_department`, `permissions`) to provision required companies, roles, and metadata before exercising APIs.
- Documented DocType structure requirements and ensured Based Pyright is configured with local stubs.

