"""FLEXT gRPC Configuration - Generic Configuration System with Patterns.

Extensive Pydantic models, generic patterns, and FLEXT ecosystem integration
for complete gRPC configuration management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TypeAlias

from flext_grpc.models import FlextGrpcModels

GrpcNetworkConfig: TypeAlias = FlextGrpcModels.Grpc.NetworkConfig
GrpcSecurityConfig: TypeAlias = FlextGrpcModels.Grpc.SecurityConfig
GrpcPerformanceConfig: TypeAlias = FlextGrpcModels.Grpc.PerformanceConfig
GrpcStreamingConfig: TypeAlias = FlextGrpcModels.Grpc.StreamingConfig
GrpcClientConfig: TypeAlias = FlextGrpcModels.Grpc.ClientSettingsConfig
GrpcMonitoringConfig: TypeAlias = FlextGrpcModels.Grpc.MonitoringConfig
__all__ = ["FlextGrpcModels", "FlextGrpcSettings"]
