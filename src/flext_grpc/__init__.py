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

# API functions
from flext_grpc.api import (
    create_channel,
    create_client,
    create_config,
    create_server,
    create_service,
    create_stream,
    create_complete_setup,
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
    FlextGrpcServerService,
    FlextGrpcClientService, 
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
    "FlextGrpcPlatform", 
    "FlextResult",
    "__version__",
    "__version_info__",
    
    # Configuration
    "FlextGrpcConfig",
    
    # Domain Entities
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcServer", 
    "FlextGrpcService",
    "FlextGrpcStream",
    
    # Domain Services
    "FlextGrpcServerService",
    "FlextGrpcClientService",
    "FlextGrpcStreamService",
    
    # Errors
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError", 
    "FlextGrpcError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
    
    # API Functions
    "create_channel",
    "create_client",
    "create_config", 
    "create_server",
    "create_service",
    "create_stream",
    "create_complete_setup",
    "parse_address",
    "validate_address",
    
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
    "flext_grpc_parse_target",
    "flext_grpc_validate_target",
]

# Module metadata
__architecture__ = "Clean Architecture + DDD"