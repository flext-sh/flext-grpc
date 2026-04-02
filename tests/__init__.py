# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_tests import d, e, h, r, s, x

    from tests import conftest, constants, models, protocols, typings, unit, utilities
    from tests.conftest import clean_container, sample_grpc_config, test_addresses
    from tests.constants import FlextGrpcTestConstants, FlextGrpcTestConstants as c
    from tests.models import FlextGrpcTestModels, FlextGrpcTestModels as m
    from tests.protocols import FlextGrpcTestProtocols, FlextGrpcTestProtocols as p
    from tests.typings import FlextGrpcTestTypes, FlextGrpcTestTypes as t
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
    from tests.utilities import FlextGrpcTestUtilities, FlextGrpcTestUtilities as u

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
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
        "d": "flext_tests",
        "e": "flext_tests",
        "h": "flext_tests",
        "m": ("tests.models", "FlextGrpcTestModels"),
        "models": "tests.models",
        "p": ("tests.protocols", "FlextGrpcTestProtocols"),
        "protocols": "tests.protocols",
        "r": "flext_tests",
        "s": "flext_tests",
        "sample_grpc_config": "tests.conftest",
        "t": ("tests.typings", "FlextGrpcTestTypes"),
        "test_addresses": "tests.conftest",
        "typings": "tests.typings",
        "u": ("tests.utilities", "FlextGrpcTestUtilities"),
        "unit": "tests.unit",
        "utilities": "tests.utilities",
        "x": "flext_tests",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
