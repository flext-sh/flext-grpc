"""FLEXT gRPC Configuration - Unified Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import threading
from typing import ClassVar, Self

from pydantic import Field, field_validator
from pydantic_settings import SettingsConfigDict

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
    """Single Pydantic 2 Settings class for flext-grpc extending FlextConfig.

    Follows standardized pattern:
    - Extends FlextConfig from flext-core
    - No nested classes within Config
    - All defaults from FlextGrpcConstants
    - Dependency injection integration with flext-core container
    - Uses Pydantic 2.11+ features (field_validator, model_validator)
    """

    # Singleton pattern attributes
    _global_instance: ClassVar[FlextGrpcConfig | None] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    model_config = SettingsConfigDict(
        env_prefix=FLEXT_GRPC_,
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra=ignore,
        validate_assignment=True,
        use_enum_values=True,
        arbitrary_types_allowed=True,
    )

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
            >>> config: dict["str", "object"] = FlextGrpcConfig(
            ...     host=FlextConstants.Platform.DEFAULT_HOST,
            ...     port=FlextConstants.Platform.GRPC_DEFAULT_PORT,
            ... )
            >>> config.get_address()
            'localhost:50051'

        """
        return f"{self.host}:{self.port}"

    @classmethod
    def create_for_environment(
        cls, environment: str, **overrides: object
    ) -> FlextGrpcConfig:
        """Create configuration for specific environment."""
        return cls(environment=environment, **overrides)

    @classmethod
    def create_default(cls) -> FlextGrpcConfig:
        """Create default configuration instance."""
        return cls()

    # Singleton pattern override for proper typing
    @classmethod
    def get_global_instance(cls) -> FlextGrpcConfig:
        """Get the global singleton instance of FlextGrpcConfig."""
        if cls._global_instance is None:
            with cls._lock:
                if cls._global_instance is None:
                    cls._global_instance = cls()
        return cls._global_instance

    @classmethod
    def reset_global_instance(cls) -> None:
        """Reset the global FlextGrpcConfig instance (mainly for testing)."""
        cls._global_instance = None


__all__ = [
    "FlextGrpcConfig",
]
