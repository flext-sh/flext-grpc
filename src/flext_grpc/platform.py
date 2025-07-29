"""FLEXT gRPC Platform - Unified gRPC communication platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Platform class providing unified access to gRPC communication services.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextResult, get_flext_container

from flext_grpc.services import FlextGrpcService

if TYPE_CHECKING:
    from flext_grpc.entities import (
        FlextGrpcClient,
        FlextGrpcServer,
        FlextGrpcStream,
    )


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
            self.container.register("flext_grpc_service", FlextGrpcService())

    @property
    def service(self) -> FlextGrpcService:
        """Get unified gRPC service."""
        result = self.container.get("flext_grpc_service")
        if result.is_failure:
            service = FlextGrpcService()
            self.container.register("flext_grpc_service", service)
            return service
        return result.data

    def server_operation(
        self,
        operation: str,
        server: FlextGrpcServer,
        **options: object,
    ) -> FlextResult[object]:
        """Execute server operation."""
        return self.service.execute("server", operation, server, **options)

    def client_operation(
        self,
        operation: str,
        client: FlextGrpcClient,
        **options: object,
    ) -> FlextResult[object]:
        """Execute client operation."""
        return self.service.execute("client", operation, client, **options)

    def stream_operation(
        self,
        operation: str,
        **options: object,
    ) -> FlextResult[object]:
        """Execute stream operation."""
        return self.service.execute("stream", operation, **options)

    # Convenience methods for common operations
    def start_server(
        self,
        server: FlextGrpcServer,
        **options: object,
    ) -> FlextResult[FlextGrpcServer]:
        """Start a gRPC server."""
        return self.server_operation("start", server, **options)

    def stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop a gRPC server."""
        return self.server_operation("stop", server)

    def connect_client(self, client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
        """Connect a gRPC client."""
        return self.client_operation("connect", client)

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
        return self.server_operation("status", server)

    def get_client_status(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[dict[str, object]]:
        """Get client status."""
        return self.client_operation("status", client)

    def create_stream(
        self,
        client: FlextGrpcClient,
        method_name: str,
        stream_type: str = "unary",
        **options: object,
    ) -> FlextResult[FlextGrpcStream]:
        """Create a gRPC stream."""
        return self.stream_operation(
            "create",
            client=client,
            method_name=method_name,
            stream_type=stream_type,
            **options,
        )
