# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_grpc.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_core import d as d, e as e, h as h, r as r, x as x
    from flext_grpc.api import FlextGrpc as FlextGrpc, grpc as grpc
    from flext_grpc.base import FlextGrpcServiceBase as FlextGrpcServiceBase, s as s
    from flext_grpc.constants import FlextGrpcConstants as FlextGrpcConstants, c as c
    from flext_grpc.models import FlextGrpcModels as FlextGrpcModels, m as m
    from flext_grpc.protocols import FlextGrpcProtocols as FlextGrpcProtocols, p as p
    from flext_grpc.settings import FlextGrpcSettings as FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes as FlextGrpcTypes, t as t
    from flext_grpc.utilities import FlextGrpcUtilities as FlextGrpcUtilities, u as u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api": (
            "FlextGrpc",
            "grpc",
        ),
        ".base": (
            "FlextGrpcServiceBase",
            "s",
        ),
        ".constants": (
            "FlextGrpcConstants",
            "c",
        ),
        ".models": (
            "FlextGrpcModels",
            "m",
        ),
        ".protocols": (
            "FlextGrpcProtocols",
            "p",
        ),
        ".settings": ("FlextGrpcSettings",),
        ".typings": (
            "FlextGrpcTypes",
            "t",
        ),
        ".utilities": (
            "FlextGrpcUtilities",
            "u",
        ),
        "flext_core": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)


__all__: tuple[str, ...] = (
    "FlextGrpc",
    "FlextGrpcConstants",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceBase",
    "FlextGrpcSettings",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "grpc",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    public_exports=__all__,
)
