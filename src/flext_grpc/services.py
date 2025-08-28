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

import gc
import sys
import threading
import time
from collections import deque
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Protocol, TypedDict, cast

import grpc
import psutil

# Import centralized constants from flext-core to eliminate duplication
from flext_core import FlextConstants, FlextContainer, FlextResult, get_logger

from flext_grpc.entities import (
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)
from flext_grpc.proto import (
    EchoRequest,
    FlextGrpcServiceStub,
    HealthRequest,
    StreamRequest,
    add_FlextGrpcServiceServicer_to_server,
)
from flext_grpc.real_servicer import create_real_servicer

# Use centralized gRPC constants following SOLID DRY principles
CLIENT_STREAMING_BUFFER_THRESHOLD = (
    FlextConstants.GRPC.CLIENT_STREAMING_BUFFER_THRESHOLD
)
SERVER_STREAMING_BATCH_SIZE = FlextConstants.GRPC.SERVER_STREAMING_BATCH_SIZE
BIDIRECTIONAL_STREAMING_QUEUE_SIZE = (
    FlextConstants.GRPC.BIDIRECTIONAL_STREAMING_QUEUE_SIZE
)
STREAM_CLEANUP_MAX_AGE_SECONDS = FlextConstants.GRPC.STREAM_CLEANUP_MAX_AGE_SECONDS
STREAM_PROCESSING_TIMEOUT_SECONDS = (
    FlextConstants.GRPC.STREAM_PROCESSING_TIMEOUT_SECONDS
)
MAX_CONCURRENT_STREAMS_PER_CLIENT = (
    FlextConstants.GRPC.MAX_CONCURRENT_STREAMS_PER_CLIENT
)
STREAM_METRICS_COLLECTION_INTERVAL = (
    FlextConstants.GRPC.STREAM_METRICS_COLLECTION_INTERVAL
)
STREAM_HEALTH_DEGRADED_THRESHOLD = FlextConstants.GRPC.STREAM_HEALTH_DEGRADED_THRESHOLD

# Centralized memory efficiency constants from FlextConstants.GRPC
MAX_BUFFER_SIZE_BYTES = FlextConstants.GRPC.MAX_BUFFER_SIZE_BYTES
MEMORY_PRESSURE_THRESHOLD = FlextConstants.GRPC.MEMORY_PRESSURE_THRESHOLD
BUFFER_CLEANUP_BATCH_SIZE = FlextConstants.GRPC.BUFFER_CLEANUP_BATCH_SIZE
LOW_MEMORY_THRESHOLD = FlextConstants.GRPC.LOW_MEMORY_THRESHOLD
ADAPTIVE_BUFFER_SCALING_FACTOR = FlextConstants.GRPC.ADAPTIVE_BUFFER_SCALING_FACTOR
MEMORY_CLEANUP_INTERVAL_SHORT = FlextConstants.GRPC.MEMORY_CLEANUP_INTERVAL_SHORT
MEMORY_CLEANUP_INTERVAL_LONG = FlextConstants.GRPC.MEMORY_CLEANUP_INTERVAL_LONG
HIGH_PRESSURE_RATIO_THRESHOLD = FlextConstants.GRPC.HIGH_PRESSURE_RATIO_THRESHOLD


# Stream info types for enterprise-grade stream management
class StreamInfo(TypedDict):
    """Enterprise-grade stream information with comprehensive tracking."""

    stream_id: str
    type: str  # stream type
    created_at: float
    active: bool
    target: str
    stub: object  # gRPC stub
    channel: object  # gRPC channel

    # Enterprise buffering and queueing
    request_buffer: list[object]  # Buffer for streaming requests
    request_queue: Queue[object]  # Thread-safe queue for high throughput
    response_buffer: deque[object]  # Circular buffer for responses

    # Performance tracking
    sequence_counter: int
    last_activity: float
    total_requests_sent: int
    total_responses_received: int
    bytes_sent: int
    bytes_received: int
    error_count: int
    average_latency_ms: float

    # Concurrency management
    processing_lock: threading.Lock
    is_processing: bool
    max_queue_size: int
    current_queue_size: int

    # Health monitoring
    health_status: str  # "healthy", "degraded", "unhealthy"
    last_health_check: float

    # Memory efficiency tracking
    buffer_size_bytes: int  # Current buffer memory usage
    max_buffer_size_bytes: int  # Maximum allowed buffer size
    memory_pressure_score: float  # 0.0 to 1.0 pressure indicator
    last_memory_cleanup: float  # Last time buffers were cleaned


# Protocol for gRPC objects (since we can't import their types)
class GrpcChannelProtocol(Protocol):
    """Protocol for gRPC channel objects."""

    def close(self) -> None: ...


class GrpcServerProtocol(Protocol):
    """Protocol for gRPC server objects."""

    def stop(self, grace: float) -> None: ...


# Type aliases for better readability
type TGrpcServerEntity = FlextGrpcServer
type TGrpcClientEntity = FlextGrpcClient
type TGrpcStreamEntity = FlextGrpcStream
type TGrpcServiceDef = FlextGrpcService
type TMethodCallResult = dict[str, object]


# =============================================================================
# MEMORY EFFICIENCY UTILITIES
# =============================================================================


