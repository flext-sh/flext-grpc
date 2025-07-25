"""FLEXT gRPC Platform - Unified gRPC communication platform.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Platform class providing unified access to gRPC communication services.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import FlextContainer, FlextResult

if TYPE_CHECKING:
    from flext_grpc.application.services import (
        FlextGrpcClientService,
        FlextGrpcServerService,
        FlextGrpcStreamService,
    )
    from flext_grpc.domain.entities import (
        FlextGrpcClient,
        FlextGrpcServer,
        FlextGrpcService,
        FlextGrpcStream,
    )


class FlextGrpcPlatform:
    """Platform for gRPC communication operations."""

    def __init__(self, config: dict[str, object] | None = None) -> None:
        """Initialize gRPC platform.

        Args:
            config: Platform configuration

        """
        self.config = config or {}
        self.container = FlextContainer()
        self._setup_services()

    def _setup_services(self) -> None:
        """Setup platform services."""
        # Import here to avoid circular imports
        from flext_grpc.application.services import (
            FlextGrpcClientService,
            FlextGrpcServerService,
            FlextGrpcStreamService,
        )

        # Register services in container
        self.container.register(
            "grpc_server_service",
            FlextGrpcServerService(self.container),
        )
        self.container.register(
            "grpc_client_service",
            FlextGrpcClientService(self.container),
        )
        self.container.register(
            "grpc_stream_service",
            FlextGrpcStreamService(self.container),
        )

    @property
    def server_service(self) -> FlextGrpcServerService:
        """Get gRPC server service."""
        return self.container.get("grpc_server_service")

    @property
    def client_service(self) -> FlextGrpcClientService:
        """Get gRPC client service."""
        return self.container.get("grpc_client_service")

    @property
    def stream_service(self) -> FlextGrpcStreamService:
        """Get gRPC stream service."""
        return self.container.get("grpc_stream_service")

    def start_server(
        self,
        server: FlextGrpcServer,
        **options: Any,
    ) -> FlextResult[bool]:
        """Start a gRPC server.

        Args:
            server: gRPC server to start
            **options: Additional server options

        Returns:
            FlextResult indicating if server start was successful

        """
        return self.server_service.start_server(server, **options)

    def stop_server(self, server: FlextGrpcServer) -> FlextResult[bool]:
        """Stop a gRPC server.

        Args:
            server: gRPC server to stop

        Returns:
            FlextResult indicating if server stop was successful

        """
        return self.server_service.stop_server(server)

    def add_service_to_server(
        self,
        server: FlextGrpcServer,
        service: FlextGrpcService,
    ) -> FlextResult[bool]:
        """Add a service to a gRPC server.

        Args:
            server: gRPC server
            service: gRPC service to add

        Returns:
            FlextResult indicating if service was added successfully

        """
        return self.server_service.add_service_to_server(server, service)

    def get_server_status(self, server: FlextGrpcServer) -> FlextResult[dict[str, Any]]:
        """Get server status information.

        Args:
            server: gRPC server

        Returns:
            FlextResult containing server status information

        """
        return self.server_service.get_server_status(server)

    def connect_client(self, client: FlextGrpcClient) -> FlextResult[bool]:
        """Connect a gRPC client.

        Args:
            client: gRPC client to connect

        Returns:
            FlextResult indicating if client connection was successful

        """
        return self.client_service.connect_client(client)

    def disconnect_client(self, client: FlextGrpcClient) -> FlextResult[bool]:
        """Disconnect a gRPC client.

        Args:
            client: gRPC client to disconnect

        Returns:
            FlextResult indicating if client disconnection was successful

        """
        return self.client_service.disconnect_client(client)

    def make_call(
        self,
        client: FlextGrpcClient,
        method_name: str,
        request_data: Any,
        **options: Any,
    ) -> FlextResult[Any]:
        """Make a gRPC call using the client.

        Args:
            client: gRPC client
            method_name: Name of the method to call
            request_data: Request data
            **options: Additional call options

        Returns:
            FlextResult containing the response data

        """
        return self.client_service.make_call(
            client,
            method_name,
            request_data,
            **options,
        )

    def get_client_status(self, client: FlextGrpcClient) -> FlextResult[dict[str, Any]]:
        """Get client status information.

        Args:
            client: gRPC client

        Returns:
            FlextResult containing client status information

        """
        return self.client_service.get_client_status(client)

    def create_stream(
        self,
        client: FlextGrpcClient,
        method_name: str,
        stream_type: str,
        **options: Any,
    ) -> FlextResult[FlextGrpcStream]:
        """Create a gRPC stream.

        Args:
            client: gRPC client
            method_name: Name of the streaming method
            stream_type: Type of stream
            **options: Additional stream options

        Returns:
            FlextResult containing the created stream

        """
        return self.stream_service.create_stream(
            client,
            method_name,
            stream_type,
            **options,
        )

    def send_stream_message(
        self,
        stream: FlextGrpcStream,
        message_data: Any,
    ) -> FlextResult[bool]:
        """Send a message through a gRPC stream.

        Args:
            stream: gRPC stream
            message_data: Message data to send

        Returns:
            FlextResult indicating if message was sent successfully

        """
        return self.stream_service.send_stream_message(stream, message_data)

    def close_stream(self, stream: FlextGrpcStream) -> FlextResult[bool]:
        """Close a gRPC stream.

        Args:
            stream: gRPC stream to close

        Returns:
            FlextResult indicating if stream was closed successfully

        """
        return self.stream_service.close_stream(stream)


# Backwards compatibility alias
GrpcPlatform = FlextGrpcPlatform
