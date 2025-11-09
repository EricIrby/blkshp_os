from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]

from blkshp_os.inventory.doctype.inventory_balance.inventory_balance import (
	InventoryBalance,
)


class TestRecipeBatch(FrappeTestCase):
	"""Validate recipe batch production flows."""

	_is_reloaded = False

	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		if not cls._is_reloaded:
			frappe.clear_cache(doctype="Recipe Batch Ingredient")
			frappe.reload_doc("recipes", "doctype", "recipe_batch_ingredient")
			frappe.clear_cache(doctype="Recipe Batch")
			frappe.reload_doc("recipes", "doctype", "recipe_batch")
			frappe.clear_cache(doctype="Recipe")
			frappe.reload_doc("recipes", "doctype", "recipe")
			frappe.clear_cache(doctype="Recipe Ingredient")
			frappe.reload_doc("recipes", "doctype", "recipe_ingredient")
			frappe.clear_cache(doctype="Inventory Balance")
			frappe.reload_doc("inventory", "doctype", "inventory_balance")
			cls._is_reloaded = True

	def setUp(self) -> None:
		super().setUp()
		self.company = self._ensure_company()
		self.department = self._ensure_department("Batch QA Department")
		self.raw_product = self._ensure_product("Batch Raw Product", self.department)
		self.output_product = self._ensure_product(
			"Batch Output Product", self.department, is_prep=True
		)
		self.recipe = self._ensure_recipe()
		InventoryBalance.update_for(
			self.raw_product,
			self.department,
			self.company,
			quantity=25,
		)
		InventoryBalance.update_for(
			self.output_product,
			self.department,
			self.company,
			quantity=5,
		)

	def tearDown(self) -> None:
		frappe.db.rollback()
		super().tearDown()

	def test_submit_batch_updates_inventory(self) -> None:
		batch = frappe.get_doc(
			{
				"doctype": "Recipe Batch",
				"recipe": self.recipe.name,
				"department": self.department,
				"company": self.company,
				"produced_quantity": 8,
				"produced_unit": "each",
			}
		).insert(ignore_permissions=True)

		# Sanity check that ingredient table is populated and metrics computed.
		self.assertEqual(len(batch.ingredients), 1)
		row = batch.ingredients[0]
		self.assertGreater(row.expected_base_quantity, 0)
		self.assertAlmostEqual(row.variance, 0)

		batch.submit()

		raw_balance = frappe.get_doc(
			"Inventory Balance",
			f"{self.raw_product}-{self.department}-{self.company}",
		)
		self.assertAlmostEqual(raw_balance.quantity, 25 - 4)  # 2 each per yield (4 * 2 = 8 units -> primary 4)

		output_balance = frappe.get_doc(
			"Inventory Balance",
			f"{self.output_product}-{self.department}-{self.company}",
		)
		self.assertAlmostEqual(output_balance.quantity, 5 + 8)

	def test_overridden_usage_adjusts_variance(self) -> None:
		batch = frappe.get_doc(
			{
				"doctype": "Recipe Batch",
				"recipe": self.recipe.name,
				"department": self.department,
				"company": self.company,
				"produced_quantity": 4,
				"produced_unit": "each",
			}
		)
		batch.insert(ignore_permissions=True)

		# Override actual usage before submit.
		row = batch.ingredients[0]
		row.quantity_used = 5
		batch.save(ignore_permissions=True)

		self.assertGreater(row.variance, 0)

		batch.submit()

		raw_balance = frappe.get_doc(
			"Inventory Balance",
			f"{self.raw_product}-{self.department}-{self.company}",
		)
		self.assertAlmostEqual(raw_balance.quantity, 25 - 5)

		output_balance = frappe.get_doc(
			"Inventory Balance",
			f"{self.output_product}-{self.department}-{self.company}",
		)
		self.assertAlmostEqual(output_balance.quantity, 5 + 4)

	# ------------------------------------------------------------------
	# Fixture helpers
	# ------------------------------------------------------------------
	def _ensure_company(self, name: str = "Batch QA Company") -> str:
		existing = frappe.db.exists("Company", {"company_name": name})
		if existing:
			return existing

		doc = frappe.get_doc(
			{
				"doctype": "Company",
				"company_name": name,
				"company_code": "".join(part[0] for part in name.split() if part).upper()[:8]
				or "COMP",
				"default_currency": "USD",
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

	def _ensure_department(self, name: str) -> str:
		existing = frappe.db.exists("Department", {"department_name": name})
		if existing:
			return existing

		doc = frappe.get_doc(
			{
				"doctype": "Department",
				"department_name": name,
				"department_code": "".join(part[0] for part in name.split() if part).upper()[:8]
				or "DEPT",
				"department_type": "Food",
				"company": self.company,
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

	def _ensure_product(self, name: str, department: str, *, is_prep: bool = False) -> str:
		existing = frappe.db.exists("Product", {"product_name": name})
		if existing:
			return existing

		doc = frappe.get_doc(
			{
				"doctype": "Product",
				"product_name": name,
				"primary_count_unit": "each",
				"default_department": department,
				"company": self.company,
				"prep_item": 1 if is_prep else 0,
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

	def _ensure_recipe(self):
		existing = frappe.db.exists("Recipe", {"recipe_name": "Batch Prep"})
		if existing:
			return frappe.get_doc("Recipe", existing)

		recipe = frappe.get_doc(
			{
				"doctype": "Recipe",
				"recipe_name": "Batch Prep",
				"recipe_type": "Prep",
				"is_prep_item": 1,
				"department": self.department,
				"company": self.company,
				"yield_quantity": 4,
				"yield_unit": "each",
				"output_product": self.output_product,
				"ingredients": [
					{
						"ingredient_type": "Product",
						"product": self.raw_product,
						"quantity": 2,
						"unit": "each",
						"cost_per_unit": 1.0,
					}
				],
			}
		)
		recipe.insert(ignore_permissions=True)
		return recipe


