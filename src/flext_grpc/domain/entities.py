"""FLEXT gRPC Domain Entities - Core gRPC business entities.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

Core domain entities for gRPC communication system.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum
from typing import Any

from flext_core import FlextEntity, FlextEntityId

# Constants for magic numbers
MAX_PORT_NUMBER = 65535


class GrpcChannelState(Enum):
    """gRPC channel state enumeration."""

    IDLE = "idle"
    CONNECTING = "connecting"
    READY = "ready"
    TRANSIENT_FAILURE = "transient_failure"
    SHUTDOWN = "shutdown"


class GrpcServerState(Enum):
    """gRPC server state enumeration."""

    STOPPED = "stopped"
    STARTING = "starting"
    RUNNING = "running"
    STOPPING = "stopping"
    ERROR = "error"


class FlextGrpcChannel(FlextEntity):
    """gRPC channel entity representing a connection to a gRPC server."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        target: str = "",
        options: dict[str, Any] | None = None,
        state: GrpcChannelState = GrpcChannelState.IDLE,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize gRPC channel entity.

        Args:
            entity_id: Unique entity identifier
            target: gRPC server target address
            options: Channel options
            state: Channel state
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.target = target
        self.options = options or {}
        self.state = state
        self.created_at = created_at or datetime.now(UTC)

    def is_valid(self) -> bool:
        """Validate gRPC channel entity state.

        Returns:
            True if channel is valid, False otherwise

        """
        return bool(self.target)

    def is_ready(self) -> bool:
        """Check if channel is ready for communication.

        Returns:
            True if channel is ready, False otherwise

        """
        return self.state == GrpcChannelState.READY

    def connect(self) -> bool:
        """Mark channel as connecting.

        Returns:
            True if state change successful, False otherwise

        """
        if self.state == GrpcChannelState.IDLE:
            self.state = GrpcChannelState.CONNECTING
            return True
        return False

    def mark_ready(self) -> bool:
        """Mark channel as ready.

        Returns:
            True if state change successful, False otherwise

        """
        if self.state == GrpcChannelState.CONNECTING:
            self.state = GrpcChannelState.READY
            return True
        return False

    def disconnect(self) -> bool:
        """Mark channel as shutdown.

        Returns:
            True if state change successful, False otherwise

        """
        if self.state in {GrpcChannelState.READY, GrpcChannelState.CONNECTING}:
            self.state = GrpcChannelState.SHUTDOWN
            return True
        return False


