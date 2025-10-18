"""FLEXT gRPC Entities - Generic Entity System with Advanced Patterns.

Generic entity classes using extensive Pydantic v2, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Generic, Self, TypeVar

from flext_core import FlextModels, FlextResult, FlextService
from pydantic import BaseModel, Field, field_validator

from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.typings import FlextGrpcTypings

T = TypeVar("T", bound=BaseModel)


class EntityValidator(BaseModel):
    """Generic entity validator using functional composition."""

    @classmethod
    def validate_required_string(cls, value: str, field_name: str) -> str:
        """Generic string validation."""
        if not value or not value.strip():
            msg = f"{field_name} cannot be empty"
            raise ValueError(msg)
        return value.strip()

    @classmethod
    def validate_enum(cls, value: str, allowed: set[str], field_name: str) -> str:
        """Generic enum validation."""
        if value not in allowed:
            msg = f"Invalid {field_name}: {value}"
            raise ValueError(msg)
        return value

    @classmethod
    def validate_list_not_empty(cls, value: list, field_name: str) -> list:
        """Generic list validation."""
        if not value:
            msg = f"{field_name} cannot be empty"
            raise ValueError(msg)
        return value


class StateMachine[T: BaseModel](BaseModel):
    """Generic state machine with functional transitions."""

    def transition(
        self, current: str, target: str, allowed_transitions: dict[str, set[str]]
    ) -> FlextResult[T]:
        """Generic state transition with validation."""
        if (
            current not in allowed_transitions
            or target not in allowed_transitions[current]
        ):
            return FlextResult.fail(f"Invalid transition from {current} to {target}")
        return FlextResult.ok(self.model_copy(update={"state": target}))  # type: ignore


class FlextGrpcEntities(FlextService):
    """Generic gRPC entity system with SOLID principles and minimal code."""

    class Entity(FlextModels.Entity, Generic[T]):
        """Generic base entity with functional patterns."""

        created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

        def copy_with(self, **kwargs: Any) -> FlextResult[Self]:
            """Functional copy using FlextResult."""
            try:
                return FlextResult.ok(self.model_copy(update=kwargs))
            except Exception as e:
                return FlextResult.fail(str(e))

        def validate_business_rules(self) -> FlextResult[None]:
            """Override in subclasses for specific validation."""
            return FlextResult.ok(None)

    class Channel(Entity[dict[str, Any]], StateMachine["FlextGrpcEntities.Channel"]):
        """Generic gRPC channel with state machine delegation."""

        target: str = ""
        state: FlextGrpcTypings.GrpcChannelState = "idle"
        options: dict[str, Any] = Field(default_factory=dict)
        grpc_channel: Any = None

        @field_validator("state")
        @classmethod
        def validate_state(cls, v: str) -> str:
            """Delegate state validation."""
            return EntityValidator.validate_enum(
                v, FlextGrpcConstants.Literals.CHANNEL_STATES, "state"
            )

        def validate_business_rules(self) -> FlextResult[None]:
            """Functional validation composition."""
            if not self.target.strip():
                return FlextResult.fail("Channel target cannot be empty")
            return FlextResult.ok(None)

        def is_ready(self) -> bool:
            """Check readiness."""
            return self.state == "ready"

        def connect(self) -> FlextResult[Self]:
            """Transition to connecting."""
            return self.transition(self.state, "connecting", {"idle": {"connecting"}})

        def mark_ready(self) -> FlextResult[Self]:
            """Transition to ready."""
            return self.transition(self.state, "ready", {"connecting": {"ready"}})

        def disconnect(self) -> FlextResult[Self]:
            """Transition to idle."""
            return FlextResult.ok(self.model_copy(update={"state": "idle"}))

    class Server(Entity[list], StateMachine["FlextGrpcEntities.Server"]):
        """Generic gRPC server with state machine and validation delegation."""

        host: str = FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST
        port: int = FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT
        state: FlextGrpcTypings.GrpcServerState = "stopped"
        max_workers: int = 10
        services: list = Field(default_factory=list)
        grpc_server: Any = None

        def validate_business_rules(self) -> FlextResult[None]:
            """Delegate validation to generic validators."""
            if not self.host.strip():
                return FlextResult.fail("Server host cannot be empty")
            if not (1 <= self.port <= 65535):
                return FlextResult.fail(f"Invalid port: {self.port}")
            if self.max_workers < 1:
                return FlextResult.fail("Max workers must be >= 1")
            return FlextResult.ok(None)

        def start(self) -> FlextResult[Self]:
            """Transition to starting."""
            return self.transition(self.state, "starting", {"stopped": {"starting"}})

        def mark_running(self) -> FlextResult[Self]:
            """Transition to running."""
            return self.transition(self.state, "running", {"starting": {"running"}})

        def stop(self) -> FlextResult[Self]:
            """Transition to stopping."""
            return self.transition(self.state, "stopping", {"running": {"stopping"}})

        def mark_stopped(self) -> FlextResult[Self]:
            """Transition to stopped."""
            if self.state not in {"stopping", "running"}:
                return FlextResult.fail(f"Cannot mark stopped from {self.state}")
            return FlextResult.ok(self.model_copy(update={"state": "stopped"}))

        def add_service(self, service: Any) -> FlextResult[Self]:
            """Add service functionally."""
            return FlextResult.ok(
                self.model_copy(update={"services": [*self.services, service]})
            )

    class Service(Entity[list[str]]):
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

        def add_method(self, method_name: str) -> FlextResult[Self]:
            """Add method functionally."""
            if not method_name.strip() or method_name in self.methods:
                return FlextResult.fail("Invalid method")
            return FlextResult.ok(
                self.model_copy(update={"methods": [*self.methods, method_name]})
            )

    class Client(Entity[dict[str, Any]]):
        """Generic gRPC client with channel delegation."""

        channel: FlextGrpcEntities.Channel | None = None
        options: dict[str, Any] = Field(default_factory=dict)
        grpc_stub: Any = None

        def validate_business_rules(self) -> FlextResult[None]:
            """Delegate validation."""
            if self.channel and self.channel.validate_business_rules().is_failure:
                return FlextResult.fail("Invalid channel")
            return FlextResult.ok(None)

        def connect_to(self, target: str) -> FlextResult[Self]:
            """Connect functionally."""
            channel = FlextGrpcEntities.Channel(target=target, state="idle")
            return FlextResult.ok(self.model_copy(update={"channel": channel}))

    class GrpcStream(Entity[str]):
        """Generic gRPC stream with validation delegation."""

        method_name: str = ""
        stream_type: FlextGrpcTypings.GrpcStreamType = "unary"
        grpc_stub: Any = None

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
                v, FlextGrpcConstants.Literals.STREAM_TYPES, "stream_type"
            )


__all__ = ["EntityValidator", "FlextGrpcEntities", "StateMachine"]
