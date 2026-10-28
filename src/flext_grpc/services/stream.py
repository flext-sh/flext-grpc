"""Stream processing service mixin for flext-grpc.

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

from typing import ClassVar

from flext_grpc import c, e, m, p, r, s, t
from flext_grpc.services._entities import FlextGrpcStreamManagerImpl


class FlextGrpcStream(s):
    """Mixin providing stream processing for FlextGrpc facade."""

    GrpcStreamManager: ClassVar[type[FlextGrpcStreamManagerImpl]] = (
        FlextGrpcStreamManagerImpl
    )

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create and register stream runtime state using the dedicated manager.

        Args:
            method_name: RPC method name backing the stream.
            stream_type: Stream communication pattern name.

        Returns:
            The resulting ``p.Result[m.Grpc.GrpcStream]``.

        """
        if not method_name.strip():
            return e.fail_validation("method_name", error="cannot be empty")
        if stream_type not in c.Grpc.STREAM_TYPES:
            return r[m.Grpc.GrpcStream].fail(f"Invalid stream type: {stream_type}")
        return self._stream_manager.create_stream(
            method_name=method_name,
            stream_type=stream_type,
        )

    def close_stream(self, stream: m.Grpc.GrpcStream) -> p.Result[m.Grpc.GrpcStream]:
        """Close stream runtime state via the dedicated manager.

        Args:
            stream: Stream entity to close.

        Returns:
            The resulting ``p.Result[m.Grpc.GrpcStream]``.

        """
        return self._stream_manager.close_stream(stream)

    def send_data(
        self,
        stream: m.Grpc.GrpcStream,
        data: t.JsonMapping | None,
    ) -> p.Result[m.Grpc.Payload]:
        """Send stream data via the dedicated stream manager.

        Args:
            stream: Stream entity that receives the data.
            data: Optional payload mapping to send.

        Returns:
            The resulting ``p.Result[m.Grpc.Payload]``.

        """
        return self._stream_manager.send_data(stream, data)

    _stream_manager: FlextGrpcStreamManagerImpl = m.PrivateAttr(
        default_factory=FlextGrpcStreamManagerImpl,
    )


__all__: list[str] = ["FlextGrpcStream"]
