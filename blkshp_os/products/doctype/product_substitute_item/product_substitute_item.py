import frappe
from frappe import _
from frappe.model.document import Document


class ProductSubstituteItem(Document):
    """Child table for substitute products."""

    def validate(self):
        if self.substitute_product == self.parent:
            frappe.throw(_("Product cannot substitute itself."))

