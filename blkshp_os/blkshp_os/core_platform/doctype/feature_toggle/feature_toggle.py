"""Controller for Feature Toggle records."""
from __future__ import annotations

import re

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.core_platform.services import clear_subscription_context_cache

_FEATURE_KEY_PATTERN = re.compile(r"^[a-z0-9_.-]+$")


class FeatureToggle(Document):
	"""Defines a granular feature flag that can be assigned to plans or tenants."""

	def validate(self) -> None:
		self._normalize_feature_key()
		self._validate_feature_key_pattern()

	def on_update(self) -> None:
		clear_subscription_context_cache()

	def on_trash(self) -> None:
		clear_subscription_context_cache()

	def _normalize_feature_key(self) -> None:
		if not self.feature_key:
			return
		self.feature_key = self.feature_key.strip().lower()

	def _validate_feature_key_pattern(self) -> None:
		if not self.feature_key:
			raise frappe.ValidationError(_("Feature Key is required."))

		if not _FEATURE_KEY_PATTERN.match(self.feature_key):
			raise frappe.ValidationError(
				_(
					"Feature Key {0} is invalid. Use lower-case letters, numbers, dots, underscores, or hyphens."
				).format(self.feature_key)
			)
