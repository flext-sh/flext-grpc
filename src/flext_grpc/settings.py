"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeAlias

from flext_core import FlextSettings, r
from pydantic import Field, computed_field

from flext_grpc import c
from flext_grpc.models import FlextGrpcModels

GrpcNetworkConfig: TypeAlias = FlextGrpcModels.Grpc.NetworkConfig
GrpcSecurityConfig: TypeAlias = FlextGrpcModels.Grpc.SecurityConfig
GrpcPerformanceConfig: TypeAlias = FlextGrpcModels.Grpc.PerformanceConfig
GrpcStreamingConfig: TypeAlias = FlextGrpcModels.Grpc.StreamingConfig
GrpcClientConfig: TypeAlias = FlextGrpcModels.Grpc.ClientSettingsConfig
GrpcMonitoringConfig: TypeAlias = FlextGrpcModels.Grpc.MonitoringConfig


class FlextGrpcSettings(FlextSettings):
    """gRPC runtime settings with flat convenience fields and nested configurations.

    Provides both flat fields for simple configuration and nested config models
    for advanced settings. Flat fields are convenience accessors that sync with
    nested configurations.
    """

    # Flat convenience fields (settable via constructor)
    host: str = Field(
        default=c.Grpc.GrpcNetwork.DEFAULT_HOST, validation_alias="grpc_host"
    )
    port: int = Field(
        default=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        ge=1,
        le=65535,
        validation_alias="grpc_port",
    )
    max_workers: int = Field(
        default=c.Grpc.Service.MAX_WORKERS,
        ge=1,
        le=100,
        validation_alias="grpc_max_workers",
    )
    timeout: float = Field(
        default=c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT,
        gt=0,
        validation_alias="grpc_timeout",
    )

    # Nested configuration models
    network: GrpcNetworkConfig = Field(default_factory=GrpcNetworkConfig)
    security: GrpcSecurityConfig = Field(default_factory=GrpcSecurityConfig)
    performance: GrpcPerformanceConfig = Field(default_factory=GrpcPerformanceConfig)
    streaming: GrpcStreamingConfig = Field(default_factory=GrpcStreamingConfig)
    client: GrpcClientConfig = Field(default_factory=GrpcClientConfig)
    monitoring: GrpcMonitoringConfig = Field(default_factory=GrpcMonitoringConfig)

    @computed_field
    @property
    def tls_enabled(self) -> bool:
        """Computed property indicating if TLS is enabled."""
        return self.security.tls_enabled

    @computed_field
    @property
    def streaming_enabled(self) -> bool:
        """Computed property indicating if streaming is enabled."""
        return self.streaming.enabled

    def validate_configuration(self) -> r[bool]:
        """Validate configuration consistency.

        Checks that security configuration is valid, particularly that
        client certificates are not required without TLS enabled.

        Returns:
            r[bool]: Success if configuration is valid, failure with error message otherwise.

        """
        if not self.security.tls_enabled and self.security.client_cert_required:
            return r[bool].fail("Client certificates require TLS to be enabled")
        return r[bool].ok(True)

    @classmethod
    def create_production_config(cls) -> r[FlextGrpcSettings]:
        """Create a production-ready gRPC configuration.

        Production configuration enables TLS and uses secure defaults.

        Returns:
            r[FlextGrpcSettings]: Production configuration instance.

        """
        return r[FlextGrpcSettings].ok(
            cls.model_validate({
                "host": "0.0.0.0",  # noqa: S104 - Production servers require binding to all interfaces (0.0.0.0) for Kubernetes/container deployments. TLS is enabled to mitigate security risk. See https://kubernetes.io/docs/concepts/services-networking/service/#type-loadbalancer
                "security": {"tls_enabled": True},
            })
        )

    @classmethod
    def create_development_config(cls) -> r[FlextGrpcSettings]:
        """Create a development gRPC configuration.

        Development configuration uses localhost and insecure defaults
        for ease of testing.

        Returns:
            r[FlextGrpcSettings]: Development configuration instance.

        """
        return r[FlextGrpcSettings].ok(cls.model_validate({"host": "127.0.0.1"}))


__all__ = ["FlextGrpcModels", "FlextGrpcSettings"]
