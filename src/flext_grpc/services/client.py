"""Client connection service mixin for flext-grpc."""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import m, p, s, t

from ._entities.client_manager import FlextGrpcClientManagerImpl


class FlextGrpcClient(s):
    """Mixin providing client connection management for FlextGrpc facade."""

    GrpcClientManager: ClassVar[type[FlextGrpcClientManagerImpl]] = (
        FlextGrpcClientManagerImpl
    )

    _client_manager: FlextGrpcClientManagerImpl = m.PrivateAttr(
        default_factory=FlextGrpcClientManagerImpl
    )

    def connect_client(self, target: str) -> p.Result[m.Grpc.Client]:
        """Establish a client connection through the dedicated manager."""
        return self._client_manager.connect(target)

    def disconnect_client(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Client]:
        """Disconnect a client connection through the dedicated manager."""
        return self._client_manager.disconnect(client)

    def client_status(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Payload]:
        """Fetch client connection status via the dedicated manager."""
        return self._client_manager.client_status(client)

    def make_call(
        self, client: m.Grpc.Client, method: str, request: t.JsonMapping | None
    ) -> p.Result[m.Grpc.Payload]:
        """Execute an RPC call through the dedicated client manager."""
        return self._client_manager.make_call(client, method, request)


__all__: list[str] = ["FlextGrpcClient"]
