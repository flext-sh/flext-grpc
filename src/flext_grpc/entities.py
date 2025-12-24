"""FLEXT gRPC Entities - Generic Entity System with Patterns.

Generic entity classes using extensive Pydantic v2, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Self, TypeVar

from flext_core import r
from flext_core._models.entity import FlextModelsEntity
from flext_core.models import FlextModels
from pydantic import BaseModel, Field, field_validator

from flext_grpc.constants import c
from flext_grpc.models import FlextGrpcModels
from flext_grpc.typings import t

# Import entity helpers from models.py (centralized location)
_m = FlextGrpcModels
EntityValidator = _m.Entities.EntityValidator
StateMachine = _m.Entities.StateMachine

# Rebuild parent model to resolve forward references before extending
FlextModels.Entity.model_rebuild()

T = TypeVar("T", bound=BaseModel)


class FlextGrpcEntities:
    """Generic gRPC entity system with SOLID principles and minimal code."""

    class Entity(FlextModelsEntity.Entry):
        """Generic base entity with functional patterns."""

        created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

        def copy_with(self, **kwargs: str | int | bool | None) -> r[Self]:
            """Functional copy using r.

            Args:
            **kwargs: Field updates for the entity

            """
            try:
                return r.ok(self.model_copy(update=kwargs))
            except Exception as e:
                return r.fail(str(e))

        def validate_business_rules(self) -> r[bool]:
            """Override in subclasses for specific validation."""
            return r.ok(True)

    class Channel(Entity, StateMachine):
        """Generic gRPC channel with state machine delegation."""

        target: str = ""
        state: t.GrpcChannelState = c.Grpc.ChannelState.IDLE
        options: dict[str, object] = Field(default_factory=dict)
        grpc_channel: object = None

        @field_validator("state")
        @classmethod
        def validate_state(cls, v: str) -> str:
            """Delegate state validation."""
            return EntityValidator.validate_enum(
                v,
                set(c.Grpc.CHANNEL_STATES),
                "state",
            )

        def validate_business_rules(self) -> r[bool]:
            """Functional validation composition."""
            if not self.target.strip():
                return r.fail("Channel target cannot be empty")
            return r.ok(True)

        def is_ready(self) -> bool:
            """Check readiness."""
            return self.state == "ready"

        def connect(self) -> r[Self]:
            """Transition to connecting."""
            return self.transition(self.state, "connecting", {"idle": {"connecting"}})

        def mark_ready(self) -> r[Self]:
            """Transition to ready."""
            return self.transition(self.state, "ready", {"connecting": {"ready"}})

        def disconnect(self) -> r[Self]:
            """Transition to idle."""
            return r.ok(self.model_copy(update={"state": c.Grpc.ChannelState.IDLE}))

    class Server(Entity, StateMachine):
        """Generic gRPC server with state machine and validation delegation."""

        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT
        state: t.GrpcServerState = c.Grpc.ServerState.STOPPED
        max_workers: int = 10
        services: list[object] = Field(default_factory=list)
        grpc_server: object = None

        def validate_business_rules(self) -> r[bool]:
            """Delegate validation to generic validators."""
            if not self.host.strip():
                return r.fail("Server host cannot be empty")
            # Port range validation using IANA standard range
            min_port = 1
            max_port = 65535
            if not (min_port <= self.port <= max_port):
                return r.fail(f"Invalid port: {self.port}")
            if self.max_workers < 1:
                return r.fail("Max workers must be >= 1")
            return r.ok(True)

        def start(self) -> r[Self]:
            """Transition to starting."""
            return self.transition(self.state, "starting", {"stopped": {"starting"}})

        def mark_running(self) -> r[Self]:
            """Transition to running."""
            return self.transition(self.state, "running", {"starting": {"running"}})

        def stop(self) -> r[Self]:
            """Transition to stopping."""
            return self.transition(self.state, "stopping", {"running": {"stopping"}})

        def mark_stopped(self) -> r[Self]:
            """Transition to stopped."""
            if self.state not in {"stopping", "running"}:
                return r.fail(f"Cannot mark stopped from {self.state}")
            return r.ok(self.model_copy(update={"state": c.Grpc.ServerState.STOPPED}))

        def add_service(self, service: object) -> r[Self]:
            """Add service functionally.

            Args:
            service: gRPC service object (dynamic type from grpc library)

            """
            return r.ok(
                self.model_copy(update={"services": [*self.services, service]}),
            )

    class Service(Entity):
        """Generic gRPC service with validation delegation."""

        name: str = ""
        methods: list[str] = Field(default_factory=list)

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Delegate name validation."""
            return EntityValidator.validate_required_string(v, "name")

        @field_validator("methods")
        @classmethod
        def validate_methods(cls, v: list[str]) -> list[str]:
            """Delegate methods validation."""
            EntityValidator.validate_list_not_empty(v, "methods")
            for method in v:
                EntityValidator.validate_required_string(method, "method")
            return v

        def has_method(self, method_name: str) -> bool:
            """Check method existence."""
            return method_name in self.methods

        def add_method(self, method_name: str) -> r[Self]:
            """Add method functionally."""
            if not method_name.strip() or method_name in self.methods:
                return r.fail("Invalid method")
            return r.ok(
                self.model_copy(update={"methods": [*self.methods, method_name]}),
            )

    class Client(Entity):
        """Generic gRPC client with channel delegation."""

        channel: FlextGrpcEntities.Channel | None = None
        options: dict[str, object] = Field(default_factory=dict)
        grpc_stub: object = None

        def validate_business_rules(self) -> r[bool]:
            """Delegate validation."""
            if self.channel and self.channel.validate_business_rules().is_failure:
                return r.fail("Invalid channel")
            return r.ok(True)

        def connect_to(self, target: str) -> r[Self]:
            """Connect functionally."""
            channel = FlextGrpcEntities.Channel(
                target=target,
                state=c.Grpc.ChannelState.IDLE,
            )
            return r.ok(self.model_copy(update={"channel": channel}))

    class GrpcStream(Entity):
        """Generic gRPC stream with validation delegation."""

        id: str = ""
        method_name: str = ""
        stream_type: t.GrpcStreamType = c.Grpc.GrpcOperations.UNARY
        grpc_stub: object = None

        @field_validator("method_name")
        @classmethod
        def validate_method_name(cls, v: str) -> str:
            """Delegate method name validation."""
            return EntityValidator.validate_required_string(v, "method_name")

        @field_validator("stream_type")
        @classmethod
        def validate_stream_type(cls, v: str) -> str:
            """Delegate stream type validation."""
            return EntityValidator.validate_enum(
                v,
                set(c.Grpc.STREAM_TYPES),
                "stream_type",
            )


__all__ = ["EntityValidator", "FlextGrpcEntities", "StateMachine"]
