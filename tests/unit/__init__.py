# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Unit package."""

from __future__ import annotations

import typing as _t

from flext_core.constants import FlextConstants as c
from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports
from flext_core.mixins import FlextMixins as x
from flext_core.models import FlextModels as m
from flext_core.protocols import FlextProtocols as p
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from flext_core.typings import FlextTypes as t
from flext_core.utilities import FlextUtilities as u
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

if _t.TYPE_CHECKING:
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

    _ = (
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
        d,
        e,
        h,
        m,
        p,
        r,
        s,
        t,
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
        u,
        x,
    )
_LAZY_IMPORTS = {
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
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("flext_core.typings", "FlextTypes"),
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
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
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
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
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
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
