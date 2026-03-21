# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_grpc import d, e, h, r, s, x

    from . import unit as unit
    from .conftest import clean_container, sample_grpc_config, test_addresses
    from .constants import TestsFlextGrpcConstants, TestsFlextGrpcConstants as c
    from .models import TestsFlextGrpcModels, TestsFlextGrpcModels as m, tm
    from .protocols import TestsFlextGrpcProtocols, TestsFlextGrpcProtocols as p
    from .typings import TestsFlextGrpcTypes, TestsFlextGrpcTypes as t
    from .unit import (
        FlextGrpcEntities,
        TestErrorIntegration,
        TestFlextGrpc,
        TestFlextGrpcConnectionError,
        TestFlextGrpcConstants,
        TestFlextGrpcEntities,
        TestFlextGrpcError,
        TestFlextGrpcModels,
        TestFlextGrpcProtocols,
        TestFlextGrpcServices,
        TestFlextGrpcSettings,
        TestFlextGrpcSettingsurationError,
        TestFlextGrpcTimeoutError,
        TestFlextGrpcTypes,
        TestFlextGrpcUtilities,
        TestFlextGrpcValidationError,
    )
    from .utilities import TestsFlextGrpcUtilities, TestsFlextGrpcUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextGrpcEntities": ("tests.unit", "FlextGrpcEntities"),
    "TestErrorIntegration": ("tests.unit", "TestErrorIntegration"),
    "TestFlextGrpc": ("tests.unit", "TestFlextGrpc"),
    "TestFlextGrpcConnectionError": ("tests.unit", "TestFlextGrpcConnectionError"),
    "TestFlextGrpcConstants": ("tests.unit", "TestFlextGrpcConstants"),
    "TestFlextGrpcEntities": ("tests.unit", "TestFlextGrpcEntities"),
    "TestFlextGrpcError": ("tests.unit", "TestFlextGrpcError"),
    "TestFlextGrpcModels": ("tests.unit", "TestFlextGrpcModels"),
    "TestFlextGrpcProtocols": ("tests.unit", "TestFlextGrpcProtocols"),
    "TestFlextGrpcServices": ("tests.unit", "TestFlextGrpcServices"),
    "TestFlextGrpcSettings": ("tests.unit", "TestFlextGrpcSettings"),
    "TestFlextGrpcSettingsurationError": (
        "tests.unit",
        "TestFlextGrpcSettingsurationError",
    ),
    "TestFlextGrpcTimeoutError": ("tests.unit", "TestFlextGrpcTimeoutError"),
    "TestFlextGrpcTypes": ("tests.unit", "TestFlextGrpcTypes"),
    "TestFlextGrpcUtilities": ("tests.unit", "TestFlextGrpcUtilities"),
    "TestFlextGrpcValidationError": ("tests.unit", "TestFlextGrpcValidationError"),
    "TestsFlextGrpcConstants": ("tests.constants", "TestsFlextGrpcConstants"),
    "TestsFlextGrpcModels": ("tests.models", "TestsFlextGrpcModels"),
    "TestsFlextGrpcProtocols": ("tests.protocols", "TestsFlextGrpcProtocols"),
    "TestsFlextGrpcTypes": ("tests.typings", "TestsFlextGrpcTypes"),
    "TestsFlextGrpcUtilities": ("tests.utilities", "TestsFlextGrpcUtilities"),
    "c": ("tests.constants", "TestsFlextGrpcConstants"),
    "clean_container": ("tests.conftest", "clean_container"),
    "d": ("flext_grpc", "d"),
    "e": ("flext_grpc", "e"),
    "h": ("flext_grpc", "h"),
    "m": ("tests.models", "TestsFlextGrpcModels"),
    "p": ("tests.protocols", "TestsFlextGrpcProtocols"),
    "r": ("flext_grpc", "r"),
    "s": ("flext_grpc", "s"),
    "sample_grpc_config": ("tests.conftest", "sample_grpc_config"),
    "t": ("tests.typings", "TestsFlextGrpcTypes"),
    "test_addresses": ("tests.conftest", "test_addresses"),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "TestsFlextGrpcUtilities"),
    "unit": ("tests.unit", ""),
    "x": ("flext_grpc", "x"),
}

__all__ = [
    "FlextGrpcEntities",
    "TestErrorIntegration",
    "TestFlextGrpc",
    "TestFlextGrpcConnectionError",
    "TestFlextGrpcConstants",
    "TestFlextGrpcEntities",
    "TestFlextGrpcError",
    "TestFlextGrpcModels",
    "TestFlextGrpcProtocols",
    "TestFlextGrpcServices",
    "TestFlextGrpcSettings",
    "TestFlextGrpcSettingsurationError",
    "TestFlextGrpcTimeoutError",
    "TestFlextGrpcTypes",
    "TestFlextGrpcUtilities",
    "TestFlextGrpcValidationError",
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcUtilities",
    "c",
    "clean_container",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "sample_grpc_config",
    "t",
    "test_addresses",
    "tm",
    "u",
    "unit",
    "x",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
