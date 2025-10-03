"""FLEXT gRPC Configuration - Advanced Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Literal

from pydantic import Field, field_validator, model_validator
from pydantic_settings import SettingsConfigDict

from flext_core import (
    FlextConfig,
    FlextConstants,
    FlextExceptions,
    FlextResult,
)
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.models import FlextGrpcModels

# Generate gRPC-specific exceptions
_grpc_exceptions = FlextExceptions.create_module_exception_classes("flext_grpc")
FlextGrpcConfigurationError = _grpc_exceptions.get("FlextGrpcConfigurationError", Exception)


class FlextGrpcConfig(FlextConfig):
    """Advanced gRPC configuration extending FlextConfig with enterprise features.

    Leverages FlextConfig's advanced capabilities:
    - Multi-source configuration loading (env, files, secrets)
    - Configuration profiles and environments
    - Enhanced validation and transformation
    - Singleton management with dependency injection
    - Environment-specific overrides

    Provides comprehensive gRPC configuration for:
    - Server lifecycle and threading
    - Client connection management
    - Streaming operations
    - Security and TLS
    - Monitoring and observability
    - Service discovery
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_GRPC_",
        case_sensitive=False,
        extra="allow",  # Allow extra fields for flexibility
        validate_assignment=True,
        str_strip_whitespace=True,
        json_schema_serialization_defaults_required=True,
        json_schema_extra={
            "title": "FLEXT gRPC Advanced Configuration",
            "description": "Enterprise gRPC service configuration with FlextConfig integration",
            "examples": [
                {
                    "host": "localhost",
                    "port": 50051,
                    "environment": "development",
                    "security": {"tls_enabled": False},
                    "performance": {"max_workers": 10}
                }
            ]
        },
    )

    # === CORE SERVER CONFIGURATION ===
    host: str = Field(
        default=FlextGrpcModels.ServerConfig.model_fields["host"].default,
        description="gRPC server bind host",
        examples=["localhost", "127.0.0.1", "grpc.example.com"]
    )
    port: int = Field(
        default=FlextGrpcModels.ServerConfig.model_fields["port"].default,
        description="gRPC server bind port",
        ge=FlextConstants.Network.MIN_PORT,
        le=FlextConstants.Network.MAX_PORT,
        examples=[50051, 8080, 443]
    )
    environment: str = Field(
        default="development",
        description="Deployment environment",
        examples=["development", "production"]
    )

    # === SERVER LIFECYCLE CONFIGURATION ===
    max_workers: int = Field(
        default=FlextGrpcModels.ServerConfig.model_fields["max_workers"].default,
        description="Maximum worker threads for request processing",
        ge=FlextGrpcConstants.MIN_WORKERS,
        le=FlextGrpcConstants.MAX_WORKERS,
        examples=[4, 10, 50]
    )
    max_concurrent_rpcs: int = Field(
        default=FlextGrpcConstants.DEFAULT_MAX_CONCURRENT_RPCS,
        description="Maximum concurrent RPC calls",
        ge=1,
        le=10000,
        examples=[100, 1000, 5000]
    )
    server_shutdown_timeout: float = Field(
        default=30.0,
        description="Graceful shutdown timeout in seconds",
        gt=0,
        le=300,
        examples=[30.0, 60.0, 120.0]
    )

    # === CLIENT CONFIGURATION ===
    client_timeout: float = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
        description="Default client request timeout",
        gt=0,
        le=300,
        examples=[30.0, 60.0, 120.0]
    )
    client_keepalive_time: float = Field(
        default=30.0,
        description="Client keepalive ping interval",
        gt=0,
        examples=[30.0, 60.0]
    )
    client_keepalive_timeout: float = Field(
        default=5.0,
        description="Client keepalive timeout",
        gt=0,
        examples=[5.0, 10.0]
    )
    client_max_connection_age: float = Field(
        default=300.0,
        description="Maximum connection age before recreation",
        gt=0,
        examples=[300.0, 600.0]
    )

    # === MESSAGE SIZE LIMITS ===
    max_receive_message_length: int = Field(
        default=4 * 1024 * 1024,  # 4MB
        description="Maximum receive message size in bytes",
        ge=1024,
        le=100 * 1024 * 1024,  # 100MB
        examples=[4194304, 10485760, 52428800]
    )
    max_send_message_length: int = Field(
        default=4 * 1024 * 1024,  # 4MB
        description="Maximum send message size in bytes",
        ge=1024,
        le=100 * 1024 * 1024,  # 100MB
        examples=[4194304, 10485760, 52428800]
    )

    # === STREAMING CONFIGURATION ===
    streaming_enabled: bool = Field(
        default=True,
        description="Enable streaming operations",
        examples=[True, False]
    )
    max_concurrent_streams: int = Field(
        default=100,
        description="Maximum concurrent streams per connection",
        ge=1,
        le=1000,
        examples=[10, 50, 100]
    )
    stream_timeout: float = Field(
        default=300.0,
        description="Default stream operation timeout",
        gt=0,
        examples=[300.0, 600.0]
    )

    # === SECURITY CONFIGURATION ===
    tls_enabled: bool = Field(
        default=False,
        description="Enable TLS/SSL encryption",
        examples=[False, True]
    )
    tls_cert_file: str | None = Field(
        default=None,
        description="Path to TLS certificate file",
        examples=["/path/to/cert.pem"]
    )
    tls_key_file: str | None = Field(
        default=None,
        description="Path to TLS private key file",
        examples=["/path/to/key.pem"]
    )
    tls_ca_file: str | None = Field(
        default=None,
        description="Path to TLS CA certificate file",
        examples=["/path/to/ca.pem"]
    )
    auth_enabled: bool = Field(
        default=False,
        description="Enable authentication",
        examples=[False, True]
    )
    auth_token: str | None = Field(
        default=None,
        description="Authentication token",
        examples=["your-secret-token"]
    )

    # === MONITORING CONFIGURATION ===
    metrics_enabled: bool = Field(
        default=True,
        description="Enable metrics collection",
        examples=[True, False]
    )
    metrics_interval: float = Field(
        default=60.0,
        description="Metrics collection interval",
        gt=0,
        examples=[30.0, 60.0, 300.0]
    )
    tracing_enabled: bool = Field(
        default=False,
        description="Enable distributed tracing",
        examples=[False, True]
    )
    health_check_enabled: bool = Field(
        default=True,
        description="Enable health check endpoint",
        examples=[True, False]
    )
    health_check_interval: float = Field(
        default=30.0,
        description="Health check interval",
        gt=0,
        examples=[30.0, 60.0]
    )

    # === SERVICE DISCOVERY ===
    service_discovery_enabled: bool = Field(
        default=False,
        description="Enable service discovery",
        examples=[False, True]
    )
    service_registry_type: Literal["consul", "etcd", "zookeeper", "dns"] | None = Field(
        default=None,
        description="Service registry type",
        examples=["consul", "etcd"]
    )
    service_registry_host: str | None = Field(
        default=None,
        description="Service registry host",
        examples=["localhost", "consul.example.com"]
    )
    service_registry_port: int | None = Field(
        default=None,
        description="Service registry port",
        examples=[8500, 2379]
    )

    # === LOAD BALANCING ===
    load_balancing_policy: Literal["round_robin", "least_requests", "ring_hash"] = Field(
        default="round_robin",
        description="Load balancing policy",
        examples=["round_robin", "least_requests"]
    )
    max_connection_pool_size: int = Field(
        default=10,
        description="Maximum connection pool size",
        ge=1,
        le=100,
        examples=[5, 10, 20]
    )

    # === ADVANCED FEATURES ===
    compression_enabled: bool = Field(
        default=True,
        description="Enable message compression",
        examples=[True, False]
    )
    compression_algorithm: Literal["gzip", "deflate", "none"] = Field(
        default="gzip",
        description="Compression algorithm",
        examples=["gzip", "deflate"]
    )
    interceptors_enabled: bool = Field(
        default=True,
        description="Enable gRPC interceptors",
        examples=[True, False]
    )

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host using FlextGrpcModels.ServerConfig as source."""
        try:
            FlextGrpcModels.ServerConfig(host=v, port=50051, max_workers=10, timeout=30.0)
            return v.strip()
        except Exception as e:
            msg = f"Invalid host: {e}"
            raise ValueError(msg) from e

    @field_validator("port")
    @classmethod
    def validate_port(cls, v: int) -> int:
        """Validate port using FlextGrpcModels.ServerConfig as source."""
        try:
            FlextGrpcModels.ServerConfig(host="localhost", port=v, max_workers=10, timeout=30.0)
            return v
        except Exception as e:
            msg = f"Invalid port: {e}"
            raise ValueError(msg) from e

    @field_validator("max_workers")
    @classmethod
    def validate_max_workers(cls, v: int) -> int:
        """Validate max workers using FlextGrpcModels.ServerConfig as source."""
        try:
            FlextGrpcModels.ServerConfig(host="localhost", port=50051, max_workers=v, timeout=30.0)
            return v
        except Exception as e:
            msg = f"Invalid max_workers: {e}"
            raise ValueError(msg) from e

    @field_validator("tls_cert_file", "tls_key_file", "tls_ca_file")
    @classmethod
    def validate_tls_files(cls, v: str | None) -> str | None:
        """Validate TLS file paths exist when TLS is enabled."""
        if v is not None and not Path(v).exists():
            msg = f"TLS file does not exist: {v}"
            raise ValueError(msg)
        return v

    @model_validator(mode="after")
    def validate_tls_configuration(self) -> FlextGrpcConfig:
        """Validate TLS configuration consistency."""
        if self.tls_enabled and (not self.tls_cert_file or not self.tls_key_file):
            msg = "TLS certificate and key files required when TLS is enabled"
            raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_service_discovery_config(self) -> FlextGrpcConfig:
        """Validate service discovery configuration."""
        if self.service_discovery_enabled:
            if not self.service_registry_type:
                msg = "Service registry type required when service discovery is enabled"
                raise ValueError(msg)
            if not self.service_registry_host or self.service_registry_port is None:
                msg = "Service registry host and port required when service discovery is enabled"
                raise ValueError(msg)
        return self

    @model_validator(mode="after")
    def validate_environment_specific_defaults(self) -> FlextGrpcConfig:
        """Apply environment-specific configuration defaults."""
        if self.environment == "production":
            # Stricter defaults for production
            if self.tls_enabled is False:
                self.tls_enabled = True  # Force TLS in production
            if self.metrics_enabled is False:
                self.metrics_enabled = True  # Force metrics in production
            if self.health_check_enabled is False:
                self.health_check_enabled = True  # Force health checks in production
        elif self.environment == "development":
            # Relaxed defaults for development
            self.client_timeout = min(self.client_timeout, 60.0)  # Shorter timeouts for faster feedback
        return self

    def get_server_address(self) -> str:
        """Get the full server address as host:port."""
        return f"{self.host}:{self.port}"

    def get_client_config(self) -> dict[str, Any]:
        """Get client-specific configuration subset."""
        return {
            "timeout": self.client_timeout,
            "keepalive_time": self.client_keepalive_time,
            "keepalive_timeout": self.client_keepalive_timeout,
            "max_connection_age": self.client_max_connection_age,
            "tls_enabled": self.tls_enabled,
            "tls_ca_file": self.tls_ca_file,
            "auth_enabled": self.auth_enabled,
            "auth_token": self.auth_token,
            "compression_enabled": self.compression_enabled,
            "compression_algorithm": self.compression_algorithm,
        }

    def get_server_config(self) -> dict[str, Any]:
        """Get server-specific configuration subset."""
        return {
            "host": self.host,
            "port": self.port,
            "max_workers": self.max_workers,
            "max_concurrent_rpcs": self.max_concurrent_rpcs,
            "server_shutdown_timeout": self.server_shutdown_timeout,
            "max_receive_message_length": self.max_receive_message_length,
            "max_send_message_length": self.max_send_message_length,
            "tls_enabled": self.tls_enabled,
            "tls_cert_file": self.tls_cert_file,
            "tls_key_file": self.tls_key_file,
            "auth_enabled": self.auth_enabled,
            "auth_token": self.auth_token,
            "metrics_enabled": self.metrics_enabled,
            "metrics_interval": self.metrics_interval,
            "health_check_enabled": self.health_check_enabled,
            "health_check_interval": self.health_check_interval,
            "compression_enabled": self.compression_enabled,
            "interceptors_enabled": self.interceptors_enabled,
        }

    def get_streaming_config(self) -> dict[str, Any]:
        """Get streaming-specific configuration subset."""
        return {
            "streaming_enabled": self.streaming_enabled,
            "max_concurrent_streams": self.max_concurrent_streams,
            "stream_timeout": self.stream_timeout,
        }

    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == "production"

    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == "development"

    def get_environment_config(self) -> dict[str, Any]:
        """Get environment-specific configuration."""
        base_config = {
            "environment": self.environment,
            "is_production": self.is_production(),
            "is_development": self.is_development(),
        }

        if self.is_production():
            base_config.update({
                "log_level": "WARNING",
                "debug_mode": False,
                "performance_monitoring": True,
            })
        else:
            base_config.update({
                "log_level": "DEBUG",
                "debug_mode": True,
                "performance_monitoring": False,
            })

        return base_config

    @classmethod
    def create_from_env(cls, **overrides: Any) -> FlextGrpcConfig:
        """Create configuration instance with environment variable loading and overrides.

        Uses FlextConfig's advanced loading capabilities:
        - Environment variables with FLEXT_GRPC_ prefix
        - Configuration files (.env, config.json, etc.)
        - Runtime overrides
        """
        return cls(**overrides)

    @classmethod
    def create_for_environment(
        cls,
        environment: str,
        **overrides: Any
    ) -> FlextGrpcConfig:
        """Create configuration optimized for specific environment."""
        config_overrides: dict[str, Any] = {"environment": environment}

        # Environment-specific defaults
        if environment == "production":
            config_overrides.update({
                "tls_enabled": True,
                "metrics_enabled": True,
                "health_check_enabled": True,
                "max_workers": 20,  # Higher for production
                "max_concurrent_rpcs": 1000,
            })
        elif environment == "development":
            config_overrides.update({
                "tls_enabled": False,
                "metrics_enabled": False,
                "max_workers": 4,  # Lower for development
                "client_timeout": 30.0,
            })

        config_overrides.update(overrides)
        return cls(**config_overrides)

    def to_dict(self) -> dict[str, Any]:
        """Convert configuration to dictionary for serialization."""
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> FlextGrpcConfig:
        """Create configuration from dictionary."""
        return cls(**data)

    def validate_configuration(self) -> FlextResult[FlextGrpcConfig]:
        """Validate the complete configuration for consistency and requirements."""
        try:
            # Re-validate the model to ensure all constraints are met
            validated_config = self.model_validate(self.model_dump())
            return FlextResult.ok(validated_config)
        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    def get_connection_string(self) -> str:
        """Get gRPC connection string for clients."""
        scheme = "grpcs" if self.tls_enabled else "grpc"
        return f"{scheme}://{self.host}:{self.port}"

    def to_server_config(self) -> FlextGrpcModels.ServerConfig:
        """Convert to FlextGrpcModels.ServerConfig (source of truth)."""
        return FlextGrpcModels.ServerConfig(
            host=self.host,
            port=self.port,
            max_workers=self.max_workers,
            timeout=self.client_timeout,
        )

    @classmethod
    def from_server_config(
        cls,
        server_config: FlextGrpcModels.ServerConfig,
        **overrides: Any
    ) -> FlextGrpcConfig:
        """Create from FlextGrpcModels.ServerConfig (source of truth)."""
        data = server_config.model_dump()
        data.update(overrides)
        return cls(**data)

    def validate_with_models(self) -> FlextResult[FlextGrpcConfig]:
        """Validate using FlextGrpcModels as source of truth."""
        try:
            # Validate server config first (source of truth)
            server_config = self.to_server_config()
            validated_server = server_config.model_validate(server_config.model_dump())

            # Update with validated server config
            validated_data = self.model_dump()
            validated_data.update({
                "host": validated_server.host,
                "port": validated_server.port,
                "max_workers": validated_server.max_workers,
                "client_timeout": validated_server.timeout,
            })

            # Validate full config
            validated_config = self.model_validate(validated_data)
            return FlextResult.ok(validated_config)

        except Exception as e:
            return FlextResult.fail(f"Model-based validation failed: {e}")


__all__ = [
    "FlextGrpcConfig",
]
