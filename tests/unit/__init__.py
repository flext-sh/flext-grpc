# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests.unit package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import c, d, e, h, m, p, r, s, t, td, tf, tk, tm, tv, u, x

    from .test_api import TestsFlextGrpcApi
    from .test_config import TestsFlextGrpcConfig
    from .test_constants import Grpc, TestsFlextGrpcConstantsUnit
    from .test_entities import TestsFlextGrpcEntities
    from .test_errors import TestsFlextGrpcErrors
    from .test_models import TestsFlextGrpcModelsUnit
    from .test_protocols import TestsFlextGrpcProtocolsUnit
    from .test_services import TestsFlextGrpcServices
    from .test_typings import TestsFlextGrpcTypesUnit
    from .test_utilities import TestsFlextGrpcUtilitiesUnit
__all__: tuple[str, ...] = (
    "Grpc",
    "TestsFlextGrpcApi",
    "TestsFlextGrpcConfig",
    "TestsFlextGrpcConstantsUnit",
    "TestsFlextGrpcEntities",
    "TestsFlextGrpcErrors",
    "TestsFlextGrpcModelsUnit",
    "TestsFlextGrpcProtocolsUnit",
    "TestsFlextGrpcServices",
    "TestsFlextGrpcTypesUnit",
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
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".test_api": ("TestsFlextGrpcApi",),
            ".test_config": ("TestsFlextGrpcConfig",),
            ".test_constants": ("Grpc", "TestsFlextGrpcConstantsUnit"),
            ".test_entities": ("TestsFlextGrpcEntities",),
            ".test_errors": ("TestsFlextGrpcErrors",),
            ".test_models": ("TestsFlextGrpcModelsUnit",),
            ".test_protocols": ("TestsFlextGrpcProtocolsUnit",),
            ".test_services": ("TestsFlextGrpcServices",),
            ".test_typings": ("TestsFlextGrpcTypesUnit",),
            ".test_utilities": ("TestsFlextGrpcUtilitiesUnit",),
            "flext_tests": (
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
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
