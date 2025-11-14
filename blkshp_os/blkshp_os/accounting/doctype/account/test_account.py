import frappe
from frappe.tests.utils import FrappeTestCase


class TestAccount(FrappeTestCase):
	def test_create_account(self):
		company = _ensure_company()

		doc = frappe.get_doc(
			{
				"doctype": "Account",
				"account_name": "Food Cost",
				"account_code": "6100",
				"company": company,
				"account_type": "Expense",
			}
		)
		doc.insert()

		self.assertEqual(doc.account_name, "Food Cost")
		self.assertEqual(doc.account_code, "6100")
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

