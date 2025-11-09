"""Service layer for Products domain."""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable, Sequence

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.permissions.service import get_accessible_departments, has_department_permission

DEFAULT_LIST_FIELDS: list[str] = [
	"name",
	"product_name",
	"product_code",
	"product_type",
	"company",
	"primary_count_unit",
	"default_department",
	"is_non_inventory",
	"active",
]

_BYPASS_USERS = {"Administrator", "Guest"}
_BYPASS_ROLES = {"System Manager"}


def _get_user(user: str | None = None) -> str:
	return user or frappe.session.user


def _user_bypasses_department_permissions(user: str) -> bool:
	if user in _BYPASS_USERS:
		return True
	roles = set(frappe.get_roles(user))
	return bool(_BYPASS_ROLES.intersection(roles))


def _get_product_departments(product_names: Sequence[str]) -> dict[str, set[str]]:
	if not product_names:
		return {}

	rows = frappe.get_all(
		"Product Department",
		filters={
			"parent": ["in", list(product_names)],
			"parenttype": "Product",
		},
		fields=["parent", "department"],
	)

	department_map: dict[str, set[str]] = defaultdict(set)
	for row in rows:
		if row.department:
			department_map[row.parent].add(row.department)
	return department_map


def _filter_rows_by_permission(rows: list[dict[str, Any]], user: str, permission_flag: str = "can_read") -> list[dict[str, Any]]:
	if not rows:
		return []

	user = _get_user(user)
	if _user_bypasses_department_permissions(user):
		return rows

	accessible = set(get_accessible_departments(user, permission_flag=permission_flag))
	product_names = [row["name"] for row in rows if row.get("name")]
	department_map = _get_product_departments(product_names)

	filtered: list[dict[str, Any]] = []
	for row in rows:
		if row.get("is_non_inventory"):
			filtered.append(row)
			continue

		departments = department_map.get(row["name"], set())
		if not departments:
			filtered.append(row)
			continue

		if accessible.intersection(departments):
			filtered.append(row)

	return filtered


def list_products(
	*,
	filters: dict[str, Any] | None = None,
	fields: Sequence[str] | None = None,
	limit: int = 50,
	offset: int = 0,
	order_by: str = "product_name asc",
	search_text: str | None = None,
	user: str | None = None,
) -> dict[str, Any]:
	"""Return a list of products visible to the user."""
	user = _get_user(user)
	fields = list(fields) if fields else list(DEFAULT_LIST_FIELDS)

	if isinstance(filters, str):
		filters = frappe.parse_json(filters)
	filters = filters.copy() if filters else {}

	or_filters: list[dict[str, Any]] = []
	if search_text:
		like = f"%{search_text}%"
		or_filters.append({"product_name": ["like", like]})
		or_filters.append({"product_code": ["like", like]})
	elif "search_text" in filters:
		like = f"%{filters.pop('search_text')}%"
		or_filters.append({"product_name": ["like", like]})
		or_filters.append({"product_code": ["like", like]})

	results = frappe.get_all(
		"Product",
		fields=fields,
		filters=filters,
		or_filters=or_filters or None,
		limit_page_length=limit,
		limit_start=offset,
		order_by=order_by,
		distinct=True,
	)

	results = _filter_rows_by_permission(results, user, permission_flag="can_read")
	return {
		"results": results,
		"count": len(results),
	}


def _validate_user_can_modify_product(doc: Document, user: str, permission_flag: str) -> None:
	user = _get_user(user)

	if not frappe.has_permission("Product", permission_flag.replace("can_", ""), doc=doc, user=user):
		frappe.throw(_("User {0} lacks {1} permission for Product.").format(user, permission_flag), frappe.PermissionError)

	if doc.get("is_non_inventory"):
		return

	departments = {row.department for row in doc.get("departments", []) if row.department}
	if not departments:
		return

	for department in departments:
		if not has_department_permission(user, department, permission_flag):
			frappe.throw(
				_("User {0} lacks {1} permission for Department {2}.").format(user, permission_flag, department),
				frappe.PermissionError,
			)


def create_product(data: dict[str, Any], user: str | None = None) -> dict[str, Any]:
	"""Create a new product after validating permissions."""
	user = _get_user(user)
	doc = frappe.new_doc("Product")
	doc.update(data)

	_validate_user_can_modify_product(doc, user, permission_flag="can_create")
	saved = doc.insert(ignore_permissions=True)
	return saved.as_dict()


def update_product(name: str, data: dict[str, Any], user: str | None = None) -> dict[str, Any]:
	"""Update an existing product."""
	user = _get_user(user)
	doc = frappe.get_doc("Product", name)

	if not user_can_access_product(doc, user, permission_flag="can_read"):
		frappe.throw(_("You do not have permission to view this product."), frappe.PermissionError)

	doc.update(data)
	_validate_user_can_modify_product(doc, user, permission_flag="can_write")
	doc.save(ignore_permissions=True)
	return doc.as_dict()


def user_can_access_product(product: Document | str, user: str | None = None, permission_flag: str = "can_read") -> bool:
	"""Return True when the user can access the product."""
	user = _get_user(user)
	doc = frappe.get_doc("Product", product) if isinstance(product, str) else product

	if _user_bypasses_department_permissions(user):
		return True

	if doc.is_non_inventory:
		return True

	departments = {row.department for row in doc.get("departments", []) if row.department}
	if not departments:
		return True

	for department in departments:
		if has_department_permission(user, department, permission_flag):
			return True

	return False


def get_product(name: str, user: str | None = None) -> dict[str, Any]:
	"""Return a single product document."""
	user = _get_user(user)
	doc = frappe.get_doc("Product", name)
	if not user_can_access_product(doc, user, permission_flag="can_read"):
		frappe.throw(_("You do not have permission to view this product."), frappe.PermissionError)
	return doc.as_dict()


def convert_quantity(
	product: str,
	quantity: float,
	from_unit: str | None = None,
	to_unit: str | None = None,
	user: str | None = None,
) -> dict[str, Any]:
	"""Convert quantity using the product's conversion utilities."""
	user = _get_user(user)
	doc = frappe.get_doc("Product", product)
	if not user_can_access_product(doc, user, permission_flag="can_read"):
		frappe.throw(_("You do not have permission to view this product."), frappe.PermissionError)

	if from_unit and to_unit:
		result = doc.convert_between_units(from_unit, to_unit, quantity)
	elif from_unit:
		result = doc.convert_to_primary_unit(from_unit, quantity)
		to_unit = doc.primary_count_unit
	else:
		if not to_unit:
			frappe.throw(_("Target unit is required when converting from primary unit."))
		result = doc.convert_from_primary_unit(to_unit, quantity)

	return {
		"product": product,
		"quantity": quantity,
		"from_unit": from_unit or doc.primary_count_unit,
		"to_unit": to_unit or doc.primary_count_unit,
		"converted_quantity": result,
	}


def get_purchase_units(product: str, vendor: str | None = None, user: str | None = None) -> list[dict[str, Any]]:
	"""Return purchase unit rows for the product (optionally filtered by vendor)."""
	user = _get_user(user)
	doc = frappe.get_doc("Product", product)
	if not user_can_access_product(doc, user, permission_flag="can_read"):
		frappe.throw(_("You do not have permission to view this product."), frappe.PermissionError)

	purchase_units = []
	for row in doc.get("purchase_units", []):
		if vendor and row.vendor != vendor:
			continue
		purchase_units.append(row.as_dict())
	return purchase_units

