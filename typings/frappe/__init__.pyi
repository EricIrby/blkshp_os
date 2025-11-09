from __future__ import annotations

from typing import Any, Mapping, overload


class PermissionError(Exception):
	...

class UniqueValidationError(Exception):
	...


class Document:
	name: str

	def __init__(self, data: Mapping[str, Any] | None = ...) -> None: ...

	def insert(self, *, ignore_permissions: bool | None = ...) -> Document: ...


class _DatabaseModule:
	def rollback(self) -> None: ...

	def get_value(
		self,
		doctype: str,
		filters: Mapping[str, Any] | str | None = ...,
		fieldname: str | None = ...,
		*,
		as_dict: bool | None = ...,
	) -> Any: ...

	def exists(
		self,
		doctype: str,
		filters: Mapping[str, Any] | str,
	) -> str | None: ...

	def count(
		self,
		doctype: str,
		filters: Mapping[str, Any] | None = ...,
	) -> int: ...

	def has_column(self, doctype: str, fieldname: str) -> bool: ...


db: _DatabaseModule


flags: Any
session: Any


def set_user(user: str) -> None: ...

def clear_cache(*, doctype: str | None = ...) -> None: ...

def reload_doc(
	module: str,
	dt: str,
	dn: str,
	*,
	force: bool | None = ...,
	reset_permissions: bool | None = ...,
) -> Any: ...

def get_roles(user: str | None = ...) -> list[str]: ...

def get_all(
	doctype: str,
	*,
	filters: Mapping[str, Any] | None = ...,
	fields: list[str] | None = ...,
	order_by: str | None = ...,
	pluck: str | None = ...,
) -> list[Any]: ...

def get_meta(doctype: str, *, cached: bool | None = ...) -> Any: ...

def throw(message: str, exc: type[BaseException] | None = ...) -> None: ...


@overload
def get_doc(document: Mapping[str, Any]) -> Document: ...


@overload
def get_doc(
	doctype: str,
	name: str | None = ...,
	filters: Mapping[str, Any] | None = ...,
	**kwargs: Any,
) -> Document: ...


def get_doc(*args: Any, **kwargs: Any) -> Document: ...


