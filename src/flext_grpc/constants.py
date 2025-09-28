"""FLEXT gRPC Constants.

gRPC-specific constants including network settings, service configuration,
validation rules, and configuration defaults. Designed for consistent
configuration management and enterprise deployment standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final

from flext_core import FlextConstants


class FlextGrpcConstants(FlextConstants):
    """gRPC-specific constants following FLEXT unified single-class pattern.

    Inherits from FlextConstants for universal constants, defines only
    gRPC-specific constants using nested namespace classes.

    Layer N Foundation: gRPC domain-specific constants building on flext-core Layer 0.

    Usage:
        ```python
        from flext_grpc import FlextGrpcConstants

        timeout = FlextGrpcConstants.Service.DEFAULT_TIMEOUT
        port = FlextGrpcConstants.Network.DEFAULT_PORT
        ```
    """

    # Project metadata (Final attributes inherited from FlextConstants)
    # CONSTANTS_VERSION, PROJECT_PREFIX, PROJECT_NAME inherited from FlextConstants

    # gRPC-specific network constants
    DEFAULT_GRPC_PORT: Final[int] = 50051  # Standard gRPC port
    HOST_NAME_PATTERN: Final[str] = r"^[a-zA-Z0-9.-]+$"

    # Port validation constants
    MIN_PORT: Final[int] = FlextConstants.Network.MIN_PORT
    MAX_PORT: Final[int] = FlextConstants.Network.MAX_PORT

    # Default timeout constant
    DEFAULT_TIMEOUT: Final[float] = FlextConstants.Network.DEFAULT_TIMEOUT

    # Additional platform constants for gRPC
    METRICS_PORT: Final[int] = 9090  # Prometheus metrics port
    GRPC_DEFAULT_PORT: Final[int] = 50051  # Alias for DEFAULT_GRPC_PORT
    PRODUCTION_HOST: Final[str] = "127.0.0.1"  # Localhost for production binding
    LOCALHOST_IP: Final[str] = "127.0.0.1"  # Localhost IP address

    # gRPC keepalive constants (in milliseconds)
    DEFAULT_KEEPALIVE_TIME_MS: Final[int] = 30000  # 30 seconds
    DEFAULT_KEEPALIVE_TIMEOUT_MS: Final[int] = 5000  # 5 seconds

    # gRPC-specific service constants
    DEFAULT_MAX_WORKERS: Final[int] = FlextConstants.Container.MAX_WORKERS
    MIN_WORKERS: Final[int] = FlextConstants.Container.MIN_WORKERS
    MAX_WORKERS: Final[int] = 100
    MIN_REQUIRED_ARGS: Final[int] = 2

    # Production validation constants
    PRODUCTION_MIN_WORKERS: Final[int] = 5
    PRODUCTION_MIN_PORT: Final[int] = 1024
    HIGH_WORKER_THRESHOLD: Final[int] = 20
    HIGH_WORKER_TIMEOUT: Final[float] = 30.0
    PRODUCTION_RETRY_ATTEMPTS: Final[int] = 3
    PRODUCTION_RETRY_TIMEOUT: Final[float] = 30.0
    MAX_RETRY_ATTEMPTS: Final[int] = 5
    HIGH_RETRY_TIMEOUT: Final[float] = 10.0

    # gRPC-specific validation constants
    MAX_SERVICE_NAME_LENGTH: Final[int] = 255
    MAX_METHOD_NAME_LENGTH: Final[int] = 200

    # gRPC-specific error and status messages
    SERVICE_START_FAILED: Final[str] = "gRPC service failed to start: {error}"
    SERVICE_STARTED: Final[str] = "gRPC service started on {host}:{port}"
    CONNECTION_FAILED: Final[str] = "gRPC connection failed: {error}"
    TIMEOUT_ERROR: Final[str] = "gRPC operation timed out after {timeout}s"

    # gRPC-specific errors
    GRPC_SERVICE_ERROR: Final[str] = "GRPC_SERVICE_ERROR"
    GRPC_CONNECTION_ERROR: Final[str] = "GRPC_CONNECTION_ERROR"
    GRPC_TIMEOUT_ERROR: Final[str] = "GRPC_TIMEOUT_ERROR"

    # gRPC-specific network constants (not overriding parent)
    GRPC_DEFAULT_HOST: Final[str] = "127.0.0.1"
    GRPC_DEFAULT_TIMEOUT: Final[float] = 30.0

    # Performance and health check constants
    PERFORMANCE_EXCELLENT_LATENCY_MS: Final[int] = 100
    PERFORMANCE_GOOD_LATENCY_MS: Final[int] = 500
    PERFORMANCE_ACCEPTABLE_LATENCY_MS: Final[int] = 1000
    PERFORMANCE_EXCELLENT_ERROR_RATE: Final[float] = 1.0
    PERFORMANCE_GOOD_ERROR_RATE: Final[float] = 5.0
    PERFORMANCE_ACCEPTABLE_ERROR_RATE: Final[float] = 10.0
    HEALTH_CHECK_AGE_RECENT_SECONDS: Final[int] = 300  # 5 minutes
    SUCCESS_RATE_HEALTHY_PERCENT: Final[float] = 95.0
    RESPONSE_TIME_HEALTHY_MS: Final[int] = 1000

    # Request size limits
    MAX_REQUEST_SIZE_MB: Final[int] = 10

    # Error rate limits
    MAX_ERROR_RATE_PERCENT: Final[float] = 100.0


__all__: list[str] = [
    "FlextGrpcConstants",
]