def get_system_memory_usage() -> float:
    """Get current system memory usage as percentage (0.0 to 1.0)."""
    try:
        return psutil.virtual_memory().percent / 100.0
    except Exception:
        # Fallback if psutil fails
        return 0.5  # Assume moderate usage


def get_buffer_size_bytes(buffer: list[object] | deque[object]) -> int:
    """Estimate buffer size in bytes using sys.getsizeof recursively."""
    try:
        total_size = sys.getsizeof(buffer)
        for item in buffer:
            total_size += sys.getsizeof(item)
            # If item is a dict or complex object, add its size
            if hasattr(item, "__dict__"):
                total_size += sys.getsizeof(vars(item))
            elif isinstance(item, dict):
                total_size += sum(
                    sys.getsizeof(k) + sys.getsizeof(v) for k, v in item.items()
                )
        return total_size
    except Exception:
        # Fallback estimation: assume 1KB per item
        return len(buffer) * 1024


def trigger_memory_cleanup() -> None:
    """Trigger garbage collection to free memory."""
    gc.collect()  # Full garbage collection
    gc.collect()  # Run twice for better cleanup


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

    def __init__(self, max_servers: int = 10, thread_pool_size: int = 50) -> None:
        """Initialize service with real gRPC server registry and performance optimization.

        Args:
            max_servers: Maximum number of concurrent servers (default: 10)
            thread_pool_size: Thread pool size for gRPC servers (default: 50)

        """
        self._active_servers: dict[str, GrpcServerProtocol] = {}
        self._max_servers = max_servers
        self._thread_pool_size = thread_pool_size
        self._server_metrics: dict[str, dict[str, float]] = {}  # Performance metrics

        # Create shared thread pool for better resource management
        self._thread_pool = ThreadPoolExecutor(
            max_workers=thread_pool_size, thread_name_prefix="flext-grpc-server"
        )

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
            return FlextResult[TGrpcServerEntity | dict[str, object]].fail(
                f"Server validation failed: {validation.error}"
            )

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
                return FlextResult[TGrpcServerEntity | dict[str, object]].fail(
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

        return FlextResult[TGrpcServerEntity | dict[str, object]].fail(
            f"Unknown server command: {command}"
        )

    def _start_server(
        self,
        server: TGrpcServerEntity,
    ) -> FlextResult[TGrpcServerEntity]:
        """Start server with REAL gRPC server implementation and performance optimization."""
        # Check server limit for resource management
        if len(self._active_servers) >= self._max_servers:
            return FlextResult[TGrpcServerEntity].fail(
                f"Maximum server limit reached ({self._max_servers}). "
                "Stop some servers or increase max_servers limit."
            )

        # Record start time for metrics
        self._startup_start_time = time.time()

        # Transition: stopped → starting
        start_result = server.start()
        if start_result.is_failure:
            return start_result

        starting_server = start_result.data
        return self._create_and_start_grpc_server(starting_server)

    def _create_and_start_grpc_server(
        self, starting_server: TGrpcServerEntity
    ) -> FlextResult[TGrpcServerEntity]:
        """Create and start the actual gRPC server."""
        server_key = f"{starting_server.host}:{starting_server.port}"

        try:
            # Create REAL gRPC server
            grpc_server = grpc.server(
                ThreadPoolExecutor(max_workers=starting_server.max_workers)
            )

            # Configure port binding
            port_result = self._configure_server_port(grpc_server, starting_server)
            if port_result.is_failure:
                grpc_server.stop(grace=1.0)
                return port_result

            configured_server = port_result.data
            server_key = f"{configured_server.host}:{configured_server.port}"

            # Start the REAL gRPC server
            try:
                grpc_server.start()
            except Exception as e:
                return FlextResult[TGrpcServerEntity].fail(
                    f"Failed to start gRPC server on {configured_server.host}:{configured_server.port}: {e}"
                )

            # Store and transition to running
            return self._finalize_server_startup(
                grpc_server, configured_server, server_key
            )

        except Exception as e:
            return FlextResult[TGrpcServerEntity].fail(
                f"Failed to start gRPC server: {e}"
            )

    def _configure_server_port(
        self, grpc_server: object, starting_server: TGrpcServerEntity
    ) -> FlextResult[TGrpcServerEntity]:
        """Configure server port binding."""
        if starting_server.port == 0:
            # Let gRPC choose available port
            actual_port = grpc_server.add_insecure_port(f"{starting_server.host}:0")
            # Update entity with actual port
            port_update_result = starting_server.copy_with(port=actual_port)
            if port_update_result.is_failure:
                return FlextResult[TGrpcServerEntity].fail(
                    f"Failed to update port: {port_update_result.error}"
                )
            return FlextResult[TGrpcServerEntity].ok(port_update_result.data)
        # Use specified port
        try:
            grpc_server.add_insecure_port(
                f"{starting_server.host}:{starting_server.port}"
            )
            return FlextResult[TGrpcServerEntity].ok(starting_server)
        except Exception as e:
            return FlextResult[TGrpcServerEntity].fail(
                f"Failed to bind to {starting_server.host}:{starting_server.port}: {e}"
            )

    def _finalize_server_startup(
        self, grpc_server: object, configured_server: TGrpcServerEntity, server_key: str
    ) -> FlextResult[TGrpcServerEntity]:
        """Finalize server startup and transition to running state."""
        # Store the real server for lifecycle management
        self._active_servers[server_key] = cast("GrpcServerProtocol", grpc_server)

        # Transition: starting → running
        running_result = configured_server.mark_running()
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
            "connection_count": 0,
            "request_count": 0,
        }

        return FlextResult[TGrpcServerEntity].ok(running_result.data)

    def _stop_server(self, server: TGrpcServerEntity) -> FlextResult[TGrpcServerEntity]:
        """Stop server with REAL gRPC server shutdown."""
        # Transition: running → stopping
        stop_result = server.stop()
        if stop_result.is_failure:
            return stop_result

        stopping_server = stop_result.data
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

            return FlextResult[TGrpcServerEntity].ok(stopped_result.data)

        except Exception as e:
            return FlextResult[TGrpcServerEntity].fail(
                f"Failed to stop gRPC server: {e}"
            )

    def _add_service(
        self,
        server: TGrpcServerEntity,
        service_def: TGrpcServiceDef,
    ) -> FlextResult[TGrpcServerEntity]:
        """Add REAL gRPC service to server."""
        if server.state != "running":
            return FlextResult[TGrpcServerEntity].fail(
                f"Cannot add service to server in state: {server.state}",
            )

        server_key = f"{server.host}:{server.port}"

        try:
            # Get the REAL gRPC server
            if server_key not in self._active_servers:
                return FlextResult[TGrpcServerEntity].fail(
                    f"No active gRPC server found for {server_key}"
                )

            grpc_server = self._active_servers[server_key]

            # Create REAL servicer and register it with the server
            real_servicer = create_real_servicer(f"{server.host}:{server.port}")
            add_FlextGrpcServiceServicer_to_server(real_servicer, grpc_server)

            # Add service to server entity (tracks the registration)
            add_result = server.add_service(service_def)
            if add_result.is_failure:
                return add_result

            return FlextResult[TGrpcServerEntity].ok(add_result.data)

        except Exception as e:
            return FlextResult[TGrpcServerEntity].fail(
                f"Failed to add service to gRPC server: {e}"
            )

    def _get_status(self, server: TGrpcServerEntity) -> FlextResult[dict[str, object]]:
        """Get server status information including REAL gRPC server status."""
        server_key = f"{server.host}:{server.port}"

        # Check if we have a real gRPC server running
        grpc_server_active = server_key in self._active_servers

        # Include performance metrics if available
        metrics = self._server_metrics.get(server_key, {})
        current_time = time.time()

        status: dict[str, object] = {
            "state": server.state,
            "host": server.host,
            "port": server.port,
            "max_workers": server.max_workers,
            "address": server.address,
            "is_running": server.is_running,
            "service_count": len(server.services),
            "grpc_server_active": grpc_server_active,
            "server_key": server_key,
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

    def __init__(
        self, connection_timeout: float = 5.0, max_retry_attempts: int = 3
    ) -> None:
        """Initialize service with real gRPC client registry and connection optimization.

        Args:
            connection_timeout: Connection timeout in seconds (default: 5.0)
            max_retry_attempts: Maximum retry attempts for failed operations (default: 3)

        """
        self._active_channels: dict[str, GrpcChannelProtocol] = {}
        self._connection_timeout = connection_timeout
        self._max_retry_attempts = max_retry_attempts
        self._client_metrics: dict[str, dict[str, object]] = {}  # Connection metrics

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
            return FlextResult[
                TGrpcClientEntity | TMethodCallResult | dict[str, object]
            ].fail(f"Client validation failed: {validation.error}")

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
                return FlextResult[
                    TGrpcClientEntity | TMethodCallResult | dict[str, object]
                ].fail(
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

        return FlextResult[
            TGrpcClientEntity | TMethodCallResult | dict[str, object]
        ].fail(f"Unknown client command: {command}")

    def _connect_client(
        self,
        client: TGrpcClientEntity,
    ) -> FlextResult[TGrpcClientEntity]:
        """Connect client with REAL gRPC channel establishment."""
        # Validate client preconditions
        validation_result = self._validate_client_for_connection(client)
        if validation_result.is_failure:
            return validation_result

        target = client.target
        try:
            # Create and test gRPC channel
            channel_result = self._create_and_test_grpc_channel(target)
            if channel_result.is_failure:
                return FlextResult[TGrpcClientEntity].fail(
                    channel_result.error or "Channel creation failed"
                )

            grpc_channel = channel_result.data
            # Transition client to connected state
            return self._transition_client_to_connected(client, grpc_channel, target)

        except Exception as e:
            return FlextResult[TGrpcClientEntity].fail(
                f"Failed to establish gRPC connection: {e}"
            )

    def _validate_client_for_connection(
        self, client: TGrpcClientEntity
    ) -> FlextResult[TGrpcClientEntity]:
        """Validate client preconditions for connection."""
        if client.channel is None:
            return FlextResult[TGrpcClientEntity].fail(
                "Client has no channel to connect"
            )

        if client.target is None:
            return FlextResult[TGrpcClientEntity].fail(
                "Client has no target to connect to"
            )

        return FlextResult[TGrpcClientEntity].ok(client)

    def _create_and_test_grpc_channel(self, target: str) -> FlextResult[object]:
        """Create gRPC channel and test connectivity."""
        # Retry connection with exponential backoff
        for attempt in range(self._max_retry_attempts):
            try:
                # Create REAL gRPC channel
                grpc_channel = grpc.insecure_channel(target)

                # Test connectivity with configurable timeout
                grpc.channel_ready_future(grpc_channel).result(
                    timeout=self._connection_timeout
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
                grpc_channel.close()

                # If this is the last attempt, fail
                if attempt == self._max_retry_attempts - 1:
                    return FlextResult[object].fail(
                        f"Failed to connect to {target}: connection timeout after {self._max_retry_attempts} attempts"
                    )

                # Wait before retrying with exponential backoff
                wait_time = (2**attempt) * 0.5  # 0.5s, 1s, 2s, etc.
                time.sleep(wait_time)

        # This should never be reached due to the logic above, but for type safety
        return FlextResult[object].fail(f"Connection failed unexpectedly to {target}")

    def _transition_client_to_connected(
        self, client: TGrpcClientEntity, grpc_channel: object, target: str
    ) -> FlextResult[TGrpcClientEntity]:
        """Transition client channel states to connected."""
        # Store the real channel for lifecycle management
        self._active_channels[target] = cast("GrpcChannelProtocol", grpc_channel)

        # Transition: idle → connecting
        connect_result = client.channel.connect()
        if connect_result.is_failure:
            cast("GrpcChannelProtocol", grpc_channel).close()
            self._active_channels.pop(target, None)
            return FlextResult[TGrpcClientEntity].fail(
                f"Channel connection failed: {connect_result.error}"
            )

        connecting_channel = connect_result.data
        # Transition: connecting → ready
        ready_result = connecting_channel.mark_ready()
        if ready_result.is_failure:
            cast("GrpcChannelProtocol", grpc_channel).close()
            self._active_channels.pop(target, None)
            return FlextResult[TGrpcClientEntity].fail(
                f"Channel ready transition failed: {ready_result.error}"
            )

        # Update client with new channel
        return client.copy_with(channel=ready_result.data)

    def _disconnect_client(
        self,
        client: TGrpcClientEntity,
    ) -> FlextResult[TGrpcClientEntity]:
        """Disconnect client with REAL gRPC channel closure."""
        # Check if client has a channel
        if client.channel is None:
            return FlextResult[TGrpcClientEntity].fail(
                "Client has no channel to disconnect"
            )

        target = client.target
        if target is None:
            return FlextResult[TGrpcClientEntity].fail(
                "Client has no target to disconnect from"
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
                return FlextResult[TGrpcClientEntity].fail(
                    f"Channel disconnection failed: {disconnect_result.error}",
                )

            # Update client with disconnected channel
            return client.copy_with(channel=disconnect_result.data)

        except Exception as e:
            return FlextResult[TGrpcClientEntity].fail(
                f"Failed to disconnect gRPC client: {e}"
            )

    def _make_call(
        self,
        client: TGrpcClientEntity,
        method: str,
        request: object,
    ) -> FlextResult[TMethodCallResult]:
        """Execute REAL gRPC method call."""
        if not client.is_connected:
            return FlextResult[TMethodCallResult].fail(
                f"Cannot make call with disconnected client: {client.target or 'no target'}",
            )

        target = client.target
        if target is None:
            return FlextResult[TMethodCallResult].fail(
                "Client has no target for method call"
            )

        try:
            # Get REAL gRPC channel
            if target not in self._active_channels:
                return FlextResult[TMethodCallResult].fail(
                    f"No active gRPC channel for {target}"
                )

            grpc_channel = self._active_channels[target]

            # Validate channel is still ready
            try:
                grpc.channel_ready_future(grpc_channel).result(timeout=1.0)
            except grpc.FutureTimeoutError:
                return FlextResult[TMethodCallResult].fail(
                    f"gRPC channel not ready for {target}"
                )

            # Create REAL gRPC stub and make REAL call
            stub = FlextGrpcServiceStub(grpc_channel)

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
                grpc_response = stub.Echo(echo_request, timeout=10.0)

                # Convert to result format
                response = {
                    "method": "Echo",
                    "status": "success",
                    "message": grpc_response.message,
                    "server_id": grpc_response.server_id,
                    "timestamp": grpc_response.timestamp,
                    "target": target,
                    "channel_ready": True,
                }

            elif method == "HealthCheck":
                health_request = HealthRequest(service="FlextGrpcService")
                grpc_response = stub.HealthCheck(health_request, timeout=5.0)

                response = {
                    "method": "HealthCheck",
                    "status": "success",
                    "serving_status": grpc_response.status,
                    "message": grpc_response.message,
                    "target": target,
                    "channel_ready": True,
                }

            else:
                # For other methods, create a generic Echo call
                echo_request = EchoRequest(message=f"Method: {method}")
                grpc_response = stub.Echo(echo_request, timeout=10.0)

                response = {
                    "method": method,
                    "status": "success",
                    "message": grpc_response.message,
                    "server_id": grpc_response.server_id,
                    "timestamp": grpc_response.timestamp,
                    "target": target,
                    "channel_ready": True,
                }

            return FlextResult[TMethodCallResult].ok(response)

        except grpc.RpcError as rpc_error:
            return FlextResult[TMethodCallResult].fail(
                f"gRPC call failed: {rpc_error.code()} - {rpc_error.details()}"
            )
        except Exception as e:
            return FlextResult[TMethodCallResult].fail(f"Failed to make gRPC call: {e}")

    def _get_status(self, client: TGrpcClientEntity) -> FlextResult[dict[str, object]]:
        """Get client status information including REAL gRPC channel status."""
        target = client.target

        # Check if we have a real gRPC channel active
        grpc_channel_active = target is not None and target in self._active_channels
        grpc_channel_ready = False

        if grpc_channel_active and target is not None:
            grpc_channel = self._active_channels[target]
            try:
                grpc.channel_ready_future(grpc_channel).result(timeout=0.1)
                grpc_channel_ready = True
            except grpc.FutureTimeoutError:
                grpc_channel_ready = False

        status: dict[str, object] = {
            "channel_state": client.channel.state if client.channel else "no_channel",
            "target": client.target,
            "is_connected": client.is_connected,
            "grpc_channel_active": grpc_channel_active,
            "grpc_channel_ready": grpc_channel_ready,
        }
        return FlextResult[dict[str, object]].ok(status)


class FlextGrpcStreamService:
    """gRPC stream domain service for streaming operations.

    Implements business logic for gRPC streaming operations including stream
    creation, data flow management, and stream lifecycle operations.

    Commands:
      - create: Create new gRPC stream
      - send: Send data through stream
      - close: Close stream gracefully

    """

    def __init__(
        self,
        max_concurrent_streams: int = MAX_CONCURRENT_STREAMS_PER_CLIENT,
        stream_buffer_size: int = BIDIRECTIONAL_STREAMING_QUEUE_SIZE,
        metrics_interval: float = STREAM_METRICS_COLLECTION_INTERVAL,
    ) -> None:
        """Initialize enterprise-grade stream service with advanced configuration.

        Args:
            max_concurrent_streams: Maximum concurrent streams per client
            stream_buffer_size: Buffer size for streaming operations
            metrics_interval: Interval for metrics collection (seconds)

        """
        self._active_streams: dict[str, StreamInfo] = {}  # Enterprise stream tracking
        self._active_channels: dict[str, GrpcChannelProtocol] = {}  # Channel pool

        # Enterprise-grade configuration
        self._max_concurrent_streams = max_concurrent_streams
        self._stream_buffer_size = stream_buffer_size
        self._metrics_interval = metrics_interval

        # Performance tracking
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

        # Thread management
        self._metrics_thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()
        self._metrics_lock = threading.RLock()

        # Start background metrics collection
        self._start_metrics_collection()

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
            return FlextResult[TGrpcStreamEntity | TMethodCallResult].fail(
                f"Stream validation failed: {validation.error}"
            )

        # Execute command
        if command == "create":
            target = args[0] if args else kwargs.get("target")
            if target is not None and not isinstance(target, str):
                return FlextResult[TGrpcStreamEntity | TMethodCallResult].fail(
                    f"Target must be string, got: {type(target)}"
                )
            result = self._create_stream(stream, target)
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
        return FlextResult[TGrpcStreamEntity | TMethodCallResult].fail(
            f"Unknown stream command: {command}"
        )

    def _create_stream(
        self,
        stream: TGrpcStreamEntity,
        target: str | None = None,
    ) -> FlextResult[TGrpcStreamEntity]:
        """Create REAL gRPC stream."""
        stream_key = f"{stream.id.root}_{stream.stream_type}"

        try:
            # For real streaming, we need a target server
            if target is None:
                target = "localhost:50051"  # Default target

            # Create real gRPC channel if not exists
            if target not in self._active_channels:
                grpc_channel = grpc.insecure_channel(target)
                self._active_channels[target] = cast(
                    "GrpcChannelProtocol", grpc_channel
                )

            grpc_channel = self._active_channels[target]

            # Create real gRPC stub for streaming
            stub = FlextGrpcServiceStub(grpc_channel)

            # Register the REAL stream with actual gRPC objects and buffers
            stream_info: StreamInfo = {
                "stream_id": stream.id.root,
                "type": stream.stream_type,
                "created_at": stream.created_at.root.timestamp(),
                "active": True,
                "target": target,
                "stub": stub,  # Real gRPC stub
                "channel": grpc_channel,  # Real gRPC channel
                "request_buffer": [],  # Buffer for client streaming
                "request_queue": Queue(
                    maxsize=BIDIRECTIONAL_STREAMING_QUEUE_SIZE
                ),  # Thread-safe queue
                "response_buffer": deque(
                    maxlen=SERVER_STREAMING_BATCH_SIZE
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

            return FlextResult[TGrpcStreamEntity].ok(stream)

        except Exception as e:
            return FlextResult[TGrpcStreamEntity].fail(
                f"Failed to create gRPC stream: {e}"
            )

    def _handle_client_streaming(
        self,
        stream: TGrpcStreamEntity,
        stream_info: StreamInfo,
        stream_request: object,
        data: object,
        stub: object,
    ) -> FlextResult[TMethodCallResult]:
        """Handle client streaming with memory optimization."""
        # Check memory pressure before adding to buffer
        current_buffer_size = get_buffer_size_bytes(stream_info["request_buffer"])
        system_memory = get_system_memory_usage()

        # Update memory tracking
        stream_info["buffer_size_bytes"] = current_buffer_size
        stream_info["memory_pressure_score"] = system_memory

        # Check if we need to trigger early flush due to memory pressure
        should_flush_early = (
            current_buffer_size > MAX_BUFFER_SIZE_BYTES * ADAPTIVE_BUFFER_SCALING_FACTOR
            or system_memory > MEMORY_PRESSURE_THRESHOLD
        )

        # Add request to buffer for client streaming accumulation
        if not should_flush_early or len(stream_info["request_buffer"]) == 0:
            stream_info["request_buffer"].append(stream_request)

        stream_info["sequence_counter"] += 1
        stream_info["last_activity"] = time.time()

        # Send all buffered requests when buffer reaches threshold, explicit flush, or memory pressure
        buffered_requests = stream_info["request_buffer"]
        should_flush = (
            len(buffered_requests) >= CLIENT_STREAMING_BUFFER_THRESHOLD
            or str(data) == "__FLUSH_BUFFER__"
            or should_flush_early
        )

        if should_flush:
            # Make real client streaming call with all buffered requests
            response = stub.ClientStream(iter(buffered_requests), timeout=10.0)

            # Clear buffer after successful call and trigger memory cleanup if needed
            stream_info["request_buffer"].clear()
            stream_info["last_memory_cleanup"] = time.time()

            # Update memory stats
            stream_info["buffer_size_bytes"] = 0

            # Trigger garbage collection if memory pressure is high
            if system_memory > MEMORY_PRESSURE_THRESHOLD:
                trigger_memory_cleanup()

            result = {
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id.root,
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
            result = {
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id.root,
                "buffer_status": "buffered",
                "buffer_size": len(buffered_requests),
                "sequence": stream_info["sequence_counter"],
            }

        return FlextResult[TMethodCallResult].ok(result)

    def _handle_bidirectional_streaming(
        self,
        stream: TGrpcStreamEntity,
        stream_info: StreamInfo,
        stream_request: object,
        data: object,
        stub: object,
    ) -> FlextResult[TMethodCallResult]:
        """Handle bidirectional streaming operations."""
        # Add to buffer for bidirectional streaming
        stream_info["request_buffer"].append(stream_request)
        stream_info["sequence_counter"] += 1
        stream_info["last_activity"] = time.time()

        # For bidirectional, we can send immediately but batch responses
        response_iterator = stub.BidirectionalStream(
            iter([stream_request]), timeout=10.0
        )
        responses = []
        try:
            for response in response_iterator:
                responses.append({
                    "data": response.data,
                    "sequence": response.sequence,
                    "server_id": response.server_id,
                    "timestamp": response.timestamp,
                })
                # Break after first response for immediate processing
                break
        except Exception:
            # Handle streaming errors gracefully
            responses = []

        result = {
            "sent": str(data),
            "stream_type": stream.stream_type,
            "stream_id": stream.id.root,
            "responses": responses,
            "response_count": len(responses),
            "sequence": stream_info["sequence_counter"],
            "buffer_size": len(stream_info["request_buffer"]),
        }

        return FlextResult[TMethodCallResult].ok(result)

    def _validate_stream_for_sending(
        self, stream_key: str
    ) -> FlextResult[TMethodCallResult]:
        """Validate stream exists and is active for sending data."""
        if stream_key not in self._active_streams:
            return FlextResult[TMethodCallResult].fail(
                f"No active gRPC stream found: {stream_key}"
            )

        stream_info = self._active_streams[stream_key]
        if not stream_info.get("active", False):
            return FlextResult[TMethodCallResult].fail(
                f"gRPC stream is not active: {stream_key}"
            )

        return FlextResult[TMethodCallResult].ok({})

    def _handle_server_streaming(
        self,
        stream: TGrpcStreamEntity,
        _stream_info: StreamInfo,
        stream_request: object,
        data: object,
        stub: object,
    ) -> FlextResult[TMethodCallResult]:
        """Handle server streaming operations."""
        # Server streaming: get iterator of responses
        response_iterator = stub.ServerStream(stream_request, timeout=10.0)
        responses = [
            {
                "data": response.data,
                "sequence": response.sequence,
                "server_id": response.server_id,
                "timestamp": response.timestamp,
            }
            for response in response_iterator
        ]

        result = {
            "sent": str(data),
            "stream_type": stream.stream_type,
            "stream_id": stream.id.root,
            "responses": responses,
            "response_count": len(responses),
        }
        return FlextResult[TMethodCallResult].ok(result)

    def _handle_unary_streaming(
        self,
        stream: TGrpcStreamEntity,
        _stream_info: StreamInfo,
        _stream_request: object,
        data: object,
        stub: object,
    ) -> FlextResult[TMethodCallResult]:
        """Handle unary operations."""
        # For unary, convert to Echo call
        echo_request = EchoRequest(message=str(data))
        response = stub.Echo(echo_request, timeout=10.0)

        result = {
            "sent": str(data),
            "stream_type": stream.stream_type,
            "stream_id": stream.id.root,
            "response": {
                "message": response.message,
                "server_id": response.server_id,
                "timestamp": response.timestamp,
            },
        }
        return FlextResult[TMethodCallResult].ok(result)

    def _send_data(
        self,
        stream: TGrpcStreamEntity,
        data: object,
    ) -> FlextResult[TMethodCallResult]:
        """Send data through REAL gRPC stream."""
        stream_key = f"{stream.id.root}_{stream.stream_type}"

        try:
            # Validate stream existence and activity
            validation_result = self._validate_stream_for_sending(stream_key)
            if validation_result.is_failure:
                return validation_result

            stream_info = self._active_streams[stream_key]
            stub = stream_info["stub"]

            # Create real StreamRequest
            stream_request = StreamRequest(
                data=str(data), sequence=1, client_id=stream.id.root
            )

            # Use command mapping pattern to reduce returns
            stream_handlers = {
                "server_streaming": self._handle_server_streaming,
                "client_streaming": self._handle_client_streaming,
                "bidirectional": self._handle_bidirectional_streaming,
                "unary": self._handle_unary_streaming,
            }

            handler = stream_handlers.get(stream.stream_type)
            if handler:
                return handler(stream, stream_info, stream_request, data, stub)

            return FlextResult[TMethodCallResult].fail(
                f"Unknown stream type: {stream.stream_type}"
            )

        except grpc.RpcError as rpc_error:
            return FlextResult[TMethodCallResult].fail(
                f"gRPC streaming failed: {rpc_error.code()} - {rpc_error.details()}"
            )
        except Exception as e:
            return FlextResult[TMethodCallResult].fail(
                f"Failed to send data through gRPC stream: {e}"
            )

    def _close_stream(
        self,
        stream: TGrpcStreamEntity,
    ) -> FlextResult[TGrpcStreamEntity]:
        """Close REAL gRPC stream gracefully."""
        stream_key = f"{stream.id.root}_{stream.stream_type}"

        try:
            # Close real gRPC stream if it exists
            if stream_key in self._active_streams:
                stream_info = self._active_streams[stream_key]

                # Close real gRPC channel if this was the last stream using it
                target = stream_info.get("target")
                if (
                    target
                    and isinstance(target, str)
                    and target in self._active_channels
                ):
                    # Check if any other streams are using this channel
                    other_streams_using_channel = any(
                        info.get("target") == target
                        for key, info in self._active_streams.items()
                        if key != stream_key and info.get("active", False)
                    )

                    if not other_streams_using_channel:
                        # Close the real gRPC channel
                        channel = self._active_channels[target]
                        channel.close()
                        del self._active_channels[target]

                # Mark as inactive and remove
                stream_info["active"] = False
                del self._active_streams[stream_key]

            return FlextResult[TGrpcStreamEntity].ok(stream)

        except Exception as e:
            return FlextResult[TGrpcStreamEntity].fail(
                f"Failed to close gRPC stream: {e}"
            )

    def _cleanup_expired_buffers(
        self, max_age_seconds: float = STREAM_CLEANUP_MAX_AGE_SECONDS
    ) -> None:
        """Clean up expired stream buffers to prevent memory leaks."""
        current_time = time.time()
        expired_streams = []

        for stream_key, stream_info in self._active_streams.items():
            last_activity = stream_info.get("last_activity", 0)
            if current_time - last_activity > max_age_seconds:
                expired_streams.append(stream_key)

        # Clean up expired streams
        for stream_key in expired_streams:
            stream_info = self._active_streams[stream_key]
            target = stream_info.get("target")

            # Clear buffer to free memory
            if "request_buffer" in stream_info:
                stream_info["request_buffer"].clear()

            # Close channel if no other streams using it
            if target and target in self._active_channels:
                other_streams = any(
                    info.get("target") == target and key != stream_key
                    for key, info in self._active_streams.items()
                )
                if not other_streams:
                    channel = self._active_channels[target]
                    channel.close()
                    del self._active_channels[target]

            # Remove expired stream
            del self._active_streams[stream_key]

    def _proactive_memory_cleanup(self) -> None:
        """Proactively clean up memory when under pressure."""
        try:
            # Find streams with large buffers and clean them up
            streams_to_clean = []
            current_time = time.time()

            for stream_key, stream_info in self._active_streams.items():
                buffer_size_bytes = stream_info.get("buffer_size_bytes", 0)
                last_cleanup = stream_info.get("last_memory_cleanup", 0)
                time_since_cleanup = current_time - last_cleanup

                # Clean up buffers that are large or haven't been cleaned recently
                if (
                    buffer_size_bytes > MAX_BUFFER_SIZE_BYTES * 0.5
                    and time_since_cleanup > MEMORY_CLEANUP_INTERVAL_SHORT
                ) or (
                    buffer_size_bytes > MAX_BUFFER_SIZE_BYTES * 0.2
                    and time_since_cleanup > MEMORY_CLEANUP_INTERVAL_LONG
                ):
                    streams_to_clean.append(stream_key)

            # Clean up buffers in batches to avoid blocking
            for stream_key in streams_to_clean[:BUFFER_CLEANUP_BATCH_SIZE]:
                if stream_key in self._active_streams:
                    stream_info = self._active_streams[stream_key]

                    # Partial buffer cleanup - keep only recent items
                    buffer = stream_info.get("request_buffer", [])
                    if len(buffer) > CLIENT_STREAMING_BUFFER_THRESHOLD * 2:
                        # Keep only the most recent half of buffer items
                        keep_count = len(buffer) // 2
                        stream_info["request_buffer"] = buffer[-keep_count:]
                        stream_info["buffer_size_bytes"] = get_buffer_size_bytes(
                            stream_info["request_buffer"]
                        )
                        stream_info["last_memory_cleanup"] = current_time

            # Trigger system garbage collection
            trigger_memory_cleanup()

        except Exception as e:
            logger = get_logger(__name__)
            logger.debug(f"Proactive memory cleanup error: {e}")

    def _start_metrics_collection(self) -> None:
        """Start background metrics collection thread."""
        if self._metrics_thread is None or not self._metrics_thread.is_alive():
            self._metrics_thread = threading.Thread(
                target=self._collect_metrics_periodically,
                daemon=True,
                name="FlextGrpcStreamMetrics",
            )
            self._metrics_thread.start()

    def _collect_metrics_periodically(self) -> None:
        """Periodically collect stream performance metrics."""
        while not self._shutdown_event.is_set():
            try:
                with self._metrics_lock:
                    current_time = time.time()

                    # Update global metrics including memory usage
                    self._global_metrics["total_streams_active"] = len(
                        self._active_streams
                    )
                    self._global_metrics["memory_pressure_score"] = (
                        get_system_memory_usage()
                    )

                    # Calculate total memory usage across all streams
                    total_memory_bytes = 0
                    memory_pressure_count = 0

                    # Collect per-stream metrics
                    for stream_key, stream_info in self._active_streams.items():
                        if stream_key not in self._stream_metrics:
                            self._stream_metrics[stream_key] = {
                                "creation_time": stream_info.get(
                                    "created_at", current_time
                                ),
                                "total_requests": 0.0,
                                "total_responses": 0.0,
                                "bytes_processed": 0.0,
                                "last_metric_update": current_time,
                            }

                        # Update stream-specific metrics (all numeric)
                        metrics = self._stream_metrics[stream_key]
                        metrics["last_metric_update"] = current_time
                        metrics["uptime"] = current_time - metrics["creation_time"]

                        # Update buffer sizes and memory usage
                        buffer_size = len(stream_info.get("request_buffer", []))
                        buffer_size_bytes = stream_info.get("buffer_size_bytes", 0)
                        memory_pressure = stream_info.get("memory_pressure_score", 0.0)

                        metrics["buffer_size"] = float(buffer_size)
                        metrics["buffer_size_bytes"] = float(buffer_size_bytes)
                        metrics["memory_pressure"] = memory_pressure

                        # Accumulate global memory stats
                        total_memory_bytes += buffer_size_bytes
                        if memory_pressure > MEMORY_PRESSURE_THRESHOLD:
                            memory_pressure_count += 1

                        # Update activity status
                        last_activity = stream_info.get("last_activity", 0)
                        idle_time = current_time - last_activity
                        metrics["idle_time"] = idle_time

                        # Health status as numeric score (0=unhealthy, 1=degraded, 2=healthy)
                        if idle_time > STREAM_CLEANUP_MAX_AGE_SECONDS:
                            metrics["health_score"] = 0.0  # unhealthy
                        elif idle_time > STREAM_HEALTH_DEGRADED_THRESHOLD:
                            metrics["health_score"] = 1.0  # degraded
                        else:
                            metrics["health_score"] = 2.0  # healthy

                    # Update global memory metrics
                    self._global_metrics["total_memory_used_bytes"] = total_memory_bytes

                    # Trigger proactive memory cleanup if too many streams under pressure
                    high_pressure_ratio = memory_pressure_count / max(
                        1, len(self._active_streams)
                    )
                    if (
                        high_pressure_ratio > HIGH_PRESSURE_RATIO_THRESHOLD
                    ):  # More than 50% of streams under pressure
                        self._proactive_memory_cleanup()
                        self._global_metrics["buffers_cleaned_up"] += 1

                # Clean up expired buffers
                self._cleanup_expired_buffers()

            except Exception as e:
                # Log error but continue metrics collection
                logger = get_logger(__name__)
                logger.warning(f"Metrics collection error: {e}")

            # Wait for next collection interval
            self._shutdown_event.wait(self._metrics_interval)

    def get_stream_metrics(self) -> dict[str, object]:
        """Get comprehensive stream performance metrics."""
        with self._metrics_lock:
            return {
                "global_metrics": self._global_metrics.copy(),
                "stream_metrics": {
                    stream_key: metrics.copy()
                    for stream_key, metrics in self._stream_metrics.items()
                },
                "active_channels": list(self._active_channels.keys()),
                "total_channels": len(self._active_channels),
            }

    def shutdown(self) -> None:
        """Gracefully shutdown the streaming service."""
        self._shutdown_event.set()

        # Close all active channels
        logger = get_logger(__name__)
        for channel in self._active_channels.values():
            try:
                channel.close()
            except Exception as e:
                logger.debug(f"Error closing channel during shutdown: {e}")

        self._active_channels.clear()
        self._active_streams.clear()

        # Wait for metrics thread to finish
        if self._metrics_thread and self._metrics_thread.is_alive():
            self._metrics_thread.join(timeout=2.0)


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
        self._container = container or FlextContainer.get_global()
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
