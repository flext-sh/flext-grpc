# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from tests.conftest import clean_container, sample_grpc_config, test_addresses
from tests.constants import FlextGrpcTestConstants, FlextGrpcTestConstants as c
from tests.models import FlextGrpcTestModels, FlextGrpcTestModels as m
from tests.protocols import FlextGrpcTestProtocols, FlextGrpcTestProtocols as p
from tests.typings import FlextGrpcTestTypes, FlextGrpcTestTypes as t
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
from tests.utilities import FlextGrpcTestUtilities, FlextGrpcTestUtilities as u

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants

    constants = _tests_constants
    import tests.models as _tests_models

    models = _tests_models
    import tests.protocols as _tests_protocols

    protocols = _tests_protocols
    import tests.typings as _tests_typings

    typings = _tests_typings
    import tests.unit as _tests_unit

    unit = _tests_unit
    import tests.unit.test_api as _tests_unit_test_api

    test_api = _tests_unit_test_api
    import tests.unit.test_config as _tests_unit_test_config

    test_config = _tests_unit_test_config
    import tests.unit.test_constants as _tests_unit_test_constants

    test_constants = _tests_unit_test_constants
    import tests.unit.test_entities as _tests_unit_test_entities

    test_entities = _tests_unit_test_entities
    import tests.unit.test_errors as _tests_unit_test_errors

    test_errors = _tests_unit_test_errors
    import tests.unit.test_models as _tests_unit_test_models

    test_models = _tests_unit_test_models
    import tests.unit.test_protocols as _tests_unit_test_protocols

    test_protocols = _tests_unit_test_protocols
    import tests.unit.test_services as _tests_unit_test_services

    test_services = _tests_unit_test_services
    import tests.unit.test_typings as _tests_unit_test_typings

    test_typings = _tests_unit_test_typings
    import tests.unit.test_utilities as _tests_unit_test_utilities

    test_utilities = _tests_unit_test_utilities
    import tests.utilities as _tests_utilities

    utilities = _tests_utilities

    _ = (
        FlextGrpcTestConstants,
        FlextGrpcTestModels,
        FlextGrpcTestProtocols,
        FlextGrpcTestTypes,
        FlextGrpcTestUtilities,
        TestErrorIntegration,
        TestFlextGrpc,
        TestFlextGrpcConfigurationError,
        TestFlextGrpcConnectionError,
        TestFlextGrpcConstants,
        TestFlextGrpcEntities,
        TestFlextGrpcError,
        TestFlextGrpcModels,
        TestFlextGrpcServices,
        TestFlextGrpcSettings,
        TestFlextGrpcTimeoutError,
        TestFlextGrpcTypes,
        TestFlextGrpcValidationError,
        Testp,
        Testu,
        c,
        clean_container,
        conftest,
        constants,
        d,
        e,
        h,
        m,
        models,
        p,
        protocols,
        r,
        s,
        sample_grpc_config,
        t,
        test_addresses,
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
        typings,
        u,
        unit,
        utilities,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    ("tests.unit",),
    {
        "FlextGrpcTestConstants": "tests.constants",
        "FlextGrpcTestModels": "tests.models",
        "FlextGrpcTestProtocols": "tests.protocols",
        "FlextGrpcTestTypes": "tests.typings",
        "FlextGrpcTestUtilities": "tests.utilities",
        "c": ("tests.constants", "FlextGrpcTestConstants"),
        "clean_container": "tests.conftest",
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("tests.models", "FlextGrpcTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextGrpcTestProtocols"),
        "protocols": "tests.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "sample_grpc_config": "tests.conftest",
        "t": ("tests.typings", "FlextGrpcTestTypes"),
        "test_addresses": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextGrpcTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)

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
    "TestFlextGrpcServices",
    "TestFlextGrpcSettings",
    "TestFlextGrpcTimeoutError",
    "TestFlextGrpcTypes",
    "TestFlextGrpcValidationError",
    "Testp",
    "Testu",
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