class FlextGrpcService(FlextEntity):
    """gRPC service entity representing a registered service."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        name: str = "",
        methods: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize gRPC service entity.

        Args:
            entity_id: Unique entity identifier
            name: Service name
            methods: List of service methods
            metadata: Service metadata
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.name = name
        self.methods = methods or []
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now(UTC)

    def is_valid(self) -> bool:
        """Validate gRPC service entity state.

        Returns:
            True if service is valid, False otherwise

        """
        return bool(self.name and self.methods)

    def has_method(self, method_name: str) -> bool:
        """Check if service has a specific method.

        Args:
            method_name: Name of method to check

        Returns:
            True if service has the method, False otherwise

        """
        return method_name in self.methods

    def add_method(self, method_name: str) -> bool:
        """Add a method to the service.

        Args:
            method_name: Name of method to add

        Returns:
            True if method was added, False if already exists

        """
        if method_name not in self.methods:
            self.methods.append(method_name)
            return True
        return False


class FlextGrpcServer(FlextEntity):
    """gRPC server entity representing a gRPC server instance."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        host: str = "localhost",
        port: int = 50051,
        services: list[FlextGrpcService] | None = None,
        state: GrpcServerState = GrpcServerState.STOPPED,
        options: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize gRPC server entity.

        Args:
            entity_id: Unique entity identifier
            host: Server host address
            port: Server port
            services: List of registered services
            state: Server state
            options: Server options
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.host = host
        self.port = port
        self.services = services or []
        self.state = state
        self.options = options or {}
        self.created_at = created_at or datetime.now(UTC)

    def is_valid(self) -> bool:
        """Validate gRPC server entity state.

        Returns:
            True if server is valid, False otherwise

        """
        return bool(self.host and 1 <= self.port <= MAX_PORT_NUMBER)

    def is_running(self) -> bool:
        """Check if server is running.

        Returns:
            True if server is running, False otherwise

        """
        return self.state == GrpcServerState.RUNNING

    def start(self) -> bool:
        """Mark server as starting.

        Returns:
            True if state change successful, False otherwise

        """
        if self.state == GrpcServerState.STOPPED:
            self.state = GrpcServerState.STARTING
            return True
        return False

    def mark_running(self) -> bool:
        """Mark server as running.

        Returns:
            True if state change successful, False otherwise

        """
        if self.state == GrpcServerState.STARTING:
            self.state = GrpcServerState.RUNNING
            return True
        return False

    def stop(self) -> bool:
        """Mark server as stopping.

        Returns:
            True if state change successful, False otherwise

        """
        if self.state == GrpcServerState.RUNNING:
            self.state = GrpcServerState.STOPPING
            return True
        return False

    def mark_stopped(self) -> bool:
        """Mark server as stopped.

        Returns:
            True if state change successful, False otherwise

        """
        if self.state == GrpcServerState.STOPPING:
            self.state = GrpcServerState.STOPPED
            return True
        return False

    def add_service(self, service: FlextGrpcService) -> bool:
        """Add a service to the server.

        Args:
            service: Service to add

        Returns:
            True if service was added, False if already exists

        """
        if service.is_valid() and service not in self.services:
            self.services.append(service)
            return True
        return False

    def get_address(self) -> str:
        """Get server address.

        Returns:
            Server address as host:port

        """
        return f"{self.host}:{self.port}"


class FlextGrpcClient(FlextEntity):
    """gRPC client entity representing a gRPC client instance."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        channel: FlextGrpcChannel | None = None,
        options: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize gRPC client entity.

        Args:
            entity_id: Unique entity identifier
            channel: gRPC channel for communication
            options: Client options
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.channel = channel
        self.options = options or {}
        self.created_at = created_at or datetime.now(UTC)

    def is_valid(self) -> bool:
        """Validate gRPC client entity state.

        Returns:
            True if client is valid, False otherwise

        """
        return bool(self.channel and self.channel.is_valid())

    def is_connected(self) -> bool:
        """Check if client is connected.

        Returns:
            True if client channel is ready, False otherwise

        """
        return bool(self.channel and self.channel.is_ready())


class FlextGrpcStream(FlextEntity):
    """gRPC stream entity representing a streaming connection."""

    def __init__(
        self,
        entity_id: FlextEntityId | None = None,
        method_name: str = "",
        stream_type: str = "unary",
        metadata: dict[str, Any] | None = None,
        created_at: datetime | None = None,
    ) -> None:
        """Initialize gRPC stream entity.

        Args:
            entity_id: Unique entity identifier
            method_name: Name of the streaming method
            stream_type: Type of stream (unary, client_streaming, server_streaming, bidirectional)
            metadata: Stream metadata
            created_at: Creation timestamp

        """
        super().__init__(entity_id)
        self.method_name = method_name
        self.stream_type = stream_type
        self.metadata = metadata or {}
        self.created_at = created_at or datetime.now(UTC)

    def is_valid(self) -> bool:
        """Validate gRPC stream entity state.

        Returns:
            True if stream is valid, False otherwise

        """
        valid_types = ["unary", "client_streaming", "server_streaming", "bidirectional"]
        return bool(self.method_name and self.stream_type in valid_types)

    def is_streaming(self) -> bool:
        """Check if this is a streaming call.

        Returns:
            True if stream type is not unary, False otherwise

        """
        return self.stream_type != "unary"


# Backwards compatibility aliases
GrpcChannel = FlextGrpcChannel
GrpcService = FlextGrpcService
GrpcServer = FlextGrpcServer
GrpcClient = FlextGrpcClient
GrpcStream = FlextGrpcStream
