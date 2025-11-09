from __future__ import annotations

from typing import Any, Mapping


def create_custom_field(
	doctype: str,
	df: Mapping[str, Any],
	ignore_validate: bool | None = ...,
	is_system_generated: bool | None = ...,
) -> Any: ...

