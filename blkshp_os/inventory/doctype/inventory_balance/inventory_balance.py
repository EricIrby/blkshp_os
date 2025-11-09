from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime  # type: ignore[import]


class InventoryBalance(Document):
	"""Product + Department inventory balance."""

	def autoname(self) -> None:
		if not (self.product and self.department and self.company):
			frappe.throw(_("Product, Department, and Company are required before naming the balance."))
		self.name = f"{self.product}-{self.department}-{self.company}"

	def validate(self) -> None:
		self._ensure_required_fields()
		self._ensure_unique_combination()

	def before_save(self) -> None:
		self.last_updated = now_datetime()

	@classmethod
	def update_for(
		cls,
		product: str,
		department: str,
		company: str,
		quantity: float,
		*,
		last_audit_date: str | None = None,
	) -> "InventoryBalance":
		"""Create or update a balance for the given identifiers."""
		existing_name = frappe.db.exists(
			"Inventory Balance",
			{
				"product": product,
				"department": department,
				"company": company,
			},
		)
		if existing_name:
			doc = frappe.get_doc("Inventory Balance", existing_name)
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Inventory Balance",
					"product": product,
					"department": department,
					"company": company,
				}
			)

		doc.quantity = quantity
		if last_audit_date:
			doc.last_audit_date = last_audit_date
		doc.save(ignore_permissions=True)
		return doc

	def apply_adjustment(self, quantity_delta: float) -> None:
		"""Adjust the balance by the delta supplied."""
		self.quantity = (self.quantity or 0) + quantity_delta

	@classmethod
	def apply_delta(
		cls,
		product: str,
		department: str,
		company: str,
		delta: float,
		*,
		last_audit_date: str | None = None,
	) -> "InventoryBalance":
		"""Apply a quantity delta to an existing balance, creating it if missing."""
		existing_name = frappe.db.exists(
			"Inventory Balance",
			{
				"product": product,
				"department": department,
				"company": company,
			},
		)
		if existing_name:
			doc: InventoryBalance = frappe.get_doc("Inventory Balance", existing_name)
		else:
			doc = frappe.get_doc(
				{
					"doctype": "Inventory Balance",
					"product": product,
					"department": department,
					"company": company,
					"quantity": 0,
				}
			)

		doc.apply_adjustment(float(delta or 0))
		if last_audit_date:
			doc.last_audit_date = last_audit_date
		doc.save(ignore_permissions=True)
		return doc

	def _ensure_required_fields(self) -> None:
		if not self.product:
			frappe.throw(_("Product is required."))
		if not self.department:
			frappe.throw(_("Department is required."))
		if not self.company:
			frappe.throw(_("Company is required."))

	def _ensure_unique_combination(self) -> None:
		filters: dict[str, object] = {
			"product": self.product,
			"department": self.department,
			"company": self.company,
		}
		if not self.is_new():
			filters["name"] = ["!=", self.name]
		if frappe.db.exists("Inventory Balance", filters):
			frappe.throw(
				_("Inventory balance already exists for {0} / {1} in company {2}.").format(
					self.product,
					self.department,
					self.company,
				)
			)

