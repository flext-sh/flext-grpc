# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .api_runtime import FlextGrpcApiRuntime
    from .client import FlextGrpcClient
    from .connection_pool import FlextGrpcConnectionPool
    from .metrics import FlextGrpcMetrics
    from .server import FlextGrpcServer
    from .stream import FlextGrpcStream
__all__: tuple[str, ...] = (
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConnectionPool",
    "FlextGrpcMetrics",
    "FlextGrpcServer",
    "FlextGrpcStream",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".api_runtime": ("FlextGrpcApiRuntime",),
            ".client": ("FlextGrpcClient",),
            ".connection_pool": ("FlextGrpcConnectionPool",),
            ".metrics": ("FlextGrpcMetrics",),
            ".server": ("FlextGrpcServer",),
            ".stream": ("FlextGrpcStream",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
