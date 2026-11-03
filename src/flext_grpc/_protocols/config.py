# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_grpc/_protocols/config
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_grpc._protocols import FlextGrpcProtocolsStream


class FlextGrpcProtocolsConfig:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class Network(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def default_channel_ready_timeout(self) -> float:
            """Seconds to wait for a channel to become ready."""
            ...

        @property
        def default_graceful_shutdown_timeout(self) -> float:
            """Seconds to wait during graceful shutdown."""
            ...

        @property
        def default_host(self) -> str:
            """Default bind/connect host."""
            ...

        @property
        def default_keepalive_time_ms(self) -> int:
            """Keepalive probe interval in milliseconds."""
            ...

        @property
        def default_keepalive_timeout_ms(self) -> int:
            """Keepalive probe timeout in milliseconds."""
            ...

        @property
        def default_port(self) -> int:
            """Default gRPC port."""
            ...

        @property
        def default_timeout(self) -> float:
            """Default request timeout in seconds."""
            ...

        @property
        def host_pattern(self) -> str:
            """Regex validating a host name."""
            ...

        @property
        def max_port(self) -> int:
            """Maximum valid port."""
            ...

        @property
        def min_port(self) -> int:
            """Minimum valid port."""
            ...

    @runtime_checkable
    class Performance(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def default_message_length(self) -> int:
            """Default maximum message length in bytes."""
            ...

        @property
        def default_thread_pool_size(self) -> int:
            """Default executor thread-pool size."""
            ...

        @property
        def max_message_length(self) -> int:
            """Absolute maximum message length in bytes."""
            ...

        @property
        def max_thread_pool_size(self) -> int:
            """Absolute maximum thread-pool size."""
            ...

        @property
        def min_message_length(self) -> int:
            """Absolute minimum message length in bytes."""
            ...

        @property
        def min_thread_pool_size(self) -> int:
            """Absolute minimum thread-pool size."""
            ...

    @runtime_checkable
    class ServicePolicy(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def default_max_concurrent_rpcs(self) -> int:
            """Default RPC concurrency limit."""
            ...

        @property
        def default_max_workers(self) -> int:
            """Default worker pool size."""
            ...

        @property
        def max_workers(self) -> int:
            """Maximum worker pool size."""
            ...

        @property
        def min_workers(self) -> int:
            """Minimum worker pool size."""
            ...

    @runtime_checkable
    class Streaming(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def bidirectional_queue_size(self) -> int:
            """Bidirectional stream queue size."""
            ...

        @property
        def client_buffer_threshold(self) -> int:
            """Client-stream buffer threshold."""
            ...

        @property
        def default_buffer_size(self) -> int:
            """Default per-stream buffer size."""
            ...

        @property
        def default_max_concurrent_streams(self) -> int:
            """Default concurrent stream limit."""
            ...

        @property
        def max_buffer_size(self) -> int:
            """Absolute maximum buffer size."""
            ...

        @property
        def min_buffer_size(self) -> int:
            """Absolute minimum buffer size."""
            ...

        @property
        def server_batch_size(self) -> int:
            """Server-stream batch size."""
            ...

    @runtime_checkable
    class ConnectionPool(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def default_pool_size(self) -> int:
            """Default number of pooled channels."""
            ...

    @runtime_checkable
    class Grpc(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def network(self) -> FlextGrpcProtocolsConfig.Network:
            """Network defaults and validation thresholds."""
            ...

        @property
        def performance(self) -> FlextGrpcProtocolsConfig.Performance:
            """Message and thread-pool performance limits."""
            ...

        @property
        def service(self) -> FlextGrpcProtocolsConfig.ServicePolicy:
            """Server/worker policy defaults."""
            ...

        @property
        def streaming(self) -> FlextGrpcProtocolsStream.Streaming:
            """Streaming buffer and concurrency policy."""
            ...

        @property
        def connection_pool(self) -> FlextGrpcProtocolsConfig.ConnectionPool:
            """Connection-pool defaults."""
            ...

    @runtime_checkable
    class Root(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def Grpc(self) -> FlextGrpcProtocolsConfig.Grpc:
            """GRPC business-rule config namespace."""
            ...


__all__: list[str] = [
    "FlextGrpcProtocolsConfig",
]
