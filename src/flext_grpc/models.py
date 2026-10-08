"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections import deque
from datetime import datetime
from types import MappingProxyType
from typing import Annotated, Self, override

from flext_cli import FlextCliModels

from flext_core import r
from flext_grpc import c, p, t
from flext_grpc._models import FlextGrpcConfigModels, FlextGrpcModelsBase


class FlextGrpcModels(FlextCliModels):
    """gRPC domain models extending flext-core m.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Grpc(FlextGrpcConfigModels, FlextGrpcModelsBase):
        """Domain models for gRPC core business entities."""

        # =========================================================================
        # PROTO MESSAGE MODELS - RPC request/response messages
        # =========================================================================

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
            ) -> p.Result[FlextGrpcModels.Grpc.StateTransition]:
                """Perform a generic state transition with validation.

                Args:
                    current: Current state
                    target: Target state
                    allowed_transitions: Map of allowed transitions

                Returns:
                    r with state update dict on success

                """
                if (
                    current not in allowed_transitions
                    or target not in allowed_transitions[current]
                ):
                    return r[FlextGrpcModels.Grpc.StateTransition].fail(
                        f"Invalid transition from {current} to {target}",
                    )
                return r[FlextGrpcModels.Grpc.StateTransition].ok(
                    FlextGrpcModels.Grpc.StateTransition(state=target),
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

            operation: FlextGrpcModels.Grpc.OperationSpec = FlextCliModels.Field(
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

        class Payload(FlextCliModels.BaseModel):
            """Structured payload model replacing ad-hoc dict responses."""

            values: t.JsonMapping = FlextCliModels.Field(
                default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
                description="Key-value payload data",
            )

            @classmethod
            def from_values(cls, **values: t.JsonPayload | None) -> Self:
                """Build payload from keyword values.

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

        class Entity(FlextCliModels.Entity):
            """Generic base entity with functional patterns."""

            def copy_with(self, **kwargs: t.Scalar | None) -> p.Result[Self]:
                """Functional copy using r.

                Args:
                **kwargs: u.Field updates for the entity

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                return r[Self].create_from_callable(
                    lambda: self.model_copy(update=kwargs),
                )

            def validate_business_rules(self) -> p.Result[bool]:
                """Override in subclasses for specific validation.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                return r[bool].ok(value=True)

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
                p.Grpc.GrpcChannel | None,
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

            @override
            def validate_business_rules(self) -> p.Result[bool]:
                """Functional validation composition.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                if not self.target.strip():
                    return r[bool].fail("Channel target cannot be empty")
                return r[bool].ok(value=True)

        class Server(Entity, StateMachine):
            """Generic gRPC server with state machine and validation delegation."""

            host: Annotated[
                str,
                FlextCliModels.Field(description="Server bind host address"),
            ] = c.Grpc.NETWORK_DEFAULT_HOST
            port: Annotated[
                t.PortNumber,
                FlextCliModels.Field(description="Server listen port number"),
            ] = c.Grpc.NETWORK_DEFAULT_GRPC_PORT
            state: Annotated[
                c.Grpc.ServerState,
                FlextCliModels.Field(description="Current server lifecycle state"),
            ] = c.Grpc.ServerState.STOPPED
            max_workers: Annotated[
                t.WorkerCount,
                FlextCliModels.Field(
                    description="Maximum worker threads for request handling",
                ),
            ] = c.Grpc.SERVICE_DEFAULT_MAX_WORKERS
            services: Annotated[
                t.SequenceOf[p.Grpc.GrpcServicer],
                FlextCliModels.Field(description="gRPC services"),
            ] = FlextCliModels.Field(default_factory=tuple)
            grpc_server: Annotated[
                p.Grpc.GrpcServer | None,
                FlextCliModels.Field(description="Underlying gRPC server instance"),
            ] = None

            def add_service(self, service: p.Grpc.GrpcServicer) -> p.Result[Self]:
                """Add service functionally.

                Args:
                service: gRPC service t.JsonValue (dynamic type from grpc library)

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                return r[Self].ok(
                    self.model_copy(
                        update={"services": [*self.services, service]},
                    ),
                )

            def mark_running(self) -> p.Result[Self]:
                """Transition to running.

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                return self.transition(
                    self.state,
                    "running",
                    {"starting": {"running"}},
                ).map(lambda update: self.model_copy(update={"state": update.state}))

            def mark_stopped(self) -> p.Result[Self]:
                """Transition to stopped.

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                if self.state not in {"stopping", "running"}:
                    return (
                        r[Self]
                        .fail(f"Cannot mark stopped from {self.state}")
                        .map(lambda _unused: self)
                    )
                return r[Self].ok(
                    self.model_copy(
                        update={"state": c.Grpc.ServerState.STOPPED.value},
                    ),
                )

            def start(self) -> p.Result[Self]:
                """Transition to starting.

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                return self.transition(
                    self.state,
                    "starting",
                    {"stopped": {"starting"}},
                ).map(lambda update: self.model_copy(update={"state": update.state}))

            def stop(self) -> p.Result[Self]:
                """Transition to stopping.

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                return self.transition(
                    self.state,
                    "stopping",
                    {"running": {"stopping"}},
                ).map(lambda update: self.model_copy(update={"state": update.state}))

            @override
            def validate_business_rules(self) -> p.Result[bool]:
                """Delegate validation to generic validators.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                if not self.host.strip():
                    return r[bool].fail("Server host cannot be empty")
                # Port range validation using IANA standard range
                min_port = 1
                max_port = 65535
                if not (min_port <= self.port <= max_port):
                    return r[bool].fail(f"Invalid port: {self.port}")
                if self.max_workers < 1:
                    return r[bool].fail("Max workers must be >= 1")
                return r[bool].ok(value=True)

        class Service(Entity):
            """Generic gRPC service with validation delegation."""

            name: Annotated[
                str,
                FlextCliModels.Field(description="Service name identifier"),
            ] = ""
            methods: t.StrSequence = FlextCliModels.Field(
                default_factory=tuple[str, ...],
                description="Registered RPC method names",
            )

            @FlextCliModels.field_validator("methods")
            @classmethod
            def validate_methods(cls, v: t.StrSequence) -> t.StrSequence:
                """Validate methods list is not empty with valid items.

                Returns:
                    The resulting ``t.StrSequence``.

                Raises:
                    ValueError: If methods cannot be empty; or if method cannot be
                        empty.
                """
                if not v:
                    msg = "methods cannot be empty"
                    raise ValueError(msg)
                for method in v:
                    if not method or not method.strip():
                        msg = "method cannot be empty"
                        raise ValueError(msg)
                return v

            @FlextCliModels.field_validator("name")
            @classmethod
            def validate_name(cls, v: str) -> str:
                """Validate name is not empty or whitespace.

                Returns:
                    The resulting ``str``.

                Raises:
                    ValueError: If name cannot be empty.
                """
                if not v or not v.strip():
                    msg = "name cannot be empty"
                    raise ValueError(msg)
                return v

            def add_method(self, method_name: str) -> p.Result[Self]:
                """Add method functionally.

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                if not method_name.strip() or method_name in self.methods:
                    return r[Self].fail("Invalid method").map(lambda _unused: self)
                return r[Self].ok(
                    self.model_copy(
                        update={"methods": [*self.methods, method_name]},
                    ),
                )

            def has_method(self, method_name: str) -> bool:
                """Check method existence.

                Returns:
                    The resulting ``bool``.
                """
                return method_name in self.methods

        class Client(Entity):
            """Generic gRPC client with channel delegation."""

            channel: Annotated[
                FlextGrpcModels.Grpc.Channel | None,
                FlextCliModels.Field(
                    description="Associated gRPC channel for communication",
                ),
            ] = None
            options: t.JsonMapping | None = FlextCliModels.Field(
                default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
                description="Client configuration options",
            )
            grpc_stub: Annotated[
                p.Grpc.GrpcStub | None,
                FlextCliModels.Field(description="gRPC client stub for RPC calls"),
            ] = None

            def connect_to(self, target: str) -> p.Result[Self]:
                """Connect functionally.

                Returns:
                    The resulting ``p.Result[Self]``.
                """
                channel = FlextGrpcModels.Grpc.Channel(
                    target=target,
                    state=c.Grpc.ChannelState.IDLE,
                    options={},
                    domain_events=[],
                )
                return r[Self].ok(
                    self.model_copy(update={"channel": channel}),
                )

            @override
            def validate_business_rules(self) -> p.Result[bool]:
                """Delegate validation.

                Returns:
                    The resulting ``p.Result[bool]``.
                """
                if self.channel and self.channel.validate_business_rules().failure:
                    return r[bool].fail("Invalid channel")
                return r[bool].ok(value=True)

        class GrpcStream(Entity):
            """Generic gRPC stream with validation delegation."""

            id: Annotated[
                str,
                FlextCliModels.Field(description="Unique stream identifier"),
            ] = ""
            method_name: Annotated[
                str,
                FlextCliModels.Field(description="RPC method name for this stream"),
            ] = ""
            stream_type: Annotated[
                c.Grpc.GrpcOperations,
                FlextCliModels.Field(description="Stream communication pattern type"),
            ] = c.Grpc.GrpcOperations.UNARY
            grpc_stub: Annotated[
                p.Grpc.GrpcStub | None,
                FlextCliModels.Field(description="gRPC stub used by this stream"),
            ] = None

            @FlextCliModels.field_validator("method_name")
            @classmethod
            def validate_method_name(cls, v: str) -> str:
                """Validate method_name is not empty or whitespace.

                Returns:
                    The resulting ``str``.

                Raises:
                    ValueError: If method_name cannot be empty.
                """
                if not v or not v.strip():
                    msg = "method_name cannot be empty"
                    raise ValueError(msg)
                return v

        class StreamRuntimeState(FlextCliModels.Value):
            """Bounded runtime state tracked for one open gRPC stream."""

            stream: FlextGrpcModels.Grpc.GrpcStream = FlextCliModels.Field(
                description="gRPC stream instance being tracked",
            )
            created_at: float = FlextCliModels.Field(
                description="Stream creation timestamp in epoch seconds",
            )
            buffer: deque[t.JsonMapping | None] = FlextCliModels.Field(
                default_factory=lambda: deque[t.JsonMapping | None](
                    maxlen=c.Grpc.STREAMING_DEFAULT_BUFFER_SIZE,
                ),
                description="Bounded message buffer for stream processing",
            )

        class CompleteSetup(FlextCliModels.BaseModel):
            """Complete gRPC setup result with server, client, and service."""

            server: FlextGrpcModels.Grpc.Server = FlextCliModels.Field(
                description="Configured gRPC server instance",
            )
            client: FlextGrpcModels.Grpc.Client = FlextCliModels.Field(
                description="Configured gRPC client instance",
            )
            service: FlextGrpcModels.Grpc.Service = FlextCliModels.Field(
                description="Configured gRPC service definition",
            )
            target: str = FlextCliModels.Field(
                description="Target server address for the setup",
            )


m = FlextGrpcModels

__all__: list[str] = ["FlextGrpcModels", "m"]
