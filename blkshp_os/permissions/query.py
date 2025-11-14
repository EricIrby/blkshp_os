"""Permission query helpers registered in hooks."""

from __future__ import annotations

from . import service


def department_permission_query(user: str) -> str:
    """Return permission query condition restricting Department records."""
    return service.get_department_permission_clause(user, permission_flag="can_read")
