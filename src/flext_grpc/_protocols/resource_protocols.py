"""gRPC resource and runtime protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_grpc._protocols.channel_protocols import FlextGrpcProtocolsChannel
from flext_grpc._protocols.server_protocols import FlextGrpcProtocolsServer

if TYPE_CHECKING:
    from concurrent.futures import Executor

    from flext_grpc import p, t


class FlextGrpcProtocolsResource:
    """gRPC resource protocol contracts composed into ``p.Grpc``."""

    @runtime_checkable
    class GrpcResource(Protocol):
        """Protocol for gRPC resource objects (channels, servers, streams)."""

    @runtime_checkable
    class ResourceManager(Protocol):
        """Protocol for gRPC resource management operations."""

        def acquire(self) -> p.Result[FlextGrpcProtocolsResource.GrpcResource]:
            """Acquire a resource.

            Returns:
                The resulting ``p.Result[GrpcResource]``.

            """
            ...

        def cleanup(self) -> p.Result[bool]:
            """Cleanup all resources.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            ...

        def release(
            self,
            resource: FlextGrpcProtocolsResource.GrpcResource,
        ) -> p.Result[bool]:
            """Release a resource.

            Args:
                resource: Resource to release.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            ...

    @runtime_checkable
    class GrpcCallbackFunction(Protocol):
        """Protocol for gRPC callback functions."""

        def __call__(self, *args: t.Scalar, **kwargs: t.Scalar) -> None:
            """Call the callback."""
            ...

    @runtime_checkable
    class GrpcRuntime(Protocol):
        """Protocol for the imported grpc runtime module."""

        RpcError: type[Exception]
        FutureTimeoutError: type[Exception]

        def insecure_channel(
            self,
            target: str,
        ) -> FlextGrpcProtocolsChannel.GrpcChannel:
            """Create an insecure channel for a target.

            Args:
                target: gRPC server target address.

            Returns:
                The created channel.

            """
            ...

        def channel_ready_future(
            self,
            channel: FlextGrpcProtocolsChannel.GrpcChannel,
        ) -> FlextGrpcProtocolsChannel.GrpcReadyFuture:
            """Create a future used to wait for channel readiness.

            Args:
                channel: Channel whose readiness is awaited.

            Returns:
                The readiness future.

            """
            ...

        def server(
            self,
            thread_pool: Executor,
        ) -> FlextGrpcProtocolsServer.GrpcServer:
            """Create a gRPC server using the given thread pool.

            Args:
                thread_pool: Executor servicing RPC handlers.

            Returns:
                The created server.

            """
            ...

    @runtime_checkable
    class EntityFactory(Protocol):
        """Protocol for entity factory callables."""

        def __call__(
            self,
            **kwargs: t.Scalar,
        ) -> p.Result[FlextGrpcProtocolsResource.GrpcResource]:
            """Create entity with given arguments.

            Args:
                **kwargs: Field values applied to the entity.

            Returns:
                The resulting ``p.Result[GrpcResource]``.

            """
            ...

    @runtime_checkable
    class OperationHandler(Protocol):
        """Protocol for operation handler callables."""

        def __call__(
            self,
            **kwargs: t.Scalar,
        ) -> p.Result[FlextGrpcProtocolsResource.GrpcResource]:
            """Execute operation with given arguments.

            Args:
                **kwargs: Operation arguments.

            Returns:
                The resulting ``p.Result[GrpcResource]``.

            """
            ...


__all__: list[str] = ["FlextGrpcProtocolsResource"]
