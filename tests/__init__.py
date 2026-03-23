# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import unit
    from tests.conftest import clean_container, sample_grpc_config, test_addresses
    from tests.constants import FlextGrpcTestConstants, FlextGrpcTestConstants as c
    from tests.models import FlextGrpcTestModels, FlextGrpcTestModels as m
    from tests.protocols import FlextGrpcTestProtocols, FlextGrpcTestProtocols as p
    from tests.typings import FlextGrpcTestTypes, FlextGrpcTestTypes as t
    from tests.unit.test_api import TestFlextGrpc
    from tests.unit.test_config import TestFlextGrpcSettings
    from tests.unit.test_constants import TestFlextGrpcConstants
    from tests.unit.test_entities import FlextGrpcEntities, TestFlextGrpcEntities
    from tests.unit.test_errors import (
        TestErrorIntegration,
        TestFlextGrpcConnectionError,
        TestFlextGrpcError,
        TestFlextGrpcSettingsurationError,
        TestFlextGrpcTimeoutError,
        TestFlextGrpcValidationError,
    )
    from tests.unit.test_models import TestFlextGrpcModels
    from tests.unit.test_protocols import TestFlextGrpcProtocols
    from tests.unit.test_services import TestFlextGrpcServices
    from tests.unit.test_typings import TestFlextGrpcTypes
    from tests.unit.test_utilities import TestFlextGrpcUtilities
    from tests.utilities import FlextGrpcTestUtilities, FlextGrpcTestUtilities as u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextGrpcEntities": ("tests.unit.test_entities", "FlextGrpcEntities"),
    "FlextGrpcTestConstants": ("tests.constants", "FlextGrpcTestConstants"),
    "FlextGrpcTestModels": ("tests.models", "FlextGrpcTestModels"),
    "FlextGrpcTestProtocols": ("tests.protocols", "FlextGrpcTestProtocols"),
    "FlextGrpcTestTypes": ("tests.typings", "FlextGrpcTestTypes"),
    "FlextGrpcTestUtilities": ("tests.utilities", "FlextGrpcTestUtilities"),
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
    "c": ("tests.constants", "FlextGrpcTestConstants"),
    "clean_container": ("tests.conftest", "clean_container"),
    "d": ("flext_tests", "d"),
    "e": ("flext_tests", "e"),
    "h": ("flext_tests", "h"),
    "m": ("tests.models", "FlextGrpcTestModels"),
    "p": ("tests.protocols", "FlextGrpcTestProtocols"),
    "r": ("flext_tests", "r"),
    "s": ("flext_tests", "s"),
    "sample_grpc_config": ("tests.conftest", "sample_grpc_config"),
    "t": ("tests.typings", "FlextGrpcTestTypes"),
    "test_addresses": ("tests.conftest", "test_addresses"),
    "u": ("tests.utilities", "FlextGrpcTestUtilities"),
    "unit": ("tests.unit", ""),
    "x": ("flext_tests", "x"),
}

__all__ = [
    "FlextGrpcEntities",
    "FlextGrpcTestConstants",
    "FlextGrpcTestModels",
    "FlextGrpcTestProtocols",
    "FlextGrpcTestTypes",
    "FlextGrpcTestUtilities",
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
