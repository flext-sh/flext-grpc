"""Client connection service mixin for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import m, p, s, t
from flext_grpc.services._entities.client_manager import FlextGrpcClientManagerImpl


class FlextGrpcClient(s):
    """Mixin providing client connection management for FlextGrpc facade."""

    GrpcClientManager: ClassVar[type[FlextGrpcClientManagerImpl]] = (
        FlextGrpcClientManagerImpl
    )

    _client_manager: FlextGrpcClientManagerImpl = m.PrivateAttr(
        default_factory=FlextGrpcClientManagerImpl,
    )

    def connect_client(self, target: str) -> p.Result[m.Grpc.Client]:
        """Establish a client connection through the dedicated manager.

        Returns:
            The resulting ``p.Result[m.Grpc.Client]``.
        """
        return self._client_manager.connect(target)

    def disconnect_client(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Client]:
        """Disconnect a client connection through the dedicated manager.

        Returns:
            The resulting ``p.Result[m.Grpc.Client]``.
        """
        return self._client_manager.disconnect(client)

    def client_status(self, client: m.Grpc.Client) -> p.Result[m.Grpc.Payload]:
        """Fetch client connection status via the dedicated manager.

        Returns:
            The resulting ``p.Result[m.Grpc.Payload]``.
        """
        return self._client_manager.client_status(client)

    def make_call(
        self,
        client: m.Grpc.Client,
        method: str,
        request: t.JsonMapping | None,
    ) -> p.Result[m.Grpc.Payload]:
        """Execute an RPC call through the dedicated client manager.

        Returns:
            The resulting ``p.Result[m.Grpc.Payload]``.
        """
        return self._client_manager.make_call(client, method, request)


__all__: list[str] = ["FlextGrpcClient"]
