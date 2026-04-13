"""FLEXT gRPC Services - Backward-compatible shim.

Delegates to the restructured services/ subpackage.
Tests and consumers that reference FlextGrpcServices continue to work.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import p, r
from flext_grpc import (
    FlextGrpcClient,
    FlextGrpcConnectionPool,
    FlextGrpcMetrics,
    FlextGrpcServer,
    FlextGrpcStream,
    c,
    m,
    t,
    u,
)


class FlextGrpcServices:
    """Backward-compatible service facade delegating to service mixins.

    This class preserves the existing public API while the implementation
    now lives in flext_grpc.services.* mixin classes.
    """

    class Grpc:
        """Nested service implementations — delegates to mixin inner classes."""

        MetricsCollector = FlextGrpcMetrics.MetricsCollector
        ConnectionPool = FlextGrpcConnectionPool.ConnectionPool
        GrpcServerManager = FlextGrpcServer.GrpcServerManager
        GrpcClientManager = FlextGrpcClient.GrpcClientManager
        GrpcStreamManager = FlextGrpcStream.GrpcStreamManager

    def __init__(self) -> None:
        """Initialize service with dependency injection and delegation."""
        super().__init__()
        self._server_manager = FlextGrpcServer.GrpcServerManager()
        self._client_manager = FlextGrpcClient.GrpcClientManager()
        self._stream_manager = FlextGrpcStream.GrpcStreamManager()
        self._metrics_collector = FlextGrpcMetrics.MetricsCollector()
        self._resource_manager = FlextGrpcConnectionPool.ConnectionPool(max_size=20)

    def close_stream(self, stream: m.Grpc.GrpcStream) -> p.Result[m.Grpc.GrpcStream]:
        """Delegate stream closing to specialized manager."""
        return self._stream_manager.close_stream(stream)

    def connect_client(self, target: str) -> p.Result[m.Grpc.Client]:
        """Delegate client connection to specialized manager."""
        return self._client_manager.connect(target)

    def create_stream(
        self,
        method_name: str | int | None = "DefaultMethod",
        **kwargs: t.OptionalContainerValue,
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Delegate stream creation to specialized manager."""
        method_name_str = (
            str(method_name) if method_name is not None else "DefaultMethod"
        )
        kwargs["method_name"] = method_name_str
        return self._stream_manager.create_stream(**kwargs)

    def disconnect_client(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Client]:
        """Delegate client disconnection to specialized manager."""
        return self._client_manager.disconnect(client)

    def execute(self, **_kwargs: t.Scalar) -> p.Result[m.Grpc.Payload]:
        """Execute main service operation."""
        return r[m.Grpc.Payload].ok(
            m.Grpc.Payload.from_values(status="ready", service="flext-grpc-service"),
        )

    def client_status(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Payload]:
        """Get client status through delegation."""
        return self._client_manager.client_status(client)

    def server_status(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Payload]:
        """Delegate server status to specialized manager."""
        return self._server_manager.server_metrics(server)

    def make_call(
        self,
        client: m.Grpc.Client,
        method: str,
        request: t.OptionalContainerValueMapping,
    ) -> p.Result[m.Grpc.Payload]:
        """Delegate method calls to specialized manager.

        Args:
        client: Client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        """
        return self._client_manager.make_call(client, method, request)

    def send_data(
        self,
        stream: m.Grpc.GrpcStream,
        data: t.OptionalContainerValueMapping,
    ) -> p.Result[m.Grpc.Payload]:
        """Delegate data sending to specialized manager.

        Args:
        stream: Stream entity
        data: Message data (gRPC protocol message - dynamic type)

        """
        return self._stream_manager.send_data(stream, data)

    def start_server(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Server]:
        """Delegate server start to specialized manager."""
        return self._server_manager.start_server(server)

    def stop_server(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Server]:
        """Delegate server stop to specialized manager."""
        return self._server_manager.stop_server(server)

    def _create_client_entity(
        self,
        target: str,
        options: t.OptionalContainerValueMapping | None = None,
    ) -> p.Result[m.Grpc.Client]:
        """Delegate entity creation to utilities.

        Args:
        target: gRPC target address
        options: Channel options (gRPC-specific configuration)

        """
        return u.Grpc.create_client_entity(target, options)

    def _create_stream_entity(
        self,
        method_name: str,
        stream_type: c.Grpc.GrpcOperations | str,
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Delegate entity creation to utilities."""
        return u.Grpc.create_stream_entity(method_name, stream_type)

    def _execute_client_command(
        self,
        command: str,
        client: m.Grpc.Client,
        **kwargs: t.OptionalContainerValue,
    ) -> p.Result[m.Grpc.Payload]:
        """Execute client-specific commands."""
        if command == "connect":
            connect_result = self.connect_client(str(kwargs.get("target", "")))
            if connect_result.failure:
                return r[m.Grpc.Payload].fail(
                    connect_result.error or "Client connect command failed",
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="connected"))
        if command == "disconnect":
            disconnect_result = self.disconnect_client(client)
            if disconnect_result.failure:
                return r[m.Grpc.Payload].fail(
                    disconnect_result.error or "Client disconnect command failed",
                )
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(status="disconnected"),
            )
        if command == "status":
            return self.client_status(client)
        if command == "call":
            request = kwargs.get("request")
            if request is None:
                return r[m.Grpc.Payload].fail("Request parameter is required")
            if not isinstance(request, Mapping):
                return r[m.Grpc.Payload].fail("Request parameter must be a mapping")
            return self.make_call(client, str(kwargs.get("method", "")), request)
        return r[m.Grpc.Payload].fail(f"Unsupported client command: {command}")

    def _execute_server_command(
        self,
        command: str,
        server: m.Grpc.Server,
    ) -> p.Result[m.Grpc.Payload]:
        """Execute server-specific commands."""
        if command == "start":
            start_result = self.start_server(server)
            if start_result.failure:
                return r[m.Grpc.Payload].fail(
                    start_result.error or "Server start command failed",
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="started"))
        if command == "stop":
            stop_result = self.stop_server(server)
            if stop_result.failure:
                return r[m.Grpc.Payload].fail(
                    stop_result.error or "Server stop command failed",
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="stopped"))
        if command == "status":
            return self.server_status(server)
        return r[m.Grpc.Payload].fail(f"Unsupported server command: {command}")

    def _execute_stream_command(
        self,
        command: str,
        stream: m.Grpc.GrpcStream,
        **kwargs: t.OptionalContainerValue,
    ) -> p.Result[m.Grpc.Payload]:
        """Execute stream-specific commands."""
        if command == "create":
            method_name = str(kwargs.get("method_name", "DefaultMethod"))
            create_result = self.create_stream(method_name=method_name, **kwargs)
            if create_result.failure:
                return r[m.Grpc.Payload].fail(
                    create_result.error or "Stream create command failed",
                )
            created_stream = create_result.value
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(
                    status="created",
                    stream_id=created_stream.id,
                ),
            )
        if command == "send":
            data = kwargs.get("data")
            if data is None:
                return r[m.Grpc.Payload].fail("Data parameter is required")
            if not isinstance(data, Mapping):
                return r[m.Grpc.Payload].fail("Data parameter must be a mapping")
            return self.send_data(stream, data)
        if command == "close":
            close_result = self.close_stream(stream)
            if close_result.failure:
                return r[m.Grpc.Payload].fail(
                    close_result.error or "Stream close command failed",
                )
            return r[m.Grpc.Payload].ok(m.Grpc.Payload.from_values(status="closed"))
        return r[m.Grpc.Payload].fail(f"Unsupported stream command: {command}")


__all__: list[str] = [
    "FlextGrpcServices",
]
