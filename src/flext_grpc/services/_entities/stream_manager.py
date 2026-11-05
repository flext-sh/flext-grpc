"""gRPC stream manager implementation entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import time
from collections.abc import MutableMapping

from flext_grpc.constants import c
from flext_grpc.exceptions import e
from flext_grpc.models import m
from flext_grpc.protocols import p
from flext_grpc.result import r
from flext_grpc.services._entities import FlextGrpcMetricsCollectorImpl
from flext_grpc.typings import t
from flext_grpc.utilities import u


class FlextGrpcStreamManagerImpl:
    """Dedicated stream processing with buffering."""

    def __init__(self) -> None:
        """Initialize stream manager with metrics tracking."""
        super().__init__()
        self._active_streams: MutableMapping[str, m.Grpc.StreamRuntimeState] = {}
        self._metrics = FlextGrpcMetricsCollectorImpl()

    def close_stream(self, stream: p.Grpc.GrpcStream) -> p.Result[p.Grpc.GrpcStream]:
        """Close a stream and clean up its runtime state.

        Args:
            stream: Stream entity to close.

        Returns:
            The resulting ``p.Result[p.Grpc.GrpcStream]``.

        """
        stream_key = f"{stream.id}_{stream.stream_type}"
        if stream_key in self._active_streams:
            del self._active_streams[stream_key]
        return r[p.Grpc.GrpcStream].ok(stream)

    def create_stream(
        self,
        **kwargs: t.JsonValue | None,
    ) -> p.Result[p.Grpc.GrpcStream]:
        """Create a stream with proper setup.

        Args:
            **kwargs: Stream fields including ``method_name`` and
                ``stream_type``.

        Returns:
            The resulting ``p.Result[p.Grpc.GrpcStream]``.

        """
        method_name = str(kwargs.get("method_name", "DefaultMethod"))
        stream_type = str(kwargs.get("stream_type", "unary"))
        stream_result = u.Grpc.create_stream_entity(
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
        )
        self._metrics.record_metric(f"{stream_key}_created", time.time())
        return r[p.Grpc.GrpcStream].ok(stream)

    def send_data(
        self,
        stream: p.Grpc.GrpcStream,
        data: t.JsonMapping | None,
    ) -> p.Result[p.Grpc.Payload]:
        """Send data using a bounded buffering strategy.

        Args:
            stream: Stream entity receiving the data.
            data: Optional payload mapping to send.

        Returns:
            The resulting ``p.Result[p.Grpc.Payload]``.

        """
        stream_key = f"{stream.id}_{stream.stream_type}"
        if stream_key not in self._active_streams:
            return e.fail_not_found(c.ProcessingMode.STREAM, stream.id)
        stream_state = self._active_streams[stream_key]
        stream_state.buffer.append(data)
        return r[p.Grpc.Payload].ok(
            m.Grpc.Payload.from_values(
                stream_id=stream.id,
                data_sent=str(data),
                buffer_size=len(stream_state.buffer),
            ),
        )


__all__: list[str] = ["FlextGrpcStreamManagerImpl"]
