"""FLEXT gRPC Services - Unified Domain Services and Platform.

🎯 CONSOLIDATES 2 SERVICE FILES INTO SINGLE PEP8 MODULE:
- services.py (800+ lines) - Domain services for gRPC operations orchestration
- platform.py (600+ lines) - Platform facade for unified gRPC management

TOTAL CONSOLIDATION: 1400+ lines → grpc_services.py (PEP8 organized)

This module provides unified domain services and platform facade for FLEXT gRPC,
implementing business logic orchestration and simplified platform operations with
comprehensive error handling and enterprise patterns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Callable
from typing import cast

from flext_core import FlextContainer, FlextResult, get_flext_container

from flext_grpc.entities import (
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)

# Type aliases for better readability
type TGrpcServerEntity = FlextGrpcServer
type TGrpcClientEntity = FlextGrpcClient
type TGrpcStreamEntity = FlextGrpcStream
type TGrpcServiceDef = FlextGrpcService
type TMethodCallResult = dict[str, object]

# =============================================================================
# GRPC DOMAIN SERVICES
# =============================================================================


class FlextGrpcServerService:
    """gRPC server domain service for lifecycle management.

    Implements business logic for gRPC server operations including startup,
    shutdown, service registration, and status monitoring. Follows Domain-Driven
    Design patterns with comprehensive validation and error handling.

    Commands:
      - start: Start server lifecycle (stopped → starting → running)
      - stop: Stop server lifecycle (running → stopping → stopped)
      - add_service: Register gRPC service with server
      - status: Get current server status and health information

    Example:
      >>> service = FlextGrpcServerService()
      >>> result = service.execute("start", server)
      >>> if result.success:
      ...     running_server = result.data
      ...     print(f"Server running: {running_server.state}")

    """

    def execute(
        self,
        command: str,
        server: TGrpcServerEntity,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[TGrpcServerEntity | dict[str, object]]:
        """Execute server command with validation and error handling."""
        # Import here to avoid circular imports

        # Validate server entity
        validation = server.validate_business_rules()
        if validation.is_failure:
            return FlextResult[None].fail(f"Server validation failed: {validation.error}")

        # Command mapping to reduce return statements
        command_handlers: dict[
            str,
            Callable[[], FlextResult[TGrpcServerEntity | dict[str, object]]],
        ] = {
            "start": lambda: cast(
                "FlextResult[TGrpcServerEntity | dict[str, object]]",
                self._start_server(server),
            ),
            "stop": lambda: cast(
                "FlextResult[TGrpcServerEntity | dict[str, object]]",
                self._stop_server(server),
            ),
            "status": lambda: cast(
                "FlextResult[TGrpcServerEntity | dict[str, object]]",
                self._get_status(server),
            ),
        }

        # Handle add_service command with validation
        if command == "add_service":
            service_def = args[0] if args else kwargs.get("service")
            if not isinstance(service_def, FlextGrpcService):
                return FlextResult[None].fail(
                    f"Service definition must be FlextGrpcService, got: {type(service_def)}",
                )
            return cast(
                "FlextResult[TGrpcServerEntity | dict[str, object]]",
                self._add_service(server, service_def),
            )

        # Execute mapped commands
        if command in command_handlers:
            handler = command_handlers[command]
            return handler()

        return FlextResult[None].fail(f"Unknown server command: {command}")

    def _start_server(
        self,
        server: TGrpcServerEntity,
    ) -> FlextResult[TGrpcServerEntity]:
        """Start server with state transition validation."""
        # Transition: stopped → starting
        start_result = server.start()
        if start_result.is_failure:
            return start_result

        # Simulate server startup (in real implementation, start actual gRPC server)
        starting_server = start_result.data
        if starting_server is None:
            return FlextResult[None].fail("Failed to get starting server data")

        # Transition: starting → running
        running_result = starting_server.mark_running()
        if running_result.is_failure:
            return running_result

        if running_result.data is None:
            return FlextResult[None].fail("Failed to get running server data")
        return FlextResult[None].ok(running_result.data)

    def _stop_server(self, server: TGrpcServerEntity) -> FlextResult[TGrpcServerEntity]:
        """Stop server with graceful shutdown."""
        # Transition: running → stopping
        stop_result = server.stop()
        if stop_result.is_failure:
            return stop_result

        # Simulate server shutdown (in real implementation, stop actual gRPC server)
        stopping_server = stop_result.data
        if stopping_server is None:
            return FlextResult[None].fail("Failed to get stopping server data")

        # Transition: stopping → stopped
        stopped_result = stopping_server.mark_stopped()
        if stopped_result.is_failure:
            return stopped_result

        if stopped_result.data is None:
            return FlextResult[None].fail("Failed to get stopped server data")
        return FlextResult[None].ok(stopped_result.data)

    def _add_service(
        self,
        server: TGrpcServerEntity,
        _service_def: TGrpcServiceDef,
    ) -> FlextResult[TGrpcServerEntity]:
        """Add gRPC service to server."""
        if server.state != "running":
            return FlextResult[None].fail(
                f"Cannot add service to server in state: {server.state}",
            )

        # In real implementation, register service with gRPC server
        return FlextResult[None].ok(server)

    def _get_status(self, server: TGrpcServerEntity) -> FlextResult[dict[str, object]]:
        """Get server status information."""
        status = {
            "state": server.state,
            "host": server.host,
            "port": server.port,
            "max_workers": server.max_workers,
            "address": server.address,
        }
        return FlextResult[None].ok(status)


class FlextGrpcClientService:
    """gRPC client domain service for connection management.

    Implements business logic for gRPC client operations including connection
    establishment, remote calls, and connection lifecycle management.

    Commands:
      - connect: Establish client connection (idle → connecting → ready)
      - disconnect: Close client connection (ready → shutdown)
      - call: Execute remote method call
      - status: Get current client status and connection information

    Example:
      >>> service = FlextGrpcClientService()
      >>> result = service.execute("connect", client)
      >>> if result.success:
      ...     connected_client = result.data
      ...     print(f"Client connected: {connected_client.channel_state}")

    """

    def execute(
        self,
        command: str,
        client: TGrpcClientEntity,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]:
        """Execute client command with validation and error handling."""
        # Validate client entity
        validation = client.validate_business_rules()
        if validation.is_failure:
            return FlextResult[None].fail(f"Client validation failed: {validation.error}")

        # Command mapping to reduce return statements
        command_handlers: dict[
            str,
            Callable[
                [],
                FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]],
            ],
        ] = {
            "connect": lambda: cast(
                "FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]",
                self._connect_client(client),
            ),
            "disconnect": lambda: cast(
                "FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]",
                self._disconnect_client(client),
            ),
            "status": lambda: cast(
                "FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]",
                self._get_status(client),
            ),
        }

        # Handle call command with validation
        if command == "call":
            method_name = args[0] if args else kwargs.get("method")
            request = args[1] if len(args) > 1 else kwargs.get("request")
            if not isinstance(method_name, str):
                return FlextResult[None].fail(
                    f"Method name must be string, got: {type(method_name)}",
                )
            return cast(
                "FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]",
                self._make_call(client, method_name, request),
            )

        # Execute mapped commands
        if command in command_handlers:
            handler = command_handlers[command]
            return handler()

        return FlextResult[None].fail(f"Unknown client command: {command}")

    def _connect_client(
        self,
        client: TGrpcClientEntity,
    ) -> FlextResult[TGrpcClientEntity]:
        """Connect client with state transition validation."""
        # Check if client has a channel
        if client.channel is None:
            return FlextResult[None].fail("Client has no channel to connect")

        # Transition: idle → connecting
        connect_result = client.channel.connect()
        if connect_result.is_failure:
            return FlextResult[None].fail(
                f"Channel connection failed: {connect_result.error}",
            )

        # Simulate connection establishment
        connecting_channel = connect_result.data
        if connecting_channel is None:
            return FlextResult[None].fail("Failed to get connecting channel data")

        # Transition: connecting → ready
        ready_result = connecting_channel.mark_ready()
        if ready_result.is_failure:
            return FlextResult[None].fail(
                f"Channel ready transition failed: {ready_result.error}",
            )

        if ready_result.data is None:
            return FlextResult[None].fail("Failed to get ready channel data")

        # Update client with new channel
        return client.copy_with(channel=ready_result.data)

    def _disconnect_client(
        self,
        client: TGrpcClientEntity,
    ) -> FlextResult[TGrpcClientEntity]:
        """Disconnect client with graceful shutdown."""
        # Check if client has a channel
        if client.channel is None:
            return FlextResult[None].fail("Client has no channel to disconnect")

        # Transition: ready → shutdown
        disconnect_result = client.channel.disconnect()
        if disconnect_result.is_failure:
            return FlextResult[None].fail(
                f"Channel disconnection failed: {disconnect_result.error}",
            )

        if disconnect_result.data is None:
            return FlextResult[None].fail("Failed to get disconnected channel data")

        # Update client with disconnected channel
        return client.copy_with(channel=disconnect_result.data)

    def _make_call(
        self,
        client: TGrpcClientEntity,
        method: str,
        request: object,
    ) -> FlextResult[TMethodCallResult]:
        """Execute remote method call."""
        if not client.is_connected:
            return FlextResult[None].fail(
                f"Cannot make call with disconnected client: {client.target or 'no target'}",
            )

        # In real implementation, execute actual gRPC call
        response = {"method": method, "status": "success", "data": request}
        return FlextResult[None].ok(response)

    def _get_status(self, client: TGrpcClientEntity) -> FlextResult[dict[str, object]]:
        """Get client status information."""
        status: dict[str, object] = {
            "channel_state": client.channel.state if client.channel else "no_channel",
            "target": client.target,
            "is_connected": client.is_connected,
        }
        return FlextResult[None].ok(status)


class FlextGrpcStreamService:
    """gRPC stream domain service for streaming operations.

    Implements business logic for gRPC streaming operations including stream
    creation, data flow management, and stream lifecycle operations.

    Commands:
      - create: Create new gRPC stream
      - send: Send data through stream
      - close: Close stream gracefully

    """

    def execute(
        self,
        command: str,
        stream: TGrpcStreamEntity,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[TGrpcStreamEntity | TMethodCallResult]:
        """Execute stream command with validation and error handling."""
        # Validate stream entity
        validation = stream.validate_business_rules()
        if validation.is_failure:
            return FlextResult[None].fail(f"Stream validation failed: {validation.error}")

        # Execute command
        if command == "create":
            result = self._create_stream(stream)
            return cast("FlextResult[TGrpcStreamEntity | TMethodCallResult]", result)
        if command == "send":
            data = args[0] if args else kwargs.get("data")
            send_result = self._send_data(stream, data)
            return cast(
                "FlextResult[TGrpcStreamEntity | TMethodCallResult]",
                send_result,
            )
        if command == "close":
            result = self._close_stream(stream)
            return cast("FlextResult[TGrpcStreamEntity | TMethodCallResult]", result)
        return FlextResult[None].fail(f"Unknown stream command: {command}")

    def _create_stream(
        self,
        stream: TGrpcStreamEntity,
    ) -> FlextResult[TGrpcStreamEntity]:
        """Create gRPC stream."""
        # In real implementation, create actual gRPC stream
        return FlextResult[None].ok(stream)

    def _send_data(
        self,
        stream: TGrpcStreamEntity,
        data: object,
    ) -> FlextResult[TMethodCallResult]:
        """Send data through stream."""
        # In real implementation, send data through gRPC stream
        return FlextResult[None].ok({"sent": data, "stream_type": stream.stream_type})

    def _close_stream(
        self,
        stream: TGrpcStreamEntity,
    ) -> FlextResult[TGrpcStreamEntity]:
        """Close stream gracefully."""
        # In real implementation, close actual gRPC stream
        return FlextResult[None].ok(stream)


# =============================================================================
# GRPC PLATFORM FACADE
# =============================================================================


class FlextGrpcPlatform:
    """Unified gRPC platform facade for simplified operations.

    Provides high-level interface for gRPC platform operations, abstracting
    complexity of individual services and providing enterprise-grade patterns
    for common gRPC communication scenarios.

    Features:
      - Simplified server and client lifecycle management
      - Unified error handling and logging
      - Integration with global dependency injection container
      - Enterprise patterns for service orchestration

    Example:
      >>> platform = FlextGrpcPlatform()
      >>> server_result = platform.start_server(server)
      >>> if server_result.success:
      ...     client_result = platform.connect_client(client)
      ...     if client_result.success:
      ...         response = platform.make_call(client_result.data, "GetData", {})

    """

    def __init__(self, container: FlextContainer | None = None) -> None:
        """Initialize platform with optional container."""
        self._container = container or get_flext_container()
        self._server_service = FlextGrpcServerService()
        self._client_service = FlextGrpcClientService()
        self._stream_service = FlextGrpcStreamService()

    def start_server(
        self,
        server: TGrpcServerEntity,
    ) -> FlextResult[TGrpcServerEntity | dict[str, object]]:
        """Start gRPC server with comprehensive lifecycle management."""
        return self._server_service.execute("start", server)

    def stop_server(
        self,
        server: TGrpcServerEntity,
    ) -> FlextResult[TGrpcServerEntity | dict[str, object]]:
        """Stop gRPC server with graceful shutdown."""
        return self._server_service.execute("stop", server)

    def connect_client(
        self,
        client: TGrpcClientEntity,
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]:
        """Connect gRPC client with connection management."""
        return self._client_service.execute("connect", client)

    def disconnect_client(
        self,
        client: TGrpcClientEntity,
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]:
        """Disconnect gRPC client with graceful shutdown."""
        return self._client_service.execute("disconnect", client)

    def make_call(
        self,
        client: TGrpcClientEntity,
        method: str,
        request: object,
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]:
        """Execute remote method call through client."""
        return self._client_service.execute("call", client, method, request)

    def create_stream(
        self,
        stream: TGrpcStreamEntity,
    ) -> FlextResult[TGrpcStreamEntity | TMethodCallResult]:
        """Create gRPC stream for streaming operations."""
        return self._stream_service.execute("create", stream)

    def get_server_status(
        self,
        server: TGrpcServerEntity,
    ) -> FlextResult[dict[str, object]]:
        """Get comprehensive server status information."""
        result = self._server_service.execute("status", server)
        # Cast is safe since status command always returns dict[str, object]
        return cast("FlextResult[dict[str, object]]", result)

    def get_client_status(
        self,
        client: TGrpcClientEntity,
    ) -> FlextResult[dict[str, object]]:
        """Get comprehensive client status information."""
        result = self._client_service.execute("status", client)
        # Cast is safe since status command always returns dict[str, object]
        return cast("FlextResult[dict[str, object]]", result)


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    "FlextGrpcClientService",
    "FlextGrpcPlatform",
    "FlextGrpcServerService",
    "FlextGrpcStreamService",
]
