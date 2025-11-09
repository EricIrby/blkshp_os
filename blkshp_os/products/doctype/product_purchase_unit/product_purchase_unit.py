import frappe
from frappe import _
from frappe.model.document import Document


class ProductPurchaseUnit(Document):
    """Child table that defines vendor-specific purchase units."""

    def validate(self):
        self._validate_conversion()

    def _validate_conversion(self):
        if not self.conversion_to_primary_cu or self.conversion_to_primary_cu <= 0:
            frappe.throw(
                _("Conversion to primary count unit must be greater than zero for purchase unit {0}.").format(
                    self.purchase_unit or self.vendor or self.name
                )
            )

