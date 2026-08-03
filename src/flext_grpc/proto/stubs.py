"""FLEXT gRPC Proto Stubs - Service definitions and message types.

Provides Pydantic-based message types and service stubs for gRPC operations.
These are used by services.py until full protobuf code generation is in place.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_grpc import c
from flext_grpc.models import FlextGrpcModels
from flext_grpc.protocols import FlextGrpcProtocols


class FlextGrpcServiceServicer:
    """Base class for gRPC service implementations."""

    pass


class FlextGrpcServiceStub:
    """gRPC service stub for client calls."""

    def __init__(self, channel: FlextGrpcProtocols.Grpc.GrpcChannel) -> None:
        """Initialize stub with channel."""
        self.channel = channel

    def echo(
        self, request: FlextGrpcModels.Grpc.EchoRequest
    ) -> FlextGrpcModels.Grpc.EchoResponse:
        """Echo RPC method."""
        return FlextGrpcModels.Grpc.EchoResponse(message=request.message, server_id="")

    def health_check(
        self, request: FlextGrpcModels.Grpc.HealthRequest
    ) -> FlextGrpcModels.Grpc.HealthResponse:
        """Health check RPC method."""
        return FlextGrpcModels.Grpc.HealthResponse(
            status=c.HealthStatus.HEALTHY.value, message=request.service
        )


def add_flext_grpc_service_servicer_to_server(
    servicer: FlextGrpcProtocols.Grpc.GrpcServicer,
    server: FlextGrpcProtocols.Grpc.GrpcServer,
) -> None:
    """Add gRPC service servicer to server."""
    pass


__all__ = [
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "add_flext_grpc_service_servicer_to_server",
]
