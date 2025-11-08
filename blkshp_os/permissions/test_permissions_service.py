"""Tests for permission service helpers."""
from __future__ import annotations

import json

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]

from blkshp_os.permissions import service


class TestPermissionService(FrappeTestCase):
	"""Exercise the department permission helper functions."""

	def setUp(self) -> None:
		super().setUp()
		self.company = self._ensure_company()
		self.user = self._ensure_user("permission_service@example.com")
		self.kitchen = self._create_department("KITCHEN", "Kitchen")
		self.bar = self._create_department("BAR", "Bar")

	def tearDown(self) -> None:
		frappe.db.rollback()
		super().tearDown()

	def test_permission_flags_constant(self) -> None:
		flags = service.get_permission_flags()
		self.assertIn("can_read", flags)
		self.assertIn("can_write", flags)
		self.assertEqual(len(flags), len(set(flags)))

	def test_get_accessible_departments_returns_active_departments(self) -> None:
		self._create_department_permission(self.kitchen.name, can_read=1)
		self._create_department_permission(self.bar.name, can_read=1, can_write=1)

		self.bar.is_active = 0
		self.bar.save(ignore_permissions=True)

		departments = service.get_accessible_departments(self.user)
		self.assertEqual(departments, [self.kitchen.name])

		all_departments = service.get_accessible_departments(
			self.user, include_inactive=True
		)
		self.assertCountEqual(all_departments, [self.kitchen.name, self.bar.name])

	def test_has_department_permission_checks_flag(self) -> None:
		self._create_department_permission(self.kitchen.name, can_read=1)
		self.assertTrue(service.has_department_permission(self.user, self.kitchen.name))
		self.assertFalse(
			service.has_department_permission(self.user, self.kitchen.name, "can_write")
		)

	def test_system_manager_bypasses_department_restrictions(self) -> None:
		user_doc = frappe.get_doc("User", self.user)
		user_doc.add_roles("System Manager")

		departments = service.get_accessible_departments(self.user)
		self.assertIn(self.kitchen.name, departments)
		self.assertIn(self.bar.name, departments)

	def _ensure_company(self, name: str = "Permissions Test Company") -> str:
		if frappe.db.exists("Company", {"company_name": name}):
			return name

		company = frappe.get_doc(
			{
				"doctype": "Company",
				"company_name": name,
				"default_currency": "USD",
			}
		)
		company.insert(ignore_permissions=True)
		return name

	def _ensure_user(self, email: str) -> str:
		if frappe.db.exists("User", email):
			return email

		user = frappe.get_doc(
			{
				"doctype": "User",
				"email": email,
				"first_name": "Permissions",
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
				"settings": json.dumps({"custom_settings": {}}),
			}
		)
		department.insert(ignore_permissions=True)
		return department

	def _create_department_permission(self, department: str, **flags: int) -> None:
		default_flags = {flag: 0 for flag in service.get_permission_flags()}
		default_flags.update(flags)
		permission = frappe.get_doc(
			{
				"doctype": "Department Permission",
				"parent": self.user,
				"parenttype": "User",
				"parentfield": "department_permissions",
				"department": department,
				**default_flags,
			}
		)
		permission.insert(ignore_permissions=True)


