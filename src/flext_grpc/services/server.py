"""Server lifecycle service mixin for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import m, p, s
from flext_grpc.services._entities import FlextGrpcServerManagerImpl


class FlextGrpcServer(s):
    """Mixin providing server lifecycle management for FlextGrpc facade."""

    GrpcServerManager: ClassVar[type[FlextGrpcServerManagerImpl]] = (
        FlextGrpcServerManagerImpl
    )

    def start_server(
        self,
        server: m.Grpc.Server,
    ) -> p.Result[m.Grpc.Server]:
        """Start a server through the dedicated lifecycle manager.

        Args:
            server: Server entity to transition to running.

        Returns:
            The resulting ``p.Result[m.Grpc.Server]``.

        """
        return self._server_manager.start_server(server)

    def stop_server(
        self,
        server: m.Grpc.Server,
    ) -> p.Result[m.Grpc.Server]:
        """Stop a server through the dedicated lifecycle manager.

        Args:
            server: Server entity to transition to stopped.

        Returns:
            The resulting ``p.Result[m.Grpc.Server]``.

        """
        return self._server_manager.stop_server(server)

    def server_status(
        self,
        server: m.Grpc.Server,
    ) -> p.Result[m.Grpc.Payload]:
        """Fetch server runtime metrics through the dedicated manager.

        Args:
            server: Server entity to inspect.

        Returns:
            The resulting ``p.Result[m.Grpc.Payload]``.

        """
        return self._server_manager.server_metrics(server)

    _server_manager: FlextGrpcServerManagerImpl = m.PrivateAttr(
        default_factory=FlextGrpcServerManagerImpl,
    )


__all__: list[str] = ["FlextGrpcServer"]
