"""Test cases for Department DocType."""
from __future__ import annotations

import json

import frappe
from frappe.tests.utils import FrappeTestCase

from blkshp_os.departments.doctype.department.department import (
	SETTINGS_PERMISSION_FLAGS,
	get_accessible_departments,
	get_department_setting,
)


class TestDepartment(FrappeTestCase):
	"""Exercise core validation and helper utilities for the Department DocType."""

	def setUp(self) -> None:
		super().setUp()
		self.company = self._ensure_company()

	def tearDown(self) -> None:
		frappe.db.rollback()
		super().tearDown()

	def test_department_code_is_unique_per_company(self) -> None:
		self._create_department(code="KIT-A", name="Kitchen")

		with self.assertRaises(frappe.ValidationError):
			self._create_department(code="KIT-A", name="Kitchen Duplicate")

		# Same code allowed for different company
		other_company = self._ensure_company("Test Company 2")
		self._create_department(code="KIT-A", name="Kitchen Other", company=other_company)

	def test_settings_must_be_valid_json(self) -> None:
		department = self._create_department(code="BAR-A", name="Bar")
		department.settings = "not json at all"
		with self.assertRaises(frappe.ValidationError):
			department.save(ignore_permissions=True)

	def test_numeric_settings_type_validation(self) -> None:
		department = self._create_department(code="BAR-B", name="Bar B")
		department.settings = json.dumps({"reorder_point_buffer": "invalid"})
		with self.assertRaises(frappe.ValidationError):
			department.save(ignore_permissions=True)

	def test_get_department_setting_helper(self) -> None:
		department = self._create_department(
			code="BAR-C",
			name="Bar C",
			settings={"default_ordering_day": "monday", "custom_settings": {"foo": "bar"}},
		)

		self.assertEqual(get_department_setting(department.name, "default_ordering_day"), "monday")
		self.assertEqual(
			get_department_setting(department.name, "custom_settings"),
			{"foo": "bar"},
		)
		self.assertEqual(get_department_setting(department.name, "missing_key", "fallback"), "fallback")

	def test_get_accessible_departments_returns_filtered_list(self) -> None:
		user = self._ensure_user("department_tester@example.com")
		kitchen = self._create_department(code="KIT-B", name="Kitchen B")
		bar = self._create_department(code="BAR-D", name="Bar D")

		self._create_department_permission(user, kitchen.name, can_read=1)
		self._create_department_permission(user, bar.name, can_read=1, can_write=1)

		result = get_accessible_departments(user, "can_read")
		self.assertCountEqual(result, [kitchen.name, bar.name])

		write_departments = get_accessible_departments(user, "can_write")
		self.assertEqual(write_departments, [bar.name])

		with self.assertRaises(frappe.ValidationError):
			get_accessible_departments(user, "does_not_exist")

	def test_settings_permission_flags_export(self) -> None:
		flags = tuple(SETTINGS_PERMISSION_FLAGS())
		self.assertIn("can_read", flags)
		self.assertIn("can_write", flags)
		self.assertIn("can_approve", flags)
		self.assertEqual(len(flags), len(set(flags)))

	def _create_department(
		self,
		code: str,
		name: str,
		company: str | None = None,
		settings: dict | None = None,
	) -> frappe.Document:
		doc = frappe.get_doc(
			{
				"doctype": "Department",
				"department_code": code,
				"department_name": name,
				"department_type": "Food",
				"company": company or self.company,
			}
		)
		if settings is not None:
			doc.settings = json.dumps(settings)
		doc.insert(ignore_permissions=True)
		return doc

	def _create_department_permission(
		self,
		user: str,
		department: str,
		**flags: int,
	) -> None:
		default_flags = {flag: 0 for flag in SETTINGS_PERMISSION_FLAGS()}
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

	def _ensure_company(self, name: str = "Test Company 1") -> str:
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
				"first_name": "Department",
				"last_name": "Tester",
				"send_welcome_email": 0,
			}
		)
		user.insert(ignore_permissions=True)
		return email

