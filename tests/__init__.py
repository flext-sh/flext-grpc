# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import unit as unit
    from flext_grpc import FlextGrpcConstants
    from flext_tests import FlextTestsConstants, d, e, h, r, td, tf, tk, tm, tv, x

    from .base import TestsFlextGrpcServiceBase, TestsFlextGrpcServiceBase as s
    from .conftest import (
        fixture_connection_pool,
        fixture_grpc_facade,
        fixture_metrics_collector,
    )
    from .constants import TestsFlextGrpcConstants, TestsFlextGrpcConstants as c
    from .models import TestsFlextGrpcModels, TestsFlextGrpcModels as m
    from .protocols import TestsFlextGrpcProtocols, TestsFlextGrpcProtocols as p
    from .settings import TestsFlextGrpcSettings
    from .typings import TestsFlextGrpcTypes, TestsFlextGrpcTypes as t
    from .utilities import TestsFlextGrpcUtilities, TestsFlextGrpcUtilities as u
__all__: tuple[str, ...] = (
    "FlextGrpcConstants",
    "FlextTestsConstants",
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcServiceBase",
    "TestsFlextGrpcSettings",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcUtilities",
    "c",
    "d",
    "e",
    "fixture_connection_pool",
    "fixture_grpc_facade",
    "fixture_metrics_collector",
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
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextGrpcServiceBase", "s"),
            ".conftest": (
                "fixture_connection_pool",
                "fixture_grpc_facade",
                "fixture_metrics_collector",
            ),
            ".constants": ("TestsFlextGrpcConstants", "c"),
            ".models": ("TestsFlextGrpcModels", "m"),
            ".protocols": ("TestsFlextGrpcProtocols", "p"),
            ".settings": ("TestsFlextGrpcSettings",),
            ".typings": ("TestsFlextGrpcTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextGrpcUtilities", "u"),
            "flext_grpc": ("FlextGrpcConstants",),
            "flext_tests": (
                "FlextTestsConstants",
                "d",
                "e",
                "h",
                "r",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
