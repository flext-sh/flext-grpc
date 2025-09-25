"""FLEXT gRPC Types - Domain-specific gRPC type definitions.

This module provides gRPC-specific type definitions extending FlextTypes.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextTypes properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import Literal, Protocol, TypeVar, runtime_checkable

from flext_core import FlextLogger, FlextTypes

# =============================================================================
# GRPC-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for gRPC operations
# =============================================================================

# gRPC domain TypeVars
TGrpcServer = TypeVar("TGrpcServer")
TGrpcClient = TypeVar("TGrpcClient")
TGrpcChannel = TypeVar("TGrpcChannel")
TGrpcService = TypeVar("TGrpcService")
TGrpcStream = TypeVar("TGrpcStream")
TGrpcStub = TypeVar("TGrpcStub")
TGrpcHandler = TypeVar("TGrpcHandler")
TGrpcInterceptor = TypeVar("TGrpcInterceptor")


class FlextGrpcTypes(FlextTypes):
    """gRPC-specific type definitions extending FlextTypes.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # =============================================================================
    # NETWORK CONSTANTS
    # =============================================================================
    MIN_PORT = 1
    MAX_PORT = 65535

    # =========================================================================
    # GRPC SERVER TYPES - Complex server management types
    # =========================================================================

    class Server:
        """gRPC server complex types."""

        type ServerConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ServerLifecycle = dict[str, str | bool | int | dict[str, object]]
        type ServerMetrics = dict[
            str, int | float | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ServerSecurity = dict[
            str, bool | str | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ServiceRegistry = dict[
            str, list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type HandlerConfiguration = list[dict[str, str | object]]

    # =========================================================================
    # GRPC CLIENT TYPES - Complex client management types
    # =========================================================================

    class Client:
        """gRPC client complex types."""

        type ClientConfiguration = dict[
            str, str | int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type ConnectionPool = dict[str, int | bool | dict[str, object]]
        type RetryConfiguration = dict[str, int | float | bool | list[str]]
        type LoadBalancing = dict[
            str, str | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ClientMetrics = dict[
            str, int | float | dict[str, FlextTypes.Core.JsonValue]
        ]
        type ChannelOptions = dict[str, str | int | bool | dict[str, object]]

    # =========================================================================
    # GRPC STREAMING TYPES - Complex streaming operation types
    # =========================================================================

    class Streaming:
        """gRPC streaming complex types."""

        type StreamConfiguration = dict[
            str, bool | int | str | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type StreamingContext = dict[
            str, str | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type StreamMetrics = dict[str, int | float | bool | dict[str, object]]
        type FlowControl = dict[
            str, int | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type BackpressureHandling = dict[str, str | int | bool | dict[str, object]]
        type StreamingPipeline = list[dict[str, str | object]]

    # =========================================================================
    # GRPC SERVICE TYPES - Complex service definition types
    # =========================================================================

    class GrpcService:
        """gRPC service complex types."""

        type ServiceDefinition = dict[
            str, str | list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type MethodDefinition = dict[str, str | bool | dict[str, object]]
        type ServiceMetadata = dict[
            str, str | int | dict[str, FlextTypes.Core.JsonValue]
        ]
        type InterceptorChain = list[dict[str, str | object]]
        type ServiceDiscovery = dict[
            str, str | list[str] | dict[str, FlextTypes.Core.JsonValue]
        ]
        type HealthCheck = dict[str, bool | str | int | dict[str, object]]

    # =========================================================================
    # GRPC SECURITY TYPES - Complex security configuration types
    # =========================================================================

    class Security:
        """gRPC security complex types."""

        type SecurityConfiguration = dict[
            str, bool | str | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type TlsConfiguration = dict[str, str | bool | dict[str, object]]
        type AuthenticationConfig = dict[
            str, str | dict[str, FlextTypes.Core.JsonValue]
        ]
        type AuthorizationRules = list[dict[str, str | bool | list[str]]]
        type CertificateManagement = dict[
            str, str | bool | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type SecurityMetrics = dict[
            str, int | bool | dict[str, FlextTypes.Core.JsonValue]
        ]

    # =========================================================================
    # GRPC MONITORING TYPES - Complex monitoring and observability types
    # =========================================================================

    class Monitoring:
        """gRPC monitoring complex types."""

        type MonitoringConfiguration = dict[
            str, bool | str | int | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type MetricsCollection = dict[
            str, str | bool | dict[str, FlextTypes.Core.JsonValue]
        ]
        type TracingConfiguration = dict[str, bool | str | dict[str, object]]
        type LoggingSetup = dict[
            str, str | bool | int | dict[str, FlextTypes.Core.ConfigValue]
        ]
        type AlertingRules = list[dict[str, str | int | float | bool]]
        type PerformanceMetrics = dict[
            str, float | int | dict[str, FlextTypes.Core.JsonValue]
        ]

    # =========================================================================
    # GRPC LITERAL TYPES - Domain-specific literal values
    # =========================================================================

    # Channel state literals
    type ChannelState = Literal[
        "idle", "connecting", "ready", "transient_failure", "shutdown"
    ]

    # Server state literals
    type ServerState = Literal["stopped", "starting", "running", "stopping"]

    # Stream type literals
    type StreamType = Literal[
        "unary", "server_streaming", "client_streaming", "bidirectional"
    ]

    # Load balancing policy literals
    type LoadBalancingPolicy = Literal[
        "round_robin", "pick_first", "grpclb", "xds_cluster_resolver"
    ]

    # Compression literals
    type CompressionType = Literal["none", "gzip", "deflate"]

    # =========================================================================
    # GRPC PROTOCOLS - Protocol definitions for gRPC interfaces
    # =========================================================================

    class Protocols:
        """gRPC protocol types for interface definitions."""

        @runtime_checkable
        class GrpcChannel(Protocol):
            """Protocol for gRPC channel operations."""

            def close(self) -> None:
                """Close the channel."""
                ...

            def unsubscribe(self, callback: object) -> None:
                """Remove a subscription callback from the channel."""
                ...

        @runtime_checkable
        class GrpcServer(Protocol):
            """Protocol for gRPC server operations."""

            def add_generic_rpc_handlers(self, handlers: list[object]) -> None:
                """Add generic RPC handlers."""
                ...

            def start(self) -> None:
                """Start the server."""
                ...

            def stop(self, grace: float | None) -> None:
                """Stop the server with optional grace period."""
                ...

        @runtime_checkable
        class GrpcStub(Protocol):
            """Protocol for gRPC client stub."""

            def __init__(self, channel: FlextGrpcTypes.Protocols.GrpcChannel) -> None:
                """Initialize the stub with a channel."""
                ...

    # =========================================================================
    # GRPC VALIDATION - Helper functions for gRPC operations
    # =========================================================================

    class GrpcValidation:
        """gRPC validation utilities."""

        @staticmethod
        def validate_target(target: str) -> bool:
            """Validate a gRPC target string in the form host:port."""
            if not target or ":" not in target:
                return False
            try:
                host, port_str = target.split(":", 1)
                if not host or not port_str:
                    return False
                if not re.match(r"^[a-zA-Z0-9.-]+$", host):
                    return False
                port = int(port_str)
                return FlextGrpcTypes.MIN_PORT <= port <= FlextGrpcTypes.MAX_PORT
            except (ValueError, AttributeError):
                logger = FlextLogger(__name__)
                logger.debug("Invalid gRPC target: %s", target)
                return False

        @staticmethod
        def parse_target(target: str) -> tuple[str, int]:
            """Parse a validated gRPC target into (host, port).

            Raises ValueError if the target is invalid. Prefer checking with
            validate_target() beforehand when you need a boolean.

            Returns:
                tuple[str, int]: Host and port components.

            """
            if not FlextGrpcTypes.GrpcValidation.validate_target(target):
                msg = f"Invalid gRPC target: {target}"
                raise ValueError(msg)
            host, port_str = target.split(":", 1)
            return (host, int(port_str))


# =============================================================================
# PUBLIC API EXPORTS - gRPC TypeVars and types
# =============================================================================

__all__: list[str] = [
    # gRPC Types class
    "FlextGrpcTypes",
    # gRPC-specific TypeVars
    "TGrpcChannel",
    "TGrpcClient",
    "TGrpcHandler",
    "TGrpcInterceptor",
    "TGrpcServer",
    "TGrpcService",
    "TGrpcStream",
    "TGrpcStub",
]
