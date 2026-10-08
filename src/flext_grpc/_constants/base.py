"""Private constants base for flext-grpc.

Owns every plain-literal scalar constant value so the public ``constants.py``
facade module never declares a bare literal class attribute directly
(ENFORCE-079); the facade re-exports them via ``c.Grpc.*`` through
inheritance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_core import t


class FlextGrpcConstantsBase:
    """Private constants owner for gRPC scalar defaults and state enums."""

    # ===== Enums (single source of truth) =====
    @unique
    class ChannelState(StrEnum):
        """gRPC channel state enumeration (single source of truth).

        DRY Pattern:
            StrEnum is the single source of truth. Use ChannelState.IDLE.value
            or ChannelState.IDLE directly - no base strings needed.
        """

        IDLE = "idle"
        READY = "ready"

    @unique
    class ServerState(StrEnum):
        """gRPC server state enumeration (single source of truth).

        DRY Pattern:
            StrEnum is the single source of truth. Use ServerState.STOPPED.value
            or ServerState.STOPPED directly - no base strings needed.
        """

        STOPPED = "stopped"
        STARTING = "starting"
        RUNNING = "running"
        STOPPING = "stopping"

    @unique
    class GrpcOperations(StrEnum):
        """gRPC operation types (single source of truth).

        DRY Pattern:
            StrEnum is the single source of truth. Use GrpcOperations.UNARY.value
            or GrpcOperations.UNARY directly - no base strings needed.
        """

        UNARY = "unary"

    @unique
    class ServiceMethod(StrEnum):
        """gRPC service method names (single source of truth).

        DRY Pattern:
            StrEnum is the single source of truth. Use ServiceMethod.ECHO.value
            or ServiceMethod.ECHO directly - no base strings needed.
        """

        ECHO = "Echo"
        HEALTH_CHECK = "HealthCheck"

    @unique
    class ServingStatus(StrEnum):
        """gRPC health-checking serving states (grpc.health.v1 wire names).

        DRY Pattern:
            StrEnum is the single source of truth. Use ServingStatus.SERVING.value
            or ServingStatus.SERVING directly - no base strings needed.
        """

        UNKNOWN = "UNKNOWN"
        SERVING = "SERVING"
        NOT_SERVING = "NOT_SERVING"
        SERVICE_UNKNOWN = "SERVICE_UNKNOWN"

    @unique
    class CompressionTypes(StrEnum):
        """gRPC compression types (single source of truth).

        DRY Pattern:
            StrEnum is the single source of truth. Use CompressionTypes.NONE.value
            or CompressionTypes.NONE directly - no base strings needed.
        """

        NONE = "none"

    @unique
    class LoadBalancingPolicies(StrEnum):
        """gRPC load balancing policies (single source of truth).

        DRY Pattern:
            StrEnum is the single source of truth. Use
            LoadBalancingPolicies.ROUND_ROBIN.value or
            LoadBalancingPolicies.ROUND_ROBIN directly - no base strings needed.
        """

        ROUND_ROBIN = "round_robin"

    # ===== Enum-derived frozensets (immutable collections) =====
    CHANNEL_STATES: Final[frozenset[t.JsonValue]] = frozenset(
        member.value for member in ChannelState.__members__.values()
    )
    """Channel states frozenset - generated from ChannelState StrEnum."""

    SERVER_STATES: Final[frozenset[t.JsonValue]] = frozenset(
        member.value for member in ServerState.__members__.values()
    )
    """Server states frozenset - generated from ServerState StrEnum."""

    STREAM_TYPES: Final[frozenset[str]] = frozenset(
        member.value for member in GrpcOperations.__members__.values()
    )
    """Stream types frozenset - generated from GrpcOperations StrEnum."""

    LOAD_BALANCING_POLICIES: Final[frozenset[str]] = frozenset(
        member.value for member in LoadBalancingPolicies.__members__.values()
    )
    """Load balancing policies frozenset from LoadBalancingPolicies StrEnum."""

    # ===== Network constants =====
    NETWORK_DEFAULT_TIMEOUT: Final[float] = 30.0
    NETWORK_DEFAULT_CHANNEL_READY_TIMEOUT: Final[float] = 5.0
    NETWORK_DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT: Final[float] = 2.0
    NETWORK_DEFAULT_GRPC_PORT: Final[int] = 50051
    NETWORK_DEFAULT_HOST: Final[str] = "127.0.0.1"
    NETWORK_MAX_PORT: Final[int] = 65535
    NETWORK_MIN_PORT: Final[int] = 1
    NETWORK_HOST_PATTERN: Final[str] = r"^[a-zA-Z0-9.-]+$"

    # ===== Service constants =====
    SERVICE_DEFAULT_MAX_WORKERS: Final[int] = 10
    SERVICE_PROTO_NAME: Final[str] = "FlextGrpcService"
    """Service name declared in ``protos/flext.proto``."""

    # ===== Streaming configuration =====
    BIDIRECTIONAL_STREAMING_QUEUE_SIZE: Final[int] = 1000
    CLIENT_STREAMING_BUFFER_THRESHOLD: Final[int] = 10
    STREAMING_DEFAULT_BUFFER_SIZE: Final[int] = 500
    SERVER_STREAMING_BATCH_SIZE: Final[int] = 100

    # ===== Connection pool defaults =====
    CONNECTION_DEFAULT_POOL_SIZE: Final[int] = 20

    # ===== Validation constants =====
    VALIDATION_ADDRESS_PARTS_COUNT: Final[int] = 2
    VALIDATION_MAX_PORT_NUMBER: Final[int] = 65535
    VALIDATION_VERSION_PATTERN: Final[str] = r"Version.*(\d+\.\d+\.\d+)"


__all__: list[str] = ["FlextGrpcConstantsBase"]
