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
    from tests.unit.test_api import *
    from tests.unit.test_config import *
    from tests.unit.test_constants import *
    from tests.unit.test_entities import *
    from tests.unit.test_errors import *
    from tests.unit.test_models import *
    from tests.unit.test_protocols import *
    from tests.unit.test_services import *
    from tests.unit.test_typings import *
    from tests.unit.test_utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
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
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
