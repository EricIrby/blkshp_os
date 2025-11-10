"""Fixture smoke tests for the Core Platform subscription objects."""
from __future__ import annotations

import json
from collections.abc import Iterable

import frappe
from frappe.tests.utils import FrappeTestCase

EXPECTED_MODULE_KEYS = {"core", "products", "inventory", "procurement", "analytics"}
EXPECTED_FEATURE_KEYS = {
	"core.workspace.access",
	"products.bulk_operations",
	"inventory.audit_workflows",
	"procurement.ottimate_import",
	"analytics.finance_dashboard",
}


class TestSubscriptionPlanFixtures(FrappeTestCase):
	"""Ensure default plans, modules, and feature toggles ship with the app."""

	_is_loaded = False

	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		if not cls._is_loaded:
			for doctype in ("feature_toggle", "subscription_plan", "module_activation"):
				frappe.reload_doc("core_platform", "doctype", doctype)
			cls._is_loaded = True

	def setUp(self) -> None:
		super().setUp()
		frappe.db.rollback()

	def test_foundation_plan_fixture_present(self) -> None:
		plan_name = frappe.db.exists("Subscription Plan", {"plan_code": "FOUNDATION"})
		self.assertIsNotNone(plan_name, "Subscription Plan 'FOUNDATION' should exist as a fixture")

		plan = frappe.get_doc("Subscription Plan", plan_name)
		self.assertEqual(plan.plan_name, "Foundation")
		self.assertTrue(plan.is_active)

		overrides = self._load_json(plan.default_feature_overrides)
		self.assertIn("core.workspace.access", overrides)
		self.assertTrue(overrides["core.workspace.access"])

	def test_default_feature_toggles_registered(self) -> None:
		feature_keys = {row.feature_key for row in frappe.get_all("Feature Toggle", fields=["feature_key"])}
		self.assertTrue(EXPECTED_FEATURE_KEYS.issubset(feature_keys))

	def test_module_activation_dependencies(self) -> None:
		modules = frappe.get_all(
			"Module Activation",
			filters={"plan": "FOUNDATION"},
			fields=["module_key", "depends_on", "is_required", "feature_overrides"],
		)
		module_keys = {row.module_key for row in modules}
		self.assertSetEqual(module_keys, EXPECTED_MODULE_KEYS)

		for module in modules:
			dependencies = self._split_dependencies(module.depends_on)
			self._assert_dependencies_valid(module.module_key, dependencies)

			if module.feature_overrides:
				overrides = self._load_json(module.feature_overrides)
				for feature_key in overrides:
					self.assertIn(
						feature_key,
						EXPECTED_FEATURE_KEYS,
						msg=f"Feature override {feature_key} is not part of the default registry",
					)

	def test_basic_plan_fixture(self) -> None:
		"""Compatibility wrapper for the acceptance test reference in BLK-6."""
		self.test_foundation_plan_fixture_present()

	def _split_dependencies(self, raw: str | None) -> set[str]:
		if not raw:
			return set()
		return {token.strip().lower() for token in raw.split(",") if token.strip()}

	def _assert_dependencies_valid(self, module_key: str, dependencies: Iterable[str]) -> None:
		dependency_set = set(dependencies)
		self.assertNotIn(module_key, dependency_set, f"Module {module_key} cannot depend on itself")
		self.assertTrue(dependency_set.issubset(EXPECTED_MODULE_KEYS), "Dependencies must reference known modules")

	def _load_json(self, raw: str | None) -> dict[str, object]:
		if not raw:
			return {}
		return json.loads(raw)
