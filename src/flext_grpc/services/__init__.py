# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports

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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._entities": ("_entities",),
            "._entities.client_manager": ("FlextGrpcClientManagerImpl",),
            "._entities.connection_pool_impl": ("FlextGrpcConnectionPoolImpl",),
            "._entities.metric_value": ("FlextGrpcMetricValueModel",),
            "._entities.metrics_collector": ("FlextGrpcMetricsCollectorImpl",),
            "._entities.server_manager": ("FlextGrpcServerManagerImpl",),
            "._entities.stream_manager": ("FlextGrpcStreamManagerImpl",),
            "._entities.stream_state": ("FlextGrpcStreamRuntimeState",),
            ".api_runtime": ("FlextGrpcApiRuntime",),
            ".client": ("FlextGrpcClient",),
            ".connection_pool": ("FlextGrpcConnectionPool",),
            ".metrics": ("FlextGrpcMetrics",),
            ".server": ("FlextGrpcServer",),
            ".stream": ("FlextGrpcStream",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
