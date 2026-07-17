"""Flext-grpc config protocols.

Protocol interfaces for the validated ``config.Grpc.*`` business-rule SSOT.
Models are defined in ``_models/config.py``; this module only declares the
shape consumed by ``_config.py`` and typed consumers.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from flext_grpc._models.config import FlextGrpcConfigModels


class FlextGrpcProtocolsConfig:
    """Namespace of config protocol interfaces for flext-grpc."""

    class Network(Protocol):
        """gRPC network defaults and validation thresholds."""

        @property
        def default_channel_ready_timeout(self) -> float: ...
        @property
        def default_graceful_shutdown_timeout(self) -> float: ...
        @property
        def default_host(self) -> str: ...
        @property
        def default_keepalive_time_ms(self) -> int: ...
        @property
        def default_keepalive_timeout_ms(self) -> int: ...
        @property
        def default_port(self) -> int: ...
        @property
        def default_timeout(self) -> float: ...
        @property
        def host_pattern(self) -> str: ...
        @property
        def max_port(self) -> int: ...
        @property
        def min_port(self) -> int: ...

    class Performance(Protocol):
        """gRPC message and thread-pool performance limits."""

        @property
        def default_message_length(self) -> int: ...
        @property
        def default_thread_pool_size(self) -> int: ...
        @property
        def max_message_length(self) -> int: ...
        @property
        def max_thread_pool_size(self) -> int: ...
        @property
        def min_message_length(self) -> int: ...
        @property
        def min_thread_pool_size(self) -> int: ...

    class Service(Protocol):
        """gRPC server/worker policy defaults."""

        @property
        def default_max_concurrent_rpcs(self) -> int: ...
        @property
        def default_max_workers(self) -> int: ...
        @property
        def max_workers(self) -> int: ...
        @property
        def min_workers(self) -> int: ...

    class Streaming(Protocol):
        """gRPC streaming buffer and concurrency policy."""

        @property
        def bidirectional_queue_size(self) -> int: ...
        @property
        def client_buffer_threshold(self) -> int: ...
        @property
        def default_buffer_size(self) -> int: ...
        @property
        def default_max_concurrent_streams(self) -> int: ...
        @property
        def max_buffer_size(self) -> int: ...
        @property
        def min_buffer_size(self) -> int: ...
        @property
        def server_batch_size(self) -> int: ...

    class ConnectionPool(Protocol):
        """gRPC connection-pool defaults."""

        @property
        def default_pool_size(self) -> int: ...

    class Grpc(Protocol):
        """Root gRPC business-rule namespace."""

        @property
        def network(self) -> FlextGrpcConfigModels.Network: ...
        @property
        def performance(self) -> FlextGrpcConfigModels.Performance: ...
        @property
        def service(self) -> FlextGrpcConfigModels.Service: ...
        @property
        def streaming(self) -> FlextGrpcConfigModels.Streaming: ...
        @property
        def connection_pool(self) -> FlextGrpcConfigModels.ConnectionPool: ...


__all__: list[str] = ["FlextGrpcProtocolsConfig"]
