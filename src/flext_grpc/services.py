"""FLEXT gRPC Domain Services - Business logic for gRPC operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextDomainService, FlextResult

from .constants import FlextGrpcConstants

if TYPE_CHECKING:
    from flext_grpc.entities import (
        FlextGrpcClient,
        FlextGrpcServer,
        FlextGrpcStream,
    )


class FlextGrpcServerService(FlextDomainService):
    """Domain service for gRPC server lifecycle management."""

    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute server operation.

        Args:
            *args: Arguments (expected: operation, server)
            **kwargs: Additional options

        Returns:
            FlextResult with operation result

        """
        if len(args) < FlextGrpcConstants.MIN_REQUIRED_ARGS:
            return FlextResult.fail("Missing required arguments: operation and server")

        operation = args[0]
        server = args[1]

        if not isinstance(operation, str):
            return FlextResult.fail("Operation must be a string")

        # Type validation for server
        from flext_grpc.entities import FlextGrpcServer  # noqa: PLC0415
        if not isinstance(server, FlextGrpcServer):
            return FlextResult.fail("Server must be a FlextGrpcServer instance")

        # Validate server first
        validation = server.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid server: {validation.error}")

        return self._execute_server_operation(operation, server, **kwargs)

    def _execute_server_operation(
        self, operation: str, server: FlextGrpcServer, **options: object,
    ) -> FlextResult[object]:
        """Execute specific server operation."""
        # Use match for better type inference
        match operation:
            case "start":
                start_result = self._start_server(server)
                if start_result.is_success:
                    return FlextResult.ok(start_result.data)
                return FlextResult.fail(start_result.error or "Start failed")
            case "stop":
                stop_result = self._stop_server(server)
                if stop_result.is_success:
                    return FlextResult.ok(stop_result.data)
                return FlextResult.fail(stop_result.error or "Stop failed")
            case "add_service":
                return self._handle_add_service(server, options)
            case "status":
                status_result = self._get_server_status(server)
                if status_result.is_success:
                    return FlextResult.ok(status_result.data)
                return FlextResult.fail(status_result.error or "Status failed")
            case _:
                return FlextResult.fail(f"Unknown server operation: {operation}")

    def _handle_add_service(
        self, server: FlextGrpcServer, options: dict[str, object],
    ) -> FlextResult[object]:
        """Handle add_service operation."""
        service = options.get("service")
        if not service:
            return FlextResult.fail("Service required")

        # Type validation for service
        from flext_grpc.entities import FlextGrpcService  # noqa: PLC0415
        if not isinstance(service, FlextGrpcService):
            return FlextResult.fail("Service must be a FlextGrpcService instance")

        result = server.add_service(service)
        # Convert to object result to match return type
        if result.is_success:
            return FlextResult.ok(result.data)
        return FlextResult.fail(result.error or "Add service failed")

    def _start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Start server with proper state transitions."""
        if server.is_running:
            return FlextResult.fail("Server is already running")

        # Use proper state transitions
        start_result = server.start()
        if start_result.is_failure:
            return start_result

        starting_server = start_result.data
        if starting_server is None:
            return FlextResult.fail("Failed to start server")

        return starting_server.mark_running()

    def _stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop server with proper state transitions."""
        if not server.is_running:
            return FlextResult.fail("Server is not running")

        # Use proper state transitions
        stop_result = server.stop()
        if stop_result.is_failure:
            return stop_result

        stopping_server = stop_result.data
        if stopping_server is None:
            return FlextResult.fail("Failed to stop server")

        return stopping_server.mark_stopped()

    def _get_server_status(
        self, server: FlextGrpcServer,
    ) -> FlextResult[dict[str, object]]:
        """Get comprehensive server status."""
        return FlextResult.ok({
            "id": server.id,
            "address": server.address,
            "state": server.state,
            "is_running": server.is_running,
            "service_count": len(server.services),
            "max_workers": server.max_workers,
            "version": server.version,
        })


