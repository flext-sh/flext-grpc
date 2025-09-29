"""FLEXT gRPC Services.

Service implementations for the FLEXT gRPC framework.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
import logging
import threading
import time
from collections import deque
from collections.abc import Callable, Iterator
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Any, Protocol, cast, override

import grpc

from flext_core import (
    FlextConstants,
    FlextResult,
    FlextService,
)
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import (
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService as FlextGrpcServiceEntity,
    FlextGrpcStream,
)

# gRPC streaming constants
from flext_grpc.proto import (
    EchoRequest,
    FlextGrpcServiceStub,
    HealthRequest,
    StreamRequest,
    add_FlextGrpcServiceServicer_to_server,
)
from flext_grpc.real_servicer import create_real_servicer
from flext_grpc.utilities import FlextGrpcUtilities

CLIENT_STREAMING_BUFFER_THRESHOLD = 1000
SERVER_STREAMING_BATCH_SIZE = 100
BIDIRECTIONAL_STREAMING_QUEUE_SIZE = 500
STREAM_CLEANUP_MAX_AGE_SECONDS = 300
STREAM_PROCESSING_TIMEOUT_SECONDS = 30
MAX_CONCURRENT_STREAMS_PER_CLIENT = 10
STREAM_METRICS_COLLECTION_INTERVAL = 60
STREAM_HEALTH_DEGRADED_THRESHOLD = 0.8

# Memory efficiency constants
MAX_BUFFER_SIZE_BYTES = 1024 * 1024  # 1MB
MEMORY_PRESSURE_THRESHOLD = 0.8
BUFFER_CLEANUP_BATCH_SIZE = 100
LOW_MEMORY_THRESHOLD = 0.6
ADAPTIVE_BUFFER_SCALING_FACTOR = 0.5
MEMORY_CLEANUP_INTERVAL_SHORT = 30
MEMORY_CLEANUP_INTERVAL_LONG = 300
HIGH_PRESSURE_RATIO_THRESHOLD = 0.9


# Stream info types for enterprise-grade stream management
# StreamInfo is now imported from FlextGrpcModels - using standardized models
# This class has been replaced by FlextGrpcModels.StreamInfo for consistency  # Last time buffers were cleaned


# Protocol for gRPC objects (since we can't import their types)
class GrpcChannelProtocol(Protocol):
    """Protocol for gRPC channel objects - DEPRECATED: Use FlextGrpcProtocols.ChannelProtocol."""

    def close(self) -> None:
        """Close the gRPC channel - DEPRECATED: Use FlextGrpcProtocols.ChannelProtocol."""


class GrpcServerProtocol(Protocol):
    """Protocol for gRPC server objects - DEPRECATED: Use FlextGrpcProtocols.ServerProtocol."""

    def stop(self, grace: float) -> None:
        """Stop the gRPC server with grace period - DEPRECATED: Use FlextGrpcProtocols.ServerProtocol."""


# Use direct types - no legacy aliases


class FlextGrpcService(
    FlextService[
        FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
    ]
):
    """Single unified gRPC service class following FLEXT standards.

    Contains all gRPC server, client, and streaming functionality.
    Follows FLEXT pattern: one class per module with nested subclasses.
    """

    @override
    def __init__(self, max_servers: int = 10, thread_pool_size: int = 50) -> None:
        """Initialize service with real gRPC server registry and performance optimization.

        Args:
            max_servers: Maximum number of concurrent servers (default: 10)
            thread_pool_size: Thread pool size for gRPC servers (default: 50)

        Returns:
            object: Description of return value.

        """
        super().__init__()
        self._active_servers: dict[str, GrpcServerProtocol] = {}
        self._max_servers = max_servers
        self._thread_pool_size = thread_pool_size
        self._server_metrics: dict[str, dict[str, float]] = {}  # Performance metrics

        # Create shared thread pool for better resource management
        self._thread_pool = ThreadPoolExecutor(
            max_workers=thread_pool_size,
            thread_name_prefix="flext-grpc-server",
        )

        # Initialize client service attributes
        self._active_channels: dict[str, GrpcChannelProtocol] = {}
        self._connection_timeout: float = 5.0
        self._max_retry_attempts: int = 3
        self._client_metrics: dict[str, dict[str, object]] = {}

        # Initialize stream service attributes
        self._active_streams: dict[str, dict[str, object]] = {}
        self._max_concurrent_streams: int = MAX_CONCURRENT_STREAMS_PER_CLIENT
        self._stream_buffer_size: int = BIDIRECTIONAL_STREAMING_QUEUE_SIZE
        self._metrics_interval: float = STREAM_METRICS_COLLECTION_INTERVAL
        self._stream_metrics: dict[str, dict[str, float]] = {}
        self._global_metrics = {
            "total_streams_created": 0,
            "total_streams_active": 0,
            "total_bytes_streamed": 0,
            "average_stream_duration": 0.0,
            "total_memory_used_bytes": 0,
            "memory_pressure_score": 0.0,
            "buffers_cleaned_up": 0,
        }
        self._metrics_thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()
        self._metrics_lock = threading.RLock()

        # Start background metrics collection
        self._start_metrics_collection()

    @override
    def execute(
        self,
        command: str | None = None,
        entity: FlextGrpcServer
        | FlextGrpcClient
        | FlextGrpcStream
        | dict[str, object]
        | None = None,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[
        FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
    ]:
        """Execute command with validation and error handling for any gRPC entity."""
        if command is None:
            return FlextResult[
                FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
            ].ok({
                "status": "ready",
                "service": "flext-grpc-service",
            })

        if entity is None:
            return FlextResult[
                FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
            ].fail("Entity instance required")

        # Route to appropriate handler based on entity type
        if isinstance(entity, FlextGrpcServer):
            # Validate server entity
            validation = entity.validate_business_rules()
            if validation.is_failure:
                return FlextResult[
                    FlextGrpcServer
                    | FlextGrpcClient
                    | FlextGrpcStream
                    | dict[str, object]
                ].fail(
                    f"Server validation failed: {validation.error}",
                )

            # Command mapping for server operations
            if command == "start":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._start_server(entity),
                )
            if command == "stop":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._stop_server(entity),
                )
            if command == "status":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._get_status(entity),
                )
            if command == "add_service":
                service_def = args[0] if args else kwargs.get("service")
                if not isinstance(service_def, FlextGrpcServiceEntity):
                    return FlextResult[
                        FlextGrpcServer
                        | FlextGrpcClient
                        | FlextGrpcStream
                        | dict[str, object]
                    ].fail(
                        f"Service definition must be FlextGrpcServiceEntity, got: {type(service_def)}",
                    )
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._add_service(entity, service_def),
                )
            return FlextResult[
                FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
            ].fail(
                f"Unknown server command: {command}",
            )
        if isinstance(entity, FlextGrpcClient):
            # Validate client entity
            validation = entity.validate_business_rules()
            if validation.is_failure:
                return FlextResult[
                    FlextGrpcServer
                    | FlextGrpcClient
                    | FlextGrpcStream
                    | dict[str, object]
                ].fail(
                    f"Client validation failed: {validation.error}",
                )

            # Command mapping for client operations
            if command == "connect":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._connect_client(entity),
                )
            if command == "disconnect":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._disconnect_client(entity),
                )
            if command == "status":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._get_client_status(entity),
                )
            if command == "call":
                method_name = args[0] if args else kwargs.get("method_name", "")
                if not isinstance(method_name, str) or not method_name.strip():
                    return FlextResult[
                        FlextGrpcServer
                        | FlextGrpcClient
                        | FlextGrpcStream
                        | dict[str, object]
                    ].fail("Method name must be a string")
                request = kwargs.get(
                    "request",
                    kwargs.get(
                        "message", args[1] if len(args) > 1 else "default_request"
                    ),
                )
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._make_call(entity, method_name, request),
                )
            return FlextResult[
                FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
            ].fail(
                f"Unknown client command: {command}",
            )
        if isinstance(entity, FlextGrpcStream):
            # Validate stream entity
            validation = entity.validate_business_rules()
            if validation.is_failure:
                return FlextResult[
                    FlextGrpcServer
                    | FlextGrpcClient
                    | FlextGrpcStream
                    | dict[str, object]
                ].fail(
                    f"Stream validation failed: {validation.error}",
                )

            # Command mapping for stream operations
            if command == "create":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._create_stream(entity),
                )
            if command == "send":
                data = args[0] if args else kwargs.get("data", {})
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._send_data(entity, data),
                )
            if command == "close":
                return cast(
                    "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]]",
                    self._close_stream(entity),
                )
            return FlextResult[
                FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
            ].fail(
                f"Unknown stream command: {command}",
            )
        return FlextResult[
            FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
        ].fail(f"Unsupported entity type: {type(entity)}")

    def _start_server(
        self,
        server: FlextGrpcServer,
    ) -> FlextResult[FlextGrpcServer]:
        """Start server with REAL gRPC server implementation and performance optimization."""
        # Check server limit for resource management
        if len(self._active_servers) >= self._max_servers:
            return FlextResult[FlextGrpcServer].fail(
                f"Maximum server limit reached ({self._max_servers}). "
                "Stop some servers or increase max_servers limit.",
            )

        # Record start time for metrics
        self._startup_start_time = time.time()

        # Transition: stopped → starting
        start_result: FlextResult[FlextGrpcServer] = server.start()
        if start_result.is_failure:
            return start_result

        starting_server = start_result.unwrap()
        return self._create_and_start_grpc_server(starting_server)

    def _create_and_start_grpc_server(
        self,
        starting_server: FlextGrpcServer,
    ) -> FlextResult[FlextGrpcServer]:
        """Create and start the actual gRPC server."""
        server_key = f"{starting_server.host}:{starting_server.port}"

        try:
            # Create REAL gRPC server
            grpc_server = grpc.server(
                ThreadPoolExecutor(max_workers=starting_server.max_workers),
            )

            # Configure port binding
            port_result: FlextResult[FlextGrpcServer] = self._configure_server_port(
                grpc_server, starting_server
            )
            if port_result.is_failure:
                grpc_server.stop(grace=1.0)
                return port_result

            configured_server: FlextGrpcServer = port_result.unwrap()
            server_key = f"{configured_server.host}:{configured_server.port}"

            # Start the REAL gRPC server
            try:
                grpc_server.start()
            except Exception as e:
                return FlextResult[FlextGrpcServer].fail(
                    f"Failed to start gRPC server on {configured_server.host}:{configured_server.port}: {e}",
                )

            # Store and transition to running
            return self._finalize_server_startup(
                grpc_server,
                configured_server,
                server_key,
            )

        except Exception as e:
            return FlextResult[FlextGrpcServer].fail(
                f"Failed to start gRPC server: {e}",
            )

    def _configure_server_port(
        self,
        grpc_server: grpc.Server,
        starting_server: FlextGrpcServer,
    ) -> FlextResult[FlextGrpcServer]:
        """Configure server port binding."""
        if starting_server.port == 0:
            # Let gRPC choose available port
            actual_port = grpc_server.add_insecure_port(f"{starting_server.host}:0")
            # Update entity with actual port
            updated_server = starting_server.model_copy(update={"port": actual_port})
            return FlextResult[FlextGrpcServer].ok(updated_server)
        # Use specified port
        try:
            grpc_server.add_insecure_port(
                f"{starting_server.host}:{starting_server.port}",
            )
            return FlextResult[FlextGrpcServer].ok(starting_server)
        except Exception as e:
            return FlextResult[FlextGrpcServer].fail(
                f"Failed to bind to {starting_server.host}:{starting_server.port}: {e}",
            )

    def _finalize_server_startup(
        self,
        grpc_server: object,
        configured_server: FlextGrpcServer,
        server_key: str,
    ) -> FlextResult[FlextGrpcServer]:
        """Finalize server startup and transition to running state."""
        # Store the real server for lifecycle management
        self._active_servers[server_key] = cast("GrpcServerProtocol", grpc_server)

        # Transition: starting → running
        running_result: FlextResult[FlextGrpcServer] = configured_server.mark_running()
        if running_result.is_failure:
            # Cleanup on failure
            cast("GrpcServerProtocol", grpc_server).stop(grace=1.0)
            self._active_servers.pop(server_key, None)
            return running_result

        # Record performance metrics
        startup_time = time.time() - getattr(self, "_startup_start_time", time.time())
        self._server_metrics[server_key] = {
            "startup_time": startup_time,
            "started_at": time.time(),
            "connection_count": 0.0,
            "request_count": 0.0,
        }

        return FlextResult[FlextGrpcServer].ok(running_result.unwrap())

    def _stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop server with REAL gRPC server shutdown."""
        # Transition: running → stopping
        stop_result: FlextResult[FlextGrpcServer] = server.stop()
        if stop_result.is_failure:
            return stop_result

        stopping_server = stop_result.unwrap()
        server_key = f"{stopping_server.host}:{stopping_server.port}"

        try:
            # Stop REAL gRPC server if it exists
            if server_key in self._active_servers:
                grpc_server = self._active_servers[server_key]
                grpc_server.stop(grace=2.0)  # Graceful shutdown

                # Remove from active servers
                del self._active_servers[server_key]

                # Clean up performance metrics
                self._server_metrics.pop(server_key, None)

            # Transition: stopping → stopped
            stopped_result = stopping_server.mark_stopped()
            if stopped_result.is_failure:
                return stopped_result

            return stopped_result

        except Exception as e:
            return FlextResult[FlextGrpcServer].fail(
                f"Failed to stop gRPC server: {e}",
            )

    def _add_service(
        self,
        server: FlextGrpcServer,
        service_def: FlextGrpcServiceEntity,
    ) -> FlextResult[FlextGrpcServer]:
        """Add REAL gRPC service to server."""
        if server.state != "running":
            return FlextResult[FlextGrpcServer].fail(
                f"Cannot add service to server in state: {server.state}",
            )

        server_key = f"{server.host}:{server.port}"

        try:
            # Get the REAL gRPC server
            if server_key not in self._active_servers:
                return FlextResult[FlextGrpcServer].fail(
                    f"No active gRPC server found for {server_key}",
                )

            grpc_server = self._active_servers[server_key]

            # Create REAL servicer and register it with the server
            real_servicer = create_real_servicer(f"{server.host}:{server.port}")
            add_FlextGrpcServiceServicer_to_server(
                real_servicer, cast("grpc.Server", grpc_server)
            )

            # Add service to server entity (tracks the registration)
            add_result: FlextResult[FlextGrpcServer] = server.add_service(service_def)
            if add_result.is_failure:
                return add_result

            return FlextResult[FlextGrpcServer].ok(add_result.unwrap())

        except Exception as e:
            return FlextResult[FlextGrpcServer].fail(
                f"Failed to add service to gRPC server: {e}",
            )

    def _get_status(
        self,
        server: FlextGrpcServer,
    ) -> FlextResult[dict[str, object]]:
        """Get server status information including REAL gRPC server status."""
        server_key = f"{server.host}:{server.port}"

        # Check if we have a real gRPC server running

        # Include performance metrics if available
        metrics: dict[str, float] = self._server_metrics.get(server_key, {})
        current_time = time.time()

        status: dict[str, object] = {
            "state": server.state,
            "host": server.host,
            "port": server.port,
            "max_workers": server.max_workers,
            "address": server.address,
            "is_running": server.is_running,
            "service_count": len(server.services),
            "grpc_server_active": "grpc_server_active",
            "server_key": "server_key",
            # Performance metrics
            "metrics": {
                "startup_time_seconds": metrics.get("startup_time", 0.0),
                "uptime_seconds": current_time
                - metrics.get("started_at", current_time),
                "connection_count": metrics.get("connection_count", 0),
                "request_count": metrics.get("request_count", 0),
                "thread_pool_size": self._thread_pool_size,
                "active_servers": len(self._active_servers),
                "max_servers": self._max_servers,
            },
        }
        return FlextResult[dict[str, object]].ok(status)

    # Client service operations (previously FlextGrpcClientService) - unified pattern
    class _ClientServiceHelper:
        """Nested helper class for gRPC client service operations."""

        @staticmethod
        def execute_client_operation(
            service: FlextGrpcService,
            command: str,
            client: FlextGrpcClient,
            *args: object,
            **kwargs: object,
        ) -> FlextResult[FlextGrpcClient | dict[str, object]]:
            """Execute client command with validation and error handling."""
            # Validate client entity
            validation = client.validate_business_rules()
            if validation.is_failure:
                return FlextResult[FlextGrpcClient | dict[str, object]].fail(
                    f"Client validation failed: {validation.error}"
                )

            # Command mapping to reduce return statements
            command_handlers: dict[
                str,
                Callable[
                    [],
                    FlextResult[FlextGrpcClient | dict[str, object]],
                ],
            ] = {
                "connect": lambda: cast(
                    "FlextResult[FlextGrpcClient | dict[str, object]]",
                    service._connect_client(client),
                ),
                "disconnect": lambda: cast(
                    "FlextResult[FlextGrpcClient | dict[str, object]]",
                    service._disconnect_client(client),
                ),
                "status": lambda: cast(
                    "FlextResult[FlextGrpcClient | dict[str, object]]",
                    service._get_client_status(client),
                ),
            }

            # Handle call command with validation
            if command == "call":
                method_name = args[0] if args else kwargs.get("method")
                request = args[1] if len(args) > 1 else kwargs.get("request")
                if not isinstance(method_name, str):
                    return FlextResult[FlextGrpcClient | dict[str, object]].fail(
                        f"Method name must be string, got: {type(method_name)}"
                    )
                return cast(
                    "FlextResult[FlextGrpcClient | dict[str, object]]",
                    service._make_call(client, method_name, request),
                )

            # Execute mapped commands
            if command in command_handlers:
                handler = command_handlers[command]
                return handler()

            return FlextResult[FlextGrpcClient | dict[str, object]].fail(
                f"Unknown client command: {command}"
            )

    def execute_client_command(
        self,
        command: str,
        client: FlextGrpcClient,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[FlextGrpcClient | dict[str, object]]:
        """Execute client command using nested helper."""
        return self._ClientServiceHelper.execute_client_operation(
            self, command, client, *args, **kwargs
        )

    def _connect_client(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[FlextGrpcClient]:
        """Connect client with REAL gRPC channel establishment."""
        # Validate client preconditions
        validation_result: FlextResult[FlextGrpcClient] = (
            self._validate_client_for_connection(client)
        )
        if validation_result.is_failure:
            return validation_result

        target = client.target
        if target is None:
            return FlextResult[FlextGrpcClient].fail("Client target cannot be None")

        try:
            # Create and test gRPC channel
            channel_result: FlextResult[object] = self._create_and_test_grpc_channel(
                target
            )
            if channel_result.is_failure:
                return FlextResult[FlextGrpcClient].fail(
                    channel_result.error or "Channel creation failed",
                )

            grpc_channel = channel_result.unwrap()
            # Transition client to connected state
            return self._transition_client_to_connected(client, grpc_channel, target)

        except Exception as e:
            return FlextResult[FlextGrpcClient].fail(
                f"Failed to establish gRPC connection: {e}",
            )

    def _validate_client_for_connection(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[FlextGrpcClient]:
        """Validate client preconditions for connection."""
        if client.channel is None:
            return FlextResult[FlextGrpcClient].fail(
                "Client has no channel to connect",
            )

        if client.target is None:
            return FlextResult[FlextGrpcClient].fail(
                "Client has no target to connect to",
            )

        return FlextResult[FlextGrpcClient].ok(client)

    def _create_and_test_grpc_channel(self, target: str) -> FlextResult[object]:
        """Create gRPC channel and test connectivity."""
        # Retry connection with exponential backoff
        for attempt in range(self._max_retry_attempts):
            grpc_channel = None
            try:
                # Create REAL gRPC channel
                grpc_channel = grpc.insecure_channel(target)

                # Test connectivity with configurable timeout
                grpc.channel_ready_future(grpc_channel).result(
                    timeout=self._connection_timeout,
                )

                # Record successful connection metrics
                self._client_metrics[target] = {
                    "connected_at": time.time(),
                    "connection_attempt": attempt + 1,
                    "total_requests": 0,
                    "failed_requests": 0,
                }

                return FlextResult[object].ok(grpc_channel)

            except grpc.FutureTimeoutError:
                if grpc_channel is not None:
                    grpc_channel.close()

                # If this is the last attempt, fail
                if attempt == self._max_retry_attempts - 1:
                    return FlextResult[object].fail(
                        f"Failed to connect to {target}: connection timeout after {self._max_retry_attempts} attempts",
                    )

                # Wait before retrying with exponential backoff
                wait_time = (2**attempt) * 0.5  # 0.5s, 1s, 2s, etc.
                time.sleep(wait_time)

        # This should never be reached due to the logic above, but for type safety
        return FlextResult[object].fail(f"Connection failed unexpectedly to {target}")

    def _transition_client_to_connected(
        self,
        client: FlextGrpcClient,
        grpc_channel: object,
        target: str,
    ) -> FlextResult[FlextGrpcClient]:
        """Transition client channel states to connected."""
        # Store the real channel for lifecycle management
        self._active_channels[target] = cast("GrpcChannelProtocol", grpc_channel)

        # Transition: idle → connecting
        if client.channel is None:
            return FlextResult[FlextGrpcClient].fail("Client channel cannot be None")
        connect_result = client.channel.connect()
        if connect_result.is_failure:
            cast("GrpcChannelProtocol", grpc_channel).close()
            self._active_channels.pop(target, None)
            return FlextResult[FlextGrpcClient].fail(
                f"Channel connection failed: {connect_result.error}",
            )

        connecting_channel = connect_result.unwrap()
        # Transition: connecting → ready
        ready_result = connecting_channel.mark_ready()
        if ready_result.is_failure:
            cast("GrpcChannelProtocol", grpc_channel).close()
            self._active_channels.pop(target, None)
            return FlextResult[FlextGrpcClient].fail(
                f"Channel ready transition failed: {ready_result.error}",
            )

        # Update client with new channel
        updated_client = client.model_copy(update={"channel": ready_result.unwrap()})
        return FlextResult[FlextGrpcClient].ok(updated_client)

    def _disconnect_client(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[FlextGrpcClient]:
        """Disconnect client with REAL gRPC channel closure."""
        # Check if client has a channel
        if client.channel is None:
            return FlextResult[FlextGrpcClient].fail(
                "Client has no channel to disconnect",
            )

        target = client.target
        if target is None:
            return FlextResult[FlextGrpcClient].fail(
                "Client has no target to disconnect from",
            )

        try:
            # Close REAL gRPC channel if it exists
            if target in self._active_channels:
                grpc_channel = self._active_channels[target]
                grpc_channel.close()

                # Remove from active channels
                del self._active_channels[target]

            # Transition: ready → shutdown
            disconnect_result = client.channel.disconnect()
            if disconnect_result.is_failure:
                return FlextResult[FlextGrpcClient].fail(
                    f"Channel disconnection failed: {disconnect_result.error}",
                )

            # Update client with disconnected channel
            updated_client = client.model_copy(
                update={"channel": disconnect_result.unwrap()}
            )
            return FlextResult[FlextGrpcClient].ok(updated_client)

        except Exception as e:
            return FlextResult[FlextGrpcClient].fail(
                f"Failed to disconnect gRPC client: {e}",
            )

    def _make_call(
        self,
        client: FlextGrpcClient,
        method: str,
        request: object,
    ) -> FlextResult[dict[str, object]]:
        """Execute gRPC method call."""
        if not client.is_connected:
            return FlextResult[dict[str, object]].fail(
                f"Cannot make call with disconnected client: {client.target or 'no target'}",
            )

        target = client.target
        if target is None:
            return FlextResult[dict[str, object]].fail(
                "Client has no target for method call",
            )

        try:
            # Get REAL gRPC channel
            if target not in self._active_channels:
                return FlextResult[dict[str, object]].fail(
                    f"No active gRPC channel for {target}",
                )

            grpc_channel = self._active_channels[target]

            # Validate channel is still ready
            try:
                grpc.channel_ready_future(cast("grpc.Channel", grpc_channel)).result(
                    timeout=1.0,
                )
            except grpc.FutureTimeoutError:
                return FlextResult[dict[str, object]].fail(
                    f"gRPC channel not ready for {target}",
                )

            # Create REAL gRPC stub and make REAL call
            stub = FlextGrpcServiceStub(cast("grpc.Channel", grpc_channel))

            # Handle different method types - REAL gRPC calls
            if method == "Echo":
                # Prepare real Echo request
                if isinstance(request, dict):
                    echo_request = EchoRequest(
                        message=str(request.get("message", "test")),
                        metadata=request.get("metadata", {}),
                    )
                else:
                    echo_request = EchoRequest(message=str(request))

                # Make REAL gRPC call
                grpc_response = stub.Echo(cast("Any", echo_request))

                # Convert to result format
                response = {
                    "method": "Echo",
                    "status": "success",
                    "message": grpc_response.message,
                    "server_id": grpc_response.server_id,
                    "timestamp": grpc_response.timestamp,
                    "target": "target",
                    "channel_ready": "True",
                }

            elif method == "HealthCheck":
                health_request = HealthRequest(service="FlextGrpcService")
                health_response = stub.HealthCheck(cast("Any", health_request))

                response = {
                    "method": "HealthCheck",
                    "status": "success",
                    "serving_status": health_response.status,
                    "message": health_response.message,
                    "target": "target",
                    "channel_ready": "True",
                }

            else:
                # For other methods, create a generic Echo call
                echo_request = EchoRequest(message=f"Method: {method}")
                grpc_response = stub.Echo(cast("Any", echo_request))

                response = {
                    "method": "method",
                    "status": "success",
                    "message": grpc_response.message,
                    "server_id": grpc_response.server_id,
                    "timestamp": grpc_response.timestamp,
                    "target": "target",
                    "channel_ready": "True",
                }

            return FlextResult[dict[str, object]].ok(
                cast("dict[str, object]", response)
            )

        except grpc.RpcError as rpc_error:
            return FlextResult[dict[str, object]].fail(
                f"gRPC call failed: {rpc_error.code()} - {rpc_error.details()}",
            )
        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Failed to make gRPC call: {e}")

    def _get_client_status(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[dict[str, object]]:
        """Get client status information including REAL gRPC channel status."""
        target = client.target

        # Check if we have a real gRPC channel active
        grpc_channel_active = target is not None and target in self._active_channels

        if grpc_channel_active and target is not None:
            grpc_channel = self._active_channels[target]
            with contextlib.suppress(grpc.FutureTimeoutError):
                grpc.channel_ready_future(cast("grpc.Channel", grpc_channel)).result(
                    timeout=0.1,
                )

        status: dict[str, object] = {
            "channel_state": client.channel.state if client.channel else "no_channel",
            "target": client.target,
            "is_connected": client.is_connected,
            "grpc_channel_active": "grpc_channel_active",
            "grpc_channel_ready": "grpc_channel_ready",
        }
        return FlextResult[dict[str, object]].ok(status)

    # Stream service operations (previously FlextGrpcStreamService) - unified pattern
    class _StreamServiceHelper:
        """Nested helper class for gRPC stream service operations."""

        @staticmethod
        def execute_stream_operation(
            service: FlextGrpcService,
            command: str,
            stream: FlextGrpcStream,
            *args: object,
            **kwargs: object,
        ) -> FlextResult[FlextGrpcStream | dict[str, object]]:
            """Execute stream command with validation and error handling."""
            # Validate stream entity
            validation = stream.validate_business_rules()
            if validation.is_failure:
                return FlextResult[FlextGrpcStream | dict[str, object]].fail(
                    f"Stream validation failed: {validation.error}",
                )

            # Execute command
            if command == "create":
                target = args[0] if args else kwargs.get("target")
                if target is not None and not isinstance(target, str):
                    return FlextResult[FlextGrpcStream | dict[str, object]].fail(
                        f"Target must be string, got: {type(target)}",
                    )
                result: FlextResult[FlextGrpcStream] = service._create_stream(
                    stream, target
                )
                return cast("FlextResult[FlextGrpcStream | dict[str, object]]", result)
            if command == "send":
                data = args[0] if args else kwargs.get("data")
                return cast(
                    "FlextResult[FlextGrpcStream | dict[str, object]]",
                    service._send_data(stream, data),
                )
            if command == "close":
                return cast(
                    "FlextResult[FlextGrpcStream | dict[str, object]]",
                    service._close_stream(stream),
                )
            return FlextResult[FlextGrpcStream | dict[str, object]].fail(
                f"Unknown stream command: {command}",
            )

    def execute_stream_command(
        self,
        command: str,
        stream: FlextGrpcStream,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[FlextGrpcStream | dict[str, object]]:
        """Execute stream command using nested helper."""
        return self._StreamServiceHelper.execute_stream_operation(
            self, command, stream, *args, **kwargs
        )

    def _start_metrics_collection(self) -> None:
        """Start background metrics collection thread."""
        if self._metrics_thread is None or not self._metrics_thread.is_alive():
            self._metrics_thread = threading.Thread(
                target=self._collect_metrics_loop,
                daemon=True,
                name="flext-grpc-metrics",
            )
            self._metrics_thread.start()

    def _collect_metrics_loop(self) -> None:
        """Background metrics collection loop."""
        while not self._shutdown_event.wait(self._metrics_interval):
            try:
                with self._metrics_lock:
                    self._update_global_metrics()
            except Exception as e:
                # Log error in background thread instead of silent pass
                logger = logging.getLogger(__name__)
                logger.warning(f"Background metrics collection failed: {e}")

    def _update_global_metrics(self) -> None:
        """Update global streaming metrics."""
        self._global_metrics["total_streams_active"] = len(self._active_streams)

        # Calculate memory usage
        total_memory = 0
        for stream_info in self._active_streams.values():
            if isinstance(stream_info, dict):
                buffer_size = stream_info.get("buffer_size_bytes", 0)
                if isinstance(buffer_size, (int, float)):
                    total_memory += int(buffer_size)

        self._global_metrics["total_memory_used_bytes"] = total_memory
        self._global_metrics["memory_pressure_score"] = (
            FlextGrpcUtilities.SystemUtilities.get_system_memory_usage()
        )

    def _create_stream(
        self,
        stream: FlextGrpcStream,
        target: str | None = None,
    ) -> FlextResult[FlextGrpcStream]:
        """Create REAL gRPC stream."""
        stream_key = f"{stream.id}_{stream.stream_type}"

        try:
            # For real streaming, we need a target server
            if target is None:
                target = f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}"  # Default target

            # Create real gRPC channel if not exists
            if target not in self._active_channels:
                grpc_channel = grpc.insecure_channel(target)
                self._active_channels[target] = cast(
                    "GrpcChannelProtocol",
                    grpc_channel,
                )

            grpc_channel = cast("grpc.Channel", self._active_channels[target])

            # Create real gRPC stub for streaming
            grpc_stub = FlextGrpcServiceStub(grpc_channel)

            # Register the REAL stream with actual gRPC objects and buffers
            # Use dict instead of StreamInfo TypedDict for flexibility
            stream_info: dict[str, object] = {
                "stream_id": stream.id,
                "type": stream.stream_type,
                "created_at": stream.created_at.timestamp(),
                "active": True,
                "target": target,
                "stub": grpc_stub,  # Real gRPC stub
                "channel": grpc_channel,  # Real gRPC channel
                "request_buffer": [],  # Buffer for client streaming
                "request_queue": Queue(
                    maxsize=BIDIRECTIONAL_STREAMING_QUEUE_SIZE,
                ),  # Thread-safe queue
                "response_buffer": deque(
                    maxlen=SERVER_STREAMING_BATCH_SIZE,
                ),  # Circular buffer
                "sequence_counter": 0,
                "last_activity": time.time(),
                "total_requests_sent": 0,
                "total_responses_received": 0,
                "bytes_sent": 0,
                "bytes_received": 0,
                "error_count": 0,
                "average_latency_ms": 0.0,
                "processing_lock": threading.Lock(),
                "is_processing": False,
                "max_queue_size": BIDIRECTIONAL_STREAMING_QUEUE_SIZE,
                "current_queue_size": 0,
                "health_status": "healthy",
                "last_health_check": time.time(),
                "buffer_size_bytes": 0,
                "max_buffer_size_bytes": MAX_BUFFER_SIZE_BYTES,
                "memory_pressure_score": 0.0,
                "last_memory_cleanup": time.time(),
            }
            self._active_streams[stream_key] = stream_info

            return FlextResult[FlextGrpcStream].ok(stream)

        except Exception as e:
            return FlextResult[FlextGrpcStream].fail(
                f"Failed to create gRPC stream: {e}",
            )

    def _send_data(
        self, stream: FlextGrpcStream, data: object
    ) -> FlextResult[dict[str, object]]:
        """Send data through gRPC stream."""
        stream_key = f"{stream.id}_{stream.stream_type}"

        if stream_key not in self._active_streams:
            return FlextResult[dict[str, object]].fail(
                f"Stream {stream_key} not found or not active"
            )

        stream_info = self._active_streams[stream_key]

        try:
            # Create stream request
            sequence_counter = stream_info.get("sequence_counter", 0)
            if not isinstance(sequence_counter, int):
                sequence_counter = 0
            stream_request = StreamRequest(data=str(data), sequence=sequence_counter)

            # Handle different stream types
            if stream.stream_type == "client_streaming":
                return self._handle_client_streaming(
                    stream,
                    stream_info,
                    stream_request,
                    data,
                    cast("FlextGrpcServiceStub", stream_info.get("stub")),
                )
            if stream.stream_type == "server_streaming":
                return self._handle_server_streaming(
                    stream,
                    stream_info,
                    stream_request,
                    data,
                    cast("FlextGrpcServiceStub", stream_info.get("stub")),
                )
            # For other stream types, create a basic response
            result = {
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "sequence": stream_info.get("sequence_counter", 0),
            }
            return FlextResult[dict[str, object]].ok(cast("dict[str, object]", result))

        except Exception as e:
            return FlextResult[dict[str, object]].fail(
                f"Failed to send data through stream: {e}"
            )

    def _close_stream(self, stream: FlextGrpcStream) -> FlextResult[FlextGrpcStream]:
        """Close gRPC stream."""
        stream_key = f"{stream.id}_{stream.stream_type}"

        if stream_key in self._active_streams:
            # Clean up stream resources
            del self._active_streams[stream_key]

        return FlextResult[FlextGrpcStream].ok(stream)

    def _handle_client_streaming(
        self,
        stream: FlextGrpcStream,
        stream_info: dict[str, object],
        stream_request: object,
        data: object,
        stub: FlextGrpcServiceStub,
    ) -> FlextResult[dict[str, object]]:
        """Handle client streaming with memory optimization."""
        # Check memory pressure before adding to buffer
        request_buffer = stream_info.get("request_buffer", [])
        if not isinstance(request_buffer, list):
            return FlextResult[dict[str, object]].fail("Invalid request buffer type")
        current_buffer_size = FlextGrpcUtilities.SystemUtilities.get_buffer_size_bytes(
            request_buffer
        )
        system_memory = FlextGrpcUtilities.SystemUtilities.get_system_memory_usage()

        # Update memory tracking
        stream_info["buffer_size_bytes"] = current_buffer_size
        stream_info["memory_pressure_score"] = system_memory

        # Check if we need to trigger early flush due to memory pressure
        should_flush_early = (
            current_buffer_size > MAX_BUFFER_SIZE_BYTES * ADAPTIVE_BUFFER_SCALING_FACTOR
            or system_memory > MEMORY_PRESSURE_THRESHOLD
        )

        # Add request to buffer for client streaming accumulation
        if not should_flush_early or len(request_buffer) == 0:
            request_buffer.append(stream_request)

        sequence_counter = stream_info.get("sequence_counter", 0)
        if isinstance(sequence_counter, int):
            stream_info["sequence_counter"] = sequence_counter + 1
        else:
            stream_info["sequence_counter"] = 1
        stream_info["last_activity"] = time.time()

        # Send all buffered requests when buffer reaches threshold, explicit flush, or memory pressure
        buffered_requests = request_buffer
        should_flush = (
            len(buffered_requests) >= CLIENT_STREAMING_BUFFER_THRESHOLD
            or str(data) == "__FLUSH_BUFFER__"
            or should_flush_early
        )

        if should_flush:
            # Make real client streaming call with all buffered requests
            response = stub.ClientStream(cast("Iterator[Any]", iter(buffered_requests)))

            # Clear buffer after successful call and trigger memory cleanup if needed
            request_buffer.clear()
            stream_info["last_memory_cleanup"] = time.time()

            # Update memory stats
            stream_info["buffer_size_bytes"] = 0

            # Trigger garbage collection if memory pressure is high
            if system_memory > MEMORY_PRESSURE_THRESHOLD:
                FlextGrpcUtilities.SystemUtilities.trigger_memory_cleanup()

            result = {
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "buffered_count": len(buffered_requests),
                "response": {
                    "data": response.data,
                    "sequence": response.sequence,
                    "server_id": response.server_id,
                    "timestamp": response.timestamp,
                },
            }
        else:
            # Request added to buffer, waiting for more or flush
            sequence_counter = stream_info.get("sequence_counter", 0)
            if not isinstance(sequence_counter, int):
                sequence_counter = 0
            result = {
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "buffer_status": "buffered",
                "buffer_size": len(buffered_requests),
                "sequence": sequence_counter,
            }

        return FlextResult[dict[str, object]].ok(cast("dict[str, object]", result))

    def _handle_server_streaming(
        self,
        stream: FlextGrpcStream,
        stream_info: dict[str, object],
        stream_request: object,
        data: object,
        stub: FlextGrpcServiceStub,
    ) -> FlextResult[dict[str, object]]:
        """Handle server streaming with multiple responses."""
        try:
            # Make real server streaming call
            response_iterator = stub.ServerStream(cast("Any", stream_request))

            # Collect all responses from the stream
            responses = []
            response_count = 0

            for response in response_iterator:
                responses.append({
                    "data": response.data,
                    "sequence": response.sequence,
                    "server_id": response.server_id,
                    "timestamp": response.timestamp,
                })
                response_count += 1

                # Limit responses to prevent infinite loops
                if response_count >= FlextGrpcConstants.MAX_RESPONSE_COUNT:
                    break

            # Update sequence counter
            sequence_counter = stream_info.get("sequence_counter", 0)
            if isinstance(sequence_counter, int):
                stream_info["sequence_counter"] = sequence_counter + 1
            else:
                stream_info["sequence_counter"] = 1

            stream_info["last_activity"] = time.time()

            result = {
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "sequence": stream_info.get("sequence_counter", 0),
                "responses": responses,
                "response_count": response_count,
            }

            return FlextResult[dict[str, object]].ok(cast("dict[str, object]", result))

        except Exception as e:
            return FlextResult[dict[str, object]].fail(f"Server streaming failed: {e}")


# Service aliases for backward compatibility and API consistency
class FlextGrpcServerService(FlextGrpcService):
    """Server-specific gRPC service operations."""

    def __init__(self, max_servers: int = 10, thread_pool_size: int = 50) -> None:
        """Initialize server service."""
        super().__init__(max_servers=max_servers, thread_pool_size=thread_pool_size)

    def execute(
        self,
        command: str | None = None,
        entity: FlextGrpcServer
        | FlextGrpcClient
        | FlextGrpcStream
        | dict[str, object]
        | None = None,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[
        FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
    ]:
        """Execute server-specific commands."""
        if command in {"start", "stop", "restart", "status", "add_service"}:
            return super().execute(command, entity, *args, **kwargs)
        return FlextResult[
            FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
        ].fail(f"Unknown server command: {command}")


class FlextGrpcClientService(FlextGrpcService):
    """Client-specific gRPC service operations."""

    def __init__(self, max_servers: int = 10, thread_pool_size: int = 50) -> None:
        """Initialize client service."""
        super().__init__(max_servers=max_servers, thread_pool_size=thread_pool_size)

    def execute(
        self,
        command: str | None = None,
        entity: FlextGrpcServer
        | FlextGrpcClient
        | FlextGrpcStream
        | dict[str, object]
        | None = None,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[
        FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
    ]:
        """Execute client-specific commands."""
        if command in {"connect", "disconnect", "call", "status"}:
            return super().execute(command, entity, *args, **kwargs)
        return FlextResult[
            FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
        ].fail(f"Unknown client command: {command}")


class FlextGrpcStreamService(FlextGrpcService):
    """Stream-specific gRPC service operations."""

    def __init__(self, max_servers: int = 10, thread_pool_size: int = 50) -> None:
        """Initialize stream service."""
        super().__init__(max_servers=max_servers, thread_pool_size=thread_pool_size)

    def execute(
        self,
        command: str | None = None,
        entity: FlextGrpcServer
        | FlextGrpcClient
        | FlextGrpcStream
        | dict[str, object]
        | None = None,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[
        FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
    ]:
        """Execute stream-specific commands."""
        if command in {"create", "close", "send", "receive", "status"}:
            return super().execute(command, entity, *args, **kwargs)
        return FlextResult[
            FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | dict[str, object]
        ].fail(f"Unknown stream command: {command}")


__all__ = [
    "FlextGrpcClientService",
    "FlextGrpcServerService",
    "FlextGrpcService",
    "FlextGrpcStreamService",
    "GrpcChannelProtocol",
    "GrpcServerProtocol",
]
