"""Tests for the Products service layer."""
from __future__ import annotations

from typing import Any

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.products import service as product_service
from blkshp_os.permissions import service as permission_service


class TestProductService(FrappeTestCase):
	def setUp(self) -> None:
		super().setUp()
		self.company = self._ensure_company("Products Test Company")
		self.kitchen = self._create_department("P-KITCHEN", "Products Kitchen")
		self.bar = self._create_department("P-BAR", "Products Bar")
		self.user = self._ensure_user("products-service@example.com")

	def tearDown(self) -> None:
		frappe.set_user("Administrator")
		frappe.db.rollback()
		super().tearDown()

	def test_list_products_filters_by_department_permissions(self) -> None:
		frappe.set_user("Administrator")
		kitchen_product = self._create_product(
			"Kitchen Flour",
			self.kitchen.name,
		)
		self._create_product("Bar Syrup", self.bar.name)

		self._grant_department_permission(self.user, self.kitchen.name, can_read=1)

		frappe.set_user(self.user)
		response = product_service.list_products()
		names = {row["name"] for row in response["results"]}

		self.assertIn(kitchen_product, names)
		self.assertNotIn("Bar Syrup", names)

	def test_get_product_requires_permission(self) -> None:
		frappe.set_user("Administrator")
		product_name = self._create_product("Restricted Item", self.bar.name)

		self._grant_department_permission(self.user, self.kitchen.name, can_read=1)
		frappe.set_user(self.user)

		with self.assertRaises(frappe.PermissionError):
			product_service.get_product(product_name)

	def test_convert_quantity_uses_product_conversion(self) -> None:
		frappe.set_user("Administrator")
		product_name = self._create_product(
			"Soda Can",
			self.kitchen.name,
			extra_fields={
				"volume_conversion_unit": "fl oz",
				"volume_conversion_factor": 12,
			},
		)
		self._grant_department_permission(self.user, self.kitchen.name, can_read=1)

		frappe.set_user(self.user)
		result = product_service.convert_quantity(
			product=product_name,
			quantity=1,
			from_unit="gallon",
			to_unit="each",
		)

		self.assertAlmostEqual(result["converted_quantity"], 128 / 12, places=4)

	# -------------------------------------------------------------------------
	# Helpers
	# -------------------------------------------------------------------------
	def _ensure_company(self, name: str) -> str:
		existing = frappe.db.get_value("Company", {"company_name": name})
		if existing:
			return existing

		code = "".join(part[0] for part in name.split() if part).upper()[:8] or "COMP"
		company = frappe.get_doc(
			{
				"doctype": "Company",
				"company_name": name,
				"company_code": code,
				"default_currency": "USD",
			}
		)
		company.insert(ignore_permissions=True)
		return company.name

	def _ensure_user(self, email: str) -> str:
		if frappe.db.exists("User", email):
			return email
		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": "Products",
				"last_name": "Tester",
				"send_welcome_email": 0,
			}
		)
		user.insert(ignore_permissions=True)
		return email

	def _create_department(self, code: str, name: str) -> frappe.Document:
		department = frappe.get_doc(
			{
				"doctype": "Department",
				"department_code": code,
				"department_name": name,
				"department_type": "Food",
				"company": self.company,
			}
		)
		department.insert(ignore_permissions=True)
		return department

	def _grant_department_permission(self, user: str, department: str, **flags: int) -> None:
		default_flags = {flag: 0 for flag in permission_service.get_permission_flags()}
		default_flags.update(flags)
		permission = frappe.get_doc(
			{
				"doctype": "Department Permission",
				"parent": user,
				"parenttype": "User",
				"parentfield": "department_permissions",
				"department": department,
				**default_flags,
			}
		)
		permission.insert(ignore_permissions=True)

	def _create_product(
		self,
		product_name: str,
		department: str,
		extra_fields: dict[str, Any] | None = None,
	) -> str:
		payload: dict[str, Any] = {
			"product_name": product_name,
			"product_code": product_name.upper().replace(" ", "-"),
			"company": self.company,
			"product_type": "Food",
			"primary_count_unit": "each",
			"default_department": department,
			"departments": [
				{
					"department": department,
					"is_primary": 1,
				}
			],
		}
		# Explicitly clear optional conversion fields so validation does not
		# assume defaults when the tests do not provide them.
		payload.setdefault("volume_conversion_unit", "")
		payload.setdefault("volume_conversion_factor", None)
		payload.setdefault("weight_conversion_unit", "")
		payload.setdefault("weight_conversion_factor", None)

		if extra_fields:
			payload.update(extra_fields)

		doc = product_service.create_product(payload)
		return doc["name"]

