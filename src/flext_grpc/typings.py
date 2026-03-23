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
from collections.abc import Mapping, Sequence

from flext_core import FlextTypes

from flext_grpc import FlextGrpcProtocols, c


class FlextGrpcTypes(FlextTypes):
    """gRPC-specific type definitions extending t.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    type ConfigValue = FlextTypes.ContainerValue | None
    GrpcOptions = Mapping[str, FlextTypes.ContainerValue | None]

    class Grpc:
        """gRPC-specific type namespace for domain aliases and validators."""

        type GrpcServicer = FlextGrpcProtocols.Grpc.GrpcServicer

        type Dict = Mapping[str, FlextTypes.ContainerValue | None]
        type GrpcDict = dict[str, FlextTypes.ContainerValue | None]
        type Headers = Mapping[str, str]
        type Metadata = Mapping[str, FlextTypes.ContainerValue | None]
        type ConfigDict = Mapping[
            str,
            str | int | bool | FlextTypes.ContainerValue | None,
        ]
        type Address = Mapping[str, str | int]
        type Endpoint = Mapping[str, str | int | bool]
        type Connection = Mapping[str, FlextTypes.ContainerValue | None]
        type ServiceData = Mapping[str, FlextTypes.ContainerValue | None]
        type MethodData = Mapping[str, FlextTypes.ContainerValue | None]
        type RequestDict = Mapping[str, FlextTypes.ContainerValue | None]
        type ResponseDict = Mapping[str, FlextTypes.ContainerValue | None]
        type StreamData = Mapping[str, FlextTypes.ContainerValue | None]
        type StreamMeta = Mapping[str, str | int | bool]
        Target = str
        StreamType = c.Grpc.StreamTypeLiteral
        type ChannelState = c.Grpc.ChannelStateLiteral
        type ServerState = c.Grpc.ServerStateLiteral
        type Options = Mapping[
            str,
            FlextTypes.Scalar
            | Sequence[FlextTypes.ContainerValue | None]
            | Mapping[str, FlextTypes.ContainerValue | None]
            | None,
        ]

        class Server:
            """gRPC server complex types."""

            ServerConfiguration = Mapping[
                str,
                str | int | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ServerLifecycle = Mapping[
                str,
                str | bool | int | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ServerMetrics = Mapping[
                str,
                int | float | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ServerSecurity = Mapping[
                str,
                bool | str | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ServiceRegistry = Mapping[
                str,
                Sequence[str] | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            type HandlerConfiguration = Sequence[
                Mapping[str, str | FlextTypes.ContainerValue | None]
            ]

        class Client:
            """gRPC client complex types."""

            ClientConfiguration = Mapping[
                str,
                str | int | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ConnectionPool = Mapping[
                str,
                int | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            type RetryConfiguration = Mapping[str, int | float | bool | Sequence[str]]
            type LoadBalancing = Mapping[
                str,
                str | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ClientMetrics = Mapping[
                str,
                int | float | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ChannelOptions = Mapping[
                str,
                str | int | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]

        class Streaming:
            """gRPC streaming complex types."""

            StreamConfiguration = Mapping[
                str,
                bool | int | str | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            StreamingContext = Mapping[
                str,
                str | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            StreamMetrics = Mapping[
                str,
                int | float | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            FlowControl = Mapping[
                str,
                int | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            BackpressureHandling = Mapping[
                str,
                str | int | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            type StreamingPipeline = Sequence[
                Mapping[str, str | FlextTypes.ContainerValue | None]
            ]

        class GrpcService:
            """gRPC service complex types."""

            ServiceDefinition = Mapping[
                str,
                str | Sequence[str] | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            MethodDefinition = Mapping[
                str,
                str | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ServiceMetadata = Mapping[
                str,
                str | int | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            type InterceptorChain = Sequence[
                Mapping[str, str | FlextTypes.ContainerValue | None]
            ]
            ServiceDiscovery = Mapping[
                str,
                str | Sequence[str] | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            HealthCheck = Mapping[
                str,
                bool | str | int | Mapping[str, FlextTypes.ContainerValue | None],
            ]

        class Security:
            """gRPC security complex types."""

            SecurityConfiguration = Mapping[
                str,
                bool | str | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            TlsConfiguration = Mapping[
                str,
                str | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            type AuthenticationConfig = Mapping[
                str,
                str | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            type AuthorizationRules = Sequence[Mapping[str, str | bool | Sequence[str]]]
            CertificateManagement = Mapping[
                str,
                str | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            SecurityMetrics = Mapping[
                str,
                int | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]

        class Monitoring:
            """gRPC monitoring complex types."""

            MonitoringConfiguration = Mapping[
                str,
                bool | str | int | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            MetricsCollection = Mapping[
                str,
                str | bool | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            TracingConfiguration = Mapping[
                str,
                bool | str | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            LoggingSetup = Mapping[
                str,
                str | bool | int | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            type AlertingRules = Sequence[Mapping[str, FlextTypes.Scalar]]
            PerformanceMetrics = Mapping[
                str,
                float | int | Mapping[str, FlextTypes.ContainerValue | None],
            ]

        class Project:
            """gRPC-specific project types.

            Adds gRPC/microservices-specific project types.
            Follows domain separation principle:
            gRPC domain owns microservices-specific types.
            """

            ProjectConfig = Mapping[str, FlextTypes.ContainerValue | None]
            type MicroserviceConfig = Mapping[str, str | int | bool | Sequence[str]]
            StreamingConfig = Mapping[
                str,
                bool | str | Mapping[str, FlextTypes.ContainerValue | None],
            ]
            ServiceMeshConfig = Mapping[str, FlextTypes.ContainerValue | None]

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
