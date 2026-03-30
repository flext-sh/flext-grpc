# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import conftest, constants, models, protocols, typings, unit, utilities
    from tests.conftest import clean_container, sample_grpc_config, test_addresses
    from tests.constants import FlextGrpcTestConstants, FlextGrpcTestConstants as c
    from tests.models import FlextGrpcTestModels, FlextGrpcTestModels as m
    from tests.protocols import FlextGrpcTestProtocols, FlextGrpcTestProtocols as p
    from tests.typings import FlextGrpcTestTypes, FlextGrpcTestTypes as t
    from tests.unit import (
        test_api,
        test_config,
        test_constants,
        test_entities,
        test_errors,
        test_models,
        test_protocols,
        test_services,
        test_typings,
        test_utilities,
    )
    from tests.unit.test_api import TestFlextGrpc
    from tests.unit.test_config import TestFlextGrpcSettings
    from tests.unit.test_constants import TestFlextGrpcConstants
    from tests.unit.test_entities import TestFlextGrpcEntities
    from tests.unit.test_errors import (
        TestErrorIntegration,
        TestFlextGrpcConfigurationError,
        TestFlextGrpcConnectionError,
        TestFlextGrpcError,
        TestFlextGrpcTimeoutError,
        TestFlextGrpcValidationError,
    )
    from tests.unit.test_models import TestFlextGrpcModels
    from tests.unit.test_protocols import TestFlextGrpcProtocols
    from tests.unit.test_services import TestFlextGrpcServices
    from tests.unit.test_typings import TestFlextGrpcTypes
    from tests.unit.test_utilities import TestFlextGrpcUtilities
    from tests.utilities import FlextGrpcTestUtilities, FlextGrpcTestUtilities as u

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextGrpcTestConstants": ["tests.constants", "FlextGrpcTestConstants"],
    "FlextGrpcTestModels": ["tests.models", "FlextGrpcTestModels"],
    "FlextGrpcTestProtocols": ["tests.protocols", "FlextGrpcTestProtocols"],
    "FlextGrpcTestTypes": ["tests.typings", "FlextGrpcTestTypes"],
    "FlextGrpcTestUtilities": ["tests.utilities", "FlextGrpcTestUtilities"],
    "TestErrorIntegration": ["tests.unit.test_errors", "TestErrorIntegration"],
    "TestFlextGrpc": ["tests.unit.test_api", "TestFlextGrpc"],
    "TestFlextGrpcConfigurationError": [
        "tests.unit.test_errors",
        "TestFlextGrpcConfigurationError",
    ],
    "TestFlextGrpcConnectionError": [
        "tests.unit.test_errors",
        "TestFlextGrpcConnectionError",
    ],
    "TestFlextGrpcConstants": ["tests.unit.test_constants", "TestFlextGrpcConstants"],
    "TestFlextGrpcEntities": ["tests.unit.test_entities", "TestFlextGrpcEntities"],
    "TestFlextGrpcError": ["tests.unit.test_errors", "TestFlextGrpcError"],
    "TestFlextGrpcModels": ["tests.unit.test_models", "TestFlextGrpcModels"],
    "TestFlextGrpcProtocols": ["tests.unit.test_protocols", "TestFlextGrpcProtocols"],
    "TestFlextGrpcServices": ["tests.unit.test_services", "TestFlextGrpcServices"],
    "TestFlextGrpcSettings": ["tests.unit.test_config", "TestFlextGrpcSettings"],
    "TestFlextGrpcTimeoutError": [
        "tests.unit.test_errors",
        "TestFlextGrpcTimeoutError",
    ],
    "TestFlextGrpcTypes": ["tests.unit.test_typings", "TestFlextGrpcTypes"],
    "TestFlextGrpcUtilities": ["tests.unit.test_utilities", "TestFlextGrpcUtilities"],
    "TestFlextGrpcValidationError": [
        "tests.unit.test_errors",
        "TestFlextGrpcValidationError",
    ],
    "c": ["tests.constants", "FlextGrpcTestConstants"],
    "clean_container": ["tests.conftest", "clean_container"],
    "conftest": ["tests.conftest", ""],
    "constants": ["tests.constants", ""],
    "d": ["flext_tests", "d"],
    "e": ["flext_tests", "e"],
    "h": ["flext_tests", "h"],
    "m": ["tests.models", "FlextGrpcTestModels"],
    "models": ["tests.models", ""],
    "p": ["tests.protocols", "FlextGrpcTestProtocols"],
    "protocols": ["tests.protocols", ""],
    "r": ["flext_tests", "r"],
    "s": ["flext_tests", "s"],
    "sample_grpc_config": ["tests.conftest", "sample_grpc_config"],
    "t": ["tests.typings", "FlextGrpcTestTypes"],
    "test_addresses": ["tests.conftest", "test_addresses"],
    "test_api": ["tests.unit.test_api", ""],
    "test_config": ["tests.unit.test_config", ""],
    "test_constants": ["tests.unit.test_constants", ""],
    "test_entities": ["tests.unit.test_entities", ""],
    "test_errors": ["tests.unit.test_errors", ""],
    "test_models": ["tests.unit.test_models", ""],
    "test_protocols": ["tests.unit.test_protocols", ""],
    "test_services": ["tests.unit.test_services", ""],
    "test_typings": ["tests.unit.test_typings", ""],
    "test_utilities": ["tests.unit.test_utilities", ""],
    "typings": ["tests.typings", ""],
    "u": ["tests.utilities", "FlextGrpcTestUtilities"],
    "unit": ["tests.unit", ""],
    "utilities": ["tests.utilities", ""],
    "x": ["flext_tests", "x"],
}

__all__ = [
    "FlextGrpcTestConstants",
    "FlextGrpcTestModels",
    "FlextGrpcTestProtocols",
    "FlextGrpcTestTypes",
    "FlextGrpcTestUtilities",
    "TestErrorIntegration",
    "TestFlextGrpc",
    "TestFlextGrpcConfigurationError",
    "TestFlextGrpcConnectionError",
    "TestFlextGrpcConstants",
    "TestFlextGrpcEntities",
    "TestFlextGrpcError",
    "TestFlextGrpcModels",
    "TestFlextGrpcProtocols",
    "TestFlextGrpcServices",
    "TestFlextGrpcSettings",
    "TestFlextGrpcTimeoutError",
    "TestFlextGrpcTypes",
    "TestFlextGrpcUtilities",
    "TestFlextGrpcValidationError",
    "c",
    "clean_container",
    "conftest",
    "constants",
    "d",
    "e",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "r",
    "s",
    "sample_grpc_config",
    "t",
    "test_addresses",
    "test_api",
    "test_config",
    "test_constants",
    "test_entities",
    "test_errors",
    "test_models",
    "test_protocols",
    "test_services",
    "test_typings",
    "test_utilities",
    "typings",
    "u",
    "unit",
    "utilities",
    "x",
]


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


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


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
