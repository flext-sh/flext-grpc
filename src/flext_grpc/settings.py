"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Annotated

from flext_core import FlextSettings, r
from pydantic import Field, computed_field

from flext_grpc import c
from flext_grpc.models import FlextGrpcModels


class FlextGrpcSettings(FlextSettings):
    """gRPC runtime settings with flat convenience fields and nested configurations.

    Provides both flat fields for simple configuration and nested config models
    for advanced settings. Flat fields are convenience accessors that sync with
    nested configurations.
    """

    # Flat convenience fields (settable via constructor)
    host: Annotated[
        str,
        Field(default=c.Grpc.GrpcNetwork.DEFAULT_HOST, validation_alias="grpc_host"),
    ]
    port: Annotated[
        int,
        Field(
            default=c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
            ge=1,
            le=65535,
            validation_alias="grpc_port",
        ),
    ]
    max_workers: Annotated[
        int,
        Field(
            default=c.Grpc.Service.MAX_WORKERS,
            ge=1,
            le=100,
            validation_alias="grpc_max_workers",
        ),
    ]
    timeout: Annotated[
        float,
        Field(
            default=c.Grpc.GrpcNetwork.DEFAULT_TIMEOUT,
            gt=0,
            validation_alias="grpc_timeout",
        ),
    ]

    # Nested configuration models
    network: Annotated[GrpcNetworkConfig, Field(default_factory=GrpcNetworkConfig)]
    security: Annotated[GrpcSecurityConfig, Field(default_factory=GrpcSecurityConfig)]
    performance: Annotated[
        GrpcPerformanceConfig, Field(default_factory=GrpcPerformanceConfig)
    ]
    streaming: Annotated[
        GrpcStreamingConfig, Field(default_factory=GrpcStreamingConfig)
    ]
    client: Annotated[GrpcClientConfig, Field(default_factory=GrpcClientConfig)]
    monitoring: Annotated[
        GrpcMonitoringConfig, Field(default_factory=GrpcMonitoringConfig)
    ]

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
                "host": c.Grpc.GrpcNetwork.DEFAULT_HOST,
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
