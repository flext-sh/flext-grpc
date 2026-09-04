# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc import c, d, e, h, m, p, r, s, u, x

    from .typings import ExamplesFlextGrpcTypes, ExamplesFlextGrpcTypes as t
__all__: tuple[str, ...] = (
    "ExamplesFlextGrpcTypes",
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
            ".typings": ("ExamplesFlextGrpcTypes", "t"),
            "flext_grpc": ("c", "d", "e", "h", "m", "p", "r", "s", "u", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
