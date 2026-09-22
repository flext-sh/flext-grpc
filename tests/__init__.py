# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_cli import cli
    from flext_infra import docs_main, infra, main
    from flext_tests import (
        active_rules,
        api,
        config,
        discover_repository_root,
        install_local_packages,
        load_infra_report,
        settings,
        split_csv,
        td,
        tf,
        tk,
        tm,
        tv,
    )
    from pydantic_core import from_json, to_json, to_jsonable_python

    from flext_core import core, d, e, h, lazy_attribute, r, x
    from flext_grpc import grpc

    from . import unit
    from .base import TestsFlextGrpcServiceBase, TestsFlextGrpcServiceBase as s
    from .constants import TestsFlextGrpcConstants, TestsFlextGrpcConstants as c
    from .models import TestsFlextGrpcModels, TestsFlextGrpcModels as m
    from .protocols import TestsFlextGrpcProtocols, TestsFlextGrpcProtocols as p
    from .settings import TestsFlextGrpcSettings
    from .typings import TestsFlextGrpcTypes, TestsFlextGrpcTypes as t
    from .utilities import TestsFlextGrpcUtilities, TestsFlextGrpcUtilities as u
__all__: tuple[str, ...] = (
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcServiceBase",
    "TestsFlextGrpcSettings",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcUtilities",
    "active_rules",
    "api",
    "c",
    "cli",
    "config",
    "core",
    "d",
    "discover_repository_root",
    "docs_main",
    "e",
    "from_json",
    "grpc",
    "h",
    "infra",
    "install_local_packages",
    "lazy_attribute",
    "load_infra_report",
    "m",
    "main",
    "p",
    "r",
    "s",
    "settings",
    "split_csv",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "to_json",
    "to_jsonable_python",
    "tv",
    "u",
    "unit",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".base": ("TestsFlextGrpcServiceBase", "s"),
            ".constants": ("TestsFlextGrpcConstants", "c"),
            ".models": ("TestsFlextGrpcModels", "m"),
            ".protocols": ("TestsFlextGrpcProtocols", "p"),
            ".settings": ("TestsFlextGrpcSettings",),
            ".typings": ("TestsFlextGrpcTypes", "t"),
            ".unit": ("unit",),
            ".utilities": ("TestsFlextGrpcUtilities", "u"),
            "flext_cli": ("cli",),
            "flext_core": ("core", "d", "e", "h", "lazy_attribute", "r", "x"),
            "flext_grpc": ("grpc",),
            "flext_infra": ("docs_main", "infra", "main"),
            "flext_tests": (
                "active_rules",
                "api",
                "config",
                "discover_repository_root",
                "install_local_packages",
                "load_infra_report",
                "settings",
                "split_csv",
                "td",
                "tf",
                "tk",
                "tm",
                "tv",
            ),
            "pydantic_core": ("from_json", "to_json", "to_jsonable_python"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
