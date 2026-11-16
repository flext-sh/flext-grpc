# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Constants package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._constants.base import FlextGrpcConstantsBase
    from flext_grpc._constants.derived import FlextGrpcConstantsDerived


__all__: tuple[str, ...] = ("FlextGrpcConstantsBase", "FlextGrpcConstantsDerived")

install_lazy_exports(
    __name__,
    globals(),
    {"FlextGrpcConstantsBase": ".base", "FlextGrpcConstantsDerived": ".derived"},
    public_exports=__all__,
    deferred_members={
        "FlextGrpcConstantsBase": (
            "ChannelState",
            "ServerState",
            "GrpcOperations",
            "ServiceMethod",
            "ServingStatus",
            "CompressionTypes",
            "LoadBalancingPolicies",
            "CHANNEL_STATES",
            "SERVER_STATES",
            "STREAM_TYPES",
            "LOAD_BALANCING_POLICIES",
            "NETWORK_DEFAULT_TIMEOUT",
            "NETWORK_DEFAULT_CHANNEL_READY_TIMEOUT",
            "NETWORK_DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT",
            "NETWORK_DEFAULT_GRPC_PORT",
            "NETWORK_DEFAULT_HOST",
            "NETWORK_HOST_PATTERN",
            "SERVICE_DEFAULT_MAX_WORKERS",
            "SERVICE_PROTO_NAME",
            "BIDIRECTIONAL_STREAMING_QUEUE_SIZE",
            "CLIENT_STREAMING_BUFFER_THRESHOLD",
            "STREAMING_DEFAULT_BUFFER_SIZE",
            "SERVER_STREAMING_BATCH_SIZE",
            "CONNECTION_DEFAULT_POOL_SIZE",
            "VALIDATION_ADDRESS_PARTS_COUNT",
            "VALIDATION_VERSION_PATTERN",
        ),
        "FlextGrpcConstantsDerived": (
            "NETWORK_HOST_RE",
            "VALIDATION_VERSION_RE",
        ),
    },
)
