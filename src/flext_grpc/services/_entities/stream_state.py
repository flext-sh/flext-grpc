"""Stream runtime state model entity (ENFORCE-067: one class per module)."""

from __future__ import annotations

from collections import deque

from flext_grpc import c, m, t, u


class FlextGrpcStreamRuntimeState(m.Value):
    """Bounded runtime state tracked for one open gRPC stream."""

    stream: m.Grpc.GrpcStream = u.Field(
        description="gRPC stream instance being tracked"
    )
    created_at: float = u.Field(
        description="Stream creation timestamp in epoch seconds"
    )
    buffer: deque[t.JsonMapping | None] = u.Field(
        default_factory=lambda: deque[t.JsonMapping | None](
            maxlen=c.Grpc.STREAMING_DEFAULT_BUFFER_SIZE
        ),
        description="Bounded message buffer for stream processing",
    )


__all__: list[str] = ["FlextGrpcStreamRuntimeState"]
