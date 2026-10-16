"""FLEXT gRPC proto message and payload models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import datetime
from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import FlextCliModels

from flext_grpc import c, t


class FlextGrpcModelsMessage:
    """gRPC message models composed into ``m.Grpc``."""

    class EchoRequest(FlextCliModels.Value):
        """Echo request message (immutable value model)."""

        message: Annotated[str, FlextCliModels.Field(description="Echo message")]

    class EchoResponse(FlextCliModels.Value):
        """Echo response message (immutable value model)."""

        message: Annotated[str, FlextCliModels.Field(description="Echo message")]
        server_id: Annotated[
            str,
            FlextCliModels.Field(description="Server identifier"),
        ] = ""
        timestamp: datetime = FlextCliModels.Field(
            default_factory=datetime.now,
            description="Response timestamp",
        )

    class HealthRequest(FlextCliModels.Value):
        """Health check request message (immutable value model)."""

        service: Annotated[
            str,
            FlextCliModels.Field(description="Service name"),
        ] = ""

    class HealthResponse(FlextCliModels.Value):
        """Health check response message (immutable value model)."""

        status: Annotated[str, FlextCliModels.Field(description="Health status")]
        message: Annotated[
            str,
            FlextCliModels.Field(description="Health check message"),
        ] = ""

    class StreamInfo(FlextCliModels.Value):
        """Basic stream information (immutable value model)."""

        stream_id: str = FlextCliModels.Field(
            description="Unique stream identifier",
        )
        stream_type: str = FlextCliModels.Field(
            description="Stream communication type",
        )
        target: str = FlextCliModels.Field(description="Target endpoint address")
        created_at: datetime = FlextCliModels.Field(
            default_factory=datetime.now,
            description="Stream creation timestamp",
        )
        total_requests_sent: Annotated[
            t.NonNegativeInt,
            FlextCliModels.Field(description="Total requests sent on stream"),
        ] = 0
        average_latency_ms: Annotated[
            t.NonNegativeFloat,
            FlextCliModels.Field(description="Average latency in milliseconds"),
        ] = 0.0
        error_count: Annotated[
            t.NonNegativeInt,
            FlextCliModels.Field(description="Number of errors on stream"),
        ] = 0

    class HealthCheck(FlextCliModels.Value):
        """gRPC health check model (immutable value model)."""

        service_name: Annotated[
            str,
            FlextCliModels.Field(description="Service name"),
        ]
        status: Annotated[str, FlextCliModels.Field(description="Health status")]
        timestamp: Annotated[
            datetime,
            FlextCliModels.Field(description="Check timestamp"),
        ]

    class OperationExecutionRequest(FlextCliModels.Value):
        """Operation execution request for gRPC service operations."""

        operation_name: Annotated[
            str,
            FlextCliModels.Field(description="Operation name to execute"),
        ]
        arguments: t.ScalarMapping = FlextCliModels.Field(
            default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
            description="Positional arguments as dict",
        )
        keyword_arguments: t.ScalarMapping = FlextCliModels.Field(
            default_factory=lambda: MappingProxyType[str, t.Scalar]({}),
            description="Keyword arguments",
        )

    class Payload(FlextCliModels.BaseModel):
        """Structured payload model replacing ad-hoc dict responses."""

        values: t.JsonMapping = FlextCliModels.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Key-value payload data",
        )

        @classmethod
        def from_values(cls, **values: t.JsonPayload | None) -> Self:
            """Build payload from keyword values.

            Args:
                **values: Payload entries keyed by name; ``None`` and
                    non-primitive values are normalized to strings.

            Returns:
                The resulting ``Self``.

            """

            def normalize_payload_value(
                value: t.JsonPayload | None,
            ) -> t.JsonValue | None:
                if value is None:
                    return ""
                if isinstance(value, c.PRIMITIVES_TYPES):
                    return value
                return str(value)

            normalized_values: t.JsonMapping = {
                metric_key: normalize_payload_value(metric_value)
                for metric_key, metric_value in values.items()
            }
            return cls(values=normalized_values)


__all__: list[str] = [
    "EchoRequest",
    "EchoResponse",
    "FlextGrpcModelsMessage",
    "HealthCheck",
    "HealthRequest",
    "HealthResponse",
    "OperationExecutionRequest",
    "Payload",
    "StreamInfo",
]
