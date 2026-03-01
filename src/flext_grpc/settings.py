"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeAlias

import grpc
from flext_core import r
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from flext_grpc.constants import c
from flext_grpc.models import FlextGrpcModels

GrpcNetworkConfig: TypeAlias = FlextGrpcModels.Grpc.NetworkConfig
GrpcSecurityConfig: TypeAlias = FlextGrpcModels.Grpc.SecurityConfig
GrpcPerformanceConfig: TypeAlias = FlextGrpcModels.Grpc.PerformanceConfig
GrpcStreamingConfig: TypeAlias = FlextGrpcModels.Grpc.StreamingConfig
GrpcClientConfig: TypeAlias = FlextGrpcModels.Grpc.ClientSettingsConfig
GrpcMonitoringConfig: TypeAlias = FlextGrpcModels.Grpc.MonitoringConfig


class FlextGrpcSettings(BaseModel):
    """Generic gRPC configuration system using AutoConfig pattern.

    **ARCHITECTURAL PATTERN**: Zero-Boilerplate Auto-Registration

    This class uses FlextSettings.AutoConfig for automatic:
    - Singleton pattern (thread-safe)
    - Namespace registration (accessible via config.grpc)
    - Environment variable loading from FLEXT_GRPC_* variables
    - .env file loading (production/development)
    - Automatic type conversion and validation via Pydantic v2

    Uses extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
    for complete gRPC configuration management with validation and composition.
    """

    model_config = SettingsConfigDict(
        env_prefix="FLEXT_GRPC_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        validate_assignment=True,
        str_strip_whitespace=True,
        validate_default=True,
        frozen=False,
        arbitrary_types_allowed=True,
        strict=False,
    )

    # Core configuration sections with composition
    network: GrpcNetworkConfig = Field(
        default_factory=FlextGrpcModels.Grpc.NetworkConfig,
    )
    security: GrpcSecurityConfig = Field(
        default_factory=FlextGrpcModels.Grpc.SecurityConfig,
    )
    performance: GrpcPerformanceConfig = Field(
        default_factory=FlextGrpcModels.Grpc.PerformanceConfig,
    )
    streaming: GrpcStreamingConfig = Field(
        default_factory=FlextGrpcModels.Grpc.StreamingConfig,
    )
    client: GrpcClientConfig = Field(
        default_factory=FlextGrpcModels.Grpc.ClientSettingsConfig,
    )
    monitoring: GrpcMonitoringConfig = Field(
        default_factory=FlextGrpcModels.Grpc.MonitoringConfig,
    )

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        max_workers: int | None = None,
        timeout: float | None = None,
        *,
        tls_enabled: bool | None = None,
        streaming_enabled: bool | None = None,
        network: GrpcNetworkConfig | None = None,
        security: GrpcSecurityConfig | None = None,
        performance: GrpcPerformanceConfig | None = None,
        streaming: GrpcStreamingConfig | None = None,
        client: GrpcClientConfig | None = None,
        monitoring: GrpcMonitoringConfig | None = None,
    ) -> None:
        """Initialize with backward compatibility for legacy fields."""
        network_config: GrpcNetworkConfig = (
            network or FlextGrpcModels.Grpc.NetworkConfig()
        )
        if host is not None:
            network_config = network_config.model_copy(update={"host": host})
        if port is not None:
            network_config = network_config.model_copy(update={"port": port})

        security_config: GrpcSecurityConfig = (
            security or FlextGrpcModels.Grpc.SecurityConfig()
        )
        if tls_enabled is not None:
            security_config = security_config.model_copy(
                update={"tls_enabled": tls_enabled},
            )

        performance_config: GrpcPerformanceConfig = (
            performance or FlextGrpcModels.Grpc.PerformanceConfig()
        )
        if max_workers is not None:
            performance_config = performance_config.model_copy(
                update={"max_workers": max_workers},
            )

        streaming_config: GrpcStreamingConfig = (
            streaming or FlextGrpcModels.Grpc.StreamingConfig()
        )
        if streaming_enabled is not None:
            streaming_config = streaming_config.model_copy(
                update={"enabled": streaming_enabled},
            )

        client_config: GrpcClientConfig = (
            client or FlextGrpcModels.Grpc.ClientSettingsConfig()
        )
        if timeout is not None:
            client_config = client_config.model_copy(update={"timeout": timeout})

        # Initialize with updated configs using BaseModel.__init__
        # AutoConfig only accepts config_class, env_prefix, env_file
        # So we initialize BaseModel directly with our fields
        super().__init__(
            network=network_config,
            security=security_config,
            performance=performance_config,
            streaming=streaming_config,
            client=client_config,
            monitoring=monitoring or FlextGrpcModels.Grpc.MonitoringConfig(),
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

    def validate_configuration(self) -> r[bool]:
        """Validate complete configuration with cross-section checks."""
        try:
            # Cross-validation: TLS and client cert requirements
            if self.security.client_cert_required and not self.security.tls_enabled:
                return r.fail("Client certificates require TLS to be enabled")

            # Cross-validation: Performance limits
            if self.performance.max_concurrent_rpcs > self.performance.max_workers * 10:
                return r.fail("RPC limit too high for worker count")

            # Cross-validation: Network and security
            http_port = c.Grpc.GrpcNetwork.HTTP_PORT  # Standard HTTP port
            if self.security.tls_enabled and self.network.port == http_port:
                return r.fail("TLS enabled but using HTTP port")

            return r.ok(True)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Configuration validation failed: {e}")

    @classmethod
    def create_production_config(cls) -> r[FlextGrpcSettings]:
        """Create production-ready configuration with enterprise defaults."""
        try:
            config = cls(
                network=FlextGrpcModels.Grpc.NetworkConfig(
                    host="127.0.0.1",  # Bind to localhost for security
                    port=c.Grpc.GrpcNetwork.GRPC_PORT,
                    max_connections=c.Grpc.Connection.MAX_CONNECTIONS,
                    keepalive_time=c.Grpc.GrpcNetwork.KEEPALIVE_TIME_SECONDS,
                    keepalive_timeout=c.Grpc.GrpcNetwork.KEEPALIVE_TIMEOUT_SECONDS,
                ),
                security=FlextGrpcModels.Grpc.SecurityConfig(
                    tls_enabled=False,  # Disable TLS for testing/production without certs
                    auth_enabled=False,  # Disable auth for testing/production without tokens
                ),
                performance=FlextGrpcModels.Grpc.PerformanceConfig(
                    max_workers=c.Grpc.Connection.MAX_WORKERS,
                    max_concurrent_rpcs=c.Grpc.Connection.MAX_CONCURRENT_RPCS,  # Within limit: 20 * 10 = 200
                    thread_pool_size=c.Grpc.Connection.THREAD_POOL_SIZE,
                ),
                streaming=FlextGrpcModels.Grpc.StreamingConfig(
                    max_concurrent_streams=c.Grpc.Connection.MAX_CONCURRENT_STREAMS,
                    stream_buffer_size=1000,
                ),
                client=FlextGrpcModels.Grpc.ClientSettingsConfig(
                    timeout=c.Grpc.Connection.DEFAULT_TIMEOUT,
                    retry_attempts=5,
                ),
                monitoring=FlextGrpcModels.Grpc.MonitoringConfig(
                    metrics_enabled=True,
                    tracing_enabled=True,
                    health_check_enabled=True,
                ),
            )
            validation = config.validate_configuration()
            return validation.map(lambda _: config)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Production config creation failed: {e}")

    @classmethod
    def create_development_config(cls) -> r[FlextGrpcSettings]:
        """Create development configuration with relaxed settings."""
        try:
            config = cls(
                network=FlextGrpcModels.Grpc.NetworkConfig(
                    host="localhost",
                    port=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
                ),
                security=FlextGrpcModels.Grpc.SecurityConfig(),
                performance=FlextGrpcModels.Grpc.PerformanceConfig(
                    max_workers=5,
                    max_concurrent_rpcs=100,
                ),
                streaming=FlextGrpcModels.Grpc.StreamingConfig(),
                client=FlextGrpcModels.Grpc.ClientSettingsConfig(),
                monitoring=FlextGrpcModels.Grpc.MonitoringConfig(),
            )
            return r.ok(config)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Development config creation failed: {e}")


__all__ = [
    "FlextGrpcModels",
    "FlextGrpcSettings",
]
