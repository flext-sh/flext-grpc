# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc.services.api_runtime import FlextGrpcApiRuntime
    from flext_grpc.services.client import FlextGrpcClient
    from flext_grpc.services.connection_pool import (
        FlextGrpcConnectionPool,
        FlextGrpcConnectionPoolImpl,
    )
    from flext_grpc.services.metrics import (
        FlextGrpcMetrics,
        FlextGrpcMetricsCollectorImpl,
    )
    from flext_grpc.services.server import FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream


__all__: tuple[str, ...] = (
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConnectionPool",
    "FlextGrpcConnectionPoolImpl",
    "FlextGrpcMetrics",
    "FlextGrpcMetricsCollectorImpl",
    "FlextGrpcServer",
    "FlextGrpcStream",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcApiRuntime": ".api_runtime",
        "FlextGrpcClient": ".client",
        "FlextGrpcConnectionPool": ".connection_pool",
        "FlextGrpcConnectionPoolImpl": ".connection_pool",
        "FlextGrpcMetrics": ".metrics",
        "FlextGrpcMetricsCollectorImpl": ".metrics",
        "FlextGrpcServer": ".server",
        "FlextGrpcStream": ".stream",
    }),
    public_exports=__all__,
)
