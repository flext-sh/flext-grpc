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
from typing import override

import grpc
from flext_core import r
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from flext_grpc import (
    EchoRequest,
    FlextGrpcModels as FlextGrpcEntities,
    FlextGrpcServiceServicer,
    FlextGrpcServiceStub,
    FlextGrpcUtilities,
    HealthRequest,
    add_FlextGrpcServiceServicer_to_server,
    c,
    t,
)


def create_real_servicer(_server_key: str) -> FlextGrpcServiceServicer:
    """Create runtime gRPC servicer instance for server registration."""
    return FlextGrpcServiceServicer()


class ServicePayload(BaseModel):
    """Structured payload model replacing ad-hoc dict responses."""

    values: t.Grpc.GrpcDict = Field(default_factory=dict)

    @classmethod
    def from_values(cls, **values: t.GeneralValueType) -> ServicePayload:
        """Build payload from keyword values."""
        return cls(values=dict(values))  # type: dict[str, t.GeneralValueType]


class _MetricValueModel(BaseModel):
    """Normalize metric values to JSON-compatible types."""

    value: t.JsonValue = None

    @field_validator("value", mode="before")
    @classmethod
    def normalize_value(cls, value: t.GeneralValueType) -> t.JsonValue:
        """Normalize runtime values to stable JSON-compatible output."""
        match value:
            case None | str() | int() | float() | bool():
                return value
            case list() as values:
                return [
                    _MetricValueModel.model_validate({"value": item}).value
                    for item in values
                ]
            case tuple() as values:
                return [
                    _MetricValueModel.model_validate({"value": item}).value
                    for item in values
                ]
            case _:
                return str(value)


def _new_stream_buffer() -> deque[t.ConfigValue]:
    """Create bounded stream buffer with explicit typing."""
    return deque(maxlen=500)


