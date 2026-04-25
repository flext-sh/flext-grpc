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
    from tests.unit.test_entities import TestsFlextGrpcEntities
    from tests.unit.test_errors import TestsFlextGrpcErrors
    from tests.unit.test_models import TestsFlextGrpcModelsUnit
    from tests.unit.test_protocols import TestsFlextGrpcProtocolsUnit
    from tests.unit.test_services import TestsFlextGrpcServices
    from tests.unit.test_typings import TestsFlextGrpcTypesUnit
    from tests.unit.test_utilities import TestsFlextGrpcUtilitiesUnit
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
            ".unit.test_entities": ("TestsFlextGrpcEntities",),
            ".unit.test_errors": ("TestsFlextGrpcErrors",),
            ".unit.test_models": ("TestsFlextGrpcModelsUnit",),
            ".unit.test_protocols": ("TestsFlextGrpcProtocolsUnit",),
            ".unit.test_services": ("TestsFlextGrpcServices",),
            ".unit.test_typings": ("TestsFlextGrpcTypesUnit",),
            ".unit.test_utilities": ("TestsFlextGrpcUtilitiesUnit",),
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__: list[str] = [
    "TestsFlextGrpcApi",
    "TestsFlextGrpcConfig",
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcConstantsUnit",
    "TestsFlextGrpcEntities",
    "TestsFlextGrpcErrors",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcModelsUnit",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcProtocolsUnit",
    "TestsFlextGrpcServices",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcTypesUnit",
    "TestsFlextGrpcUtilities",
    "TestsFlextGrpcUtilitiesUnit",
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
