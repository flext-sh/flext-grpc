"""FLEXT gRPC - Enterprise gRPC Communication Platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Modern gRPC communication platform following Clean Architecture and Domain-Driven Design.
Built on Python 3.13 with unified client/server management and streaming capabilities.
"""

from __future__ import annotations

import importlib.metadata

# Import from flext-core for foundational patterns
from flext_core import FlextContainer, FlextResult

try:
    __version__ = importlib.metadata.version("flext-grpc")
except importlib.metadata.PackageNotFoundError:
    __version__ = "1.0.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

# Application services
from flext_grpc.application.services import (
    FlextGrpcClientService,
    FlextGrpcServerService,
    FlextGrpcStreamService,
)

# Configuration
from flext_grpc.config import (
    FlextGrpcClientConfig,
    FlextGrpcServerConfig,
)

# Domain entities
from flext_grpc.domain.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)

# Platform
from flext_grpc.platform import FlextGrpcPlatform

# Simple API
from flext_grpc.simple_api import (
    create_flext_grpc_channel,
    create_flext_grpc_client,
    create_flext_grpc_server,
    validate_flext_grpc_address,
)

# Main FlextGrpc aliases
FlextGrpc = FlextGrpcPlatform
FlextGrpcResult = FlextResult

# Prefixed helper functions
flext_grpc_create_channel = create_flext_grpc_channel
flext_grpc_create_client = create_flext_grpc_client
flext_grpc_create_server = create_flext_grpc_server
flext_grpc_create_service = create_flext_grpc_server  # Alias for backward compatibility
flext_grpc_validate_address = validate_flext_grpc_address


def create_flext_grpc_platform(
    config: dict[str, object] | None = None,
) -> FlextGrpcPlatform:
    """Create unified FLEXT gRPC platform instance.

    Args:
        config: Optional configuration dictionary

    Returns:
        Configured FlextGrpcPlatform instance

    """
    return FlextGrpcPlatform(config or {})


flext_grpc_create_platform = create_flext_grpc_platform

__all__ = [
    "FlextContainer",
    "FlextGrpc",
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcClientConfig",
    "FlextGrpcClientService",
    "FlextGrpcPlatform",
    "FlextGrpcResult",
    "FlextGrpcServer",
    "FlextGrpcServerConfig",
    "FlextGrpcServerService",
    "FlextGrpcService",
    "FlextGrpcStream",
    "FlextGrpcStreamService",
    "FlextResult",
    "__version__",
    "__version_info__",
    "create_flext_grpc_channel",
    "create_flext_grpc_client",
    "create_flext_grpc_platform",
    "create_flext_grpc_server",
    "flext_grpc_create_channel",
    "flext_grpc_create_client",
    "flext_grpc_create_platform",
    "flext_grpc_create_server",
    "flext_grpc_create_service",
    "flext_grpc_validate_address",
    "validate_flext_grpc_address",
]

# Module metadata
__architecture__ = "Clean Architecture + DDD"
