# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import *

    from tests import conftest, constants, models, protocols, typings, utilities
    from tests.conftest import *
    from tests.constants import *
    from tests.models import *
    from tests.protocols import *
    from tests.typings import *
    from tests.unit import *
    from tests.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextGrpcTestConstants": "tests.constants",
    "FlextGrpcTestModels": "tests.models",
    "FlextGrpcTestProtocols": "tests.protocols",
    "FlextGrpcTestTypes": "tests.typings",
    "FlextGrpcTestUtilities": "tests.utilities",
    "TestErrorIntegration": "tests.unit.test_errors",
    "TestFlextGrpc": "tests.unit.test_api",
    "TestFlextGrpcConfigurationError": "tests.unit.test_errors",
    "TestFlextGrpcConnectionError": "tests.unit.test_errors",
    "TestFlextGrpcConstants": "tests.unit.test_constants",
    "TestFlextGrpcEntities": "tests.unit.test_entities",
    "TestFlextGrpcError": "tests.unit.test_errors",
    "TestFlextGrpcModels": "tests.unit.test_models",
    "TestFlextGrpcProtocols": "tests.unit.test_protocols",
    "TestFlextGrpcServices": "tests.unit.test_services",
    "TestFlextGrpcSettings": "tests.unit.test_config",
    "TestFlextGrpcTimeoutError": "tests.unit.test_errors",
    "TestFlextGrpcTypes": "tests.unit.test_typings",
    "TestFlextGrpcUtilities": "tests.unit.test_utilities",
    "TestFlextGrpcValidationError": "tests.unit.test_errors",
    "c": ["tests.constants", "FlextGrpcTestConstants"],
    "clean_container": "tests.conftest",
    "conftest": "tests.conftest",
    "constants": "tests.constants",
    "d": "flext_tests",
    "e": "flext_tests",
    "h": "flext_tests",
    "m": ["tests.models", "FlextGrpcTestModels"],
    "models": "tests.models",
    "p": ["tests.protocols", "FlextGrpcTestProtocols"],
    "protocols": "tests.protocols",
    "r": "flext_tests",
    "s": "flext_tests",
    "sample_grpc_config": "tests.conftest",
    "t": ["tests.typings", "FlextGrpcTestTypes"],
    "test_addresses": "tests.conftest",
    "test_api": "tests.unit.test_api",
    "test_config": "tests.unit.test_config",
    "test_constants": "tests.unit.test_constants",
    "test_entities": "tests.unit.test_entities",
    "test_errors": "tests.unit.test_errors",
    "test_models": "tests.unit.test_models",
    "test_protocols": "tests.unit.test_protocols",
    "test_services": "tests.unit.test_services",
    "test_typings": "tests.unit.test_typings",
    "test_utilities": "tests.unit.test_utilities",
    "typings": "tests.typings",
    "u": ["tests.utilities", "FlextGrpcTestUtilities"],
    "unit": "tests.unit",
    "utilities": "tests.utilities",
    "x": "flext_tests",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
