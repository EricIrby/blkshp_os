from __future__ import annotations

import frappe  # type: ignore[import]
from frappe.model.document import Document  # type: ignore[import]
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
			frappe.clear_cache(doctype="Recipe Allergen")
			frappe.reload_doc("recipes", "doctype", "recipe_allergen")
			frappe.clear_cache(doctype="Recipe Inherited Allergen")
			frappe.reload_doc("recipes", "doctype", "recipe_inherited_allergen")
			frappe.clear_cache(doctype="Allergen")
			frappe.reload_doc("recipes", "doctype", "allergen")
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

	def test_department_company_alignment_is_enforced(self) -> None:
		other_company = self._ensure_company("Recipe QA Alt Company")
		other_department = self._ensure_department("Recipe Alt Department", company=other_company)
		external_product = self._ensure_product(
			"Recipe Alt Product",
			other_department,
			company=other_company,
		)

		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Recipe",
					"recipe_name": "Mismatched Company Recipe",
					"department": other_department,
					"company": self.company,
					"yield_quantity": 1,
					"yield_unit": "each",
					"ingredients": [
						{
							"ingredient_type": "Product",
							"product": external_product,
							"quantity": 1,
							"unit": "each",
							"cost_per_unit": 1.0,
						}
					],
				}
			).insert(ignore_permissions=True)

	def test_product_ingredient_must_match_department(self) -> None:
		other_department = self._ensure_department("Recipe Alt Department 2")
		misaligned_product = self._ensure_product("Recipe Alt Product 2", other_department)

		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Recipe",
					"recipe_name": "Department Mismatch Recipe",
					"department": self.department,
					"company": self.company,
					"yield_quantity": 1,
					"yield_unit": "each",
					"ingredients": [
						{
							"ingredient_type": "Product",
							"product": misaligned_product,
							"quantity": 1,
							"unit": "each",
							"cost_per_unit": 1.0,
						}
					],
				}
			).insert(ignore_permissions=True)

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

	def test_duplicate_allergens_are_rejected(self) -> None:
		gluten = self._ensure_allergen("Gluten")

		with self.assertRaises(frappe.ValidationError):
			frappe.get_doc(
				{
					"doctype": "Recipe",
					"recipe_name": "Duplicate Allergen Test",
					"department": self.department,
					"company": self.company,
					"yield_quantity": 1,
					"yield_unit": "each",
					"ingredients": [
						{
							"ingredient_type": "Product",
							"product": self.product_a,
							"quantity": 1,
							"unit": "each",
							"cost_per_unit": 1.0,
						}
					],
					"allergens": [
						{"allergen": gluten},
						{"allergen": gluten},
					],
				}
			).insert(ignore_permissions=True)

	def test_allergens_inherit_from_subrecipes(self) -> None:
		gluten = self._ensure_allergen("Gluten")
		shellfish = self._ensure_allergen("Shellfish")
		output_product = self._ensure_product("Allergen Output Product", self.department)

		subrecipe = frappe.get_doc(
			{
				"doctype": "Recipe",
				"recipe_name": "Allergen Heavy Base",
				"recipe_type": "Prep",
				"is_prep_item": 1,
				"output_product": output_product,
				"department": self.department,
				"company": self.company,
				"yield_quantity": 1,
				"yield_unit": "each",
				"ingredients": [
					{
						"ingredient_type": "Product",
						"product": self.product_a,
						"quantity": 1,
						"unit": "each",
						"cost_per_unit": 1.0,
					}
				],
				"allergens": [
					{"allergen": gluten},
				],
			}
		).insert(ignore_permissions=True)

		parent = frappe.get_doc(
			{
				"doctype": "Recipe",
				"recipe_name": "Parent Recipe With Allergens",
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
				"allergens": [
					{"allergen": shellfish},
				],
			}
		).insert(ignore_permissions=True)

		self.assertIn(shellfish, {row.allergen for row in parent.allergens})
		inherited = {row.allergen for row in parent.inherited_allergens}
		self.assertIn(gluten, inherited)
		self.assertNotIn(shellfish, inherited)
		matching_row = next(
			row for row in parent.inherited_allergens if row.allergen == gluten
		)
		self.assertEqual(matching_row.source_recipes, subrecipe.name)

	def _create_basic_recipe(
		self,
		*,
		name: str,
		product: str,
		cost_per_unit: float,
		yield_quantity: float,
	) -> Document:
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

	def _ensure_department(self, name: str, *, company: str | None = None) -> str:
		existing = frappe.db.exists("Department", {"department_name": name})
		if existing:
			return existing

		target_company = company or self.company
		doc = frappe.get_doc(
			{
				"doctype": "Department",
				"department_name": name,
				"department_code": "".join(part[0] for part in name.split() if part).upper()[:8]
				or "DEPT",
				"department_type": "Food",
				"company": target_company,
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

	def _ensure_product(self, name: str, department: str, *, company: str | None = None) -> str:
		existing = frappe.db.exists("Product", {"product_name": name})
		if existing:
			return existing

		target_company = company or self.company
		doc = frappe.get_doc(
			{
				"doctype": "Product",
				"product_name": name,
				"primary_count_unit": "each",
				"default_department": department,
				"company": target_company,
				"volume_conversion_unit": "ml",
				"volume_conversion_factor": 1,
				"weight_conversion_unit": "g",
				"weight_conversion_factor": 1,
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

	def _ensure_allergen(self, name: str) -> str:
		existing = frappe.db.exists("Allergen", name)
		if existing:
			return existing

		doc = frappe.get_doc(
			{
				"doctype": "Allergen",
				"allergen_name": name,
				"allergen_code": "".join(part[0] for part in name.split() if part).upper()[:8]
				or name[:8].upper(),
			}
		)
		doc.insert(ignore_permissions=True)
		return doc.name

