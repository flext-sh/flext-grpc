"""Stream processing service mixin for flext-grpc."""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import c, e, m, p, r, s, t

from ._entities.stream_manager import FlextGrpcStreamManagerImpl
from ._entities.stream_state import FlextGrpcStreamRuntimeState


class FlextGrpcStream(s):
    """Mixin providing stream processing for FlextGrpc facade."""

    _FlextGrpcStreamRuntimeState: ClassVar[type[FlextGrpcStreamRuntimeState]] = (
        FlextGrpcStreamRuntimeState
    )
    GrpcStreamManager: ClassVar[type[FlextGrpcStreamManagerImpl]] = (
        FlextGrpcStreamManagerImpl
    )

    def create_stream(
        self, method_name: str = "DefaultMethod", stream_type: str = "unary"
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create and register stream runtime state using the dedicated manager."""
        if not method_name.strip():
            return e.fail_validation("method_name", error="cannot be empty")
        if stream_type not in c.Grpc.STREAM_TYPES:
            return r[m.Grpc.GrpcStream].fail(f"Invalid stream type: {stream_type}")
        return self._stream_manager.create_stream(
            method_name=method_name, stream_type=stream_type
        )

    def close_stream(self, stream: m.Grpc.GrpcStream) -> p.Result[m.Grpc.GrpcStream]:
        """Close stream runtime state via the dedicated manager."""
        return self._stream_manager.close_stream(stream)

    def send_data(
        self, stream: m.Grpc.GrpcStream, data: t.JsonMapping | None
    ) -> p.Result[m.Grpc.Payload]:
        """Send stream data via the dedicated stream manager."""
        return self._stream_manager.send_data(stream, data)

    _stream_manager: FlextGrpcStreamManagerImpl = m.PrivateAttr(
        default_factory=FlextGrpcStreamManagerImpl
    )


__all__: list[str] = ["FlextGrpcStream"]
