"""FLEXT gRPC - Enterprise gRPC Communication Platform with Clean Architecture.

This module provides the public API for the FLEXT gRPC communication platform,
offering enterprise-grade gRPC client/server management, streaming capabilities,
and comprehensive configuration management. Built following Clean Architecture
and Domain-Driven Design principles for maintainable, scalable communication.

Public API Overview:
    The FLEXT gRPC platform provides a comprehensive API for gRPC communication:
    - Domain Entities: Server, Client, Channel, Service, Stream management
    - Configuration: Type-safe, validated configuration with environment integration
    - Services: Domain services for server, client, and stream operations
    - Platform: Unified facade for simplified gRPC operations
    - Types: Type definitions for enhanced type safety
    - API Functions: High-level convenience functions for common operations
    - Error Handling: Custom exception hierarchy for detailed error reporting

Architecture:
    The platform implements Clean Architecture with Domain-Driven Design:
    - Domain Layer: Entities with business logic and validation
    - Application Layer: Domain services orchestrating business workflows
    - Infrastructure Layer: Platform integration and external system coordination
    - Interface Layer: Public API providing simplified access to functionality

Key Features:
    - Unified client/server management with lifecycle coordination
    - Streaming communication support (unary, server, client, bidirectional)
    - Enterprise-grade configuration with comprehensive validation
    - Global dependency injection container integration
    - Type-safe operations with comprehensive error handling
    - Clean Architecture boundaries with dependency inversion
    - Production-ready patterns for enterprise deployment

Example:
    Basic platform usage for gRPC communication:

    >>> from flext_grpc import (
    ...     FlextGrpcPlatform,
    ...     FlextGrpcServer,
    ...     FlextGrpcClient,
    ...     FlextGrpcConfig,
    ...     create_server,
    ...     create_client,
    ... )
    >>>
    >>> # Platform-based approach
    >>> platform = FlextGrpcPlatform()
    >>> server = create_server("api-server", "localhost", 50051)
    >>> client = create_client("api-client", "localhost:50051")
    >>>
    >>> # Start server and connect client
    >>> start_result = platform.start_server(server)
    >>> if start_result.is_success:
    ...     connect_result = platform.connect_client(client)
    ...     if connect_result.is_success:
    ...         # Make remote call
    ...         response = platform.make_call(
    ...             connect_result.data, "GetData", {"query": "latest"}
    ...         )
    >>>
    >>> # Service-based approach for advanced usage
    >>> from flext_grpc import FlextGrpcServerService
    >>> server_service = FlextGrpcServerService()
    >>> result = server_service.execute("start", server)

Integration:
    - Built on flext-core foundation for consistent patterns across FLEXT ecosystem
    - Integrates with flext-observability for monitoring and metrics
    - Supports FLEXT ecosystem service discovery and configuration
    - Compatible with enterprise deployment and orchestration platforms

Version Information:
    - Version: Retrieved from package metadata (fallback: 1.0.0)
    - Architecture: Clean Architecture + Domain-Driven Design
    - Python Requirements: 3.13+
    - gRPC Integration: Modern gRPC Python libraries

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import importlib.metadata

from flext_core import FlextContainer, FlextResult

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
from flext_grpc.config import FlextGrpcConfig
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.errors import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)
from flext_grpc.platform import FlextGrpcPlatform
from flext_grpc.services import (
    FlextGrpcClientService,
    FlextGrpcServerService,
    FlextGrpcStreamService,
)
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

try:
    __version__ = importlib.metadata.version("flext-grpc")
except importlib.metadata.PackageNotFoundError:
    __version__ = "1.0.0"

__version_info__ = tuple(int(x) for x in __version__.split(".") if x.isdigit())

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

# Module metadata for API documentation and tooling
__architecture__ = "Clean Architecture + DDD"
__author__ = "FLEXT Development Team"
__license__ = "MIT"
__copyright__ = "Copyright (c) 2025 FLEXT Contributors"
__status__ = "Production"
__maintainer__ = "FLEXT Development Team"
__email__ = "noreply@flext.dev"
__url__ = "https://github.com/flext/flext-grpc"
__description__ = "Enterprise gRPC communication platform with Clean Architecture"

# API stability and compatibility information
__api_version__ = "1.0"
__stability__ = "stable"
__compatibility__ = "Python 3.13+"
