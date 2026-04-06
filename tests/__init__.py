# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _t.TYPE_CHECKING:
    import tests.conftest as _tests_conftest

    conftest = _tests_conftest
    import tests.constants as _tests_constants
    from tests.conftest import (
        grpc_settings,
        pytest_plugins,
        sample_grpc_config,
        test_addresses,
    )

    constants = _tests_constants
    import tests.models as _tests_models
    from tests.constants import FlextGrpcTestConstants, FlextGrpcTestConstants as c

    models = _tests_models
    import tests.protocols as _tests_protocols
    from tests.models import FlextGrpcTestModels, FlextGrpcTestModels as m

    protocols = _tests_protocols
    import tests.typings as _tests_typings
    from tests.protocols import FlextGrpcTestProtocols, FlextGrpcTestProtocols as p

    typings = _tests_typings
    import tests.unit as _tests_unit
    from tests.typings import FlextGrpcTestTypes, FlextGrpcTestTypes as t

    unit = _tests_unit
    import tests.utilities as _tests_utilities
    from tests.unit import (
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

    utilities = _tests_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.utilities import FlextGrpcTestUtilities, FlextGrpcTestUtilities as u
_LAZY_IMPORTS = merge_lazy_imports(
    ("tests.unit",),
    {
        "FlextGrpcTestConstants": ("tests.constants", "FlextGrpcTestConstants"),
        "FlextGrpcTestModels": ("tests.models", "FlextGrpcTestModels"),
        "FlextGrpcTestProtocols": ("tests.protocols", "FlextGrpcTestProtocols"),
        "FlextGrpcTestTypes": ("tests.typings", "FlextGrpcTestTypes"),
        "FlextGrpcTestUtilities": ("tests.utilities", "FlextGrpcTestUtilities"),
        "c": ("tests.constants", "FlextGrpcTestConstants"),
        "conftest": "tests.conftest",
        "constants": "tests.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "grpc_settings": ("tests.conftest", "grpc_settings"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("tests.models", "FlextGrpcTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextGrpcTestProtocols"),
        "protocols": "tests.protocols",
        "pytest_plugins": ("tests.conftest", "pytest_plugins"),
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "sample_grpc_config": ("tests.conftest", "sample_grpc_config"),
        "t": ("tests.typings", "FlextGrpcTestTypes"),
        "test_addresses": ("tests.conftest", "test_addresses"),
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextGrpcTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

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
    "conftest",
    "constants",
    "d",
    "e",
    "grpc_settings",
    "h",
    "m",
    "models",
    "p",
    "protocols",
    "pytest_plugins",
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
