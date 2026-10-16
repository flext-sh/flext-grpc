"""gRPC server lifecycle protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    import threading
    from collections.abc import Iterable

    from flext_grpc import p, t


class FlextGrpcProtocolsServer:
    """gRPC server protocol contracts composed into ``p.Grpc``."""

    @runtime_checkable
    class ServerLifecycle(Protocol):
        """Base class for gRPC server lifecycle management."""

    @runtime_checkable
    class GrpcServicer(Protocol):
        """Protocol for gRPC service implementations (duck typing)."""

    @runtime_checkable
    class Server(Protocol):
        """Protocol for gRPC server management operations."""

        def add_service(
            self,
            service: FlextGrpcProtocolsServer.GrpcServicer,
            server: FlextGrpcProtocolsServer.GrpcServer,
        ) -> p.Result[bool]:
            """Add gRPC service to server.

            Args:
                service: Servicer implementing the service methods.
                server: Server receiving the service registration.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            ...

        def configure_port(
            self,
            server: FlextGrpcProtocolsServer.GrpcServer,
            host: str,
            port: int,
            *,
            secure: bool = False,
        ) -> p.Result[int]:
            """Configure the server port binding.

            Args:
                server: Server to bind.
                host: Host address to bind.
                port: Port number to bind.
                secure: Whether to bind a secure port.

            Returns:
                The resulting ``p.Result[int]``.

            """
            ...

        def server_status(self) -> p.Result[t.JsonValue | None]:
            """Get gRPC server status information.

            Returns:
                The resulting ``p.Result[t.JsonValue | None]``.

            """
            ...

        def start_server(
            self,
            host: str,
            port: int,
            services: t.SequenceOf[FlextGrpcProtocolsServer.GrpcServicer] | None = None,
        ) -> p.Result[FlextGrpcProtocolsServer.GrpcServer]:
            """Start gRPC server.

            Args:
                host: Host address to bind.
                port: Port number to bind.
                services: Optional servicers to register before starting.

            Returns:
                The resulting ``p.Result[GrpcServer]``.

            """
            ...

        def stop_server(self, *, grace_period: float = 30.0) -> p.Result[bool]:
            """Stop gRPC server.

            Args:
                grace_period: Grace period in seconds for in-flight RPCs.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            ...

    @runtime_checkable
    class GrpcRpcHandler(Protocol):
        """Protocol for gRPC RPC handlers."""

    @runtime_checkable
    class GrpcServer(Protocol):
        """Protocol for gRPC server operations (duck typing for grpc.Server)."""

        def add_insecure_port(self, address: str) -> int:
            """Bind the server to an insecure address.

            Args:
                address: Address in the form ``host:port``.

            Returns:
                Bound port number.

            """
            ...

        def add_generic_rpc_handlers(
            self,
            generic_rpc_handlers: Iterable[FlextGrpcProtocolsServer.GrpcRpcHandler],
        ) -> None:
            """Add generic RPC handlers.

            Args:
                generic_rpc_handlers: Handlers dispatching the RPC methods.

            """
            ...

        def start(self) -> None:
            """Start the server."""
            ...

        def stop(self, grace: float | None) -> threading.Event:
            """Stop the server with optional grace period.

            Args:
                grace: Grace period in seconds, or ``None`` for immediate stop.

            Returns:
                Event signalling full shutdown.

            """
            ...

    @runtime_checkable
    class GrpcServicerContext(Protocol):
        """Protocol for the per-RPC servicer context (grpc.ServicerContext)."""

        def peer(self) -> str:
            """Return the address of the calling peer.

            Returns:
                Peer address string.

            """
            ...


__all__: list[str] = [
    "FlextGrpcProtocolsServer",
    "GrpcRpcHandler",
    "GrpcServer",
    "GrpcServicer",
    "GrpcServicerContext",
    "Server",
    "ServerLifecycle",
]
