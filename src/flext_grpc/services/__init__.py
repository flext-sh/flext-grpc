# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT gRPC services subpackage."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_grpc.services import (
        _compat,
        client,
        connection_pool,
        metrics,
        server,
        stream,
    )
    from flext_grpc.services._compat import FlextGrpcServices
    from flext_grpc.services.client import FlextGrpcClient
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.services.metrics import FlextGrpcMetrics
    from flext_grpc.services.server import FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextGrpcClient": "flext_grpc.services.client",
    "FlextGrpcConnectionPool": "flext_grpc.services.connection_pool",
    "FlextGrpcMetrics": "flext_grpc.services.metrics",
    "FlextGrpcServer": "flext_grpc.services.server",
    "FlextGrpcServices": "flext_grpc.services._compat",
    "FlextGrpcStream": "flext_grpc.services.stream",
    "_compat": "flext_grpc.services._compat",
    "client": "flext_grpc.services.client",
    "connection_pool": "flext_grpc.services.connection_pool",
    "metrics": "flext_grpc.services.metrics",
    "server": "flext_grpc.services.server",
    "stream": "flext_grpc.services.stream",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
