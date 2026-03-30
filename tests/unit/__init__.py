# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT gRPC Unit Tests Package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests.unit import (
        test_api as test_api,
        test_config as test_config,
        test_constants as test_constants,
        test_entities as test_entities,
        test_errors as test_errors,
        test_models as test_models,
        test_protocols as test_protocols,
        test_services as test_services,
        test_typings as test_typings,
        test_utilities as test_utilities,
    )
    from tests.unit.test_api import TestFlextGrpc as TestFlextGrpc
    from tests.unit.test_config import TestFlextGrpcSettings as TestFlextGrpcSettings
    from tests.unit.test_constants import (
        TestFlextGrpcConstants as TestFlextGrpcConstants,
    )
    from tests.unit.test_entities import TestFlextGrpcEntities as TestFlextGrpcEntities
    from tests.unit.test_errors import (
        TestErrorIntegration as TestErrorIntegration,
        TestFlextGrpcConfigurationError as TestFlextGrpcConfigurationError,
        TestFlextGrpcConnectionError as TestFlextGrpcConnectionError,
        TestFlextGrpcError as TestFlextGrpcError,
        TestFlextGrpcTimeoutError as TestFlextGrpcTimeoutError,
        TestFlextGrpcValidationError as TestFlextGrpcValidationError,
    )
    from tests.unit.test_models import TestFlextGrpcModels as TestFlextGrpcModels
    from tests.unit.test_protocols import (
        TestFlextGrpcProtocols as TestFlextGrpcProtocols,
    )
    from tests.unit.test_services import TestFlextGrpcServices as TestFlextGrpcServices
    from tests.unit.test_typings import TestFlextGrpcTypes as TestFlextGrpcTypes
    from tests.unit.test_utilities import (
        TestFlextGrpcUtilities as TestFlextGrpcUtilities,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
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
}

_EXPORTS: Sequence[str] = [
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
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
