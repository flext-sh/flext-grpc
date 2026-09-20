# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc import FlextGrpcConstants, d, e, h, r, s, x

    from .constants import ExamplesFlextGrpcConstants, ExamplesFlextGrpcConstants as c
    from .models import ExamplesFlextGrpcModels, ExamplesFlextGrpcModels as m
    from .protocols import ExamplesFlextGrpcProtocols, ExamplesFlextGrpcProtocols as p
    from .typings import ExamplesFlextGrpcTypes, ExamplesFlextGrpcTypes as t
    from .utilities import ExamplesFlextGrpcUtilities, ExamplesFlextGrpcUtilities as u
__all__: tuple[str, ...] = (
    "ExamplesFlextGrpcConstants", "ExamplesFlextGrpcModels", "ExamplesFlextGrpcProtocols", "ExamplesFlextGrpcTypes",
    "ExamplesFlextGrpcUtilities", "FlextGrpcConstants", "c", "d",
    "e", "h", "m", "p",
    "r", "s", "t", "u",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".constants": ("ExamplesFlextGrpcConstants", "c"),
            ".models": ("ExamplesFlextGrpcModels", "m"),
            ".protocols": ("ExamplesFlextGrpcProtocols", "p"),
            ".typings": ("ExamplesFlextGrpcTypes", "t"),
            ".utilities": ("ExamplesFlextGrpcUtilities", "u"),
            "flext_grpc": ("FlextGrpcConstants", "d", "e", "h", "r", "s", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
