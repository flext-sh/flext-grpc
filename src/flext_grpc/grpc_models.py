"""FLEXT gRPC Models - Unified Domain Entities and Types.

🎯 CONSOLIDATES 2 MODEL FILES INTO SINGLE PEP8 MODULE:
- entities.py (800+ lines) - Core gRPC domain entities with Clean Architecture
- types.py (600+ lines) - Comprehensive type definitions and protocols

TOTAL CONSOLIDATION: 1400+ lines → grpc_models.py (PEP8 organized)

This module provides unified domain entities and type system for FLEXT gRPC platform,
implementing Clean Architecture and Domain-Driven Design principles with comprehensive
type safety and domain validation.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime

from flext_core import FlextEntity, FlextResult
from pydantic import Field

from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.grpc_config import (
    FLEXT_GRPC_MAX_PORT,
    FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH,
    FLEXT_GRPC_MIN_PORT,
)
from flext_grpc.typings import (
    TGrpcChannelState,
    TGrpcEntityId,
    TGrpcHost,
    TGrpcMethodName,
    TGrpcPort,
    TGrpcServerState,
    TGrpcServiceName,
    TGrpcStreamType,
    TGrpcTarget,
    TGrpcTimeout,
    flext_grpc_parse_target,
    flext_grpc_validate_target,
)

# =============================================================================
# GRPC TYPE DEFINITIONS
# =============================================================================


# =============================================================================
# GRPC DOMAIN ENTITIES
# =============================================================================


class FlextGrpcEntity(FlextEntity):
    """Base entity class for all gRPC domain entities.

    Provides common functionality for gRPC entities following unified FLEXT patterns.
    All gRPC entities inherit from this base class to ensure consistent behavior.

    Features:
      - Inherits FlextEntity with immutable behavior and validation
      - Implements entity_type property for runtime type identification
      - Supports business rule validation through validate_business_rules()

    Example:
      >>> entity = FlextGrpcEntity(id="test", created_at=datetime.now(timezone.utc))
      >>> print(entity.entity_type)
      'FlextGrpcEntity'

    """

    @property
    def entity_type(self) -> str:
        """Get the entity type name for runtime identification."""
        return self.__class__.__name__


class FlextGrpcServer(FlextGrpcEntity):
    """gRPC server domain entity with lifecycle management.

    Represents a gRPC server with comprehensive state management, configuration,
    and business rule validation. Implements immutable state transitions and
    enterprise-grade server lifecycle operations.

    Attributes:
      host: Server host address (required)
      port: Server port number (required, validated range)
      max_workers: Maximum worker threads (default: 10)
      state: Current server state (default: "stopped")
      ssl_enabled: SSL/TLS encryption enabled (default: False)

    State Transitions:
      stopped → starting → running → stopping → stopped

    Example:
      >>> server = FlextGrpcServer(
      ...     id="api-server",
      ...     host="localhost",
      ...     port=50051,
      ...     max_workers=10,
      ...     created_at=datetime.now(timezone.utc),
      ... )
      >>> result = server.validate_business_rules()
      >>> print(result.success)
      True

    """

    host: TGrpcHost = Field(...)
    port: TGrpcPort = Field(...)
    max_workers: int = Field(default=10)
    state: TGrpcServerState = Field(default="stopped")
    ssl_enabled: bool = Field(default=False)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate server business rules and configuration."""
        # Import here to avoid circular imports

        # Validate host
        if not self.host or not self.host.strip():
            return FlextResult.fail("Host cannot be empty")

        # Validate port range
        if not (FLEXT_GRPC_MIN_PORT <= self.port <= FLEXT_GRPC_MAX_PORT):
            return FlextResult.fail(
                f"Port {self.port} must be between {FLEXT_GRPC_MIN_PORT} and {FLEXT_GRPC_MAX_PORT}",
            )

        # Validate worker count

        if (
            self.max_workers < FlextGrpcConstants.Service.MIN_WORKERS
            or self.max_workers > FlextGrpcConstants.Service.MAX_WORKERS
        ):
            return FlextResult.fail(
                f"Max workers must be between {FlextGrpcConstants.Service.MIN_WORKERS} and {FlextGrpcConstants.Service.MAX_WORKERS}",
            )

        return FlextResult.ok(None)

    def start(self) -> FlextResult[FlextGrpcServer]:
        """Start the server (state transition: stopped → starting)."""
        if self.state != "stopped":
            return FlextResult.fail(f"Cannot start server in state: {self.state}")

        return FlextResult.ok(
            self.model_copy(update={"state": "starting"}),
        )

    def mark_running(self) -> FlextResult[FlextGrpcServer]:
        """Mark server as running (state transition: starting → running)."""
        if self.state != "starting":
            return FlextResult.fail(f"Cannot mark running from state: {self.state}")

        return FlextResult.ok(
            self.model_copy(update={"state": "running"}),
        )

    def stop(self) -> FlextResult[FlextGrpcServer]:
        """Stop the server (state transition: running → stopping)."""
        if self.state != "running":
            return FlextResult.fail(f"Cannot stop server in state: {self.state}")

        return FlextResult.ok(
            self.model_copy(update={"state": "stopping"}),
        )

    def mark_stopped(self) -> FlextResult[FlextGrpcServer]:
        """Mark server as stopped (state transition: stopping → stopped)."""
        if self.state != "stopping":
            return FlextResult.fail(f"Cannot mark stopped from state: {self.state}")

        return FlextResult.ok(
            self.model_copy(update={"state": "stopped"}),
        )


