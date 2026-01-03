"""FLEXT gRPC Types - Domain-specific gRPC type definitions.

This module provides gRPC-specific type definitions extending t.
Follows FLEXT standards:
- Domain-specific complex types only
- No simple aliases to primitive types
- Python 3.13+ syntax
- Extends t properly

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import logging
import re

# Note: All protocol definitions are centralized in protocols.py
# Use p.Grpc.* for protocols (ServerProtocol, ClientProtocol, GrpcChannel, etc.)
from flext_grpc.constants import FlextGrpcConstants

c = FlextGrpcConstants

# =============================================================================
# GRPC-SPECIFIC TYPE VARIABLES - Domain-specific TypeVars for gRPC operations
# =============================================================================


# JSON value type alias - defined at module level for recursive reference
type JsonValue = (
    str | int | float | bool | list[JsonValue] | dict[str, JsonValue] | None
)


# FLEXT Foundation Types (minimal implementation for independence)
class FlextTypes:
    """Minimal FlextTypes implementation for independence."""

    # Re-export module-level JsonValue for class access (recursive type)
    type JsonValue = (
        str
        | int
        | float
        | bool
        | list[FlextTypes.JsonValue]
        | dict[str, FlextTypes.JsonValue]
        | None
    )
    type ConfigValue = (
        str | int | bool | list[str] | dict[str, FlextTypes.JsonValue] | None
    )
    type GeneralValueType = JsonValue  # Alias for compatibility


# gRPC domain TypeVars
class FlextGrpcTypes(FlextTypes):
    """gRPC-specific type definitions extending t.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # Type aliases for convenience (moved inside class)
    # ConfigValue inherited from FlextTypes

    # gRPC target types (moved from flext-core to domain-specific location)
    type GrpcTarget = str
    # Type aliases for gRPC literals - use type alias syntax
    # Updated to access Literal types directly from Grpc (not via GrpcLiterals)
    type GrpcStreamType = c.Grpc.StreamTypeLiteral
    type GrpcChannelState = c.Grpc.ChannelStateLiteral
    type GrpcServerState = c.Grpc.ServerStateLiteral

    # gRPC options type - standardized options dict
    type GrpcOptions = dict[
        str,
        str
        | int
        | float
        | bool
        | list[FlextTypes.JsonValue]
        | dict[str, FlextTypes.JsonValue]
        | None,
    ]

    # =========================================================================
    # GRPC SERVER TYPES - Complex server management types
    # =========================================================================

    # =========================================================================
    # GRPC CORE TYPES - Commonly used gRPC-specific types
    # =========================================================================

    class GrpcCore:
        """Core gRPC types extending t."""

        # gRPC basic types
        type GrpcDict = dict[str, FlextTypes.JsonValue]
        type GrpcHeaders = dict[str, str]
        type GrpcMetadata = dict[str, FlextTypes.JsonValue]
        type GrpcConfigDict = dict[str, str | int | bool | FlextTypes.JsonValue]

        # gRPC network types
        type GrpcAddress = dict[str, str | int]
        type GrpcEndpoint = dict[str, str | int | bool]
        type GrpcConnection = dict[str, FlextTypes.JsonValue]

        # gRPC service types
        type GrpcServiceData = dict[str, FlextTypes.JsonValue]
        type GrpcMethodData = dict[str, FlextTypes.JsonValue]
        type GrpcRequestDict = dict[str, FlextTypes.JsonValue]
        type GrpcResponseDict = dict[str, FlextTypes.JsonValue]

        # gRPC stream types
        type GrpcStreamData = dict[str, FlextTypes.JsonValue]
        type GrpcStreamMeta = dict[str, str | int | bool]

    # Alias for backward compatibility - avoid inheritance to prevent override issues
    # class Core:
    #     """Alias for GrpcCore for backward compatibility."""

    class Server:
        """gRPC server complex types."""

        type ServerConfiguration = dict[
            str,
            str | int | bool | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type ServerLifecycle = dict[
            str, str | bool | int | dict[str, FlextTypes.JsonValue]
        ]
        type ServerMetrics = dict[
            str,
            int | float | bool | dict[str, FlextTypes.JsonValue],
        ]
        type ServerSecurity = dict[
            str,
            bool | str | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type ServiceRegistry = dict[
            str,
            list[str] | dict[str, FlextTypes.JsonValue],
        ]
        type HandlerConfiguration = list[dict[str, str | FlextTypes.JsonValue]]

    # =========================================================================
    # GRPC CLIENT TYPES - Complex client management types
    # =========================================================================

    class Client:
        """gRPC client complex types."""

        type ClientConfiguration = dict[
            str,
            str | int | bool | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type ConnectionPool = dict[str, int | bool | dict[str, FlextTypes.JsonValue]]
        type RetryConfiguration = dict[str, int | float | bool | list[str]]
        type LoadBalancing = dict[str, str | bool | dict[str, FlextTypes.JsonValue]]
        type ClientMetrics = dict[
            str,
            int | float | dict[str, FlextTypes.JsonValue],
        ]
        type ChannelOptions = dict[
            str, str | int | bool | dict[str, FlextTypes.JsonValue]
        ]

    # =========================================================================
    # GRPC STREAMING TYPES - Complex streaming operation types
    # =========================================================================

    class Streaming:
        """gRPC streaming complex types."""

        type StreamConfiguration = dict[
            str,
            bool | int | str | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type StreamingContext = dict[
            str,
            str | bool | dict[str, FlextTypes.JsonValue],
        ]
        type StreamMetrics = dict[
            str, int | float | bool | dict[str, FlextTypes.JsonValue]
        ]
        type FlowControl = dict[str, int | bool | dict[str, FlextGrpcTypes.ConfigValue]]
        type BackpressureHandling = dict[
            str, str | int | bool | dict[str, FlextTypes.JsonValue]
        ]
        type StreamingPipeline = list[dict[str, str | FlextTypes.JsonValue]]

    # =========================================================================
    # GRPC SERVICE TYPES - Complex service definition types
    # =========================================================================

    class GrpcService:
        """gRPC service complex types."""

        type ServiceDefinition = dict[
            str,
            str | list[str] | dict[str, FlextTypes.JsonValue],
        ]
        type MethodDefinition = dict[str, str | bool | dict[str, FlextTypes.JsonValue]]
        type ServiceMetadata = dict[
            str,
            str | int | dict[str, FlextTypes.JsonValue],
        ]
        type InterceptorChain = list[dict[str, str | FlextTypes.JsonValue]]
        type ServiceDiscovery = dict[
            str,
            str | list[str] | dict[str, FlextTypes.JsonValue],
        ]
        type HealthCheck = dict[str, bool | str | int | dict[str, FlextTypes.JsonValue]]

    # =========================================================================
    # GRPC SECURITY TYPES - Complex security configuration types
    # =========================================================================

    class Security:
        """gRPC security complex types."""

        type SecurityConfiguration = dict[
            str,
            bool | str | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type TlsConfiguration = dict[str, str | bool | dict[str, FlextTypes.JsonValue]]
        type AuthenticationConfig = dict[str, str | dict[str, FlextTypes.JsonValue]]
        type AuthorizationRules = list[dict[str, str | bool | list[str]]]
        type CertificateManagement = dict[
            str,
            str | bool | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type SecurityMetrics = dict[
            str,
            int | bool | dict[str, FlextTypes.JsonValue],
        ]

    # =========================================================================
    # GRPC MONITORING TYPES - Complex monitoring and observability types
    # =========================================================================

    class Monitoring:
        """gRPC monitoring complex types."""

        type MonitoringConfiguration = dict[
            str,
            bool | str | int | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type MetricsCollection = dict[
            str,
            str | bool | dict[str, FlextTypes.JsonValue],
        ]
        type TracingConfiguration = dict[
            str, bool | str | dict[str, FlextTypes.JsonValue]
        ]
        type LoggingSetup = dict[
            str,
            str | bool | int | dict[str, FlextGrpcTypes.ConfigValue],
        ]
        type AlertingRules = list[dict[str, str | int | float | bool]]
        type PerformanceMetrics = dict[
            str,
            float | int | dict[str, FlextTypes.JsonValue],
        ]

    # =========================================================================
    # GRPC LITERAL TYPES - Domain-specific literal values (moved to constants)
    # =========================================================================
    # All literal types are now defined at c.Grpc level for direct access.
    # Use: c.Grpc.ChannelStateLiteral, c.Grpc.ServerStateLiteral, c.Grpc.StreamTypeLiteral

    # =========================================================================
    # GRPC PROJECT TYPES - Domain-specific project types extending t
    # =========================================================================

    class Project:
        """gRPC-specific project types.

        Adds gRPC/microservices-specific project types.
        Follows domain separation principle:
        gRPC domain owns microservices-specific types.
        """

        # gRPC-specific project configurations
        type GrpcProjectConfig = dict[
            str, FlextGrpcTypes.ConfigValue | FlextTypes.JsonValue
        ]
        type MicroserviceConfig = dict[str, str | int | bool | list[str]]
        type StreamingConfig = dict[str, bool | str | dict[str, FlextTypes.JsonValue]]
        type ServiceMeshConfig = dict[
            str, FlextGrpcTypes.ConfigValue | FlextTypes.JsonValue
        ]

    class Grpc:
        """Grpc types namespace for cross-project access.

        Provides organized access to all Grpc types for other FLEXT projects.
        Usage: Other projects can reference `t.Grpc.Server.*`, `t.Grpc.Client.*`, etc.
        This enables consistent namespace patterns for cross-project type access.

        Examples:
            from flext_grpc.typings import t
            config: t.Grpc.Server.ServerConfiguration = ...
            client: t.Grpc.Client.ClientConfiguration = ...

        Note: Namespace composition via inheritance - no aliases needed.
        Access parent namespaces directly through inheritance.

        """

    # =========================================================================
    # GRPC PROTOCOLS - Moved to protocols.py
    # =========================================================================
    # All protocol definitions are centralized in protocols.py
    # Use p.Grpc.* for protocols (GrpcChannel, GrpcServer, GrpcStub, etc.)

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
                logger = logging.getLogger(__name__)
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
            if not FlextGrpcTypes.GrpcValidation.validate_target(target):
                msg = f"Invalid gRPC target: {target}"
                raise ValueError(msg)
            host, port_str = target.split(":", 1)
            return (host, int(port_str))


# Alias for simplified usage
t = FlextGrpcTypes

# Namespace composition via class inheritance
# Grpc namespace provides access to nested classes through inheritance
# Access patterns:
# - t.Grpc.* for Grpc-specific types
# - t.Project.* for project types
# - t.Core.* for core types (inherited from parent)

__all__ = ["FlextGrpcTypes", "t"]
