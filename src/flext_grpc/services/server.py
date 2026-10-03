"""Server lifecycle service mixin for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import FlextGrpcModels, m, p, s
from flext_grpc.services._entities.server_manager import FlextGrpcServerManagerImpl


class FlextGrpcServer(s):
    """Mixin providing server lifecycle management for FlextGrpc facade."""

    GrpcServerManager: ClassVar[type[FlextGrpcServerManagerImpl]] = (
        FlextGrpcServerManagerImpl
    )

    def start_server(
        self, server: FlextGrpcModels.Grpc.Server,
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Start a server through the dedicated lifecycle manager.

        Returns:
            The resulting ``p.Result[FlextGrpcModels.Grpc.Server]``.
        """
        return self._server_manager.start_server(server)

    def stop_server(
        self, server: FlextGrpcModels.Grpc.Server,
    ) -> p.Result[FlextGrpcModels.Grpc.Server]:
        """Stop a server through the dedicated lifecycle manager.

        Returns:
            The resulting ``p.Result[FlextGrpcModels.Grpc.Server]``.
        """
        return self._server_manager.stop_server(server)

    def server_status(
        self, server: FlextGrpcModels.Grpc.Server,
    ) -> p.Result[FlextGrpcModels.Grpc.Payload]:
        """Fetch server runtime metrics through the dedicated manager.

        Returns:
            The resulting ``p.Result[FlextGrpcModels.Grpc.Payload]``.
        """
        return self._server_manager.server_metrics(server)

    _server_manager: FlextGrpcServerManagerImpl = m.PrivateAttr(
        default_factory=FlextGrpcServerManagerImpl,
    )


__all__: list[str] = ["FlextGrpcServer"]
