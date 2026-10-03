# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_tests import api, td, tf, tk, tm

    from flext_core import d, e, h, r, x
    from tests import unit
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
            "flext_core": ("d", "e", "h", "r", "x"),
            "flext_tests": ("api", "td", "tf", "tk", "tm"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
