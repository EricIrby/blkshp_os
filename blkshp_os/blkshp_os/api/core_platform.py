"""Core Platform API endpoints."""

from __future__ import annotations

from typing import Any

import frappe
from blkshp_os.core_platform.services import (
    get_feature_matrix_for_user,
    get_user_profile,
)
from frappe.utils import cint


@frappe.whitelist()
def get_feature_matrix(refresh: int | str | None = None) -> dict[str, Any]:
    """Return the feature matrix for the current tenant user.

    The response is strictly read-only; feature toggles remain managed solely by
    BLKSHP Operations. Pass ``refresh=1`` to bypass cached plan data.
    """
    force_refresh = bool(cint(refresh)) if refresh is not None else False
    return get_feature_matrix_for_user(refresh=force_refresh)


@frappe.whitelist()
def get_profile(refresh: int | str | None = None) -> dict[str, Any]:
    """Return the authenticated user's profile summary.

    Includes tenant company, department access, subscription snapshot, and
    permission summary. Pass ``refresh=1`` to bypass cached plan data.
    """
    force_refresh = bool(cint(refresh)) if refresh is not None else False
    return get_user_profile(refresh=force_refresh)
