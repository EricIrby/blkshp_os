import frappe
from frappe import _
from frappe.model.document import Document


class ProductCategory(Document):
    """Product category master with optional hierarchy."""

    def before_insert(self):
        if not self.category_code:
            self.category_code = self._generate_category_code()

    def validate(self):
        self._ensure_unique_code()
        self._prevent_circular_reference()

    def _generate_category_code(self):
        return frappe.model.naming.make_autoname("PCAT-.#####")

    def _ensure_unique_code(self):
        if not self.category_code:
            return

        if frappe.db.exists(
            "Product Category",
            {
                "name": ["!=", self.name],
                "category_code": self.category_code,
            },
        ):
            frappe.throw(
                _("Category code {0} is already in use.").format(self.category_code),
                frappe.UniqueValidationError,
            )

    def _prevent_circular_reference(self):
        if not self.parent_category:
            return

        if self.parent_category == self.name:
            frappe.throw(_("A category cannot be its own parent."))

        ancestor = self.parent_category
        visited = {self.name}

        while ancestor:
            if ancestor in visited:
                frappe.throw(_("Detected circular hierarchy for Product Category."))
            visited.add(ancestor)
            ancestor = frappe.db.get_value(
                "Product Category", ancestor, "parent_category"
            )
