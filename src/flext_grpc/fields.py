"""FLEXT gRPC Field Definitions.

This module provides field definitions and validators for gRPC entities,
following the flext-core pattern for consistent field validation across
the FLEXT ecosystem.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from pydantic import Field
from pydantic.fields import FieldInfo

from flext_grpc.constants import FlextGrpcConstants


# Host field validation
def grpc_host_field(
    default: str = FlextGrpcConstants.GRPC_DEFAULT_HOST,
    description: str = "gRPC server host address",
) -> FieldInfo:
    """Create a validated gRPC host field."""
    return Field(
        default=default,
        description=description,
        min_length=1,
        max_length=255,
        pattern=r"^[a-zA-Z0-9.-]+$",
    )


# Port field validation
def grpc_port_field(
    default: int = FlextGrpcConstants.GRPC_DEFAULT_PORT,
    description: str = "gRPC server port number",
) -> FieldInfo:
    """Create a validated gRPC port field."""
    return Field(
        default=default,
        description=description,
        ge=1024,
        le=65535,
    )


# Service name field validation
def grpc_service_name_field(
    description: str = "gRPC service name",
) -> FieldInfo:
    """Create a validated gRPC service name field."""
    return Field(
        description=description,
        min_length=1,
        max_length=100,
        pattern=r"^[a-zA-Z][a-zA-Z0-9_.]*[a-zA-Z0-9]$",
    )


# Method name field validation
def grpc_method_name_field(
    description: str = "gRPC method name",
) -> FieldInfo:
    """Create a validated gRPC method name field."""
    return Field(
        description=description,
        min_length=1,
        max_length=100,
        pattern=r"^[a-zA-Z][a-zA-Z0-9_]*$",
    )


# Timeout field validation
def grpc_timeout_field(
    default: float = FlextGrpcConstants.GRPC_DEFAULT_TIMEOUT,
    description: str = "gRPC operation timeout in seconds",
) -> FieldInfo:
    """Create a validated gRPC timeout field."""
    return Field(
        default=default,
        description=description,
        gt=0.0,
        le=3600.0,
    )


# Worker count field validation
def grpc_workers_field(
    default: int = 10,
    description: str = "Maximum number of gRPC worker threads",
) -> FieldInfo:
    """Create a validated gRPC workers field."""
    return Field(
        default=default,
        description=description,
        ge=1,
        le=1000,
    )
