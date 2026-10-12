# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.services. Entities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc.services._entities.client_manager import FlextGrpcClientManagerImpl
    from flext_grpc.services._entities.connection_pool_impl import (
        FlextGrpcConnectionPoolImpl,
    )
    from flext_grpc.services._entities.metrics_collector import (
        FlextGrpcMetricsCollectorImpl,
    )
    from flext_grpc.services._entities.server_manager import FlextGrpcServerManagerImpl
    from flext_grpc.services._entities.service_handler import (
        FlextGrpcServiceHandlerImpl,
    )
    from flext_grpc.services._entities.stream_manager import FlextGrpcStreamManagerImpl


__all__: tuple[str, ...] = (
    "FlextGrpcClientManagerImpl",
    "FlextGrpcConnectionPoolImpl",
    "FlextGrpcMetricsCollectorImpl",
    "FlextGrpcServerManagerImpl",
    "FlextGrpcServiceHandlerImpl",
    "FlextGrpcStreamManagerImpl",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcClientManagerImpl": ".client_manager",
        "FlextGrpcConnectionPoolImpl": ".connection_pool_impl",
        "FlextGrpcMetricsCollectorImpl": ".metrics_collector",
        "FlextGrpcServerManagerImpl": ".server_manager",
        "FlextGrpcServiceHandlerImpl": ".service_handler",
        "FlextGrpcStreamManagerImpl": ".stream_manager",
    }),
    public_exports=__all__,
)
