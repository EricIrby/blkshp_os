"""Tests for feature matrix service and API helpers."""
from __future__ import annotations

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.core_platform.services import (
	clear_feature_matrix_cache,
	clear_subscription_context_cache,
	get_feature_matrix,
	get_feature_matrix_for_user,
	get_user_profile,
)
from blkshp_os.core_platform.services.feature_matrix import FEATURE_MATRIX_CACHE_KEY


class TestFeatureMatrix(FrappeTestCase):
	"""Validate feature matrix aggregation and profile helpers."""

	_is_loaded = False

	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		if not cls._is_loaded:
			for module, doctype in [
				("core_platform", "feature_toggle"),
				("core_platform", "subscription_plan"),
				("core_platform", "module_activation"),
				("core_platform", "tenant_branding"),
				("departments", "department"),
				("permissions", "department_permission"),
			]:
				frappe.reload_doc(module, "doctype", doctype)
			cls._is_loaded = True

	def setUp(self) -> None:
		super().setUp()
		frappe.db.rollback()
		clear_subscription_context_cache()
		clear_feature_matrix_cache()

		self.company = self._create_company("Matrix Test Company", "MTC", "USD")
		self.department = self._create_department("Matrix Department", "MATRIX", self.company.name)
		self._create_tenant_branding(self.company.name, "FOUNDATION")

		self._ensure_role("Employee")
		self._ensure_role("System Manager")

		self.standard_user = self._create_user(
			"matrix.user@example.com",
			"Matrix",
			roles=["Employee"],
			company=self.company.name,
			department=self.department.name,
		)
		self.operations_user = self._create_user(
			"ops.user@example.com",
			"Ops",
			roles=["System Manager"],
			company=self.company.name,
		)

	def test_feature_matrix_includes_modules_and_features(self) -> None:
		"""Plan metadata, modules, and feature flags are exposed for tenant users."""
		matrix = get_feature_matrix_for_user(user=self.standard_user)

		self.assertEqual(matrix["plan_code"], "FOUNDATION")
		self.assertIn("core", matrix["enabled_modules"])

		module_map = {module["key"]: module for module in matrix["modules"]}
		self.assertTrue(module_map["core"]["user_has_access"])
		self.assertIn("core.workspace.access", matrix["user_feature_access"])
		self.assertTrue(matrix["user_feature_access"]["core.workspace.access"])

	def test_feature_matrix_cache_cleared(self) -> None:
		"""Plan-level cache persists and can be cleared explicitly."""
		get_feature_matrix(plan_code="FOUNDATION")
		cached = frappe.cache().get_value(FEATURE_MATRIX_CACHE_KEY)
		self.assertIsInstance(cached, dict)
		self.assertIn("foundation", cached)

		clear_feature_matrix_cache()
		self.assertIsNone(frappe.cache().get_value(FEATURE_MATRIX_CACHE_KEY))

	def test_disabled_module_blocks_user_but_not_operations(self) -> None:
		"""Disabled modules remain inaccessible to standard users but bypass roles still see them."""
		module_name = frappe.get_value(
			"Module Activation",
			{"plan": "FOUNDATION", "module_key": "inventory"},
			"name",
		)
		self.assertIsNotNone(module_name)

		module_doc = frappe.get_doc("Module Activation", module_name)
		original_state = int(module_doc.is_enabled)

		try:
			module_doc.is_enabled = 0
			module_doc.save(ignore_permissions=True)
			clear_subscription_context_cache()
			clear_feature_matrix_cache()

			standard_matrix = get_feature_matrix_for_user(user=self.standard_user, refresh=True)
			operations_matrix = get_feature_matrix_for_user(user=self.operations_user, refresh=True)

			standard_inventory = next(module for module in standard_matrix["modules"] if module["key"] == "inventory")
			operations_inventory = next(module for module in operations_matrix["modules"] if module["key"] == "inventory")

			self.assertFalse(standard_inventory["is_enabled"])
			self.assertFalse(standard_inventory["user_has_access"])
			self.assertTrue(operations_inventory["user_has_access"])
		finally:
			module_doc.is_enabled = original_state
			module_doc.save(ignore_permissions=True)
			clear_subscription_context_cache()
			clear_feature_matrix_cache()

	def test_inactive_plan_flag_reflected(self) -> None:
		"""Inactive plans propagate their status in the matrix payload."""
		plan_doc = frappe.get_doc("Subscription Plan", "FOUNDATION")
		original_state = int(plan_doc.is_active)

		try:
			plan_doc.is_active = 0
			plan_doc.save(ignore_permissions=True)
			clear_subscription_context_cache()
			clear_feature_matrix_cache()

			matrix = get_feature_matrix_for_user(user=self.standard_user, refresh=True)
			self.assertIsNotNone(matrix["plan"])
			self.assertFalse(matrix["plan"]["is_active"])
		finally:
			plan_doc.is_active = original_state
			plan_doc.save(ignore_permissions=True)
			clear_subscription_context_cache()
			clear_feature_matrix_cache()

	def test_user_profile_summary(self) -> None:
		"""Profile endpoint returns company and permission details."""
		profile = get_user_profile(user=self.standard_user)

		self.assertEqual(profile["company"], self.company.name)
		self.assertTrue(profile["departments"])
		self.assertIn("plan_code", profile["subscription"])
		self.assertEqual(profile["subscription"]["plan_code"], "FOUNDATION")
		self.assertGreaterEqual(profile["permissions"]["total"], 0)
		self.assertIn("modules", profile["subscription"])
		module_keys = {module["key"] for module in profile["subscription"]["modules"]}
		self.assertIn("core", module_keys)

	# Helpers -----------------------------------------------------------------

	def _create_company(self, company_name: str, abbr: str, default_currency: str):
		existing = frappe.db.exists("Company", company_name)
		if existing:
			return frappe.get_doc("Company", existing)
		company = frappe.get_doc(
			{
				"doctype": "Company",
				"company_name": company_name,
				"abbr": abbr,
				"default_currency": default_currency,
			}
		)
		return company.insert(ignore_permissions=True)

	def _create_department(self, department_name: str, department_code: str, company: str):
		existing = frappe.db.exists(
			"Department",
			{"department_code": department_code, "company": company},
		)
		if existing:
			return frappe.get_doc("Department", existing)
		department = frappe.get_doc(
			{
				"doctype": "Department",
				"department_name": department_name,
				"department_code": department_code,
				"department_type": "Other",
				"company": company,
				"is_active": 1,
			}
		)
		return department.insert(ignore_permissions=True)

	def _create_tenant_branding(self, company: str, plan: str) -> None:
		existing = frappe.db.exists("Tenant Branding", company)
		if existing:
			branding = frappe.get_doc("Tenant Branding", existing)
			branding.plan = plan
			branding.save(ignore_permissions=True)
			return
		branding = frappe.get_doc(
			{
				"doctype": "Tenant Branding",
				"company": company,
				"plan": plan,
				"theme_name": "Default",
			}
		)
		branding.insert(ignore_permissions=True)

	def _ensure_role(self, role_name: str) -> None:
		if frappe.db.exists("Role", role_name):
			return
		role = frappe.get_doc({"doctype": "Role", "role_name": role_name})
		role.insert(ignore_permissions=True)

	def _create_user(
		self,
		email: str,
		first_name: str,
		*,
		roles: list[str],
		company: str | None = None,
		department: str | None = None,
	) -> str:
		existing = frappe.db.exists("User", email)
		if existing:
			return existing

		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": first_name,
				"send_welcome_email": 0,
				"time_zone": "UTC",
			}
		)
		for role in roles:
			user.append("roles", {"role": role})
		if company:
			user.company = company
		if department:
			user.append(
				"department_permissions",
				{"department": department, "can_read": 1, "can_write": 0},
			)
		user.insert(ignore_permissions=True)

		if department:
			user_doc = frappe.get_doc("User", email)
			user_doc.company = company
			user_doc.save(ignore_permissions=True)

		return email
