"""FLEXT gRPC Platform - Unified gRPC communication platform.

Platform class providing unified access to gRPC communication services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import FlextResult, get_flext_container

from flext_grpc.entities import (
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcStream,
)
from flext_grpc.services import FlextGrpcPlatformService


class FlextGrpcPlatform:
    """Platform for gRPC communication operations using global container."""

    def __init__(self, config: dict[str, object] | None = None) -> None:
        """Initialize gRPC platform.

        Args:
            config: Platform configuration

        """
        self.config = config or {}
        self.container = get_flext_container()
        self._setup_services()

    def _setup_services(self) -> None:
        """Set up platform services using unified service."""
        # Register unified service in global container
        service_result = self.container.get("flext_grpc_service")
        if service_result.is_failure:
            self.container.register("flext_grpc_service", FlextGrpcPlatformService())

    @property
    def service(self) -> FlextGrpcPlatformService:
        """Get unified gRPC service."""
        result = self.container.get("flext_grpc_service")
        if result.is_failure:
            service = FlextGrpcPlatformService()
            self.container.register("flext_grpc_service", service)
            return service

        # Safe cast since we registered it as FlextGrpcPlatformService
        if isinstance(result.data, FlextGrpcPlatformService):
            return result.data
        # Fallback: create new service if wrong type
        service = FlextGrpcPlatformService()
        self.container.register("flext_grpc_service", service)
        return service

    def server_operation(
        self,
        operation: str,
        server: FlextGrpcServer,
        **options: object,
    ) -> FlextResult[object]:
        """Execute server operation."""
        return self.service.execute_operation("server", operation, server, **options)

    def client_operation(
        self,
        operation: str,
        client: FlextGrpcClient,
        **options: object,
    ) -> FlextResult[object]:
        """Execute client operation."""
        return self.service.execute_operation("client", operation, client, **options)

    def stream_operation(
        self,
        operation: str,
        **options: object,
    ) -> FlextResult[object]:
        """Execute stream operation."""
        return self.service.execute_operation("stream", operation, **options)

    # Convenience methods for common operations
    def start_server(
        self,
        server: FlextGrpcServer,
        **options: object,
    ) -> FlextResult[FlextGrpcServer]:
        """Start a gRPC server."""
        result = self.server_operation("start", server, **options)
        if result.is_failure:
            return FlextResult[None].fail(result.error or "Start server failed")
        # Safe cast since we know server operations return FlextGrpcServer
        if isinstance(result.data, FlextGrpcServer):
            return FlextResult[None].ok(result.data)
        return FlextResult[None].fail("Invalid server result type")

    def stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop a gRPC server."""
        result = self.server_operation("stop", server)
        if result.is_failure:
            return FlextResult[None].fail(result.error or "Stop server failed")
        # Safe cast since we know server operations return FlextGrpcServer
        if isinstance(result.data, FlextGrpcServer):
            return FlextResult[None].ok(result.data)
        return FlextResult[None].fail("Invalid server result type")

    def connect_client(self, client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
        """Connect a gRPC client."""
        result = self.client_operation("connect", client)
        if result.is_failure:
            return FlextResult[None].fail(result.error or "Connect client failed")
        # Safe cast since we know client operations return FlextGrpcClient
        if isinstance(result.data, FlextGrpcClient):
            return FlextResult[None].ok(result.data)
        return FlextResult[None].fail("Invalid client result type")

    def make_call(
        self,
        client: FlextGrpcClient,
        method_name: str,
        request_data: object,
        **options: object,
    ) -> FlextResult[object]:
        """Make a gRPC call."""
        return self.client_operation(
            "call",
            client,
            method_name=method_name,
            request_data=request_data,
            **options,
        )

    def get_server_status(
        self,
        server: FlextGrpcServer,
    ) -> FlextResult[dict[str, object]]:
        """Get server status."""
        result = self.server_operation("status", server)
        if result.is_failure:
            return FlextResult[None].fail(result.error or "Get server status failed")
        # Safe cast since we know status operations return dict
        if isinstance(result.data, dict):
            return FlextResult[None].ok(result.data)
        return FlextResult[None].fail("Invalid status result type")

    def get_client_status(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[dict[str, object]]:
        """Get client status."""
        result = self.client_operation("status", client)
        if result.is_failure:
            return FlextResult[None].fail(result.error or "Get client status failed")
        # Safe cast since we know status operations return dict
        if isinstance(result.data, dict):
            return FlextResult[None].ok(result.data)
        return FlextResult[None].fail("Invalid status result type")

    def create_stream(
        self,
        client: FlextGrpcClient,
        method_name: str,
        stream_type: str = "unary",
        **options: object,
    ) -> FlextResult[FlextGrpcStream]:
        """Create a gRPC stream."""
        result = self.stream_operation(
            "create",
            client=client,
            method_name=method_name,
            stream_type=stream_type,
            **options,
        )
        if result.is_failure:
            return FlextResult[None].fail(result.error or "Create stream failed")
        # Safe cast since we know stream operations return FlextGrpcStream
        if isinstance(result.data, FlextGrpcStream):
            return FlextResult[None].ok(result.data)
        return FlextResult[None].fail("Invalid stream result type")
