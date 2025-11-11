"""Controller for the Subscription Plan DocType."""
from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.core_platform.services import clear_subscription_context_cache


class SubscriptionPlan(Document):
	"""Represents a collection of modules and feature defaults offered to tenants."""

	def validate(self) -> None:
		self._normalize_plan_code()
		self._validate_feature_overrides()

	def _normalize_plan_code(self) -> None:
		if not self.plan_code:
			return
		self.plan_code = self.plan_code.strip().upper()

	def _validate_feature_overrides(self) -> None:
		if not self.default_feature_overrides:
			return

		try:
			overrides: dict[str, Any] = json.loads(self.default_feature_overrides)
		except (TypeError, ValueError) as exc:
			raise frappe.ValidationError(
				_
				("Default Feature Overrides must contain valid JSON. "
				"Original error: {0}").format(exc)
			) from exc

		if not isinstance(overrides, dict):
			raise frappe.ValidationError(
				_("Default Feature Overrides must be a JSON object mapping feature keys to values."),
			)

		for feature_key, value in overrides.items():
			if not isinstance(feature_key, str) or not feature_key:
				raise frappe.ValidationError(
					_("Feature override keys must be non-empty strings."),
				)
			if not isinstance(value, (bool, dict)):
				raise frappe.ValidationError(
					_("Override for feature {0} must be a boolean or nested configuration." ).format(feature_key),
				)

	def on_update(self) -> None:
		clear_subscription_context_cache()

	def on_trash(self) -> None:
		clear_subscription_context_cache()
