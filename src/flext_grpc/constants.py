"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

from flext_core import FlextConstants


class FlextGrpcConstants(FlextConstants):
    """gRPC-specific constants following FLEXT unified single-class pattern.

    Defines ALL constants used by the flext-grpc project, including inherited
    constants redefined for gRPC context. NO direct imports from c
    should be used - all constants must come from this class.

    Layer N Foundation: gRPC domain-specific constants building on flext-core Layer 0.

    Usage:
    ```python
    from flext_grpc import FlextGrpcConstants, t

    timeout = FlextGrpcConstants.Grpc.NETWORK_DEFAULT_TIMEOUT
    port = FlextGrpcConstants.Grpc.NETWORK_DEFAULT_GRPC_PORT
    ```
    """

    class Grpc:
        """gRPC domain constants namespace.

        All gRPC-specific constants are organized here as flat SSOT members,
        enabling direct access via c.Grpc.CONSTANT_NAME (no nested subclasses).
        """

        # ===== Network constants =====
        NETWORK_DEFAULT_CHANNEL_READY_TIMEOUT: Final[float] = 5.0
        NETWORK_DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT: Final[float] = 2.0
        NETWORK_DEFAULT_GRPC_PORT: Final[int] = 50051
        NETWORK_DEFAULT_HOST: Final[str] = "127.0.0.1"
        NETWORK_DEFAULT_KEEPALIVE_TIME_MS: Final[int] = 30000
        NETWORK_DEFAULT_KEEPALIVE_TIMEOUT_MS: Final[int] = 5000
        NETWORK_DEFAULT_TIMEOUT: Final[float] = float(
            FlextConstants.DEFAULT_TIMEOUT_SECONDS,
        )
        NETWORK_MAX_PORT: Final[int] = 65535
        NETWORK_MIN_PORT: Final[int] = 1

        # ===== Performance limits =====
        PERFORMANCE_DEFAULT_MESSAGE_LENGTH: Final[int] = 4 * 1024 * 1024
        PERFORMANCE_DEFAULT_THREAD_POOL_SIZE: Final[int] = 50
        PERFORMANCE_MAX_MESSAGE_LENGTH: Final[int] = 100 * 1024 * 1024
        PERFORMANCE_MAX_THREAD_POOL_SIZE: Final[int] = 200
        PERFORMANCE_MIN_MESSAGE_LENGTH: Final[int] = 1024
        PERFORMANCE_MIN_THREAD_POOL_SIZE: Final[int] = 1

        # ===== Service constants =====
        SERVICE_DEFAULT_MAX_CONCURRENT_RPCS: Final[int] = 1000
        SERVICE_DEFAULT_MAX_WORKERS: Final[int] = 10
        SERVICE_MAX_WORKERS: Final[int] = 100
        SERVICE_MIN_WORKERS: Final[int] = 1

        # ===== Streaming configuration =====
        STREAMING_BIDIRECTIONAL_QUEUE_SIZE: Final[int] = 1000
        STREAMING_CLIENT_BUFFER_THRESHOLD: Final[int] = 10
        STREAMING_DEFAULT_BUFFER_SIZE: Final[int] = 500
        STREAMING_DEFAULT_MAX_CONCURRENT_STREAMS: Final[int] = 10
        STREAMING_MAX_BUFFER_SIZE: Final[int] = 10000
        STREAMING_MIN_BUFFER_SIZE: Final[int] = 10
        STREAMING_SERVER_BATCH_SIZE: Final[int] = 100

        # ===== Connection pool defaults =====
        CONNECTION_DEFAULT_POOL_SIZE: Final[int] = 20
        CONNECTION_DEFAULT_TIMEOUT: Final[float] = float(
            FlextConstants.DEFAULT_TIMEOUT_SECONDS,
        )

        # ===== Production validation =====
        PRODUCTION_MIN_PORT: Final[int] = 1024
        PRODUCTION_RETRY_ATTEMPTS: Final[int] = FlextConstants.MAX_RETRY_ATTEMPTS
        PRODUCTION_MAX_RETRY_ATTEMPTS: Final[int] = 5

        # ===== Validation constants =====
        VALIDATION_ADDRESS_PARTS_COUNT: Final[int] = 2
        VALIDATION_MAX_PORT_NUMBER: Final[int] = 65535

        # ===== Error messages =====
        MESSAGE_TIMEOUT_ERROR: Final[str] = "gRPC operation timed out after {timeout}s"

        # ===== Error codes =====
        ERROR_CONNECTION: Final[str] = "GRPC_CONNECTION_ERROR"
        ERROR_TIMEOUT: Final[str] = "GRPC_TIMEOUT_ERROR"
        ERROR_VALIDATION: Final[str] = "GRPC_VALIDATION_ERROR"
        ERROR_SERVER: Final[str] = "GRPC_SERVER_ERROR"

        # ===== Timeout validation =====
        TIMEOUT_MAX_SECONDS: Final[float] = 300.0

        # ===== Enums (single source of truth) =====
        @unique
        class ChannelState(StrEnum):
            """gRPC channel state enumeration (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use ChannelState.IDLE.value
                or ChannelState.IDLE directly - no base strings needed.
            """

            IDLE = "idle"
            CONNECTING = "connecting"
            READY = "ready"
            TRANSIENT_FAILURE = "transient_failure"
            SHUTDOWN = "shutdown"

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
            SERVER_STREAMING = "server_streaming"
            CLIENT_STREAMING = "client_streaming"
            BIDIRECTIONAL = "bidirectional"

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
        class CompressionTypes(StrEnum):
            """gRPC compression types (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use CompressionTypes.NONE.value
                or CompressionTypes.NONE directly - no base strings needed.
            """

            NONE = "none"
            GZIP = "gzip"
            DEFLATE = "deflate"

        @unique
        class LoadBalancingPolicies(StrEnum):
            """gRPC load balancing policies (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use LoadBalancingPolicies.ROUND_ROBIN.value
                or LoadBalancingPolicies.ROUND_ROBIN directly - no base strings needed.
            """

            ROUND_ROBIN = "round_robin"
            PICK_FIRST = "pick_first"
            GRPCLB = "grpclb"
            XDS_CLUSTER_RESOLVER = "xds_cluster_resolver"

        # ===== Enum-derived frozensets (immutable collections) =====
        CHANNEL_STATES: Final[frozenset[str]] = frozenset(
            member.value for member in ChannelState.__members__.values()
        )
        """Channel states frozenset - generated from ChannelState StrEnum."""

        COMPRESSION_TYPES: Final[frozenset[str]] = frozenset(
            member.value for member in CompressionTypes.__members__.values()
        )
        """Compression types frozenset - generated from CompressionTypes StrEnum."""

        LOAD_BALANCING_POLICIES: Final[frozenset[str]] = frozenset(
            member.value for member in LoadBalancingPolicies.__members__.values()
        )
        """Load balancing policies frozenset - generated from LoadBalancingPolicies StrEnum."""

        SERVER_STATES: Final[frozenset[str]] = frozenset(
            member.value for member in ServerState.__members__.values()
        )
        """Server states frozenset - generated from ServerState StrEnum."""

        STREAM_TYPES: Final[frozenset[str]] = frozenset(
            member.value for member in GrpcOperations.__members__.values()
        )
        """Stream types frozenset - generated from GrpcOperations StrEnum."""


c = FlextGrpcConstants

__all__: tuple[str, ...] = ("FlextGrpcConstants", "c")
