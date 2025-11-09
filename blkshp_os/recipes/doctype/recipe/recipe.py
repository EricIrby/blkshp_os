from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname


class Recipe(Document):
	"""Recipe master with automatic costing."""

	_SERIES = "RECIPE-.#####"

	def autoname(self) -> None:
		if not self.recipe_code:
			self.recipe_code = self._generate_code()
		self.name = self.recipe_code

	def validate(self) -> None:
		self._ensure_department()
		self._ensure_ingredients_present()
		self._ensure_unique_code()
		self._ensure_no_self_reference()
		self._ensure_positive_yield()
		self._calculate_costs()

	def after_save(self) -> None:
		self._update_parent_recipes()

	def on_update(self) -> None:
		self._update_parent_recipes()

	# -------------------------------------------------------------------------
	# Internal helpers
	# -------------------------------------------------------------------------
	def _generate_code(self) -> str:
		return make_autoname(self._SERIES)

	def _ensure_department(self) -> None:
		if not self.department:
			frappe.throw(_("Recipes must be assigned to a department."))

	def _ensure_positive_yield(self) -> None:
		if (self.yield_quantity or 0) <= 0:
			frappe.throw(_("Yield quantity must be greater than zero."))

	def _ensure_ingredients_present(self) -> None:
		if not self.ingredients:
			frappe.throw(_("Add at least one ingredient to the recipe."))

	def _ensure_unique_code(self) -> None:
		if not self.recipe_code:
			return
		filters: dict[str, object] = {"recipe_code": self.recipe_code}
		if not self.is_new():
			filters["name"] = ["!=", self.name]
		if frappe.db.exists("Recipe", filters):
			frappe.throw(
				_("Recipe code {0} already exists.").format(self.recipe_code),
				frappe.UniqueValidationError,
			)

	def _ensure_no_self_reference(self) -> None:
		for row in self.ingredients or []:
			if row.ingredient_type == "Recipe" and row.subrecipe == self.name:
				frappe.throw(_("Recipe cannot include itself as a subrecipe."))

	def _calculate_costs(self) -> None:
		total_cost = 0.0
		for row in self.ingredients or []:
			row.cost_total = self._calculate_row_cost(row)
			total_cost += row.cost_total
		self.total_cost = total_cost
		yield_qty = self.yield_quantity or 0
		self.cost_per_unit = total_cost / yield_qty if yield_qty else 0.0

	def _calculate_row_cost(self, row: Document) -> float:
		row.base_quantity = 0.0
		quantity = row.quantity or 0.0

		if row.ingredient_type == "Product":
			if not row.product:
				frappe.throw(_("Select a product for product ingredients."))

			product_doc = frappe.get_doc("Product", row.product)
			unit = row.unit or product_doc.primary_count_unit or ""
			row.base_quantity = float(product_doc.convert_to_primary_unit(unit, quantity))

			if row.cost_per_unit is None:
				frappe.throw(
					_("Cost per unit is required for product ingredient {0}.").format(
						product_doc.product_name or product_doc.name
					)
				)
			return row.base_quantity * float(row.cost_per_unit)

		if row.ingredient_type == "Recipe":
			if not row.subrecipe:
				frappe.throw(_("Select a subrecipe for recipe ingredients."))

			subrecipe = frappe.get_doc("Recipe", row.subrecipe)
			subrecipe.reload()
			if (subrecipe.yield_quantity or 0) <= 0:
				frappe.throw(
					_("Subrecipe {0} must have a positive yield to be used as an ingredient.").format(
						subrecipe.recipe_name or subrecipe.name
					)
				)
			row.base_quantity = quantity
			row.cost_per_unit = subrecipe.cost_per_unit or 0.0
			return quantity * row.cost_per_unit

		frappe.throw(_("Invalid ingredient type {0}.").format(row.ingredient_type))
		return 0.0

	def _update_parent_recipes(self) -> None:
		if getattr(frappe.flags, "_updating_recipe_parents", False):
			return

		parent_names = frappe.get_all(
			"Recipe Ingredient",
			filters={
				"ingredient_type": "Recipe",
				"subrecipe": self.name,
				"parenttype": "Recipe",
			},
			pluck="parent",
		)
		if not parent_names:
			return

		frappe.flags._updating_recipe_parents = True  # type: ignore[attr-defined]
		try:
			for parent_name in parent_names:
				if parent_name == self.name:
					continue
				parent_recipe = frappe.get_doc("Recipe", parent_name)
				for row in parent_recipe.ingredients or []:
					if row.ingredient_type == "Recipe" and row.subrecipe == self.name:
						row.cost_per_unit = self.cost_per_unit or 0.0
						row.cost_total = (row.quantity or 0.0) * row.cost_per_unit
						if row.name:
							frappe.db.set_value(
								"Recipe Ingredient",
								row.name,
								{
									"cost_per_unit": row.cost_per_unit,
									"cost_total": row.cost_total,
								},
							)
				parent_recipe._calculate_costs()
				frappe.db.set_value(
					"Recipe",
					parent_recipe.name,
					{
						"total_cost": parent_recipe.total_cost,
						"cost_per_unit": parent_recipe.cost_per_unit,
					},
				)
		finally:
			frappe.flags._updating_recipe_parents = False  # type: ignore[attr-defined]

