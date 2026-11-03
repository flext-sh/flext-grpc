# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contracts.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_grpc/_protocols/runtime_models
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections import deque
from collections.abc import Sequence
from typing import TYPE_CHECKING, Protocol, Self, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_grpc._protocols import FlextGrpcProtocolsChannelModels

if TYPE_CHECKING:
    from flext_cli import p

    from flext_grpc import t
    from flext_grpc._constants import FlextGrpcConstantsBase
    from flext_grpc._protocols import (
        FlextGrpcProtocolsConnection,
        FlextGrpcProtocolsServer,
    )


class FlextGrpcProtocolsRuntimeModels:
    """Own the structural contracts declared by its model source."""

    @runtime_checkable
    class Server(
        FlextGrpcProtocolsChannelModels.Entity,
        FlextGrpcProtocolsChannelModels.StateMachine,
        Protocol,
    ):
        """Structural data contract projected from the owning model."""

        host: str
        port: t.PortNumber

        @property
        def state(self) -> FlextGrpcConstantsBase.ServerState:
            """Current server lifecycle state."""
            ...

        max_workers: t.WorkerCount

        @property
        def services(self) -> Sequence[FlextGrpcProtocolsServer.GrpcServicer]:
            """GRPC services."""
            ...

        @property
        def grpc_server(self) -> FlextGrpcProtocolsServer.GrpcServer | None:
            """Underlying gRPC server instance."""
            ...

        def add_service(
            self, service: FlextGrpcProtocolsServer.GrpcServicer
        ) -> p.Result[Self]:
            """Add a gRPC servicer to the server."""
            ...

        def mark_running(self) -> p.Result[Self]:
            """Transition to running."""
            ...

        def mark_stopped(self) -> p.Result[Self]:
            """Transition to stopped."""
            ...

        def start(self) -> p.Result[Self]:
            """Transition to starting."""
            ...

        def stop(self) -> p.Result[Self]:
            """Transition to stopping."""
            ...

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate the server host, port range, and worker bound."""
            ...

    @runtime_checkable
    class Service(FlextGrpcProtocolsChannelModels.Entity, Protocol):
        """Structural data contract projected from the owning model."""

        name: str
        methods: Sequence[str]

        def add_method(self, method_name: str) -> p.Result[Self]:
            """Add an RPC method name to the service."""
            ...

        def has_method(self, method_name: str) -> bool:
            """Check whether the method name is registered."""
            ...

    @runtime_checkable
    class Client(FlextGrpcProtocolsChannelModels.Entity, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def channel(self) -> FlextGrpcProtocolsChannelModels.Channel | None:
            """Associated gRPC channel for communication."""
            ...

        options: t.JsonMapping | None

        @property
        def grpc_stub(self) -> FlextGrpcProtocolsConnection.GrpcStub | None:
            """GRPC client stub for RPC calls."""
            ...

        def connect_to(self, target: str) -> p.Result[Self]:
            """Connect the client to the target by creating a channel."""
            ...

        def validate_business_rules(self) -> p.Result[bool]:
            """Validate the client business rules through its channel."""
            ...

    @runtime_checkable
    class GrpcStream(FlextGrpcProtocolsChannelModels.Entity, Protocol):
        """Structural data contract projected from the owning model."""

        id: str
        method_name: str

        @property
        def stream_type(self) -> FlextGrpcConstantsBase.GrpcOperations:
            """Stream communication pattern type."""
            ...

        @property
        def grpc_stub(self) -> FlextGrpcProtocolsConnection.GrpcStub | None:
            """GRPC stub used by this stream."""
            ...

    @runtime_checkable
    class StreamRuntimeState(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def stream(self) -> FlextGrpcProtocolsRuntimeModels.GrpcStream:
            """GRPC stream instance being tracked."""
            ...

        @property
        def created_at(self) -> float:
            """Stream creation timestamp in epoch seconds."""
            ...

        @property
        def buffer(self) -> deque[t.JsonMapping | None]:
            """Bounded message buffer for stream processing."""
            ...

    @runtime_checkable
    class CompleteSetup(FlextCliProtocols.BaseModel, Protocol):
        """Structural data contract projected from the owning model."""

        @property
        def server(self) -> FlextGrpcProtocolsRuntimeModels.Server:
            """Configured gRPC server instance."""
            ...

        @property
        def client(self) -> FlextGrpcProtocolsRuntimeModels.Client:
            """Configured gRPC client instance."""
            ...

        @property
        def service(self) -> FlextGrpcProtocolsRuntimeModels.Service:
            """Configured gRPC service definition."""
            ...

        target: str


__all__: list[str] = [
    "FlextGrpcProtocolsRuntimeModels",
]
