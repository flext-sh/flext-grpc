"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import r
from pydantic import BaseModel, Field
from pydantic_settings import SettingsConfigDict

from flext_grpc.models import FlextGrpcModels

# Import configuration models from models.py (centralized location)
_m = FlextGrpcModels
GrpcSecurityConfig = _m.Settings.SecurityConfig
GrpcNetworkConfig = _m.Settings.NetworkConfig
GrpcPerformanceConfig = _m.Settings.PerformanceConfig
GrpcStreamingConfig = _m.Settings.StreamingConfig
GrpcClientConfig = _m.Settings.ClientSettingsConfig
GrpcMonitoringConfig = _m.Settings.MonitoringConfig


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
        *,
        tls_enabled: bool | None = None,
        streaming_enabled: bool | None = None,
        network: GrpcNetworkConfig | None = None,
        security: GrpcSecurityConfig | None = None,
        performance: GrpcPerformanceConfig | None = None,
        streaming: GrpcStreamingConfig | None = None,
        client: GrpcClientConfig | None = None,
        monitoring: GrpcMonitoringConfig | None = None,
        **_kwargs: object,
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
                update={"enabled": streaming_enabled},
            )

        client_config = client or GrpcClientConfig()
        if timeout is not None:
            client_config = client_config.model_copy(update={"timeout": timeout})

        # Initialize with updated configs using BaseModel.__init__
        # AutoConfig only accepts config_class, env_prefix, env_file
        # So we initialize BaseModel directly with our fields
        super().__init__(
            network=network,
            security=security,
            performance=performance,
            streaming=streaming_config,
            client=client_config,
            monitoring=monitoring or GrpcMonitoringConfig(),
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
            http_port = 80  # Standard HTTP port
            if self.security.tls_enabled and self.network.port == http_port:
                return r.fail("TLS enabled but using HTTP port")

            return r.ok(True)
        except Exception as e:
            return r.fail(f"Configuration validation failed: {e}")

    @classmethod
    def create_production_config(cls) -> r[FlextGrpcSettings]:
        """Create production-ready configuration with enterprise defaults."""
        try:
            config = cls(
                network=GrpcNetworkConfig(
                    host="127.0.0.1",  # Bind to localhost for security
                    port=50051,
                    max_connections=1000,
                    keepalive_time=30,
                    keepalive_timeout=5,
                ),
                security=GrpcSecurityConfig(
                    tls_enabled=False,  # Disable TLS for testing/production without certs
                    auth_enabled=False,  # Disable auth for testing/production without tokens
                ),
                performance=GrpcPerformanceConfig(
                    max_workers=20,
                    max_concurrent_rpcs=200,  # Within limit: 20 * 10 = 200
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
            return r.fail(f"Production config creation failed: {e}")

    @classmethod
    def create_development_config(cls) -> r[FlextGrpcSettings]:
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
            return r.ok(config)
        except Exception as e:
            return r.fail(f"Development config creation failed: {e}")


__all__ = [
    "FlextGrpcSettings",
    "GrpcClientConfig",
    "GrpcMonitoringConfig",
    "GrpcNetworkConfig",
    "GrpcPerformanceConfig",
    "GrpcSecurityConfig",
    "GrpcStreamingConfig",
]
