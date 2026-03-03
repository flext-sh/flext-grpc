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
from typing import TypeAlias

from flext_core import FlextTypes

from flext_grpc import c


# gRPC domain TypeVars
class FlextGrpcTypes(FlextTypes):
    """gRPC-specific type definitions extending t.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    # Inherit ContainerValue from FlextTypes
    ConfigValue: TypeAlias = FlextTypes.JsonValue
    GrpcOptions = dict[str, FlextTypes.JsonValue]

    class Grpc:
        """gRPC-specific type namespace for domain aliases and validators."""

        # Type aliases using TypeAlias (not PEP 695 type statements inside class)
        # gRPC basic types
        Dict: TypeAlias = dict[str, FlextTypes.JsonValue]
        GrpcDict: TypeAlias = dict[str, FlextTypes.JsonValue]
        Headers: TypeAlias = dict[str, str]
        Metadata: TypeAlias = dict[str, FlextTypes.JsonValue]
        ConfigDict: TypeAlias = dict[str, str | int | bool | FlextTypes.JsonValue]

        # gRPC network types
        Address: TypeAlias = dict[str, str | int]
        Endpoint: TypeAlias = dict[str, str | int | bool]
        Connection: TypeAlias = dict[str, FlextTypes.JsonValue]

        # gRPC service types
        ServiceData: TypeAlias = dict[str, FlextTypes.JsonValue]
        MethodData: TypeAlias = dict[str, FlextTypes.JsonValue]
        RequestDict: TypeAlias = dict[str, FlextTypes.JsonValue]
        ResponseDict: TypeAlias = dict[str, FlextTypes.JsonValue]

        # gRPC stream types
        StreamData: TypeAlias = dict[str, FlextTypes.JsonValue]
        StreamMeta: TypeAlias = dict[str, str | int | bool]

        # gRPC target types (moved from flext-core to domain-specific location)
        Target = str
        # Type aliases for gRPC literals - use type alias syntax
        # Updated to access Literal types directly from Grpc (not via GrpcLiterals)
        StreamType = c.Grpc.StreamTypeLiteral
        ChannelState: TypeAlias = c.Grpc.ChannelStateLiteral
        ServerState: TypeAlias = c.Grpc.ServerStateLiteral

        # gRPC options type - standardized options dict
        Options: TypeAlias = dict[
            str,
            FlextTypes.Scalar
            | list[FlextTypes.JsonValue]
            | dict[str, FlextTypes.JsonValue]
            | None,
        ]

        # =========================================================================
        # GRPC SERVER TYPES - Complex server management types
        # =========================================================================

        class Server:
            """gRPC server complex types."""

            ServerConfiguration = dict[
                str,
                str | int | bool | dict[str, FlextTypes.JsonValue],
            ]
            ServerLifecycle = dict[
                str,
                str | bool | int | dict[str, FlextTypes.JsonValue],
            ]
            ServerMetrics = dict[
                str,
                int | float | bool | dict[str, FlextTypes.JsonValue],
            ]
            ServerSecurity = dict[
                str,
                bool | str | dict[str, FlextTypes.JsonValue],
            ]
            ServiceRegistry = dict[
                str,
                list[str] | dict[str, FlextTypes.JsonValue],
            ]
            HandlerConfiguration: TypeAlias = list[
                dict[str, str | FlextTypes.JsonValue]
            ]

        # =========================================================================
        # GRPC CLIENT TYPES - Complex client management types
        # =========================================================================

        class Client:
            """gRPC client complex types."""

            ClientConfiguration = dict[
                str,
                str | int | bool | dict[str, FlextTypes.JsonValue],
            ]
            ConnectionPool = dict[str, int | bool | dict[str, FlextTypes.JsonValue]]
            RetryConfiguration: TypeAlias = dict[str, int | float | bool | list[str]]
            LoadBalancing: TypeAlias = dict[
                str,
                str | bool | dict[str, FlextTypes.JsonValue],
            ]
            ClientMetrics = dict[
                str,
                int | float | dict[str, FlextTypes.JsonValue],
            ]
            ChannelOptions = dict[
                str,
                str | int | bool | dict[str, FlextTypes.JsonValue],
            ]

        # =========================================================================
        # GRPC STREAMING TYPES - Complex streaming operation types
        # =========================================================================

        class Streaming:
            """gRPC streaming complex types."""

            StreamConfiguration = dict[
                str,
                bool | int | str | dict[str, FlextTypes.JsonValue],
            ]
            StreamingContext = dict[
                str,
                str | bool | dict[str, FlextTypes.JsonValue],
            ]
            StreamMetrics = dict[
                str,
                int | float | bool | dict[str, FlextTypes.JsonValue],
            ]
            FlowControl = dict[str, int | bool | dict[str, FlextTypes.JsonValue]]
            BackpressureHandling = dict[
                str,
                str | int | bool | dict[str, FlextTypes.JsonValue],
            ]
            StreamingPipeline: TypeAlias = list[dict[str, str | FlextTypes.JsonValue]]

        # =========================================================================
        # GRPC SERVICE TYPES - Complex service definition types
        # =========================================================================

        class GrpcService:
            """gRPC service complex types."""

            ServiceDefinition = dict[
                str,
                str | list[str] | dict[str, FlextTypes.JsonValue],
            ]
            MethodDefinition = dict[str, str | bool | dict[str, FlextTypes.JsonValue]]
            ServiceMetadata = dict[
                str,
                str | int | dict[str, FlextTypes.JsonValue],
            ]
            InterceptorChain: TypeAlias = list[dict[str, str | FlextTypes.JsonValue]]
            ServiceDiscovery = dict[
                str,
                str | list[str] | dict[str, FlextTypes.JsonValue],
            ]
            HealthCheck = dict[str, bool | str | int | dict[str, FlextTypes.JsonValue]]

        # =========================================================================
        # GRPC SECURITY TYPES - Complex security configuration types
        # =========================================================================

        class Security:
            """gRPC security complex types."""

            SecurityConfiguration = dict[
                str,
                bool | str | dict[str, FlextTypes.JsonValue],
            ]
            TlsConfiguration = dict[str, str | bool | dict[str, FlextTypes.JsonValue]]
            AuthenticationConfig: TypeAlias = dict[
                str,
                str | dict[str, FlextTypes.JsonValue],
            ]
            AuthorizationRules: TypeAlias = list[dict[str, str | bool | list[str]]]
            CertificateManagement = dict[
                str,
                str | bool | dict[str, FlextTypes.JsonValue],
            ]
            SecurityMetrics = dict[
                str,
                int | bool | dict[str, FlextTypes.JsonValue],
            ]

        # =========================================================================
        # GRPC MONITORING TYPES - Complex monitoring and observability types
        # =========================================================================

        class Monitoring:
            """gRPC monitoring complex types."""

            MonitoringConfiguration = dict[
                str,
                bool | str | int | dict[str, FlextTypes.JsonValue],
            ]
            MetricsCollection = dict[
                str,
                str | bool | dict[str, FlextTypes.JsonValue],
            ]
            TracingConfiguration = dict[
                str,
                bool | str | dict[str, FlextTypes.JsonValue],
            ]
            LoggingSetup = dict[
                str,
                str | bool | int | dict[str, FlextTypes.JsonValue],
            ]
            AlertingRules: TypeAlias = list[dict[str, FlextTypes.Scalar]]
            PerformanceMetrics = dict[
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
            ProjectConfig = dict[str, FlextTypes.JsonValue]
            MicroserviceConfig: TypeAlias = dict[str, str | int | bool | list[str]]
            StreamingConfig = dict[str, bool | str | dict[str, FlextTypes.JsonValue]]
            ServiceMeshConfig = dict[str, FlextTypes.JsonValue]

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
                if not FlextGrpcTypes.Grpc.GrpcValidation.validate_target(target):
                    msg = f"Invalid gRPC target: {target}"
                    raise ValueError(msg)
                host, port_str = target.split(":", 1)
                return (host, int(port_str))


t = FlextGrpcTypes

__all__ = ["FlextGrpcTypes", "t"]
