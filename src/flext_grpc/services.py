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
from typing import cast

import grpc
from flext_core import (
    FlextBus,
    FlextConstants,
    FlextContainer,
    FlextContext,
    FlextDispatcher,
    FlextProcessors,
    FlextRegistry,
    FlextResult,
    FlextService,
    FlextTypes,
)

# Factory methods now implemented directly in service class
from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import FlextGrpcEntities

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


class FlextGrpcServices(FlextService):
    """Unified gRPC service class following FLEXT namespace pattern.

    Single class containing all server, client, and streaming functionality.
    Uses nested helper classes for organization while maintaining clean API.
    """

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
        # Logger is provided by parent class FlextService via property
        # No need to set it explicitly

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
        self._max_concurrent_streams: int = 10
        self._stream_buffer_size: int = 500
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
        self._shutdown_event = threading.Event()
        self._metrics_lock = threading.RLock()
        self._metrics_interval = 30.0  # seconds

    # === SERVER OPERATIONS ===

    def start_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Start gRPC server with validation and error handling."""
        return self._start_server(server)

    def stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Stop gRPC server with graceful shutdown."""
        return self._stop_server(server)

    def get_server_status(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextTypes.Dict]:
        """Get server status and metrics."""
        return self._get_server_status(server)

    # === FACTORY METHODS ===

    def _create_client_entity(
        self, target: str, options: FlextTypes.Dict | None = None
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Create a gRPC client entity using utilities."""
        return FlextGrpcUtilities.create_client_entity(target, options)

    def _create_stream_entity(
        self, method_name: str, stream_type: str
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Create a gRPC stream entity using utilities."""
        return FlextGrpcUtilities.create_stream_entity(method_name, stream_type)

    # === CLIENT OPERATIONS ===

    def connect_client(self, target: str) -> FlextResult[FlextGrpcEntities.Client]:
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
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Disconnect gRPC client."""
        return self._disconnect_client(client)

    def make_call(
        self, client: FlextGrpcEntities.Client, method: str, request: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Make gRPC call through client."""
        return self._make_call(client, method, request)

    def get_client_status(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextTypes.Dict]:
        """Get client status."""
        return self._get_client_status(client)

    # === STREAM OPERATIONS ===

    def create_stream(
        self, stream_type: str = "unary", **kwargs: object
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Create gRPC stream."""
        stream_result = self._create_stream_entity(
            method_name=str(kwargs.get("method_name", "DefaultMethod")),
            stream_type=stream_type,
        )
        if stream_result.is_failure:
            return FlextResult.fail(
                f"Stream entity creation failed: {stream_result.error}"
            )
        stream = stream_result.unwrap()
        target_value = kwargs.get("target")
        target_str = str(target_value) if target_value is not None else None
        return self._create_stream(stream, target_str)

    def send_data(
        self, stream: FlextGrpcEntities.GrpcStream, data: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Send data through stream."""
        return self._send_data(stream, data)

    def close_stream(
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Close gRPC stream."""
        return self._close_stream(stream)

    def execute_grpc(
        self,
        command: str | None = None,
        entity: FlextGrpcEntities.Server
        | FlextGrpcEntities.Client
        | FlextGrpcEntities.GrpcStream
        | FlextTypes.Dict
        | None = None,
        *args: object,
        **kwargs: object,
    ) -> FlextResult[FlextTypes.Dict]:
        """Execute gRPC command with routing to appropriate handler."""
        if command is None:
            return FlextResult.ok(
                {
                    "status": "ready",
                    "service": "flext-grpc-service",
                }
            )

        if entity is None:
            return FlextResult.fail("Entity instance required")

        # Route to appropriate handler based on entity type and command
        if isinstance(entity, FlextGrpcEntities.Server):
            return self.ServerOps.execute_command(
                self, command, entity, *args, **kwargs
            )
        if isinstance(entity, FlextGrpcEntities.Client):
            return self.ClientOps.execute_command(
                self, command, entity, *args, **kwargs
            )
        if isinstance(entity, FlextGrpcEntities.GrpcStream):
            return self.StreamOps.execute_command(
                self, command, entity, *args, **kwargs
            )

        return FlextResult.fail(f"Unsupported entity type: {type(entity)}")

    def execute(self) -> FlextResult[FlextTypes.Dict]:
        """Execute main service operation."""
        return self.execute_grpc()

    # === NESTED HELPER CLASSES ===

    class ServerOps:
        """Nested helper class for server operations."""

        @staticmethod
        def execute_command(
            service: FlextGrpcServices,
            command: str,
            server: FlextGrpcEntities.Server,
        ) -> FlextResult[FlextTypes.Dict]:
            """Execute server command with validation."""
            validation = server.validate_business_rules()
            if validation.is_failure:
                return FlextResult.fail(f"Server validation failed: {validation.error}")

            command_handlers: dict[str, Callable[[], FlextResult[FlextTypes.Dict]]] = {
                "start": lambda: service._get_server_status(server),
                "stop": lambda: service._get_server_status(server),
                "status": lambda: service._get_server_status(server),
                "add_service": lambda: FlextResult.ok({"status": "service_added"}),
            }

            handler = command_handlers.get(command)
            return (
                handler()
                if handler
                else FlextResult.fail(f"Unknown server command: {command}")
            )

    class ClientOps:
        """Nested helper class for client operations."""

        @staticmethod
        def execute_command(
            service: FlextGrpcServices,
            command: str,
            client: FlextGrpcEntities.Client,
        ) -> FlextResult[FlextTypes.Dict]:
            """Execute client command with validation."""
            validation = client.validate_business_rules()
            if validation.is_failure:
                return FlextResult.fail(f"Client validation failed: {validation.error}")

            command_handlers: dict[str, Callable[[], FlextResult[FlextTypes.Dict]]] = {
                "connect": lambda: service._get_client_status(client),
                "disconnect": lambda: service._get_client_status(client),
                "status": lambda: service._get_client_status(client),
                "call": lambda: FlextResult.ok({"method_called": True}),
            }

            handler = command_handlers.get(command)
            return (
                handler()
                if handler
                else FlextResult.fail(f"Unknown client command: {command}")
            )

    class StreamOps:
        """Nested helper class for stream operations."""

        @staticmethod
        def execute_command(
            _service: FlextGrpcServices,
            command: str,
            stream: FlextGrpcEntities.GrpcStream,
        ) -> FlextResult[FlextTypes.Dict]:
            """Execute stream command with validation."""
            validation = stream.validate_business_rules()
            if validation.is_failure:
                return FlextResult.fail(f"Stream validation failed: {validation.error}")

            command_handlers: dict[str, Callable[[], FlextResult[FlextTypes.Dict]]] = {
                "create": lambda: FlextResult.ok({"stream_created": True}),
                "send": lambda: FlextResult.ok({"data_sent": True}),
                "close": lambda: FlextResult.ok({"stream_closed": True}),
            }

            handler = command_handlers.get(command)
            return (
                handler()
                if handler
                else FlextResult.fail(f"Unknown stream command: {command}")
            )

    # === PRIVATE IMPLEMENTATION METHODS ===

    def _start_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
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
        self, starting_server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
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
        self, grpc_server: grpc.Server, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Configure server port binding."""
        if server.port == 0:
            actual_port = grpc_server.add_insecure_port(f"{server.host}:0")
            return FlextResult.ok(server.model_copy(update={"port": actual_port}))
        grpc_server.add_insecure_port(f"{server.host}:{server.port}")
        return FlextResult.ok(server)

    def _finalize_server_startup(
        self, grpc_server: object, server: FlextGrpcEntities.Server, server_key: str
    ) -> FlextResult[FlextGrpcEntities.Server]:
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

    def _stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
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
        self, server: FlextGrpcEntities.Server, service_def: FlextGrpcEntities.Service
    ) -> FlextResult[FlextGrpcEntities.Server]:
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
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextTypes.Dict]:
        """Get server status."""
        server_key = f"{server.host}:{server.port}"
        metrics = self._server_metrics.get(server_key, {})
        current_time = time.time()

        return FlextResult.ok(
            {
                "state": server.state,
                "host": server.host,
                "port": server.port,
                "max_workers": server.max_workers,
                "address": f"{server.host}:{server.port}",
                "is_running": server.state == "running",
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
            }
        )

    def _connect_client(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Connect client with channel establishment."""
        if client.channel is None:
            return FlextResult.fail("Client has no channel to connect")

        target = client.channel.target if client.channel else ""
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
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Disconnect client."""
        if client.channel is None:
            return FlextResult.fail("Client has no channel to disconnect")

        target = client.channel.target if client.channel else ""
        if target is None:
            return FlextResult.fail("Client has no target")

        if target in self._active_channels:
            grpc_channel = self._active_channels[target]
            grpc_channel.disconnect_client(grpc_channel)
            del self._active_channels[target]

        disconnect_result = client.channel.disconnect()
        if disconnect_result.is_success:
            return FlextResult.ok(
                client.model_copy(update={"channel": disconnect_result.unwrap()})
            )
        return FlextResult[FlextGrpcEntities.Client].fail(
            disconnect_result.error or "Disconnect failed"
        )

    def _make_call(
        self, client: FlextGrpcEntities.Client, method: str, request: object
    ) -> FlextResult[FlextTypes.Dict]:
        """Make gRPC call."""
        if not client.grpc_stub:
            target = client.channel.target if client.channel else ""
            return FlextResult.fail(
                f"Cannot make call with disconnected client: {target}"
            )

        target = client.channel.target if client.channel else ""
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
                return FlextResult.ok(
                    {
                        "method": "Echo",
                        "status": "success",
                        "message": response.message,
                        "server_id": response.server_id,
                        "timestamp": response.timestamp,
                    }
                )
            if method == "HealthCheck":
                health_request = HealthRequest(service="FlextGrpcService")
                health_response = stub.HealthCheck(health_request)
                return FlextResult.ok(
                    {
                        "method": "HealthCheck",
                        "status": "success",
                        "serving_status": health_response.status,
                        "message": health_response.message,
                    }
                )
            return FlextResult.fail(f"Unsupported method: {method}")

        except grpc.RpcError as rpc_error:
            return FlextResult.fail(
                f"gRPC call failed: {rpc_error.code()} - {rpc_error.details()}"
            )
        except Exception as e:
            return FlextResult.fail(f"Failed to make gRPC call: {e}")

    def _get_client_status(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextTypes.Dict]:
        """Get client status."""
        target = client.channel.target if client.channel else ""
        grpc_channel_active = target is not None and target in self._active_channels

        if grpc_channel_active and target:
            grpc_channel = self._active_channels[target]
            with contextlib.suppress(grpc.FutureTimeoutError):
                grpc.channel_ready_future(cast("grpc.Channel", grpc_channel)).result(
                    timeout=0.1
                )

        return FlextResult.ok(
            {
                "channel_state": client.channel.state
                if client.channel
                else "no_channel",
                "target": client.channel.target if client.channel else "",
                "is_connected": client.grpc_stub is not None,
                "grpc_channel_active": grpc_channel_active,
            }
        )

    def _create_stream(
        self, stream: FlextGrpcEntities.GrpcStream, target: str | None = None
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Create stream."""
        if target is None:
            target = f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT}"

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
                maxsize=FlextGrpcConstants.Streaming.BIDIRECTIONAL_STREAMING_QUEUE_SIZE
            ),
            "response_buffer": deque(
                maxlen=FlextGrpcConstants.Streaming.SERVER_STREAMING_BATCH_SIZE
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
            "max_queue_size": FlextGrpcConstants.Streaming.BIDIRECTIONAL_STREAMING_QUEUE_SIZE,
            "current_queue_size": 0,
            "health_status": "healthy",
            "last_health_check": time.time(),
            "buffer_size_bytes": 0,
            "max_buffer_size_bytes": FlextGrpcConstants.Streaming.MAX_BUFFER_SIZE_BYTES,
            "memory_pressure_score": 0.0,
            "last_memory_cleanup": time.time(),
        }

        return FlextResult.ok(stream)

    def _send_data(
        self, stream: FlextGrpcEntities.GrpcStream, data: object
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

            stub = cast("FlextGrpcServiceStub", stream_info.get("stub"))
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
            return FlextResult.ok(
                {
                    "sent": str(data),
                    "stream_type": stream.stream_type,
                    "stream_id": stream.id,
                    "sequence": int(sequence_counter),
                }
            )

        except Exception as e:
            return FlextResult.fail(f"Failed to send data: {e}")

    def _close_stream(
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Close gRPC stream."""
        stream_key = f"{stream.id}_{stream.stream_type}"
        self._active_streams.pop(stream_key, None)
        return FlextResult.ok(stream)

    def _handle_client_streaming(
        self,
        stream: FlextGrpcEntities.GrpcStream,
        stream_info: dict,
        stream_request: object,
        data: object,
        stub: FlextGrpcServiceStub,
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
            >= FlextGrpcConstants.Streaming.CLIENT_STREAMING_BUFFER_THRESHOLD
            or str(data) == "__FLUSH_BUFFER__"
            or current_buffer_size
            > FlextGrpcConstants.Streaming.MAX_BUFFER_SIZE_BYTES
            * FlextGrpcConstants.Streaming.ADAPTIVE_BUFFER_SCALING_FACTOR
            or system_memory > FlextGrpcConstants.Streaming.MEMORY_PRESSURE_THRESHOLD
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

            if system_memory > FlextGrpcConstants.Streaming.MEMORY_PRESSURE_THRESHOLD:
                FlextGrpcUtilities.SystemUtilities.trigger_memory_cleanup()

            stream_info["buffer_size_bytes"] = 0

            return FlextResult.ok(
                {
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
                }
            )
        return FlextResult.ok(
            {
                "sent": str(data),
                "stream_type": stream.stream_type,
                "stream_id": stream.id,
                "buffer_status": "buffered",
                "buffer_size": len(request_buffer),
                "sequence": sequence_counter + 1,
            }
        )

    def _handle_server_streaming(
        self,
        stream: FlextGrpcEntities.GrpcStream,
        stream_info: dict,
        stream_request: object,
        data: object,
        stub: FlextGrpcServiceStub,
    ) -> FlextResult[FlextTypes.Dict]:
        """Handle server streaming."""
        try:
            response_iterator = stub.ServerStream(stream_request)

            responses = []
            response_count = 0

            for response in response_iterator:
                responses.append(
                    {
                        "data": response.data,
                        "sequence": response.sequence,
                        "server_id": response.server_id,
                        "timestamp": response.timestamp,
                    }
                )
                response_count += 1
                if response_count >= FlextGrpcConstants.Timeouts.MAX_RESPONSE_COUNT:
                    break

            sequence_counter = stream_info.get("sequence_counter", 0)
            stream_info["sequence_counter"] = sequence_counter + 1

            return FlextResult.ok(
                {
                    "sent": str(data),
                    "stream_type": stream.stream_type,
                    "stream_id": stream.id,
                    "sequence": sequence_counter + 1,
                    "responses": responses,
                    "response_count": response_count,
                }
            )

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


__all__ = [
    "FlextGrpcServices",  # Main service class with nested helper classes
]
