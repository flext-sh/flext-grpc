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
            t.Scalar | t.JsonValue | None,
        ]
        type Address = t.HeaderMapping
        type Endpoint = Mapping[str, t.Scalar]
        type StreamMeta = Mapping[str, t.Scalar]
        type Options = Mapping[
            str,
            t.Scalar | Sequence[t.JsonValue | None] | t.JsonMapping | None,
        ]

        class Server:
            """gRPC server complex types."""

            ServerConfiguration = Mapping[
                str,
                t.Scalar | t.JsonMapping | None,
            ]
            ServerLifecycle = Mapping[
                str,
                str | bool | int | t.JsonMapping | None,
            ]
            ServerMetrics = Mapping[
                str,
                t.Numeric | bool | t.JsonMapping | None,
            ]
            ServerSecurity = Mapping[
                str,
                bool | str | t.JsonMapping | None,
            ]
            ServiceRegistry = Mapping[
                str,
                t.StrSequence | t.JsonMapping | None,
            ]
            type HandlerConfiguration = Sequence[t.JsonMapping | None]

        class Client:
            """gRPC client complex types."""

            ClientConfiguration = Mapping[
                str,
                t.Scalar | t.JsonMapping | None,
            ]
            ConnectionPool = Mapping[
                str,
                int | bool | t.JsonMapping | None,
            ]
            type RetryConfiguration = Mapping[
                str,
                t.Numeric | bool | t.StrSequence,
            ]
            type LoadBalancing = Mapping[
                str,
                str | bool | t.JsonMapping | None,
            ]
            ClientMetrics = Mapping[
                str,
                t.Numeric | t.JsonMapping | None,
            ]
            ChannelOptions = Mapping[
                str,
                t.Scalar | t.JsonMapping | None,
            ]

        class Streaming:
            """gRPC streaming complex types."""

            StreamConfiguration = Mapping[
                str,
                bool | int | str | t.JsonMapping | None,
            ]
            StreamingContext = Mapping[
                str,
                str | bool | t.JsonMapping | None,
            ]
            StreamMetrics = Mapping[
                str,
                t.Numeric | bool | t.JsonMapping | None,
            ]
            FlowControl = Mapping[
                str,
                int | bool | t.JsonMapping | None,
            ]
            BackpressureHandling = Mapping[
                str,
                t.Scalar | t.JsonMapping | None,
            ]
            type StreamingPipeline = Sequence[t.JsonMapping | None]

        class GrpcService:
            """gRPC service complex types."""

            ServiceDefinition = Mapping[
                str,
                str | t.StrSequence | t.JsonMapping | None,
            ]
            MethodDefinition = Mapping[
                str,
                str | bool | t.JsonMapping | None,
            ]
            ServiceMetadata = Mapping[
                str,
                str | int | t.JsonMapping | None,
            ]
            type InterceptorChain = Sequence[t.JsonMapping | None]
            ServiceDiscovery = Mapping[
                str,
                str | t.StrSequence | t.JsonMapping | None,
            ]
            HealthCheck = Mapping[
                str,
                bool | str | int | t.JsonMapping | None,
            ]

        class Security:
            """gRPC security complex types."""

            SecurityConfiguration = Mapping[
                str,
                bool | str | t.JsonMapping | None,
            ]
            TlsConfiguration = Mapping[
                str,
                str | bool | t.JsonMapping | None,
            ]
            type AuthenticationConfig = Mapping[
                str,
                str | t.JsonMapping | None,
            ]
            type AuthorizationRules = Sequence[Mapping[str, str | bool | t.StrSequence]]
            CertificateManagement = Mapping[
                str,
                str | bool | t.JsonMapping | None,
            ]
            SecurityMetrics = Mapping[
                str,
                int | bool | t.JsonMapping | None,
            ]

        class Monitoring:
            """gRPC monitoring complex types."""

            MonitoringConfiguration = Mapping[
                str,
                bool | str | int | t.JsonMapping | None,
            ]
            MetricsCollection = Mapping[
                str,
                str | bool | t.JsonMapping | None,
            ]
            TracingConfiguration = Mapping[
                str,
                bool | str | t.JsonMapping | None,
            ]
            LoggingSetup = Mapping[
                str,
                str | bool | int | t.JsonMapping | None,
            ]
            type AlertingRules = Sequence[Mapping[str, t.Scalar]]
            PerformanceMetrics = Mapping[
                str,
                float | int | t.JsonMapping | None,
            ]

        class Project:
            """gRPC-specific project types.

            Adds gRPC/microservices-specific project types.
            Follows domain separation principle:
            gRPC domain owns microservices-specific types.
            """

            ProjectConfig = t.JsonMapping | None
            type MicroserviceConfig = Mapping[
                str,
                t.Scalar | t.StrSequence,
            ]
            StreamingConfig = Mapping[
                str,
                bool | str | t.JsonMapping | None,
            ]
            ServiceMeshConfig = t.JsonMapping | None

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
