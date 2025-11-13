"""Centralized unit conversion service for products.

This module provides a shared conversion service that all modules can use
to prevent conversion drift and ensure consistent unit handling across
the system.
"""
from __future__ import annotations

from typing import Any, TypedDict

import frappe
from frappe import _  # type: ignore[attr-defined] # noqa: F401


# Standard unit conversion constants
VOLUME_TO_ML: dict[str, float] = {
	"ml": 1,
	"milliliter": 1,
	"l": 1000,
	"liter": 1000,
	"litre": 1000,
	"fl oz": 29.5735,
	"fluid ounce": 29.5735,
	"pint": 473.176,
	"quart": 946.353,
	"gallon": 3785.41,
}

WEIGHT_TO_G: dict[str, float] = {
	"g": 1,
	"gram": 1,
	"kg": 1000,
	"kilogram": 1000,
	"oz": 28.3495,
	"ounce": 28.3495,
	"lb": 453.592,
	"pound": 453.592,
}


class ProductConversionData(TypedDict, total=False):
	"""Product data structure for conversion operations."""

	name: str
	primary_count_unit: str
	volume_conversion_unit: str | None
	volume_conversion_factor: float | None
	weight_conversion_unit: str | None
	weight_conversion_factor: float | None
	purchase_units: list[dict[str, Any]] | None


def _normalize_unit(unit: str | None) -> str:
	"""Normalize unit name for comparison."""
	if not unit:
		return ""
	return (unit or "").strip().lower()


def _load_product_data(product: str | ProductConversionData) -> ProductConversionData:
	"""Load product data from name or return dict directly."""
	if isinstance(product, dict):
		return product

	if isinstance(product, str):
		doc = frappe.get_doc("Product", product)
		return {
			"name": doc.name,
			"primary_count_unit": doc.primary_count_unit or "",
			"volume_conversion_unit": doc.volume_conversion_unit,
			"volume_conversion_factor": doc.volume_conversion_factor,
			"weight_conversion_unit": doc.weight_conversion_unit,
			"weight_conversion_factor": doc.weight_conversion_factor,
			"purchase_units": [
				{
					"purchase_unit": row.purchase_unit,
					"conversion_to_primary_cu": row.conversion_to_primary_cu,
					"name": row.name,
				}
				for row in doc.get("purchase_units", [])
			]
			if doc.get("purchase_units")
			else None,
		}

	raise ValueError(_("Product must be a string (name) or dict (data), got {0}").format(type(product)))


def _convert_standard_volume(quantity: float, from_unit: str, to_unit: str) -> float | None:
	"""Convert between standard volume units."""
	from_unit = _normalize_unit(from_unit)
	to_unit = _normalize_unit(to_unit)

	if from_unit not in VOLUME_TO_ML or to_unit not in VOLUME_TO_ML:
		return None

	ml = quantity * VOLUME_TO_ML[from_unit]
	return ml / VOLUME_TO_ML[to_unit]


def _convert_standard_weight(quantity: float, from_unit: str, to_unit: str) -> float | None:
	"""Convert between standard weight units."""
	from_unit = _normalize_unit(from_unit)
	to_unit = _normalize_unit(to_unit)

	if from_unit not in WEIGHT_TO_G or to_unit not in WEIGHT_TO_G:
		return None

	grams = quantity * WEIGHT_TO_G[from_unit]
	return grams / WEIGHT_TO_G[to_unit]


def _convert_from_purchase_unit(
	product_data: ProductConversionData, from_unit: str, quantity: float
) -> float | None:
	"""Convert from purchase unit to primary unit."""
	from_unit = _normalize_unit(from_unit)
	purchase_units = product_data.get("purchase_units") or []

	for row in purchase_units:
		purchase_unit = row.get("purchase_unit")
		if not purchase_unit:
			continue

		if _normalize_unit(purchase_unit) == from_unit:
			conversion = row.get("conversion_to_primary_cu", 0)
			if conversion <= 0:
				return None
			return quantity * conversion

		# Check if unit matches row name
		row_name = row.get("name")
		if row_name and _normalize_unit(str(row_name)) == from_unit:
			conversion = row.get("conversion_to_primary_cu", 0)
			if conversion <= 0:
				return None
			return quantity * conversion

	return None


