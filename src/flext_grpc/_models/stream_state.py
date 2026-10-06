"""Stream runtime state model entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING

from flext_cli import FlextCliModels

from flext_grpc.constants import c
from flext_grpc.typings import t

if TYPE_CHECKING:
    from flext_grpc.models import GrpcStream


class FlextGrpcStreamRuntimeState(FlextCliModels.Value):
    """Bounded runtime state tracked for one open gRPC stream."""

    stream: GrpcStream = FlextCliModels.Field(
        description="gRPC stream instance being tracked",
    )
    created_at: float = FlextCliModels.Field(
        description="Stream creation timestamp in epoch seconds",
    )
    buffer: deque[t.JsonMapping | None] = FlextCliModels.Field(
        default_factory=lambda: deque[t.JsonMapping | None](
            maxlen=c.Grpc.STREAMING_DEFAULT_BUFFER_SIZE,
        ),
        description="Bounded message buffer for stream processing",
    )


__all__: list[str] = ["FlextGrpcStreamRuntimeState"]
