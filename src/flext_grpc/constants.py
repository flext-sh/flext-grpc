"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Final, Literal

from flext_core import FlextCore


class FlextGrpcConstants(FlextCore.Constants):
    """gRPC-specific constants following FLEXT unified single-class pattern.

    Defines ALL constants used by the flext-grpc project, including inherited
    constants redefined for gRPC context. NO direct imports from FlextCore.Constants
    should be used - all constants must come from this class.

    Layer N Foundation: gRPC domain-specific constants building on flext-core Layer 0.

    Usage:
        ```python
        from flext_grpc.constants import FlextGrpcConstants

        timeout = FlextGrpcConstants.Network.DEFAULT_TIMEOUT
        port = FlextGrpcConstants.Network.DEFAULT_GRPC_PORT
        ```
    """

    class Network:
        """gRPC network constants extending FlextCore.Constants.Network."""

        # gRPC-specific network constants - OVERRIDE parent constants for gRPC context
        DEFAULT_HOST: Final[str] = "127.0.0.1"  # gRPC default host
        DEFAULT_GRPC_PORT: Final[int] = 50051  # Standard gRPC port
        HOST_NAME_PATTERN: Final[str] = r"^[a-zA-Z0-9.-]+$"

        # Port validation constants - OVERRIDE for gRPC-specific ranges
        MIN_PORT: Final[int] = 1  # gRPC allows port 1
        MAX_PORT: Final[int] = 65535  # Standard port range

        # Default timeout constant - OVERRIDE for gRPC context
        DEFAULT_TIMEOUT: Final[float] = 30.0  # gRPC default timeout

        # Additional platform constants for gRPC
        METRICS_PORT: Final[int] = 9090  # Prometheus metrics port
        GRPC_DEFAULT_PORT: Final[int] = 50051  # Alias for DEFAULT_GRPC_PORT
        HOST: Final[str] = "127.0.0.1"  # Localhost for production binding
        LOCALHOST_IP: Final[str] = "127.0.0.1"  # Localhost IP address

        # gRPC keepalive constants (in milliseconds)
        DEFAULT_KEEPALIVE_TIME_MS: Final[int] = 30000  # 30 seconds
        DEFAULT_KEEPALIVE_TIMEOUT_MS: Final[int] = 5000  # 5 seconds

    class Service:
        """gRPC service constants extending FlextCore.Constants.Service."""

        # gRPC-specific service constants - OVERRIDE parent constants
        DEFAULT_MAX_WORKERS: Final[int] = 10  # gRPC default workers
        MIN_WORKERS: Final[int] = 1  # Minimum gRPC workers
        MAX_WORKERS: Final[int] = 100  # Maximum gRPC workers
        DEFAULT_MAX_CONCURRENT_RPCS: Final[int] = 1000
        MIN_REQUIRED_ARGS: Final[int] = 2

    class Production:
        """gRPC production validation constants."""

        # Production validation constants
        MIN_WORKERS: Final[int] = 5
        MIN_PORT: Final[int] = 1024
        HIGH_WORKER_THRESHOLD: Final[int] = 20
        HIGH_WORKER_TIMEOUT: Final[float] = 30.0
        RETRY_ATTEMPTS: Final[int] = 3
        RETRY_TIMEOUT: Final[float] = 30.0
        MAX_RETRY_ATTEMPTS: Final[int] = 5  # Maximum retry attempts for gRPC
        HIGH_RETRY_TIMEOUT: Final[float] = 10.0

    class Validation:
        """gRPC validation constants extending FlextCore.Constants.Validation."""

        # Additional gRPC-specific constants
        ADDRESS_PARTS_COUNT: Final[int] = 2
        MAX_PORT_NUMBER: Final[int] = 65535

        # gRPC-specific validation constants
        MAX_SERVICE_NAME_LENGTH: Final[int] = 255
        MAX_METHOD_NAME_LENGTH: Final[int] = 200

    class Messages:
        """gRPC-specific error and status messages."""

        # gRPC-specific error and status messages
        SERVICE_START_FAILED: Final[str] = "gRPC service failed to start: {error}"
        SERVICE_STARTED: Final[str] = "gRPC service started on {host}:{port}"
        CONNECTION_FAILED: Final[str] = "gRPC connection failed: {error}"
        TIMEOUT_ERROR: Final[str] = "gRPC operation timed out after {timeout}s"

    class Errors:
        """gRPC-specific error codes."""

        # gRPC-specific errors
        GRPC_SERVICE_ERROR: Final[str] = "GRPC_SERVICE_ERROR"
        GRPC_CONNECTION_ERROR: Final[str] = "GRPC_CONNECTION_ERROR"
        GRPC_TIMEOUT_ERROR: Final[str] = "GRPC_TIMEOUT_ERROR"

    class Performance:
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

    class Limits:
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
        HEARTBEAT_INTERVAL_SECONDS: Final[float] = 30.0

    class Literals:
        """gRPC-specific literal types following FLEXT patterns."""

        # Channel state literals
        CHANNEL_STATES: Final[tuple[str, ...]] = (
            "idle",
            "connecting",
            "ready",
            "transient_failure",
            "shutdown",
        )
        type ChannelState = Literal[
            "idle", "connecting", "ready", "transient_failure", "shutdown"
        ]

        # Server state literals
        SERVER_STATES: Final[tuple[str, ...]] = (
            "stopped",
            "starting",
            "running",
            "stopping",
        )
        type ServerState = Literal["stopped", "starting", "running", "stopping"]

        # Stream type literals
        STREAM_TYPES: Final[tuple[str, ...]] = (
            "unary",
            "server_streaming",
            "client_streaming",
            "bidirectional",
        )
        type StreamType = Literal[
            "unary", "server_streaming", "client_streaming", "bidirectional"
        ]

        # Load balancing policy literals
        LOAD_BALANCING_POLICIES: Final[tuple[str, ...]] = (
            "round_robin",
            "pick_first",
            "grpclb",
            "xds_cluster_resolver",
        )
        type LoadBalancingPolicy = Literal[
            "round_robin", "pick_first", "grpclb", "xds_cluster_resolver"
        ]

        # Compression literals
        COMPRESSION_TYPES: Final[tuple[str, ...]] = ("none", "gzip", "deflate")
        type CompressionType = Literal["none", "gzip", "deflate"]


__all__: FlextCore.Types.StringList = [
    "FlextGrpcConstants",
]
