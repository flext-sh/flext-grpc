"""FLEXT gRPC Services - SOLID Service Architecture with Delegation.

Generic service classes using SOLID principles, delegation, and patterns.
Each class has single responsibility with clear separation of concerns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import TypeVar

import grpc
from flext_core import FlextTypes, r

from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.entities import FlextGrpcEntities
from flext_grpc.proto import (
    EchoRequest,
    FlextGrpcServiceStub,
    HealthRequest,
    add_FlextGrpcServiceServicer_to_server,
)
from flext_grpc.protocols import p
from flext_grpc.real_servicer import create_real_servicer
from flext_grpc.typings import t
from flext_grpc.utilities import FlextGrpcUtilities

T = TypeVar("T")

# Protocol reference from centralized protocols.py for backward compatibility
GrpcResourceManager = p.Grpc.ResourceManagerProtocol


class ServerLifecycleManager(ABC):
    """Abstract base for server lifecycle management."""

    @abstractmethod
    def start_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Start server implementation."""

    @abstractmethod
    def stop_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Stop server implementation."""


class ClientConnectionManager(ABC):
    """Abstract base for client connection management."""

    @abstractmethod
    def connect(self, target: str) -> r[FlextGrpcEntities.Client]:
        """Connect to target."""

    @abstractmethod
    def disconnect(
        self,
        client: FlextGrpcEntities.Client,
    ) -> r[FlextGrpcEntities.Client]:
        """Disconnect client."""


class StreamProcessor(ABC):
    """Abstract base for stream processing."""

    @abstractmethod
    def create_stream(
        self,
        **kwargs: str | int | bool | None,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Create stream."""

    @abstractmethod
    def send_data(
        self,
        stream: FlextGrpcEntities.GrpcStream,
        data: t.ConfigValue,
    ) -> r[dict[str, object]]:
        """Send data through stream.

        Note: Uses Any for gRPC message compatibility
        """

    @abstractmethod
    def close_stream(
        self,
        stream: FlextGrpcEntities.GrpcStream,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Close stream."""


class MetricsCollector:
    """Dedicated metrics collection with thread safety."""

    def __init__(self) -> None:
        """Initialize metrics collector with thread-safe storage."""
        super().__init__()
        self._metrics: dict[str, object] = {}
        self._lock = threading.RLock()

    def record_metric(self, key: str, value: object) -> None:
        """Thread-safe metric recording.

        Args:
        key: Metric identifier
        value: Metric value (supports any JSON-serializable type)

        """
        with self._lock:
            self._metrics[key] = value

    def get_metric(self, key: str) -> FlextTypes.JsonValue:
        """Thread-safe metric retrieval.

        Returns:
        Metric value or None if not found

        """
        with self._lock:
            value = self._metrics.get(key)
            # Convert to t.GeneralValueType for type compatibility
            if value is None:
                return None
            # Type narrowing: ensure value is t.GeneralValueType
            if isinstance(value, (str, int, float, bool, type(None))):
                return value
            if isinstance(value, (list, tuple)):
                return list(value)
            if isinstance(value, dict):
                return dict(value)
            return str(value)

    def get_all_metrics(self) -> dict[str, object]:
        """Get all metrics snapshot."""
        with self._lock:
            return self._metrics.copy()


class ConnectionPool:
    """Generic connection pool with resource management."""

    def __init__(self, max_size: int = 10) -> None:
        """Initialize connection pool.

        Args:
        max_size: Maximum pool size

        """
        super().__init__()
        self._pool: Queue[object] = Queue(maxsize=max_size)
        self._active: set[object] = set()
        self._lock = threading.RLock()

    def acquire(self) -> r[object]:
        """Acquire connection from pool."""
        try:
            with self._lock:
                if not self._pool.empty():
                    conn = self._pool.get_nowait()
                    self._active.add(conn)
                    return r.ok(conn)
                return r.fail("No available connections")
        except Exception as e:
            return r.fail(f"Connection acquisition failed: {e}")

    def release(self, connection: object) -> r[bool]:
        """Release connection back to pool."""
        try:
            with self._lock:
                if connection in self._active:
                    self._active.remove(connection)
                    if self._pool.full():
                        return r.ok(True)
                    self._pool.put_nowait(connection)
                return r.ok(True)
        except Exception as e:
            return r.fail(f"Connection release failed: {e}")

    def cleanup(self) -> r[bool]:
        """Cleanup all connections."""
        with self._lock:
            self._active.clear()
            while not self._pool.empty():
                try:
                    self._pool.get_nowait()
                except Exception:
                    break
        return r.ok(True)


class GrpcServerManager(ServerLifecycleManager):
    """Dedicated server lifecycle management."""

    def __init__(self) -> None:
        """Initialize server manager with metrics tracking."""
        super().__init__()
        self._active_servers: dict[str, object] = {}
        self._metrics = MetricsCollector()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=50,
            thread_name_prefix="flext-grpc-server",
        )

    def start_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Start gRPC server with proper lifecycle."""
        server_key = f"{server.host}:{server.port}"

        if server_key in self._active_servers:
            return r.fail(f"Server already running: {server_key}")

        try:
            # Transition to starting state
            starting_result = server.start()
            if starting_result.is_failure:
                return starting_result

            starting_server = starting_result.value

            # Create actual gRPC server
            grpc_server = grpc.server(self._thread_pool)
            grpc_server.add_insecure_port(
                f"{starting_server.host}:{starting_server.port}",
            )

            # Add services if any
            for _service in starting_server.services:
                real_servicer = create_real_servicer(server_key)
                add_FlextGrpcServiceServicer_to_server(real_servicer, grpc_server)

            # Start server
            grpc_server.start()

            # Store server reference
            self._active_servers[server_key] = grpc_server

            # Record metrics
            self._metrics.record_metric(f"{server_key}_started_at", time.time())

            # Mark as running
            return starting_server.mark_running()

        except Exception as e:
            return r.fail(f"Server start failed: {e}")

    def stop_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Stop gRPC server gracefully."""
        server_key = f"{server.host}:{server.port}"

        if server_key not in self._active_servers:
            return r.fail(f"No active server: {server_key}")

        try:
            # Transition to stopping
            stopping_result = server.stop()
            if stopping_result.is_failure:
                return stopping_result

            stopping_server = stopping_result.value

            # Stop gRPC server
            grpc_server = self._active_servers[server_key]
            # Type narrowing: ensure grpc_server has stop method
            if hasattr(grpc_server, "stop"):
                grpc_server.stop(grace=2.0)

            # Cleanup
            del self._active_servers[server_key]
            self._metrics.record_metric(f"{server_key}_stopped_at", time.time())

            return stopping_server.mark_stopped()

        except Exception as e:
            return r.fail(f"Server stop failed: {e}")

    def get_server_metrics(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[dict[str, object]]:
        """Get server metrics."""
        server_key = f"{server.host}:{server.port}"
        started_at = self._metrics.get_metric(f"{server_key}_started_at")
        stopped_at = self._metrics.get_metric(f"{server_key}_stopped_at")
        # Ensure metrics are object compatible
        metrics: dict[str, object] = {
            "is_active": server_key in self._active_servers,
            "started_at": started_at if started_at is not None else None,
            "stopped_at": stopped_at if stopped_at is not None else None,
        }
        return r[dict[str, object]].ok(metrics)


class GrpcClientManager(ClientConnectionManager):
    """Dedicated client connection management."""

    def __init__(self) -> None:
        """Initialize client manager with connection pooling."""
        super().__init__()
        self._active_channels: dict[str, object] = {}
        self._connection_pool = ConnectionPool(max_size=20)
        self._metrics = MetricsCollector()

    def connect(self, target: str) -> r[FlextGrpcEntities.Client]:
        """Establish client connection with pooling."""
        if target in self._active_channels:
            return FlextGrpcUtilities.create_client_entity(target=target)

        try:
            # Create channel
            grpc_channel: grpc.Channel = grpc.insecure_channel(target)
            grpc.channel_ready_future(grpc_channel).result(timeout=5.0)

            # Store channel
            self._active_channels[target] = grpc_channel
            self._metrics.record_metric(f"{target}_connected_at", time.time())

            # Create client entity
            return FlextGrpcUtilities.create_client_entity(target=target)

        except Exception as e:
            return r.fail(f"Connection failed: {e}")

    def disconnect(
        self,
        client: FlextGrpcEntities.Client,
    ) -> r[FlextGrpcEntities.Client]:
        """Disconnect client and cleanup resources."""
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""

        if target and target in self._active_channels:
            grpc_channel = self._active_channels[target]
            # Type narrowing: ensure grpc_channel has close method
            if hasattr(grpc_channel, "close") and callable(
                getattr(grpc_channel, "close", None),
            ):
                grpc_channel.close()
            del self._active_channels[target]

        return r.ok(client)

    def make_call(
        self,
        client: FlextGrpcEntities.Client,
        method: str,
        request: t.ConfigValue,
    ) -> r[dict[str, object]]:
        """Execute gRPC call through client.

        Args:
        client: Client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        """
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""

        if not target or target not in self._active_channels:
            return r.fail("Client not connected")

        try:
            channel_obj = self._active_channels[target]
            # Type narrowing: ensure channel_obj is grpc.Channel
            if not isinstance(channel_obj, grpc.Channel):
                return r[dict[str, object]].fail(
                    f"Invalid channel type: {type(channel_obj)}",
                )
            grpc_channel: grpc.Channel = channel_obj
            stub = FlextGrpcServiceStub(grpc_channel)

            # Route to appropriate method
            if method == "Echo":
                echo_response = stub.Echo(
                    EchoRequest(message=str(request), metadata={}),
                )
                return r.ok({
                    "method": "Echo",
                    "message": echo_response.message,
                    "server_id": echo_response.server_id,
                    "timestamp": echo_response.timestamp,
                })
            if method == "HealthCheck":
                health_response = stub.HealthCheck(
                    HealthRequest(service="FlextGrpcService"),
                )
                return r.ok({
                    "method": "HealthCheck",
                    "status": health_response.status,
                    "message": health_response.message,
                })

            return r.fail(f"Unsupported method: {method}")

        except grpc.RpcError as e:
            return r.fail(f"gRPC call failed: {e.code()} - {e.details()}")
        except Exception as e:
            return r.fail(f"Call execution failed: {e}")


class GrpcStreamManager(StreamProcessor):
    """Dedicated stream processing with buffering."""

    def __init__(self) -> None:
        """Initialize stream manager with metrics tracking."""
        super().__init__()
        self._active_streams: dict[str, object] = {}
        self._metrics = MetricsCollector()

    def create_stream(
        self,
        **kwargs: str | int | bool | None,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Create stream with proper setup."""
        method_name = str(kwargs.get("method_name", "DefaultMethod"))
        stream_type = str(kwargs.get("stream_type", "unary"))

        # Create entity first
        stream_result = FlextGrpcUtilities.create_stream_entity(
            method_name,
            stream_type,
        )
        if stream_result.is_failure:
            return stream_result

        stream = stream_result.value
        stream_key = f"{stream.id}_{stream.stream_type}"

        # Setup stream metadata
        self._active_streams[stream_key] = {
            "stream": stream,
            "created_at": time.time(),
            "buffer": deque(maxlen=500),
            "active": True,
        }

        self._metrics.record_metric(f"{stream_key}_created", time.time())
        return r.ok(stream)

    def send_data(
        self,
        stream: FlextGrpcEntities.GrpcStream,
        data: t.ConfigValue,
    ) -> r[dict[str, object]]:
        """Send data with buffering strategy.

        Args:
        stream: Stream entity
        data: Message data (gRPC protocol message - dynamic type)

        """
        stream_key = f"{stream.id}_{stream.stream_type}"

        if stream_key not in self._active_streams:
            return r.fail("Stream not found")

        stream_info = self._active_streams[stream_key]

        try:
            # Type narrowing: ensure stream_info is a dict
            if not isinstance(stream_info, dict):
                return r[dict[str, object]].fail("Invalid stream info type")
            # Buffer management
            buffer = stream_info.get("buffer")
            if buffer is None:
                return r[dict[str, object]].fail("Buffer not found in stream info")
            buffer.append(data)

            # For now, just acknowledge (streaming logic would go here)
            return r.ok({
                "stream_id": stream.id,
                "data_sent": str(data),
                "buffer_size": len(buffer),
            })

        except Exception as e:
            return r.fail(f"Data send failed: {e}")

    def close_stream(
        self,
        stream: FlextGrpcEntities.GrpcStream,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Close stream and cleanup."""
        stream_key = f"{stream.id}_{stream.stream_type}"

        if stream_key in self._active_streams:
            del self._active_streams[stream_key]

        return r.ok(stream)


class FlextGrpcServices:
    """Generic gRPC service facade using SOLID principles and delegation.

    Delegates responsibilities to specialized managers while maintaining clean API.
    Uses composition over inheritance and dependency injection.
    """

    def __init__(self) -> None:
        """Initialize service with dependency injection and delegation."""
        super().__init__()

        # Dependency injection - each manager has single responsibility
        self._server_manager = GrpcServerManager()
        self._client_manager = GrpcClientManager()
        self._stream_manager = GrpcStreamManager()
        self._metrics_collector = MetricsCollector()
        self._resource_manager = ConnectionPool(max_size=20)

    # === DELEGATED SERVER OPERATIONS ===

    def start_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Delegate server start to specialized manager."""
        return self._server_manager.start_server(server)

    def stop_server(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[FlextGrpcEntities.Server]:
        """Delegate server stop to specialized manager."""
        return self._server_manager.stop_server(server)

    def get_server_status(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[dict[str, object]]:
        """Delegate server status to specialized manager."""
        return self._server_manager.get_server_metrics(server)

    # === DELEGATED CLIENT OPERATIONS ===

    def connect_client(self, target: str) -> r[FlextGrpcEntities.Client]:
        """Delegate client connection to specialized manager."""
        return self._client_manager.connect(target)

    def disconnect_client(
        self,
        client: FlextGrpcEntities.Client,
    ) -> r[FlextGrpcEntities.Client]:
        """Delegate client disconnection to specialized manager."""
        return self._client_manager.disconnect(client)

    def make_call(
        self,
        client: FlextGrpcEntities.Client,
        method: str,
        request: t.ConfigValue,
    ) -> r[dict[str, object]]:
        """Delegate method calls to specialized manager.

        Args:
        client: Client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        """
        return self._client_manager.make_call(client, method, request)

    def get_client_status(
        self,
        client: FlextGrpcEntities.Client,
    ) -> r[dict[str, object]]:
        """Get client status through delegation."""
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""
        is_connected = target and target in self._client_manager._active_channels
        return r.ok({"connected": is_connected, "target": target})

    # === DELEGATED STREAM OPERATIONS ===

    def create_stream(
        self,
        method_name: str | int | None = "DefaultMethod",
        **kwargs: str | int | bool | None,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Delegate stream creation to specialized manager."""
        # Ensure method_name is a string
        method_name_str = (
            str(method_name) if method_name is not None else "DefaultMethod"
        )
        kwargs["method_name"] = method_name_str
        return self._stream_manager.create_stream(**kwargs)

    def send_data(
        self,
        stream: FlextGrpcEntities.GrpcStream,
        data: t.ConfigValue,
    ) -> r[dict[str, object]]:
        """Delegate data sending to specialized manager.

        Args:
        stream: Stream entity
        data: Message data (gRPC protocol message - dynamic type)

        """
        return self._stream_manager.send_data(stream, data)

    def close_stream(
        self,
        stream: FlextGrpcEntities.GrpcStream,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Delegate stream closing to specialized manager."""
        return self._stream_manager.close_stream(stream)

    # === FACTORY METHODS WITH DELEGATION ===

    def _create_client_entity(
        self,
        target: str,
        options: t.GrpcOptions | None = None,
    ) -> r[FlextGrpcEntities.Client]:
        """Delegate entity creation to utilities.

        Args:
        target: gRPC target address
        options: Channel options (gRPC-specific configuration)

        """
        return FlextGrpcUtilities.create_client_entity(target, options)

    def _create_stream_entity(
        self,
        method_name: str,  # gRPC method name
        stream_type: FlextGrpcConstants.Grpc.StreamTypeLiteral | str,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Delegate entity creation to utilities."""
        return FlextGrpcUtilities.create_stream_entity(method_name, stream_type)

    # === LEGACY COMPATIBILITY METHODS ===

    def _execute_server_command(
        self,
        command: str,
        server: FlextGrpcEntities.Server,
    ) -> r[dict[str, object]]:
        """Execute server-specific commands."""
        if command == "start":
            return self.start_server(server).map(lambda _: {"status": "started"})
        if command == "stop":
            return self.stop_server(server).map(lambda _: {"status": "stopped"})
        if command == "status":
            return self.get_server_status(server)
        return r.fail(f"Unsupported server command: {command}")

    def _execute_client_command(
        self,
        command: str,
        client: FlextGrpcEntities.Client,
        **kwargs: str | int | bool | None,
    ) -> r[dict[str, object]]:
        """Execute client-specific commands."""
        if command == "connect":
            return self.connect_client(str(kwargs.get("target", ""))).map(
                lambda _: {"status": "connected"},
            )
        if command == "disconnect":
            return self.disconnect_client(client).map(
                lambda _: {"status": "disconnected"},
            )
        if command == "status":
            return self.get_client_status(client)
        if command == "call":
            return self.make_call(
                client,
                str(kwargs.get("method", "")),
                kwargs.get("request"),
            )
        return r.fail(f"Unsupported client command: {command}")

    def _execute_stream_command(
        self,
        command: str,
        stream: FlextGrpcEntities.GrpcStream,
        **kwargs: str | int | bool | None,
    ) -> r[dict[str, object]]:
        """Execute stream-specific commands."""
        if command == "create":
            method_name = str(kwargs.get("method_name", "DefaultMethod"))
            return self.create_stream(method_name=method_name, **kwargs).map(
                lambda _: {"status": "created"},
            )
        if command == "send":
            return self.send_data(stream, kwargs.get("data"))
        if command == "close":
            return self.close_stream(stream).map(lambda _: {"status": "closed"})
        return r.fail(f"Unsupported stream command: {command}")

    def execute_grpc(
        self,
        command: str | None = None,
        entity: FlextGrpcEntities.Server
        | FlextGrpcEntities.Client
        | FlextGrpcEntities.GrpcStream
        | dict[str, object]
        | None = None,
        *_args: str | int | bool | None,
        **kwargs: str | int | bool | None,
    ) -> r[dict[str, object]]:
        """Legacy compatibility method - delegates to appropriate manager."""
        if command is None:
            return r.ok({
                "status": "ready",
                "service": "flext-grpc-service",
            })

        if entity is None:
            return r.fail("Entity instance required")

        # Route based on entity type and command
        if isinstance(entity, FlextGrpcEntities.Server):
            return self._execute_server_command(command, entity)
        if isinstance(entity, FlextGrpcEntities.Client):
            return self._execute_client_command(command, entity, **kwargs)
        if isinstance(entity, FlextGrpcEntities.GrpcStream):
            return self._execute_stream_command(command, entity, **kwargs)

        return r.fail(f"Unsupported entity type: {type(entity)}")

    def execute(self, **_kwargs: object) -> r[dict[str, object]]:
        """Execute main service operation."""
        return self.execute_grpc()


__all__ = [
    "ConnectionPool",
    "FlextGrpcServices",
    "GrpcClientManager",
    "GrpcServerManager",
    "GrpcStreamManager",
    "MetricsCollector",
]
