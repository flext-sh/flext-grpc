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
from typing import Any, Protocol, TypeVar

import grpc
from flext_core import FlextResult, FlextService

from flext_grpc.entities import FlextGrpcEntities

# Protocol buffer imports
from flext_grpc.proto import (
    EchoRequest,
    FlextGrpcServiceStub,
    HealthRequest,
    add_FlextGrpcServiceServicer_to_server,
)
from flext_grpc.real_servicer import create_real_servicer
from flext_grpc.typings import FlextGrpcTypes
from flext_grpc.utilities import FlextGrpcUtilities

T = TypeVar("T")


class GrpcResourceManager(Protocol):
    """Protocol for resource management."""

    def acquire(self) -> FlextResult[Any]: ...
    def release(self, resource: object) -> FlextResult[None]: ...
    def cleanup(self) -> FlextResult[None]: ...


class ServerLifecycleManager(ABC):
    """Abstract base for server lifecycle management."""

    @abstractmethod
    def start_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Start server implementation."""

    @abstractmethod
    def stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Stop server implementation."""


class ClientConnectionManager(ABC):
    """Abstract base for client connection management."""

    @abstractmethod
    def connect(self, target: str) -> FlextResult[FlextGrpcEntities.Client]:
        """Connect to target."""

    @abstractmethod
    def disconnect(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Disconnect client."""


class StreamProcessor(ABC):
    """Abstract base for stream processing."""

    @abstractmethod
    def create_stream(
        self, **kwargs: str | int | bool | None
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Create stream."""

    @abstractmethod
    def send_data(
        self, stream: FlextGrpcEntities.GrpcStream, data: FlextGrpcTypes.ConfigValue
    ) -> FlextResult[dict[str, Any]]:
        """Send data through stream.

        Note: Uses Any for gRPC message compatibility
        """

    @abstractmethod
    def close_stream(
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Close stream."""


class MetricsCollector:
    """Dedicated metrics collection with thread safety."""

    def __init__(self) -> None:
        """Initialize metrics collector with thread-safe storage."""
        super().__init__()
        self._metrics: dict[str, Any] = {}
        self._lock = threading.RLock()

    def record_metric(self, key: str, value: object) -> None:
        """Thread-safe metric recording.

        Args:
        key: Metric identifier
        value: Metric value (supports any JSON-serializable type)

        """
        with self._lock:
            self._metrics[key] = value

    def get_metric(self, key: str) -> FlextGrpcTypes.JsonValue:
        """Thread-safe metric retrieval.

        Returns:
        Metric value or None if not found

        """
        with self._lock:
            return self._metrics.get(key)

    def get_all_metrics(self) -> dict[str, Any]:
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
        self._pool: Queue[Any] = Queue(maxsize=max_size)
        self._active: set[Any] = set()
        self._lock = threading.RLock()

    def acquire(self) -> FlextResult[Any]:
        """Acquire connection from pool."""
        try:
            with self._lock:
                if not self._pool.empty():
                    conn = self._pool.get_nowait()
                    self._active.add(conn)
                    return FlextResult.ok(conn)
                return FlextResult.fail("No available connections")
        except Exception as e:
            return FlextResult.fail(f"Connection acquisition failed: {e}")

    def release(self, connection: object) -> FlextResult[None]:
        """Release connection back to pool."""
        try:
            with self._lock:
                if connection in self._active:
                    self._active.remove(connection)
                    if self._pool.full():
                        return FlextResult.ok(True)
                    self._pool.put_nowait(connection)
                return FlextResult.ok(True)
        except Exception as e:
            return FlextResult.fail(f"Connection release failed: {e}")

    def cleanup(self) -> FlextResult[None]:
        """Cleanup all connections."""
        with self._lock:
            self._active.clear()
            while not self._pool.empty():
                try:
                    self._pool.get_nowait()
                except Exception:
                    break
        return FlextResult.ok(True)


class GrpcServerManager(ServerLifecycleManager):
    """Dedicated server lifecycle management."""

    def __init__(self) -> None:
        """Initialize server manager with metrics tracking."""
        super().__init__()
        self._active_servers: dict[str, Any] = {}
        self._metrics = MetricsCollector()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=50, thread_name_prefix="flext-grpc-server"
        )

    def start_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Start gRPC server with proper lifecycle."""
        server_key = f"{server.host}:{server.port}"

        if server_key in self._active_servers:
            return FlextResult.fail(f"Server already running: {server_key}")

        try:
            # Transition to starting state
            starting_result = server.start()
            if starting_result.is_failure:
                return starting_result

            starting_server = starting_result.unwrap()

            # Create actual gRPC server
            grpc_server = grpc.server(self._thread_pool)
            grpc_server.add_insecure_port(
                f"{starting_server.host}:{starting_server.port}"
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
            return FlextResult.fail(f"Server start failed: {e}")

    def stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Stop gRPC server gracefully."""
        server_key = f"{server.host}:{server.port}"

        if server_key not in self._active_servers:
            return FlextResult.fail(f"No active server: {server_key}")

        try:
            # Transition to stopping
            stopping_result = server.stop()
            if stopping_result.is_failure:
                return stopping_result

            stopping_server = stopping_result.unwrap()

            # Stop gRPC server
            grpc_server = self._active_servers[server_key]
            grpc_server.stop(grace=2.0)

            # Cleanup
            del self._active_servers[server_key]
            self._metrics.record_metric(f"{server_key}_stopped_at", time.time())

            return stopping_server.mark_stopped()

        except Exception as e:
            return FlextResult.fail(f"Server stop failed: {e}")

    def get_server_metrics(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[dict[str, Any]]:
        """Get server metrics."""
        server_key = f"{server.host}:{server.port}"
        metrics = {
            "is_active": server_key in self._active_servers,
            "started_at": self._metrics.get_metric(f"{server_key}_started_at"),
            "stopped_at": self._metrics.get_metric(f"{server_key}_stopped_at"),
        }
        return FlextResult.ok(metrics)


class GrpcClientManager(ClientConnectionManager):
    """Dedicated client connection management."""

    def __init__(self) -> None:
        """Initialize client manager with connection pooling."""
        super().__init__()
        self._active_channels: dict[str, Any] = {}
        self._connection_pool = ConnectionPool(max_size=20)
        self._metrics = MetricsCollector()

    def connect(self, target: str) -> FlextResult[FlextGrpcEntities.Client]:
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
            return FlextResult.fail(f"Connection failed: {e}")

    def disconnect(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Disconnect client and cleanup resources."""
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""

        if target and target in self._active_channels:
            grpc_channel = self._active_channels[target]
            grpc_channel.close()
            del self._active_channels[target]

        return FlextResult.ok(client)

    def make_call(
        self,
        client: FlextGrpcEntities.Client,
        method: str,
        request: FlextGrpcTypes.ConfigValue,
    ) -> FlextResult[dict[str, Any]]:
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
            return FlextResult.fail("Client not connected")

        try:
            grpc_channel: grpc.Channel = self._active_channels[target]
            stub = FlextGrpcServiceStub(grpc_channel)

            # Route to appropriate method
            if method == "Echo":
                echo_response = stub.Echo(
                    EchoRequest(message=str(request), metadata={})
                )
                return FlextResult.ok({
                    "method": "Echo",
                    "message": echo_response.message,
                    "server_id": echo_response.server_id,
                    "timestamp": echo_response.timestamp,
                })
            if method == "HealthCheck":
                health_response = stub.HealthCheck(
                    HealthRequest(service="FlextGrpcService")
                )
                return FlextResult.ok({
                    "method": "HealthCheck",
                    "status": health_response.status,
                    "message": health_response.message,
                })

            return FlextResult.fail(f"Unsupported method: {method}")

        except grpc.RpcError as e:
            return FlextResult.fail(f"gRPC call failed: {e.code()} - {e.details()}")
        except Exception as e:
            return FlextResult.fail(f"Call execution failed: {e}")


class GrpcStreamManager(StreamProcessor):
    """Dedicated stream processing with buffering."""

    def __init__(self) -> None:
        """Initialize stream manager with metrics tracking."""
        super().__init__()
        self._active_streams: dict[str, Any] = {}
        self._metrics = MetricsCollector()

    def create_stream(
        self, **kwargs: str | int | bool | None
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Create stream with proper setup."""
        method_name = str(kwargs.get("method_name", "DefaultMethod"))
        stream_type = str(kwargs.get("stream_type", "unary"))

        # Create entity first
        stream_result = FlextGrpcUtilities.create_stream_entity(
            method_name, stream_type
        )
        if stream_result.is_failure:
            return stream_result

        stream = stream_result.unwrap()
        stream_key = f"{stream.id}_{stream.stream_type}"

        # Setup stream metadata
        self._active_streams[stream_key] = {
            "stream": stream,
            "created_at": time.time(),
            "buffer": deque(maxlen=500),
            "active": True,
        }

        self._metrics.record_metric(f"{stream_key}_created", time.time())
        return FlextResult.ok(stream)

    def send_data(
        self, stream: FlextGrpcEntities.GrpcStream, data: FlextGrpcTypes.ConfigValue
    ) -> FlextResult[dict[str, Any]]:
        """Send data with buffering strategy.

        Args:
        stream: Stream entity
        data: Message data (gRPC protocol message - dynamic type)

        """
        stream_key = f"{stream.id}_{stream.stream_type}"

        if stream_key not in self._active_streams:
            return FlextResult.fail("Stream not found")

        stream_info = self._active_streams[stream_key]

        try:
            # Buffer management
            buffer = stream_info["buffer"]
            buffer.append(data)

            # For now, just acknowledge (streaming logic would go here)
            return FlextResult.ok({
                "stream_id": stream.id,
                "data_sent": str(data),
                "buffer_size": len(buffer),
            })

        except Exception as e:
            return FlextResult.fail(f"Data send failed: {e}")

    def close_stream(
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Close stream and cleanup."""
        stream_key = f"{stream.id}_{stream.stream_type}"

        if stream_key in self._active_streams:
            del self._active_streams[stream_key]

        return FlextResult.ok(stream)


class FlextGrpcServices(FlextService[Any]):
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
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Delegate server start to specialized manager."""
        return self._server_manager.start_server(server)

    def stop_server(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[FlextGrpcEntities.Server]:
        """Delegate server stop to specialized manager."""
        return self._server_manager.stop_server(server)

    def get_server_status(
        self, server: FlextGrpcEntities.Server
    ) -> FlextResult[dict[str, Any]]:
        """Delegate server status to specialized manager."""
        return self._server_manager.get_server_metrics(server)

    # === DELEGATED CLIENT OPERATIONS ===

    def connect_client(self, target: str) -> FlextResult[FlextGrpcEntities.Client]:
        """Delegate client connection to specialized manager."""
        return self._client_manager.connect(target)

    def disconnect_client(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Delegate client disconnection to specialized manager."""
        return self._client_manager.disconnect(client)

    def make_call(
        self,
        client: FlextGrpcEntities.Client,
        method: str,
        request: FlextGrpcTypes.ConfigValue,
    ) -> FlextResult[dict[str, Any]]:
        """Delegate method calls to specialized manager.

        Args:
        client: Client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        """
        return self._client_manager.make_call(client, method, request)

    def get_client_status(
        self, client: FlextGrpcEntities.Client
    ) -> FlextResult[dict[str, Any]]:
        """Get client status through delegation."""
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""
        is_connected = target and target in self._client_manager._active_channels
        return FlextResult.ok({"connected": is_connected, "target": target})

    # === DELEGATED STREAM OPERATIONS ===

    def create_stream(
        self,
        method_name: str | int | None = "DefaultMethod",
        **kwargs: str | int | bool | None,
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Delegate stream creation to specialized manager."""
        # Ensure method_name is a string
        method_name_str = (
            str(method_name) if method_name is not None else "DefaultMethod"
        )
        kwargs["method_name"] = method_name_str
        return self._stream_manager.create_stream(**kwargs)

    def send_data(
        self, stream: FlextGrpcEntities.GrpcStream, data: FlextGrpcTypes.ConfigValue
    ) -> FlextResult[dict[str, Any]]:
        """Delegate data sending to specialized manager.

        Args:
        stream: Stream entity
        data: Message data (gRPC protocol message - dynamic type)

        """
        return self._stream_manager.send_data(stream, data)

    def close_stream(
        self, stream: FlextGrpcEntities.GrpcStream
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Delegate stream closing to specialized manager."""
        return self._stream_manager.close_stream(stream)

    # === FACTORY METHODS WITH DELEGATION ===

    def _create_client_entity(
        self, target: str, options: dict[str, Any] | None = None
    ) -> FlextResult[FlextGrpcEntities.Client]:
        """Delegate entity creation to utilities.

        Args:
        target: gRPC target address
        options: Channel options (gRPC-specific configuration)

        """
        return FlextGrpcUtilities.create_client_entity(target, options)

    def _create_stream_entity(
        self, method_name: str, stream_type: str
    ) -> FlextResult[FlextGrpcEntities.GrpcStream]:
        """Delegate entity creation to utilities."""
        return FlextGrpcUtilities.create_stream_entity(method_name, stream_type)

    # === LEGACY COMPATIBILITY METHODS ===

    def _execute_server_command(
        self, command: str, server: FlextGrpcEntities.Server
    ) -> FlextResult[dict[str, Any]]:
        """Execute server-specific commands."""
        if command == "start":
            return self.start_server(server).map(lambda _: {"status": "started"})
        if command == "stop":
            return self.stop_server(server).map(lambda _: {"status": "stopped"})
        if command == "status":
            return self.get_server_status(server)
        return FlextResult.fail(f"Unsupported server command: {command}")

    def _execute_client_command(
        self,
        command: str,
        client: FlextGrpcEntities.Client,
        **kwargs: str | int | bool | None,
    ) -> FlextResult[dict[str, Any]]:
        """Execute client-specific commands."""
        if command == "connect":
            return self.connect_client(str(kwargs.get("target", ""))).map(
                lambda _: {"status": "connected"}
            )
        if command == "disconnect":
            return self.disconnect_client(client).map(
                lambda _: {"status": "disconnected"}
            )
        if command == "status":
            return self.get_client_status(client)
        if command == "call":
            return self.make_call(
                client, str(kwargs.get("method", "")), kwargs.get("request")
            )
        return FlextResult.fail(f"Unsupported client command: {command}")

    def _execute_stream_command(
        self,
        command: str,
        stream: FlextGrpcEntities.GrpcStream,
        **kwargs: str | int | bool | None,
    ) -> FlextResult[dict[str, Any]]:
        """Execute stream-specific commands."""
        if command == "create":
            method_name = str(kwargs.get("method_name", "DefaultMethod"))
            return self.create_stream(method_name=method_name, **kwargs).map(
                lambda _: {"status": "created"}
            )
        if command == "send":
            return self.send_data(stream, kwargs.get("data"))
        if command == "close":
            return self.close_stream(stream).map(lambda _: {"status": "closed"})
        return FlextResult.fail(f"Unsupported stream command: {command}")

    def execute_grpc(
        self,
        command: str | None = None,
        entity: FlextGrpcEntities.Server
        | FlextGrpcEntities.Client
        | FlextGrpcEntities.GrpcStream
        | dict[str, Any]
        | None = None,
        *_args: str | int | bool | None,
        **kwargs: str | int | bool | None,
    ) -> FlextResult[dict[str, Any]]:
        """Legacy compatibility method - delegates to appropriate manager."""
        if command is None:
            return FlextResult.ok({
                "status": "ready",
                "service": "flext-grpc-service",
            })

        if entity is None:
            return FlextResult.fail("Entity instance required")

        # Route based on entity type and command
        if isinstance(entity, FlextGrpcEntities.Server):
            return self._execute_server_command(command, entity)
        if isinstance(entity, FlextGrpcEntities.Client):
            return self._execute_client_command(command, entity, **kwargs)
        if isinstance(entity, FlextGrpcEntities.GrpcStream):
            return self._execute_stream_command(command, entity, **kwargs)

        return FlextResult.fail(f"Unsupported entity type: {type(entity)}")

    def execute(self, **_kwargs: object) -> FlextResult[dict[str, Any]]:
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
