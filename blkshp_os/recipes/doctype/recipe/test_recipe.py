from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]


class TestRecipe(FrappeTestCase):
	"""Recipe costing and dependency refresh tests."""

	_is_reloaded = False

	@classmethod
	def setUpClass(cls) -> None:
		super().setUpClass()
		if not cls._is_reloaded:
			frappe.clear_cache(doctype="Recipe Ingredient")
			frappe.reload_doc("recipes", "doctype", "recipe_ingredient")
			frappe.clear_cache(doctype="Recipe")
			frappe.reload_doc("recipes", "doctype", "recipe")
			cls._is_reloaded = True

	def setUp(self) -> None:
		super().setUp()
		self.company = self._ensure_company()
		self.department = self._ensure_department("Recipe QA Department")
		self.product_a = self._ensure_product("Recipe Product A", self.department)
		self.product_b = self._ensure_product("Recipe Product B", self.department)

	def tearDown(self) -> None:
		frappe.db.rollback()
		super().tearDown()

	def test_product_ingredient_costing(self) -> None:
		recipe = frappe.get_doc(
			{
				"doctype": "Recipe",
				"recipe_name": "House Salsa",
				"department": self.department,
				"company": self.company,
				"yield_quantity": 4,
				"yield_unit": "each",
				"ingredients": [
					{
						"ingredient_type": "Product",
						"product": self.product_a,
						"quantity": 2,
						"unit": "each",
						"cost_per_unit": 1.5,
					},
					{
						"ingredient_type": "Product",
						"product": self.product_b,
						"quantity": 1,
						"unit": "each",
						"cost_per_unit": 2.25,
					},
				],
			}
		).insert(ignore_permissions=True)

		self.assertGreater(recipe.cost_per_unit, 0)
		self.assertAlmostEqual(recipe.total_cost, 5.25)
		self.assertAlmostEqual(recipe.cost_per_unit, 1.3125)
		self.assertAlmostEqual(recipe.ingredients[0].cost_total, 3.0)
		self.assertAlmostEqual(recipe.ingredients[1].cost_total, 2.25)

	def test_subrecipe_cost_is_applied(self) -> None:
		subrecipe = self._create_basic_recipe(
			name="Guacamole Base",
			product=self.product_a,
			cost_per_unit=2.0,
			yield_quantity=1,
		)

		parent = frappe.get_doc(
			{
				"doctype": "Recipe",
				"recipe_name": "Guacamole Bowl",
				"department": self.department,
				"company": self.company,
				"yield_quantity": 2,
				"yield_unit": "each",
				"ingredients": [
					{
						"ingredient_type": "Recipe",
						"subrecipe": subrecipe.name,
						"quantity": 2,
					}
				],
			}
		).insert(ignore_permissions=True)

		self.assertAlmostEqual(parent.total_cost, 4.0)
		self.assertAlmostEqual(parent.cost_per_unit, 2.0)

	def test_updating_subrecipe_refreshes_parent_cost(self) -> None:
		subrecipe = self._create_basic_recipe(
			name="Simple Syrup",
			product=self.product_a,
			cost_per_unit=0.5,
			yield_quantity=1,
		)

		parent = frappe.get_doc(
			{
				"doctype": "Recipe",
				"recipe_name": "Old Fashioned",
				"department": self.department,
				"company": self.company,
				"yield_quantity": 1,
				"yield_unit": "each",
				"ingredients": [
					{
						"ingredient_type": "Recipe",
						"subrecipe": subrecipe.name,
						"quantity": 1,
					}
				],
			}
		).insert(ignore_permissions=True)

		self.assertAlmostEqual(parent.cost_per_unit, 0.5)
		rows = frappe.get_all(
			"Recipe Ingredient",
			filters={"parent": parent.name},
			fields=["ingredient_type", "subrecipe"],
		)
		self.assertTrue(any(row.subrecipe == subrecipe.name for row in rows))

		# Increase subrecipe cost and save, verifying the parent is updated automatically.
		subrecipe.ingredients[0].cost_per_unit = 0.75
		subrecipe.save(ignore_permissions=True)

		frappe.clear_document_cache("Recipe", parent.name)
		updated_cost = frappe.db.get_value("Recipe", parent.name, "cost_per_unit")
		self.assertAlmostEqual(updated_cost, 0.75)
		parent = frappe.get_doc("Recipe", parent.name)
		self.assertAlmostEqual(parent.cost_per_unit, 0.75)

	def _create_basic_recipe(
		self,
		*,
		name: str,
		product: str,
		cost_per_unit: float,
		yield_quantity: float,
	) -> frappe.model.document.Document:
		return frappe.get_doc(
			{
				"doctype": "Recipe",
				"recipe_name": name,
				"department": self.department,
				"company": self.company,
				"yield_quantity": yield_quantity,
				"yield_unit": "each",
				"ingredients": [
					{
						"ingredient_type": "Product",
						"product": product,
						"quantity": yield_quantity,
						"unit": "each",
						"cost_per_unit": cost_per_unit,
					}
				],
			}
		).insert(ignore_permissions=True)

	def _ensure_company(self, name: str = "Recipe QA Company") -> str:
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

	def _ensure_product(self, name: str, department: str) -> str:
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
				"volume_conversion_unit": "ml",
				"volume_conversion_factor": 1,
				"weight_conversion_unit": "g",
				"weight_conversion_factor": 1,
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

