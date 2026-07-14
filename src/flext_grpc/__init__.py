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
    from flext_core import d, e, h, r, x

    from ._settings import FlextGrpcSettings, settings
    from .api import FlextGrpc, grpc
    from .base import FlextGrpcServiceBase, s
    from .constants import FlextGrpcConstants, FlextGrpcConstants as c
    from .models import FlextGrpcModels, FlextGrpcModels as m
    from .protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
    from .typings import FlextGrpcTypes, FlextGrpcTypes as t
    from .utilities import FlextGrpcUtilities, FlextGrpcUtilities as u

    _ = (
        c,
        FlextGrpcConstants,
        t,
        FlextGrpcTypes,
        p,
        FlextGrpcProtocols,
        m,
        FlextGrpcModels,
        u,
        FlextGrpcUtilities,
        d,
        e,
        h,
        r,
        x,
        s,
        FlextGrpcServiceBase,
        FlextGrpcSettings,
        settings,
        FlextGrpc,
        grpc,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._settings": (
        "FlextGrpcSettings",
        "settings",
    ),
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
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES,
    alias_groups=_LAZY_ALIAS_GROUPS,
    sort_keys=False,
)

_DIRECT_IMPORTS: tuple[str, ...] = (
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
    "build_lazy_import_map",
    "c",
    "d",
    "e",
    "grpc",
    "h",
    "install_lazy_exports",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
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
    "settings",
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
