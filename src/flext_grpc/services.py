"""FLEXT gRPC Services - SOLID Service Architecture with Delegation.

Generic service classes using SOLID principles, delegation, and patterns.
Each class has single responsibility with clear separation of concerns.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import threading
import time
from collections import deque
from collections.abc import MutableMapping
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
from typing import Annotated

import grpc
from flext_core import r
from pydantic import Field, ValidationError

from flext_grpc import (
    ClientConnection,
    EchoRequest,
    FlextGrpcServiceServicer,
    FlextGrpcServiceStub,
    HealthRequest,
    ServerLifecycle,
    StreamProcessor,
    add_FlextGrpcServiceServicer_to_server,
    c,
    m,
    t,
    u,
)


def _new_stream_buffer() -> deque[t.ConfigValue]:
    return deque(maxlen=500)


class _MetricValueModel(m.Value):
    value: t.ConfigValue


class _StreamRuntimeState(m.Value):
    stream: m.Grpc.GrpcStream
    created_at: float
    buffer: Annotated[deque[t.ConfigValue], Field(default_factory=_new_stream_buffer)]


def create_real_servicer(_server_key: str) -> FlextGrpcServiceServicer:
    """Create runtime gRPC servicer instance for server registration."""
    return FlextGrpcServiceServicer()


class MetricsCollector:
    """Dedicated metrics collection with thread safety."""

    def __init__(self) -> None:
        """Initialize metrics collector with thread-safe storage."""
        super().__init__()
        self._metrics = m.Grpc.Payload(values={})
        self._lock = threading.RLock()

    def get_all_metrics(self) -> m.Grpc.Payload:
        """Get all metrics snapshot."""
        with self._lock:
            return m.Grpc.Payload(values=self._metrics.values.copy())

    def get_metric(self, key: str) -> t.ConfigValue | None:
        """Thread-safe metric retrieval.

        Returns:
        Metric value or None if not found

        """
        with self._lock:
            return self._metrics.values.get(key)

    def record_metric(self, key: str, value: t.ConfigValue) -> None:
        """Thread-safe metric recording.

        Args:
        key: Metric identifier
        value: Metric value (JSON-serializable: str, int, float, bool, list, dict, None)

        """

        def _normalize_value(val: t.ConfigValue) -> t.ConfigValue:
            if val is None:
                return ""
            if u.is_primitive(val):
                return val
            return str(val)

        with self._lock:
            normalized = _MetricValueModel(value=value)
            json_val = _normalize_value(normalized.value)
            self._metrics.values[key] = json_val


class ConnectionPool:
    """Generic connection pool with resource management."""

    def __init__(self, max_size: int = 10) -> None:
        """Initialize connection pool.

        Args:
        max_size: Maximum pool size

        """
        super().__init__()
        self._pool: Queue[grpc.Channel] = Queue(maxsize=max_size)
        self._active: set[grpc.Channel] = set()
        self._lock = threading.RLock()

    def acquire(self) -> r[grpc.Channel]:
        """Acquire connection from pool."""
        try:
            with self._lock:
                if not self._pool.empty():
                    conn = self._pool.get_nowait()
                    self._active.add(conn)
                    return r[grpc.Channel].ok(conn)
                return r[grpc.Channel].fail("No available connections")
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r[grpc.Channel].fail(f"Connection acquisition failed: {e}")

    def cleanup(self) -> r[bool]:
        """Cleanup all connections."""
        with self._lock:
            self._active.clear()
            while not self._pool.empty():
                try:
                    _ = self._pool.get_nowait()
                except (grpc.RpcError, ConnectionError, TimeoutError):
                    break
        return r[bool].ok(True)

    def release(self, connection: grpc.Channel) -> r[bool]:
        """Release connection back to pool."""

        def _release() -> bool:
            with self._lock:
                if connection in self._active:
                    self._active.remove(connection)
                    if self._pool.full():
                        return True
                    self._pool.put_nowait(connection)
                return True

        return u.try_(
            _release,
            catch=(grpc.RpcError, ConnectionError, TimeoutError),
        ).map_error(lambda e: f"Connection release failed: {e}")


class GrpcServerManager(ServerLifecycle):
    """Dedicated server lifecycle management."""

    def __init__(self) -> None:
        """Initialize server manager with metrics tracking."""
        super().__init__()
        self._active_servers: MutableMapping[str, grpc.Server] = {}
        self._metrics = MetricsCollector()
        self._thread_pool = ThreadPoolExecutor(
            max_workers=50, thread_name_prefix="flext-grpc-server"
        )

    def get_server_metrics(self, server: m.Grpc.Server) -> r[m.Grpc.Payload]:
        """Get server metrics."""
        server_key = f"{server.host}:{server.port}"
        started_at_raw = self._metrics.get_metric(f"{server_key}_started_at")
        stopped_at_raw = self._metrics.get_metric(f"{server_key}_stopped_at")
        started_at_str: str = str(started_at_raw) if started_at_raw is not None else ""
        stopped_at_str: str = str(stopped_at_raw) if stopped_at_raw is not None else ""
        return r[m.Grpc.Payload].ok(
            m.Grpc.Payload.from_values(
                is_active=server_key in self._active_servers,
                started_at=started_at_str,
                stopped_at=stopped_at_str,
            )
        )

    def start_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Start gRPC server with proper lifecycle."""
        server_key = f"{server.host}:{server.port}"
        if server_key in self._active_servers:
            return r[m.Grpc.Server].fail(f"Server already running: {server_key}")
        try:
            starting_result = server.start()
            if starting_result.is_failure:
                return starting_result
            starting_server = starting_result.value
            grpc_server = grpc.server(self._thread_pool)
            _ = grpc_server.add_insecure_port(
                f"{starting_server.host}:{starting_server.port}"
            )
            for _service in starting_server.services:
                real_servicer = create_real_servicer(server_key)
                add_FlextGrpcServiceServicer_to_server(real_servicer, grpc_server)
            grpc_server.start()
            self._active_servers[server_key] = grpc_server
            self._metrics.record_metric(f"{server_key}_started_at", time.time())
            return starting_server.mark_running()
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r[m.Grpc.Server].fail(f"Server start failed: {e}")

    def stop_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Stop gRPC server gracefully."""
        server_key = f"{server.host}:{server.port}"
        if server_key not in self._active_servers:
            return r[m.Grpc.Server].fail(f"No active server: {server_key}")
        try:
            stopping_result = server.stop()
            if stopping_result.is_failure:
                return stopping_result
            stopping_server = stopping_result.value
            grpc_server = self._active_servers[server_key]
            _ = grpc_server.stop(grace=2.0)
            del self._active_servers[server_key]
            self._metrics.record_metric(f"{server_key}_stopped_at", time.time())
            return stopping_server.mark_stopped()
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r[m.Grpc.Server].fail(f"Server stop failed: {e}")


class GrpcClientManager(ClientConnection):
    """Dedicated client connection management."""

    def __init__(self) -> None:
        """Initialize client manager with connection pooling."""
        super().__init__()
        self._active_channels: MutableMapping[str, grpc.Channel] = {}
        self._connection_pool = ConnectionPool(max_size=20)
        self._metrics = MetricsCollector()

    def connect(self, target: str) -> r[m.Grpc.Client]:
        """Establish client connection with pooling."""
        if target in self._active_channels:
            return u.create_client_entity(target=target)

        def _connect() -> m.Grpc.Client:
            try:
                grpc_channel: grpc.Channel = grpc.insecure_channel(target)
                grpc.channel_ready_future(grpc_channel).result(timeout=5.0)
            except (grpc.RpcError, grpc.FutureTimeoutError) as exc:
                raise RuntimeError(str(exc)) from exc
            self._active_channels[target] = grpc_channel
            self._metrics.record_metric(f"{target}_connected_at", time.time())
            client_result = u.create_client_entity(target=target)
            if client_result.is_failure:
                raise RuntimeError(client_result.error or "Connection failed")
            return client_result.value

        return u.try_(
            _connect,
            catch=(
                ConnectionError,
                TimeoutError,
                RuntimeError,
            ),
        ).map_error(lambda e: f"Connection failed: {e}")

    def disconnect(self, client: m.Grpc.Client) -> r[m.Grpc.Client]:
        """Disconnect client and cleanup resources."""
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""
        if target and target in self._active_channels:
            grpc_channel = self._active_channels[target]
            grpc_channel.close()
            del self._active_channels[target]
        return r[m.Grpc.Client].ok(client)

    def get_client_status(self, client: m.Grpc.Client) -> r[m.Grpc.Payload]:
        """Get client connection status."""
        target = ""
        if client.channel is not None:
            target = client.channel.target or ""
        is_connected = bool(target and target in self._active_channels)
        return r[m.Grpc.Payload].ok(
            m.Grpc.Payload.from_values(connected=is_connected, target=target)
        )

    def make_call(
        self, client: m.Grpc.Client, method: str, request: t.ConfigValue
    ) -> r[m.Grpc.Payload]:
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
            return r[m.Grpc.Payload].fail("Client not connected")
        try:
            grpc_channel = self._active_channels[target]
            stub = FlextGrpcServiceStub(grpc_channel)
            if method == "Echo":
                echo_response = stub.Echo(EchoRequest(message=str(request)))
                return r[m.Grpc.Payload].ok(
                    m.Grpc.Payload.from_values(
                        method="Echo",
                        message=echo_response.message,
                        server_id=echo_response.server_id,
                        timestamp=echo_response.timestamp,
                    )
                )
            if method == "HealthCheck":
                health_response = stub.HealthCheck(
                    HealthRequest(service="FlextGrpcService")
                )
                return r[m.Grpc.Payload].ok(
                    m.Grpc.Payload.from_values(
                        method="HealthCheck",
                        status=health_response.status,
                        message=health_response.message,
                    )
                )
            return r[m.Grpc.Payload].fail(f"Unsupported method: {method}")
        except grpc.RpcError as e:
            code_val = e.code() if hasattr(e, "code") else None
            details_val = e.details() if hasattr(e, "details") else str(e)
            return r[m.Grpc.Payload].fail(
                f"gRPC call failed: {code_val} - {details_val}"
            )
        except (ConnectionError, TimeoutError) as e:
            return r[m.Grpc.Payload].fail(f"Call execution failed: {e}")


class GrpcStreamManager(StreamProcessor):
    """Dedicated stream processing with buffering."""

    def __init__(self) -> None:
        """Initialize stream manager with metrics tracking."""
        super().__init__()
        self._active_streams: MutableMapping[str, _StreamRuntimeState] = {}
        self._metrics = MetricsCollector()

    def close_stream(self, stream: m.Grpc.GrpcStream) -> r[m.Grpc.GrpcStream]:
        """Close stream and cleanup."""
        stream_key = f"{stream.id}_{stream.stream_type}"
        if stream_key in self._active_streams:
            del self._active_streams[stream_key]
        return r[m.Grpc.GrpcStream].ok(stream)

    def create_stream(self, **kwargs: t.ConfigValue) -> r[m.Grpc.GrpcStream]:
        """Create stream with proper setup."""
        method_name = str(kwargs.get("method_name", "DefaultMethod"))
        stream_type = str(kwargs.get("stream_type", "unary"))
        stream_result = u.create_stream_entity(method_name, stream_type)
        if stream_result.is_failure:
            return stream_result
        stream = stream_result.value
        stream_key = f"{stream.id}_{stream.stream_type}"
        self._active_streams[stream_key] = _StreamRuntimeState(
            stream=stream,
            created_at=time.time(),
            buffer=_new_stream_buffer(),
        )
        self._metrics.record_metric(f"{stream_key}_created", time.time())
        return r[m.Grpc.GrpcStream].ok(stream)

    def send_data(
        self, stream: m.Grpc.GrpcStream, data: t.ConfigValue
    ) -> r[m.Grpc.Payload]:
        """Send data with buffering strategy.

        Args:
        stream: Stream entity
        data: Message data (gRPC protocol message - dynamic type)

        """
        stream_key = f"{stream.id}_{stream.stream_type}"
        if stream_key not in self._active_streams:
            return r[m.Grpc.Payload].fail("Stream not found")
        stream_info = self._active_streams[stream_key]
        try:
            stream_state = _StreamRuntimeState.model_validate(stream_info)
            stream_state.buffer.append(data)
            self._active_streams[stream_key] = stream_state
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(
                    stream_id=stream.id,
                    data_sent=str(data),
                    buffer_size=len(stream_state.buffer),
                )
            )
        except ValidationError as e:
            return r[m.Grpc.Payload].fail(f"Invalid stream state: {e}")
        except (grpc.RpcError, ConnectionError, TimeoutError) as e:
            return r[m.Grpc.Payload].fail(f"Data send failed: {e}")


class FlextGrpcServices:
    """Generic gRPC service facade using SOLID principles and delegation.

    Delegates responsibilities to specialized managers while maintaining clean API.
    Uses composition over inheritance and dependency injection.
    """

    def __init__(self) -> None:
        """Initialize service with dependency injection and delegation."""
        super().__init__()
        self._server_manager = GrpcServerManager()
        self._client_manager = GrpcClientManager()
        self._stream_manager = GrpcStreamManager()
        self._metrics_collector = MetricsCollector()
        self._resource_manager = ConnectionPool(max_size=20)

    def close_stream(self, stream: m.Grpc.GrpcStream) -> r[m.Grpc.GrpcStream]:
        """Delegate stream closing to specialized manager."""
        return self._stream_manager.close_stream(stream)

    def connect_client(self, target: str) -> r[m.Grpc.Client]:
        """Delegate client connection to specialized manager."""
        return self._client_manager.connect(target)

    def create_stream(
        self, method_name: str | int | None = "DefaultMethod", **kwargs: t.ConfigValue
    ) -> r[m.Grpc.GrpcStream]:
        """Delegate stream creation to specialized manager."""
        method_name_str = (
            str(method_name) if method_name is not None else "DefaultMethod"
        )
        kwargs["method_name"] = method_name_str
        return self._stream_manager.create_stream(**kwargs)

    def disconnect_client(self, client: m.Grpc.Client) -> r[m.Grpc.Client]:
        """Delegate client disconnection to specialized manager."""
        return self._client_manager.disconnect(client)

    def execute(self, **_kwargs: t.Scalar) -> r[m.Grpc.Payload]:
        """Execute main service operation."""
        return r[m.Grpc.Payload].ok(
            m.Grpc.Payload.from_values(status="ready", service="flext-grpc-service")
        )

    def get_client_status(self, client: m.Grpc.Client) -> r[m.Grpc.Payload]:
        """Get client status through delegation."""
        return self._client_manager.get_client_status(client)

    def get_server_status(self, server: m.Grpc.Server) -> r[m.Grpc.Payload]:
        """Delegate server status to specialized manager."""
        return self._server_manager.get_server_metrics(server)

    def make_call(
        self, client: m.Grpc.Client, method: str, request: t.ConfigValue
    ) -> r[m.Grpc.Payload]:
        """Delegate method calls to specialized manager.

        Args:
        client: Client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        """
        return self._client_manager.make_call(client, method, request)

    def send_data(
        self, stream: m.Grpc.GrpcStream, data: t.ConfigValue
    ) -> r[m.Grpc.Payload]:
        """Delegate data sending to specialized manager.

        Args:
        stream: Stream entity
        data: Message data (gRPC protocol message - dynamic type)

        """
        return self._stream_manager.send_data(stream, data)

    def start_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Delegate server start to specialized manager."""
        return self._server_manager.start_server(server)

    def stop_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Delegate server stop to specialized manager."""
        return self._server_manager.stop_server(server)

    def _create_client_entity(
        self, target: str, options: t.GrpcOptions | None = None
    ) -> r[m.Grpc.Client]:
        """Delegate entity creation to utilities.

        Args:
        target: gRPC target address
        options: Channel options (gRPC-specific configuration)

        """
        return u.create_client_entity(target, options)

    def _create_stream_entity(
        self, method_name: str, stream_type: c.Grpc.StreamTypeLiteral | str
    ) -> r[m.Grpc.GrpcStream]:
        """Delegate entity creation to utilities."""
        return u.create_stream_entity(method_name, stream_type)

    def _execute_client_command(
        self, command: str, client: m.Grpc.Client, **kwargs: t.ConfigValue
    ) -> r[m.Grpc.Payload]:
        """Execute client-specific commands."""
        if command == "connect":
            connect_result = self.connect_client(str(kwargs.get("target", "")))
            if connect_result.is_failure:
                return r[m.Grpc.Payload].fail(
                    connect_result.error or "Client connect command failed"
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="connected"))
        if command == "disconnect":
            disconnect_result = self.disconnect_client(client)
            if disconnect_result.is_failure:
                return r[m.Grpc.Payload].fail(
                    disconnect_result.error or "Client disconnect command failed"
                )
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(status="disconnected")
            )
        if command == "status":
            return self.get_client_status(client)
        if command == "call":
            request = kwargs.get("request")
            if request is None:
                return r[m.Grpc.Payload].fail("Request parameter is required")
            return self.make_call(client, str(kwargs.get("method", "")), request)
        return r[m.Grpc.Payload].fail(f"Unsupported client command: {command}")

    def _execute_server_command(
        self, command: str, server: m.Grpc.Server
    ) -> r[m.Grpc.Payload]:
        """Execute server-specific commands."""
        if command == "start":
            start_result = self.start_server(server)
            if start_result.is_failure:
                return r[m.Grpc.Payload].fail(
                    start_result.error or "Server start command failed"
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="started"))
        if command == "stop":
            stop_result = self.stop_server(server)
            if stop_result.is_failure:
                return r[m.Grpc.Payload].fail(
                    stop_result.error or "Server stop command failed"
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="stopped"))
        if command == "status":
            return self.get_server_status(server)
        return r[m.Grpc.Payload].fail(f"Unsupported server command: {command}")

    def _execute_stream_command(
        self,
        command: str,
        stream: m.Grpc.GrpcStream,
        **kwargs: t.ConfigValue,
    ) -> r[m.Grpc.Payload]:
        """Execute stream-specific commands."""
        if command == "create":
            method_name = str(kwargs.get("method_name", "DefaultMethod"))
            create_result = self.create_stream(method_name=method_name, **kwargs)
            if create_result.is_failure:
                return r[m.Grpc.Payload].fail(
                    create_result.error or "Stream create command failed"
                )
            created_stream = create_result.value
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(
                    status="created", stream_id=created_stream.id
                )
            )
        if command == "send":
            data = kwargs.get("data")
            if data is None:
                return r[m.Grpc.Payload].fail("Data parameter is required")
            return self.send_data(stream, data)
        if command == "close":
            close_result = self.close_stream(stream)
            if close_result.is_failure:
                return r[m.Grpc.Payload].fail(
                    close_result.error or "Stream close command failed"
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="closed"))
        return r[m.Grpc.Payload].fail(f"Unsupported stream command: {command}")


ServicePayload = m.Grpc.Payload
"""Type alias for gRPC service payload (structured dict response)."""

__all__ = [
    "ClientConnection",
    "ConnectionPool",
    "FlextGrpcServices",
    "GrpcClientManager",
    "GrpcServerManager",
    "GrpcStreamManager",
    "MetricsCollector",
    "ServerLifecycle",
    "ServicePayload",
    "StreamProcessor",
]
