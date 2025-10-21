"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re

from flext_core import FlextConstants, FlextResult
from pydantic import BaseModel, Field, field_validator, model_validator

from flext_grpc.constants import FlextGrpcConstants


class GrpcSecurityConfig(BaseModel):
    """Generic gRPC security configuration with validation."""

    tls_enabled: bool = Field(default=False, description="Enable TLS encryption")
    tls_cert_file: str | None = Field(
        default=None, description="TLS certificate file path"
    )
    tls_key_file: str | None = Field(
        default=None, description="TLS private key file path"
    )
    tls_ca_file: str | None = Field(
        default=None, description="TLS CA certificate file path"
    )
    auth_enabled: bool = Field(default=False, description="Enable authentication")
    auth_token: str | None = Field(default=None, description="Authentication token")
    client_cert_required: bool = Field(
        default=False, description="Require client certificates"
    )

    @model_validator(mode="after")
    def validate_security_config(self) -> GrpcSecurityConfig:
        """Validate security configuration consistency."""
        if self.tls_enabled and not self.tls_cert_file:
            msg = "TLS certificate required when TLS is enabled"
            raise ValueError(msg)
        if self.auth_enabled and not self.auth_token:
            msg = "Auth token required when authentication is enabled"
            raise ValueError(msg)
        return self


class GrpcNetworkConfig(BaseModel):
    """Generic gRPC network configuration with validation."""

    host: str = Field(
        default=FlextConstants.Platform.DEFAULT_HOST,
        min_length=1,
        description="gRPC server host",
    )
    port: int = Field(
        default=FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT,
        ge=1,
        le=65535,
        description="gRPC server port",
    )
    max_connections: int = Field(
        default=1000, ge=1, le=10000, description="Maximum concurrent connections"
    )
    keepalive_time: int = Field(
        default=30, ge=1, description="Keepalive ping interval (seconds)"
    )
    keepalive_timeout: int = Field(
        default=5, ge=1, description="Keepalive timeout (seconds)"
    )

    @field_validator("host")
    @classmethod
    def validate_host(cls, v: str) -> str:
        """Validate host format."""
        if not v.strip():
            msg = "Host cannot be empty"
            raise ValueError(msg)
        # Allow localhost, IP addresses, and domain names
        if not re.match(r"^(localhost|[\w.-]+|\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})$", v):
            msg = "Invalid host format"
            raise ValueError(msg)
        return v.strip()


class GrpcPerformanceConfig(BaseModel):
    """Generic gRPC performance configuration."""

    max_workers: int = Field(
        default=FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS,
        ge=1,
        le=1000,
        description="Maximum worker threads",
    )
    max_concurrent_rpcs: int = Field(
        default=1000, ge=1, le=10000, description="Maximum concurrent RPCs"
    )
    max_receive_message_length: int = Field(
        default=4 * 1024 * 1024,  # 4MB
        ge=1024,
        le=100 * 1024 * 1024,  # 100MB
        description="Maximum receive message length (bytes)",
    )
    max_send_message_length: int = Field(
        default=4 * 1024 * 1024,  # 4MB
        ge=1024,
        le=100 * 1024 * 1024,  # 100MB
        description="Maximum send message length (bytes)",
    )
    thread_pool_size: int = Field(
        default=50, ge=1, le=200, description="Thread pool size"
    )


class GrpcStreamingConfig(BaseModel):
    """Generic gRPC streaming configuration."""

    enabled: bool = Field(default=True, description="Enable streaming operations")
    max_concurrent_streams: int = Field(
        default=10, ge=1, le=100, description="Maximum concurrent streams"
    )
    stream_buffer_size: int = Field(
        default=500, ge=10, le=10000, description="Stream buffer size"
    )
    max_stream_duration: int = Field(
        default=300,  # 5 minutes
        ge=10,
        le=3600,  # 1 hour
        description="Maximum stream duration (seconds)",
    )
    enable_compression: bool = Field(
        default=True, description="Enable message compression"
    )


class GrpcClientConfig(BaseModel):
    """Generic gRPC client configuration."""

    timeout: float = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
        gt=0,
        le=300,
        description="RPC timeout (seconds)",
    )
    retry_attempts: int = Field(
        default=3, ge=0, le=10, description="Maximum retry attempts"
    )
    retry_backoff: float = Field(
        default=1.0, gt=0, le=60, description="Retry backoff multiplier"
    )
    load_balancing_policy: str = Field(
        default="round_robin", description="Load balancing policy"
    )
    channel_options: dict[str, str | int] = Field(
        default_factory=dict, description="Additional channel options"
    )


class GrpcMonitoringConfig(BaseModel):
    """Generic gRPC monitoring and observability configuration."""

    metrics_enabled: bool = Field(default=True, description="Enable metrics collection")
    tracing_enabled: bool = Field(
        default=False, description="Enable distributed tracing"
    )
    health_check_enabled: bool = Field(default=True, description="Enable health checks")
    health_check_interval: int = Field(
        default=30, ge=5, le=300, description="Health check interval (seconds)"
    )
    log_level: str = Field(default="INFO", description="Logging level")


