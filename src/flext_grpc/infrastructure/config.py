"""Configuration for FLEXT-GRPC infrastructure.

Uses flext-core BaseSettings with mixins, types, and constants.
Zero tolerance for duplication.
"""

from __future__ import annotations

import pathlib
from typing import Any

from pydantic import field_validator
from pydantic_settings import SettingsConfigDict

from flext_core.config import BaseSettings
from flext_core.config import get_container
from flext_core.config import singleton
from flext_core.domain.pydantic_base import Field
from flext_core.domain.types import FlextConstants
from flext_core.domain.types import ProjectName
from flext_core.domain.types import Version


@singleton()
class GRPCConfig(BaseSettings):
    """gRPC service configuration with enhanced types and constants."""

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_GRPC_",
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )

    # Project metadata
    project_name: ProjectName = Field(
        default="flext-grpc",
        description="Project name for service identification",
    )
    version: Version = Field(
        default="1.0.0",
        description="Service version",
    )

    # Server configuration
    host: str = Field(
        default="0.0.0.0",
        description="gRPC server host address",
    )
    port: int = Field(
        default=50051,
        ge=1024,
        le=65535,
        description="gRPC server port",
    )
    max_workers: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of worker threads",
    )
    max_concurrent_rpcs: int = Field(
        default=100,
        ge=1,
        le=1000,
        description="Maximum concurrent RPC calls",
    )
    max_message_size: int = Field(
        default=104857600,  # 100MB
        ge=1024,
        description="Maximum message size in bytes",
    )

    # SSL/TLS configuration
    ssl_enabled: bool = Field(
        default=False,
        description="Enable SSL/TLS encryption",
    )
    ssl_cert_path: str = Field(
        default="/etc/ssl/certs/server.crt",
        description="Path to SSL certificate file",
    )
    ssl_key_path: str = Field(
        default="/etc/ssl/private/server.key",
        description="Path to SSL private key file",
    )
    ssl_ca_path: str = Field(
        default="/etc/ssl/certs/ca.crt",
        description="Path to SSL CA certificate file",
    )

    # Keepalive configuration
    keepalive_time_ms: int = Field(
        default=10000,
        ge=1000,
        description="Keepalive time in milliseconds",
    )
    keepalive_timeout_ms: int = Field(
        default=5000,
        ge=1000,
        description="Keepalive timeout in milliseconds",
    )
    keepalive_permit_without_calls: bool = Field(
        default=True,
        description="Allow keepalive pings without active calls",
    )

    # Database settings (for service persistence)
    database_url: str = Field(
        default="postgresql://flext:flext@localhost:5432/flext_grpc",
        description="Database connection URL",
    )
    database_pool_size: int = Field(
        default=FlextConstants.DEFAULT_PAGE_SIZE,
        ge=1,
        description="Database connection pool size",
    )
    database_max_overflow: int = Field(
        default=FlextConstants.DEFAULT_PAGE_SIZE * 2,
        ge=0,
        description="Database pool max overflow",
    )

    # Redis settings (for caching/sessions)
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis connection URL",
    )
    redis_max_connections: int = Field(
        default=20,
        ge=1,
        description="Maximum Redis connections",
    )

    # Metrics and monitoring
    metrics_enabled: bool = Field(
        default=True,
        description="Enable Prometheus metrics collection",
    )
    metrics_port: int = Field(
        default=9090,
        ge=1024,
        le=65535,
        description="Metrics server port",
    )
    tracing_enabled: bool = Field(
        default=True,
        description="Enable distributed tracing",
    )

    # Authentication
    auth_enabled: bool = Field(
        default=True,
        description="Enable authentication for gRPC endpoints",
    )
    jwt_secret_key: str = Field(
        default="your-secret-key-here",
        description="JWT secret key for token validation",
    )

    @property
    def address(self) -> str:
        """Get the full server address."""
        return f"{self.host}:{self.port}"

    @property
    def ssl_credentials_available(self) -> bool:
        """Check if SSL credentials are available."""
        try:
            return (
                pathlib.Path(self.ssl_cert_path).is_file()
                and pathlib.Path(self.ssl_key_path).is_file()
            )
        except (OSError, FileNotFoundError, PermissionError):
            return False

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format.

        Args:
            v: Database URL to validate.

        Returns:
            Validated database URL.

        Raises:
            ValueError: If URL format is invalid.

        """
        if not v.startswith(("postgresql://", "postgresql+asyncpg://", "sqlite://")):
            msg = "Database URL must start with postgresql:// or sqlite://"
            raise ValueError(msg)
        return v

    @field_validator("redis_url")
    @classmethod
    def validate_redis_url(cls, v: str) -> str:
        """Validate Redis URL format.

        Args:
            v: Redis URL to validate.

        Returns:
            Validated Redis URL.

        Raises:
            ValueError: If URL format is invalid.

        """
        if not v.startswith(("redis://", "rediss://")):

            msg = "Redis URL must start with redis:// or rediss://"
            raise ValueError(msg)
        return v

    def configure_dependencies(self, container: Any = None) -> None:
        """Configure dependency injection container."""
        if container is None:
            container = get_container()

        # Register configuration instance
        container.register(GRPCConfig, self)

        # Call parent configuration
        super().configure_dependencies(container)


# Convenience function for getting settings
def get_grpc_config() -> GRPCConfig:
    container = get_container()
    return container.resolve(GRPCConfig)


# Convenience export for backward compatibility
# Note: Don't instantiate at module level to avoid circular dependencies
