"""Extensions to the Frappe User DocType."""
from __future__ import annotations

from typing import Iterable

from . import service


class UserPermissionMixin:
	"""Mixin attached to Frappe's User Doctype at runtime."""

	def get_department_permissions(self, permission_flag: str | None = None) -> list[dict[str, object]]:
		"""Return Department Permission rows linked to this user."""
		return service.get_user_department_permissions(
			user=self.name,
			permission_flag=permission_flag,
		)

	def has_department_permission(self, department: str, permission_flag: str = "can_read") -> bool:
		"""Return True when the user has the requested permission for the department."""
		return service.has_department_permission(
			user=self.name,
			department=department,
			permission_flag=permission_flag,
		)

	def get_accessible_departments(
		self, permission_flag: str = "can_read", include_inactive: bool = False
	) -> list[str]:
		"""Return departments accessible to this user for the supplied permission flag."""
		return service.get_accessible_departments(
			user=self.name,
			permission_flag=permission_flag,
			include_inactive=include_inactive,
		)

	@staticmethod
	def get_permission_flags() -> Iterable[str]:
		"""Expose valid department permission flags."""
		return service.get_permission_flags()


