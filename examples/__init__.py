# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
<<<<<<< HEAD
    from flext_core import (
        core,
        d,
        e,
        h,
        lazy,
        lazy_attribute,
        normalize_lazy_imports,
        r,
        x,
    )
    from flext_grpc import c, config, grpc, m, main, p, s, settings, u
=======
    from flext_grpc import c, d, e, h, m, p, r, s, u, x
>>>>>>> recovery/rope-automation-20260921

    from .constants import ExamplesFlextGrpcConstants
    from .models import ExamplesFlextGrpcModels
    from .protocols import ExamplesFlextGrpcProtocols
    from .typings import ExamplesFlextGrpcTypes, ExamplesFlextGrpcTypes as t
    from .utilities import ExamplesFlextGrpcUtilities


__all__: tuple[str, ...] = (
    "ExamplesFlextGrpcConstants",
    "ExamplesFlextGrpcModels",
    "ExamplesFlextGrpcProtocols",
    "ExamplesFlextGrpcTypes",
    "ExamplesFlextGrpcUtilities",
    "c",
    "d",
    "e",
    "h",
<<<<<<< HEAD
    "lazy",
    "lazy_attribute",
    "m",
    "main",
    "normalize_lazy_imports",
    "p",
    "r",
    "s",
    "settings",
=======
    "m",
    "p",
    "r",
    "s",
>>>>>>> recovery/rope-automation-20260921
    "t",
    "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("ExamplesFlextGrpcConstants",),
            ".models": ("ExamplesFlextGrpcModels",),
            ".protocols": ("ExamplesFlextGrpcProtocols",),
            ".typings": ("ExamplesFlextGrpcTypes", "t"),
            ".utilities": ("ExamplesFlextGrpcUtilities",),
<<<<<<< HEAD
            "flext_core": (
                "core",
                "d",
                "e",
                "h",
                "lazy",
                "lazy_attribute",
                "normalize_lazy_imports",
                "r",
                "x",
            ),
            "flext_grpc": (
                "c",
                "config",
                "grpc",
                "m",
                "main",
                "p",
                "s",
                "settings",
                "u",
            ),
=======
            "flext_grpc": ("c", "d", "e", "h", "m", "p", "r", "s", "u", "x"),
>>>>>>> recovery/rope-automation-20260921
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
