from __future__ import annotations

from collections import defaultdict

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
        self._ensure_output_product()
        self._ensure_unique_code()
        self._ensure_no_self_reference()
        self._ensure_positive_yield()
        self._ensure_ingredient_company_alignment()
        self._refresh_allergens()
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

        dept_info = frappe.db.get_value(
            "Department",
            self.department,
            ["company"],
            as_dict=True,
        )
        if not dept_info:
            frappe.throw(_("Department {0} does not exist.").format(self.department))

        dept_company = (dept_info.get("company") or "").strip()
        if not dept_company:
            frappe.throw(
                _(
                    "Department {0} must be linked to a company before recipes can reference it."
                ).format(self.department)
            )

        if self.company and self.company != dept_company:
            frappe.throw(
                _("Recipe company {0} must match the department's company {1}.").format(
                    self.company,
                    dept_company,
                )
            )

        self.company = self.company or dept_company

    def _ensure_output_product(self) -> None:
        if self.is_prep_item or (self.recipe_type or "").lower() == "prep":
            if not self.output_product:
                frappe.throw(_("Prep recipes require an output product."))

        if self.output_product:
            product_department = frappe.db.get_value(
                "Product", self.output_product, "default_department"
            )
            if (
                product_department
                and self.department
                and product_department != self.department
            ):
                frappe.throw(
                    _(
                        "Output product {0} belongs to department {1}, which does not match recipe department {2}."
                    ).format(
                        self.output_product,
                        product_department,
                        self.department,
                    )
                )

            product_company = frappe.db.get_value(
                "Product", self.output_product, "company"
            )
            if product_company and self.company and product_company != self.company:
                frappe.throw(
                    _(
                        "Output product {0} belongs to company {1}, which does not match recipe company {2}."
                    ).format(
                        self.output_product,
                        product_company,
                        self.company,
                    )
                )

    def _ensure_positive_yield(self) -> None:
        if (self.yield_quantity or 0) <= 0:
            frappe.throw(_("Yield quantity must be greater than zero."))

    def _ensure_ingredients_present(self) -> None:
        if not self.ingredients:
            frappe.throw(_("Add at least one ingredient to the recipe."))

    def _ensure_ingredient_company_alignment(self) -> None:
        if not self.company:
            return

        for row in self.ingredients or []:
            if row.ingredient_type == "Product" and row.product:
                product_info = frappe.db.get_value(
                    "Product",
                    row.product,
                    ["company", "default_department"],
                    as_dict=True,
                )
                if product_info:
                    if product_info.company and product_info.company != self.company:
                        frappe.throw(
                            _(
                                "Product {0} belongs to company {1}, which does not match recipe company {2}."
                            ).format(
                                row.product,
                                product_info.company,
                                self.company,
                            )
                        )
                    if (
                        product_info.default_department
                        and product_info.default_department != self.department
                    ):
                        frappe.throw(
                            _(
                                "Product {0} is assigned to department {1}, which does not match recipe department {2}."
                            ).format(
                                row.product,
                                product_info.default_department,
                                self.department,
                            )
                        )
            if row.ingredient_type == "Recipe" and row.subrecipe:
                subrecipe_info = frappe.db.get_value(
                    "Recipe",
                    row.subrecipe,
                    ["company", "department"],
                    as_dict=True,
                )
                if subrecipe_info:
                    if (
                        subrecipe_info.company
                        and subrecipe_info.company != self.company
                    ):
                        frappe.throw(
                            _(
                                "Subrecipe {0} belongs to company {1}, which does not match recipe company {2}."
                            ).format(
                                row.subrecipe,
                                subrecipe_info.company,
                                self.company,
                            )
                        )
                    if (
                        subrecipe_info.department
                        and subrecipe_info.department != self.department
                    ):
                        frappe.throw(
                            _(
                                "Subrecipe {0} is assigned to department {1}, which does not match recipe department {2}."
                            ).format(
                                row.subrecipe,
                                subrecipe_info.department,
                                self.department,
                            )
                        )

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
            row.base_quantity = float(
                product_doc.convert_to_primary_unit(unit, quantity)
            )

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
                    _(
                        "Subrecipe {0} must have a positive yield to be used as an ingredient."
                    ).format(subrecipe.recipe_name or subrecipe.name)
                )
            row.base_quantity = quantity
            row.cost_per_unit = subrecipe.cost_per_unit or 0.0
            return quantity * row.cost_per_unit

        frappe.throw(_("Invalid ingredient type {0}.").format(row.ingredient_type))
        return 0.0

    def _refresh_allergens(self) -> None:
        manual_allergens: set[str] = set()
        duplicate_entries: set[str] = set()

        for row in self.allergens or []:
            if not row.allergen:
                continue
            if row.allergen in manual_allergens:
                duplicate_entries.add(row.allergen)
            manual_allergens.add(row.allergen)

        if duplicate_entries:
            frappe.throw(
                _("Allergens cannot be duplicated: {0}.").format(
                    ", ".join(sorted(duplicate_entries))
                )
            )

        inherited_map: defaultdict[str, set[str]] = defaultdict(set)
        visited: set[str] = set(filter(None, [self.name]))

        for ingredient in self.ingredients or []:
            if ingredient.ingredient_type != "Recipe" or not ingredient.subrecipe:
                continue
            sub_allergens = self._collect_allergens_from_recipe(
                ingredient.subrecipe,
                visited.copy(),
            )
            for allergen in sub_allergens:
                if allergen not in manual_allergens:
                    inherited_map[allergen].add(ingredient.subrecipe)

        self.set("inherited_allergens", [])
        for allergen in sorted(inherited_map):
            self.append(
                "inherited_allergens",
                {
                    "allergen": allergen,
                    "source_recipes": ", ".join(sorted(inherited_map[allergen])),
                },
            )

    def _collect_allergens_from_recipe(
        self, recipe_name: str, visited: set[str]
    ) -> set[str]:
        if recipe_name in visited:
            return set()

        visited.add(recipe_name)
        recipe_doc = frappe.get_cached_doc("Recipe", recipe_name)

        manual = {
            row.allergen
            for row in recipe_doc.get("allergens") or []
            if getattr(row, "allergen", None)
        }
        aggregated = set(manual)

        for ingredient in recipe_doc.get("ingredients") or []:
            if ingredient.ingredient_type == "Recipe" and ingredient.subrecipe:
                aggregated |= self._collect_allergens_from_recipe(
                    ingredient.subrecipe,
                    visited.copy(),
                )

        return aggregated

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
                parent_recipe._refresh_allergens()
                parent_recipe.save(ignore_permissions=True)
        finally:
            frappe.flags._updating_recipe_parents = False  # type: ignore[attr-defined]
