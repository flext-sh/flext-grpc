# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from tests import (
        conftest as conftest,
        constants as constants,
        models as models,
        protocols as protocols,
        typings as typings,
        unit as unit,
        utilities as utilities,
    )
    from tests.conftest import (
        clean_container as clean_container,
        sample_grpc_config as sample_grpc_config,
        test_addresses as test_addresses,
    )
    from tests.constants import (
        FlextGrpcTestConstants as FlextGrpcTestConstants,
        FlextGrpcTestConstants as c,
    )
    from tests.models import (
        FlextGrpcTestModels as FlextGrpcTestModels,
        FlextGrpcTestModels as m,
    )
    from tests.protocols import (
        FlextGrpcTestProtocols as FlextGrpcTestProtocols,
        FlextGrpcTestProtocols as p,
    )
    from tests.typings import (
        FlextGrpcTestTypes as FlextGrpcTestTypes,
        FlextGrpcTestTypes as t,
    )
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
    from tests.utilities import (
        FlextGrpcTestUtilities as FlextGrpcTestUtilities,
        FlextGrpcTestUtilities as u,
    )

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

_EXPORTS: Sequence[str] = [
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
