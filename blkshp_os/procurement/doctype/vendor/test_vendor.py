import frappe
from frappe.tests.utils import FrappeTestCase


class TestVendor(FrappeTestCase):
	def test_create_vendor(self):
		company = _ensure_company()

		doc = frappe.get_doc(
			{
				"doctype": "Vendor",
				"vendor_name": "Fresh Farms",
				"vendor_code": "FRESH",
				"company": company,
				"primary_contact_email": "orders@freshfarms.test",
			}
		)
		doc.insert()

		self.assertEqual(doc.vendor_name, "Fresh Farms")
		self.assertEqual(doc.vendor_code, "FRESH")
		self.assertEqual(doc.company, company)


def _ensure_company() -> str:
	existing = frappe.db.exists("Company", {"company_name": "Test Company"})
	if existing:
		return existing

	company = frappe.get_doc(
		{
			"doctype": "Company",
			"company_name": "Test Company",
			"company_code": "TESTCOMP",
		}
	)
	company.insert()
	return company.name

