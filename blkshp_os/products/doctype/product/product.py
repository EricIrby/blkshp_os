import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.naming import make_autoname

from blkshp_os.products import conversion


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
        self._validate_valuation_fields()
        self._set_default_valuation_method()

    # -------------------------------------------------------------------------
    # Public helpers
    # -------------------------------------------------------------------------
    def get_available_count_units(self):
        """Get all available count units for this product."""
        return conversion.get_available_count_units(self)

    def convert_to_primary_unit(self, from_unit, quantity):
        """Convert any unit to primary unit (hub conversion)."""
        return conversion.convert_to_primary_unit(self, from_unit, quantity)

    def convert_from_primary_unit(self, to_unit, quantity):
        """Convert from primary unit to any unit."""
        return conversion.convert_from_primary_unit(self, to_unit, quantity)

    def convert_between_units(self, from_unit, to_unit, quantity):
        """Convert between any two units via primary unit (hub-and-spoke)."""
        return conversion.convert_between_units(self, from_unit, to_unit, quantity)

    def get_departments(self, active_only=True):
        allocations = self.departments or []
        if active_only:
            allocations = [row for row in allocations if row.department]
        return [row.department for row in allocations if row.department]

    def assign_to_department(self, department, is_primary=False):
        original_department = department
        department = frappe.db.get_value("Department", department)
        if not department:
            frappe.throw(
                _("Department {0} does not exist.").format(original_department)
            )

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
            frappe.throw(
                _("Volume conversion factor is required when a volume unit is set.")
            )
        if self.volume_conversion_factor and self.volume_conversion_factor <= 0:
            frappe.throw(_("Volume conversion factor must be greater than zero."))

        if self.weight_conversion_unit and not self.weight_conversion_factor:
            frappe.throw(
                _("Weight conversion factor is required when a weight unit is set.")
            )
        if self.weight_conversion_factor and self.weight_conversion_factor <= 0:
            frappe.throw(_("Weight conversion factor must be greater than zero."))

        for row in self.purchase_units or []:
            if not row.conversion_to_primary_cu or row.conversion_to_primary_cu <= 0:
                frappe.throw(
                    _(
                        "Conversion to primary count unit must be greater than zero for purchase unit {0}."
                    ).format(row.purchase_unit or row.vendor or row.name)
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

    def _validate_valuation_fields(self):
        """Validate valuation-related fields."""
        # Validate valuation_rate is non-negative
        if self.valuation_rate and self.valuation_rate < 0:
            frappe.throw(_("Valuation Rate cannot be negative."))

        # Validate default_incoming_rate is non-negative
        if self.default_incoming_rate and self.default_incoming_rate < 0:
            frappe.throw(_("Default Incoming Rate cannot be negative."))

        # Warn if valuation method is Manual but no valuation_rate is set
        if self.valuation_method == "Manual" and not self.valuation_rate:
            frappe.msgprint(
                _("Manual valuation method selected but no valuation rate set. "
                  "Please set a valuation rate."),
                indicator="orange",
                alert=True
            )

    def _set_default_valuation_method(self):
        """Set default valuation method if not specified."""
        if not self.valuation_method:
            self.valuation_method = "Moving Average"

        # Initialize valuation_rate to 0 if not set
        if self.valuation_rate is None:
            self.valuation_rate = 0.0