class _StreamRuntimeState(BaseModel):
    """Typed runtime state for stream buffers."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    stream: FlextGrpcEntities.GrpcStream
    created_at: float
    buffer: deque[t.ConfigValue] = Field(default_factory=_new_stream_buffer)
    active: bool = True


class _ServerEntityEnvelope(BaseModel):
    """Pydantic envelope for server entities."""

    entity: FlextGrpcEntities.Server


class _ClientEntityEnvelope(BaseModel):
    """Pydantic envelope for client entities."""

    entity: FlextGrpcEntities.Client


class _StreamEntityEnvelope(BaseModel):
    """Pydantic envelope for stream entities."""

    entity: FlextGrpcEntities.GrpcStream


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
        **kwargs: t.ConfigValue,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Create stream."""

    @abstractmethod
    def send_data(
        self,
        stream: FlextGrpcEntities.GrpcStream,
        data: t.ConfigValue,
    ) -> r[ServicePayload]:
        """Send data through stream.

        Note: Uses t.ConfigValue for gRPC message compatibility
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
        self._metrics = ServicePayload()
        self._lock = threading.RLock()

    def record_metric(self, key: str, value: t.GeneralValueType) -> None:
        """Thread-safe metric recording.

        Args:
        key: Metric identifier
        value: Metric value (JSON-serializable: str, int, float, bool, list, dict, None)

        """
        with self._lock:
            normalized = _MetricValueModel.model_validate({"value": value})
            self._metrics.values[key] = normalized.value

    def get_metric(self, key: str) -> t.JsonValue:
        """Thread-safe metric retrieval.

        Returns:
        Metric value or None if not found

        """
        with self._lock:
            return self._metrics.values.get(key)

    def get_all_metrics(self) -> ServicePayload:
        """Get all metrics snapshot."""
        with self._lock:
            return ServicePayload(values=self._metrics.values.copy())


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
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Connection acquisition failed: {e}")

    def release(self, connection: t.GeneralValueType) -> r[bool]:
        """Release connection back to pool."""
        try:
            with self._lock:
                if connection in self._active:
                    self._active.remove(connection)
                    if self._pool.full():
                        return r.ok(True)
                    self._pool.put_nowait(connection)
                return r.ok(True)
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Connection release failed: {e}")

    def cleanup(self) -> r[bool]:
        """Cleanup all connections."""
        with self._lock:
            self._active.clear()
            while not self._pool.empty():
                try:
                    _ = self._pool.get_nowait()
                except (grpc.RpcError, ConnectionError, TimeoutError):
                    break
        return r.ok(True)


class GrpcServerManager(ServerLifecycleManager):
    """Dedicated server lifecycle management."""

    def __init__(self) -> None:
        """Initialize server manager with metrics tracking."""
        super().__init__()
        self._active_servers = {}
        self._metrics = MetricsCollector()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=50,
            thread_name_prefix="flext-grpc-server",
        )

    @override
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
            _ = grpc_server.add_insecure_port(
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

        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Server start failed: {e}")

    @override
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
            _ = grpc_server.stop(grace=2.0)

            # Cleanup
            del self._active_servers[server_key]
            self._metrics.record_metric(f"{server_key}_stopped_at", time.time())

            return stopping_server.mark_stopped()

        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Server stop failed: {e}")

    def get_server_metrics(
        self,
        server: FlextGrpcEntities.Server,
    ) -> r[ServicePayload]:
        """Get server metrics."""
        server_key = f"{server.host}:{server.port}"
        started_at = self._metrics.get_metric(f"{server_key}_started_at")
        stopped_at = self._metrics.get_metric(f"{server_key}_stopped_at")
        return r.ok(
            ServicePayload.from_values(
                is_active=server_key in self._active_servers,
                started_at=started_at,
                stopped_at=stopped_at,
            ),
        )


class GrpcClientManager(ClientConnectionManager):
    """Dedicated client connection management."""

    def __init__(self) -> None:
        """Initialize client manager with connection pooling."""
        super().__init__()
        self._active_channels = {}
        self._connection_pool = ConnectionPool(max_size=20)
        self._metrics = MetricsCollector()

    @override
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

        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Connection failed: {e}")

    @override
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
            grpc_channel.close()
            del self._active_channels[target]

        return r.ok(client)

    def make_call(
        self,
        client: FlextGrpcEntities.Client,
        method: str,
        request: t.ConfigValue,
    ) -> r[ServicePayload]:
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
            grpc_channel = self._active_channels[target]
            stub = FlextGrpcServiceStub(grpc_channel)

            # Route to appropriate method
            if method == "Echo":
                echo_response = stub.Echo(
                    EchoRequest(message=str(request), metadata={}),
                )
                return r.ok(
                    ServicePayload.from_values(
                        method="Echo",
                        message=echo_response.message,
                        server_id=echo_response.server_id,
                        timestamp=echo_response.timestamp,
                    ),
                )
            if method == "HealthCheck":
                health_response = stub.HealthCheck(
                    HealthRequest(service="FlextGrpcService"),
                )
                return r.ok(
                    ServicePayload.from_values(
                        method="HealthCheck",
                        status=health_response.status,
                        message=health_response.message,
                    ),
                )

            return r.fail(f"Unsupported method: {method}")

        except grpc.RpcError as e:
            code_fn = e.code if hasattr(e, "code") else lambda: None
            details_fn = e.details if hasattr(e, "details") else lambda: ""
            code_val = code_fn() if callable(code_fn) else None
            details_val = details_fn() if callable(details_fn) else str(e)
            return r.fail(f"gRPC call failed: {code_val} - {details_val}")
        except (ConnectionError, TimeoutError) as e:
            return r.fail(f"Call execution failed: {e}")


class GrpcStreamManager(StreamProcessor):
    """Dedicated stream processing with buffering."""

    def __init__(self) -> None:
        """Initialize stream manager with metrics tracking."""
        super().__init__()
        self._active_streams = {}
        self._metrics = MetricsCollector()

    @override
    def create_stream(
        self,
        **kwargs: t.ConfigValue,
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
        self._active_streams[stream_key] = _StreamRuntimeState(
            stream=stream,
            created_at=time.time(),
        )

        self._metrics.record_metric(f"{stream_key}_created", time.time())
        return r.ok(stream)

    @override
    def send_data(
        self,
        stream: FlextGrpcEntities.GrpcStream,
        data: t.ConfigValue,
    ) -> r[ServicePayload]:
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
            stream_state = _StreamRuntimeState.model_validate(stream_info)
            stream_state.buffer.append(data)
            self._active_streams[stream_key] = stream_state

            return r.ok(
                ServicePayload.from_values(
                    stream_id=stream.id,
                    data_sent=str(data),
                    buffer_size=len(stream_state.buffer),
                ),
            )

        except ValidationError as e:
            return r.fail(f"Invalid stream state: {e}")

        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r.fail(f"Data send failed: {e}")

    @override
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
    ) -> r[ServicePayload]:
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
    ) -> r[ServicePayload]:
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
    ) -> r[ServicePayload]:
        """Get client status through delegation."""
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""
        is_connected = bool(target and target in self._client_manager._active_channels)
        return r.ok(ServicePayload.from_values(connected=is_connected, target=target))

    # === DELEGATED STREAM OPERATIONS ===

    def create_stream(
        self,
        method_name: str | int | None = "DefaultMethod",
        **kwargs: t.ConfigValue,
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
    ) -> r[ServicePayload]:
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
        stream_type: c.Grpc.StreamTypeLiteral | str,
    ) -> r[FlextGrpcEntities.GrpcStream]:
        """Delegate entity creation to utilities."""
        return FlextGrpcUtilities.create_stream_entity(method_name, stream_type)

    def _execute_server_command(
        self,
        command: str,
        server: FlextGrpcEntities.Server,
    ) -> r[ServicePayload]:
        """Execute server-specific commands."""
        if command == "start":
            start_result = self.start_server(server)
            if start_result.is_failure:
                return r.fail(start_result.error or "Server start command failed")
            return r.ok(ServicePayload.from_values(status="started"))
        if command == "stop":
            stop_result = self.stop_server(server)
            if stop_result.is_failure:
                return r.fail(stop_result.error or "Server stop command failed")
            return r.ok(ServicePayload.from_values(status="stopped"))
        if command == "status":
            return self.get_server_status(server)
        return r.fail(f"Unsupported server command: {command}")

    def _execute_client_command(
        self,
        command: str,
        client: FlextGrpcEntities.Client,
        **kwargs: t.ConfigValue,
    ) -> r[ServicePayload]:
        """Execute client-specific commands."""
        if command == "connect":
            connect_result = self.connect_client(str(kwargs.get("target", "")))
            if connect_result.is_failure:
                return r.fail(connect_result.error or "Client connect command failed")
            return r.ok(ServicePayload.from_values(status="connected"))
        if command == "disconnect":
            disconnect_result = self.disconnect_client(client)
            if disconnect_result.is_failure:
                return r.fail(
                    disconnect_result.error or "Client disconnect command failed"
                )
            return r.ok(ServicePayload.from_values(status="disconnected"))
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
        **kwargs: t.ConfigValue,
    ) -> r[ServicePayload]:
        """Execute stream-specific commands."""
        if command == "create":
            method_name = str(kwargs.get("method_name", "DefaultMethod"))
            create_result = self.create_stream(method_name=method_name, **kwargs)
            if create_result.is_failure:
                return r.fail(create_result.error or "Stream create command failed")
            return r.ok(ServicePayload.from_values(status="created"))
        if command == "send":
            return self.send_data(stream, kwargs.get("data"))
        if command == "close":
            close_result = self.close_stream(stream)
            if close_result.is_failure:
                return r.fail(close_result.error or "Stream close command failed")
            return r.ok(ServicePayload.from_values(status="closed"))
        return r.fail(f"Unsupported stream command: {command}")

    def execute(self, **_kwargs: t.GeneralValueType) -> r[ServicePayload]:
        """Execute main service operation."""
        return r.ok(
            ServicePayload.from_values(status="ready", service="flext-grpc-service")
        )


__all__ = [
    "ConnectionPool",
    "FlextGrpcServices",
    "GrpcClientManager",
    "GrpcServerManager",
    "GrpcStreamManager",
    "MetricsCollector",
    "ServicePayload",
]
