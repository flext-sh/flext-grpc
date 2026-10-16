"""gRPC channel and readiness protocol contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from collections.abc import Callable

    from flext_grpc import t


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
class Channel(Protocol):
    """Protocol for gRPC channel management operations."""

    def close_channel(
        self,
        channel: GrpcChannel,
    ) -> p.Result[bool]:
        """Close gRPC channel.

        Args:
            channel: Channel to close.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        ...

    def create_channel(
        self,
        target: str,
        options: t.MappingKV[str, t.JsonValue | None] | None = None,
    ) -> p.Result[GrpcChannel]:
        """Create gRPC channel.

        Args:
            target: gRPC server target address.
            options: Optional channel options keyed by name.

        Returns:
            The resulting ``p.Result[GrpcChannel]``.

        """
        ...

    def channel_state(
        self,
        channel: GrpcChannel,
    ) -> p.Result[str]:
        """Get gRPC channel connection state.

        Args:
            channel: Channel to inspect.

        Returns:
            The resulting ``p.Result[str]``.

        """
        ...

    def wait_for_state_change(
        self,
        channel: GrpcChannel,
        last_state: str,
        *,
        timeout: float = 30.0,
    ) -> p.Result[bool]:
        """Wait for channel state change.

        Args:
            channel: Channel to observe.
            last_state: Previously observed state name.
            timeout: Maximum wait in seconds.

        Returns:
            The resulting ``p.Result[bool]``.

        """
        ...


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


__all__: list[str] = [
    "Channel",
    "GrpcChannel",
    "GrpcChannelCredentials",
    "GrpcReadyFuture",
]
