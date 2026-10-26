# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x
    from flext_tests import (
        api,
        config,
        install_local_packages,
        settings,
        td,
        tf,
        tk,
        tm,
    )

    from flext_grpc import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        core,
        grpc,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        main,
        merge_lazy_imports,
        normalize_lazy_imports,
        resolve_lazy_members,
    )
    from tests.base import TestsFlextGrpcServiceBase, s
    from tests.constants import TestsFlextGrpcConstants, c
    from tests.models import TestsFlextGrpcModels, m
    from tests.protocols import TestsFlextGrpcProtocols, p
    from tests.settings import TestsFlextGrpcSettings
    from tests.typings import TestsFlextGrpcTypes, t
    from tests.utilities import TestsFlextGrpcUtilities, u


__all__: tuple[str, ...] = (
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcServiceBase",
    "TestsFlextGrpcSettings",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcUtilities",
    "api",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "config",
    "core",
    "d",
    "e",
    "grpc",
    "h",
    "install_lazy_exports",
    "install_local_packages",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "TestsFlextGrpcConstants": ".constants",
        "TestsFlextGrpcModels": ".models",
        "TestsFlextGrpcProtocols": ".protocols",
        "TestsFlextGrpcServiceBase": ".base",
        "TestsFlextGrpcSettings": ".settings",
        "TestsFlextGrpcTypes": ".typings",
        "TestsFlextGrpcUtilities": ".utilities",
        "api": "flext_tests",
        "build_lazy_import_map": "flext_grpc",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_grpc",
        "config": "flext_tests",
        "core": "flext_grpc",
        "d": "flext_core",
        "e": "flext_core",
        "grpc": "flext_grpc",
        "h": "flext_core",
        "install_lazy_exports": "flext_grpc",
        "install_local_packages": "flext_tests",
        "lazy": "flext_grpc",
        "lazy_getattr": "flext_grpc",
        "lazy_member": "flext_grpc",
        "m": ".models",
        "main": "flext_grpc",
        "merge_lazy_imports": "flext_grpc",
        "normalize_lazy_imports": "flext_grpc",
        "p": ".protocols",
        "r": "flext_core",
        "resolve_lazy_members": "flext_grpc",
        "s": ".base",
        "settings": "flext_tests",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_core",
    }),
    public_exports=__all__,
)
