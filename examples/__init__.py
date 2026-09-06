# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc import (
        FlextGrpcConstants,
        FlextGrpcConstants as c,
        d,
        e,
        h,
        m,
        p,
        r,
        s,
        u,
        x,
    )

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
    "FlextGrpcConstants",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
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
            "flext_grpc": (
                "FlextGrpcConstants",
                "c",
                "d",
                "e",
                "h",
                "m",
                "p",
                "r",
                "s",
                "u",
                "x",
            ),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
