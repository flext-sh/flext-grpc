"""gRPC client connection protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_grpc._protocols import FlextGrpcProtocolsChannel


class FlextGrpcProtocolsConnection:
    """gRPC connection protocol contracts composed into ``p.Grpc``."""

    @runtime_checkable
    class ClientConnection(Protocol):
        """Base class for gRPC client connection management."""

    @runtime_checkable
    class GrpcStub(Protocol):
        """Protocol for gRPC client stub (duck typing for grpc stubs)."""

        def __init__(self, channel: FlextGrpcProtocolsChannel.GrpcChannel) -> None:
            """Initialize the stub with a channel."""
            ...

    @runtime_checkable
    class GrpcCallFailure(Protocol):
        """Protocol for gRPC call failures exposing status details."""

        def code(self) -> str | None:
            """Return the gRPC status code, if available.

            Returns:
                Status code string, or ``None`` when unavailable.

            """
            ...

        def details(self) -> str:
            """Return the gRPC status details.

            Returns:
                Status details string.

            """
            ...


__all__: list[str] = ["FlextGrpcProtocolsConnection"]
