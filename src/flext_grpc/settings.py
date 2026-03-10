"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeAlias

from flext_core import FlextSettings

from flext_grpc.models import FlextGrpcModels

GrpcNetworkConfig: TypeAlias = FlextGrpcModels.Grpc.NetworkConfig
GrpcSecurityConfig: TypeAlias = FlextGrpcModels.Grpc.SecurityConfig
GrpcPerformanceConfig: TypeAlias = FlextGrpcModels.Grpc.PerformanceConfig
GrpcStreamingConfig: TypeAlias = FlextGrpcModels.Grpc.StreamingConfig
GrpcClientConfig: TypeAlias = FlextGrpcModels.Grpc.ClientSettingsConfig
GrpcMonitoringConfig: TypeAlias = FlextGrpcModels.Grpc.MonitoringConfig


class FlextGrpcSettings(FlextSettings):
    """gRPC runtime settings."""

    network: GrpcNetworkConfig = GrpcNetworkConfig()
    security: GrpcSecurityConfig = GrpcSecurityConfig()
    performance: GrpcPerformanceConfig = GrpcPerformanceConfig()
    streaming: GrpcStreamingConfig = GrpcStreamingConfig()
    client: GrpcClientConfig = GrpcClientConfig()
    monitoring: GrpcMonitoringConfig = GrpcMonitoringConfig()


__all__ = ["FlextGrpcModels", "FlextGrpcSettings"]
