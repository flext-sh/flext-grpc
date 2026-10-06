# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc.services import _entities
    from flext_grpc.services._entities.client_manager import FlextGrpcClientManagerImpl
    from flext_grpc.services._entities.connection_pool_impl import (
        FlextGrpcConnectionPoolImpl,
    )
    from flext_grpc.services._entities.metric_value import FlextGrpcMetricValueModel
    from flext_grpc.services._entities.metrics_collector import (
        FlextGrpcMetricsCollectorImpl,
    )
    from flext_grpc.services._entities.server_manager import FlextGrpcServerManagerImpl
    from flext_grpc.services._entities.stream_manager import FlextGrpcStreamManagerImpl
    from flext_grpc.services._entities.stream_state import FlextGrpcStreamRuntimeState
    from flext_grpc.services.api_runtime import FlextGrpcApiRuntime
    from flext_grpc.services.client import FlextGrpcClient
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.services.metrics import FlextGrpcMetrics
    from flext_grpc.services.server import FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream


__all__: tuple[str, ...] = (
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcClientManagerImpl",
    "FlextGrpcConnectionPool",
    "FlextGrpcConnectionPoolImpl",
    "FlextGrpcMetricValueModel",
    "FlextGrpcMetrics",
    "FlextGrpcMetricsCollectorImpl",
    "FlextGrpcServer",
    "FlextGrpcServerManagerImpl",
    "FlextGrpcStream",
    "FlextGrpcStreamManagerImpl",
    "FlextGrpcStreamRuntimeState",
    "_entities",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcApiRuntime": ".api_runtime",
        "FlextGrpcClient": ".client",
        "FlextGrpcClientManagerImpl": "._entities.client_manager",
        "FlextGrpcConnectionPool": ".connection_pool",
        "FlextGrpcConnectionPoolImpl": "._entities.connection_pool_impl",
        "FlextGrpcMetricValueModel": "._entities.metric_value",
        "FlextGrpcMetrics": ".metrics",
        "FlextGrpcMetricsCollectorImpl": "._entities.metrics_collector",
        "FlextGrpcServer": ".server",
        "FlextGrpcServerManagerImpl": "._entities.server_manager",
        "FlextGrpcStream": ".stream",
        "FlextGrpcStreamManagerImpl": "._entities.stream_manager",
        "FlextGrpcStreamRuntimeState": "._entities.stream_state",
        "_entities": "._entities",
    }),
    public_exports=__all__,
)
