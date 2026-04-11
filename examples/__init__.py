# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from examples.typings import CompleteSetup, ExamplesFlextGrpcTypes, t
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from flext_grpc.constants import c
    from flext_grpc.models import m
    from flext_grpc.protocols import p
    from flext_grpc.utilities import u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".typings": (
            "CompleteSetup",
            "ExamplesFlextGrpcTypes",
            "t",
        ),
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
        "flext_core.service": ("s",),
        "flext_grpc.constants": ("c",),
        "flext_grpc.models": ("m",),
        "flext_grpc.protocols": ("p",),
        "flext_grpc.utilities": ("u",),
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
