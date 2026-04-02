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
from flext_grpc import FlextGrpcProtocols


class FlextGrpcTypes(FlextTypes):
    """gRPC-specific type definitions extending t.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Grpc:
        """gRPC-specific type namespace for domain aliases and validators."""

        type GrpcServicer = FlextGrpcProtocols.Grpc.GrpcServicer

        type Headers = FlextTypes.StrMapping
        type ConfigDict = Mapping[
            str,
            FlextTypes.Scalar | FlextTypes.ContainerValue | None,
        ]
        type Address = FlextTypes.HeaderMapping
        type Endpoint = Mapping[str, FlextTypes.Scalar]
        type StreamMeta = Mapping[str, FlextTypes.Scalar]
        type Options = Mapping[
            str,
            FlextTypes.Scalar
            | Sequence[FlextTypes.ContainerValue | None]
            | FlextTypes.OptionalContainerValueMapping
            | None,
        ]

        class Server:
            """gRPC server complex types."""

            ServerConfiguration = Mapping[
                str,
                FlextTypes.Scalar | FlextTypes.OptionalContainerValueMapping,
            ]
            ServerLifecycle = Mapping[
                str,
                str | bool | int | FlextTypes.OptionalContainerValueMapping,
            ]
            ServerMetrics = Mapping[
                str,
                FlextTypes.Numeric | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            ServerSecurity = Mapping[
                str,
                bool | str | FlextTypes.OptionalContainerValueMapping,
            ]
            ServiceRegistry = Mapping[
                str,
                FlextTypes.StrSequence | FlextTypes.OptionalContainerValueMapping,
            ]
            type HandlerConfiguration = Sequence[
                FlextTypes.OptionalContainerValueMapping
            ]

        class Client:
            """gRPC client complex types."""

            ClientConfiguration = Mapping[
                str,
                FlextTypes.Scalar | FlextTypes.OptionalContainerValueMapping,
            ]
            ConnectionPool = Mapping[
                str,
                int | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            type RetryConfiguration = Mapping[
                str,
                FlextTypes.Numeric | bool | FlextTypes.StrSequence,
            ]
            type LoadBalancing = Mapping[
                str,
                str | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            ClientMetrics = Mapping[
                str,
                FlextTypes.Numeric | FlextTypes.OptionalContainerValueMapping,
            ]
            ChannelOptions = Mapping[
                str,
                FlextTypes.Scalar | FlextTypes.OptionalContainerValueMapping,
            ]

        class Streaming:
            """gRPC streaming complex types."""

            StreamConfiguration = Mapping[
                str,
                bool | int | str | FlextTypes.OptionalContainerValueMapping,
            ]
            StreamingContext = Mapping[
                str,
                str | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            StreamMetrics = Mapping[
                str,
                FlextTypes.Numeric | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            FlowControl = Mapping[
                str,
                int | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            BackpressureHandling = Mapping[
                str,
                FlextTypes.Scalar | FlextTypes.OptionalContainerValueMapping,
            ]
            type StreamingPipeline = Sequence[FlextTypes.OptionalContainerValueMapping]

        class GrpcService:
            """gRPC service complex types."""

            ServiceDefinition = Mapping[
                str,
                str | FlextTypes.StrSequence | FlextTypes.OptionalContainerValueMapping,
            ]
            MethodDefinition = Mapping[
                str,
                str | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            ServiceMetadata = Mapping[
                str,
                str | int | FlextTypes.OptionalContainerValueMapping,
            ]
            type InterceptorChain = Sequence[FlextTypes.OptionalContainerValueMapping]
            ServiceDiscovery = Mapping[
                str,
                str | FlextTypes.StrSequence | FlextTypes.OptionalContainerValueMapping,
            ]
            HealthCheck = Mapping[
                str,
                bool | str | int | FlextTypes.OptionalContainerValueMapping,
            ]

        class Security:
            """gRPC security complex types."""

            SecurityConfiguration = Mapping[
                str,
                bool | str | FlextTypes.OptionalContainerValueMapping,
            ]
            TlsConfiguration = Mapping[
                str,
                str | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            type AuthenticationConfig = Mapping[
                str,
                str | FlextTypes.OptionalContainerValueMapping,
            ]
            type AuthorizationRules = Sequence[
                Mapping[str, str | bool | FlextTypes.StrSequence]
            ]
            CertificateManagement = Mapping[
                str,
                str | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            SecurityMetrics = Mapping[
                str,
                int | bool | FlextTypes.OptionalContainerValueMapping,
            ]

        class Monitoring:
            """gRPC monitoring complex types."""

            MonitoringConfiguration = Mapping[
                str,
                bool | str | int | FlextTypes.OptionalContainerValueMapping,
            ]
            MetricsCollection = Mapping[
                str,
                str | bool | FlextTypes.OptionalContainerValueMapping,
            ]
            TracingConfiguration = Mapping[
                str,
                bool | str | FlextTypes.OptionalContainerValueMapping,
            ]
            LoggingSetup = Mapping[
                str,
                str | bool | int | FlextTypes.OptionalContainerValueMapping,
            ]
            type AlertingRules = Sequence[Mapping[str, FlextTypes.Scalar]]
            PerformanceMetrics = Mapping[
                str,
                float | int | FlextTypes.OptionalContainerValueMapping,
            ]

        class Project:
            """gRPC-specific project types.

            Adds gRPC/microservices-specific project types.
            Follows domain separation principle:
            gRPC domain owns microservices-specific types.
            """

            ProjectConfig = FlextTypes.OptionalContainerValueMapping
            type MicroserviceConfig = Mapping[
                str,
                FlextTypes.Scalar | FlextTypes.StrSequence,
            ]
            StreamingConfig = Mapping[
                str,
                bool | str | FlextTypes.OptionalContainerValueMapping,
            ]
            ServiceMeshConfig = FlextTypes.OptionalContainerValueMapping

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