def _convert_from_volume_unit(
	product_data: ProductConversionData, from_unit: str, quantity: float
) -> float | None:
	"""Convert from volume unit to primary unit."""
	volume_unit = product_data.get("volume_conversion_unit")
	volume_factor = product_data.get("volume_conversion_factor")

	if not volume_unit or not volume_factor or volume_factor <= 0:
		return None

	from_unit = _normalize_unit(from_unit)
	base_unit = _normalize_unit(volume_unit)

	if from_unit == base_unit:
		return quantity / volume_factor

	# Convert via standard volume units
	qty_in_base = _convert_standard_volume(quantity, from_unit, base_unit)
	if qty_in_base is None:
		return None

	return qty_in_base / volume_factor


def _convert_from_weight_unit(
	product_data: ProductConversionData, from_unit: str, quantity: float
) -> float | None:
	"""Convert from weight unit to primary unit."""
	weight_unit = product_data.get("weight_conversion_unit")
	weight_factor = product_data.get("weight_conversion_factor")

	if not weight_unit or not weight_factor or weight_factor <= 0:
		return None

	from_unit = _normalize_unit(from_unit)
	base_unit = _normalize_unit(weight_unit)

	if from_unit == base_unit:
		return quantity / weight_factor

	# Convert via standard weight units
	qty_in_base = _convert_standard_weight(quantity, from_unit, base_unit)
	if qty_in_base is None:
		return None

	return qty_in_base / weight_factor


def _convert_to_purchase_unit(
	product_data: ProductConversionData, to_unit: str, quantity: float
) -> float | None:
	"""Convert from primary unit to purchase unit."""
	to_unit = _normalize_unit(to_unit)
	purchase_units = product_data.get("purchase_units") or []

	for row in purchase_units:
		purchase_unit = row.get("purchase_unit")
		if not purchase_unit:
			continue

		if _normalize_unit(purchase_unit) == to_unit:
			conversion = row.get("conversion_to_primary_cu", 0)
			if conversion <= 0:
				return None
			return quantity / conversion

		# Check if unit matches row name
		row_name = row.get("name")
		if row_name and _normalize_unit(str(row_name)) == to_unit:
			conversion = row.get("conversion_to_primary_cu", 0)
			if conversion <= 0:
				return None
			return quantity / conversion

	return None


def _convert_to_volume_unit(
	product_data: ProductConversionData, to_unit: str, quantity: float
) -> float | None:
	"""Convert from primary unit to volume unit."""
	volume_unit = product_data.get("volume_conversion_unit")
	volume_factor = product_data.get("volume_conversion_factor")

	if not volume_unit or not volume_factor or volume_factor <= 0:
		return None

	to_unit = _normalize_unit(to_unit)
	base_unit = _normalize_unit(volume_unit)

	qty_in_base = quantity * volume_factor

	if to_unit == base_unit:
		return qty_in_base

	# Convert via standard volume units
	converted = _convert_standard_volume(qty_in_base, base_unit, to_unit)
	if converted is None:
		return None
	return converted


def _convert_to_weight_unit(
	product_data: ProductConversionData, to_unit: str, quantity: float
) -> float | None:
	"""Convert from primary unit to weight unit."""
	weight_unit = product_data.get("weight_conversion_unit")
	weight_factor = product_data.get("weight_conversion_factor")

	if not weight_unit or not weight_factor or weight_factor <= 0:
		return None

	to_unit = _normalize_unit(to_unit)
	base_unit = _normalize_unit(weight_unit)

	qty_in_base = quantity * weight_factor

	if to_unit == base_unit:
		return qty_in_base

	# Convert via standard weight units
	converted = _convert_standard_weight(qty_in_base, base_unit, to_unit)
	if converted is None:
		return None
	return converted


