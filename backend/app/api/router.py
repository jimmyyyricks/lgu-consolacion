"""
Master API Router - Consolidated API Layer
========================================
Central hub connecting all routes in the consolidated API structure.

Route groups:
  AUTH    (/api/auth/*)      — staff authentication
  CONTENT (/api/content/*)   — public records and staff publishing
  SYSTEM  (/api/*)           — first-run setup and health
"""
from importlib import import_module
from collections.abc import Sequence
from enum import Enum
from typing import cast

from fastapi import APIRouter

# Create master router
api_router = APIRouter()


def _include_route_modules(
    module_paths: Sequence[str], *, prefix: str | None = None, tags: Sequence[str | Enum]
) -> None:
    for module_path in module_paths:
        router = import_module(module_path).router
        api_router.include_router(router, prefix=prefix or "", tags=cast(list[str | Enum], list(tags)))


SYSTEM_ROUTE_MODULES = [
    "app.api.system.auth",
    "app.api.system.setup",
    "app.api.system.health",
    "app.api.system.version",
]

CONTENT_ROUTE_MODULES = [
    "app.api.content",
]

_include_route_modules(SYSTEM_ROUTE_MODULES, tags=["System"])
_include_route_modules(CONTENT_ROUTE_MODULES, prefix="", tags=["Public Content"])

__all__ = ["api_router"]
