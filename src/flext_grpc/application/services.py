"""FLEXT gRPC Application Services - gRPC communication services.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Application services for gRPC communication operations.
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from flext_core import FlextContainer, FlextDomainService, FlextResult

if TYPE_CHECKING:
    from flext_grpc.domain.entities import (
        FlextGrpcClient,
        FlextGrpcServer,
        FlextGrpcService,
        FlextGrpcStream,
    )

from flext_grpc.domain.entities import FlextGrpcStream


class FlextGrpcServerService(FlextDomainService):
    """Service for gRPC server management."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize gRPC server service.

        Args:
            container: Dependency injection container

        """
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def start_server(
        self,
        server: FlextGrpcServer,
        **options: dict[str, object],  # noqa: ARG002
    ) -> FlextResult[bool]:
        """Start a gRPC server.

        Args:
            server: gRPC server to start
            **options: Additional server options

        Returns:
            FlextResult indicating if server start was successful

        """
        try:
            if not server.is_valid():
                return FlextResult.fail("Invalid server configuration")

            if server.is_running():
                return FlextResult.fail("Server is already running")

            # Mark server as starting
            if not server.start():
                return FlextResult.fail("Server is not in a startable state")

            # Server startup logic would go here
            # This is a placeholder implementation
            server.mark_running()
            return FlextResult.ok(success=True)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to start server: {e}")

    def stop_server(self, server: FlextGrpcServer) -> FlextResult[bool]:
        """Stop a gRPC server.

        Args:
            server: gRPC server to stop

        Returns:
            FlextResult indicating if server stop was successful

        """
        try:
            if not server.is_running():
                return FlextResult.fail("Server is not running")

            # Mark server as stopping
            if not server.stop():
                return FlextResult.fail("Server is not in a stoppable state")

            # Server shutdown logic would go here
            # This is a placeholder implementation
            server.mark_stopped()
            return FlextResult.ok(success=True)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to stop server: {e}")

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
        try:
            if not server.is_valid():
                return FlextResult.fail("Invalid server")

            if not service.is_valid():
                return FlextResult.fail("Invalid service")

            if server.add_service(service):
                return FlextResult.ok(success=True)
            return FlextResult.fail("Service already exists on server")

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to add service to server: {e}")

    def get_server_status(self, server: FlextGrpcServer) -> FlextResult[dict[str, Any]]:
        """Get server status information.

        Args:
            server: gRPC server

        Returns:
            FlextResult containing server status information

        """
        try:
            if not server.is_valid():
                return FlextResult.fail("Invalid server")

            status = {
                "address": server.get_address(),
                "state": server.state.value,
                "is_running": server.is_running(),
                "service_count": len(server.services),
                "services": [service.name for service in server.services],
            }

            return FlextResult.ok(status)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to get server status: {e}")


class FlextGrpcClientService(FlextDomainService):
    """Service for gRPC client management."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize gRPC client service.

        Args:
            container: Dependency injection container

        """
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def connect_client(self, client: FlextGrpcClient) -> FlextResult[bool]:
        """Connect a gRPC client.

        Args:
            client: gRPC client to connect

        Returns:
            FlextResult indicating if client connection was successful

        """
        try:
            if not client.is_valid():
                return FlextResult.fail("Invalid client configuration")

            if client.is_connected():
                return FlextResult.fail("Client is already connected")

            # Use FLEXT connection service instead of manual connection
            connection_service = self.container.get("FlextGrpcConnectionService")
            if not connection_service:
                return FlextResult.fail("FLEXT gRPC connection service not available")

            result = connection_service.establish_channel_connection(client)
            if not result.success:
                return result

            return FlextResult.ok(success=True)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to connect client: {e}")

    def disconnect_client(self, client: FlextGrpcClient) -> FlextResult[bool]:
        """Disconnect a gRPC client.

        Args:
            client: gRPC client to disconnect

        Returns:
            FlextResult indicating if client disconnection was successful

        """
        try:
            if not client.is_connected():
                return FlextResult.fail("Client is not connected")

            # Use FLEXT connection service instead of manual disconnection
            connection_service = self.container.get("FlextGrpcConnectionService")
            if not connection_service:
                return FlextResult.fail("FLEXT gRPC connection service not available")

            result = connection_service.release_channel_connection(client)
            if not result.success:
                return result

            return FlextResult.ok(success=True)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to disconnect client: {e}")

    def make_call(
        self,
        client: FlextGrpcClient,
        method_name: str,
        request_data: dict[str, object],
        **options: dict[str, object],  # noqa: ARG002
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
        try:
            if not client.is_valid():
                return FlextResult.fail("Invalid client")

            if not client.is_connected():
                return FlextResult.fail("Client is not connected")

            if not method_name:
                return FlextResult.fail("Method name is required")

            # gRPC call logic would go here
            # This is a placeholder implementation
            response = {
                "status": "success",
                "method": method_name,
                "data": request_data,
            }
            return FlextResult.ok(response)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to make gRPC call: {e}")

    def get_client_status(self, client: FlextGrpcClient) -> FlextResult[dict[str, Any]]:
        """Get client status information.

        Args:
            client: gRPC client

        Returns:
            FlextResult containing client status information

        """
        try:
            if not client.is_valid():
                return FlextResult.fail("Invalid client")

            status = {
                "is_connected": client.is_connected(),
                "channel_target": client.channel.target if client.channel else None,
                "channel_state": client.channel.state.value if client.channel else None,
                "options": client.options,
            }

            return FlextResult.ok(status)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to get client status: {e}")


class FlextGrpcStreamService(FlextDomainService):
    """Service for gRPC streaming operations."""

    container: FlextContainer

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize gRPC stream service.

        Args:
            container: Dependency injection container

        """
        super().__init__(container=container or FlextContainer())

    def execute(self, *args: object, **kwargs: object) -> FlextResult[Any]:  # noqa: ARG002
        """Execute service operation (required by FlextDomainService).

        This method is required by the abstract base class but services
        provide specific methods for their operations.

        Returns:
            FlextResult indicating this method should not be used directly

        """
        return FlextResult.fail("Use specific service methods instead of execute")

    def create_stream(
        self,
        client: FlextGrpcClient,
        method_name: str,
        stream_type: str,
        **options: dict[str, object],
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
        try:
            if not client.is_valid():
                return FlextResult.fail("Invalid client")

            if not client.is_connected():
                return FlextResult.fail("Client is not connected")

            if not method_name:
                return FlextResult.fail("Method name is required")

            stream = FlextGrpcStream(
                entity_id=str(uuid.uuid4()),
                method_name=method_name,
                stream_type=stream_type,
                metadata=options,
            )

            if not stream.is_valid():
                return FlextResult.fail("Invalid stream configuration")

            return FlextResult.ok(stream)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to create stream: {e}")

    def send_stream_message(
        self,
        stream: FlextGrpcStream,
        message_data: dict[str, object],  # noqa: ARG002
    ) -> FlextResult[bool]:
        """Send a message through a gRPC stream.

        Args:
            stream: gRPC stream
            message_data: Message data to send

        Returns:
            FlextResult indicating if message was sent successfully

        """
        try:
            if not stream.is_valid():
                return FlextResult.fail("Invalid stream")

            # Stream message sending logic would go here
            # This is a placeholder implementation
            return FlextResult.ok(success=True)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to send stream message: {e}")

    def close_stream(self, stream: FlextGrpcStream) -> FlextResult[bool]:
        """Close a gRPC stream.

        Args:
            stream: gRPC stream to close

        Returns:
            FlextResult indicating if stream was closed successfully

        """
        try:
            if not stream.is_valid():
                return FlextResult.fail("Invalid stream")

            # Stream closing logic would go here
            # This is a placeholder implementation
            return FlextResult.ok(success=True)

        except (ValueError, TypeError) as e:
            return FlextResult.fail(f"Failed to close stream: {e}")


# Backwards compatibility aliases
GrpcServerService = FlextGrpcServerService
GrpcClientService = FlextGrpcClientService
GrpcStreamService = FlextGrpcStreamService
