# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT gRPC Tests - Test infrastructure and utilities.

Provides TestsFlextGrpc classes extending FlextTests and FlextGrpc for comprehensive testing.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from tests.conftest import clean_container, sample_grpc_config, test_addresses
    from tests.constants import TestsFlextGrpcConstants, c
    from tests.models import TestsFlextGrpcModels, m, tm
    from tests.protocols import TestsFlextGrpcProtocols, p
    from tests.typings import TestsFlextGrpcTypes
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
    from tests.unit.test_typings import TestFlextGrpcTypes, TestFlextGrpcTypes as t
    from tests.unit.test_utilities import TestFlextGrpcUtilities
    from tests.utilities import TestsFlextGrpcUtilities, u

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
    "c": ("tests.constants", "c"),
    "clean_container": ("tests.conftest", "clean_container"),
    "m": ("tests.models", "m"),
    "p": ("tests.protocols", "p"),
    "sample_grpc_config": ("tests.conftest", "sample_grpc_config"),
    "t": ("tests.unit.test_typings", "TestFlextGrpcTypes"),
    "test_addresses": ("tests.conftest", "test_addresses"),
    "tm": ("tests.models", "tm"),
    "u": ("tests.utilities", "u"),
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
    "m",
    "p",
    "sample_grpc_config",
    "t",
    "test_addresses",
    "tm",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
