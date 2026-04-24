# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)

if _t.TYPE_CHECKING:
    from flext_tests import td, tf, tk, tm, tv

    from flext_grpc import d, e, h, r, s, x
    from tests.constants import TestsFlextGrpcConstants, c
    from tests.models import TestsFlextGrpcModels, m
    from tests.protocols import TestsFlextGrpcProtocols, p
    from tests.typings import TestsFlextGrpcTypes, t
    from tests.unit.test_api import TestsFlextGrpcApi
    from tests.unit.test_config import TestsFlextGrpcConfig
    from tests.unit.test_constants import TestsFlextGrpcConstantsUnit
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
    from tests.unit.test_protocols import TestsFlextGrpcProtocolsUnit
    from tests.unit.test_services import TestFlextGrpcServiceComponents
    from tests.unit.test_typings import TestsFlextGrpcTypesUnit
    from tests.unit.test_utilities import Testu
    from tests.utilities import TestsFlextGrpcUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (".unit",),
    build_lazy_import_map(
        {
            ".constants": (
                "TestsFlextGrpcConstants",
                "c",
            ),
            ".models": (
                "TestsFlextGrpcModels",
                "m",
            ),
            ".protocols": (
                "TestsFlextGrpcProtocols",
                "p",
            ),
            ".typings": (
                "TestsFlextGrpcTypes",
                "t",
            ),
            ".unit.test_api": ("TestsFlextGrpcApi",),
            ".unit.test_config": ("TestsFlextGrpcConfig",),
            ".unit.test_constants": ("TestsFlextGrpcConstantsUnit",),
            ".unit.test_entities": ("TestFlextGrpcEntities",),
            ".unit.test_errors": (
                "TestErrorIntegration",
                "TestFlextGrpcConfigurationError",
                "TestFlextGrpcConnectionError",
                "TestFlextGrpcError",
                "TestFlextGrpcTimeoutError",
                "TestFlextGrpcValidationError",
            ),
            ".unit.test_models": ("TestFlextGrpcModels",),
            ".unit.test_protocols": ("TestsFlextGrpcProtocolsUnit",),
            ".unit.test_services": ("TestFlextGrpcServiceComponents",),
            ".unit.test_typings": ("TestsFlextGrpcTypesUnit",),
            ".unit.test_utilities": ("Testu",),
            ".utilities": (
                "TestsFlextGrpcUtilities",
                "u",
            ),
            "flext_grpc": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
            "flext_tests": (
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestErrorIntegration",
    "TestFlextGrpcConfigurationError",
    "TestFlextGrpcConnectionError",
    "TestFlextGrpcEntities",
    "TestFlextGrpcError",
    "TestFlextGrpcModels",
    "TestFlextGrpcServiceComponents",
    "TestFlextGrpcTimeoutError",
    "TestFlextGrpcValidationError",
    "TestsFlextGrpcApi",
    "TestsFlextGrpcConfig",
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcConstantsUnit",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcProtocolsUnit",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcTypesUnit",
    "TestsFlextGrpcUtilities",
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
    "td",
    "tf",
    "tk",
    "tm",
    "tv",
    "u",
    "x",
]
