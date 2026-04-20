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
from collections.abc import (
    Mapping,
    Sequence,
)
from typing import Literal

from flext_cli import t

from flext_grpc import p


class FlextGrpcTypes(t):
    """gRPC-specific type definitions extending t.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    class Grpc:
        """gRPC-specific type namespace for domain aliases and validators."""

        type EntityKind = Literal["server", "client", "channel", "service", "stream"]
        type GrpcServicer = p.Grpc.GrpcServicer

        type Headers = t.StrMapping
        type ConfigDict = Mapping[
            str,
            t.Scalar | t.ContainerValue | None,
        ]
        type Address = t.HeaderMapping
        type Endpoint = Mapping[str, t.Scalar]
        type StreamMeta = Mapping[str, t.Scalar]
        type Options = Mapping[
            str,
            t.Scalar
            | Sequence[t.ContainerValue | None]
            | t.OptionalContainerValueMapping
            | None,
        ]

        class Server:
            """gRPC server complex types."""

            ServerConfiguration = Mapping[
                str,
                t.Scalar | t.OptionalContainerValueMapping,
            ]
            ServerLifecycle = Mapping[
                str,
                str | bool | int | t.OptionalContainerValueMapping,
            ]
            ServerMetrics = Mapping[
                str,
                t.Numeric | bool | t.OptionalContainerValueMapping,
            ]
            ServerSecurity = Mapping[
                str,
                bool | str | t.OptionalContainerValueMapping,
            ]
            ServiceRegistry = Mapping[
                str,
                t.StrSequence | t.OptionalContainerValueMapping,
            ]
            type HandlerConfiguration = Sequence[t.OptionalContainerValueMapping]

        class Client:
            """gRPC client complex types."""

            ClientConfiguration = Mapping[
                str,
                t.Scalar | t.OptionalContainerValueMapping,
            ]
            ConnectionPool = Mapping[
                str,
                int | bool | t.OptionalContainerValueMapping,
            ]
            type RetryConfiguration = Mapping[
                str,
                t.Numeric | bool | t.StrSequence,
            ]
            type LoadBalancing = Mapping[
                str,
                str | bool | t.OptionalContainerValueMapping,
            ]
            ClientMetrics = Mapping[
                str,
                t.Numeric | t.OptionalContainerValueMapping,
            ]
            ChannelOptions = Mapping[
                str,
                t.Scalar | t.OptionalContainerValueMapping,
            ]

        class Streaming:
            """gRPC streaming complex types."""

            StreamConfiguration = Mapping[
                str,
                bool | int | str | t.OptionalContainerValueMapping,
            ]
            StreamingContext = Mapping[
                str,
                str | bool | t.OptionalContainerValueMapping,
            ]
            StreamMetrics = Mapping[
                str,
                t.Numeric | bool | t.OptionalContainerValueMapping,
            ]
            FlowControl = Mapping[
                str,
                int | bool | t.OptionalContainerValueMapping,
            ]
            BackpressureHandling = Mapping[
                str,
                t.Scalar | t.OptionalContainerValueMapping,
            ]
            type StreamingPipeline = Sequence[t.OptionalContainerValueMapping]

        class GrpcService:
            """gRPC service complex types."""

            ServiceDefinition = Mapping[
                str,
                str | t.StrSequence | t.OptionalContainerValueMapping,
            ]
            MethodDefinition = Mapping[
                str,
                str | bool | t.OptionalContainerValueMapping,
            ]
            ServiceMetadata = Mapping[
                str,
                str | int | t.OptionalContainerValueMapping,
            ]
            type InterceptorChain = Sequence[t.OptionalContainerValueMapping]
            ServiceDiscovery = Mapping[
                str,
                str | t.StrSequence | t.OptionalContainerValueMapping,
            ]
            HealthCheck = Mapping[
                str,
                bool | str | int | t.OptionalContainerValueMapping,
            ]

        class Security:
            """gRPC security complex types."""

            SecurityConfiguration = Mapping[
                str,
                bool | str | t.OptionalContainerValueMapping,
            ]
            TlsConfiguration = Mapping[
                str,
                str | bool | t.OptionalContainerValueMapping,
            ]
            type AuthenticationConfig = Mapping[
                str,
                str | t.OptionalContainerValueMapping,
            ]
            type AuthorizationRules = Sequence[Mapping[str, str | bool | t.StrSequence]]
            CertificateManagement = Mapping[
                str,
                str | bool | t.OptionalContainerValueMapping,
            ]
            SecurityMetrics = Mapping[
                str,
                int | bool | t.OptionalContainerValueMapping,
            ]

        class Monitoring:
            """gRPC monitoring complex types."""

            MonitoringConfiguration = Mapping[
                str,
                bool | str | int | t.OptionalContainerValueMapping,
            ]
            MetricsCollection = Mapping[
                str,
                str | bool | t.OptionalContainerValueMapping,
            ]
            TracingConfiguration = Mapping[
                str,
                bool | str | t.OptionalContainerValueMapping,
            ]
            LoggingSetup = Mapping[
                str,
                str | bool | int | t.OptionalContainerValueMapping,
            ]
            type AlertingRules = Sequence[Mapping[str, t.Scalar]]
            PerformanceMetrics = Mapping[
                str,
                float | int | t.OptionalContainerValueMapping,
            ]

        class Project:
            """gRPC-specific project types.

            Adds gRPC/microservices-specific project types.
            Follows domain separation principle:
            gRPC domain owns microservices-specific types.
            """

            ProjectConfig = t.OptionalContainerValueMapping
            type MicroserviceConfig = Mapping[
                str,
                t.Scalar | t.StrSequence,
            ]
            StreamingConfig = Mapping[
                str,
                bool | str | t.OptionalContainerValueMapping,
            ]
            ServiceMeshConfig = t.OptionalContainerValueMapping

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
__all__: list[str] = ["FlextGrpcTypes", "t"]
