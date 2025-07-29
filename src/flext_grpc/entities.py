"""FLEXT gRPC Domain Entities - Core domain entities using flext-core patterns.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_core import (
    FlextComparableMixin,
    FlextEntity,
    FlextEntityFactory,
    FlextResult,
)
from pydantic import Field

from flext_grpc.constants import FLEXT_GRPC_MAX_PORT, FLEXT_GRPC_MIN_PORT
from flext_grpc.types import (
    TGrpcChannelState,
    TGrpcServerState,
    TGrpcStreamType,
    TGrpcTarget,
)


class FlextGrpcEntity(FlextEntity, FlextComparableMixin):
    """Base gRPC entity with common behavior."""

    @property
    def entity_type(self) -> str:
        """Get entity type name."""
        return self.__class__.__name__


class FlextGrpcChannel(FlextGrpcEntity):
    """gRPC channel entity with connection management."""

    target: TGrpcTarget = TGrpcTarget("")
    state: TGrpcChannelState = "idle"
    options: dict[str, object] = Field(default_factory=dict)

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate channel domain rules."""
        if not self.target or not str(self.target).strip():
            return FlextResult.fail("Channel target cannot be empty")

        valid_states = {"idle", "connecting", "ready", "transient_failure", "shutdown"}
        if self.state not in valid_states:
            return FlextResult.fail(f"Invalid channel state: {self.state}")
        return FlextResult.ok(None)

    def is_ready(self) -> bool:
        """Check if channel is ready for communication."""
        return self.state == "ready"

    def connect(self) -> FlextResult[FlextGrpcChannel]:
        """Connect the channel."""
        if self.state != "idle":
            return FlextResult.fail(f"Cannot connect from state: {self.state}")
        return self.copy_with(state="connecting")

    def mark_ready(self) -> FlextResult[FlextGrpcChannel]:
        """Mark channel as ready."""
        if self.state != "connecting":
            return FlextResult.fail(f"Cannot mark ready from state: {self.state}")
        return self.copy_with(state="ready")

    def disconnect(self) -> FlextResult[FlextGrpcChannel]:
        """Disconnect the channel."""
        return self.copy_with(state="idle")


class FlextGrpcServer(FlextGrpcEntity):
    """gRPC server entity with lifecycle management."""

    host: str = "localhost"
    port: int = 50051
    state: TGrpcServerState = "stopped"
    max_workers: int = 10
    services: list[object] = Field(default_factory=list)

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate server domain rules."""
        if not self.host or not self.host.strip():
            return FlextResult.fail("Server host cannot be empty")

        if not (FLEXT_GRPC_MIN_PORT <= self.port <= FLEXT_GRPC_MAX_PORT):
            return FlextResult.fail(
                f"Invalid port: {self.port} "
                f"(must be {FLEXT_GRPC_MIN_PORT}-{FLEXT_GRPC_MAX_PORT})",
            )

        if self.max_workers < 1:
            return FlextResult.fail("Max workers must be >= 1")

        if self.state not in {"stopped", "starting", "running", "stopping"}:
            return FlextResult.fail(f"Invalid server state: {self.state}")
        return FlextResult.ok(None)

    @property
    def address(self) -> str:
        """Get server address as host:port."""
        return f"{self.host}:{self.port}"

    @property
    def is_running(self) -> bool:
        """Check if server is running."""
        return self.state == "running"

    def start(self) -> FlextResult[FlextGrpcServer]:
        """Start the server."""
        if self.state in {"running", "starting"}:
            return FlextResult.fail(f"Server already {self.state}")
        return self.copy_with(state="starting")

    def mark_running(self) -> FlextResult[FlextGrpcServer]:
        """Mark server as running."""
        if self.state != "starting":
            return FlextResult.fail(f"Cannot mark running from state: {self.state}")
        return self.copy_with(state="running")

    def stop(self) -> FlextResult[FlextGrpcServer]:
        """Stop the server."""
        if self.state in {"stopped", "stopping"}:
            return FlextResult.fail(f"Server already {self.state}")
        return self.copy_with(state="stopping")

    def mark_stopped(self) -> FlextResult[FlextGrpcServer]:
        """Mark server as stopped."""
        if self.state not in {"stopping", "running"}:
            return FlextResult.fail(f"Cannot mark stopped from state: {self.state}")
        return self.copy_with(state="stopped")

    def add_service(self, service: FlextGrpcService) -> FlextResult[FlextGrpcServer]:
        """Add a service to the server."""
        for existing_service in self.services:
            if (
                hasattr(existing_service, "name")
                and existing_service.name == service.name
            ):
                return FlextResult.fail("Service already exists")

        return self.copy_with(services=[*self.services, service])


class FlextGrpcService(FlextGrpcEntity):
    """gRPC service entity with method definitions."""

    name: str = ""
    methods: list[str] = Field(default_factory=list)

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate service domain rules."""
        if not self.name or not self.name.strip():
            return FlextResult.fail("Service name cannot be empty")

        if not self.methods:
            return FlextResult.fail("Service must have at least one method")

        for method in self.methods:
            if not method or not method.strip():
                return FlextResult.fail("Method name cannot be empty")

        return FlextResult.ok(None)

    def has_method(self, method_name: str) -> bool:
        """Check if service has the specified method."""
        return method_name in self.methods

    def add_method(self, method_name: str) -> FlextResult[FlextGrpcService]:
        """Add a method to the service."""
        if not method_name or not method_name.strip():
            return FlextResult.fail("Method name cannot be empty")

        if method_name in self.methods:
            return FlextResult.fail("Method already exists")

        return self.copy_with(methods=[*self.methods, method_name])


