"""Server lifecycle service mixin for flext-grpc."""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import FlextGrpcModels, m, p, s

from ._entities.server_manager import FlextGrpcServerManagerImpl


class FlextGrpcServer(s):
    """Mixin providing server lifecycle management for FlextGrpc facade."""

    GrpcServerManager: ClassVar[type[FlextGrpcServerManagerImpl]] = (
        FlextGrpcServerManagerImpl
    )

    def start_server(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Start a server through the dedicated lifecycle manager."""
        return self._server_manager.start_server(server)

    def stop_server(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Stop a server through the dedicated lifecycle manager."""
        return self._server_manager.stop_server(server)

    def server_status(
        self, server: FlextGrpcModels.Grpc.Server
    ) -> p.Result[FlextGrpcModels.Grpc.Payload]:
        """Fetch server runtime metrics through the dedicated manager."""
        return self._server_manager.server_metrics(server)

    _server_manager: FlextGrpcServerManagerImpl = m.PrivateAttr(
        default_factory=FlextGrpcServerManagerImpl
    )


__all__: list[str] = ["FlextGrpcServer"]
