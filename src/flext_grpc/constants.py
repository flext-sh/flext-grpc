"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from enum import StrEnum
from typing import Final, Literal

from flext_core import FlextConstants


class FlextGrpcConstants(FlextConstants):
    """gRPC-specific constants following FLEXT unified single-class pattern.

    Defines ALL constants used by the flext-grpc project, including inherited
    constants redefined for gRPC context. NO direct imports from c
    should be used - all constants must come from this class.

    Layer N Foundation: gRPC domain-specific constants building on flext-core Layer 0.

    Usage:
    ```python
    from flext_grpc.constants import FlextGrpcConstants

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

            # gRPC-specific network constants
            DEFAULT_HOST: Final[str] = "127.0.0.1"  # gRPC default host
            DEFAULT_GRPC_PORT: Final[int] = 50051  # Standard gRPC port
            HOST_NAME_PATTERN: Final[str] = r"^[a-zA-Z0-9.-]+$"

            # Port validation constants for gRPC
            MIN_PORT: Final[int] = 1  # gRPC allows port 1
            MAX_PORT: Final[int] = 65535  # Standard port range

            # Default timeout constant for gRPC context
            DEFAULT_TIMEOUT: Final[float] = float(
                FlextConstants.Network.DEFAULT_TIMEOUT,
            )  # gRPC default timeout

            # Additional platform constants for gRPC
            METRICS_PORT: Final[int] = 9090  # Prometheus metrics port
            HOST: Final[str] = "127.0.0.1"  # Localhost for production binding
            LOCALHOST_IP: Final[str] = "127.0.0.1"  # Localhost IP address

            # gRPC keepalive constants (in milliseconds)
            DEFAULT_KEEPALIVE_TIME_MS: Final[int] = 30000  # 30 seconds
            DEFAULT_KEEPALIVE_TIMEOUT_MS: Final[int] = 5000  # 5 seconds

            # Extracted magic values from settings.py
            HTTP_PORT: Final[int] = 80  # Standard HTTP port
            GRPC_PORT: Final[int] = 50051  # Standard gRPC port
            KEEPALIVE_TIME_SECONDS: Final[int] = 30  # Keepalive time in seconds
            KEEPALIVE_TIMEOUT_SECONDS: Final[int] = 5  # Keepalive timeout in seconds

        class Service:
            """gRPC service constants extending c.Service."""

            # gRPC-specific service constants - OVERRIDE parent constants
            DEFAULT_MAX_WORKERS: Final[int] = 10  # gRPC default workers
            MIN_WORKERS: Final[int] = 1  # Minimum gRPC workers
            MAX_WORKERS: Final[int] = 100  # Maximum gRPC workers
            DEFAULT_MAX_CONCURRENT_RPCS: Final[int] = 1000
            MIN_REQUIRED_ARGS: Final[int] = 2

        class Connection:
            """gRPC connection and performance constants."""

            # Extracted magic values from settings.py
            MAX_CONNECTIONS: Final[int] = 1000  # Maximum concurrent connections
            MAX_WORKERS: Final[int] = 20  # Maximum worker threads
            MAX_CONCURRENT_RPCS: Final[int] = 200  # Maximum concurrent RPC calls
            MAX_CONCURRENT_STREAMS: Final[int] = 50  # Maximum concurrent streams
            DEFAULT_TIMEOUT: Final[float] = 30.0  # Default operation timeout in seconds
            THREAD_POOL_SIZE: Final[int] = 100  # Thread pool size for operations

        class Production:
            """gRPC production validation constants."""

            # Production validation constants
            MIN_WORKERS: Final[int] = 5
            MIN_PORT: Final[int] = 1024
            HIGH_WORKER_THRESHOLD: Final[int] = 20
            HIGH_WORKER_TIMEOUT: Final[float] = float(
                FlextConstants.Network.DEFAULT_TIMEOUT,
            )
            RETRY_ATTEMPTS: Final[int] = 3
            RETRY_TIMEOUT: Final[float] = float(FlextConstants.Network.DEFAULT_TIMEOUT)
            MAX_RETRY_ATTEMPTS: Final[int] = 5  # Maximum retry attempts for gRPC
            HIGH_RETRY_TIMEOUT: Final[float] = 10.0

        class GrpcValidation:
            """gRPC validation constants extending c.Validation."""

            # Additional gRPC-specific constants
            ADDRESS_PARTS_COUNT: Final[int] = 2
            MAX_PORT_NUMBER: Final[int] = 65535

            # gRPC-specific validation constants
            MAX_SERVICE_NAME_LENGTH: Final[int] = 255
            MAX_METHOD_NAME_LENGTH: Final[int] = 200

        class GrpcMessages:
            """gRPC-specific error and status messages."""

            # gRPC-specific error and status messages
            SERVICE_START_FAILED: Final[str] = "gRPC service failed to start: {error}"
            SERVICE_STARTED: Final[str] = "gRPC service started on {host}:{port}"
            CONNECTION_FAILED: Final[str] = "gRPC connection failed: {error}"
            TIMEOUT_ERROR: Final[str] = "gRPC operation timed out after {timeout}s"

        class GrpcErrors:
            """gRPC-specific error codes."""

            # gRPC-specific errors
            GRPC_BASE_ERROR: Final[str] = "GRPC_BASE_ERROR"
            CONFIG_ERROR: Final[str] = "GRPC_CONFIG_ERROR"
            CONNECTION_ERROR: Final[str] = "GRPC_CONNECTION_ERROR"
            TIMEOUT_ERROR: Final[str] = "GRPC_TIMEOUT_ERROR"
            VALIDATION_ERROR: Final[str] = "GRPC_VALIDATION_ERROR"
            SERVER_ERROR: Final[str] = "GRPC_SERVER_ERROR"
            CLIENT_ERROR: Final[str] = "GRPC_CLIENT_ERROR"
            STREAM_ERROR: Final[str] = "GRPC_STREAM_ERROR"
            PROTOCOL_ERROR: Final[str] = "GRPC_PROTOCOL_ERROR"

        class GrpcPerformance:
            """gRPC performance and health check constants."""

            # Performance and health check constants
            EXCELLENT_LATENCY_MS: Final[int] = 100
            GOOD_LATENCY_MS: Final[int] = 500
            ACCEPTABLE_LATENCY_MS: Final[int] = 1000
            EXCELLENT_ERROR_RATE: Final[float] = 1.0
            GOOD_ERROR_RATE: Final[float] = 5.0
            ACCEPTABLE_ERROR_RATE: Final[float] = 10.0
            HEALTH_CHECK_AGE_RECENT_SECONDS: Final[int] = 300  # 5 minutes
            SUCCESS_RATE_HEALTHY_PERCENT: Final[float] = 95.0
            RESPONSE_TIME_HEALTHY_MS: Final[int] = 1000

        class GrpcLimits:
            """gRPC request and error rate limits."""

            # Request size limits
            MAX_REQUEST_SIZE_MB: Final[int] = 10
            # Error rate limits
            MAX_ERROR_RATE_PERCENT: Final[float] = 100.0
            # Platform configuration constants
            MIN_CONCURRENT_STREAMS: Final[int] = 50
            MIN_KEEPALIVE_TIME_MS: Final[int] = 30000
            MAX_CONCURRENT_STREAMS_LIMIT: Final[int] = 10000

        class Timeouts:
            """gRPC timeout validation constants."""

            # Timeout validation constants
            MIN_TIMEOUT_SECONDS: Final[float] = 0.1
            MAX_TIMEOUT_SECONDS: Final[float] = 300.0  # 5 minutes
            MAX_RESPONSE_COUNT: Final[int] = 10

        class Streaming:
            """gRPC streaming constants."""

            # Streaming constants (moved from services.py)
            CLIENT_STREAMING_BUFFER_THRESHOLD: Final[int] = 10
            SERVER_STREAMING_BATCH_SIZE: Final[int] = 100
            BIDIRECTIONAL_STREAMING_QUEUE_SIZE: Final[int] = 1000
            MAX_BUFFER_SIZE_BYTES: Final[int] = 10 * 1024 * 1024  # 10MB
            ADAPTIVE_BUFFER_SCALING_FACTOR: Final[float] = 0.8
            MEMORY_PRESSURE_THRESHOLD: Final[float] = 0.8
            STREAM_TIMEOUT_SECONDS: Final[float] = 300.0  # 5 minutes
            MAX_CONCURRENT_STREAMS: Final[int] = 100
            HEARTBEAT_INTERVAL_SECONDS: Final[float] = float(
                FlextConstants.Network.DEFAULT_TIMEOUT,
            )

        # ═══════════════════════════════════════════════════════════════════
        # STRENUM CLASSES (Single Source of Truth - Defined First)
        # ═══════════════════════════════════════════════════════════════════

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

        class CompressionTypes(StrEnum):
            """gRPC compression types (single source of truth).

            DRY Pattern:
                StrEnum is the single source of truth. Use CompressionTypes.NONE.value
                or CompressionTypes.NONE directly - no base strings needed.
            """

            NONE = "none"
            GZIP = "gzip"
            DEFLATE = "deflate"

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

        # ═══════════════════════════════════════════════════════════════════
        # LITERAL TYPES (PEP 695 - Reference StrEnum Members)
        # ═══════════════════════════════════════════════════════════════════

        # Channel state literal - references ChannelState StrEnum members
        type ChannelStateLiteral = Literal[
            "idle",
            "connecting",
            "ready",
            "transient_failure",
            "shutdown",
        ]
        """Channel state literal - references ChannelState StrEnum members."""

        # Server state literal - references ServerState StrEnum members
        type ServerStateLiteral = Literal[
            "stopped",
            "starting",
            "running",
            "stopping",
        ]
        """Server state literal - references ServerState StrEnum members."""

        # Stream type literal - references GrpcOperations StrEnum members
        type StreamTypeLiteral = Literal[
            "unary",
            "server_streaming",
            "client_streaming",
            "bidirectional",
        ]
        """Stream type literal - references GrpcOperations StrEnum members."""

        # Load balancing policy literal - references LoadBalancingPolicies StrEnum members
        type LoadBalancingPolicyLiteral = Literal[
            "round_robin",
            "pick_first",
            "grpclb",
            "xds_cluster_resolver",
        ]
        """Load balancing policy literal - references LoadBalancingPolicies StrEnum members."""

        # Compression type literal - references CompressionTypes StrEnum members
        type CompressionTypeLiteral = Literal[
            "none",
            "gzip",
            "deflate",
        ]
        """Compression type literal - references CompressionTypes StrEnum members."""

        # gRPC operation literal - references GrpcOperations StrEnum members
        type GrpcOperationLiteral = Literal[
            "unary",
            "server_streaming",
            "client_streaming",
            "bidirectional",
        ]
        """gRPC operation literal - references GrpcOperations StrEnum members."""

        # ═══════════════════════════════════════════════════════════════════
        # GENERATED TUPLES (From StrEnum - Single Source of Truth)
        # ═══════════════════════════════════════════════════════════════════

        # Channel states tuple - generated from ChannelState StrEnum
        CHANNEL_STATES: Final[tuple[str, ...]] = tuple(
            member.value for member in ChannelState.__members__.values()
        )
        """Channel states tuple - generated from ChannelState StrEnum."""

        # Server states tuple - generated from ServerState StrEnum
        SERVER_STATES: Final[tuple[str, ...]] = tuple(
            member.value for member in ServerState.__members__.values()
        )
        """Server states tuple - generated from ServerState StrEnum."""

        # Stream types tuple - generated from GrpcOperations StrEnum
        STREAM_TYPES: Final[tuple[str, ...]] = tuple(
            member.value for member in GrpcOperations.__members__.values()
        )
        """Stream types tuple - generated from GrpcOperations StrEnum."""

        # Load balancing policies tuple - generated from LoadBalancingPolicies StrEnum
        LOAD_BALANCING_POLICIES: Final[tuple[str, ...]] = tuple(
            member.value for member in LoadBalancingPolicies.__members__.values()
        )
        """Load balancing policies tuple - generated from LoadBalancingPolicies StrEnum."""

        # Compression types tuple - generated from CompressionTypes StrEnum
        COMPRESSION_TYPES: Final[tuple[str, ...]] = tuple(
            member.value for member in CompressionTypes.__members__.values()
        )
        """Compression types tuple - generated from CompressionTypes StrEnum."""


c = FlextGrpcConstants

__all__: list[str] = [
    "FlextGrpcConstants",
    "c",
]