class FlextGrpcClient(FlextGrpcEntity):
    """gRPC client entity with channel management."""

    channel: FlextGrpcChannel | None = None
    options: dict[str, object] = Field(default_factory=dict)

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate client domain rules."""
        if self.channel is not None:
            channel_validation = self.channel.validate_domain_rules()
            if channel_validation.is_failure:
                return FlextResult.fail(f"Invalid channel: {channel_validation.error}")
        return FlextResult.ok(None)

    @property
    def is_connected(self) -> bool:
        """Check if client is connected."""
        return bool(self.channel and self.channel.is_ready())

    @property
    def target(self) -> str | None:
        """Get the target address."""
        return self.channel.target if self.channel else None

    def connect_to(self, target: str) -> FlextResult[FlextGrpcClient]:
        """Connect client to a target."""
        channel_result = FlextGrpcEntityFactory.create_channel(target)
        if channel_result.is_failure:
            return FlextResult.fail(channel_result.error or "Channel creation failed")

        return self.copy_with(channel=channel_result.data)


class FlextGrpcStream(FlextGrpcEntity):
    """gRPC stream entity for streaming operations."""

    method_name: str = ""
    stream_type: TGrpcStreamType = "unary"

    def validate_domain_rules(self) -> FlextResult[None]:
        """Validate stream domain rules."""
        if not self.method_name or not self.method_name.strip():
            return FlextResult.fail("Stream method name cannot be empty")

        valid_types = {"unary", "server_streaming", "client_streaming", "bidirectional"}
        if self.stream_type not in valid_types:
            return FlextResult.fail(f"Invalid stream type: {self.stream_type}")
        return FlextResult.ok(None)

    @property
    def is_streaming(self) -> bool:
        """Check if this is a streaming operation."""
        return self.stream_type != "unary"

    @property
    def is_server_streaming(self) -> bool:
        """Check if this is server streaming."""
        return self.stream_type in {"server_streaming", "bidirectional"}

    @property
    def is_client_streaming(self) -> bool:
        """Check if this is client streaming."""
        return self.stream_type in {"client_streaming", "bidirectional"}

    @property
    def is_bidirectional(self) -> bool:
        """Check if this is bidirectional streaming."""
        return self.stream_type == "bidirectional"


class FlextGrpcEntityFactory:
    """Factory for creating gRPC entities with validation."""

    # Create factory functions for each entity type
    _server_factory: object = FlextEntityFactory.create_entity_factory(
        FlextGrpcServer,
        defaults={
            "state": "stopped",
            "services": [],
            "host": "localhost",
            "port": 50051,
            "max_workers": 10,
        },
    )

    _client_factory: object = FlextEntityFactory.create_entity_factory(
        FlextGrpcClient,
        defaults={"options": {}},
    )

    _channel_factory: object = FlextEntityFactory.create_entity_factory(
        FlextGrpcChannel,
        defaults={"state": "idle", "options": {}},
    )

    _service_factory: object = FlextEntityFactory.create_entity_factory(
        FlextGrpcService,
        defaults={"methods": []},
    )

    _stream_factory: object = FlextEntityFactory.create_entity_factory(
        FlextGrpcStream,
        defaults={"stream_type": "unary"},
    )

    @classmethod
    def create_server(
        cls,
        host: str = "localhost",
        port: int = 50051,
        max_workers: int = 10,
        **options: object,
    ) -> FlextResult[FlextGrpcServer]:
        """Create a validated gRPC server."""
        return cls._server_factory(
            host=host,
            port=port,
            max_workers=max_workers,
            **options,
        )

    @classmethod
    def create_client(
        cls,
        target: str,
        **options: object,
    ) -> FlextResult[FlextGrpcClient]:
        """Create a validated gRPC client."""
        channel_result = cls.create_channel(target)
        if channel_result.is_failure:
            return FlextResult.fail(f"Failed to create client: {channel_result.error}")

        return cls._client_factory(
            channel=channel_result.data,
            options=options,
        )

    @classmethod
    def create_channel(
        cls,
        target: str,
        **options: object,
    ) -> FlextResult[FlextGrpcChannel]:
        """Create a validated gRPC channel."""
        return cls._channel_factory(
            target=TGrpcTarget(target),
            options=options,
        )

    @classmethod
    def create_service(
        cls,
        name: str,
        methods: list[str] | None = None,
        **options: object,
    ) -> FlextResult[FlextGrpcService]:
        """Create a validated gRPC service."""
        return cls._service_factory(
            name=name,
            methods=methods or [],
            **options,
        )

    @classmethod
    def create_stream(
        cls,
        method_name: str,
        stream_type: str = "unary",
        **options: object,
    ) -> FlextResult[FlextGrpcStream]:
        """Create a validated gRPC stream."""
        return cls._stream_factory(
            method_name=method_name,
            stream_type=stream_type,
            **options,
        )
