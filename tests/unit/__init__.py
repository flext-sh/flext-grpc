# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT gRPC Unit Tests Package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
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
    from tests.unit.test_protocols import Testp
    from tests.unit.test_services import TestFlextGrpcServices
    from tests.unit.test_typings import TestFlextGrpcTypes
    from tests.unit.test_utilities import Testu

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "TestErrorIntegration": "tests.unit.test_errors",
    "TestFlextGrpc": "tests.unit.test_api",
    "TestFlextGrpcConfigurationError": "tests.unit.test_errors",
    "TestFlextGrpcConnectionError": "tests.unit.test_errors",
    "TestFlextGrpcConstants": "tests.unit.test_constants",
    "TestFlextGrpcEntities": "tests.unit.test_entities",
    "TestFlextGrpcError": "tests.unit.test_errors",
    "TestFlextGrpcModels": "tests.unit.test_models",
    "TestFlextGrpcServices": "tests.unit.test_services",
    "TestFlextGrpcSettings": "tests.unit.test_config",
    "TestFlextGrpcTimeoutError": "tests.unit.test_errors",
    "TestFlextGrpcTypes": "tests.unit.test_typings",
    "TestFlextGrpcValidationError": "tests.unit.test_errors",
    "Testp": "tests.unit.test_protocols",
    "Testu": "tests.unit.test_utilities",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
