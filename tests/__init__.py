# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes


if TYPE_CHECKING:
    from flext_grpc import d, e, h, r, s, x

    from . import unit as unit
    from .conftest import clean_container, sample_grpc_config, test_addresses
    from .constants import TestsFlextGrpcConstants, TestsFlextGrpcConstants as c
    from .models import TestsFlextGrpcModels, TestsFlextGrpcModels as m, tm
    from .protocols import TestsFlextGrpcProtocols, TestsFlextGrpcProtocols as p
    from .typings import TestsFlextGrpcTypes, TestsFlextGrpcTypes as t
    from .unit.test_api import TestFlextGrpc
    from .unit.test_config import TestFlextGrpcSettings
    from .unit.test_constants import TestFlextGrpcConstants
    from .unit.test_entities import FlextGrpcEntities, TestFlextGrpcEntities
    from .unit.test_errors import (
        TestErrorIntegration,
        TestFlextGrpcConnectionError,
        TestFlextGrpcError,
        TestFlextGrpcSettingsurationError,
        TestFlextGrpcTimeoutError,
        TestFlextGrpcValidationError,
    )
    from .unit.test_models import TestFlextGrpcModels
    from .unit.test_protocols import TestFlextGrpcProtocols
    from .unit.test_services import TestFlextGrpcServices
    from .unit.test_typings import TestFlextGrpcTypes
    from .unit.test_utilities import TestFlextGrpcUtilities
    from .utilities import TestsFlextGrpcUtilities, TestsFlextGrpcUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextGrpcEntities": ("tests.unit.test_entities", "FlextGrpcEntities"),
    "TestErrorIntegration": ("tests.unit.test_errors", "TestErrorIntegration"),
    "TestFlextGrpc": ("tests.unit.test_api", "TestFlextGrpc"),
    "TestFlextGrpcConnectionError": (
        "tests.unit.test_errors",
        "TestFlextGrpcConnectionError",
    ),
    "TestFlextGrpcConstants": ("tests.unit.test_constants", "TestFlextGrpcConstants"),
    "TestFlextGrpcEntities": ("tests.unit.test_entities", "TestFlextGrpcEntities"),
    "TestFlextGrpcError": ("tests.unit.test_errors", "TestFlextGrpcError"),
    "TestFlextGrpcModels": ("tests.unit.test_models", "TestFlextGrpcModels"),
    "TestFlextGrpcProtocols": ("tests.unit.test_protocols", "TestFlextGrpcProtocols"),
    "TestFlextGrpcServices": ("tests.unit.test_services", "TestFlextGrpcServices"),
    "TestFlextGrpcSettings": ("tests.unit.test_config", "TestFlextGrpcSettings"),
    "TestFlextGrpcSettingsurationError": (
        "tests.unit.test_errors",
        "TestFlextGrpcSettingsurationError",
    ),
    "TestFlextGrpcTimeoutError": (
        "tests.unit.test_errors",
        "TestFlextGrpcTimeoutError",
    ),
    "TestFlextGrpcTypes": ("tests.unit.test_typings", "TestFlextGrpcTypes"),
    "TestFlextGrpcUtilities": ("tests.unit.test_utilities", "TestFlextGrpcUtilities"),
    "TestFlextGrpcValidationError": (
        "tests.unit.test_errors",
        "TestFlextGrpcValidationError",
    ),
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


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
