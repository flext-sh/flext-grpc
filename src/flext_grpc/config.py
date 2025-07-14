"""FLEXT gRPC Configuration - Modern Python 3.13 + Clean Architecture + DI.

REFACTORED:
    Uses flext-core BaseSettings with types and constants.
Zero tolerance for duplication.
"""

from __future__ import annotations

import pathlib
from typing import Any

from pydantic import Field
from pydantic import field_validator
from pydantic_settings import SettingsConfigDict

from flext_core.config import BaseSettings
from flext_core.config import get_container
from flext_core.config import singleton
from flext_core.domain.constants import FlextFramework


@singleton()
class GRPCSettings(BaseSettings):
    """FLEXT gRPC configuration settings with environment variable support.

    All settings can be overridden via environment variables with the
    prefix FLEXT_GRPC_ (e.g., FLEXT_GRPC_HOST).
    Uses flext-core BaseSettings foundation with DI support.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_GRPC_",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
        use_enum_values=True,
    )

    # Project identification
    project_name: str = Field("flext-grpc", description="Project name")
    project_version: str = Field(FlextFramework.VERSION, description="Project version")

    # Server configuration
    host: str = Field(
        "0.0.0.0",  # nosec B104 # gRPC server needs to bind to all interfaces
        description="gRPC server host address",
    )
    port: int = Field(
        50051,
        ge=1024,
        le=65535,
        description="gRPC server port",
    )
    max_workers: int = Field(
        10,
        ge=1,
        le=100,
        description="Maximum number of worker threads",
    )
    max_concurrent_rpcs: int = Field(
        100,
        ge=1,
        le=1000,
        description="Maximum concurrent RPC calls",
    )
    max_message_size: int = Field(
        104857600,  # 100MB
        ge=1024,
        description="Maximum message size in bytes",
    )

    # SSL/TLS configuration
    ssl_enabled: bool = Field(
        default=False,
        description="Enable SSL/TLS encryption",
    )
    ssl_cert_path: str = Field(
        default="",
        description="Path to SSL certificate file",
    )
    ssl_key_path: str = Field(
        default="",
        description="Path to SSL private key file",
    )
    ssl_ca_cert_path: str = Field(
        default="",
        description="Path to SSL CA certificate file",
    )

    # Authentication
    auth_enabled: bool = Field(
        default=True,
        description="Enable authentication for gRPC endpoints",
    )
    auth_secret_key: str = Field(
        default="",
        description="Secret key for JWT authentication",
    )
    auth_token_expiry: int = Field(
        default=3600,
        description="Token expiry time in seconds",
    )

    # Metrics and monitoring
    metrics_enabled: bool = Field(
        default=True,
        description="Enable Prometheus metrics collection",
    )
    metrics_port: int = Field(
        default=9090,
        description="Prometheus metrics port",
    )
    tracing_enabled: bool = Field(
        default=True,
        description="Enable distributed tracing",
    )
    tracing_endpoint: str = Field(
        default="http://localhost:14268/api/traces",
        description="Jaeger tracing endpoint",
    )

    # Connection settings
    max_connections: int = Field(
        default=1000,
        description="Maximum number of concurrent connections",
    )
    connection_timeout: int = Field(
        default=30,
        description="Connection timeout in seconds",
    )

    # Environment and debugging
    environment: str = Field(default="development", description="Environment name")
    debug: bool = Field(default=False, description="Debug mode")

    @property
    def address(self) -> str:
        """Get the full server address."""
        return f"{self.host}:{self.port}"

    @property
    def ssl_credentials_available(self) -> bool:
        """Check if SSL credentials are available and valid."""
        try:
            return (
                self.ssl_enabled
                and self.ssl_cert_path
                and self.ssl_key_path
                and pathlib.Path(self.ssl_cert_path).is_file()
                and pathlib.Path(self.ssl_key_path).is_file()
            )
        except (OSError, FileNotFoundError, PermissionError):
            return False

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL format."""
        if not v.startswith(("postgresql://", "postgresql+asyncpg://", "sqlite://")):
            msg = "Database URL must start with postgresql:// or sqlite://"
            raise ValueError(msg)
        return v

    def configure_dependencies(self, container: Any = None) -> None:
        """Configure dependencies in container."""
        if container is None:
            container = get_container()

        # Register this settings instance
        container.register(GRPCSettings, self)

        # Call parent configuration
        super().configure_dependencies(container)


# Convenience function for getting settings
def get_grpc_settings() -> GRPCSettings:
    """Get gRPC settings instance."""
    return GRPCSettings()
