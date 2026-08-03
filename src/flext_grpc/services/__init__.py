# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .api_runtime import FlextGrpcApiRuntime as FlextGrpcApiRuntime
    from .client import FlextGrpcClient as FlextGrpcClient
    from .connection_pool import FlextGrpcConnectionPool as FlextGrpcConnectionPool
    from .metrics import FlextGrpcMetrics as FlextGrpcMetrics
    from .server import FlextGrpcServer as FlextGrpcServer
    from .stream import FlextGrpcStream as FlextGrpcStream

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    ".api_runtime": ("FlextGrpcApiRuntime",),
    ".client": ("FlextGrpcClient",),
    ".connection_pool": ("FlextGrpcConnectionPool",),
    ".metrics": ("FlextGrpcMetrics",),
    ".server": ("FlextGrpcServer",),
    ".stream": ("FlextGrpcStream",),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConnectionPool",
    "FlextGrpcMetrics",
    "FlextGrpcServer",
    "FlextGrpcStream",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
