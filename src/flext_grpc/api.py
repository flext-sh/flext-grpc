"""FLEXT gRPC - Generic Unified Facade with Patterns.

Generic facade using extensive Pydantic models, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import r
from pydantic import BaseModel

from flext_grpc import (
    FlextGrpcClient,
    FlextGrpcConnectionPool,
    FlextGrpcMetrics,
    FlextGrpcServer,
    FlextGrpcSettings,
    FlextGrpcStream,
    c,
    m,
    t,
    u,
)


class FlextGrpc(
    FlextGrpcMetrics,
    FlextGrpcConnectionPool,
    FlextGrpcServer,
    FlextGrpcClient,
    FlextGrpcStream,
):
    """Generic unified gRPC facade with SOLID patterns and minimal code.

    Uses MRO composition from service mixins, functional composition,
    Pydantic v2 models, and delegation to reduce bloat while maintaining
    full functionality with Python 3.13+ features.
    """

    def __init__(self, config: FlextGrpcSettings | None = None) -> None:
        """Initialize facade with FLEXT ecosystem integration."""
        super().__init__()
        self._grpc_config = (
            config if config is not None else FlextGrpcSettings.model_validate({})
        )
        self._server_manager = FlextGrpcServer.GrpcServerManager()
        self._client_manager = FlextGrpcClient.GrpcClientManager()
        self._stream_manager = FlextGrpcStream.GrpcStreamManager()
        self._metrics_collector = FlextGrpcMetrics.MetricsCollector()
        self._resource_manager = FlextGrpcConnectionPool.ConnectionPool(max_size=20)

    @property
    def grpc_config(self) -> FlextGrpcSettings:
        """Get gRPC-specific configuration."""
        return self._grpc_config

    def close_stream(self, stream: m.Grpc.GrpcStream) -> r[m.Grpc.GrpcStream]:
        """Delegate stream closing.

        Args:
        stream: gRPC stream entity to close

        Returns:
        Closed stream entity

        """
        return self._stream_manager.close_stream(stream)

    def connect_client(self, target: str) -> r[m.Grpc.Client]:
        """Delegate client connection.

        Args:
        target: Target address to connect to

        Returns:
        Connected client entity

        """
        return self._client_manager.connect(target)

    def create_channel(
        self,
        target: str,
        options: t.OptionalContainerValueMapping | None = None,
    ) -> r[m.Grpc.Channel]:
        """Create typed channel entity from validated inputs."""
        return u.Grpc.create_channel_entity(
            target=target,
            options={} if options is None else options,
        )

    def create_client(
        self,
        target: str,
        options: t.OptionalContainerValueMapping | None = None,
    ) -> r[m.Grpc.Client]:
        """Create typed client entity from validated inputs."""
        return u.Grpc.create_client_entity(target=target, options=options)

    def create_complete_setup(
        self,
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        service_name: str = "DefaultService",
        methods: t.StrSequence | None = None,
    ) -> r[FlextGrpc.CompleteSetup]:
        """Complete setup using functional composition."""
        resolved_methods = ["HealthCheck"] if methods is None else methods
        target = f"{host}:{port}"

        server_result = self.create_server(host=host, port=port)
        if server_result.is_failure:
            return r[FlextGrpc.CompleteSetup].fail(
                server_result.error or "Server creation failed"
            )

        client_result = self.create_client(target=target)
        if client_result.is_failure:
            return r[FlextGrpc.CompleteSetup].fail(
                client_result.error or "Client creation failed"
            )

        service_result = self.create_service(
            name=service_name, methods=resolved_methods
        )
        if service_result.is_failure:
            return r[FlextGrpc.CompleteSetup].fail(
                service_result.error or "Service creation failed"
            )

        return r[FlextGrpc.CompleteSetup].ok(
            FlextGrpc.CompleteSetup(
                server=server_result.value,
                client=client_result.value,
                service=service_result.value,
                target=target,
            ),
        )

    def create_server(
        self,
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.Service.DEFAULT_MAX_WORKERS,
    ) -> r[m.Grpc.Server]:
        """Create typed server entity from validated inputs."""
        return u.Grpc.create_server_entity(
            host=host,
            port=port,
            max_workers=max_workers,
        )

    def create_service(
        self,
        name: str,
        methods: t.StrSequence | None = None,
    ) -> r[m.Grpc.Service]:
        """Create typed service entity from validated inputs."""
        return u.Grpc.create_service_entity(
            name=name,
            methods=[] if methods is None else methods,
        )

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
    ) -> r[m.Grpc.GrpcStream]:
        """Create typed stream entity from validated inputs."""
        if not method_name.strip():
            return r[m.Grpc.GrpcStream].fail("Stream method name cannot be empty")
        if stream_type not in c.Grpc.STREAM_TYPES:
            return r[m.Grpc.GrpcStream].fail(f"Invalid stream type: {stream_type}")
        return u.Grpc.create_stream_entity(
            method_name=method_name,
            stream_type=stream_type,
        )

    def disconnect_client(self, client: m.Grpc.Client) -> r[m.Grpc.Client]:
        """Delegate client disconnection.

        Args:
        client: gRPC client entity to disconnect

        Returns:
        Disconnected client entity

        """
        return self._client_manager.disconnect(client)

    def execute(self) -> r[FlextGrpcSettings]:
        """Execute main facade operation."""
        return r[FlextGrpcSettings].ok(self.grpc_config)

    def execute_operation(
        self,
        request: m.Grpc.OperationExecutionRequest,
    ) -> r[FlextGrpcSettings]:
        """Execute operation with validation, timeout, retry, and monitoring (Service protocol)."""
        kwargs = request.keyword_arguments
        match request.operation_name:
            case "connect_client":
                target = kwargs.get("target")
                if not isinstance(target, str):
                    return r[FlextGrpcSettings].fail(
                        "connect_client requires string target",
                    )
                result = self._client_manager.connect(target)
            case _:
                return r[FlextGrpcSettings].fail(
                    f"Unknown operation: {request.operation_name}",
                )
        if result.is_failure:
            return r[FlextGrpcSettings].fail(result.error or "Unknown error")
        return r[FlextGrpcSettings].ok(self.grpc_config)

    def get_client_status(self, client: m.Grpc.Client) -> r[m.Grpc.Payload]:
        """Get client status through delegation."""
        return self._client_manager.get_client_status(client)

    def get_server_status(self, server: m.Grpc.Server) -> r[m.Grpc.Payload]:
        """Delegate server status to specialized manager."""
        return self._server_manager.get_server_metrics(server)

    def make_call(
        self,
        client: m.Grpc.Client,
        method: str,
        request: t.OptionalContainerValueMapping,
    ) -> r[m.Grpc.Payload]:
        """Delegate method calls.

        Args:
        client: gRPC client entity
        method: gRPC method name
        request: Request message (gRPC protocol message - dynamic type)

        Returns:
        Response data dictionary

        Note: Uses ConfigValue for gRPC protocol message compatibility

        """
        return self._client_manager.make_call(client, method, request)

    def parse_address(self, address: str) -> r[tuple[str, int]]:
        """Parse gRPC address string."""
        if not u.Grpc.validate_target(address):
            return r[tuple[str, int]].fail(f"Invalid address: {address}")
        return r[tuple[str, int]].ok(u.Grpc.parse_address(address))

    def send_data(
        self,
        stream: m.Grpc.GrpcStream,
        data: t.OptionalContainerValueMapping,
    ) -> r[m.Grpc.Payload]:
        """Delegate data sending.

        Args:
        stream: gRPC stream entity
        data: Message data (gRPC protocol message - dynamic type)

        Returns:
        Response data dictionary

        Note: Uses t.NormalizedValue for gRPC message compatibility

        """
        return self._stream_manager.send_data(stream, data)

    def start_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Delegate server start.

        Args:
        server: gRPC server entity to start

        Returns:
        Started server entity

        """
        return self._server_manager.start_server(server)

    def stop_server(self, server: m.Grpc.Server) -> r[m.Grpc.Server]:
        """Delegate server stop.

        Args:
        server: gRPC server entity to stop

        Returns:
        Stopped server entity

        """
        return self._server_manager.stop_server(server)

    def validate_target(self, target: str) -> bool:
        """Validate gRPC target string."""
        return u.Grpc.validate_target(target)

    class CompleteSetup(BaseModel):
        """Complete gRPC setup result."""

        server: m.Grpc.Server
        client: m.Grpc.Client
        service: m.Grpc.Service
        target: str


__all__ = ["FlextGrpc"]
