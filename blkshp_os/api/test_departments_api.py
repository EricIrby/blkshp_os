"""Test cases for Department API endpoints."""
from __future__ import annotations

import json

import frappe  # type: ignore[import]
from frappe.tests.utils import FrappeTestCase  # type: ignore[import]

from blkshp_os.api import departments as dept_api
from blkshp_os.permissions import service as permission_service


class TestDepartmentsAPI(FrappeTestCase):
	"""Test Department REST API endpoints."""

	def setUp(self) -> None:
		super().setUp()
		self.company = self._ensure_company()
		self._ensure_role("System User")
		self.user = self._ensure_user("api_test@example.com")
		self.department_a = self._create_department("API-A", "API Test Department A")
		self.department_b = self._create_department("API-B", "API Test Department B")
		
		# Grant user access to department A
		self._grant_department_permission(self.user, self.department_a.name, can_read=1, can_write=1)
		
		# Set session user
		frappe.set_user(self.user)

	def tearDown(self) -> None:
		frappe.set_user("Administrator")
		frappe.db.rollback()
		super().tearDown()

	def test_get_accessible_departments(self) -> None:
		"""Test getting accessible departments for current user."""
		departments = dept_api.get_accessible_departments()
		
		self.assertIsInstance(departments, list)
		self.assertGreater(len(departments), 0)
		
		# User should have access to department A
		dept_names = [d["name"] for d in departments]
		self.assertIn(self.department_a.name, dept_names)

	def test_get_department_details_with_permission(self) -> None:
		"""Test getting department details with proper permissions."""
		details = dept_api.get_department_details(self.department_a.name)
		
		self.assertIsInstance(details, dict)
		self.assertIn("department", details)
		self.assertIn("products", details)
		self.assertIn("users", details)
		self.assertEqual(details["department"]["name"], self.department_a.name)

	def test_get_department_details_without_permission(self) -> None:
		"""Test that accessing department without permission raises error."""
		# Department B has no permissions granted
		with self.assertRaises(frappe.PermissionError):
			dept_api.get_department_details(self.department_b.name)

	def test_get_department_hierarchy(self) -> None:
		"""Test getting department hierarchy."""
		# Create child department
		child_dept = self._create_department("API-A-CHILD", "API Child Department")
		child_dept.parent_department = self.department_a.name
		child_dept.save(ignore_permissions=True)
		
		# Grant access to child
		self._grant_department_permission(self.user, child_dept.name, can_read=1)
		
		hierarchy = dept_api.get_department_hierarchy()
		
		self.assertIsInstance(hierarchy, list)
		# Should contain departments without parents
		dept_names = [d["name"] for d in hierarchy]
		self.assertIn(self.department_a.name, dept_names)

	def test_get_department_settings(self) -> None:
		"""Test getting department settings."""
		# Set some settings
		self.department_a.settings = json.dumps({
			"eoq_enabled": True,
			"default_ordering_day": "Monday"
		})
		self.department_a.save(ignore_permissions=True)
		
		# Get all settings
		settings = dept_api.get_department_settings(self.department_a.name)
		self.assertIsInstance(settings, dict)
		self.assertEqual(settings.get("eoq_enabled"), True)
		
		# Get specific setting
		ordering_day = dept_api.get_department_settings(
			self.department_a.name,
			setting_key="default_ordering_day"
		)
		self.assertEqual(ordering_day, "Monday")

	def test_update_department_settings(self) -> None:
		"""Test updating department settings."""
		new_settings = {
			"eoq_enabled": True,
			"minimum_order_amount": 100.0
		}
		
		updated = dept_api.update_department_settings(
			self.department_a.name,
			new_settings
		)
		
		self.assertIsInstance(updated, dict)
		self.assertEqual(updated["eoq_enabled"], True)
		self.assertEqual(updated["minimum_order_amount"], 100.0)
		
		# Verify saved
		self.department_a.reload()
		saved_settings = json.loads(self.department_a.settings)
		self.assertEqual(saved_settings["eoq_enabled"], True)

	def test_update_department_settings_without_permission(self) -> None:
		"""Test that updating settings without permission raises error."""
		with self.assertRaises(frappe.PermissionError):
			dept_api.update_department_settings(
				self.department_b.name,
				{"eoq_enabled": True}
			)

	def test_get_department_statistics(self) -> None:
		"""Test getting department statistics."""
		stats = dept_api.get_department_statistics(self.department_a.name)
		
		self.assertIsInstance(stats, dict)
		self.assertIn("product_count", stats)
		self.assertIn("user_count", stats)
		self.assertIn("inventory_value", stats)
		self.assertIn("child_department_count", stats)
		self.assertEqual(stats["department"], self.department_a.name)

	def test_system_manager_bypass(self) -> None:
		"""Test that System Manager can access all departments."""
		frappe.set_user("Administrator")
		
		# Should be able to access department B even without explicit permission
		details = dept_api.get_department_details(self.department_b.name)
		self.assertEqual(details["department"]["name"], self.department_b.name)

	def _ensure_company(self, name: str = "Test Company API") -> str:
		existing = frappe.db.exists("Company", {"company_name": name})
		if existing:
			return existing

		code = "".join(part[0] for part in name.split() if part).upper()[:8] or "COMP"
		company = frappe.get_doc({
			"doctype": "Company",
			"company_name": name,
			"company_code": code,
			"default_currency": "USD",
		})
		company.insert(ignore_permissions=True)
		return company.name

	def _ensure_user(self, email: str) -> str:
		if not frappe.db.exists("User", email):
			user = frappe.get_doc({
				"doctype": "User",
				"email": email,
				"first_name": "API",
				"last_name": "Test",
				"enabled": 1,
				"roles": [
					{
						"role": "System User",
					}
				],
				"send_welcome_email": 0,
			})
			user.insert(ignore_permissions=True)
		else:
			user = frappe.get_doc("User", email)
			if not any(role.role == "System User" for role in user.roles):
				user.append("roles", {"role": "System User"})
				user.save(ignore_permissions=True)

		return email

	def _ensure_role(self, role_name: str) -> None:
		if frappe.db.exists("Role", role_name):
			return
		role = frappe.get_doc(
			{
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 0,
			}
		)
		role.insert(ignore_permissions=True)

	def _create_department(self, code: str, name: str) -> frappe.Document:
		existing = frappe.db.exists(
			"Department",
			{
				"department_code": code,
				"company": self.company,
			},
		)
		if existing:
			return frappe.get_doc("Department", existing)

		department = frappe.get_doc({
			"doctype": "Department",
			"department_code": code,
			"department_name": name,
			"department_type": "Food",
			"company": self.company,
			"is_active": 1
		})
		department.insert(ignore_permissions=True)
		return department

	def _grant_department_permission(
		self,
		user: str,
		department: str,
		**flags: int,
	) -> None:
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

