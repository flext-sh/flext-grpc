"""FLEXT gRPC Real Servicer.

Real gRPC service implementation for FLEXT.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from collections.abc import Iterator
from typing import override

import grpc
from flext_core.constants import FlextConstants

# Import protobuf classes - these are dynamically generated
from grpc import ServicerContext

from flext_core import FlextTypes
from flext_grpc.proto.flext_grpc_pb2 import (
    EchoRequest,
    EchoResponse,
    HealthRequest,
    HealthResponse,
    StreamRequest,
    StreamResponse,
)
from flext_grpc.proto.flext_grpc_pb2_grpc import (
    FlextGrpcServiceServicer,
)


class FlextGrpcRealServicer(FlextGrpcServiceServicer):
    """Real gRPC service implementation for FLEXT.

    Provides actual gRPC service handlers for:
    - Unary calls (Echo)
    - Server streaming
    - Client streaming
    - Bidirectional streaming
    - Health checks
    """

    @override
    def __init__(self, server_id: str = "flext-grpc-server") -> None:
        """Initialize the real servicer."""
        self.server_id = server_id
        self.start_time = time.time()

    @override
    def Echo(self, request: EchoRequest, context: ServicerContext) -> EchoResponse:
        """Real unary Echo implementation."""
        try:
            # Process the actual request
            response_message = f"Echo: {request.message}"

            # Add metadata from request if present
            if hasattr(request, "metadata") and request.metadata:
                metadata_str = ", ".join(
                    f"{k}={v}" for k, v in request.metadata.items()
                )
                response_message += f" (metadata: {metadata_str})"

            # Create real response
            return EchoResponse(
                message=response_message,
                server_id=self.server_id,
                timestamp=int(time.time() * 1000),  # milliseconds since epoch
            )

        except Exception as e:
            context.set_code(internal.invalid)
            context.set_details(f"Echo service error: {e}")
            return EchoResponse()

    @override
    def ServerStream(
        self,
        request: StreamRequest,
        context: ServicerContext,
    ) -> Iterator[StreamResponse]:
        """Real server streaming implementation."""
        try:
            # Generate multiple responses for streaming
            for i in range(5):  # Send 5 responses
                if context.is_active():
                    yield StreamResponse(
                        data=f"Server stream {i + 1}: {request.data}",
                        sequence=i + 1,
                        server_id=self.server_id,
                        timestamp=int(time.time() * 1000),
                    )
                    time.sleep(0.1)  # Small delay to simulate processing
                else:
                    break

        except Exception as e:
            context.set_code(internal.invalid)
            context.set_details(f"Server streaming error: {e}")

    @override
    def ClientStream(
        self,
        request_iterator: Iterator[StreamRequest],
        context: ServicerContext,
    ) -> StreamResponse:
        """Real client streaming implementation."""
        try:
            messages: FlextTypes.StringList = []
            sequence_count = FlextConstants.Performance.MIN_CURRENT_STEP

            # Process all incoming requests
            for request in request_iterator:
                messages.append(request.data)
                sequence_count += 1

            # Return aggregated response
            combined_data: str = " | ".join(messages)
            return StreamResponse(
                data=f"Received {sequence_count} messages: {combined_data}",
                sequence=sequence_count,
                server_id=self.server_id,
                timestamp=int(time.time() * 1000),
            )

        except Exception as e:
            context.set_code(internal.invalid)
            context.set_details(f"Client streaming error: {e}")
            return StreamResponse()

    @override
    def BidirectionalStream(
        self,
        request_iterator: Iterator[StreamRequest],
        context: ServicerContext,
    ) -> Iterator[StreamResponse]:
        """Real bidirectional streaming implementation."""
        try:
            # Process each request and yield responses
            for request in request_iterator:
                if context.is_active():
                    yield StreamResponse(
                        data=f"Bidirectional echo {request.sequence}: {request.data}",
                        sequence=request.sequence,
                        server_id=self.server_id,
                        timestamp=int(time.time() * 1000),
                    )
                else:
                    break

        except Exception as e:
            context.set_code(internal.invalid)
            context.set_details(f"Bidirectional streaming error: {e}")

    @override
    def HealthCheck(
        self,
        request: HealthRequest,
        context: ServicerContext,
    ) -> HealthResponse:
        """Real health check implementation."""
        try:
            # Check server health
            uptime = time.time() - self.start_time

            if request.service and request.service != "FlextGrpcService":
                return HealthResponse(
                    status=HealthResponse.ServingStatus.SERVICE_UNKNOWN,
                    message=f"Unknown service: {request.service}",
                )

            # Server is healthy if uptime > 0
            if uptime > 0:
                return HealthResponse(
                    status=HealthResponse.ServingStatus.SERVING,
                    message=f"Service healthy, uptime: {uptime:.2f}s",
                )
            return HealthResponse(
                status=HealthResponse.ServingStatus.NOT_SERVING,
                message="Service not ready",
            )

        except Exception as e:
            context.set_code(internal.invalid)
            context.set_details(f"Health check error: {e}")
            return HealthResponse(
                status=HealthResponse.ServingStatus.UNKNOWN,
                message=f"Health check failed: {e}",
            )


def create_real_servicer(server_id: str | None = None) -> FlextGrpcRealServicer:
    """Factory function to create a real gRPC servicer.

    Args:
        server_id: Optional server identifier

    Returns:
        Configured real servicer instance

    """
    if server_id is None:
        server_id = f"flext-server-{int(time.time())}"

    return FlextGrpcRealServicer(server_id)