def convert_to_primary_unit(
	product: str | ProductConversionData, from_unit: str, quantity: float
) -> float:
	"""Convert any unit to primary unit (hub conversion).

	Args:
		product: Product name (str) or product data dict
		from_unit: Source unit to convert from
		quantity: Quantity in source unit

	Returns:
		Quantity in primary count unit

	Raises:
		frappe.ValidationError: If conversion is not possible
	"""
	product_data = _load_product_data(product)
	from_unit = _normalize_unit(from_unit)

	primary_unit = _normalize_unit(product_data.get("primary_count_unit", ""))
	if primary_unit and from_unit == primary_unit:
		return quantity

	# Try purchase unit conversion
	qty = _convert_from_purchase_unit(product_data, from_unit, quantity)
	if qty is not None:
		return qty

	# Try volume unit conversion
	qty = _convert_from_volume_unit(product_data, from_unit, quantity)
	if qty is not None:
		return qty

	# Try weight unit conversion
	qty = _convert_from_weight_unit(product_data, from_unit, quantity)
	if qty is not None:
		return qty

	product_name = product_data.get("name", str(product))
	# This line always raises, but type checker doesn't recognize it
	frappe.throw(  # type: ignore[misc]
		_("Cannot convert from unit {0} for product {1}.").format(
			from_unit or _("(empty)"), product_name
		)
	)
	raise AssertionError("Unreachable code")  # For type checker


def convert_from_primary_unit(
	product: str | ProductConversionData, to_unit: str, quantity: float
) -> float:
	"""Convert from primary unit to any unit.

	Args:
		product: Product name (str) or product data dict
		to_unit: Target unit to convert to
		quantity: Quantity in primary count unit

	Returns:
		Quantity in target unit

	Raises:
		frappe.ValidationError: If conversion is not possible
	"""
	product_data = _load_product_data(product)
	to_unit = _normalize_unit(to_unit)

	primary_unit = _normalize_unit(product_data.get("primary_count_unit", ""))
	if primary_unit and to_unit == primary_unit:
		return quantity

	# Try purchase unit conversion
	qty = _convert_to_purchase_unit(product_data, to_unit, quantity)
	if qty is not None:
		return qty

	# Try volume unit conversion
	qty = _convert_to_volume_unit(product_data, to_unit, quantity)
	if qty is not None:
		return qty

	# Try weight unit conversion
	qty = _convert_to_weight_unit(product_data, to_unit, quantity)
	if qty is not None:
		return qty

	product_name = product_data.get("name", str(product))
	# This line always raises, but type checker doesn't recognize it
	frappe.throw(  # type: ignore[misc]
		_("Cannot convert to unit {0} for product {1}.").format(
			to_unit or _("(empty)"), product_name
		)
	)
	raise AssertionError("Unreachable code")  # For type checker


def convert_between_units(
	product: str | ProductConversionData, from_unit: str, to_unit: str, quantity: float
) -> float:
	"""Convert between any two units via primary unit (hub-and-spoke).

	Args:
		product: Product name (str) or product data dict
		from_unit: Source unit to convert from
		to_unit: Target unit to convert to
		quantity: Quantity in source unit

	Returns:
		Quantity in target unit

	Raises:
		frappe.ValidationError: If conversion is not possible
	"""
	primary_qty = convert_to_primary_unit(product, from_unit, quantity)
	return convert_from_primary_unit(product, to_unit, primary_qty)


def get_available_count_units(product: str | ProductConversionData) -> list[str]:
	"""Get all available count units for a product.

	Args:
		product: Product name (str) or product data dict

	Returns:
		List of available unit names (normalized, sorted)
	"""
	product_data = _load_product_data(product)
	units = set()

	primary_unit = product_data.get("primary_count_unit")
	if primary_unit:
		units.add(_normalize_unit(primary_unit))

	volume_unit = product_data.get("volume_conversion_unit")
	if volume_unit:
		units.add(_normalize_unit(volume_unit))
		units.update(VOLUME_TO_ML.keys())

	weight_unit = product_data.get("weight_conversion_unit")
	if weight_unit:
		units.add(_normalize_unit(weight_unit))
		units.update(WEIGHT_TO_G.keys())

	purchase_units = product_data.get("purchase_units") or []
	for row in purchase_units:
		purchase_unit = row.get("purchase_unit")
		if purchase_unit:
			units.add(_normalize_unit(purchase_unit))

	return sorted(units)

