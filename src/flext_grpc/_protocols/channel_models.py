# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_grpc/_protocols/channel_models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from datetime import datetime
from typing import TYPE_CHECKING, Protocol, Self, runtime_checkable

from flext_cli import FlextCliProtocols

if TYPE_CHECKING:
    from flext_cli import p

    from flext_grpc import c, t
    from flext_grpc._protocols import FlextGrpcProtocolsChannel


class FlextGrpcProtocolsChannelModels:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class ClientConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def target(self) -> str:
            """Target server address."""
            ...

        @property
        def timeout(self) -> t.PositiveTimeout:
            """Request timeout in seconds."""
            ...

    @runtime_checkable
    class ChannelConfig(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def address(self) -> str:
            """Channel address."""
            ...

        @property
        def options(self) -> t.JsonMapping | None:
            """Channel options."""
            ...

    @runtime_checkable
    class Entity(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        version: t.NonNegativeInt
        unique_id: t.NonEmptyStr

        @property
        def created_at(self) -> datetime:
            """Creation timestamp (configured timezone)."""
            ...

        updated_at: datetime | None

        @property
        def domain_events(self) -> Sequence[p.DomainEvent]:
            """List of uncommitted domain events for event sourcing."""
            ...

        def copy_with(self, **kwargs: t.Scalar | None) -> p.Result[Self]:
            """Copy the entity with field updates applied."""
            ...

    @runtime_checkable
    class StateTransition(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def state(self) -> str:
            """Target state after transition."""
            ...

    @runtime_checkable
    class StateMachine(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

    @runtime_checkable
    class OperationSpec(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def name(self) -> str:
            """Operation name."""
            ...

        @property
        def entity_type(self) -> t.Grpc.EntityKind:
            """Type of entity to operate on."""
            ...

        @property
        def method_name(self) -> str | None:
            """Method to invoke on entity."""
            ...

        @property
        def parameters(self) -> Mapping[str, t.JsonMapping | None]:
            """Operation parameters."""
            ...

    @runtime_checkable
    class Request(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def operation(self) -> FlextGrpcProtocolsChannelModels.OperationSpec:
            """Operation specification to execute."""
            ...

        @property
        def entity(self) -> p.BaseModel | None:
            """Associated entity."""
            ...

        @property
        def data(self) -> t.JsonMapping | None:
            """Request data."""
            ...

    @runtime_checkable
    class Response(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def success(self) -> bool:
            """Operation success status."""
            ...

        @property
        def data(self) -> p.BaseModel | None:
            """Response data."""
            ...

        @property
        def error(self) -> str | None:
            """Error message if failed."""
            ...

        @property
        def metadata(self) -> Mapping[str, t.JsonMapping | None]:
            """Response metadata."""
            ...

    @runtime_checkable
    class Channel(Entity, StateMachine, Protocol):
        """Structural data contract projected from the owning model."""

        target: str
        state: c.Grpc.ChannelState
        options: t.JsonMapping | None
        grpc_channel: FlextGrpcProtocolsChannel.GrpcChannel | None

        def connect(self) -> p.Result[Self]:
            """Transition to connecting."""
            ...

        def disconnect(self) -> p.Result[Self]:
            """Transition to idle."""
            ...

        def ready(self) -> bool:
            """Check readiness."""
            ...

        def mark_ready(self) -> p.Result[Self]:
            """Transition to ready."""
            ...

        def validate_business_rules(self) -> p.Result[bool]:
            """Functional validation composition."""
            ...


__all__: list[str] = [
    "FlextGrpcProtocolsChannelModels",
]
