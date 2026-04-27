"""Stream processing service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections import deque
from collections.abc import (
    MutableMapping,
)

from flext_grpc import FlextGrpcMetrics, c, e, m, p, r, t, u
from flext_grpc.base import s


class FlextGrpcStream(s):
    """Mixin providing stream processing for FlextGrpc facade."""

    _stream_manager: FlextGrpcStream.GrpcStreamManager = m.PrivateAttr(
        default_factory=lambda: FlextGrpcStream.GrpcStreamManager()
    )

    class _StreamRuntimeState(m.Value):
        stream: m.Grpc.GrpcStream = u.Field(
            description="gRPC stream instance being tracked"
        )
        created_at: float = u.Field(
            description="Stream creation timestamp in epoch seconds"
        )
        buffer: deque[t.JsonMapping | None] = u.Field(
            default_factory=lambda: deque[t.JsonMapping | None](
                maxlen=c.Grpc.STREAMING_DEFAULT_BUFFER_SIZE,
            ),
            description="Bounded message buffer for stream processing",
        )

    @staticmethod
    def _new_stream_buffer() -> deque[t.JsonMapping | None]:
        return deque(maxlen=c.Grpc.STREAMING_DEFAULT_BUFFER_SIZE)

    class GrpcStreamManager:
        """Dedicated stream processing with buffering."""

        def __init__(self) -> None:
            """Initialize stream manager with metrics tracking."""
            super().__init__()
            self._active_streams: MutableMapping[
                str,
                FlextGrpcStream._StreamRuntimeState,
            ] = {}
            self._metrics = FlextGrpcMetrics.MetricsCollector()

        def close_stream(
            self, stream: m.Grpc.GrpcStream
        ) -> p.Result[m.Grpc.GrpcStream]:
            """Close stream and cleanup."""
            stream_key = f"{stream.id}_{stream.stream_type}"
            if stream_key in self._active_streams:
                del self._active_streams[stream_key]
            return r[m.Grpc.GrpcStream].ok(stream)

        def create_stream(
            self, **kwargs: t.JsonValue | None
        ) -> p.Result[m.Grpc.GrpcStream]:
            """Create stream with proper setup."""
            method_name = str(kwargs.get("method_name", "DefaultMethod"))
            stream_type = str(kwargs.get("stream_type", "unary"))
            stream_result = u.Grpc.create_stream_entity(method_name, stream_type)
            if stream_result.failure:
                return stream_result
            stream = stream_result.value
            stream_key = f"{stream.id}_{stream.stream_type}"
            self._active_streams[stream_key] = FlextGrpcStream._StreamRuntimeState(
                stream=stream,
                created_at=time.time(),
                buffer=FlextGrpcStream._new_stream_buffer(),
            )
            self._metrics.record_metric(f"{stream_key}_created", time.time())
            return r[m.Grpc.GrpcStream].ok(stream)

        def send_data(
            self,
            stream: m.Grpc.GrpcStream,
            data: t.JsonMapping | None,
        ) -> p.Result[m.Grpc.Payload]:
            """Send data with buffering strategy.

            Args:
            stream: Stream entity
            data: Message data (gRPC protocol message - dynamic type)

            """
            stream_key = f"{stream.id}_{stream.stream_type}"
            if stream_key not in self._active_streams:
                return e.fail_not_found("stream", stream.id)
            stream_info = self._active_streams[stream_key]
            try:
                stream_state = FlextGrpcStream._StreamRuntimeState.model_validate(
                    stream_info,
                )
                stream_state.buffer.append(data)
                self._active_streams[stream_key] = stream_state
                return r[m.Grpc.Payload].ok(
                    m.Grpc.Payload.from_values(
                        stream_id=stream.id,
                        data_sent=str(data),
                        buffer_size=len(stream_state.buffer),
                    ),
                )
            except c.ValidationError as exc:
                return e.fail_validation("stream_state", error=exc)

    def create_stream(
        self,
        method_name: str = "DefaultMethod",
        stream_type: str = "unary",
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create and register stream runtime state using the dedicated manager."""
        if not method_name.strip():
            return e.fail_validation("method_name", error="cannot be empty")
        if stream_type not in c.Grpc.STREAM_TYPES:
            return r[m.Grpc.GrpcStream].fail(f"Invalid stream type: {stream_type}")
        return self._stream_manager.create_stream(
            method_name=method_name,
            stream_type=stream_type,
        )

    def close_stream(self, stream: m.Grpc.GrpcStream) -> p.Result[m.Grpc.GrpcStream]:
        """Close stream runtime state via the dedicated manager."""
        return self._stream_manager.close_stream(stream)

    def send_data(
        self,
        stream: m.Grpc.GrpcStream,
        data: t.JsonMapping | None,
    ) -> p.Result[m.Grpc.Payload]:
        """Send stream data via the dedicated stream manager."""
        return self._stream_manager.send_data(stream, data)


__all__: list[str] = ["FlextGrpcStream"]
