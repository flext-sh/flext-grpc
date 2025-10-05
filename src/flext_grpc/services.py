"""FLEXT gRPC Services - Unified Service Implementation.

Single unified gRPC service class following FLEXT namespace pattern.
Contains all server, client, and streaming functionality with nested helpers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import contextlib
import logging
import threading
import time
from collections import deque
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import cast, override

import grpc
from flext_core import (
    FlextBus,
    FlextConstants,
    FlextContainer,
    FlextContext,
    FlextDispatcher,
    FlextLogger,
    FlextProcessors,
    FlextRegistry,
    FlextResult,
    FlextService,
    FlextTypes,
)

# Factory methods now implemented directly in service class
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
from flext_grpc.protocols import FlextGrpcProtocols
from flext_grpc.real_servicer import create_real_servicer
from flext_grpc.utilities import FlextGrpcUtilities


class FlextGrpcService(
    FlextService[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | FlextTypes.Dict]
):
    """Unified gRPC service class following FLEXT namespace pattern.

    Single class containing all server, client, and streaming functionality.
    Uses nested helper classes for organization while maintaining clean API.
    """

    # Nested constants class for streaming and memory management
    class StreamingConstants:
        """Constants for gRPC streaming operations and memory management."""

        # Streaming operation constants
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

    def __init__(self, max_servers: int = 10, thread_pool_size: int = 50) -> None:
        """Initialize unified gRPC service with complete FLEXT ecosystem integration."""
        super().__init__()

        # Complete FLEXT ecosystem integration
        self._container = FlextContainer.get_global()
        self._context = FlextContext()
        self._bus = FlextBus()
        self._dispatcher = FlextDispatcher()
        self._processors = FlextProcessors()
        self._registry = FlextRegistry(dispatcher=self._dispatcher)
        self._logger = FlextLogger(__name__)

        # Server management
        self._active_servers: dict[str, FlextGrpcProtocols.Grpc.ServerProtocol] = {}
        self._max_servers = max_servers
        self._thread_pool_size = thread_pool_size
        self._server_metrics: dict[str, FlextTypes.FloatDict] = {}
        self._thread_pool = ThreadPoolExecutor(
            max_workers=thread_pool_size,
            thread_name_prefix="flext-grpc-server",
        )

        # Client management
        self._active_channels: dict[str, FlextGrpcProtocols.Grpc.ClientProtocol] = {}
        self._connection_timeout: float = 5.0
        self._max_retry_attempts: int = 3
        self._client_metrics: FlextTypes.NestedDict = {}

        # Stream management
        self._active_streams: FlextTypes.NestedDict = {}
        self._max_concurrent_streams: int = (
            self.StreamingConstants.MAX_CONCURRENT_STREAMS_PER_CLIENT
        )
        self._stream_buffer_size: int = (
            self.StreamingConstants.BIDIRECTIONAL_STREAMING_QUEUE_SIZE
        )
        self._metrics_interval: float = (
            self.StreamingConstants.STREAM_METRICS_COLLECTION_INTERVAL
        )
        self._stream_metrics: dict[str, FlextTypes.FloatDict] = {}

        # Global metrics
        self._global_metrics = {
            "total_streams_created": 0,
            "total_streams_active": 0,
            "total_bytes_streamed": 0,
            "average_stream_duration": 0.0,
            "total_memory_used_bytes": 0,
            "memory_pressure_score": 0.0,
            "buffers_cleaned_up": 0,
        }

        # Threading coordination
        self._metrics_thread: threading.Thread | None = None
        self._shutdown_event = threading.Event()
        self._metrics_lock = threading.RLock()

    def _start_metrics_collection(self) -> None:
        """Start background metrics collection thread."""
        if self._metrics_thread is None or not self._metrics_thread.is_alive():
            self._metrics_thread = threading.Thread(
                target=self._collect_metrics_loop,
                daemon=True,
                name="flext-grpc-metrics",
            )
            self._metrics_thread.start()

    # === SERVER OPERATIONS ===

    def start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Start gRPC server with validation and error handling."""
        return self._start_server(server)

    def stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop gRPC server with graceful shutdown."""
        return self._stop_server(server)

    def get_server_status(
        self, server: FlextGrpcServer
    ) -> FlextResult[FlextTypes.Dict]:
        """Get server status and metrics."""
        return self._get_server_status(server)

    # === FACTORY METHODS ===

    def _create_client_entity(
        self, target: str, options: FlextTypes.Dict | None = None
    ) -> FlextResult[FlextGrpcClient]:
        """Create a gRPC client entity using utilities."""
        return FlextGrpcUtilities.create_client_entity(target, options)

    def _create_stream_entity(
        self, method_name: str, stream_type: str
    ) -> FlextResult[FlextGrpcStream]:
        """Create a gRPC stream entity using utilities."""
        return FlextGrpcUtilities.create_stream_entity(method_name, stream_type)

    # === CLIENT OPERATIONS ===

    def connect_client(self, target: str) -> FlextResult[FlextGrpcClient]:
        """Connect to gRPC server at target."""
        # Create client entity directly
        client_result = self._create_client_entity(target=target)
        if client_result.is_failure:
            return FlextResult.fail(
                f"Client entity creation failed: {client_result.error}"
            )
        client = client_result.unwrap()
        return self._connect_client(client)

    def disconnect_client(
        self, client: FlextGrpcClient
    ) -> FlextResult[FlextGrpcClient]:
        """Disconnect gRPC client."""
        return self._disconnect_client(client)

    def make_call(
        self, client: FlextGrpcClient, method: str, request: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Make gRPC call through client."""
        return self._make_call(client, method, request)

    def get_client_status(
        self, client: FlextGrpcClient
    ) -> FlextResult[FlextTypes.Dict]:
        """Get client status."""
        return self._get_client_status(client)

    # === STREAM OPERATIONS ===

    def create_stream(
        self, stream_type: str = "unary", **kwargs: object
    ) -> FlextResult[FlextGrpcStream]:
        """Create gRPC stream."""
        stream_result = self._create_stream_entity(
            method_name=kwargs.get("method_name", "DefaultMethod"),
            stream_type=stream_type,
        )
        if stream_result.is_failure:
            return FlextResult.fail(
                f"Stream entity creation failed: {stream_result.error}"
            )
        stream = stream_result.unwrap()
        return self._create_stream(stream, kwargs.get("target"))

    def send_data(
        self, stream: FlextGrpcStream, data: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Send data through stream."""
        return self._send_data(stream, data)

    def close_stream(self, stream: FlextGrpcStream) -> FlextResult[FlextGrpcStream]:
        """Close gRPC stream."""
        return self._close_stream(stream)

    def execute_grpc(
        self,
        command: str | None = None,
        entity: FlextGrpcServer
        | FlextGrpcClient
        | FlextGrpcStream
        | FlextTypes.Dict
        | None = None,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Dict]:
        """Execute gRPC command with routing to appropriate handler."""
        if command is None:
            return FlextResult.ok({
                "status": "ready",
                "service": "flext-grpc-service",
            })

        if entity is None:
            return FlextResult.fail("Entity instance required")

        # Route to appropriate handler based on entity type
        if isinstance(entity, FlextGrpcServer):
            result = self._ServerOps.execute_server_command(
                self, command, entity, *args, **kwargs
            )
            return (
                FlextResult.ok(cast("FlextTypes.Dict", result.unwrap()))
                if result.is_success
                else cast("FlextResult[FlextTypes.Dict]", result)
            )
        if isinstance(entity, FlextGrpcClient):
            result = self._ClientOps.execute_client_command(
                self, command, entity, *args, **kwargs
            )
            return (
                FlextResult.ok(cast("FlextTypes.Dict", result.unwrap()))
                if result.is_success
                else cast("FlextResult[FlextTypes.Dict]", result)
            )
        if isinstance(entity, FlextGrpcStream):
            result = self._StreamOps.execute_stream_command(
                self, command, entity, *args, **kwargs
            )
            return (
                FlextResult.ok(cast("FlextTypes.Dict", result.unwrap()))
                if result.is_success
                else cast("FlextResult[FlextTypes.Dict]", result)
            )
        return FlextResult.fail(f"Unsupported entity type: {type(entity)}")

    @override
    def execute(
        self,
    ) -> FlextResult[
        FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | FlextTypes.Dict
    ]:
        """Execute main service operation."""
        return cast(
            "FlextResult[FlextGrpcServer | FlextGrpcClient | FlextGrpcStream | FlextTypes.Dict]",
            self.execute_grpc(),
        )

    # === NESTED HELPER CLASSES ===

    class _ServerOps:
        """Nested helper class for server operations."""

        @staticmethod
        def execute_server_command(
            service: FlextGrpcService,
            command: str,
            server: FlextGrpcServer,
            *args: object,
            **kwargs: object,
        ) -> FlextResult[FlextGrpcServer | FlextTypes.Dict]:
            """Execute server command with validation."""
            validation = server.validate_business_rules()
            if validation.is_failure:
                return FlextResult.fail(f"Server validation failed: {validation.error}")

            command_handlers: dict[
                str, Callable[[], FlextResult[FlextGrpcServer | FlextTypes.Dict]]
            ] = {
                "start": lambda: cast(
                    "FlextResult[FlextGrpcServer | FlextTypes.Dict]",
                    service._start_server(server),
                ),
                "stop": lambda: cast(
                    "FlextResult[FlextGrpcServer | FlextTypes.Dict]",
                    service._stop_server(server),
                ),
                "status": lambda: cast(
                    "FlextResult[FlextGrpcServer | FlextTypes.Dict]",
                    service._get_server_status(server),
                ),
                "add_service": lambda: cast(
                    "FlextResult[FlextGrpcServer | FlextTypes.Dict]",
                    service._add_service_to_server(
                        server,
                        cast(
                            "FlextGrpcServiceEntity",
                            args[0] if args else kwargs.get("service"),
                        ),
                    ),
                ),
            }

            handler = command_handlers.get(command)
            return (
                handler()
                if handler
                else FlextResult.fail(f"Unknown server command: {command}")
            )

    class _ClientOps:
        """Nested helper class for client operations."""

        @staticmethod
        def execute_client_command(
            service: FlextGrpcService,
            command: str,
            client: FlextGrpcClient,
            *args: object,
            **kwargs: object,
        ) -> FlextResult[FlextGrpcClient | FlextTypes.Dict]:
            """Execute client command with validation."""
            validation = client.validate_business_rules()
            if validation.is_failure:
                return FlextResult.fail(f"Client validation failed: {validation.error}")

            command_handlers: dict[
                str, Callable[[], FlextResult[FlextGrpcClient | FlextTypes.Dict]]
            ] = {
                "connect": lambda: cast(
                    "FlextResult[FlextGrpcClient | FlextTypes.Dict]",
                    service._connect_client(client),
                ),
                "disconnect": lambda: cast(
                    "FlextResult[FlextGrpcClient | FlextTypes.Dict]",
                    service._disconnect_client(client),
                ),
                "status": lambda: cast(
                    "FlextResult[FlextGrpcClient | FlextTypes.Dict]",
                    service._get_client_status(client),
                ),
                "call": lambda: cast(
                    "FlextResult[FlextGrpcClient | FlextTypes.Dict]",
                    service._make_call(
                        client,
                        str(args[0] if args else kwargs.get("method", "")),
                        args[1] if len(args) > 1 else kwargs.get("request"),
                    ),
                ),
            }

            handler = command_handlers.get(command)
            return (
                handler()
                if handler
                else FlextResult.fail(f"Unknown client command: {command}")
            )

    class _StreamOps:
        """Nested helper class for stream operations."""

        @staticmethod
        def execute_stream_command(
            service: FlextGrpcService,
            command: str,
            stream: FlextGrpcStream,
            *args: object,
            **kwargs: object,
        ) -> FlextResult[FlextGrpcStream | FlextTypes.Dict]:
            """Execute stream command with validation."""
            validation = stream.validate_business_rules()
            if validation.is_failure:
                return FlextResult.fail(f"Stream validation failed: {validation.error}")

            command_handlers: dict[
                str, Callable[[], FlextResult[FlextGrpcStream | FlextTypes.Dict]]
            ] = {
                "create": lambda: cast(
                    "FlextResult[FlextGrpcStream | FlextTypes.Dict]",
                    service._create_stream(stream, str(kwargs.get("target") or None)),
                ),
                "send": lambda: cast(
                    "FlextResult[FlextGrpcStream | FlextTypes.Dict]",
                    service._send_data(
                        stream, args[0] if args else kwargs.get("data", {})
                    ),
                ),
                "close": lambda: cast(
                    "FlextResult[FlextGrpcStream | FlextTypes.Dict]",
                    service._close_stream(stream),
                ),
            }

            handler = command_handlers.get(command)
            return (
                handler()
                if handler
                else FlextResult.fail(f"Unknown stream command: {command}")
            )

    # === PRIVATE IMPLEMENTATION METHODS ===

    def _start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Start server with REAL gRPC server implementation."""
        if len(self._active_servers) >= self._max_servers:
            return FlextResult.fail(
                f"Maximum server limit reached ({self._max_servers})"
            )

        self._startup_start_time = time.time()

        start_result = server.start()
        if start_result.is_failure:
            return start_result

        starting_server = start_result.unwrap()
        return self._create_and_start_grpc_server(starting_server)

    def _create_and_start_grpc_server(
        self, starting_server: FlextGrpcServer
    ) -> FlextResult[FlextGrpcServer]:
        """Create and start the actual gRPC server."""
        server_key = f"{starting_server.host}:{starting_server.port}"

        try:
            grpc_server = grpc.server(self._thread_pool)
            port_result = self._configure_server_port(grpc_server, starting_server)
            if port_result.is_failure:
                grpc_server.stop(grace=1.0)
                return port_result

            configured_server = port_result.unwrap()
            server_key = f"{configured_server.host}:{configured_server.port}"

            grpc_server.start()
            return self._finalize_server_startup(
                grpc_server, configured_server, server_key
            )

        except Exception as e:
            return FlextResult.fail(f"Failed to start gRPC server: {e}")

    def _configure_server_port(
        self, grpc_server: grpc.Server, server: FlextGrpcServer
    ) -> FlextResult[FlextGrpcServer]:
        """Configure server port binding."""
        if server.port == 0:
            actual_port = grpc_server.add_insecure_port(f"{server.host}:0")
            return FlextResult.ok(server.model_copy(update={"port": actual_port}))
        grpc_server.add_insecure_port(f"{server.host}:{server.port}")
        return FlextResult.ok(server)

    def _finalize_server_startup(
        self, grpc_server: object, server: FlextGrpcServer, server_key: str
    ) -> FlextResult[FlextGrpcServer]:
        """Finalize server startup."""
        self._active_servers[server_key] = cast(
            "FlextGrpcProtocols.Grpc.ServerProtocol", grpc_server
        )

        running_result = server.mark_running()
        if running_result.is_failure:
            cast("FlextGrpcProtocols.Grpc.ServerProtocol", grpc_server).stop_server(
                grace_period=1.0
            )
            self._active_servers.pop(server_key, None)
            return running_result

        startup_time = time.time() - getattr(self, "_startup_start_time", time.time())
        self._server_metrics[server_key] = {
            "startup_time": startup_time,
            "started_at": time.time(),
            "connection_count": 0.0,
            "request_count": 0.0,
        }

        return FlextResult.ok(running_result.unwrap())

    def _stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop server with graceful shutdown."""
        stop_result = server.stop()
        if stop_result.is_failure:
            return stop_result

        stopping_server = stop_result.unwrap()
        server_key = f"{stopping_server.host}:{stopping_server.port}"

        if server_key in self._active_servers:
            grpc_server = self._active_servers[server_key]
            grpc_server.stop_server(grace_period=2.0)
            del self._active_servers[server_key]
            self._server_metrics.pop(server_key, None)

        return stopping_server.mark_stopped()

    def _add_service_to_server(
        self, server: FlextGrpcServer, service_def: FlextGrpcServiceEntity
    ) -> FlextResult[FlextGrpcServer]:
        """Add service to server."""
        if server.state != "running":
            return FlextResult.fail(
                f"Cannot add service to server in state: {server.state}"
            )

        server_key = f"{server.host}:{server.port}"

        if server_key not in self._active_servers:
            return FlextResult.fail(f"No active gRPC server found for {server_key}")

        grpc_server = self._active_servers[server_key]
        real_servicer = create_real_servicer(server_key)
        add_FlextGrpcServiceServicer_to_server(
            real_servicer, cast("grpc.Server", grpc_server)
        )

        add_result = server.add_service(service_def)
        return (
            FlextResult.ok(add_result.unwrap()) if add_result.is_success else add_result
        )

    def _get_server_status(
        self, server: FlextGrpcServer
    ) -> FlextResult[FlextTypes.Dict]:
        """Get server status."""
        server_key = f"{server.host}:{server.port}"
        metrics = self._server_metrics.get(server_key, {})
        current_time = time.time()

        return FlextResult.ok({
            "state": server.state,
            "host": server.host,
            "port": server.port,
            "max_workers": server.max_workers,
            "address": server.address,
            "is_running": server.is_running,
            "service_count": len(server.services),
            "grpc_server_active": server_key in self._active_servers,
            "server_key": server_key,
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
        })

    def _connect_client(self, client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
        """Connect client with channel establishment."""
        if client.channel is None:
            return FlextResult.fail("Client has no channel to connect")

        target = client.target
        if target is None:
            return FlextResult.fail("Client has no target to connect to")

        grpc_channel: grpc.Channel | None = None
        for attempt in range(self._max_retry_attempts):
            try:
                grpc_channel = grpc.insecure_channel(target)
                grpc.channel_ready_future(grpc_channel).result(
                    timeout=self._connection_timeout
                )

                self._active_channels[target] = cast(
                    "FlextGrpcProtocols.Grpc.ClientProtocol", grpc_channel
                )
                self._client_metrics[target] = {
                    "connected_at": time.time(),
                    "connection_attempt": attempt + 1,
                    "total_requests": 0,
                    "failed_requests": 0,
                }

                connect_result = client.channel.connect()
                if connect_result.is_success:
                    ready_result = connect_result.unwrap().mark_ready()
                    if ready_result.is_success:
                        return FlextResult.ok(
                            client.model_copy(update={"channel": ready_result.unwrap()})
                        )

            except grpc.FutureTimeoutError:
                if grpc_channel:
                    grpc_channel.close()
                if attempt == self._max_retry_attempts - 1:
                    return FlextResult.fail(
                        f"Failed to connect to {target}: connection timeout"
                    )

                wait_time = (2**attempt) * 0.5
                time.sleep(wait_time)

        return FlextResult.fail(f"Connection failed to {target}")

    def _disconnect_client(
        self, client: FlextGrpcClient
    ) -> FlextResult[FlextGrpcClient]:
        """Disconnect client."""
        if client.channel is None:
            return FlextResult.fail("Client has no channel to disconnect")

        target = client.target
        if target is None:
            return FlextResult.fail("Client has no target")

        if target in self._active_channels:
            grpc_channel = self._active_channels[target]
            cast(
                "FlextGrpcProtocols.Grpc.ClientProtocol", grpc_channel
            ).disconnect_client(grpc_channel)
            del self._active_channels[target]

        disconnect_result = client.channel.disconnect()
        if disconnect_result.is_success:
            return FlextResult.ok(
                client.model_copy(update={"channel": disconnect_result.unwrap()})
            )
        return FlextResult[FlextGrpcClient].fail(
            disconnect_result.error or "Disconnect failed"
        )

    def _make_call(
        self, client: FlextGrpcClient, method: str, request: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Make gRPC call."""
        if not client.is_connected:
            return FlextResult.fail(
                f"Cannot make call with disconnected client: {client.target}"
            )

        target = client.target
        if target is None or target not in self._active_channels:
            return FlextResult.fail(f"No active channel for {target}")

        try:
            grpc_channel = cast("grpc.Channel", self._active_channels[target])
            grpc.channel_ready_future(grpc_channel).result(timeout=1.0)

            stub = FlextGrpcServiceStub(grpc_channel)

            # Handle different method types
            if method == "Echo":
                echo_request = EchoRequest(message=str(request), metadata={})
                response = stub.Echo(echo_request)
                return FlextResult.ok({
                    "method": "Echo",
                    "status": "success",
                    "message": response.message,
                    "server_id": response.server_id,
                    "timestamp": response.timestamp,
                })
            if method == "HealthCheck":
                health_request = HealthRequest(service="FlextGrpcService")
                health_response = stub.HealthCheck(health_request)
                return FlextResult.ok({
                    "method": "HealthCheck",
                    "status": "success",
                    "serving_status": health_response.status,
                    "message": health_response.message,
                })
            echo_request = EchoRequest(message=f"Method: {method}")
            response = stub.Echo(echo_request)
            return FlextResult.ok({
                "method": method,
                "status": "success",
                "message": response.message,
                "server_id": response.server_id,
                "timestamp": response.timestamp,
            })

        except grpc.RpcError as rpc_error:
            return FlextResult.fail(
                f"gRPC call failed: {rpc_error.code()} - {rpc_error.details()}"
            )
        except Exception as e:
            return FlextResult.fail(f"Failed to make gRPC call: {e}")

    def _get_client_status(
        self, client: FlextGrpcClient
    ) -> FlextResult[FlextTypes.Dict]:
        """Get client status."""
        target = client.target
        grpc_channel_active = target is not None and target in self._active_channels

        if grpc_channel_active and target:
            grpc_channel = self._active_channels[target]
            with contextlib.suppress(grpc.FutureTimeoutError):
                grpc.channel_ready_future(cast("grpc.Channel", grpc_channel)).result(
                    timeout=0.1
                )

        return FlextResult.ok({
            "channel_state": client.channel.state if client.channel else "no_channel",
            "target": client.target,
            "is_connected": client.is_connected,
            "grpc_channel_active": grpc_channel_active,
        })

    def _create_stream(
        self, stream: FlextGrpcStream, target: str | None = None
    ) -> FlextResult[FlextGrpcStream]:
        """Create stream."""
        if target is None:
            target = f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.DEFAULT_GRPC_PORT}"

        if target not in self._active_channels:
            grpc_channel = grpc.insecure_channel(target)
            self._active_channels[target] = cast(
                "FlextGrpcProtocols.Grpc.ClientProtocol", grpc_channel
            )

        grpc_channel = cast("grpc.Channel", self._active_channels[target])
        stub = FlextGrpcServiceStub(grpc_channel)

        stream_key = f"{stream.id}_{stream.stream_type}"
        self._active_streams[stream_key] = {
            "stream_id": stream.id,
            "type": stream.stream_type,
            "created_at": stream.created_at.timestamp(),
            "active": True,
            "target": target,
            "stub": stub,
            "channel": grpc_channel,
            "request_buffer": [],
            "request_queue": Queue(
                maxsize=self.StreamingConstants.BIDIRECTIONAL_STREAMING_QUEUE_SIZE
            ),
            "response_buffer": deque(
                maxlen=self.StreamingConstants.SERVER_STREAMING_BATCH_SIZE
            ),
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
            "max_queue_size": self.StreamingConstants.BIDIRECTIONAL_STREAMING_QUEUE_SIZE,
            "current_queue_size": 0,
            "health_status": "healthy",
            "last_health_check": time.time(),
            "buffer_size_bytes": 0,
            "max_buffer_size_bytes": self.StreamingConstants.MAX_BUFFER_SIZE_BYTES,
            "memory_pressure_score": 0.0,
            "last_memory_cleanup": time.time(),
        }

        return FlextResult.ok(stream)

    def _send_data(
        self, stream: FlextGrpcStream, data: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Send data through stream."""
        stream_key = f"{stream.id}_{stream.stream_type}"

        if stream_key not in self._active_streams:
            return FlextResult.fail(f"Stream {stream_key} not found")

        stream_info = self._active_streams[stream_key]

        try:
            sequence_counter = stream_info.get("sequence_counter", 0)
            if not isinstance(sequence_counter, int):
                sequence_counter = 0
            stream_request = StreamRequest(
                data=str(data), sequence=int(sequence_counter)
            )

            stub = stream_info.get("stub")
            if stub is None:
                return FlextResult.fail("Stream stub not available")

            if stream.stream_type == "client_streaming":
                return self._handle_client_streaming(
                    stream, stream_info, stream_request, data, stub
                )
            if stream.stream_type == "server_streaming":
                return self._handle_server_streaming(
                    stream, stream_info, stream_request, data, stub
                )
            stream_info["sequence_counter"] = int(sequence_counter) + 1
            return FlextResult.ok({
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "sequence": int(sequence_counter),
            })

        except Exception as e:
            return FlextResult.fail(f"Failed to send data: {e}")

    def _close_stream(self, stream: FlextGrpcStream) -> FlextResult[FlextGrpcStream]:
        """Close gRPC stream."""
        stream_key = f"{stream.id}_{stream.stream_type}"
        self._active_streams.pop(stream_key, None)
        return FlextResult.ok(stream)

    def _handle_client_streaming(
        self,
        stream: FlextGrpcStream,
        stream_info: dict,
        stream_request: object,
        data: object,
        stub: object,
    ) -> FlextResult[FlextTypes.Dict]:
        """Handle client streaming."""
        request_buffer = stream_info.get("request_buffer", [])
        current_buffer_size = FlextGrpcUtilities.SystemUtilities.get_buffer_size_bytes(
            request_buffer
        )
        system_memory = FlextGrpcUtilities.SystemUtilities.get_system_memory_usage()

        stream_info["buffer_size_bytes"] = current_buffer_size
        stream_info["memory_pressure_score"] = system_memory

        should_flush = (
            len(request_buffer)
            >= self.StreamingConstants.CLIENT_STREAMING_BUFFER_THRESHOLD
            or str(data) == "__FLUSH_BUFFER__"
            or current_buffer_size
            > self.StreamingConstants.MAX_BUFFER_SIZE_BYTES
            * self.StreamingConstants.ADAPTIVE_BUFFER_SCALING_FACTOR
            or system_memory > self.StreamingConstants.MEMORY_PRESSURE_THRESHOLD
        )

        if not should_flush or len(request_buffer) == 0:
            request_buffer.append(stream_request)

        sequence_counter = stream_info.get("sequence_counter", 0)
        stream_info["sequence_counter"] = sequence_counter + 1
        stream_info["last_activity"] = time.time()

        if should_flush:
            response = stub.ClientStream(iter(request_buffer))
            request_buffer.clear()
            stream_info["last_memory_cleanup"] = time.time()

            if system_memory > self.StreamingConstants.MEMORY_PRESSURE_THRESHOLD:
                FlextGrpcUtilities.SystemUtilities.trigger_memory_cleanup()

            stream_info["buffer_size_bytes"] = 0

            return FlextResult.ok({
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "buffered_count": len(request_buffer) + 1,
                "response": {
                    "data": response.data,
                    "sequence": response.sequence,
                    "server_id": response.server_id,
                    "timestamp": response.timestamp,
                },
            })
        return FlextResult.ok({
            "sent": str(data),
            "stream_type": stream.stream_type,
            "stream_id": stream.id,
            "buffer_status": "buffered",
            "buffer_size": len(request_buffer),
            "sequence": sequence_counter + 1,
        })

    def _handle_server_streaming(
        self,
        stream: FlextGrpcStream,
        stream_info: dict,
        stream_request: object,
        data: object,
        stub: object,
    ) -> FlextResult[FlextTypes.Dict]:
        """Handle server streaming."""
        try:
            response_iterator = cast("FlextGrpcServiceStub", stub).ServerStream(
                stream_request
            )

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
                if response_count >= FlextGrpcConstants.MAX_RESPONSE_COUNT:
                    break

            sequence_counter = stream_info.get("sequence_counter", 0)
            stream_info["sequence_counter"] = sequence_counter + 1

            return FlextResult.ok({
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "sequence": sequence_counter + 1,
                "responses": responses,
                "response_count": response_count,
            })

        except Exception as e:
            return FlextResult.fail(f"Server streaming failed: {e}")

    def _start_metrics_collection(self) -> None:
        """Start background metrics collection."""
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
                logger = logging.getLogger(__name__)
                logger.warning(f"Background metrics collection failed: {e}")

    def _update_global_metrics(self) -> None:
        """Update global streaming metrics."""
        self._global_metrics["total_streams_active"] = len(self._active_streams)

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

    # === NESTED COMPATIBILITY CLASSES ===

    class ClientService:
        """Nested compatibility class for client operations."""

        def __init__(self, parent_service: FlextGrpcService) -> None:
            """Initialize nested compatibility class for client operations."""
            self._service = parent_service
            self._logger = FlextLogger(__name__)

        def connect(self, target: str) -> FlextResult[FlextGrpcClient]:
            """Connect to gRPC server."""
            return self._service.connect_client(target)

        def disconnect(self, client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
            """Disconnect gRPC client."""
            return self._service.disconnect_client(client)

        def call(
            self, client: FlextGrpcClient, method: str, request: object
        ) -> FlextResult[FlextTypes.Dict]:
            """Make gRPC call."""
            return self._service.make_call(client, method, request)

        def get_status(self, client: FlextGrpcClient) -> FlextResult[FlextTypes.Dict]:
            """Get client status."""
            return self._service.get_client_status(client)

        def execute(
            self, command: str, *args: object, **kwargs: object
        ) -> FlextResult[FlextGrpcClient | FlextTypes.Dict]:
            """Execute client command."""
            if command == "connect":
                return self.connect(cast("str", args[0]))
            if command == "disconnect":
                return self.disconnect(cast("FlextGrpcClient", args[0]))
            if command == "call":
                return self.call(
                    cast("FlextGrpcClient", args[0]),
                    cast("str", kwargs.get("method_name", "")),
                    cast("object", kwargs.get("data")),
                )
            if command == "status":
                return self.get_status(cast("FlextGrpcClient", args[0]))
            return FlextResult.fail(f"Unknown client command: {command}")

    class ServerService:
        """Backward compatibility facade for server operations."""

        def __init__(self) -> None:
            """Initialize backward compatibility facade for server operations."""
            self._service = FlextGrpcService()

        def start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
            """Start server."""
            return self._service.start_server(server)

        def stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
            """Stop server."""
            return self._service.stop_server(server)

        def get_server_status(
            self, server: FlextGrpcServer
        ) -> FlextResult[FlextTypes.Dict]:
            """Get server status."""
            return self._service.get_server_status(server)

        def execute(
            self, command: str, *args: object, **_kwargs: object
        ) -> FlextResult[FlextGrpcServer | FlextTypes.Dict]:
            """Execute server command."""
            if command == "start":
                return self.start_server(cast("FlextGrpcServer", args[0]))
            if command == "stop":
                return self.stop_server(cast("FlextGrpcServer", args[0]))
            if command == "status":
                return self.get_server_status(cast("FlextGrpcServer", args[0]))
            return FlextResult.fail(f"Unknown server command: {command}")

    class StreamService:
        """Backward compatibility facade for streaming operations."""

        def __init__(self) -> None:
            """Initialize backward compatibility facade for streaming operations."""
            self._service = FlextGrpcService()
            self._logger = FlextLogger(__name__)

        def create_stream(
            self, stream_type: str, target: str | None = None, **kwargs: object
        ) -> FlextResult[FlextGrpcStream]:
            """Create gRPC stream."""
            return self._service.create_stream(stream_type, target, **kwargs)

        def send_data(
            self, stream: FlextGrpcStream, data: object
        ) -> FlextResult[FlextTypes.Dict]:
            """Send data to stream."""
            return self._service.send_data(stream, data)

        def close_stream(self, stream: FlextGrpcStream) -> FlextResult[FlextGrpcStream]:
            """Close gRPC stream."""
            return self._service.close_stream(stream)

        def execute(
            self, command: str, *args: object, **kwargs: object
        ) -> FlextResult[FlextGrpcStream | FlextTypes.Dict]:
            """Execute stream command."""
            if command == "create":
                return self.create_stream(
                    cast("str", kwargs.get("stream_type", "unary")),
                    cast("str | None", kwargs.get("target")),
                    **cast("FlextTypes.Dict", kwargs),
                )
            if command == "send":
                return self.send_data(
                    cast("FlextGrpcStream", args[0]), cast("object", kwargs.get("data"))
                )
            if command == "close":
                return self.close_stream(cast("FlextGrpcStream", args[0]))
            return FlextResult.fail(f"Unknown stream command: {command}")


__all__ = [
    "FlextGrpcService",  # Main service class with nested compatibility classes
]