class FlextGrpcClient(FlextGrpcEntity):
    """gRPC client domain entity with connection management.

    Represents a gRPC client with connection state management, target configuration,
    and SSL/TLS support. Implements immutable state transitions and enterprise-grade
    client lifecycle operations.

    Attributes:
      target: gRPC target address (host:port format)
      ssl_enabled: SSL/TLS encryption enabled (default: False)
      channel_state: Current channel state (default: "idle")

    Example:
      >>> client = FlextGrpcClient(
      ...     id="api-client",
      ...     target=f"{FlextGrpcConstants.Network.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_PORT}",
      ...     created_at=datetime.now(timezone.utc),
      ... )
      >>> result = client.validate_business_rules()
      >>> print(result.success)
      True

    """

    target: TGrpcTarget = Field(...)
    ssl_enabled: bool = Field(default=False)
    channel_state: TGrpcChannelState = Field(default="idle")

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate client business rules and configuration."""
        # Validate target format
        if not flext_grpc_validate_target(self.target):
            return FlextResult.fail(f"Invalid target format: {self.target}")

        return FlextResult.ok(None)

    def connect(self) -> FlextResult[FlextGrpcClient]:
        """Connect the client (state transition: idle → connecting)."""
        if self.channel_state != "idle":
            return FlextResult.fail(f"Cannot connect from state: {self.channel_state}")

        return FlextResult.ok(
            self.model_copy(update={"channel_state": "connecting"}),
        )

    def mark_ready(self) -> FlextResult[FlextGrpcClient]:
        """Mark client as ready (state transition: connecting → ready)."""
        if self.channel_state != "connecting":
            return FlextResult.fail(
                f"Cannot mark ready from state: {self.channel_state}",
            )

        return FlextResult.ok(
            self.model_copy(update={"channel_state": "ready"}),
        )

    def disconnect(self) -> FlextResult[FlextGrpcClient]:
        """Disconnect the client (state transition: ready → shutdown)."""
        if self.channel_state not in {"ready", "connecting"}:
            return FlextResult.fail(
                f"Cannot disconnect from state: {self.channel_state}",
            )

        return FlextResult.ok(
            self.model_copy(update={"channel_state": "shutdown"}),
        )


class FlextGrpcChannel(FlextGrpcEntity):
    """gRPC channel domain entity with connection state management.

    Represents a gRPC channel with comprehensive state management and
    connection lifecycle operations.

    Attributes:
      target: gRPC target address (host:port format)
      state: Current channel state (default: "idle")

    """

    target: TGrpcTarget = Field(...)
    state: TGrpcChannelState = Field(default="idle")

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate channel business rules and configuration."""
        if not flext_grpc_validate_target(self.target):
            return FlextResult.fail(f"Invalid target format: {self.target}")

        return FlextResult.ok(None)


