"""FLEXT gRPC Configuration - Advanced Configuration Management.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextCore
from pydantic import Field

from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcConfig(FlextCore.Config):
    """gRPC configuration extending FlextCore.Config with gRPC-specific settings.

    Inherits ALL FlextCore.Config capabilities (configuration management, environment variables, etc.)
    and adds gRPC-specific configuration fields.
    """

    # gRPC Server Configuration
    host: str = Field(
        default=FlextCore.Constants.Platform.DEFAULT_HOST,
        description="gRPC server host",
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
        default=FlextCore.Constants.Network.DEFAULT_TIMEOUT,
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
