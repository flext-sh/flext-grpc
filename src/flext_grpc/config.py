"""FLEXT gRPC Configuration - Advanced Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextConfig,
    FlextConstants,
)
from pydantic import Field

from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcConfig(FlextConfig):
    """gRPC configuration extending FlextConfig with gRPC-specific settings.

    Inherits ALL FlextConfig capabilities (configuration management, environment variables, etc.)
    and adds gRPC-specific configuration fields.
    """

    # gRPC Server Configuration
    host: str = Field(
        default=FlextConstants.Platform.DEFAULT_HOST, description="gRPC server host"
    )
    port: int = Field(
        default=FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
        ge=1,
        le=65535,
        description="gRPC server port",
    )
    max_workers: int = Field(
        default=FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS,
        ge=1,
        le=100,
        description="Maximum gRPC worker threads",
    )

    # gRPC Client Configuration
    timeout: float = Field(
        default=FlextConstants.Network.DEFAULT_TIMEOUT,
        gt=0,
        description="gRPC client timeout",
    )

    # gRPC Security
    tls_enabled: bool = Field(default=False, description="Enable gRPC TLS")

    # gRPC Streaming
    streaming_enabled: bool = Field(default=True, description="Enable gRPC streaming")


__all__ = [
    "FlextGrpcConfig",
]
