"""FLEXT gRPC Configuration - Unified Configuration Management.

🎯 CONSOLIDATES 2 CONFIGURATION FILES INTO SINGLE PEP8 MODULE:
- config.py (61 lines) - Core gRPC configuration with validation
- constants.py (213 lines) - Constants, defaults, and validation rules

TOTAL CONSOLIDATION: 274 lines → grpc_config.py (PEP8 organized)

This module provides unified configuration management for FLEXT gRPC platform,
combining configuration classes with comprehensive constants and validation rules.
Built on flext-core foundation patterns for enterprise deployment standards.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_core import (
    FlextBaseConfigModel,
    FlextConstants,
    create_module_exception_classes as _create_exc,
)
from pydantic import Field, field_validator

# =============================================================================
# GRPC CONFIGURATION CONSTANTS
# =============================================================================


class FlextGrpcSemanticConstants(FlextConstants):
    """gRPC-specific semantic constants extending FlextConstants.

    Modern Python 3.13 constants following semantic grouping patterns.
    Extends the FLEXT ecosystem constants with gRPC communication specific
    values while maintaining full backward compatibility.
    """

    class GrpcNetwork:
        """gRPC network configuration constants."""

        # CONSUME from single source - NO DUPLICATION
        DEFAULT_HOST = FlextConstants.Infrastructure.DEFAULT_HOST
        DEFAULT_PORT = 50051  # gRPC-specific port
        MIN_PORT = FlextConstants.Platform.MIN_PORT_NUMBER
        MAX_PORT = FlextConstants.Platform.MAX_PORT_NUMBER
        HOST_NAME_PATTERN = r"^[a-zA-Z0-9.-]+$"

    class Service:
        """Service configuration constants."""

        # CONSUME from single source - NO DUPLICATION
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

    class Config:
        """Default configuration templates."""

        DEFAULT_CONFIG: ClassVar[dict[str, object]] = {
            "host": FlextConstants.Infrastructure.DEFAULT_HOST,
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
    Config = FlextGrpcSemanticConstants.Config

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

    DEFAULT_CONFIG = FlextGrpcSemanticConstants.Config.DEFAULT_CONFIG


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

FLEXT_GRPC_DEFAULT_CONFIG = FlextGrpcSemanticConstants.Config.DEFAULT_CONFIG


# =============================================================================
# GRPC CONFIGURATION CLASSES
# =============================================================================

# Generate gRPC-specific exceptions
_grpc_exceptions = _create_exc("flext_grpc")
FlextGrpcConfigurationError = _grpc_exceptions["FLEXT_GRPCConfigurationError"]


class FlextGrpcConfig(FlextBaseConfigModel):
    """Simplified gRPC configuration with validation."""

    host: str = Field(default="localhost")
    port: int = Field(default=50051)
    max_workers: int = Field(default=10)
    timeout: float = Field(default=30.0)

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host configuration value."""
        if not v or not v.strip():
            msg = "Host cannot be empty"
            raise FlextGrpcConfigurationError(msg)
        return v.strip()

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port configuration value."""
        if not (FLEXT_GRPC_MIN_PORT <= v <= FLEXT_GRPC_MAX_PORT):
            msg = (
                f"Port {v} must be between {FLEXT_GRPC_MIN_PORT} "
                f"and {FLEXT_GRPC_MAX_PORT}"
            )
            raise FlextGrpcConfigurationError(msg)
        return v

    @field_validator("max_workers")
    @classmethod
    def validate_max_workers(cls, v: int) -> int:
        """Validate max_workers configuration value."""
        if not (FLEXT_GRPC_MIN_WORKERS <= v <= FLEXT_GRPC_MAX_WORKERS):
            msg = (
                f"Max workers {v} must be between {FLEXT_GRPC_MIN_WORKERS} "
                f"and {FLEXT_GRPC_MAX_WORKERS}"
            )
            raise FlextGrpcConfigurationError(msg)
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        """Validate timeout configuration value."""
        if not (FLEXT_GRPC_MIN_TIMEOUT_SECONDS <= v <= FLEXT_GRPC_MAX_TIMEOUT_SECONDS):
            msg = (
                f"Timeout {v} must be between {FLEXT_GRPC_MIN_TIMEOUT_SECONDS} "
                f"and {FLEXT_GRPC_MAX_TIMEOUT_SECONDS} seconds"
            )
            raise FlextGrpcConfigurationError(msg)
        return v

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


# =============================================================================
# EXPORTS
# =============================================================================

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
