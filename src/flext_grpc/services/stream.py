"""Stream processing service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections import deque
from collections.abc import MutableMapping

from pydantic import Field, ValidationError

from flext_grpc import FlextGrpcMetrics, c, m, p, r, t, u


class FlextGrpcStream:
    """Mixin providing stream processing for FlextGrpc facade."""

    class _StreamRuntimeState(m.Value):
        stream: m.Grpc.GrpcStream = Field(
            description="gRPC stream instance being tracked"
        )
        created_at: float = Field(
            description="Stream creation timestamp in epoch seconds"
        )
        buffer: deque[t.OptionalContainerValueMapping] = Field(
            default_factory=lambda: deque[t.OptionalContainerValueMapping](
                maxlen=c.Grpc.Streaming.DEFAULT_BUFFER_SIZE,
            ),
            description="Bounded message buffer for stream processing",
        )

    @staticmethod
    def _new_stream_buffer() -> deque[t.OptionalContainerValueMapping]:
        return deque(maxlen=c.Grpc.Streaming.DEFAULT_BUFFER_SIZE)

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
            self, **kwargs: t.OptionalContainerValue
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
            data: t.OptionalContainerValueMapping,
        ) -> p.Result[m.Grpc.Payload]:
            """Send data with buffering strategy.

            Args:
            stream: Stream entity
            data: Message data (gRPC protocol message - dynamic type)

            """
            stream_key = f"{stream.id}_{stream.stream_type}"
            if stream_key not in self._active_streams:
                return r[m.Grpc.Payload].fail("Stream not found")
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
            except ValidationError as e:
                return r[m.Grpc.Payload].fail(f"Invalid stream state: {e}")


__all__: list[str] = ["FlextGrpcStream"]
