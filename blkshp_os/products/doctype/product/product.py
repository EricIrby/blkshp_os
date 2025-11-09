import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname

VOLUME_TO_ML = {
    "ml": 1,
    "milliliter": 1,
    "l": 1000,
    "liter": 1000,
    "litre": 1000,
    "fl oz": 29.5735,
    "fluid ounce": 29.5735,
    "pint": 473.176,
    "quart": 946.353,
    "gallon": 3785.41,
}

WEIGHT_TO_G = {
    "g": 1,
    "gram": 1,
    "kg": 1000,
    "kilogram": 1000,
    "oz": 28.3495,
    "ounce": 28.3495,
    "lb": 453.592,
    "pound": 453.592,
}


class Product(Document):
    """Unified product master."""

    def before_insert(self):
        if not self.product_code:
            self.product_code = self._generate_product_code()

    def validate(self):
        self._ensure_unique_product_code()
        self._validate_conversion_factors()
        self._ensure_default_department_in_allocations()
        self._validate_property_combinations()

    # -------------------------------------------------------------------------
    # Public helpers
    # -------------------------------------------------------------------------
    def get_available_count_units(self):
        units = set()
        if self.primary_count_unit:
            units.add(self.primary_count_unit.lower())

        if self.volume_conversion_unit:
            units.add(self.volume_conversion_unit.lower())
            units.update(VOLUME_TO_ML.keys())

        if self.weight_conversion_unit:
            units.add(self.weight_conversion_unit.lower())
            units.update(WEIGHT_TO_G.keys())

        for row in self.purchase_units or []:
            if row.purchase_unit:
                units.add(row.purchase_unit.lower())

        return sorted(units)

    def convert_to_primary_unit(self, from_unit, quantity):
        from_unit = (from_unit or "").lower()
        if self.primary_count_unit and from_unit == self.primary_count_unit.lower():
            return quantity

        qty = self._convert_from_purchase_unit(from_unit, quantity)
        if qty is not None:
            return qty

        qty = self._convert_from_volume_unit(from_unit, quantity)
        if qty is not None:
            return qty

        qty = self._convert_from_weight_unit(from_unit, quantity)
        if qty is not None:
            return qty

        frappe.throw(
            _("Cannot convert from unit {0} for product {1}.").format(
                from_unit or _("(empty)"), self.name
            )
        )

    def convert_from_primary_unit(self, to_unit, quantity):
        to_unit = (to_unit or "").lower()
        if self.primary_count_unit and to_unit == self.primary_count_unit.lower():
            return quantity

        qty = self._convert_to_purchase_unit(to_unit, quantity)
        if qty is not None:
            return qty

        qty = self._convert_to_volume_unit(to_unit, quantity)
        if qty is not None:
            return qty

        qty = self._convert_to_weight_unit(to_unit, quantity)
        if qty is not None:
            return qty

        frappe.throw(
            _("Cannot convert to unit {0} for product {1}.").format(
                to_unit or _("(empty)"), self.name
            )
        )

    def convert_between_units(self, from_unit, to_unit, quantity):
        primary_qty = self.convert_to_primary_unit(from_unit, quantity)
        return self.convert_from_primary_unit(to_unit, primary_qty)

    def get_departments(self, active_only=True):
        allocations = self.departments or []
        if active_only:
            allocations = [row for row in allocations if row.department]
        return [row.department for row in allocations if row.department]

    def assign_to_department(self, department, is_primary=False):
        original_department = department
        department = frappe.db.get_value("Department", department)
        if not department:
            frappe.throw(_("Department {0} does not exist.").format(original_department))

        existing = {row.department for row in self.departments or []}
        if department in existing:
            return

        self.append(
            "departments",
            {
                "department": department,
                "is_primary": 1 if is_primary else 0,
            },
        )

    # -------------------------------------------------------------------------
    # Internal helpers
    # -------------------------------------------------------------------------
    def _generate_product_code(self):
        series = "PROD-.#####"
        return make_autoname(series)

    def _ensure_unique_product_code(self):
        if not self.product_code:
            return

        filters = {
            "name": ["!=", self.name],
            "product_code": self.product_code,
        }
        if self.company:
            filters["company"] = self.company

        if frappe.db.exists("Product", filters):
            frappe.throw(
                _("Product code {0} is already used in company {1}.").format(
                    self.product_code, self.company or _("(any)")
                ),
                frappe.UniqueValidationError,
            )

    def _validate_conversion_factors(self):
        if self.volume_conversion_unit and not self.volume_conversion_factor:
            frappe.throw(_("Volume conversion factor is required when a volume unit is set."))
        if self.volume_conversion_factor and self.volume_conversion_factor <= 0:
            frappe.throw(_("Volume conversion factor must be greater than zero."))

        if self.weight_conversion_unit and not self.weight_conversion_factor:
            frappe.throw(_("Weight conversion factor is required when a weight unit is set."))
        if self.weight_conversion_factor and self.weight_conversion_factor <= 0:
            frappe.throw(_("Weight conversion factor must be greater than zero."))

        for row in self.purchase_units or []:
            if not row.conversion_to_primary_cu or row.conversion_to_primary_cu <= 0:
                frappe.throw(
                    _("Conversion to primary count unit must be greater than zero for purchase unit {0}.").format(
                        row.purchase_unit or row.vendor or row.name
                    )
                )

    def _ensure_default_department_in_allocations(self):
        if not self.default_department:
            return
        departments = {row.department for row in self.departments or []}
        if self.default_department not in departments:
            self.append(
                "departments",
                {
                    "department": self.default_department,
                    "is_primary": 1,
                },
            )
        else:
            # ensure only one primary per product
            for row in self.departments:
                row.is_primary = 1 if row.department == self.default_department else 0

    def _validate_property_combinations(self):
        if self.is_generic and self.is_prep_item:
            frappe.throw(_("Product cannot be both generic and a prep item."))

    def _convert_from_purchase_unit(self, from_unit, quantity):
        for row in self.purchase_units or []:
            if not row.purchase_unit:
                continue
            if row.purchase_unit.lower() == from_unit:
                return quantity * row.conversion_to_primary_cu
            if row.name and row.name.lower() == from_unit:
                return quantity * row.conversion_to_primary_cu
        return None

    def _convert_from_volume_unit(self, from_unit, quantity):
        if not self.volume_conversion_unit:
            return None

        base_unit = self.volume_conversion_unit.lower()
        if from_unit == base_unit:
            return quantity / self.volume_conversion_factor

        qty_in_base = self._convert_standard_volume(quantity, from_unit, base_unit)
        if qty_in_base is None:
            return None
        return qty_in_base / self.volume_conversion_factor

    def _convert_from_weight_unit(self, from_unit, quantity):
        if not self.weight_conversion_unit:
            return None

        base_unit = self.weight_conversion_unit.lower()
        if from_unit == base_unit:
            return quantity / self.weight_conversion_factor

        qty_in_base = self._convert_standard_weight(quantity, from_unit, base_unit)
        if qty_in_base is None:
            return None
        return qty_in_base / self.weight_conversion_factor

    def _convert_to_purchase_unit(self, to_unit, quantity):
        for row in self.purchase_units or []:
            if not row.purchase_unit:
                continue
            if row.purchase_unit.lower() == to_unit:
                return quantity / row.conversion_to_primary_cu
            if row.name and row.name.lower() == to_unit:
                return quantity / row.conversion_to_primary_cu
        return None

    def _convert_to_volume_unit(self, to_unit, quantity):
        if not self.volume_conversion_unit:
            return None

        base_unit = self.volume_conversion_unit.lower()
        if to_unit == base_unit:
            return quantity * self.volume_conversion_factor

        qty_in_base = quantity * self.volume_conversion_factor
        converted = self._convert_standard_volume(qty_in_base, base_unit, to_unit)
        return converted

    def _convert_to_weight_unit(self, to_unit, quantity):
        if not self.weight_conversion_unit:
            return None

        base_unit = self.weight_conversion_unit.lower()
        if to_unit == base_unit:
            return quantity * self.weight_conversion_factor

        qty_in_base = quantity * self.weight_conversion_factor
        converted = self._convert_standard_weight(qty_in_base, base_unit, to_unit)
        return converted

    def _convert_standard_volume(self, quantity, from_unit, to_unit):
        if from_unit not in VOLUME_TO_ML or to_unit not in VOLUME_TO_ML:
            return None
        ml = quantity * VOLUME_TO_ML[from_unit]
        return ml / VOLUME_TO_ML[to_unit]

    def _convert_standard_weight(self, quantity, from_unit, to_unit):
        if from_unit not in WEIGHT_TO_G or to_unit not in WEIGHT_TO_G:
            return None
        grams = quantity * WEIGHT_TO_G[from_unit]
        return grams / WEIGHT_TO_G[to_unit]

