"""gRPC stream protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_grpc._protocols.channel_protocols import GrpcChannel

if TYPE_CHECKING:
    from collections.abc import Sequence

    from flext_grpc import c, p, t


@runtime_checkable
class StreamProcessor(Protocol):
    """Base class for gRPC stream processing."""


@runtime_checkable
class GrpcMessage(Protocol):
    """Protocol for gRPC message objects (duck typing for protobuf messages)."""


@runtime_checkable
class GrpcStream(Protocol):
    """Protocol for gRPC stream objects (duck typing)."""


@runtime_checkable
class Streaming(Protocol):
    """Protocol for gRPC streaming operations."""

    def close_stream(
        self,
        stream: GrpcStream,
    ) -> p.Result[bool]:
        """Close gRPC stream.

        Args:
            stream: Stream to close.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        ...

    def create_stream(
        self,
        stream_type: c.Grpc.GrpcOperations | str,
        channel: GrpcChannel,
        method: str,
    ) -> p.Result[GrpcStream]:
        """Create gRPC stream.

        Args:
            stream_type: Stream communication pattern.
            channel: Channel carrying the stream.
            method: RPC method name backing the stream.

        Returns:
            The resulting ``p.Result[GrpcStream]``.

        """
        ...

    def handle_bidirectional_streaming(
        self,
        stream: GrpcStream,
    ) -> p.Result[t.JsonValue | None]:
        """Handle bidirectional streaming.

        Args:
            stream: Stream to process.

        Returns:
            The resulting ``p.Result[t.JsonValue | None]``.

        """
        ...

    def handle_client_streaming(
        self,
        stream: GrpcStream,
        data_list: t.SequenceOf[GrpcMessage],
    ) -> p.Result[GrpcMessage]:
        """Handle client-side streaming.

        Args:
            stream: Stream receiving the client messages.
            data_list: Messages sent by the client.

        Returns:
            The resulting ``p.Result[GrpcMessage]``.

        """
        ...

    def handle_server_streaming(
        self,
        stream: GrpcStream,
        request: GrpcMessage,
    ) -> p.Result[Sequence[GrpcMessage]]:
        """Handle server-side streaming.

        Args:
            stream: Stream carrying the server messages.
            request: Request message that starts the stream.

        Returns:
            The resulting ``p.Result[Sequence[GrpcMessage]]``.

        """
        ...

    def send_data(
        self,
        stream: GrpcStream,
        data: GrpcMessage,
    ) -> p.Result[bool]:
        """Send data through gRPC stream.

        Args:
            stream: Stream receiving the data.
            data: Message to send.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        ...


__all__: list[str] = [
    "GrpcMessage",
    "GrpcStream",
    "StreamProcessor",
    "Streaming",
]
