"""FLEXT gRPC - Enterprise gRPC Communication Platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Modern gRPC communication platform following Clean Architecture and DDD.
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

# API functions
from flext_grpc.api import (
    create_channel,
    create_client,
    create_complete_setup,
    create_config,
    create_server,
    create_service,
    create_stream,
    parse_address,
    validate_address,
)

# Configuration
from flext_grpc.config import FlextGrpcConfig

# Domain entities
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)

# Errors
from flext_grpc.errors import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)

# Platform
from flext_grpc.platform import FlextGrpcPlatform

# Domain Services
from flext_grpc.services import (
    FlextGrpcClientService,
    FlextGrpcServerService,
    FlextGrpcStreamService,
)

# Types
from flext_grpc.types import (
    TGrpcChannelState,
    TGrpcHost,
    TGrpcMethodName,
    TGrpcPort,
    TGrpcServerState,
    TGrpcServiceName,
    TGrpcStreamType,
    TGrpcTarget,
    TGrpcTimeout,
    flext_grpc_parse_target,
    flext_grpc_validate_target,
)

__all__ = [
    # Core
    "FlextContainer",
    # Domain Entities
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcClientService",
    # Configuration
    "FlextGrpcConfig",
    # Errors
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcPlatform",
    "FlextGrpcServer",
    # Domain Services
    "FlextGrpcServerService",
    "FlextGrpcService",
    "FlextGrpcStream",
    "FlextGrpcStreamService",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
    "FlextResult",
    # Types
    "TGrpcChannelState",
    "TGrpcHost",
    "TGrpcMethodName",
    "TGrpcPort",
    "TGrpcServerState",
    "TGrpcServiceName",
    "TGrpcStreamType",
    "TGrpcTarget",
    "TGrpcTimeout",
    "__version__",
    "__version_info__",
    # API Functions
    "create_channel",
    "create_client",
    "create_complete_setup",
    "create_config",
    "create_server",
    "create_service",
    "create_stream",
    "flext_grpc_parse_target",
    "flext_grpc_validate_target",
    "parse_address",
    "validate_address",
]

# Module metadata
__architecture__ = "Clean Architecture + DDD"
