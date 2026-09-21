# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services. Entities package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .client_manager import FlextGrpcClientManagerImpl
    from .connection_pool_impl import FlextGrpcConnectionPoolImpl
    from .metric_value import FlextGrpcMetricValueModel
    from .metrics_collector import FlextGrpcMetricsCollectorImpl
    from .server_manager import FlextGrpcServerManagerImpl
    from .stream_manager import FlextGrpcStreamManagerImpl
    from .stream_state import FlextGrpcStreamRuntimeState
__all__: tuple[str, ...] = (
    "FlextGrpcClientManagerImpl",
    "FlextGrpcConnectionPoolImpl",
    "FlextGrpcMetricValueModel",
    "FlextGrpcMetricsCollectorImpl",
    "FlextGrpcServerManagerImpl",
    "FlextGrpcStreamManagerImpl",
    "FlextGrpcStreamRuntimeState",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            ".client_manager": ("FlextGrpcClientManagerImpl",),
            ".connection_pool_impl": ("FlextGrpcConnectionPoolImpl",),
            ".metric_value": ("FlextGrpcMetricValueModel",),
            ".metrics_collector": ("FlextGrpcMetricsCollectorImpl",),
            ".server_manager": ("FlextGrpcServerManagerImpl",),
            ".stream_manager": ("FlextGrpcStreamManagerImpl",),
            ".stream_state": ("FlextGrpcStreamRuntimeState",),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