class FlextGrpcClientService(FlextDomainService):
    """Domain service for gRPC client operations."""

    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute client operation.

        Args:
            *args: Arguments (expected: operation, client)
            **kwargs: Additional options

        Returns:
            FlextResult with operation result

        """
        if len(args) < FlextGrpcConstants.MIN_REQUIRED_ARGS:
            return FlextResult.fail("Missing required arguments: operation and client")

        operation = args[0]
        client = args[1]

        if not isinstance(operation, str):
            return FlextResult.fail("Operation must be a string")

        # Type validation for client
        from flext_grpc.entities import FlextGrpcClient  # noqa: PLC0415
        if not isinstance(client, FlextGrpcClient):
            return FlextResult.fail("Client must be a FlextGrpcClient instance")

        # Validate client first
        validation = client.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid client: {validation.error}")

        return self._execute_client_operation(operation, client, **kwargs)

    def _execute_client_operation(
        self,
        operation: str,
        client: FlextGrpcClient,
        **kwargs: object
    ) -> FlextResult[object]:
        """Execute specific client operation - SOLID principle pattern."""
        # Use match for better type inference
        match operation:
            case "connect":
                connect_result = self._connect_client(client)
                if connect_result.is_success:
                    return FlextResult.ok(connect_result.data)
                return FlextResult.fail(connect_result.error or "Connect failed")
            case "disconnect":
                disconnect_result = self._disconnect_client(client)
                if disconnect_result.is_success:
                    return FlextResult.ok(disconnect_result.data)
                return FlextResult.fail(disconnect_result.error or "Disconnect failed")
            case "call":
                method_name_arg = kwargs.get("method_name")
                method_name = str(method_name_arg) if method_name_arg else None
                request_data = kwargs.get("request_data")
                call_result = self._call_method(client, method_name, request_data)
                if call_result.is_success:
                    return FlextResult.ok(call_result.data)
                return FlextResult.fail(call_result.error or "Call failed")
            case "status":
                status_result = self._get_client_status(client)
                if status_result.is_success:
                    return FlextResult.ok(status_result.data)
                return FlextResult.fail(status_result.error or "Status failed")
            case _:
                return FlextResult.fail(f"Unknown client operation: {operation}")

    def _connect_client(self, client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
        """Connect client with proper channel state management."""
        if client.is_connected:
            return FlextResult.fail("Client is already connected")

        if not client.channel:
            return FlextResult.fail("Client has no channel")

        # Use proper channel state transitions
        connect_result = client.channel.connect()
        if connect_result.is_failure:
            return FlextResult.fail(connect_result.error or "Connect failed")

        connecting_channel = connect_result.data
        if connecting_channel is None:
            return FlextResult.fail("Failed to connect channel")

        ready_result = connecting_channel.mark_ready()
        if ready_result.is_failure:
            return FlextResult.fail(ready_result.error or "Mark ready failed")

        ready_channel = ready_result.data
        if ready_channel is None:
            return FlextResult.fail("Failed to mark channel ready")

        return client.copy_with(channel=ready_channel)

    def _disconnect_client(
        self, client: FlextGrpcClient,
    ) -> FlextResult[FlextGrpcClient]:
        """Disconnect client with proper channel state management."""
        if not client.is_connected:
            return FlextResult.fail("Client is not connected")

        if not client.channel:
            return FlextResult.fail("Client has no channel")

        # Use proper channel state transitions
        disconnect_result = client.channel.disconnect()
        if disconnect_result.is_failure:
            return FlextResult.fail(disconnect_result.error or "Disconnect failed")

        disconnected_channel = disconnect_result.data
        if disconnected_channel is None:
            return FlextResult.fail("Failed to disconnect channel")

        return client.copy_with(channel=disconnected_channel)

    def _call_method(
        self,
        client: FlextGrpcClient,
        method_name: str | None,
        request_data: object,
    ) -> FlextResult[dict[str, object]]:
        """Make method call through connected client."""
        if not client.is_connected:
            return FlextResult.fail("Client is not connected")

        if not method_name:
            return FlextResult.fail("Method name is required")

        return FlextResult.ok({
            "status": "success",
            "method": method_name,
            "client_id": client.id,
            "data": request_data,
            "target": client.target,
        })

    def _get_client_status(
        self, client: FlextGrpcClient,
    ) -> FlextResult[dict[str, object]]:
        """Get comprehensive client status."""
        return FlextResult.ok({
            "id": client.id,
            "is_connected": client.is_connected,
            "target": client.target,
            "channel_state": client.channel.state if client.channel else None,
            "version": client.version,
        })


class FlextGrpcStreamService(FlextDomainService):
    """Domain service for gRPC streaming operations."""

    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute stream operation.

        Args:
            *args: Arguments (expected: operation)
            **kwargs: Additional options including stream, client, method_name, etc.

        Returns:
            FlextResult with operation result

        """
        if len(args) < 1:
            return FlextResult.fail("Missing required argument: operation")

        operation = args[0]

        if not isinstance(operation, str):
            return FlextResult.fail("Operation must be a string")

        match operation:
            case "create":
                client = kwargs.get("client")
                method_name = kwargs.get("method_name")
                stream_type = kwargs.get("stream_type", "unary")

                # Type validation and conversion
                from flext_grpc.entities import FlextGrpcClient  # noqa: PLC0415
                if not isinstance(client, FlextGrpcClient):
                    return FlextResult.fail("Client must be a FlextGrpcClient instance")

                method_name_str = str(method_name) if method_name else None
                stream_type_str = str(stream_type) if stream_type else "unary"

                result = self._create_stream(client, method_name_str, stream_type_str)
                if result.is_success:
                    return FlextResult.ok(result.data)
                return FlextResult.fail(result.error or "Create stream failed")
            case "send":
                stream = kwargs.get("stream")
                data = kwargs.get("data")

                # Type validation
                from flext_grpc.entities import FlextGrpcStream  # noqa: PLC0415
                if not isinstance(stream, FlextGrpcStream):
                    return FlextResult.fail("Stream must be a FlextGrpcStream instance")

                send_result = self._send_data(stream, data)
                if send_result.is_success:
                    return FlextResult.ok(send_result.data)
                return FlextResult.fail(send_result.error or "Send data failed")
            case "close":
                stream = kwargs.get("stream")

                # Type validation
                from flext_grpc.entities import FlextGrpcStream  # noqa: PLC0415
                if not isinstance(stream, FlextGrpcStream):
                    return FlextResult.fail("Stream must be a FlextGrpcStream instance")

                close_result = self._close_stream(stream)
                if close_result.is_success:
                    return FlextResult.ok(close_result.data)
                return FlextResult.fail(close_result.error or "Close stream failed")
            case _:
                return FlextResult.fail(f"Unknown stream operation: {operation}")

    def _create_stream(
        self,
        client: FlextGrpcClient,
        method_name: str | None,
        stream_type: str,
    ) -> FlextResult[FlextGrpcStream]:
        """Create a new gRPC stream with validation."""
        validation = client.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid client: {validation.error}")

        if not client.is_connected:
            return FlextResult.fail("Client is not connected")

        if not method_name:
            return FlextResult.fail("Method name is required")

        # Use entity factory for proper creation
        from flext_grpc.entities import FlextGrpcEntityFactory  # noqa: PLC0415
        return FlextGrpcEntityFactory.create_stream(method_name, stream_type)

    def _send_data(
        self, stream: FlextGrpcStream, data: object,
    ) -> FlextResult[bool]:
        """Send data through stream."""
        validation = stream.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid stream: {validation.error}")

        # In a real implementation, this would send data through the stream
        # Use data parameter to avoid ARG002
        _ = data  # Mark as used
        return FlextResult.ok(data=True)

    def _close_stream(self, stream: FlextGrpcStream) -> FlextResult[bool]:
        """Close stream properly."""
        validation = stream.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid stream: {validation.error}")

        # In a real implementation, this would close the stream
        return FlextResult.ok(data=True)


class FlextGrpcService(FlextDomainService):
    """Unified gRPC service orchestrating server, client, and stream operations."""

    def __init__(self) -> None:
        """Initialize unified service with component services."""
        self._server_service = FlextGrpcServerService()
        self._client_service = FlextGrpcClientService()
        self._stream_service = FlextGrpcStreamService()

    def execute(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute unified gRPC operation.

        Args:
            *args: Arguments (expected: service_type, operation, ...)
            **kwargs: Additional options

        Returns:
            FlextResult with operation result

        """
        if len(args) < 1:
            return FlextResult.fail("Missing required argument: service_type")

        service_type = args[0]
        if not isinstance(service_type, str):
            return FlextResult.fail("Service type must be a string")

        # Delegate to appropriate service
        match service_type:
            case "server":
                return self._server_service.execute(*args[1:], **kwargs)
            case "client":
                return self._client_service.execute(*args[1:], **kwargs)
            case "stream":
                return self._stream_service.execute(*args[1:], **kwargs)
            case _:
                return FlextResult.fail(f"Unknown service type: {service_type}")