class FlextGrpcConfig(BaseModel):
    """Generic gRPC configuration system extending FlextConfig.

    Uses extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
    for complete gRPC configuration management with validation and composition.
    """

    # Core configuration sections with composition
    network: GrpcNetworkConfig = Field(default_factory=GrpcNetworkConfig)
    security: GrpcSecurityConfig = Field(default_factory=GrpcSecurityConfig)
    performance: GrpcPerformanceConfig = Field(default_factory=GrpcPerformanceConfig)
    streaming: GrpcStreamingConfig = Field(default_factory=GrpcStreamingConfig)
    client: GrpcClientConfig = Field(default_factory=GrpcClientConfig)
    monitoring: GrpcMonitoringConfig = Field(default_factory=GrpcMonitoringConfig)

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        max_workers: int | None = None,
        timeout: float | None = None,
        tls_enabled: bool | None = None,
        streaming_enabled: bool | None = None,
        network: GrpcNetworkConfig | None = None,
        security: GrpcSecurityConfig | None = None,
        performance: GrpcPerformanceConfig | None = None,
        streaming: GrpcStreamingConfig | None = None,
        client: GrpcClientConfig | None = None,
        monitoring: GrpcMonitoringConfig | None = None,
        **kwargs: object,
    ) -> None:
        """Initialize with backward compatibility for legacy fields."""
        # Handle legacy field overrides
        network = network or GrpcNetworkConfig()
        if host is not None:
            network = network.model_copy(update={"host": host})
        if port is not None:
            network = network.model_copy(update={"port": port})

        security = security or GrpcSecurityConfig()
        if tls_enabled is not None:
            security = security.model_copy(update={"tls_enabled": tls_enabled})

        performance = performance or GrpcPerformanceConfig()
        if max_workers is not None:
            performance = performance.model_copy(update={"max_workers": max_workers})

        streaming_config = streaming or GrpcStreamingConfig()
        if streaming_enabled is not None:
            streaming_config = streaming_config.model_copy(
                update={"enabled": streaming_enabled}
            )

        client_config = client or GrpcClientConfig()
        if timeout is not None:
            client_config = client_config.model_copy(update={"timeout": timeout})

        # Initialize with updated configs
        super().__init__(
            network=network,
            security=security,
            performance=performance,
            streaming=streaming_config,
            client=client_config,
            monitoring=monitoring or GrpcMonitoringConfig(),
            **kwargs,
        )

    @property
    def host(self) -> str:
        """Get host from network config."""
        return self.network.host

    @property
    def port(self) -> int:
        """Get port from network config."""
        return self.network.port

    @property
    def max_workers(self) -> int:
        """Get max workers from performance config."""
        return self.performance.max_workers

    @property
    def timeout(self) -> float:
        """Get timeout from client config."""
        return self.client.timeout

    @property
    def tls_enabled(self) -> bool:
        """Get TLS enabled from security config."""
        return self.security.tls_enabled

    @property
    def streaming_enabled(self) -> bool:
        """Get streaming enabled from streaming config."""
        return self.streaming.enabled

    def validate_configuration(self) -> FlextResult[None]:
        """Validate complete configuration with cross-section checks."""
        try:
            # Cross-validation: TLS and client cert requirements
            if self.security.client_cert_required and not self.security.tls_enabled:
                return FlextResult.fail("Client certificates require TLS to be enabled")

            # Cross-validation: Performance limits
            if self.performance.max_concurrent_rpcs > self.performance.max_workers * 10:
                return FlextResult.fail("RPC limit too high for worker count")

            # Cross-validation: Network and security
            http_port = 80  # Standard HTTP port
            if self.security.tls_enabled and self.network.port == http_port:
                return FlextResult.fail("TLS enabled but using HTTP port")

            return FlextResult.ok(None)
        except Exception as e:
            return FlextResult.fail(f"Configuration validation failed: {e}")

    @classmethod
    def create_production_config(cls) -> FlextResult[FlextGrpcConfig]:
        """Create production-ready configuration with enterprise defaults."""
        try:
            config = cls(
                network=GrpcNetworkConfig(
                    host="0.0.0.0",
                    port=50051,
                    max_connections=1000,
                    keepalive_time=30,
                    keepalive_timeout=5,
                ),
                security=GrpcSecurityConfig(
                    tls_enabled=True,
                    auth_enabled=True,
                ),
                performance=GrpcPerformanceConfig(
                    max_workers=20,
                    max_concurrent_rpcs=2000,
                    thread_pool_size=100,
                ),
                streaming=GrpcStreamingConfig(
                    max_concurrent_streams=50,
                    stream_buffer_size=1000,
                ),
                client=GrpcClientConfig(
                    timeout=30.0,
                    retry_attempts=5,
                ),
                monitoring=GrpcMonitoringConfig(
                    metrics_enabled=True,
                    tracing_enabled=True,
                    health_check_enabled=True,
                ),
            )
            validation = config.validate_configuration()
            return validation.map(lambda _: config)
        except Exception as e:
            return FlextResult.fail(f"Production config creation failed: {e}")

    @classmethod
    def create_development_config(cls) -> FlextResult[FlextGrpcConfig]:
        """Create development configuration with relaxed settings."""
        try:
            config = cls(
                network=GrpcNetworkConfig(
                    host="localhost",
                    port=50051,
                ),
                security=GrpcSecurityConfig(),
                performance=GrpcPerformanceConfig(
                    max_workers=5,
                    max_concurrent_rpcs=100,
                ),
                streaming=GrpcStreamingConfig(),
                client=GrpcClientConfig(),
                monitoring=GrpcMonitoringConfig(),
            )
            return FlextResult.ok(config)
        except Exception as e:
            return FlextResult.fail(f"Development config creation failed: {e}")


__all__ = [
    "FlextGrpcConfig",
    "GrpcClientConfig",
    "GrpcMonitoringConfig",
    "GrpcNetworkConfig",
    "GrpcPerformanceConfig",
    "GrpcSecurityConfig",
    "GrpcStreamingConfig",
]
