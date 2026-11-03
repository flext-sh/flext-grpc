"""gRPC channel and readiness protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable


class FlextGrpcProtocolsChannel:
    """gRPC channel protocol contracts composed into ``p.Grpc``."""

    @runtime_checkable
    class GrpcChannel(Protocol):
        """Protocol for gRPC channel operations (duck typing for grpc.Channel)."""

        def close(self) -> None:
            """Close the channel."""
            ...

        def unsubscribe(self, callback: Callable[..., None]) -> None:
            """Remove a subscription callback from the channel.

            Args:
                callback: Callback previously registered on the channel.

            """
            ...

    @runtime_checkable
    class GrpcChannelCredentials(Protocol):
        """Protocol for gRPC channel credentials.

        Duck typing for ``grpc.ChannelCredentials``.
        """

    @runtime_checkable
    class GrpcReadyFuture(Protocol):
        """Protocol for gRPC ready futures."""

        def result(self, timeout: float | None = None) -> None:
            """Wait until the underlying operation is ready.

            Args:
                timeout: Maximum wait in seconds, or ``None`` to wait indefinitely.

            """
            ...

        def cancel(self) -> bool:
            """Release the channel subscription when readiness ends.

            Returns:
                ``True`` when the pending readiness attempt was cancelled.

            """
            ...


__all__: list[str] = ["FlextGrpcProtocolsChannel"]
