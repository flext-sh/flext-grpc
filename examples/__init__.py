# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from examples.typings import CompleteSetup, ExamplesFlextGrpcTypes, t
    from flext_grpc import c, d, e, h, m, p, r, s, u, x
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".typings": (
            "CompleteSetup",
            "ExamplesFlextGrpcTypes",
            "t",
        ),
        "flext_grpc": (
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
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "CompleteSetup",
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
]
