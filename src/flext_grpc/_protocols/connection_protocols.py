"""gRPC client connection protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_grpc._protocols import FlextGrpcProtocolsChannel, FlextGrpcProtocolsStream

if TYPE_CHECKING:
    from flext_core._protocols import FlextProtocolsResult

    from flext_grpc import c, t


class FlextGrpcProtocolsConnection:
    """gRPC connection protocol contracts composed into ``p.Grpc``."""

    @runtime_checkable
    class ClientConnection(Protocol):
        """Base class for gRPC client connection management."""

    @runtime_checkable
    class Client(Protocol):
        """Protocol for gRPC client communication operations."""

        def connect_client(
            self,
            target: str,
            *,
            timeout: float = 30.0,
        ) -> FlextProtocolsResult.Result[FlextGrpcProtocolsChannel.GrpcChannel]:
            """Connect gRPC client to server.

            Args:
                target: gRPC server target address.
                timeout: Connection timeout in seconds.

            Returns:
                The resulting ``p.Result[GrpcChannel]``.

            """
            ...

        def disconnect_client(
            self,
            channel: FlextGrpcProtocolsChannel.GrpcChannel,
        ) -> FlextProtocolsResult.Result[bool]:
            """Disconnect gRPC client.

            Args:
                channel: Channel to close.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            ...

        def client_status(
            self,
            channel: FlextGrpcProtocolsChannel.GrpcChannel,
        ) -> FlextProtocolsResult.Result[t.JsonValue | None]:
            """Get gRPC client status information.

            Args:
                channel: Channel to inspect.

            Returns:
                The resulting ``p.Result[t.JsonValue | None]``.

            """
            ...

        def make_call(
            self,
            channel: FlextGrpcProtocolsChannel.GrpcChannel,
            method: c.Grpc.GrpcOperations | str,
            request: FlextGrpcProtocolsStream.GrpcMessage,
            *,
            timeout: float = 30.0,
        ) -> FlextProtocolsResult.Result[FlextGrpcProtocolsStream.GrpcMessage]:
            """Make gRPC method call.

            Args:
                channel: Channel used for the call.
                method: RPC operation or method name.
                request: Request message.
                timeout: Call timeout in seconds.

            Returns:
                The resulting ``p.Result[GrpcMessage]``.

            """
            ...

        def validate_connection(
            self,
            channel: FlextGrpcProtocolsChannel.GrpcChannel,
        ) -> FlextProtocolsResult.Result[bool]:
            """Validate gRPC client connection.

            Args:
                channel: Channel to validate.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            ...

    @runtime_checkable
    class GrpcStub(Protocol):
        """Protocol for gRPC client stub (duck typing for grpc stubs)."""

        def __init__(self, channel: FlextGrpcProtocolsChannel.GrpcChannel) -> None:
            """Initialize the stub with a channel."""
            ...

    @runtime_checkable
    class GrpcCallFailure(Protocol):
        """Protocol for gRPC call failures exposing status details."""

        def code(self) -> str | None:
            """Return the gRPC status code, if available.

            Returns:
                Status code string, or ``None`` when unavailable.

            """
            ...

        def details(self) -> str:
            """Return the gRPC status details.

            Returns:
                Status details string.

            """
            ...


__all__: list[str] = ["FlextGrpcProtocolsConnection"]
