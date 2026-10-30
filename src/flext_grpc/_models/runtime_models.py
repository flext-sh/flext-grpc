"""FLEXT gRPC server, client and stream runtime models.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from types import MappingProxyType
from typing import Annotated, Self

from flext_cli import FlextCliModels

from flext_grpc import c, p, r, t
from flext_grpc._models import FlextGrpcModelsChannel


class FlextGrpcModelsRuntime:
    """gRPC runtime models composed into ``m.Grpc``."""

    class Server(FlextGrpcModelsChannel.Entity, FlextGrpcModelsChannel.StateMachine):
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
            Sequence[t.Port[p.Grpc.GrpcServicer]],
            FlextCliModels.Field(description="gRPC services"),
        ] = FlextCliModels.Field(default_factory=tuple)
        grpc_server: Annotated[
            t.Port[p.Grpc.GrpcServer] | None,
            FlextCliModels.Field(description="Underlying gRPC server instance"),
        ] = None

        def add_service(self, service: p.Grpc.GrpcServicer) -> p.Result[Self]:
            """Add a gRPC servicer to the server.

            Args:
                service: gRPC servicer to register on the server.

            Returns:
                Result wrapping the server with the service added.

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
                return r[Self].fail(f"Cannot mark stopped from {self.state}")
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

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate the server host, port range, and worker bound.

            Returns:
                Result holding the validation verdict.

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

    class Service(FlextGrpcModelsChannel.Entity):
        """Generic gRPC service with validation delegation."""

        name: Annotated[
            str,
            FlextCliModels.Field(description="Service name identifier"),
        ] = ""
        methods: Sequence[str] = FlextCliModels.Field(
            default_factory=tuple[str, ...],
            description="Registered RPC method names",
        )

        @FlextCliModels.field_validator("methods")
        @classmethod
        def validate_methods(cls, v: Sequence[str]) -> Sequence[str]:
            """Validate methods list is not empty with valid items.

            Args:
                v: Methods sequence candidate.

            Returns:
                The validated methods sequence.

            Raises:
                ValueError: If the methods list is empty or a method is
                    blank.

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

            Args:
                v: Name candidate.

            Returns:
                The validated name.

            Raises:
                ValueError: If the name is empty or whitespace.

            """
            if not v or not v.strip():
                msg = "name cannot be empty"
                raise ValueError(msg)
            return v

        def add_method(self, method_name: str) -> p.Result[Self]:
            """Add an RPC method name to the service.

            Args:
                method_name: Method name to register.

            Returns:
                Result wrapping the service with the method added, or a
                failure result for blank or duplicate names.

            """
            if not method_name.strip() or method_name in self.methods:
                return r[Self].fail("Invalid method")
            return r[Self].ok(
                self.model_copy(
                    update={"methods": [*self.methods, method_name]},
                ),
            )

        def has_method(self, method_name: str) -> bool:
            """Check whether the method name is registered.

            Args:
                method_name: Method name to look up.

            Returns:
                ``True`` when the method name is registered.

            """
            return method_name in self.methods

    class Client(FlextGrpcModelsChannel.Entity):
        """Generic gRPC client with channel delegation."""

        channel: Annotated[
            FlextGrpcModelsChannel.Channel | None,
            FlextCliModels.Field(
                description="Associated gRPC channel for communication",
            ),
        ] = None
        options: t.JsonMapping | None = FlextCliModels.Field(
            default_factory=lambda: MappingProxyType[str, t.JsonValue]({}),
            description="Client configuration options",
        )
        grpc_stub: Annotated[
            t.Port[p.Grpc.GrpcStub] | None,
            FlextCliModels.Field(description="gRPC client stub for RPC calls"),
        ] = None

        def connect_to(self, target: str) -> p.Result[Self]:
            """Connect the client to the target by creating a channel.

            Args:
                target: gRPC server target address.

            Returns:
                Result wrapping the client with the channel attached.

            """
            channel = FlextGrpcModelsChannel.Channel(
                target=target,
                state=c.Grpc.ChannelState.IDLE,
                options={},
                domain_events=[],
            )
            return r[Self].ok(
                self.model_copy(update={"channel": channel}),
            )

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate the client business rules through its channel.

            Returns:
                Result holding the validation verdict.

            """
            if self.channel and self.channel.validate_business_rules().failure:
                return r[bool].fail("Invalid channel")
            return r[bool].ok(value=True)

    class GrpcStream(FlextGrpcModelsChannel.Entity):
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
            t.Port[p.Grpc.GrpcStub] | None,
            FlextCliModels.Field(description="gRPC stub used by this stream"),
        ] = None

        @FlextCliModels.field_validator("method_name")
        @classmethod
        def validate_method_name(cls, v: str) -> str:
            """Validate method_name is not empty or whitespace.

            Args:
                v: Method name candidate.

            Returns:
                The validated method name.

            Raises:
                ValueError: If method_name is empty or whitespace.

            """
            if not v or not v.strip():
                msg = "method_name cannot be empty"
                raise ValueError(msg)
            return v

    class StreamRuntimeState(FlextCliModels.Value):
        """Bounded runtime state tracked for one open gRPC stream."""

        stream: FlextGrpcModelsRuntime.GrpcStream = FlextCliModels.Field(
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

        server: FlextGrpcModelsRuntime.Server = FlextCliModels.Field(
            description="Configured gRPC server instance",
        )
        client: FlextGrpcModelsRuntime.Client = FlextCliModels.Field(
            description="Configured gRPC client instance",
        )
        service: FlextGrpcModelsRuntime.Service = FlextCliModels.Field(
            description="Configured gRPC service definition",
        )
        target: str = FlextCliModels.Field(
            description="Target server address for the setup",
        )


__all__: list[str] = ["FlextGrpcModelsRuntime"]
