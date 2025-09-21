"""FLEXT gRPC Configuration - Unified Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from dataclasses import dataclass

from flext_core import (
    FlextExceptions,
)
from flext_grpc.constants import FlextGrpcConstants

# Constants are now imported from flext_grpc.constants - NO DUPLICATION

# Use FlextGrpcConstants from constants file


# Generate gRPC-specific exceptions
_grpc_exceptions = FlextExceptions.create_module_exception_classes("flext_grpc")
FlextGrpcConfigurationError = _grpc_exceptions["FLEXT_GRPCConfigurationError"]


@dataclass
class FlextGrpcConfig:
    """Simplified gRPC configuration with validation using FlextGrpcConstants."""

    host: str = FlextGrpcConstants.DEFAULT_HOST
    port: int = FlextGrpcConstants.DEFAULT_PORT
    max_workers: int = FlextGrpcConstants.DEFAULT_MAX_WORKERS
    timeout: float = FlextGrpcConstants.DEFAULT_TIMEOUT

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        # Validate host
        if not self.host or not self.host.strip():
            msg = "Host cannot be empty"
            raise FlextGrpcConfigurationError(msg)
        self.host = self.host.strip()

        # Validate port
        if not (
            FlextGrpcConstants.MIN_PORT <= self.port <= FlextGrpcConstants.MAX_PORT
        ):
            msg = (
                f"Port {self.port} must be between {FlextGrpcConstants.MIN_PORT} "
                f"and {FlextGrpcConstants.MAX_PORT}"
            )
            raise FlextGrpcConfigurationError(msg)

        # Validate max_workers
        if not (
            FlextGrpcConstants.MIN_WORKERS
            <= self.max_workers
            <= FlextGrpcConstants.MAX_WORKERS
        ):
            msg = (
                f"Max workers {self.max_workers} must be between {FlextGrpcConstants.MIN_WORKERS} "
                f"and {FlextGrpcConstants.MAX_WORKERS}"
            )
            raise FlextGrpcConfigurationError(msg)

        # Validate timeout
        if not (
            FlextGrpcConstants.MIN_TIMEOUT_SECONDS
            <= self.timeout
            <= FlextGrpcConstants.MAX_TIMEOUT_SECONDS
        ):
            msg = (
                f"Timeout {self.timeout} must be between {FlextGrpcConstants.MIN_TIMEOUT_SECONDS} "
                f"and {FlextGrpcConstants.MAX_TIMEOUT_SECONDS} seconds"
            )
            raise FlextGrpcConfigurationError(msg)

    def get_address(self) -> str:
        """Get formatted address string.

        Returns:
            Formatted address as "host:port"

        Example:
            >>> config = FlextGrpcConfig(
            ...     host=FlextConstants.Platform.DEFAULT_HOST,
            ...     port=FlextConstants.Platform.GRPC_DEFAULT_PORT,
            ... )
            >>> config.get_address()
            'localhost:50051'

        """
        return f"{self.host}:{self.port}"


__all__ = [
    "FlextGrpcConfig",
]