class FlextGrpcService(FlextGrpcEntity):
    """gRPC service domain entity with method management.

    Represents a gRPC service with method definitions and service metadata.

    Attributes:
      name: Service name (required)
      methods: List of available methods (default: empty list)

    """

    name: TGrpcServiceName = Field(...)
    methods: list[TGrpcMethodName] = Field(default_factory=list)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate service business rules and configuration."""
        if not self.name or not self.name.strip():
            return FlextResult.fail("Service name cannot be empty")

        # Validate service name length

        if len(self.name) > FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH:
            return FlextResult.fail(
                f"Service name too long: {len(self.name)} > {FLEXT_GRPC_MAX_SERVICE_NAME_LENGTH}",
            )

        return FlextResult.ok(None)


class FlextGrpcStream(FlextGrpcEntity):
    """gRPC stream domain entity with streaming operations.

    Represents a gRPC stream with type definitions and streaming metadata.

    Attributes:
      stream_type: Type of gRPC stream (unary, server_streaming, etc.)
      method_name: Associated method name

    """

    stream_type: TGrpcStreamType = Field(...)
    method_name: TGrpcMethodName = Field(...)

    def validate_business_rules(self) -> FlextResult[None]:
        """Validate stream business rules and configuration."""
        if not self.method_name or not self.method_name.strip():
            return FlextResult.fail("Method name cannot be empty")

        return FlextResult.ok(None)


# =============================================================================
# FACTORY FUNCTIONS - Entity Creation Helpers
# =============================================================================


def create_grpc_server(
    server_id: str,
    host: str,
    port: int,
    max_workers: int = 10,
    *,
    ssl_enabled: bool = False,
) -> FlextResult[FlextGrpcServer]:
    """Create a new gRPC server entity with validation."""
    try:
        server = FlextGrpcServer(
            id=server_id,
            host=TGrpcHost(host),
            port=TGrpcPort(port),
            max_workers=max_workers,
            ssl_enabled=ssl_enabled,
            created_at=datetime.now(UTC),
        )

        validation = server.validate_business_rules()
        if validation.is_failure:
            return FlextResult.fail(validation.error or "Server validation failed")

        return FlextResult.ok(server)
    except Exception as e:
        return FlextResult.fail(str(e))


def create_grpc_client(
    client_id: str,
    target: str,
    *,
    ssl_enabled: bool = False,
) -> FlextResult[FlextGrpcClient]:
    """Create a new gRPC client entity with validation."""
    try:
        client = FlextGrpcClient(
            id=client_id,
            target=TGrpcTarget(target),
            ssl_enabled=ssl_enabled,
            created_at=datetime.now(UTC),
        )

        validation = client.validate_business_rules()
        if validation.is_failure:
            return FlextResult.fail(validation.error or "Client validation failed")

        return FlextResult.ok(client)
    except Exception as e:
        return FlextResult.fail(str(e))


# =============================================================================
# EXPORTS
# =============================================================================

__all__ = [
    # Domain entities
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcEntity",
    "FlextGrpcServer",
    "FlextGrpcService",
    "FlextGrpcStream",
    # Type definitions
    "TGrpcChannelState",
    "TGrpcEntityId",
    "TGrpcHost",
    "TGrpcMethodName",
    "TGrpcPort",
    "TGrpcServerState",
    "TGrpcServiceName",
    "TGrpcStreamType",
    "TGrpcTarget",
    "TGrpcTimeout",
    # Factory functions
    "create_grpc_client",
    "create_grpc_server",
    # Utility functions
    "flext_grpc_parse_target",
    "flext_grpc_validate_target",
]
