"""FLEXT gRPC Tests - Test infrastructure and utilities.

Provides TestsFlextGrpc classes extending FlextTests and FlextGrpc for comprehensive testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from .constants import TestsFlextGrpcConstants, TestsFlextGrpcConstants as c
    from .models import TestsFlextGrpcModels, TestsFlextGrpcModels as m, tm
    from .utilities import TestsFlextGrpcUtilities, TestsFlextGrpcUtilities as u
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "TestsFlextGrpcConstants": ("tests.constants", "TestsFlextGrpcConstants"),
    "TestsFlextGrpcModels": ("tests.models", "TestsFlextGrpcModels"),
    "TestsFlextGrpcUtilities": ("tests.utilities", "TestsFlextGrpcUtilities"),
    "c": ("tests.constants", "TestsFlextGrpcConstants"),
    "m": ("tests.models", "TestsFlextGrpcModels"),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "TestsFlextGrpcUtilities"),
}
__all__ = [
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcUtilities",
    "c",
    "m",
    "tm",
    "u",
]


def __getattr__(name: str):
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
