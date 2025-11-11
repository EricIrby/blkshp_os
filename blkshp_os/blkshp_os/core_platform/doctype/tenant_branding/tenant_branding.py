"""Controller for Tenant Branding records."""
from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.core_platform.services import (
	clear_feature_matrix_cache,
	clear_subscription_context_cache,
)


class TenantBranding(Document):
	"""Stores branding assets and theming information for a tenant."""

	def validate(self) -> None:
		self._normalize_theme_name()
		self._validate_json_properties()

	def _normalize_theme_name(self) -> None:
		if self.theme_name:
			self.theme_name = self.theme_name.strip()

	def _validate_json_properties(self) -> None:
		if not self.custom_properties:
			return

		try:
			payload: dict[str, Any] = json.loads(self.custom_properties)
		except (TypeError, ValueError) as exc:
			raise frappe.ValidationError(
				_("Custom Properties must be valid JSON. Original error: {0}").format(exc)
			) from exc

		if not isinstance(payload, dict):
			raise frappe.ValidationError(
				_("Custom Properties must be a JSON object mapping variable names to values."),
			)

	def on_update(self) -> None:
		clear_subscription_context_cache()
		clear_feature_matrix_cache()

	def on_trash(self) -> None:
		clear_subscription_context_cache()
		clear_feature_matrix_cache()
