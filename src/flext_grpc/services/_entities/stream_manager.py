"""gRPC stream manager implementation entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from collections import deque
from typing import TYPE_CHECKING

from flext_grpc import c, e, m, p, r, t
from flext_grpc.errors import FlextGrpcErrors
from flext_grpc.services._entities.metrics_collector import (
    FlextGrpcMetricsCollectorImpl,
)
from flext_grpc.utilities import FlextGrpcUtilities

if TYPE_CHECKING:
    from collections.abc import MutableMapping


class FlextGrpcStreamManagerImpl:
    """Dedicated stream processing with buffering."""

    @staticmethod
    def _new_stream_buffer() -> deque[t.JsonMapping | None]:
        return deque(maxlen=c.Grpc.STREAMING_DEFAULT_BUFFER_SIZE)

    def __init__(self) -> None:
        """Initialize stream manager with metrics tracking."""
        super().__init__()
        self._active_streams: MutableMapping[str, m.Grpc.StreamRuntimeState] = {}
        self._metrics = FlextGrpcMetricsCollectorImpl()

    def close_stream(self, stream: m.Grpc.GrpcStream) -> p.Result[m.Grpc.GrpcStream]:
        """Close stream and cleanup.

        Returns:
            The resulting ``p.Result[m.Grpc.GrpcStream]``.
        """
        stream_key = f"{stream.id}_{stream.stream_type}"
        if stream_key in self._active_streams:
            del self._active_streams[stream_key]
        return r[m.Grpc.GrpcStream].ok(stream)

    def create_stream(
        self,
        **kwargs: t.JsonValue | None,
    ) -> p.Result[m.Grpc.GrpcStream]:
        """Create stream with proper setup.

        Returns:
            The resulting ``p.Result[m.Grpc.GrpcStream]``.
        """
        method_name = str(kwargs.get("method_name", "DefaultMethod"))
        stream_type = str(kwargs.get("stream_type", "unary"))
        stream_result = FlextGrpcUtilities.Grpc.create_stream_entity(
            method_name,
            stream_type,
        )
        if stream_result.failure:
            return stream_result
        stream = stream_result.value
        stream_key = f"{stream.id}_{stream.stream_type}"
        self._active_streams[stream_key] = m.Grpc.StreamRuntimeState(
            stream=stream,
            created_at=time.time(),
            buffer=self._new_stream_buffer(),
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

        Returns:
            The resulting ``p.Result[m.Grpc.Payload]``.
        """
        stream_key = f"{stream.id}_{stream.stream_type}"
        if stream_key not in self._active_streams:
            return e.fail_not_found("stream", stream.id)
        stream_info = self._active_streams[stream_key]
        try:
            stream_state = m.Grpc.StreamRuntimeState.model_validate(stream_info)
            stream_state.buffer.append(data)
            self._active_streams[stream_key] = stream_state
            return r[m.Grpc.Payload].ok(
                m.Grpc.Payload.from_values(
                    stream_id=stream.id,
                    data_sent=str(data),
                    buffer_size=len(stream_state.buffer),
                ),
            )
        except FlextGrpcErrors.ValidationError as exc:
            return e.fail_validation("stream_state", error=exc)


__all__: list[str] = ["FlextGrpcStreamManagerImpl"]
