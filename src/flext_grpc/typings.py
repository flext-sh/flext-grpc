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
class _GrpcServicerProtocol(Protocol):
    """Protocol for gRPC service implementations (duck typing)."""


class FlextGrpcTypes(FlextTypes):
    """gRPC-specific type definitions extending t.

    Domain-specific type system for gRPC microservices operations.
    Contains ONLY complex gRPC-specific types, no simple aliases.
    Uses Python 3.13+ type syntax and patterns.
    """

    ConfigValue: TypeAlias = object
    GrpcOptions = dict[str, object]

    class Grpc:
        """gRPC-specific type namespace for domain aliases and validators."""

        GrpcServicer: TypeAlias = _GrpcServicerProtocol

        Dict: TypeAlias = dict[str, object]
        GrpcDict: TypeAlias = dict[str, object]
        Headers: TypeAlias = dict[str, str]
        Metadata: TypeAlias = dict[str, object]
        ConfigDict: TypeAlias = dict[str, str | int | bool | object]
        Address: TypeAlias = dict[str, str | int]
        Endpoint: TypeAlias = dict[str, str | int | bool]
        Connection: TypeAlias = dict[str, object]
        ServiceData: TypeAlias = dict[str, object]
        MethodData: TypeAlias = dict[str, object]
        RequestDict: TypeAlias = dict[str, object]
        ResponseDict: TypeAlias = dict[str, object]
        StreamData: TypeAlias = dict[str, object]
        StreamMeta: TypeAlias = dict[str, str | int | bool]
        Target = str
        StreamType = c.Grpc.StreamTypeLiteral
        ChannelState: TypeAlias = c.Grpc.ChannelStateLiteral
        ServerState: TypeAlias = c.Grpc.ServerStateLiteral
        Options: TypeAlias = dict[
            str,
            FlextTypes.Scalar | list[object] | dict[str, object] | None,
        ]

        class Server:
            """gRPC server complex types."""

            ServerConfiguration = dict[str, str | int | bool | dict[str, object]]
            ServerLifecycle = dict[str, str | bool | int | dict[str, object]]
            ServerMetrics = dict[str, int | float | bool | dict[str, object]]
            ServerSecurity = dict[str, bool | str | dict[str, object]]
            ServiceRegistry = dict[str, list[str] | dict[str, object]]
            HandlerConfiguration: TypeAlias = list[dict[str, str | object]]

        class Client:
            """gRPC client complex types."""

            ClientConfiguration = dict[str, str | int | bool | dict[str, object]]
            ConnectionPool = dict[str, int | bool | dict[str, object]]
            RetryConfiguration: TypeAlias = dict[str, int | float | bool | list[str]]
            LoadBalancing: TypeAlias = dict[str, str | bool | dict[str, object]]
            ClientMetrics = dict[str, int | float | dict[str, object]]
            ChannelOptions = dict[str, str | int | bool | dict[str, object]]

        class Streaming:
            """gRPC streaming complex types."""

            StreamConfiguration = dict[str, bool | int | str | dict[str, object]]
            StreamingContext = dict[str, str | bool | dict[str, object]]
            StreamMetrics = dict[str, int | float | bool | dict[str, object]]
            FlowControl = dict[str, int | bool | dict[str, object]]
            BackpressureHandling = dict[str, str | int | bool | dict[str, object]]
            StreamingPipeline: TypeAlias = list[dict[str, str | object]]

        class GrpcService:
            """gRPC service complex types."""

            ServiceDefinition = dict[str, str | list[str] | dict[str, object]]
            MethodDefinition = dict[str, str | bool | dict[str, object]]
            ServiceMetadata = dict[str, str | int | dict[str, object]]
            InterceptorChain: TypeAlias = list[dict[str, str | object]]
            ServiceDiscovery = dict[str, str | list[str] | dict[str, object]]
            HealthCheck = dict[str, bool | str | int | dict[str, object]]

        class Security:
            """gRPC security complex types."""

            SecurityConfiguration = dict[str, bool | str | dict[str, object]]
            TlsConfiguration = dict[str, str | bool | dict[str, object]]
            AuthenticationConfig: TypeAlias = dict[str, str | dict[str, object]]
            AuthorizationRules: TypeAlias = list[dict[str, str | bool | list[str]]]
            CertificateManagement = dict[str, str | bool | dict[str, object]]
            SecurityMetrics = dict[str, int | bool | dict[str, object]]

        class Monitoring:
            """gRPC monitoring complex types."""

            MonitoringConfiguration = dict[str, bool | str | int | dict[str, object]]
            MetricsCollection = dict[str, str | bool | dict[str, object]]
            TracingConfiguration = dict[str, bool | str | dict[str, object]]
            LoggingSetup = dict[str, str | bool | int | dict[str, object]]
            AlertingRules: TypeAlias = list[dict[str, FlextTypes.Scalar]]
            PerformanceMetrics = dict[str, float | int | dict[str, object]]

        class Project:
            """gRPC-specific project types.

            Adds gRPC/microservices-specific project types.
            Follows domain separation principle:
            gRPC domain owns microservices-specific types.
            """

            ProjectConfig = dict[str, object]
            MicroserviceConfig: TypeAlias = dict[str, str | int | bool | list[str]]
            StreamingConfig = dict[str, bool | str | dict[str, object]]
            ServiceMeshConfig = dict[str, object]

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
