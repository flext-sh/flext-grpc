"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated, ClassVar

from flext_core import FlextSettings, m, u
from flext_grpc import FlextGrpcModels, c, p, r, t


@FlextSettings.auto_register("grpc")
class FlextGrpcSettings(FlextSettings):
    """gRPC runtime settings with flat convenience fields and nested configurations.

    Provides both flat fields for simple configuration and nested settings models
    for advanced settings. Flat fields are convenience accessors that sync with
    nested configurations.
    """

    model_config: ClassVar[m.SettingsConfigDict] = m.SettingsConfigDict(
        env_prefix="FLEXT_GRPC_", extra="ignore"
    )

    # Flat convenience fields (settable via constructor)
    host: Annotated[
        str,
        u.Field(),
    ] = c.Grpc.GrpcNetwork.DEFAULT_HOST
    port: Annotated[
        t.PortNumber,
        u.Field(),
    ] = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
    max_workers: Annotated[
        t.WorkerCount,
        u.Field(),
    ] = c.Grpc.Service.MAX_WORKERS
    timeout: Annotated[
        t.PositiveTimeout,
        u.Field(),
    ] = c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT

    # Nested configuration models
    network: FlextGrpcModels.Grpc.NetworkConfig = u.Field(
        default_factory=lambda: FlextGrpcModels.Grpc.NetworkConfig.model_validate({})
    )
    security: FlextGrpcModels.Grpc.SecurityConfig = u.Field(
        default_factory=lambda: FlextGrpcModels.Grpc.SecurityConfig.model_validate({})
    )
    performance: FlextGrpcModels.Grpc.PerformanceConfig = u.Field(
        default_factory=lambda: (
            FlextGrpcModels.Grpc.PerformanceConfig.model_validate({})
        )
    )
    streaming: FlextGrpcModels.Grpc.StreamingConfig = u.Field(
        default_factory=lambda: FlextGrpcModels.Grpc.StreamingConfig.model_validate({})
    )
    client: FlextGrpcModels.Grpc.ClientConfig = u.Field(
        default_factory=lambda: FlextGrpcModels.Grpc.ClientConfig.model_validate({})
    )
    monitoring: FlextGrpcModels.Grpc.MonitoringConfig = u.Field(
        default_factory=lambda: FlextGrpcModels.Grpc.MonitoringConfig.model_validate({})
    )

    @u.computed_field()
    @property
    def tls_enabled(self) -> bool:
        """Computed property indicating if TLS is enabled."""
        return self.security.tls_enabled

    @u.computed_field()
    @property
    def streaming_enabled(self) -> bool:
        """Computed property indicating if streaming is enabled."""
        return self.streaming.enabled

    def validate_configuration(self) -> p.Result[bool]:
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
    def create_production_config(cls) -> p.Result[FlextGrpcSettings]:
        """Create a production-ready gRPC configuration.

        Production configuration enables TLS and uses secure defaults.

        Returns:
            r[FlextGrpcSettings]: Production configuration instance.

        """
        return r[FlextGrpcSettings].ok(
            cls.model_validate({
                "host": c.Grpc.GrpcNetwork.DEFAULT_HOST,
                "security": {"tls_enabled": True},
            }),
        )

    @classmethod
    def create_development_config(cls) -> p.Result[FlextGrpcSettings]:
        """Create a development gRPC configuration.

        Development configuration uses localhost and insecure defaults
        for ease of testing.

        Returns:
            r[FlextGrpcSettings]: Development configuration instance.

        """
        return r[FlextGrpcSettings].ok(cls.model_validate({"host": "127.0.0.1"}))


__all__: list[str] = ["FlextGrpcSettings"]
