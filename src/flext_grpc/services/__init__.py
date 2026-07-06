# AUTO-GENERATED FILE — Regenerate with: make gen
"""Services package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc.services.api_runtime import FlextGrpcApiRuntime
    from flext_grpc.services.client import FlextGrpcClient
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.services.metrics import FlextGrpcMetrics
    from flext_grpc.services.server import FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".api_runtime": ("FlextGrpcApiRuntime",),
        ".client": ("FlextGrpcClient",),
        ".connection_pool": ("FlextGrpcConnectionPool",),
        ".metrics": ("FlextGrpcMetrics",),
        ".server": ("FlextGrpcServer",),
        ".stream": ("FlextGrpcStream",),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    publish_all=False,
)
