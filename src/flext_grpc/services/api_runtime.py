"""Runtime mixin used by the public gRPC API facade."""

from __future__ import annotations

from typing import override

from flext_grpc import u, FlextGrpcSettings, FlextGrpcUtilities, c, m, p, r, t
from flext_grpc.base import FlextGrpcServiceBase


class FlextGrpcApiRuntime(FlextGrpcServiceBase):
    """Runtime behavior composed by the public gRPC facade via MRO."""

    def create_channel(
        self, target: str, options: t.JsonMapping | None = None
    ) -> p.Result[m.Grpc.Channel]:
        """Create typed channel entity from validated inputs."""
        return FlextGrpcUtilities.Grpc.create_channel_entity(
            target=target, options={} if options is None else options
        )

    def create_client(
        self, target: str, options: t.JsonMapping | None = None
    ) -> p.Result[m.Grpc.Client]:
        """Create typed client entity from validated inputs."""
        return FlextGrpcUtilities.Grpc.create_client_entity(
            target=target, options=options
        )

    def create_complete_setup(
        self,
        host: str = c.Grpc.NETWORK_DEFAULT_HOST,
        port: int = c.Grpc.NETWORK_DEFAULT_GRPC_PORT,
        service_name: str = "DefaultService",
        methods: t.StrSequence | None = None,
    ) -> p.Result[m.Grpc.CompleteSetup]:
        """Complete setup using functional composition."""
        resolved_methods = ["HealthCheck"] if methods is None else methods
        target = f"{host}:{port}"

        server_result = self.create_server(host=host, port=port)
        if server_result.failure:
            return r[m.Grpc.CompleteSetup].from_failure(server_result)

        client_result = self.create_client(target=target)
        if client_result.failure:
            return r[m.Grpc.CompleteSetup].from_failure(client_result)

        service_result = self.create_service(
            name=service_name, methods=resolved_methods
        )
        if service_result.failure:
            return r[m.Grpc.CompleteSetup].from_failure(service_result)

        return r[m.Grpc.CompleteSetup].ok(
            m.Grpc.CompleteSetup(
                server=server_result.value,
                client=client_result.value,
                service=service_result.value,
                target=target,
            )
        )

    def create_server(
        self,
        host: str = c.Grpc.NETWORK_DEFAULT_HOST,
        port: int = c.Grpc.NETWORK_DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.SERVICE_DEFAULT_MAX_WORKERS,
    ) -> p.Result[m.Grpc.Server]:
        """Create typed server entity from validated inputs."""
        return FlextGrpcUtilities.Grpc.create_server_entity(
            host=host, port=port, max_workers=max_workers
        )

    def create_service(
        self, name: str, methods: t.StrSequence | None = None
    ) -> p.Result[m.Grpc.Service]:
        """Create typed service entity from validated inputs."""
        return FlextGrpcUtilities.Grpc.create_service_entity(
            name=name, methods=[] if methods is None else methods
        )

    @override
    def execute(self) -> p.Result[FlextGrpcSettings]:
        """Execute main facade operation."""
        return r[FlextGrpcSettings].ok(self.grpc_config)

    def execute_operation(
        self, request: m.Grpc.OperationExecutionRequest
    ) -> p.Result[FlextGrpcSettings]:
        """Execute operation with validation, timeout, retry, and monitoring."""
        kwargs = request.keyword_arguments
        match request.operation_name:
            case "connect_client":
                target = kwargs.get("target")
                if not isinstance(target, str):
                    return r[FlextGrpcSettings].fail(
                        "connect_client requires string target"
                    )
                result = self.create_client(target=target)
            case _:
                return r[FlextGrpcSettings].fail(
                    f"Unknown operation: {request.operation_name}"
                )
        if result.failure:
            return r[FlextGrpcSettings].from_failure(result)
        return r[FlextGrpcSettings].ok(self.grpc_config)

    def parse_address(self, address: str) -> p.Result[tuple[str, int]]:
        """Parse gRPC address string."""
        if not FlextGrpcUtilities.Grpc.validate_target(address):
            return r[tuple[str, int]].fail(f"Invalid address: {address}")
        return r[tuple[str, int]].ok(u.Grpc.parse_target(address))

    def validate_target(self, target: str) -> bool:
        """Validate gRPC target string."""
        return FlextGrpcUtilities.Grpc.validate_target(target)


__all__: list[str] = ["FlextGrpcApiRuntime"]
