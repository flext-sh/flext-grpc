"""FLEXT gRPC Configuration - Unified Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self

from pydantic import Field, field_validator

from flext_core import (
    FlextConfig,
    FlextExceptions,
)
from flext_grpc.constants import FlextGrpcConstants

# Constants are now imported from flext_grpc.constants - NO DUPLICATION

# Use FlextGrpcConstants from constants file


# Generate gRPC-specific exceptions
_grpc_exceptions = FlextExceptions.create_module_exception_classes("flext_grpc")
FlextGrpcConfigurationError = _grpc_exceptions["FLEXT_GRPCConfigurationError"]


class FlextGrpcConfig(FlextConfig):
    """Simplified gRPC configuration with validation using FlextGrpcConstants."""

    host: str = Field(
        default=FlextGrpcConstants.DEFAULT_HOST, description="gRPC server host"
    )
    port: int = Field(
        default=FlextGrpcConstants.DEFAULT_PORT, description="gRPC server port"
    )
    max_workers: int = Field(
        default=FlextGrpcConstants.DEFAULT_MAX_WORKERS,
        description="Maximum number of workers",
    )
    timeout: float = Field(
        default=FlextGrpcConstants.DEFAULT_TIMEOUT,
        description="Request timeout in seconds",
    )

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host is not empty."""
        if not v or not v.strip():
            msg = "Host cannot be empty"
            raise FlextGrpcConfigurationError(msg)
        return v.strip()

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port is within valid range."""
        if not (FlextGrpcConstants.MIN_PORT <= v <= FlextGrpcConstants.MAX_PORT):
            msg = (
                f"Port {v} must be between {FlextGrpcConstants.MIN_PORT} "
                f"and {FlextGrpcConstants.MAX_PORT}"
            )
            raise FlextGrpcConfigurationError(msg)
        return v

    @field_validator("max_workers")
    @classmethod
    def validate_max_workers(cls, v: int) -> int:
        """Validate max workers is within valid range."""
        if not (FlextGrpcConstants.MIN_WORKERS <= v <= FlextGrpcConstants.MAX_WORKERS):
            msg = (
                f"Max workers {v} must be between {FlextGrpcConstants.MIN_WORKERS} "
                f"and {FlextGrpcConstants.MAX_WORKERS}"
            )
            raise FlextGrpcConfigurationError(msg)
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        """Validate timeout is within valid range."""
        if not (
            FlextGrpcConstants.MIN_TIMEOUT_SECONDS
            <= v
            <= FlextGrpcConstants.MAX_TIMEOUT_SECONDS
        ):
            msg = (
                f"Timeout {v} must be between {FlextGrpcConstants.MIN_TIMEOUT_SECONDS} "
                f"and {FlextGrpcConstants.MAX_TIMEOUT_SECONDS} seconds"
            )
            raise FlextGrpcConfigurationError(msg)
        return v

    def get_address(self: Self) -> str:
        """Get formatted address string.

        Returns:
            Formatted address as "host:port"

        Example:
            >>> config: dict[str, object] = FlextGrpcConfig(
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
