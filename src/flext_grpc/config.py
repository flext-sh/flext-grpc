"""FLEXT gRPC Configuration - Configuration classes for gRPC components.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Configuration classes for gRPC clients and servers.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from flext_core import FlextCoreSettings
from pydantic import Field

# Constants
MAX_PORT_NUMBER = 65535
MIN_PORT_NUMBER = 1


class FlextGrpcServerConfig(FlextCoreSettings):
    """Configuration for gRPC servers using FLEXT Core patterns."""

    # Server configuration
    host: str = Field(
        default="localhost",
        description="gRPC server host address",
        env="FLEXT_GRPC_HOST",
    )
    port: int = Field(
        default=50051,
        description="gRPC server port",
        env="FLEXT_GRPC_PORT",
        ge=1,
        le=65535,
    )
    max_workers: int = Field(
        default=10,
        description="Maximum number of worker threads",
        env="FLEXT_GRPC_MAX_WORKERS",
        ge=1,
    )
    options: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional server options",
    )
    compression: str | None = Field(
        default=None,
        description="Compression algorithm",
        env="FLEXT_GRPC_COMPRESSION",
    )
    credentials: dict[str, Any] = Field(
        default_factory=dict,
        description="Server credentials configuration",
    )
    created_at: datetime = Field(
        default_factory=datetime.now(UTC),
        description="Creation timestamp",
    )

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        """Initialize gRPC server configuration.

        Args:
            kwargs: Configuration parameters
            host: Server host address
            port: Server port
            max_workers: Maximum number of worker threads
            options: Additional server options
            compression: Compression algorithm
            credentials: Server credentials configuration
            created_at: Creation timestamp

        """
        super().__init__(**kwargs)
        self.host: str = kwargs.get("host", "localhost")
        self.port: int = kwargs.get("port", 50051)
        self.max_workers: int = kwargs.get("max_workers", 10)
        self.options: dict[str, Any] = kwargs.get("options", {})
        self.compression: str | None = kwargs.get("compression")
        self.credentials: dict[str, Any] = kwargs.get("credentials", {})
        self.created_at: datetime = kwargs.get("created_at", datetime.now(UTC))

    def validate(self) -> bool:
        """Validate server configuration.

        Returns:
            True if configuration is valid, False otherwise

        """
        return (
            bool(self.host)
            and MIN_PORT_NUMBER <= self.port <= MAX_PORT_NUMBER
            and self.max_workers > 0
        )

    def get_address(self) -> str:
        """Get server address.

        Returns:
            Server address as host:port

        """
        return f"{self.host}:{self.port}"

    def is_secure(self) -> bool:
        """Check if server is configured for secure communication.

        Returns:
            True if credentials are configured, False otherwise

        """
        return bool(self.credentials)

    def update_host_port(self, host: str, port: int) -> None:
        """Update host and port configuration.

        Args:
            host: New host address
            port: New port number

        """
        self.host: str = host
        self.port: int = port

    def add_option(self, key: str, value: str | int | bool | None) -> None:
        """Add a server option.

        Args:
            key: Option key
            value: Option value

        """
        self.options[key] = value

    def remove_option(self, key: str) -> bool:
        """Remove a server option.

        Args:
            key: Option key to remove

        Returns:
            True if option was removed, False if not found

        """
        if key in self.options:
            del self.options[key]
            return True
        return False


class FlextGrpcClientConfig(FlextCoreSettings):
    """Configuration for gRPC clients using FLEXT Core patterns."""

    # Client configuration
    target: str = Field(
        default="localhost:50051",
        description="Target server address (host:port)",
        env="FLEXT_GRPC_TARGET",
    )
    options: dict[str, Any] = Field(
        default_factory=dict,
        description="Additional client options",
    )
    compression: str | None = Field(
        default=None,
        description="Compression algorithm",
        env="FLEXT_GRPC_COMPRESSION",
    )
    credentials: dict[str, Any] = Field(
        default_factory=dict,
        description="Client credentials configuration",
    )
    timeout: float | None = Field(
        default=30.0,
        description="Request timeout in seconds",
        env="FLEXT_GRPC_TIMEOUT",
        gt=0,
    )
    retry_config: dict[str, Any] = Field(
        default_factory=dict,
        description="Retry configuration",
    )

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        """Initialize gRPC client configuration.

        Args:
            kwargs: Configuration parameters
            target: Target server address
            options: Additional client options
            compression: Compression algorithm
            credentials: Client credentials configuration
            timeout: Request timeout in seconds
            retry_config: Retry configuration
            created_at: Creation timestamp

        """
        super().__init__(**kwargs)
        self.target: str = kwargs.get("target", "localhost:50051")
        self.options: dict[str, Any] = kwargs.get("options", {})
        self.compression: str | None = kwargs.get("compression")
        self.credentials: dict[str, Any] = kwargs.get("credentials", {})
        self.timeout: float | None = kwargs.get("timeout")
        self.retry_config: dict[str, Any] = kwargs.get("retry_config", {})
        self.created_at: datetime = kwargs.get("created_at", datetime.now(UTC))

    def validate(self) -> bool:
        """Validate client configuration.

        Returns:
            True if configuration is valid, False otherwise

        """
        return bool(self.target) and (self.timeout is None or self.timeout > 0)

    def is_secure(self) -> bool:
        """Check if client is configured for secure communication.

        Returns:
            True if credentials are configured, False otherwise

        """
        return bool(self.credentials)

    def has_retry_config(self) -> bool:
        """Check if retry configuration is set.

        Returns:
            True if retry configuration exists, False otherwise

        """
        return bool(self.retry_config)

    def update_target(self, target: str) -> None:
        """Update target server address.

        Args:
            target: New target address

        """
        self.target = target

    def set_timeout(self, timeout: float) -> None:
        """Set request timeout.

        Args:
            timeout: Timeout in seconds

        """
        if timeout > 0:
            self.timeout = timeout

    def add_option(self, key: str, value: str | int | bool | None) -> None:
        """Add a client option.

        Args:
            key: Option key
            value: Option value

        """
        self.options[key] = value

    def remove_option(self, key: str) -> bool:
        """Remove a client option.

        Args:
            key: Option key to remove

        Returns:
            True if option was removed, False if not found

        """
        if key in self.options:
            del self.options[key]
            return True
        return False

    def set_retry_config(
        self,
        max_attempts: int = 3,
        initial_backoff: float = 1.0,
        max_backoff: float = 120.0,
        backoff_multiplier: float = 2.0,
        retryable_status_codes: list[str] | None = None,
    ) -> None:
        """Set retry configuration.

        Args:
            max_attempts: Maximum number of retry attempts
            initial_backoff: Initial backoff time in seconds
            max_backoff: Maximum backoff time in seconds
            backoff_multiplier: Backoff multiplier
            retryable_status_codes: List of retryable status codes

        """
        self.retry_config = {
            "max_attempts": max_attempts,
            "initial_backoff": initial_backoff,
            "max_backoff": max_backoff,
            "backoff_multiplier": backoff_multiplier,
            "retryable_status_codes": retryable_status_codes or ["UNAVAILABLE"],
        }

    def clear_retry_config(self) -> None:
        """Clear retry configuration."""
        self.retry_config = {}


# Backwards compatibility aliases
GrpcServerConfig = FlextGrpcServerConfig
GrpcClientConfig = FlextGrpcClientConfig
