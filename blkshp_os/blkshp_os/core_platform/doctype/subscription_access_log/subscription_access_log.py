"""Subscription Access Log DocType controller."""

from __future__ import annotations

import frappe
from frappe.model.document import Document


class SubscriptionAccessLog(Document):
	"""Audit log for subscription-based access enforcement.

	This DocType records all denied access attempts and admin bypasses
	for compliance and security monitoring purposes.

	All fields are read-only after creation to ensure audit trail integrity.
	"""

	pass  # Simple audit log, no custom logic needed
