# Core Platform Subscription Model

## Overview

The Core Platform module centralises subscription plans, module activation rules, feature toggles, and tenant branding data. These DocTypes provide the foundation for enforcing feature access across the consolidated BLKSHP stack and for feeding the frontend feature matrix.

### Key DocTypes

| DocType | Purpose | Highlights |
| --- | --- | --- |
| **Subscription Plan** | Defines commercially packaged plans. | Unique plan code, billing metadata, and plan-wide feature overrides stored as JSON. |
| **Module Activation** | Lists modules enabled per plan. | Stores dependency mapping (comma-separated module keys) and feature overrides tied to a particular module. |
| **Feature Toggle** | Registry of granular feature flags. | Normalised `feature_key` (dot-notation) used by backend enforcement and the SPA feature matrix. |
| **Tenant Branding** | Branding assets for a tenant/site. | Optional link to subscription plan, colour palette, media assets, and custom CSS variables. |

## Field Conventions

- **Keys:** `plan_code`, `module_key`, and `feature_key` are stored uppercase/lowercase-normalised for predictable lookups (validation enforces formatting).
- **JSON Fields:** `default_feature_overrides`, `feature_overrides`, and `custom_properties` must contain serialisable JSON objects. Validation ensures well-formed structures during save/fixture import.
- **Dependencies:** `Module Activation.depends_on` accepts a comma-separated list of module keys. Validation rejects self-references and stores a normalised string.

## Default Fixtures

The app ships with baseline data to bootstrap new benches:

- `Feature Toggle` – five core toggles (`core.workspace.access`, `products.bulk_operations`, `inventory.audit_workflows`, `procurement.ottimate_import`, `analytics.finance_dashboard`).
- `Subscription Plan` – a **Foundation** plan (`plan_code` = `FOUNDATION`) covering core, product, inventory, procurement, and analytics modules.
- `Module Activation` – module records linked to the Foundation plan, each with dependency metadata and feature overrides.

Fixtures are managed via `hooks.fixtures` so `bench migrate` automatically loads the default catalog.

## Usage Notes

1. **Extending Plans** – Create a new `Subscription Plan` and associated `Module Activation` records. Override features per module or at the plan level using JSON payloads.
2. **Feature Enforcement** – Downstream enforcement code (BLK-7/BLK-9) should reference `Feature Toggle` keys and module activations to calculate a tenant’s effective feature set.
3. **Branding** – Use `Tenant Branding` to store per-tenant theming once provisioning workflows (BLK-12/BLK-33) assign plans to Press sites.

## Operational Separation

- **Tenant Experience:** Tenant users authenticate via the SPA and consume read/write APIs that respect the feature matrix derived from their assigned plan. They cannot self-manage plans, modules, or feature toggles.
- **BLKSHP Operations:** Plan changes, module activations, and feature overrides are performed exclusively by BLKSHP staff using internal Desk tooling (BLK-10) and automation scripts (BLK-12/BLK-33).
- **Request Flow:** Customers contact BLKSHP to request upgrades or feature adjustments. Operations staff apply changes in the admin backend, and the tenant-facing feature matrix updates automatically.
- **Audit & Logging:** All administrative changes must be logged with operator identity and rationale so tenant-visible behaviour remains traceable.

Refer to Linear issue **BLK-6** for implementation history and acceptance criteria. Run the fixture regression check with:

```bash
bench execute blkshp_os.core_platform.tests.test_subscription_plan.test_basic_plan_fixture
```
