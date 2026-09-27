"""FLEXT gRPC Proto Stub - client-side call primitives.

Provides the Pydantic-based client stub for gRPC calls, used by services.py
until full protobuf code generation is in place. Split from servicer.py
(ENFORCE-067: one top-level class per module).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc import c
from flext_grpc.models import FlextGrpcModels
from flext_grpc.protocols import FlextGrpcProtocols


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


__all__ = ["FlextGrpcServiceStub"]
