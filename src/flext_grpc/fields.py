"""FLEXT gRPC Field Definitions - Namespace Class Pattern.

This module provides field definitions and validators for gRPC entities,
following the flext-core pattern for consistent field validation across
the FLEXT ecosystem. Uses namespace class pattern with nested field creators.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import cast

from pydantic import Field
from pydantic.fields import FieldInfo

from flext_grpc.constants import FlextGrpcConstants


class FlextGrpcFields:
    """Namespace class for gRPC field definitions and validators.

    Provides nested classes for different types of field validations
    used throughout the gRPC domain. Follows FLEXT namespace pattern
    for consistent field validation across the ecosystem.
    """

    class NetworkFields:
        """Network-related field validators for gRPC entities."""

        @staticmethod
        def host_field(
            default: str = FlextGrpcConstants.GRPC_DEFAULT_HOST,
            description: str = "gRPC server host address",
        ) -> FieldInfo:
            """Create a validated gRPC host field."""
            return cast(
                "FieldInfo",
                Field(
                    default=default,
                    description=description,
                    min_length=1,
                    max_length=255,
                    pattern=r"^[a-zA-Z0-9.-]+$",
                ),
            )

        @staticmethod
        def port_field(
            default: int = FlextGrpcConstants.GRPC_DEFAULT_PORT,
            description: str = "gRPC server port number",
        ) -> FieldInfo:
            """Create a validated gRPC port field."""
            return cast(
                "FieldInfo",
                Field(
                    default=default,
                    description=description,
                    ge=1024,
                    le=65535,
                ),
            )

    class ServiceFields:
        """Service-related field validators for gRPC entities."""

        @staticmethod
        def service_name_field(
            description: str = "gRPC service name",
        ) -> FieldInfo:
            """Create a validated gRPC service name field."""
            return cast(
                "FieldInfo",
                Field(
                    description=description,
                    min_length=1,
                    max_length=100,
                    pattern=r"^[a-zA-Z][a-zA-Z0-9_.]*[a-zA-Z0-9]$",
                ),
            )

        @staticmethod
        def method_name_field(
            description: str = "gRPC method name",
        ) -> FieldInfo:
            """Create a validated gRPC method name field."""
            return cast(
                "FieldInfo",
                Field(
                    description=description,
                    min_length=1,
                    max_length=100,
                    pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$",
                ),
            )

    class PerformanceFields:
        """Performance-related field validators for gRPC entities."""

        @staticmethod
        def timeout_field(
            default: float = FlextGrpcConstants.GRPC_DEFAULT_TIMEOUT,
            description: str = "gRPC operation timeout in seconds",
        ) -> FieldInfo:
            """Create a validated gRPC timeout field."""
            return cast(
                "FieldInfo",
                Field(
                    default=default,
                    description=description,
                    gt=0.0,
                    le=3600.0,
                ),
            )

        @staticmethod
        def workers_field(
            default: int = 10,
            description: str = "Maximum number of gRPC worker threads",
        ) -> FieldInfo:
            """Create a validated gRPC workers field."""
            return cast(
                "FieldInfo",
                Field(
                    default=default,
                    description=description,
                    ge=1,
                    le=1000,
                ),
            )


# Backward compatibility aliases for existing code
grpc_host_field = FlextGrpcFields.NetworkFields.host_field
grpc_port_field = FlextGrpcFields.NetworkFields.port_field
grpc_service_name_field = FlextGrpcFields.ServiceFields.service_name_field
grpc_method_name_field = FlextGrpcFields.ServiceFields.method_name_field
grpc_timeout_field = FlextGrpcFields.PerformanceFields.timeout_field
grpc_workers_field = FlextGrpcFields.PerformanceFields.workers_field

__all__ = [
    "FlextGrpcFields",
    # Backward compatibility aliases
    "grpc_host_field",
    "grpc_method_name_field",
    "grpc_port_field",
    "grpc_service_name_field",
    "grpc_timeout_field",
    "grpc_workers_field",
]
