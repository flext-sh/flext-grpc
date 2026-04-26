"""Runtime mixin used by the public gRPC API facade."""

from __future__ import annotations

from flext_grpc import (
    FlextGrpcClient,
    FlextGrpcConnectionPool,
    FlextGrpcMetrics,
    FlextGrpcServer,
    FlextGrpcSettings,
    FlextGrpcStream,
    c,
    e,
    m,
    p,
    r,
    t,
    u,
)
from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc, __all__


class FlextGrpcApiRuntime:
    """Runtime behavior composed by the public gRPC facade via MRO."""

    def __init__(self, settings: FlextGrpcSettings | None = None) -> None:
        """Initialize facade with FLEXT ecosystem integration."""
        super().__init__()
        self._grpc_config = (
            settings if settings is not None else FlextGrpcSettings.model_validate({})
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

    def close_stream(self, stream: m.Grpc.GrpcStream) -> p.Result[m.Grpc.GrpcStream]:
        """Delegate stream closing."""
        return self._stream_manager.close_stream(stream)

    def connect_client(self, target: str) -> p.Result[m.Grpc.Client]:
        """Delegate client connection."""
        return self._client_manager.connect(target)

    def create_channel(
        self,
        target: str,
        options: t.JsonMapping | None = None,
    ) -> p.Result[m.Grpc.Channel]:
        """Create typed channel entity from validated inputs."""
        return u.Grpc.create_channel_entity(
            target=target,
            options={} if options is None else options,
        )

    def create_client(
        self,
        target: str,
        options: t.JsonMapping | None = None,
    ) -> p.Result[m.Grpc.Client]:
        """Create typed client entity from validated inputs."""
        return u.Grpc.create_client_entity(target=target, options=options)

    def create_complete_setup(
        self,
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        service_name: str = "DefaultService",
        methods: t.StrSequence | None = None,
    ) -> p.Result[m.Grpc.CompleteSetup]:
        """Complete setup using functional composition."""
        resolved_methods = ["HealthCheck"] if methods is None else methods
        target = f"{host}:{port}"

        server_result = self.create_server(host=host, port=port)
        if server_result.failure:
            return r[m.Grpc.CompleteSetup].fail(
                server_result.error or "Server creation failed"
            )

        client_result = self.create_client(target=target)
        if client_result.failure:
            return r[m.Grpc.CompleteSetup].fail(
                client_result.error or "Client creation failed"
            )

        service_result = self.create_service(
            name=service_name, methods=resolved_methods
        )
        if service_result.failure:
            return r[m.Grpc.CompleteSetup].fail(
                service_result.error or "Service creation failed"
            )

        return r[m.Grpc.CompleteSetup].ok(
            m.Grpc.CompleteSetup(
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
    ) -> p.Result[m.Grpc.Server]:
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
    ) -> p.Result[m.Grpc.Service]:
        """Create typed service entity from validated inputs."""
        return u.Grpc.create_service_entity(
            name=name,
            methods=[] if methods is None else methods,
        )

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create typed stream entity from validated inputs."""
        if not method_name.strip():
            return e.fail_validation("method_name", error="cannot be empty")
        if stream_type not in c.Grpc.STREAM_TYPES:
            return r[m.Grpc.GrpcStream].fail(f"Invalid stream type: {stream_type}")
        return u.Grpc.create_stream_entity(
            method_name=method_name,
            stream_type=stream_type,
        )

    def disconnect_client(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Client]:
        """Delegate client disconnection."""
        return self._client_manager.disconnect(client)

    def execute(self) -> p.Result[FlextGrpcSettings]:
        """Execute main facade operation."""
        return r[FlextGrpcSettings].ok(self.grpc_config)

    def execute_operation(
        self,
        request: m.Grpc.OperationExecutionRequest,
    ) -> p.Result[FlextGrpcSettings]:
        """Execute operation with validation, timeout, retry, and monitoring."""
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
        if result.failure:
            return r[FlextGrpcSettings].fail(result.error or "Unknown error")
        return r[FlextGrpcSettings].ok(self.grpc_config)

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
        request: t.JsonMapping | None,
    ) -> p.Result[m.Grpc.Payload]:
        """Delegate method calls."""
        return self._client_manager.make_call(client, method, request)

    def parse_address(self, address: str) -> p.Result[tuple[str, int]]:
        """Parse gRPC address string."""
        if not u.Grpc.validate_target(address):
            return r[tuple[str, int]].fail(f"Invalid address: {address}")
        return r[tuple[str, int]].ok(FlextGrpcUtilitiesGrpc.parse_target(address))

    def send_data(
        self,
        stream: m.Grpc.GrpcStream,
        data: t.JsonMapping | None,
    ) -> p.Result[m.Grpc.Payload]:
        """Delegate data sending."""
        return self._stream_manager.send_data(stream, data)

    def start_server(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Server]:
        """Delegate server start."""
        return self._server_manager.start_server(server)

    def stop_server(self, server: m.Grpc.Server) -> p.Result[m.Grpc.Server]:
        """Delegate server stop."""
        return self._server_manager.stop_server(server)

    def validate_target(self, target: str) -> bool:
        """Validate gRPC target string."""
        return u.Grpc.validate_target(target)


__all__: list[str] = ["FlextGrpcApiRuntime"]
