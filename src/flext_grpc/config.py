"""FLEXT gRPC Configuration - Unified Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import ClassVar

from flext_core import (
    FlextConstants,
    FlextExceptions,
    FlextTypes,
)


class FlextGrpcSemanticConstants(FlextConstants):
    """gRPC-specific semantic constants extending FlextConstants.

    Modern Python 3.13 constants following semantic grouping patterns.
    Extends the FLEXT ecosystem constants with gRPC communication specific
    values while maintaining full backward compatibility.
    """

    class GrpcNetwork:
        """gRPC network configuration constants."""

        # CONSUME from single source
        DEFAULT_HOST = FlextConstants.Platform.DEFAULT_HOST
        DEFAULT_PORT = 50051  # gRPC-specific port
        MIN_PORT = FlextConstants.Network.MIN_PORT
        MAX_PORT = FlextConstants.Network.MAX_PORT
        HOST_NAME_PATTERN = r"^[a-zA-Z0-9.-]+$"

    class Service:
        """Service configuration constants."""

        # CONSUME from single source
        DEFAULT_TIMEOUT = FlextConstants.Defaults.TIMEOUT
        DEFAULT_MAX_WORKERS = 10
        MIN_WORKERS = 1
        MAX_WORKERS = 100
        MIN_REQUIRED_ARGS = 2

    class GrpcValidation:
        """gRPC validation limits and patterns."""

        MAX_SERVICE_NAME_LENGTH = 255
        MAX_METHOD_NAME_LENGTH = 200
        MIN_TIMEOUT_SECONDS = 0.1
        MAX_TIMEOUT_SECONDS = 600.0

    class GrpcConfig:
        """Default configuration templates."""

        DEFAULT_CONFIG: ClassVar[FlextTypes.Core.Dict] = {
            "host": FlextConstants.Platform.DEFAULT_HOST,
            "port": 50051,
            "timeout": FlextConstants.Defaults.TIMEOUT,
            "max_workers": 10,
        }


class FlextGrpcConstants(FlextGrpcSemanticConstants):
    """gRPC constants with backward compatibility.

    Legacy compatibility layer providing both modern semantic access
    and traditional flat constant access patterns for smooth migration.
    """

    # Modern semantic access (Primary API) - direct references
    GrpcNetwork = FlextGrpcSemanticConstants.GrpcNetwork
    Service = FlextGrpcSemanticConstants.Service
    GrpcValidation = FlextGrpcSemanticConstants.GrpcValidation
    GrpcConfig = FlextGrpcSemanticConstants.GrpcConfig

    # Legacy compatibility - flat access patterns (DEPRECATED - use semantic access)
    DEFAULT_HOST = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_HOST
    DEFAULT_PORT = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_PORT
    MIN_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MIN_PORT
    MAX_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MAX_PORT
    HOST_NAME_PATTERN = FlextGrpcSemanticConstants.GrpcNetwork.HOST_NAME_PATTERN

    DEFAULT_TIMEOUT = FlextGrpcSemanticConstants.Service.DEFAULT_TIMEOUT
    DEFAULT_MAX_WORKERS = FlextGrpcSemanticConstants.Service.DEFAULT_MAX_WORKERS
    MIN_WORKERS = FlextGrpcSemanticConstants.Service.MIN_WORKERS
    MAX_WORKERS = FlextGrpcSemanticConstants.Service.MAX_WORKERS
    MIN_REQUIRED_ARGS = FlextGrpcSemanticConstants.Service.MIN_REQUIRED_ARGS

    MAX_SERVICE_NAME_LENGTH = (
        FlextGrpcSemanticConstants.GrpcValidation.MAX_SERVICE_NAME_LENGTH
    )
    MAX_METHOD_NAME_LENGTH = (
        FlextGrpcSemanticConstants.GrpcValidation.MAX_METHOD_NAME_LENGTH
    )
    MIN_TIMEOUT_SECONDS = FlextGrpcSemanticConstants.GrpcValidation.MIN_TIMEOUT_SECONDS
    MAX_TIMEOUT_SECONDS = FlextGrpcSemanticConstants.GrpcValidation.MAX_TIMEOUT_SECONDS

    DEFAULT_CONFIG = FlextGrpcSemanticConstants.GrpcConfig.DEFAULT_CONFIG


# Legacy module-level aliases for backward compatibility
FLEXT_GRPC_DEFAULT_HOST = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_HOST
FLEXT_GRPC_DEFAULT_PORT = FlextGrpcSemanticConstants.GrpcNetwork.DEFAULT_PORT
FLEXT_GRPC_MIN_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MIN_PORT
FLEXT_GRPC_MAX_PORT = FlextGrpcSemanticConstants.GrpcNetwork.MAX_PORT
FLEXT_GRPC_HOST_NAME_PATTERN = FlextGrpcSemanticConstants.GrpcNetwork.HOST_NAME_PATTERN

FLEXT_GRPC_DEFAULT_TIMEOUT = FlextGrpcSemanticConstants.Service.DEFAULT_TIMEOUT
FLEXT_GRPC_DEFAULT_MAX_WORKERS = FlextGrpcSemanticConstants.Service.DEFAULT_MAX_WORKERS
FLEXT_GRPC_MIN_WORKERS = FlextGrpcSemanticConstants.Service.MIN_WORKERS
FLEXT_GRPC_MAX_WORKERS = FlextGrpcSemanticConstants.Service.MAX_WORKERS

FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH = (
    FlextGrpcSemanticConstants.GrpcValidation.MAX_SERVICE_NAME_LENGTH
)
FLEXT_GRPC_MAX_METHOD_NAME_LENGTH = (
    FlextGrpcSemanticConstants.GrpcValidation.MAX_METHOD_NAME_LENGTH
)
FLEXT_GRPC_MIN_TIMEOUT_SECONDS = (
    FlextGrpcSemanticConstants.GrpcValidation.MIN_TIMEOUT_SECONDS
)
FLEXT_GRPC_MAX_TIMEOUT_SECONDS = (
    FlextGrpcSemanticConstants.GrpcValidation.MAX_TIMEOUT_SECONDS
)

FLEXT_GRPC_DEFAULT_CONFIG = FlextGrpcSemanticConstants.GrpcConfig.DEFAULT_CONFIG


# Generate gRPC-specific exceptions
_grpc_exceptions = FlextExceptions.create_module_exception_classes("flext_grpc")
FlextGrpcConfigurationError = _grpc_exceptions["FLEXT_GRPCConfigurationError"]


@dataclass
class FlextGrpcConfig:
    """Simplified gRPC configuration with validation."""

    host: str = "localhost"
    port: int = 50051
    max_workers: int = 10
    timeout: float = 30.0

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        # Validate host
        if not self.host or not self.host.strip():
            msg = "Host cannot be empty"
            raise FlextGrpcConfigurationError(msg)
        self.host = self.host.strip()

        # Validate port
        if not (FLEXT_GRPC_MIN_PORT <= self.port <= FLEXT_GRPC_MAX_PORT):
            msg = (
                f"Port {self.port} must be between {FLEXT_GRPC_MIN_PORT} "
                f"and {FLEXT_GRPC_MAX_PORT}"
            )
            raise FlextGrpcConfigurationError(msg)

        # Validate max_workers
        if not (FLEXT_GRPC_MIN_WORKERS <= self.max_workers <= FLEXT_GRPC_MAX_WORKERS):
            msg = (
                f"Max workers {self.max_workers} must be between {FLEXT_GRPC_MIN_WORKERS} "
                f"and {FLEXT_GRPC_MAX_WORKERS}"
            )
            raise FlextGrpcConfigurationError(msg)

        # Validate timeout
        if not (
            FLEXT_GRPC_MIN_TIMEOUT_SECONDS
            <= self.timeout
            <= FLEXT_GRPC_MAX_TIMEOUT_SECONDS
        ):
            msg = (
                f"Timeout {self.timeout} must be between {FLEXT_GRPC_MIN_TIMEOUT_SECONDS} "
                f"and {FLEXT_GRPC_MAX_TIMEOUT_SECONDS} seconds"
            )
            raise FlextGrpcConfigurationError(msg)

    def get_address(self) -> str:
        """Get formatted address string.

        Returns:
            Formatted address as "host:port"

        Example:
            >>> config = FlextGrpcConfig(host="localhost", port=50051)
            >>> config.get_address()
            'localhost:50051'

        """
        return f"{self.host}:{self.port}"


__all__ = [
    # Legacy module-level constants
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
    # Configuration classes
    "FlextGrpcConfig",
    "FlextGrpcConfigurationError",
    # Constants classes
    "FlextGrpcConstants",
    "FlextGrpcSemanticConstants",
]
