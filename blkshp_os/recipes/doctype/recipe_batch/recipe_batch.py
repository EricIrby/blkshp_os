from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.inventory.doctype.inventory_balance.inventory_balance import (
	InventoryBalance,
)


@dataclass(slots=True)
class _RecipeRow:
	name: str
	ingredient_type: str
	product: str | None
	subrecipe: str | None
	quantity: float
	unit: str | None
	base_quantity: float | None


class RecipeBatch(Document):
	"""Represents a production run of a recipe."""

	def validate(self) -> None:
		recipe = self._load_recipe()
		self._apply_defaults_from_recipe(recipe)
		self._ensure_recipe_yield(recipe)
		self._ensure_produced_quantity()
		self._synchronise_ingredients(recipe)
		self._recalculate_ingredient_metrics(recipe)

	def on_submit(self) -> None:
		self._post_inventory_movements()

	# ------------------------------------------------------------------
	# Internal helpers
	# ------------------------------------------------------------------
	def _load_recipe(self):
		if not self.recipe:
			frappe.throw(_("Select a recipe before saving the batch."))
		return frappe.get_doc("Recipe", self.recipe)

	def _apply_defaults_from_recipe(self, recipe) -> None:
		if not self.department:
			self.department = recipe.department
		if not self.company:
			self.company = recipe.company or frappe.db.get_value(
				"Department", self.department, "company"
			)
		if not self.company:
			frappe.throw(_("Company is required for recipe batches."))

		if not self.produced_unit:
			self.produced_unit = recipe.yield_unit or self._get_output_product_primary_unit(
				recipe
			)

	def _ensure_recipe_yield(self, recipe) -> None:
		yield_quantity = recipe.yield_quantity or 0
		if yield_quantity <= 0:
			frappe.throw(_("Recipe {0} must have a positive yield before batching.").format(recipe.name))
		if recipe.is_prep_item and not recipe.output_product:
			frappe.throw(_("Recipe {0} must define an output product to create batches.").format(recipe.name))

	def _ensure_produced_quantity(self) -> None:
		if (self.produced_quantity or 0) <= 0:
			frappe.throw(_("Produced quantity must be greater than zero."))

	def _synchronise_ingredients(self, recipe) -> None:
		existing_overrides = {
			row.source_rowname: (row.quantity_used, row.unit)
			for row in self.ingredients or []
			if getattr(row, "source_rowname", None)
		}

		self.set("ingredients", [])
		for recipe_row in self._iter_recipe_rows(recipe):
			row = self.append(
				"ingredients",
				{
					"ingredient_type": recipe_row.ingredient_type,
					"product": recipe_row.product,
					"subrecipe": recipe_row.subrecipe,
					"source_rowname": recipe_row.name,
				},
			)

			quantity_override, unit_override = existing_overrides.get(
				recipe_row.name, (None, None)
			)
			if quantity_override is None:
				scale = self._production_scale(recipe)
				row.quantity_used = recipe_row.quantity * scale
			else:
				row.quantity_used = quantity_override

			row.unit = unit_override or recipe_row.unit

	def _recalculate_ingredient_metrics(self, recipe) -> None:
		scale = self._production_scale(recipe)
		recipe_rows = {row.name: row for row in self._iter_recipe_rows(recipe)}

		for row in self.ingredients or []:
			source_row = recipe_rows.get(row.source_rowname)
			if not source_row:
				frappe.throw(
					_("Unable to match batch ingredient row to recipe definition.")
				)

			expected_qty_primary = self._convert_row_to_primary_units(
				source_row, source_row.quantity * scale, source_row.unit
			)
			actual_qty_primary = self._convert_row_to_primary_units(
				source_row, row.quantity_used, row.unit
			)

			row.expected_base_quantity = expected_qty_primary
			row.base_quantity_used = actual_qty_primary
			row.variance = (row.base_quantity_used or 0) - (row.expected_base_quantity or 0)

	def _production_scale(self, recipe) -> float:
		yield_quantity = recipe.yield_quantity or 1.0
		return float(self.produced_quantity or 0) / float(yield_quantity)

	def _convert_row_to_primary_units(
		self, recipe_row: _RecipeRow, quantity: float | None, unit: str | None
	) -> float:
		quantity = float(quantity or 0)
		if quantity == 0:
			return 0.0

		if recipe_row.ingredient_type == "Product":
			return self._convert_product_quantity(recipe_row.product, quantity, unit)

		if recipe_row.ingredient_type == "Recipe":
			if not recipe_row.subrecipe:
				frappe.throw(_("Subrecipe row is missing a reference to the recipe."))
			subrecipe = frappe.get_doc("Recipe", recipe_row.subrecipe)
			if not subrecipe.output_product:
				frappe.throw(
					_("Subrecipe {0} requires an output product before it can be consumed.").format(
						subrecipe.name
					)
				)
			conversion_unit = unit or subrecipe.yield_unit or self._get_output_product_primary_unit(
				subrecipe
			)
			return self._convert_product_quantity(
				subrecipe.output_product, quantity, conversion_unit
			)

		frappe.throw(_("Unsupported ingredient type: {0}").format(recipe_row.ingredient_type))
		return 0.0

	def _convert_product_quantity(
		self, product: str | None, quantity: float, unit: str | None
	) -> float:
		"""Convert product quantity to primary unit using centralized conversion service."""
		from blkshp_os.products import conversion

		if not product:
			frappe.throw(_("Product is required for product ingredients."))

		product_doc = frappe.get_doc("Product", product)
		target_unit = unit or product_doc.primary_count_unit
		return float(conversion.convert_to_primary_unit(product, target_unit, quantity))

	def _get_output_product_primary_unit(self, recipe) -> str:
		if not recipe.output_product:
			return ""
		product_doc = frappe.get_doc("Product", recipe.output_product)
		return product_doc.primary_count_unit or ""

	def _iter_recipe_rows(self, recipe) -> Iterable[_RecipeRow]:
		for row in recipe.ingredients or []:
			yield _RecipeRow(
				name=row.name,
				ingredient_type=row.ingredient_type,
				product=getattr(row, "product", None),
				subrecipe=getattr(row, "subrecipe", None),
				quantity=float(getattr(row, "quantity", 0) or 0),
				unit=getattr(row, "unit", None),
				base_quantity=float(getattr(row, "base_quantity", 0) or 0),
			)

	def _post_inventory_movements(self) -> None:
		recipe = self._load_recipe()
		recipe_rows = {row.name: row for row in self._iter_recipe_rows(recipe)}

		for row in self.ingredients or []:
			source_row = recipe_rows.get(row.source_rowname)
			if not source_row:
				continue

			target_product, quantity_primary = self._resolve_target_product_and_quantity(
				source_row, row.quantity_used, row.unit
			)
			if quantity_primary:
				InventoryBalance.apply_delta(
					target_product,
					self.department,
					self.company,
					-quantity_primary,
				)

		if recipe.output_product:
			produced_quantity_primary = self._convert_product_quantity(
				recipe.output_product,
				float(self.produced_quantity or 0),
				self.produced_unit or recipe.yield_unit,
			)
			if produced_quantity_primary:
				InventoryBalance.apply_delta(
					recipe.output_product,
					self.department,
					self.company,
					produced_quantity_primary,
				)

	def _resolve_target_product_and_quantity(
		self, recipe_row: _RecipeRow, quantity: float | None, unit: str | None
	) -> tuple[str, float]:
		if recipe_row.ingredient_type == "Product":
			product = recipe_row.product
			quantity_primary = self._convert_product_quantity(product, float(quantity or 0), unit or recipe_row.unit)
			return product or "", quantity_primary

		if recipe_row.ingredient_type == "Recipe":
			if not recipe_row.subrecipe:
				frappe.throw(_("Subrecipe row is missing a recipe reference."))
			subrecipe = frappe.get_doc("Recipe", recipe_row.subrecipe)
			if not subrecipe.output_product:
				frappe.throw(
					_("Subrecipe {0} must define an output product before batching.").format(
						subrecipe.name
					)
				)
			conversion_unit = unit or recipe_row.unit or subrecipe.yield_unit
			quantity_primary = self._convert_product_quantity(
				subrecipe.output_product,
				float(quantity or 0),
				conversion_unit,
			)
			return subrecipe.output_product, quantity_primary

		frappe.throw(_("Unsupported ingredient type for batching: {0}").format(recipe_row.ingredient_type))
		return "", 0.0


