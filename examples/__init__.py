# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from examples.typings import CompleteSetup, ExamplesFlextGrpcTypes, t
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".typings": (
            "CompleteSetup",
            "ExamplesFlextGrpcTypes",
            "t",
        ),
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "CompleteSetup",
    "ExamplesFlextGrpcTypes",
    "t",
]
