"""FLEXT gRPC channel, state machine and operation models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import FlextCliModels

from flext_grpc import c, p, r, t


class FlextGrpcModelsChannel:
    """gRPC channel models composed into ``m.Grpc``."""

    class ClientConfig(FlextCliModels.Value):
        """Basic client configuration (immutable value model)."""

        target: Annotated[
            str,
            FlextCliModels.Field(description="Target server address"),
        ] = f"{c.Grpc.NETWORK_DEFAULT_HOST}:{c.Grpc.NETWORK_DEFAULT_GRPC_PORT}"
        timeout: Annotated[
            t.PositiveTimeout,
            FlextCliModels.Field(description="Request timeout in seconds"),
        ] = c.Grpc.NETWORK_DEFAULT_TIMEOUT

    class ChannelConfig(FlextCliModels.Value):
        """Basic channel configuration (immutable value model)."""

        address: str = FlextCliModels.Field(description="Channel address")
        options: Annotated[
            t.JsonMapping | None,
            FlextCliModels.Field(description="Channel options"),
        ] = None

    class Entity(FlextCliModels.Entity):
        """Generic base entity with functional patterns."""

        def copy_with(self, **kwargs: t.Scalar | None) -> p.Result[Self]:
            """Copy the entity with field updates applied.

            Args:
                **kwargs: Field updates applied to the entity copy.

            Returns:
                Result wrapping the updated entity copy.

            """
            return r[Self].create_from_callable(
                lambda: self.model_copy(update=kwargs),
            )

    class StateTransition(FlextCliModels.Value):
        """State transition result model."""

        state: str = FlextCliModels.Field(
            description="Target state after transition",
        )

    class StateMachine(FlextCliModels.BaseModel):
        """Generic state machine with functional transitions.

        Provides state transition logic that can be composed into
        entity classes for state management.

        Note: Uses BaseModel (not Value/ContractModel) because
        StateMachine is composed with Entity via multiple inheritance.
        Entity's model_post_init sets updated_at which requires
        the model to NOT be frozen.
        """

        @staticmethod
        def transition(
            current: str,
            target: str,
            allowed_transitions: t.MappingKV[str, set[str]],
        ) -> p.Result[FlextGrpcModelsChannel.StateTransition]:
            """Perform a generic state transition with validation.

            Args:
                current: Current state.
                target: Target state.
                allowed_transitions: Map of allowed transitions.

            Returns:
                Result wrapping the state transition on success.

            """
            if (
                current not in allowed_transitions
                or target not in allowed_transitions[current]
            ):
                return r[FlextGrpcModelsChannel.StateTransition].fail(
                    f"Invalid transition from {current} to {target}",
                )
            return r[FlextGrpcModelsChannel.StateTransition].ok(
                FlextGrpcModelsChannel.StateTransition(state=target),
            )

    class OperationSpec(FlextCliModels.Value):
        """Generic operation specification using Pydantic."""

        name: Annotated[
            str,
            FlextCliModels.Field(min_length=1, description="Operation name"),
        ]
        entity_type: Annotated[
            t.Grpc.EntityKind,
            FlextCliModels.Field(description="Type of entity to operate on"),
        ]
        method_name: Annotated[
            str | None,
            FlextCliModels.Field(description="Method to invoke on entity"),
        ] = None
        parameters: Annotated[
            t.MappingKV[str, t.JsonMapping | None],
            FlextCliModels.Field(description="Operation parameters"),
        ] = FlextCliModels.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonMapping | None]({}),
        )

    class Request(FlextCliModels.Value):
        """Generic request model with validation."""

        operation: FlextGrpcModelsChannel.OperationSpec = FlextCliModels.Field(
            description="Operation specification to execute",
        )
        entity: Annotated[
            FlextCliModels.BaseModel | None,
            FlextCliModels.Field(description="Associated entity"),
        ] = None
        data: Annotated[
            t.JsonMapping | None,
            FlextCliModels.Field(description="Request data"),
        ] = None

        @FlextCliModels.computed_field
        @property
        def valid(self) -> bool:
            """Whether request is valid."""
            return bool(self.operation.name.strip())

    class Response(FlextCliModels.Value):
        """Generic response model with metadata."""

        success: Annotated[
            bool,
            FlextCliModels.Field(description="Operation success status"),
        ]
        data: Annotated[
            FlextCliModels.BaseModel | None,
            FlextCliModels.Field(description="Response data"),
        ] = None
        error: Annotated[
            str | None,
            FlextCliModels.Field(description="Error message if failed"),
        ] = None
        metadata: Annotated[
            t.MappingKV[str, t.JsonMapping | None],
            FlextCliModels.Field(description="Response metadata"),
        ] = FlextCliModels.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonMapping | None]({}),
        )

        @FlextCliModels.computed_field
        @property
        def has_error(self) -> bool:
            """Whether response has error."""
            return not self.success or self.error is not None

    class Channel(Entity, StateMachine):
        """Generic gRPC channel with state machine delegation."""

        target: Annotated[
            str,
            FlextCliModels.Field(description="gRPC server target address"),
        ] = ""
        state: Annotated[
            c.Grpc.ChannelState,
            FlextCliModels.Field(description="Current channel connection state"),
        ] = c.Grpc.ChannelState.IDLE
        options: t.JsonMapping | None = FlextCliModels.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Channel configuration options",
        )
        grpc_channel: Annotated[
            t.Port[p.Grpc.GrpcChannel] | None,
            FlextCliModels.Field(description="Underlying gRPC channel instance"),
        ] = None

        def connect(self) -> p.Result[Self]:
            """Transition to connecting.

            Returns:
                The resulting ``p.Result[Self]``.

            """
            return self.transition(
                self.state,
                "connecting",
                {"idle": {"connecting"}},
            ).map(lambda update: self.model_copy(update={"state": update.state}))

        def disconnect(self) -> p.Result[Self]:
            """Transition to idle.

            Returns:
                The resulting ``p.Result[Self]``.

            """
            return r[Self].ok(
                self.model_copy(update={"state": c.Grpc.ChannelState.IDLE}),
            )

        def ready(self) -> bool:
            """Check readiness.

            Returns:
                The resulting ``bool``.

            """
            # ChannelState is a StrEnum, so its members compare as plain strings.
            # `c.Grpc` widens to Any through the facade MRO for mypy, which would
            # make the comparison itself Any; binding both sides to str keeps the
            # result a real bool for every checker without changing behaviour.
            current: str = self.state
            ready_state: str = c.Grpc.ChannelState.READY
            return current == ready_state

        def mark_ready(self) -> p.Result[Self]:
            """Transition to ready.

            Returns:
                The resulting ``p.Result[Self]``.

            """
            return self.transition(
                self.state,
                "ready",
                {"connecting": {"ready"}},
            ).map(lambda update: self.model_copy(update={"state": update.state}))

        def validate_business_rules(self) -> p.Result[bool]:
            """Functional validation composition.

            Returns:
                The resulting ``p.Result[bool]``.

            """
            if not self.target.strip():
                return r[bool].fail("Channel target cannot be empty")
            return r[bool].ok(value=True)


__all__: list[str] = ["FlextGrpcModelsChannel"]
