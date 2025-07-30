"""FLEXT gRPC Constants extending flext-core platform constants.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

# Import flext-core constants for inheritance
from flext_core.constants import FlextConstants


class FlextGrpcConstants(FlextConstants):
    """gRPC constants extending flext-core platform constants."""

    # Network Constants (hardcoded as project-specific)
    DEFAULT_HOST = "localhost"
    DEFAULT_PORT = 50051
    MIN_PORT = 1
    MAX_PORT = 65535

    # Service Constants (hardcoded as project-specific)
    DEFAULT_TIMEOUT = 60
    DEFAULT_MAX_WORKERS = 10
    MIN_WORKERS = 1
    MAX_WORKERS = 100

    # Validation Constants (hardcoded as project-specific)
    MAX_SERVICE_NAME_LENGTH = 255
    MAX_METHOD_NAME_LENGTH = 200
    MIN_TIMEOUT_SECONDS = 0.1
    MAX_TIMEOUT_SECONDS = 600.0

    # Operation Constants - following SOLID principles
    MIN_REQUIRED_ARGS = 2  # Minimum arguments for service operations

    # Host Name Pattern (extend core patterns)
    HOST_NAME_PATTERN = r"^[a-zA-Z0-9.-]+$"

    # Default Configuration
    DEFAULT_CONFIG: ClassVar[dict[str, object]] = {
        "host": DEFAULT_HOST,
        "port": DEFAULT_PORT,
        "timeout": DEFAULT_TIMEOUT,
        "max_workers": DEFAULT_MAX_WORKERS,
    }


# Legacy constants for backward compatibility
FLEXT_GRPC_DEFAULT_HOST = FlextGrpcConstants.DEFAULT_HOST
FLEXT_GRPC_DEFAULT_PORT = FlextGrpcConstants.DEFAULT_PORT
FLEXT_GRPC_MIN_PORT = FlextGrpcConstants.MIN_PORT
FLEXT_GRPC_MAX_PORT = FlextGrpcConstants.MAX_PORT
FLEXT_GRPC_DEFAULT_TIMEOUT = FlextGrpcConstants.DEFAULT_TIMEOUT
FLEXT_GRPC_DEFAULT_MAX_WORKERS = FlextGrpcConstants.DEFAULT_MAX_WORKERS
FLEXT_GRPC_MIN_WORKERS = FlextGrpcConstants.MIN_WORKERS
FLEXT_GRPC_MAX_WORKERS = FlextGrpcConstants.MAX_WORKERS
FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH = FlextGrpcConstants.MAX_SERVICE_NAME_LENGTH
FLEXT_GRPC_MAX_METHOD_NAME_LENGTH = FlextGrpcConstants.MAX_METHOD_NAME_LENGTH
FLEXT_GRPC_MIN_TIMEOUT_SECONDS = FlextGrpcConstants.MIN_TIMEOUT_SECONDS
FLEXT_GRPC_MAX_TIMEOUT_SECONDS = FlextGrpcConstants.MAX_TIMEOUT_SECONDS
FLEXT_GRPC_HOST_NAME_PATTERN = FlextGrpcConstants.HOST_NAME_PATTERN
FLEXT_GRPC_DEFAULT_CONFIG = FlextGrpcConstants.DEFAULT_CONFIG

# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Legacy constants for backward compatibility
    "FLEXT_GRPC_DEFAULT_CONFIG",
    "FLEXT_GRPC_DEFAULT_HOST",
    "FLEXT_GRPC_DEFAULT_MAX_WORKERS",
    "FLEXT_GRPC_DEFAULT_PORT",
    "FLEXT_GRPC_DEFAULT_TIMEOUT",
    "FLEXT_GRPC_HOST_NAME_PATTERN",
    "FLEXT_GRPC_MAX_METHOD_NAME_LENGTH",
    "FLEXT_GRPC_MAX_PORT",
    "FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH",
    "FLEXT_GRPC_MAX_TIMEOUT_SECONDS",
    "FLEXT_GRPC_MAX_WORKERS",
    "FLEXT_GRPC_MIN_PORT",
    "FLEXT_GRPC_MIN_TIMEOUT_SECONDS",
    "FLEXT_GRPC_MIN_WORKERS",
    # Main class
    "FlextGrpcConstants",
]
