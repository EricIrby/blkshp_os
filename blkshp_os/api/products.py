"""REST API endpoints for Products domain."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

import frappe
from frappe import _
from frappe.utils import flt

from blkshp_os.products import service as product_service


@frappe.whitelist()
def list_products(
    filters: dict[str, Any] | str | None = None,
    fields: Sequence[str] | str | None = None,
    limit: int = 50,
    offset: int = 0,
    order_by: str = "product_name asc",
    search_text: str | None = None,
) -> dict[str, Any]:
    """List products visible to the current session user."""
    if isinstance(fields, str):
        fields = frappe.parse_json(fields)
    return product_service.list_products(
        filters=filters,
        fields=fields,
        limit=limit,
        offset=offset,
        order_by=order_by,
        search_text=search_text,
    )


@frappe.whitelist()
def get_product(name: str) -> dict[str, Any]:
    """Return the product document."""
    if not name:
        frappe.throw(_("Product name is required."))
    return product_service.get_product(name)


@frappe.whitelist()
def create_product(data: dict[str, Any] | str) -> dict[str, Any]:
    """Create a product."""
    if isinstance(data, str):
        data = frappe.parse_json(data)
    if not isinstance(data, dict):
        frappe.throw(_("Invalid payload for product creation."))
    return product_service.create_product(data)


@frappe.whitelist()
def update_product(name: str, data: dict[str, Any] | str) -> dict[str, Any]:
    """Update an existing product."""
    if not name:
        frappe.throw(_("Product name is required."))
    if isinstance(data, str):
        data = frappe.parse_json(data)
    if not isinstance(data, dict):
        frappe.throw(_("Invalid payload for product update."))
    return product_service.update_product(name, data)


@frappe.whitelist()
def convert_quantity(
    product: str,
    quantity: float | str,
    from_unit: str | None = None,
    to_unit: str | None = None,
) -> dict[str, Any]:
    """Convert quantity between units using the centralized conversion service.

    Args:
            product: Product name or code
            quantity: Quantity to convert
            from_unit: Source unit (optional, defaults to primary unit)
            to_unit: Target unit (optional, defaults to primary unit)

    Returns:
            Dictionary with conversion result including product, quantities, and units
    """
    if not product:
        frappe.throw(_("Product is required."))

    quantity = flt(quantity)
    if quantity < 0:
        frappe.throw(_("Quantity cannot be negative."))

    return product_service.convert_quantity(
        product=product,
        quantity=quantity,
        from_unit=from_unit,
        to_unit=to_unit,
    )


@frappe.whitelist()
def get_available_units(product: str) -> dict[str, Any]:
    """Get all available count units for a product.

    Args:
            product: Product name or code

    Returns:
            Dictionary with product name and list of available units
    """
    from blkshp_os.products import conversion

    if not product:
        frappe.throw(_("Product is required."))

    # Verify product exists and user has access
    doc = frappe.get_doc("Product", product)
    if not product_service.user_can_access_product(doc, permission_flag="can_read"):
        frappe.throw(
            _("You do not have permission to view this product."),
            frappe.PermissionError,
        )

    units = conversion.get_available_count_units(product)

    return {
        "product": product,
        "product_name": doc.product_name,
        "primary_count_unit": doc.primary_count_unit,
        "available_units": units,
    }


@frappe.whitelist()
def get_purchase_units(product: str, vendor: str | None = None) -> list[dict[str, Any]]:
    """Return purchase units for a product."""
    if not product:
        frappe.throw(_("Product is required."))
    return product_service.get_purchase_units(product, vendor=vendor)
