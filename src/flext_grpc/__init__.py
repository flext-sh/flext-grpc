# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports
from flext_grpc.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x

    from ._config import FlextGrpcConfig, config
    from ._settings import FlextGrpcSettings, settings
    from ._utilities.grpc import FlextGrpcUtilitiesGrpc
    from .api import FlextGrpc, grpc
    from .base import FlextGrpcServiceBase, s
    from .constants import FlextGrpcConstants, FlextGrpcConstants as c
    from .errors import FlextGrpcErrors
    from .models import FlextGrpcModels, FlextGrpcModels as m
    from .protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
    from .services.api_runtime import FlextGrpcApiRuntime
    from .services.client import FlextGrpcClient
    from .services.connection_pool import FlextGrpcConnectionPool
    from .services.metrics import FlextGrpcMetrics
    from .services.server import FlextGrpcServer
    from .services.stream import FlextGrpcStream
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
        FlextGrpcConfig,
        config,
        FlextGrpcSettings,
        settings,
        FlextGrpcUtilitiesGrpc,
        FlextGrpc,
        grpc,
        FlextGrpcErrors,
        FlextGrpcApiRuntime,
        FlextGrpcClient,
        FlextGrpcConnectionPool,
        FlextGrpcMetrics,
        FlextGrpcServer,
        FlextGrpcStream,
    )


_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": (
        "FlextGrpcConfig",
        "config",
    ),
    "._settings": (
        "FlextGrpcSettings",
        "settings",
    ),
    "._utilities.grpc": ("FlextGrpcUtilitiesGrpc",),
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
    ".errors": ("FlextGrpcErrors",),
    ".models": (
        "FlextGrpcModels",
        "m",
    ),
    ".protocols": (
        "FlextGrpcProtocols",
        "p",
    ),
    ".services.api_runtime": ("FlextGrpcApiRuntime",),
    ".services.client": ("FlextGrpcClient",),
    ".services.connection_pool": ("FlextGrpcConnectionPool",),
    ".services.metrics": ("FlextGrpcMetrics",),
    ".services.server": ("FlextGrpcServer",),
    ".services.stream": ("FlextGrpcStream",),
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
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConfig",
    "FlextGrpcConnectionPool",
    "FlextGrpcConstants",
    "FlextGrpcErrors",
    "FlextGrpcMetrics",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceBase",
    "FlextGrpcSettings",
    "FlextGrpcStream",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcUtilitiesGrpc",
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
    "config",
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
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConnectionPool",
    "FlextGrpcConstants",
    "FlextGrpcMetrics",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceBase",
    "FlextGrpcSettings",
    "FlextGrpcStream",
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
