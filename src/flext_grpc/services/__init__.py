# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from . import _entities
    from ._entities.client_manager import FlextGrpcClientManagerImpl
    from ._entities.connection_pool_impl import FlextGrpcConnectionPoolImpl
    from ._entities.metric_value import FlextGrpcMetricValueModel
    from ._entities.metrics_collector import FlextGrpcMetricsCollectorImpl
    from ._entities.server_manager import FlextGrpcServerManagerImpl
    from ._entities.stream_manager import FlextGrpcStreamManagerImpl
    from ._entities.stream_state import FlextGrpcStreamRuntimeState
    from .api_runtime import FlextGrpcApiRuntime
    from .client import FlextGrpcClient
    from .connection_pool import FlextGrpcConnectionPool
    from .metrics import FlextGrpcMetrics
    from .server import FlextGrpcServer
    from .stream import FlextGrpcStream


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
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
