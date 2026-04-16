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

    timeout = FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_TIMEOUT
    port = FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
    ```
    """

    class Grpc:
        """gRPC domain constants namespace.

        All gRPC-specific constants are organized here for better namespace
        organization and to enable composition with other domain constants.
        """

        class GrpcNetwork:
            """gRPC-specific network constants."""

            DEFAULT_CHANNEL_READY_TIMEOUT: Final[float] = 5.0
            DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT: Final[float] = 2.0
            DEFAULT_GRPC_PORT: Final[int] = 50051
            DEFAULT_HOST: Final[str] = "127.0.0.1"
            DEFAULT_KEEPALIVE_TIME_MS: Final[int] = 30000
            DEFAULT_KEEPALIVE_TIMEOUT_MS: Final[int] = 5000
            DEFAULT_TIMEOUT: Final[float] = float(
                FlextConstants.DEFAULT_TIMEOUT_SECONDS,
            )
            MAX_PORT: Final[int] = 65535
            MIN_PORT: Final[int] = 1

        class PerformanceLimits:
            """Performance configuration limits."""

            DEFAULT_MESSAGE_LENGTH: Final[int] = 4 * 1024 * 1024
            DEFAULT_THREAD_POOL_SIZE: Final[int] = 50
            MAX_MESSAGE_LENGTH: Final[int] = 100 * 1024 * 1024
            MAX_THREAD_POOL_SIZE: Final[int] = 200
            MIN_MESSAGE_LENGTH: Final[int] = 1024
            MIN_THREAD_POOL_SIZE: Final[int] = 1

        class Service:
            """gRPC service constants extending c.Service."""

            DEFAULT_MAX_CONCURRENT_RPCS: Final[int] = 1000
            DEFAULT_MAX_WORKERS: Final[int] = 10
            MAX_WORKERS: Final[int] = 100
            MIN_WORKERS: Final[int] = 1

        class Streaming:
            """Streaming configuration defaults."""

            BIDIRECTIONAL_STREAMING_QUEUE_SIZE: Final[int] = 1000
            CLIENT_STREAMING_BUFFER_THRESHOLD: Final[int] = 10
            DEFAULT_BUFFER_SIZE: Final[int] = 500
            DEFAULT_MAX_CONCURRENT_STREAMS: Final[int] = 10
            MAX_BUFFER_SIZE: Final[int] = 10000
            MIN_BUFFER_SIZE: Final[int] = 10
            SERVER_STREAMING_BATCH_SIZE: Final[int] = 100

        class Connection:
            """Connection pool defaults."""

            DEFAULT_POOL_SIZE: Final[int] = 20
            DEFAULT_TIMEOUT: Final[float] = float(
                FlextConstants.DEFAULT_TIMEOUT_SECONDS,
            )

        class Production:
            """gRPC production validation constants."""

            MIN_PORT: Final[int] = 1024
            RETRY_ATTEMPTS: Final[int] = FlextConstants.MAX_RETRY_ATTEMPTS
            MAX_RETRY_ATTEMPTS: Final[int] = 5

        class GrpcValidation:
            """gRPC validation constants extending c."""

            ADDRESS_PARTS_COUNT: Final[int] = 2
            MAX_PORT_NUMBER: Final[int] = 65535

        class GrpcMessages:
            """gRPC-specific error and status messages."""

            TIMEOUT_ERROR: Final[str] = "gRPC operation timed out after {timeout}s"

        class GrpcErrors:
            """gRPC-specific error codes."""

            CONNECTION_ERROR: Final[str] = "GRPC_CONNECTION_ERROR"
            TIMEOUT_ERROR: Final[str] = "GRPC_TIMEOUT_ERROR"
            VALIDATION_ERROR: Final[str] = "GRPC_VALIDATION_ERROR"
            SERVER_ERROR: Final[str] = "GRPC_SERVER_ERROR"

        class GrpcPerformance:
            """gRPC performance and health check constants."""

        class GrpcLimits:
            """gRPC request and error rate limits."""

        class Timeouts:
            """gRPC timeout validation constants."""

            MAX_TIMEOUT_SECONDS: Final[float] = 300.0

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

        CHANNEL_STATES: Final[tuple[str, ...]] = tuple(
            member.value for member in ChannelState.__members__.values()
        )
        """Channel states tuple - generated from ChannelState StrEnum."""

        COMPRESSION_TYPES: Final[tuple[str, ...]] = tuple(
            member.value for member in CompressionTypes.__members__.values()
        )
        """Compression types tuple - generated from CompressionTypes StrEnum."""

        LOAD_BALANCING_POLICIES: Final[tuple[str, ...]] = tuple(
            member.value for member in LoadBalancingPolicies.__members__.values()
        )
        """Load balancing policies tuple - generated from LoadBalancingPolicies StrEnum."""

        SERVER_STATES: Final[tuple[str, ...]] = tuple(
            member.value for member in ServerState.__members__.values()
        )
        """Server states tuple - generated from ServerState StrEnum."""

        STREAM_TYPES: Final[tuple[str, ...]] = tuple(
            member.value for member in GrpcOperations.__members__.values()
        )
        """Stream types tuple - generated from GrpcOperations StrEnum."""


c = FlextGrpcConstants

__all__: list[str] = ["FlextGrpcConstants", "c"]
