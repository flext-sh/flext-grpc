"""Private constants base for flext-grpc.

Owns every plain-literal scalar constant value so the public ``constants.py``
facade module never declares a bare literal class attribute directly
(ENFORCE-079); the facade re-exports them via ``c.Grpc.*`` through
inheritance.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Final


class FlextGrpcConstantsBase:
    """Private constants owner for gRPC scalar defaults."""

    # ===== Network constants =====
    NETWORK_DEFAULT_TIMEOUT: Final[float] = 30.0
    NETWORK_DEFAULT_CHANNEL_READY_TIMEOUT: Final[float] = 5.0
    NETWORK_DEFAULT_GRACEFUL_SHUTDOWN_TIMEOUT: Final[float] = 2.0
    NETWORK_DEFAULT_GRPC_PORT: Final[int] = 50051
    NETWORK_DEFAULT_HOST: Final[str] = "127.0.0.1"
    NETWORK_DEFAULT_KEEPALIVE_TIME_MS: Final[int] = 30000
    NETWORK_DEFAULT_KEEPALIVE_TIMEOUT_MS: Final[int] = 5000
    NETWORK_MAX_PORT: Final[int] = 65535
    NETWORK_MIN_PORT: Final[int] = 1
    NETWORK_HOST_PATTERN: Final[str] = r"^[a-zA-Z0-9.-]+$"

    # ===== Performance limits =====
    PERFORMANCE_DEFAULT_THREAD_POOL_SIZE: Final[int] = 50
    PERFORMANCE_MAX_THREAD_POOL_SIZE: Final[int] = 200
    PERFORMANCE_MIN_MESSAGE_LENGTH: Final[int] = 1024
    PERFORMANCE_MIN_THREAD_POOL_SIZE: Final[int] = 1

    # ===== Service constants =====
    SERVICE_DEFAULT_MAX_CONCURRENT_RPCS: Final[int] = 1000
    SERVICE_DEFAULT_MAX_WORKERS: Final[int] = 10
    SERVICE_MAX_WORKERS: Final[int] = 100
    SERVICE_MIN_WORKERS: Final[int] = 1

    # ===== Streaming configuration =====
    BIDIRECTIONAL_STREAMING_QUEUE_SIZE: Final[int] = 1000
    CLIENT_STREAMING_BUFFER_THRESHOLD: Final[int] = 10
    STREAMING_DEFAULT_BUFFER_SIZE: Final[int] = 500
    STREAMING_DEFAULT_MAX_CONCURRENT_STREAMS: Final[int] = 10
    STREAMING_MAX_BUFFER_SIZE: Final[int] = 10000
    STREAMING_MIN_BUFFER_SIZE: Final[int] = 10
    SERVER_STREAMING_BATCH_SIZE: Final[int] = 100

    # ===== Connection pool defaults =====
    CONNECTION_DEFAULT_POOL_SIZE: Final[int] = 20

    # ===== Validation constants =====
    VALIDATION_ADDRESS_PARTS_COUNT: Final[int] = 2
    VALIDATION_MAX_PORT_NUMBER: Final[int] = 65535
    VALIDATION_VERSION_PATTERN: Final[str] = r"Version.*(\d+\.\d+\.\d+)"


__all__: list[str] = ["FlextGrpcConstantsBase"]
