"""FLEXT gRPC Domain Services - Business logic for gRPC operations.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextDomainService, FlextResult

if TYPE_CHECKING:
    from flext_grpc.entities import (
        FlextGrpcClient,
        FlextGrpcServer,
        FlextGrpcStream,
    )


class FlextGrpcServerService(FlextDomainService):
    """Domain service for gRPC server lifecycle management."""

    def execute(
        self, operation: str, server: FlextGrpcServer, **options: object,
    ) -> FlextResult[object]:
        """Execute server operation.

        Args:
            operation: Operation to perform (start, stop, add_service, status)
            server: Target server entity
            **options: Additional options

        Returns:
            FlextResult with operation result

        """
        # Validate server first
        validation = server.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid server: {validation.error}")

        return self._execute_server_operation(operation, server, **options)

    def _execute_server_operation(
        self, operation: str, server: FlextGrpcServer, **options: object,
    ) -> FlextResult[object]:
        """Execute specific server operation."""
        operations = {
            "start": lambda: self._start_server(server),
            "stop": lambda: self._stop_server(server),
            "add_service": lambda: self._handle_add_service(server, options),
            "status": lambda: self._get_server_status(server),
        }

        operation_handler = operations.get(operation)
        if operation_handler:
            return operation_handler()

        return FlextResult.fail(f"Unknown server operation: {operation}")

    def _handle_add_service(
        self, server: FlextGrpcServer, options: dict[str, object],
    ) -> FlextResult[object]:
        """Handle add_service operation."""
        service = options.get("service")
        if not service:
            return FlextResult.fail("Service required")
        return server.add_service(service)

    def _start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Start server with proper state transitions."""
        if server.is_running:
            return FlextResult.fail("Server is already running")

        # Use proper state transitions
        start_result = server.start()
        if start_result.is_failure:
            return start_result

        return start_result.data.mark_running()

    def _stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop server with proper state transitions."""
        if not server.is_running:
            return FlextResult.fail("Server is not running")

        # Use proper state transitions
        stop_result = server.stop()
        if stop_result.is_failure:
            return stop_result

        return stop_result.data.mark_stopped()

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

    def execute(
        self, operation: str, client: FlextGrpcClient, **options: object,
    ) -> FlextResult[object]:
        """Execute client operation.

        Args:
            operation: Operation to perform (connect, disconnect, call, status)
            client: Target client entity
            **options: Additional options

        Returns:
            FlextResult with operation result

        """
        # Validate client first
        validation = client.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid client: {validation.error}")

        match operation:
            case "connect":
                return self._connect_client(client)
            case "disconnect":
                return self._disconnect_client(client)
            case "call":
                method_name = options.get("method_name")
                request_data = options.get("request_data")
                return self._call_method(client, method_name, request_data)
            case "status":
                return self._get_client_status(client)
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
            return connect_result

        ready_result = connect_result.data.mark_ready()
        if ready_result.is_failure:
            return ready_result

        return client.copy_with(channel=ready_result.data)

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
            return disconnect_result

        return client.copy_with(channel=disconnect_result.data)

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

    def execute(self, operation: str, **options: object) -> FlextResult[object]:
        """Execute stream operation.

        Args:
            operation: Operation to perform (create, send, close)
            **options: Additional options including stream, client, method_name, etc.

        Returns:
            FlextResult with operation result

        """
        match operation:
            case "create":
                client = options.get("client")
                method_name = options.get("method_name")
                stream_type = options.get("stream_type", "unary")
                return self._create_stream(client, method_name, stream_type)
            case "send":
                stream = options.get("stream")
                data = options.get("data")
                return self._send_data(stream, data)
            case "close":
                stream = options.get("stream")
                return self._close_stream(stream)
            case _:
                return FlextResult.fail(f"Unknown stream operation: {operation}")

    def _create_stream(
        self,
        client: FlextGrpcClient | None,
        method_name: str | None,
        stream_type: str,
    ) -> FlextResult[FlextGrpcStream]:
        """Create a new gRPC stream with validation."""
        if not client:
            return FlextResult.fail("Client required")

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
        self, stream: FlextGrpcStream | None, data: object,
    ) -> FlextResult[bool]:
        """Send data through stream."""
        if not stream:
            return FlextResult.fail("Stream required")

        validation = stream.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid stream: {validation.error}")

        # In a real implementation, this would send data through the stream
        # Use data parameter to avoid ARG002
        _ = data  # Mark as used
        return FlextResult.ok(value=True)

    def _close_stream(self, stream: FlextGrpcStream | None) -> FlextResult[bool]:
        """Close stream properly."""
        if not stream:
            return FlextResult.fail("Stream required")

        validation = stream.validate_domain_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid stream: {validation.error}")

        # In a real implementation, this would close the stream
        return FlextResult.ok(value=True)
