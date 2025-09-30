"""FLEXT gRPC Configuration - Unified Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Self, cast

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextExceptions,
)
from flext_grpc.constants import FlextGrpcConstants

# Constants are now imported from flext_grpc.constants - NO DUPLICATION

# Use FlextGrpcConstants from constants file


# Generate gRPC-specific exceptions
_grpc_exceptions = FlextExceptions.create_module_exception_classes("flext_grpc")
FlextGrpcConfigurationError = _grpc_exceptions["FLEXT_GRPCConfigurationError"]


class FlextGrpcConfig(FlextConfig):
    """Single Pydantic 2 Settings class for flext-grpc extending FlextConfig.

    Follows standardized pattern:
    - Extends FlextConfig from flext-core
    - No nested classes within Config
    - All defaults from FlextGrpcConstants
    - Uses enhanced singleton pattern with inverse dependency injection
    - Uses Pydantic 2.11+ features (field_validator, model_validator)
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_GRPC_",
        case_sensitive=False,
        extra="ignore",
        # Inherit enhanced Pydantic 2.11+ features from FlextConfig
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_extra={
            "title": "FLEXT gRPC Configuration",
            "description": "Enterprise gRPC service configuration extending FlextConfig",
        },
    )

    host: str = Field(
        default=FlextConstants.Platform.DEFAULT_HOST, description="gRPC server host"
    )
    port: int = Field(
        default=FlextGrpcConstants.DEFAULT_GRPC_PORT, description="gRPC server port"
    )
    max_workers: int = Field(
        default=FlextGrpcConstants.DEFAULT_MAX_WORKERS,
        description="Maximum number of workers",
    )
    timeout: float = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
        description="Request timeout in seconds",
    )

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host is not empty."""
        if not v or not v.strip():
            msg = "Host cannot be empty"
            raise ValueError(msg)
        return v.strip()

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port is within valid range."""
        if not (
            FlextConstants.Network.MIN_PORT <= v <= FlextConstants.Network.MAX_PORT
        ):
            msg = (
                f"Port {v} must be between {FlextConstants.Network.MIN_PORT} "
                f"and {FlextConstants.Network.MAX_PORT}"
            )
            raise ValueError(msg)
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
            raise ValueError(msg)
        return v

    @field_validator("timeout")
    @classmethod
    def validate_timeout(cls, v: float) -> float:
        """Validate timeout is within valid range."""
        min_timeout_seconds = FlextGrpcConstants.MIN_TIMEOUT_SECONDS
        max_timeout_seconds = FlextGrpcConstants.MAX_TIMEOUT_SECONDS
        if not (min_timeout_seconds <= v <= max_timeout_seconds):
            msg = f"Timeout {v} must be between {min_timeout_seconds} and {max_timeout_seconds} seconds"
            raise ValueError(msg)
        return v

    def get_address(self: Self) -> str:
        """Get formatted address string.

        Returns:
            Formatted address as "host:port"

        Example:
            >>> config: dict["str", "object"] = FlextGrpcConfig(
            ...     host=FlextConstants.Platform.DEFAULT_HOST,
            ...     port=FlextConstants.Platform.GRPC_DEFAULT_PORT,
            ... )
            >>> config.get_address()
            f'{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}'

        """
        return f"{self.host}:{self.port}"

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextGrpcConfig:
        """Create configuration for specific environment using enhanced singleton pattern."""
        return cast(
            "FlextGrpcConfig",
            cls.get_or_create_shared_instance(
                project_name="flext-grpc", environment=environment, **overrides
            ),
        )

    @classmethod
    def create_default(cls) -> FlextGrpcConfig:
        """Create default configuration instance using enhanced singleton pattern."""
        return cast(
            "FlextGrpcConfig",
            cls.get_or_create_shared_instance(project_name="flext-grpc"),
        )

    @classmethod
    def get_global_instance(cls) -> FlextGrpcConfig:
        """Get the global singleton instance using enhanced FlextConfig pattern."""
        return cast(
            "FlextGrpcConfig",
            cls.get_or_create_shared_instance(project_name="flext-grpc"),
        )

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextGrpcConfig instance (mainly for testing)."""
        # Use the enhanced FlextConfig reset mechanism
        # Reset the shared instance
        if hasattr(cls, "_shared_instance"):
            delattr(cls, "_shared_instance")


__all__ = [
    "FlextGrpcConfig",
]
