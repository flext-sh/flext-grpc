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
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_grpc import (
        conftest,
        constants,
        models,
        protocols,
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
        unit,
        utilities,
    )
    from flext_grpc.conftest import clean_container, sample_grpc_config, test_addresses
    from flext_grpc.constants import FlextGrpcTestConstants, FlextGrpcTestConstants as c
    from flext_grpc.models import FlextGrpcTestModels, FlextGrpcTestModels as m
    from flext_grpc.protocols import FlextGrpcTestProtocols, FlextGrpcTestProtocols as p
    from flext_grpc.typings import FlextGrpcTestTypes, FlextGrpcTestTypes as t
    from flext_grpc.unit import (
        TestFlextGrpc,
        TestFlextGrpcConstants,
        TestFlextGrpcEntities,
        TestFlextGrpcError,
        TestFlextGrpcModels,
        TestFlextGrpcServices,
        TestFlextGrpcSettings,
        TestFlextGrpcTypes,
        Testp,
        Testu,
    )
    from flext_grpc.utilities import FlextGrpcTestUtilities, FlextGrpcTestUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    ("flext_grpc.unit",),
    {
        "FlextGrpcTestConstants": "flext_grpc.constants",
        "FlextGrpcTestModels": "flext_grpc.models",
        "FlextGrpcTestProtocols": "flext_grpc.protocols",
        "FlextGrpcTestTypes": "flext_grpc.typings",
        "FlextGrpcTestUtilities": "flext_grpc.utilities",
        "c": ("flext_grpc.constants", "FlextGrpcTestConstants"),
        "clean_container": "flext_grpc.conftest",
        "conftest": "flext_grpc.conftest",
        "constants": "flext_grpc.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_grpc.models", "FlextGrpcTestModels"),
        "models": "flext_grpc.models",
        "p": ("flext_grpc.protocols", "FlextGrpcTestProtocols"),
        "protocols": "flext_grpc.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "sample_grpc_config": "flext_grpc.conftest",
        "t": ("flext_grpc.typings", "FlextGrpcTestTypes"),
        "test_addresses": "flext_grpc.conftest",
        "test_api": "flext_grpc.test_api",
        "test_config": "flext_grpc.test_config",
        "test_constants": "flext_grpc.test_constants",
        "test_entities": "flext_grpc.test_entities",
        "test_errors": "flext_grpc.test_errors",
        "test_models": "flext_grpc.test_models",
        "test_protocols": "flext_grpc.test_protocols",
        "test_services": "flext_grpc.test_services",
        "test_typings": "flext_grpc.test_typings",
        "test_utilities": "flext_grpc.test_utilities",
        "typings": "flext_grpc.typings",
        "u": ("flext_grpc.utilities", "FlextGrpcTestUtilities"),
        "unit": "flext_grpc.unit",
        "utilities": "flext_grpc.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
