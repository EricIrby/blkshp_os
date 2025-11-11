"""Controller for Module Activation records."""
from __future__ import annotations

import json
from typing import Any

import frappe
from frappe import _
from frappe.model.document import Document

from blkshp_os.core_platform.services import clear_subscription_context_cache


class ModuleActivation(Document):
	"""Defines module availability and feature overrides for a subscription plan."""

	def validate(self) -> None:
		self._normalize_module_key()
		self._validate_plan_module_uniqueness()
		self._validate_dependencies()
		self._validate_feature_overrides()

	def _normalize_module_key(self) -> None:
		if not self.module_key:
			return
		self.module_key = self.module_key.strip().lower()

	def _validate_plan_module_uniqueness(self) -> None:
		if not (self.plan and self.module_key):
			return

		duplicate = frappe.db.exists(
			"Module Activation",
			{
				"plan": self.plan,
				"module_key": self.module_key,
				"name": ("!=", self.name),
			},
		)

		if duplicate:
			raise frappe.ValidationError(
				_(
					"Module {0} is already defined for subscription plan {1}."
				).format(self.module_key, self.plan)
			)

	def _validate_dependencies(self) -> None:
		if not self.depends_on:
			return

		dependencies = [key.strip().lower() for key in self.depends_on.split(",") if key.strip()]
		if self.module_key and self.module_key in dependencies:
			raise frappe.ValidationError(
				_("Module {0} cannot depend on itself.").format(self.module_key)
			)

		# ensure dependencies are stored normalized
		self.depends_on = ", ".join(sorted(set(dependencies)))

	def _validate_feature_overrides(self) -> None:
		if not self.feature_overrides:
			return

		try:
			overrides: dict[str, Any] = json.loads(self.feature_overrides)
		except (TypeError, ValueError) as exc:
			raise frappe.ValidationError(
				_
				("Feature Overrides must contain valid JSON. "
				"Original error: {0}").format(exc)
			) from exc

		if not isinstance(overrides, dict):
			raise frappe.ValidationError(
				_("Feature Overrides must be a JSON object with feature keys."),
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
