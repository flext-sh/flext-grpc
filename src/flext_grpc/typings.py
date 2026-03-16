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
from typing import Protocol, TypeAlias, runtime_checkable

from flext_core import FlextTypes

from flext_grpc import c

@runtime_checkable

class FlextGrpcTypes(FlextTypes):
    """gRPC-specific type definitions extending t.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    ConfigValue: TypeAlias = FlextTypes.ContainerValue | None
    GrpcOptions = dict[str, FlextTypes.ContainerValue | None]

    class Grpc:
        """gRPC-specific type namespace for domain aliases and validators."""

        GrpcServicer: TypeAlias = _GrpcServicer

        Dict: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        GrpcDict: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        Headers: TypeAlias = dict[str, str]
        Metadata: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        ConfigDict: TypeAlias = dict[
            str,
            str | int | bool | FlextTypes.ContainerValue | None,
        ]
        Address: TypeAlias = dict[str, str | int]
        Endpoint: TypeAlias = dict[str, str | int | bool]
        Connection: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        ServiceData: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        MethodData: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        RequestDict: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        ResponseDict: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        StreamData: TypeAlias = dict[str, FlextTypes.ContainerValue | None]
        StreamMeta: TypeAlias = dict[str, str | int | bool]
        Target = str
        StreamType = c.Grpc.StreamTypeLiteral
        ChannelState: TypeAlias = c.Grpc.ChannelStateLiteral
        ServerState: TypeAlias = c.Grpc.ServerStateLiteral
        Options: TypeAlias = dict[
            str,
            FlextTypes.Scalar
            | list[FlextTypes.ContainerValue | None]
            | dict[str, FlextTypes.ContainerValue | None]
            | None,
        ]

        class Server:
            """gRPC server complex types."""

            ServerConfiguration = dict[
                str,
                str | int | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            ServerLifecycle = dict[
                str,
                str | bool | int | dict[str, FlextTypes.ContainerValue | None],
            ]
            ServerMetrics = dict[
                str,
                int | float | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            ServerSecurity = dict[
                str,
                bool | str | dict[str, FlextTypes.ContainerValue | None],
            ]
            ServiceRegistry = dict[
                str,
                list[str] | dict[str, FlextTypes.ContainerValue | None],
            ]
            HandlerConfiguration: TypeAlias = list[
                dict[str, str | FlextTypes.ContainerValue | None]
            ]

        class Client:
            """gRPC client complex types."""

            ClientConfiguration = dict[
                str,
                str | int | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            ConnectionPool = dict[
                str,
                int | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            RetryConfiguration: TypeAlias = dict[str, int | float | bool | list[str]]
            LoadBalancing: TypeAlias = dict[
                str,
                str | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            ClientMetrics = dict[
                str,
                int | float | dict[str, FlextTypes.ContainerValue | None],
            ]
            ChannelOptions = dict[
                str,
                str | int | bool | dict[str, FlextTypes.ContainerValue | None],
            ]

        class Streaming:
            """gRPC streaming complex types."""

            StreamConfiguration = dict[
                str,
                bool | int | str | dict[str, FlextTypes.ContainerValue | None],
            ]
            StreamingContext = dict[
                str,
                str | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            StreamMetrics = dict[
                str,
                int | float | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            FlowControl = dict[
                str,
                int | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            BackpressureHandling = dict[
                str,
                str | int | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            StreamingPipeline: TypeAlias = list[
                dict[str, str | FlextTypes.ContainerValue | None]
            ]

        class GrpcService:
            """gRPC service complex types."""

            ServiceDefinition = dict[
                str,
                str | list[str] | dict[str, FlextTypes.ContainerValue | None],
            ]
            MethodDefinition = dict[
                str,
                str | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            ServiceMetadata = dict[
                str,
                str | int | dict[str, FlextTypes.ContainerValue | None],
            ]
            InterceptorChain: TypeAlias = list[
                dict[str, str | FlextTypes.ContainerValue | None]
            ]
            ServiceDiscovery = dict[
                str,
                str | list[str] | dict[str, FlextTypes.ContainerValue | None],
            ]
            HealthCheck = dict[
                str,
                bool | str | int | dict[str, FlextTypes.ContainerValue | None],
            ]

        class Security:
            """gRPC security complex types."""

            SecurityConfiguration = dict[
                str,
                bool | str | dict[str, FlextTypes.ContainerValue | None],
            ]
            TlsConfiguration = dict[
                str,
                str | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            AuthenticationConfig: TypeAlias = dict[
                str,
                str | dict[str, FlextTypes.ContainerValue | None],
            ]
            AuthorizationRules: TypeAlias = list[dict[str, str | bool | list[str]]]
            CertificateManagement = dict[
                str,
                str | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            SecurityMetrics = dict[
                str,
                int | bool | dict[str, FlextTypes.ContainerValue | None],
            ]

        class Monitoring:
            """gRPC monitoring complex types."""

            MonitoringConfiguration = dict[
                str,
                bool | str | int | dict[str, FlextTypes.ContainerValue | None],
            ]
            MetricsCollection = dict[
                str,
                str | bool | dict[str, FlextTypes.ContainerValue | None],
            ]
            TracingConfiguration = dict[
                str,
                bool | str | dict[str, FlextTypes.ContainerValue | None],
            ]
            LoggingSetup = dict[
                str,
                str | bool | int | dict[str, FlextTypes.ContainerValue | None],
            ]
            AlertingRules: TypeAlias = list[dict[str, FlextTypes.Scalar]]
            PerformanceMetrics = dict[
                str,
                float | int | dict[str, FlextTypes.ContainerValue | None],
            ]

        class Project:
            """gRPC-specific project types.

            Adds gRPC/microservices-specific project types.
            Follows domain separation principle:
            gRPC domain owns microservices-specific types.
            """

            ProjectConfig = dict[str, FlextTypes.ContainerValue | None]
            MicroserviceConfig: TypeAlias = dict[str, str | int | bool | list[str]]
            StreamingConfig = dict[
                str,
                bool | str | dict[str, FlextTypes.ContainerValue | None],
            ]
            ServiceMeshConfig = dict[str, FlextTypes.ContainerValue | None]

        class GrpcValidation:
            """gRPC validation utilities."""

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

t = FlextGrpcTypes
__all__ = ["FlextGrpcTypes", "t"]

from typing import TypeAlias

GrpcNetworkConfig: TypeAlias = FlextGrpcModels.Grpc.NetworkConfig

GrpcSecurityConfig: TypeAlias = FlextGrpcModels.Grpc.SecurityConfig

GrpcPerformanceConfig: TypeAlias = FlextGrpcModels.Grpc.PerformanceConfig

GrpcStreamingConfig: TypeAlias = FlextGrpcModels.Grpc.StreamingConfig

GrpcClientConfig: TypeAlias = FlextGrpcModels.Grpc.ClientSettingsConfig

GrpcMonitoringConfig: TypeAlias = FlextGrpcModels.Grpc.MonitoringConfig
