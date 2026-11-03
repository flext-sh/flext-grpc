# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_grpc/_protocols/message_models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from datetime import datetime
from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_grpc import t


class FlextGrpcProtocolsMessageModels:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class EchoRequest(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message(self) -> str:
            """Echo message."""
            ...

    @runtime_checkable
    class EchoResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def message(self) -> str:
            """Echo message."""
            ...

        @property
        def server_id(self) -> str:
            """Server identifier."""
            ...

        @property
        def timestamp(self) -> datetime:
            """Response timestamp."""
            ...

    @runtime_checkable
    class HealthRequest(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def service(self) -> str:
            """Service name."""
            ...

    @runtime_checkable
    class HealthResponse(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def status(self) -> str:
            """Health status."""
            ...

        @property
        def message(self) -> str:
            """Health check message."""
            ...

    @runtime_checkable
    class StreamInfo(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def stream_id(self) -> str:
            """Unique stream identifier."""
            ...

        @property
        def stream_type(self) -> str:
            """Stream communication type."""
            ...

        @property
        def target(self) -> str:
            """Target endpoint address."""
            ...

        @property
        def created_at(self) -> datetime:
            """Stream creation timestamp."""
            ...

        @property
        def total_requests_sent(self) -> t.NonNegativeInt:
            """Total requests sent on stream."""
            ...

        @property
        def average_latency_ms(self) -> t.NonNegativeFloat:
            """Average latency in milliseconds."""
            ...

        @property
        def error_count(self) -> t.NonNegativeInt:
            """Number of errors on stream."""
            ...

    @runtime_checkable
    class HealthCheck(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def service_name(self) -> str:
            """Service name."""
            ...

        @property
        def status(self) -> str:
            """Health status."""
            ...

        @property
        def timestamp(self) -> datetime:
            """Check timestamp."""
            ...

    @runtime_checkable
    class OperationExecutionRequest(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def operation_name(self) -> str:
            """Operation name to execute."""
            ...

        @property
        def arguments(self) -> Mapping[str, t.Scalar]:
            """Positional arguments as dict."""
            ...

        @property
        def keyword_arguments(self) -> Mapping[str, t.Scalar]:
            """Keyword arguments."""
            ...

    @runtime_checkable
    class Payload(FlextCliProtocols.Model, Protocol):
        """Structural data contract projected from the owning model."""

        values: t.JsonMapping


__all__: list[str] = [
    "FlextGrpcProtocolsMessageModels",
]
