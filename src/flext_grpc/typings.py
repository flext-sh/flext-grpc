"""FLEXT gRPC Types - Domain-specific gRPC type definitions.

This module provides gRPC-specific type definitions extending FlextCore.Types.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends FlextCore.Types properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import Protocol, override, runtime_checkable

from flext_core import FlextCore

from flext_grpc.constants import FlextGrpcConstants

# =============================================================================
# GRPC-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for gRPC operations
# =============================================================================


# gRPC domain TypeVars
class FlextGrpcTypings(FlextCore.Types):
    """gRPC-specific type definitions extending FlextCore.Types.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # Type aliases for convenience (moved inside class)
    ConfigValue = FlextCore.Types.ConfigValue
    JsonValue = FlextCore.Types.JsonValue

    # gRPC target types (moved from flext-core to domain-specific location)
    type GrpcTarget = str
    type GrpcStreamType = FlextGrpcConstants.Literals.StreamType
    type GrpcChannelState = FlextGrpcConstants.Literals.ChannelState
    type GrpcServerState = FlextGrpcConstants.Literals.ServerState

    # =========================================================================
    # GRPC SERVER TYPES - Complex server management types
    # =========================================================================

    # =========================================================================
    # GRPC CORE TYPES - Commonly used gRPC-specific types
    # =========================================================================

    class GrpcCore:
        """Core gRPC types extending FlextCore.Types."""

        # gRPC basic types
        type GrpcDict = FlextCore.Types.Dict
        type GrpcHeaders = FlextCore.Types.StringDict
        type GrpcMetadata = FlextCore.Types.Dict
        type GrpcConfigDict = dict[str, str | int | bool | object]

        # gRPC network types
        type GrpcAddress = dict[str, str | int]
        type GrpcEndpoint = dict[str, str | int | bool]
        type GrpcConnection = FlextCore.Types.Dict

        # gRPC service types
        type GrpcServiceData = FlextCore.Types.Dict
        type GrpcMethodData = FlextCore.Types.Dict
        type GrpcRequestDict = FlextCore.Types.Dict
        type GrpcResponseDict = FlextCore.Types.Dict

        # gRPC stream types
        type GrpcStreamData = FlextCore.Types.Dict
        type GrpcStreamMeta = dict[str, str | int | bool]

    # Alias for backward compatibility
    class Core(GrpcCore):
        """Alias for GrpcCore for backward compatibility."""

    class Server:
        """gRPC server complex types."""

        type ServerConfiguration = dict[
            str, str | int | bool | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type ServerLifecycle = dict[str, str | bool | int | FlextCore.Types.Dict]
        type ServerMetrics = dict[
            str, int | float | bool | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type ServerSecurity = dict[
            str, bool | str | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type ServiceRegistry = dict[
            str, FlextCore.Types.StringList | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type HandlerConfiguration = list[dict[str, str | object]]

    # =========================================================================
    # GRPC CLIENT TYPES - Complex client management types
    # =========================================================================

    class Client:
        """gRPC client complex types."""

        type ClientConfiguration = dict[
            str, str | int | bool | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type ConnectionPool = dict[str, int | bool | FlextCore.Types.Dict]
        type RetryConfiguration = dict[
            str, int | float | bool | FlextCore.Types.StringList
        ]
        type LoadBalancing = dict[
            str, str | bool | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type ClientMetrics = dict[
            str, int | float | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type ChannelOptions = dict[str, str | int | bool | FlextCore.Types.Dict]

    # =========================================================================
    # GRPC STREAMING TYPES - Complex streaming operation types
    # =========================================================================

    class Streaming:
        """gRPC streaming complex types."""

        type StreamConfiguration = dict[
            str, bool | int | str | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type StreamingContext = dict[
            str, str | bool | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type StreamMetrics = dict[str, int | float | bool | FlextCore.Types.Dict]
        type FlowControl = dict[
            str, int | bool | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type BackpressureHandling = dict[str, str | int | bool | FlextCore.Types.Dict]
        type StreamingPipeline = list[dict[str, str | object]]

    # =========================================================================
    # GRPC SERVICE TYPES - Complex service definition types
    # =========================================================================

    class GrpcService:
        """gRPC service complex types."""

        type ServiceDefinition = dict[
            str,
            str | FlextCore.Types.StringList | dict[str, FlextGrpcTypings.JsonValue],
        ]
        type MethodDefinition = dict[str, str | bool | FlextCore.Types.Dict]
        type ServiceMetadata = dict[
            str, str | int | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type InterceptorChain = list[dict[str, str | object]]
        type ServiceDiscovery = dict[
            str,
            str | FlextCore.Types.StringList | dict[str, FlextGrpcTypings.JsonValue],
        ]
        type HealthCheck = dict[str, bool | str | int | FlextCore.Types.Dict]

    # =========================================================================
    # GRPC SECURITY TYPES - Complex security configuration types
    # =========================================================================

    class Security:
        """gRPC security complex types."""

        type SecurityConfiguration = dict[
            str, bool | str | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type TlsConfiguration = dict[str, str | bool | FlextCore.Types.Dict]
        type AuthenticationConfig = dict[
            str, str | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type AuthorizationRules = list[
            dict[str, str | bool | FlextCore.Types.StringList]
        ]
        type CertificateManagement = dict[
            str, str | bool | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type SecurityMetrics = dict[
            str, int | bool | dict[str, FlextGrpcTypings.JsonValue]
        ]

    # =========================================================================
    # GRPC MONITORING TYPES - Complex monitoring and observability types
    # =========================================================================

    class Monitoring:
        """gRPC monitoring complex types."""

        type MonitoringConfiguration = dict[
            str, bool | str | int | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type MetricsCollection = dict[
            str, str | bool | dict[str, FlextGrpcTypings.JsonValue]
        ]
        type TracingConfiguration = dict[str, bool | str | FlextCore.Types.Dict]
        type LoggingSetup = dict[
            str, str | bool | int | dict[str, FlextGrpcTypings.ConfigValue]
        ]
        type AlertingRules = list[dict[str, str | int | float | bool]]
        type PerformanceMetrics = dict[
            str, float | int | dict[str, FlextGrpcTypings.JsonValue]
        ]

    # =========================================================================
    # GRPC LITERAL TYPES - Domain-specific literal values (moved to constants)
    # =========================================================================
    # All literal types are now defined in FlextGrpcConstants.Literals
    # Use FlextGrpcConstants.Literals.ChannelState, etc.

    # =========================================================================
    # GRPC PROJECT TYPES - Domain-specific project types extending FlextCore.Types
    # =========================================================================

    class Project(FlextCore.Types.Project):
        """gRPC-specific project types extending FlextCore.Types.Project.

        Adds gRPC/microservices-specific project types while inheriting
        generic types from FlextCore.Types. Follows domain separation principle:
        gRPC domain owns microservices-specific types.
        """

        # gRPC-specific project configurations (no ProjectType override to avoid conflicts)

        # gRPC-specific project configurations
        type GrpcProjectConfig = dict[str, FlextGrpcTypings.ConfigValue | object]
        type MicroserviceConfig = dict[
            str, str | int | bool | FlextCore.Types.StringList
        ]
        type StreamingConfig = dict[str, bool | str | FlextCore.Types.Dict]
        type ServiceMeshConfig = dict[str, FlextGrpcTypings.ConfigValue | object]

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

            def add_generic_rpc_handlers(self, handlers: FlextCore.Types.List) -> None:
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

            @override
            def __init__(self, channel: FlextGrpcTypings.Protocols.GrpcChannel) -> None:
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
                max_port = 65535
                return 1 <= port <= max_port
            except (ValueError, AttributeError):
                logger = FlextCore.Logger(__name__)
                logger.debug("Invalid gRPC target: %s", target)
                return False

        @staticmethod
        def parse_target(target: str) -> tuple[str, int]:
            """Parse a validated gRPC target into (host, port).

            Raises ValueError if the target is invalid. Prefer checking with
            validate_target() beforehand when you need a boolean.

            Returns:
                tuple["str", "int"]: Host and port components.

            """
            if not FlextGrpcTypings.GrpcValidation.validate_target(target):
                msg = f"Invalid gRPC target: {target}"
                raise ValueError(msg)
            host, port_str = target.split(":", 1)
            return (host, int(port_str))
