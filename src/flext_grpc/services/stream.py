"""Stream processing service mixin for flext-grpc."""

from __future__ import annotations

import time
from collections import deque
from collections.abc import MutableMapping

import grpc
from flext_core import r
from pydantic import Field, ValidationError

from flext_grpc import FlextGrpcMetrics, m, t, u


class FlextGrpcStream:
    """Mixin providing stream processing for FlextGrpc facade."""

    class _StreamRuntimeState(m.Value):
        stream: m.Grpc.GrpcStream
        created_at: float
        buffer: deque[t.OptionalContainerValueMapping] = Field(
            default_factory=lambda: deque[t.OptionalContainerValueMapping](maxlen=500)
        )

    @staticmethod
    def _new_stream_buffer() -> deque[t.OptionalContainerValueMapping]:
        return deque(maxlen=500)

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

        def close_stream(self, stream: m.Grpc.GrpcStream) -> r[m.Grpc.GrpcStream]:
            """Close stream and cleanup."""
            stream_key = f"{stream.id}_{stream.stream_type}"
            if stream_key in self._active_streams:
                del self._active_streams[stream_key]
            return r[m.Grpc.GrpcStream].ok(stream)

        def create_stream(
            self, **kwargs: t.OptionalContainerValueMapping
        ) -> r[m.Grpc.GrpcStream]:
            """Create stream with proper setup."""
            method_name = str(kwargs.get("method_name", "DefaultMethod"))
            stream_type = str(kwargs.get("stream_type", "unary"))
            stream_result = u.Grpc.create_stream_entity(method_name, stream_type)
            if stream_result.is_failure:
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
        ) -> r[m.Grpc.Payload]:
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
            except (grpc.RpcError, ConnectionError, TimeoutError) as e:
                return r[m.Grpc.Payload].fail(f"Data send failed: {e}")


__all__ = ["FlextGrpcStream"]
