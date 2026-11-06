"""gRPC stream protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


class FlextGrpcProtocolsStream:
    """gRPC streaming protocol contracts composed into ``p.Grpc``."""

    @runtime_checkable
    class StreamProcessor(Protocol):
        """Base class for gRPC stream processing."""

    @runtime_checkable
    class GrpcMessage(Protocol):
        """Protocol for gRPC message objects (duck typing for protobuf messages)."""


__all__: list[str] = ["FlextGrpcProtocolsStream"]
