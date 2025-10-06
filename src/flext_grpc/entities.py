"""FLEXT gRPC Entities.

Unified gRPC entities class extending maximum flext-core functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Self
from uuid import uuid4

from flext_core import (
    FlextConstants,
    FlextModels,
    FlextResult,
    FlextService,
    FlextTypes,
)
from pydantic import Field, field_validator

from flext_grpc.constants import FlextGrpcConstants
from flext_grpc.typings import FlextGrpcTypings


class FlextGrpcEntities(FlextService):
    """Unified gRPC entities class extending FlextService with maximum flext-core integration.

    Provides a single class containing all gRPC entity definitions, leveraging:
    - FlextService for domain service patterns and principles
    - Computed fields for derived properties
    - Cross-field validation for entity consistency
    - Type-safe entity relationships and state management

    This class serves as the central hub for all gRPC domain entities,
    ensuring consistent behavior and maximum flext-core integration.
    """

    # === BASE ENTITY DEFINITIONS ===

    class Entity(FlextModels.Entity):
        """Base entity class for all gRPC domain entities.

        Provides common functionality for gRPC entities following unified FLEXT patterns.
        All gRPC entities inherit from this base class to ensure consistent behavior.

        Features:
          - Inherits FlextModels with immutable behavior and validation
          - Implements entity_type property for runtime type identification
          - Supports business rule validation through validate_business_rules()

        Example:
          >>> entity = FlextGrpcEntity(id=test, created_at=datetime.now(timezone.utc))
          >>> print(entity.entity_type)
          'FlextGrpcEntity'

        """

        # Entity fields
        created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
        updated_at: datetime | None = Field(default_factory=lambda: datetime.now(UTC))

        @property
        def entity_type(self: Self) -> str:
            """Get the entity type name for runtime identification.

            Returns:
                str: The class name of the entity for type identification

            Example:
                >>> server = Server(id=test, created_at=datetime.now(timezone.utc))
                >>> print(server.entity_type)
                'Server'

            """
            return self.__class__.__name__

        def copy_with(self: Self, **kwargs: object) -> FlextResult[Self]:
            """Create a copy of the entity with updated attributes.

            Args:
                **kwargs: Attributes to update in the copy

            Returns:
                FlextResult[Self]: Success with updated entity copy

            Example:
                >>> entity = Server(id="test", created_at=datetime.now(timezone.utc))
                >>> result = entity.copy_with(port=8080)
                >>> if result.is_success:
                ...     print(result.data.port)
                8080

            """
            try:
                updated_entity = self.model_copy(update=kwargs)
                return FlextResult.ok(updated_entity)
            except Exception as e:
                return FlextResult.fail(
                    f"Failed to copy {self.__class__.__name__}: {e}"
                )

    class Channel(Entity):
        """gRPC channel entity representing connection state and management.

        Domain entity that encapsulates gRPC channel state and connection management
        functionality. Channels represent the connection between client and server
        with proper state transitions and validation.

        Attributes:
          target: gRPC target address for connection (host:port format)
          state: Current connection state (idle, connecting, ready, etc.)
          options: Additional gRPC channel options and configuration
          grpc_channel: Optional gRPC channel object for low-level operations

        State Transitions:
          idle -> connecting -> ready -> shutdown
          object state can transition to idle through disconnect()

        Domain Rules:
          - Target cannot be empty or None
          - State must be valid gRPC channel state
          - Options must be valid dictionary

        Example:
          >>> from datetime import UTC, datetime, timezone
          >>> channel = Channel(
          ...     id="main-channel",
          ...     target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}",
          ...     state="idle",
          ...     created_at=datetime.now(timezone.utc),
          ... )
          >>> connect_result: FlextResult[object] = channel.connect()
          >>> if connect_result.is_success:
          ...     connecting_channel = connect_result.data
          ...     print(connecting_channel.state)
          'connecting'

        """

        target: FlextGrpcTypings.GrpcTarget = Field(
            default_factory=lambda: ""  # GrpcTarget is a type alias for str, not a constructor
        )
        state: FlextGrpcTypings.GrpcChannelState = "idle"
        options: FlextTypes.Dict = Field(default_factory=dict)
        grpc_channel: object | None = None

        @field_validator("state")
        @classmethod
        def validate_state(cls, v: str) -> str:
            """Validate channel state is valid."""
            valid_states = set(FlextGrpcConstants.Literals.CHANNEL_STATES)
            if v not in valid_states:
                valid_states_str = ", ".join(
                    f"'{s}'" for s in FlextGrpcConstants.Literals.CHANNEL_STATES
                )
                msg = f"Input should be {valid_states_str}"
                raise ValueError(msg)
            return v

        def validate_business_rules(self: Self) -> FlextResult[None]:
            """Validate channel domain business rules.

            Ensures channel configuration meets business requirements including
            target validation, state consistency, and option validation.

            Returns:
                FlextResult[None]: Success with None data, or failure with error message

            Domain Rules Validated:
                - Target cannot be empty or whitespace-only
                - State must be valid gRPC channel state
                - Channel must be in consistent state

            Example:
                >>> channel = Channel(
                ...     id="test",
                ...     target="",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = channel.validate_business_rules()
                >>> print(result.is_failure)
                True
                >>> print(result.error)
                'Channel target cannot be empty'

            """
            if not self.target or not str(self.target).strip():
                return FlextResult[None].fail("Channel target cannot be empty")

            valid_states = set(FlextGrpcConstants.Literals.CHANNEL_STATES)
            if self.state not in valid_states:
                return FlextResult[None].fail(f"Invalid channel state: {self.state}")
            return FlextResult[None].ok(None)

        def is_ready(self: Self) -> bool:
            """Check if channel is ready for gRPC communication.

            Returns:
                bool: True if channel state is 'ready', False otherwise

            Example:
                >>> channel = Channel(
                ...     id=test, state=ready, created_at=datetime.now(timezone.utc)
                ... )
                >>> print(channel.is_ready())
                True

            """
            return self.state == "ready"

        def connect(self: Self) -> FlextResult[FlextGrpcEntities.Channel]:
            """Initiate channel connection state transition.

            Transitions channel from 'idle' state to 'connecting' state following
            proper state machine rules. Only allows connection from idle state.

            Returns:
                FlextResult['Channel']: Success with connecting channel,
                    or failure if invalid state transition

            State Transition:
                idle -> connecting

            Example:
                >>> channel = Channel(
                ...     id=test, state=idle, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = channel.connect()
                >>> if result.is_success:
                ...     print(result.data.state)
                'connecting'

            """
            if self.state != "idle":
                return FlextResult.fail(
                    f"Cannot connect from state: {self.state}",
                )
            connecting_channel = self.model_copy(update={"state": "connecting"})
            return FlextResult.ok(connecting_channel)

        def mark_ready(self: Self) -> FlextResult[FlextGrpcEntities.Channel]:
            """Mark channel as ready for communication.

            Transitions channel from 'connecting' state to 'ready' state following
            proper state machine rules. Only allows ready transition from connecting state.

            Returns:
                FlextResult['Channel']: Success with ready channel,
                    or failure if invalid state transition

            State Transition:
                connecting -> ready

            Example:
                >>> channel = Channel(
                ...     id=test, state=connecting, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = channel.mark_ready()
                >>> if result.is_success:
                ...     print(result.data.state)
                'ready'

            """
            if self.state != "connecting":
                return FlextResult.fail(
                    f"Cannot mark ready from state: {self.state}",
                )
            ready_channel = self.model_copy(update={"state": "ready"})
            return FlextResult.ok(ready_channel)

        def disconnect(self: Self) -> FlextResult[FlextGrpcEntities.Channel]:
            """Disconnect the channel and reset to idle state.

            Transitions channel to 'idle' state from any current state. This is a
            safe operation that can be performed from any state to reset the channel.

            Returns:
                FlextResult['Channel']: Success with idle channel

            State Transition:
                any_state -> idle

            Example:
                >>> channel = Channel(
                ...     id=test, state=ready, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = channel.disconnect()
                >>> print(result.data.state)
                'idle'

            """
            idle_channel = self.model_copy(update={"state": "idle"})
            return FlextResult.ok(idle_channel)

    class Server(Entity):
        """gRPC server entity implementing complete server lifecycle management.

        Domain entity representing a gRPC server with comprehensive state management,
        configuration validation, and service lifecycle operations. Provides rich
        behavioral methods for server operations following enterprise patterns.

        Attributes:
          host: Server bind address (IPv4, IPv6, or hostname)
          port: Server port number (1024-65535 range enforced)
          state: Current server state (stopped, starting, running, stopping)
          max_workers: Maximum number of worker threads for request processing
          services: List of registered gRPC service implementations

        State Machine:
          stopped -> starting -> running -> stopping -> stopped

        Domain Rules:
          - Host cannot be empty or whitespace-only
          - Port must be in valid range (1024-65535)
          - Max workers must be >= 1
          - State must be valid server state
          - Service registrations must be valid

        Integration:
          - Works with ServerService for business operations
          - Integrates with flext-observability for health monitoring
          - Supports FLEXT ecosystem service registration patterns

        Example:
          >>> from datetime import UTC, datetime, timezone
          >>> server = Server(
          ...     id="production-server",
          ...     host=FlextConstants.Platform.DEFAULT_HOST,
          ...     port=FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
          ...     max_workers=20,
          ...     created_at=datetime.now(timezone.utc),
          ... )
          >>> validation = server.validate_business_rules()
          >>> print(validation.is_success)
          True
          >>> start_result: FlextResult[object] = server.start()
          >>> print(start_result.data.state)
          'starting'

        """

        host: str = FlextConstants.Platform.DEFAULT_HOST
        port: int = FlextGrpcConstants.Network.DEFAULT_GRPC_PORT
        state: FlextGrpcTypings.GrpcServerState = "stopped"
        max_workers: int = 10
        services: list[FlextGrpcEntities.Service] = Field(default_factory=list)
        grpc_server: object | None = None

        def validate_business_rules(self: Self) -> FlextResult[None]:
            """Validate server domain business rules and configuration.

            Ensures server configuration meets business requirements including
            host validation, port range checking, worker limits, and state consistency.
            All domain rules are enforced to maintain data integrity and operational safety.

            Returns:
                FlextResult[None]: Success with None data, or failure with error

            Domain Rules Validated:
                - Host cannot be empty or whitespace-only
                - Port must be in valid range (1024-65535)
                - Max workers must be >= 1 for processing capacity
                - Server state must be valid gRPC server state
                - All configuration values must be consistent and safe for production

            Example:
                >>> server = Server(
                ...     id="test-server",
                ...     host="",  # Invalid empty host
                ...     port=FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = server.validate_business_rules()
                >>> print(result.is_failure)
                True
                >>> print(result.error)
                'Server host cannot be empty'

                >>> valid_server = Server(
                ...     id="production-server",
                ...     host=FlextConstants.Platform.DEFAULT_HOST,
                ...     port=FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
                ...     max_workers=10,
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = valid_server.validate_business_rules()
                >>> print(result.is_success)
                True

            Integration:
                Used by ServerService before all operations to ensure
                business rule compliance. Integrates with platform validation
                workflows and error reporting systems from flext-observability.

            Performance:
                Validation is lightweight with O(1) complexity. Safe to call
                frequently during server operations without performance impact.

            """
            if not self.host or not self.host.strip():
                return FlextResult[None].fail("Server host cannot be empty")

            # Allow port 0 for automatic port selection by gRPC
            if self.port != 0 and not (
                FlextConstants.Network.MIN_PORT
                <= self.port
                <= FlextConstants.Network.MAX_PORT
            ):
                return FlextResult[None].fail(
                    f"Invalid port: {self.port} "
                    f"(must be 0 for auto-selection or {FlextConstants.Network.MIN_PORT}-{FlextConstants.Network.MAX_PORT})",
                )

            if self.max_workers < 1:
                return FlextResult[None].fail("Max workers must be >= 1")

            valid_states = set(FlextGrpcConstants.Literals.SERVER_STATES)
            if self.state not in valid_states:
                return FlextResult[None].fail(f"Invalid server state: {self.state}")
            return FlextResult[None].ok(None)

        @property
        def address(self: Self) -> str:
            """Get complete server address as host:port format.

            Returns:
                str: Server address in "host:port" format for connection strings

            Example:
                >>> server = Server(
                ...     host=FlextConstants.Platform.DEFAULT_HOST,
                ...     port=FlextGrpcConstants.Network.DEFAULT_GRPC_PORT,
                ...     id="test",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(server.address)
                f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}"

            """
            return f"{self.host}:{self.port}"

        @property
        def is_running(self: Self) -> bool:
            """Check if server is currently in running state.

            Returns:
                bool: True if server state is 'running', False otherwise

            Example:
                >>> server = Server(
                ...     state=running, id=test, created_at=datetime.now(timezone.utc)
                ... )
                >>> print(server.is_running)
                True
                >>> stopped_server = Server(
                ...     state=stopped, id=test2, created_at=datetime.now(timezone.utc)
                ... )
                >>> print(stopped_server.is_running)
                False

            """
            return self.state == "running"

        def start(self: Self) -> FlextResult[FlextGrpcEntities.Server]:
            """Initiate server startup state transition.

            Transitions server from 'stopped' state to 'starting' state following
            proper state machine rules. Prevents starting running/starting servers.

            Returns:
                FlextResult['Server']: Success with starting server,
                    or failure if invalid state transition

            State Transition:
                stopped -> starting

            Example:
                >>> server = Server(
                ...     state=stopped, id=test, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = server.start()
                >>> if result.is_success:
                ...     print(result.data.state)
                'starting'

                >>> running_server = Server(
                ...     state=running, id=test2, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = running_server.start()
                >>> print(result.is_failure)
                True

            """
            if self.state in {"running", "starting"}:
                return FlextResult.fail(f"Server already {self.state}")

            starting_server = self.model_copy(update={"state": "starting"})
            return FlextResult.ok(starting_server)

        def mark_running(self: Self) -> FlextResult[FlextGrpcEntities.Server]:
            """Mark server as running after successful startup.

            Transitions server from 'starting' state to 'running' state following
            proper state machine rules. Only allows running transition from starting state.

            Returns:
                FlextResult['Server']: Success with running server,
                    or failure if invalid state transition

            State Transition:
                starting -> running

            Example:
                >>> server = Server(
                ...     state=starting, id=test, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = server.mark_running()
                >>> if result.is_success:
                ...     print(result.data.state)
                'running'

            """
            if self.state != "starting":
                return FlextResult.fail(
                    f"Cannot mark running from state: {self.state}",
                )

            running_server = self.model_copy(update={"state": "running"})
            return FlextResult.ok(running_server)

        def stop(self: Self) -> FlextResult[FlextGrpcEntities.Server]:
            """Initiate server shutdown state transition.

            Transitions server from 'running' state to 'stopping' state following
            proper state machine rules. Prevents stopping stopped/stopping servers.

            Returns:
                FlextResult['Server']: Success with stopping server,
                    or failure if invalid state transition

            State Transition:
                running -> stopping

            Example:
                >>> server = Server(
                ...     state=running, id=test, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = server.stop()
                >>> if result.is_success:
                ...     print(result.data.state)
                'stopping'

            """
            if self.state in {"stopped", "stopping"}:
                return FlextResult.fail(f"Server already {self.state}")

            stopping_server = self.model_copy(update={"state": "stopping"})
            return FlextResult.ok(stopping_server)

        def mark_stopped(self: Self) -> FlextResult[FlextGrpcEntities.Server]:
            """Mark server as stopped after successful shutdown.

            Transitions server from 'stopping' or 'running' state to 'stopped' state.
            Allows emergency stop from running state or normal completion from stopping.

            Returns:
                FlextResult['Server']: Success with stopped server,
                    or failure if invalid state transition

            State Transitions:
                stopping -> stopped (normal shutdown completion)
                running -> stopped (emergency stop)

            Example:
                >>> server = Server(
                ...     state=stopping, id=test, created_at=datetime.now(timezone.utc)
                ... )
                >>> result: FlextResult[object] = server.mark_stopped()
                >>> if result.is_success:
                ...     print(result.data.state)
                'stopped'

            """
            if self.state not in {"stopping", "running"}:
                return FlextResult.fail(
                    f"Cannot mark stopped from state: {self.state}",
                )
            stopped_server = self.model_copy(update={"state": "stopped"})
            return FlextResult.ok(stopped_server)

        def add_service(
            self, service: FlextGrpcEntities.Service
        ) -> FlextResult[FlextGrpcEntities.Server]:
            """Add a gRPC service to the server registry.

            Registers a new gRPC service with the server, ensuring no duplicate
            service names exist. Services must be added before server startup.

            Args:
                service: "FlextGrpcEntities.Service" instance to register with the server

            Returns:
                FlextResult['Server']: Success with updated server and service,
                    or failure if service already exists or validation fails

            Example:
                >>> from flext_grpc import Service
                >>> server = Server(id=test, created_at=datetime.now(timezone.utc))
                >>> service = Service(
                ...     id="user-service",
                ...     name="UserService",
                ...     methods=["GetUser", "CreateUser"],
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = server.add_service(service)
                >>> if result.is_success:
                ...     print(len(result.data.services))
                1

            Integration:
                Services added through this method are registered with the underlying
                gRPC server during startup. Used by ServerService for
                service lifecycle management.

            """
            for existing_service in self.services:
                if existing_service.name == service.name:
                    return FlextResult.fail("Service already exists")

            updated_server = self.model_copy(
                update={"services": [*self.services, service]}
            )
            return FlextResult.ok(updated_server)

    class Service(Entity):
        """gRPC service entity representing service definitions and method registry.

        Domain entity that encapsulates gRPC service definition with method registration,
        validation, and service lifecycle management. Provides comprehensive service
        management capabilities for the FLEXT gRPC platform.

        Attributes:
          name: Service name identifier for gRPC service registration
          methods: List of method names available in this service

        Domain Rules:
          - Service name cannot be empty or whitespace-only
          - Service must have at least one method defined
          - Method names cannot be empty or whitespace-only
          - All method names must be unique within the service

        Example:
          >>> from datetime import UTC, datetime, timezone
          >>> service = Service(
          ...     id="user-service",
          ...     name="UserService",
          ...     methods=["GetUser", "CreateUser", "UpdateUser"],
          ...     created_at=datetime.now(timezone.utc),
          ... )
          >>> validation = service.validate_business_rules()
          >>> print(validation.is_success)
          True
          >>> print(service.has_method("GetUser"))
          True

        """

        name: str = ""
        methods: FlextTypes.StringList = Field(default_factory=list)

        @field_validator("name")
        @classmethod
        def validate_name(cls, v: str) -> str:
            """Validate service name is not empty."""
            if not v or not v.strip():
                msg = "Service name cannot be empty"
                raise ValueError(msg)
            return v.strip()

        @field_validator("methods")
        @classmethod
        def validate_methods(cls, v: FlextTypes.StringList) -> FlextTypes.StringList:
            """Validate methods list is not empty and contains valid method names."""
            if not v:
                msg = "Methods list cannot be empty"
                raise ValueError(msg)

            # Validate each method name
            for method in v:
                if not method or not method.strip():
                    msg = "Method names cannot be empty"
                    raise ValueError(msg)

            return v

        def validate_business_rules(self: Self) -> FlextResult[None]:
            """Validate service domain business rules and method definitions.

            Ensures service configuration meets gRPC service requirements including
            name validation, method presence, and method name validation.

            Returns:
                FlextResult[None]: Success with None data, or failure with error

            Domain Rules Validated:
                - Service name cannot be empty or whitespace-only
                - Service must have at least one method defined
                - All method names must be valid (non-empty, non-whitespace)
                - Method names must be unique within the service

            Example:
                >>> service = Service(
                ...     id="invalid-service",
                ...     name="",  # Invalid empty name
                ...     methods=[],
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = service.validate_business_rules()
                >>> print(result.is_failure)
                True
                >>> print(result.error)
                'Service name cannot be empty'

            """
            if not self.name or not self.name.strip():
                return FlextResult[None].fail("Service name cannot be empty")

            if not self.methods:
                return FlextResult[None].fail("Service must have at least one method")

            for method in self.methods:
                if not method or not method.strip():
                    return FlextResult[None].fail("Method name cannot be empty")

            return FlextResult[None].ok(None)

        def has_method(self, method_name: str) -> bool:
            """Check if service has the specified method registered.

            Args:
                method_name: Name of the method to check for existence

            Returns:
                bool: True if method exists in service, False otherwise

            Example:
                >>> service = Service(
                ...     id="user-service",
                ...     name="UserService",
                ...     methods=["GetUser", "CreateUser"],
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(service.has_method("GetUser"))
                True
                >>> print(service.has_method("DeleteUser"))
                False

            """
            return method_name in self.methods

        def add_method(
            self, method_name: str
        ) -> FlextResult[FlextGrpcEntities.Service]:
            """Add a new method to the service registry.

            Registers a new method with the service, ensuring no duplicate method
            names exist within the service.

            Args:
                method_name: Name of the method to add to the service

            Returns:
                FlextResult['Service']: Success with updated service and method,
                    or failure if method already exists or validation fails

            Example:
                >>> service = Service(
                ...     id="user-service",
                ...     name="UserService",
                ...     methods=["GetUser"],
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = service.add_method("CreateUser")
                >>> if result.is_success:
                ...     print(len(result.data.methods))
                2
                >>> print(result.data.has_method("CreateUser"))
                True

            """
            if not method_name or not method_name.strip():
                return FlextResult.fail("Method name cannot be empty")

            if method_name in self.methods:
                return FlextResult.fail("Method already exists")

            updated_service = self.model_copy(
                update={"methods": [*self.methods, method_name]}
            )
            return FlextResult.ok(updated_service)

    class Client(Entity):
        """gRPC client entity implementing connection management and communication.

        Domain entity that encapsulates gRPC client functionality with channel management,
        connection state tracking, and communication capabilities. Provides comprehensive
        client lifecycle management for the FLEXT gRPC platform.

        Attributes:
          channel: Associated gRPC channel for server communication (optional)
          options: Additional client configuration options and settings

        Domain Rules:
          - Channel must be valid if present (passes domain validation)
          - Client options must be valid dictionary structure
          - Connection state determined by channel readiness

        Integration:
          - Works with Service for business operations
          - Integrates with Channel for connection management
          - Supports FLEXT ecosystem communication patterns

        Example:
          >>> from datetime import UTC, datetime, timezone
          >>> client = Client(id="api-client", created_at=datetime.now(timezone.utc))
          >>> connect_result: FlextResult[object] = client.connect_to(
          ...     f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}"
          ... )
          >>> if connect_result.is_success:
          ...     connected_client = connect_result.data
          ...     print(connected_client.is_connected)
          True

        """

        channel: FlextGrpcEntities.Channel | None = None
        options: FlextTypes.Dict = Field(default_factory=dict)
        grpc_stub: object | None = None

        def validate_business_rules(self: Self) -> FlextResult[None]:
            """Validate client domain business rules and configuration.

            Ensures client configuration meets business requirements including
            channel validation if present and options structure validation.

            Returns:
                FlextResult[None]: Success with None data, or failure with error

            Domain Rules Validated:
                - Channel must be valid if present (passes channel domain validation)
                - Client options must be valid dictionary structure
                - All configuration values must be consistent

            Example:
                >>> invalid_channel = Channel(
                ...     id="bad-channel",
                ...     target="",  # Invalid empty target
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> client = Client(
                ...     id="test-client",
                ...     channel=invalid_channel,
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = client.validate_business_rules()
                >>> print(result.is_failure)
                True

            """
            if self.channel is not None:
                channel_validation = self.channel.validate_business_rules()
                if channel_validation.is_failure:
                    return FlextResult[None].fail(
                        f"Invalid channel: {channel_validation.error}",
                    )
            return FlextResult[None].ok(None)

        @property
        def is_connected(self: Self) -> bool:
            """Check if client is connected and ready for communication.

            Returns:
                bool: True if client has a channel and channel is ready, False otherwise

            Example:
                >>> client = Client(id=test, created_at=datetime.now(timezone.utc))
                >>> print(client.is_connected)
                False

                >>> ready_channel = Channel(
                ...     id="ready-channel",
                ...     target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}",
                ...     state="ready",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> connected_client = client.copy_with(channel=ready_channel)
                >>> print(connected_client.is_connected)
                True

            """
            return bool(self.channel and self.channel.is_ready())

        @property
        def target(self: Self) -> str | None:
            """Get the target server address for client connection.

            Returns:
                str | None: Target address if channel exists, None otherwise

            Example:
                >>> channel = Channel(
                ...     id="test-channel",
                ...     target=f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> client = Client(
                ...     id="test-client",
                ...     channel=channel,
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(client.target)
                f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}"

            """
            return self.channel.target if self.channel else None

        def connect_to(self, target: str) -> FlextResult[FlextGrpcEntities.Client]:
            """Connect client to a target server address.

            Creates a new gRPC channel for the specified target and associates it
            with the client. The channel will be in idle state initially.

            Args:
                target: Target server address in "host:port" format

            Returns:
                FlextResult['Client']: Success with client connected to target,
                    or failure if channel creation fails

            Example:
                >>> client = Client(id=test, created_at=datetime.now(timezone.utc))
                >>> result: FlextResult[object] = client.connect_to(
                ...     f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}"
                ... )
                >>> if result.is_success:
                ...     connected_client = result.data
                ...     print(connected_client.target)
                f"{FlextConstants.Platform.DEFAULT_HOST}:{FlextGrpcConstants.Network.DEFAULT_GRPC_PORT}"

            Integration:
                Used by Service for establishing server connections.
                Channel state management handled through Channel entity.

            """
            # Direct entity construction - no factory patterns
            try:
                channel = FlextGrpcEntities.Channel(
                    id=str(uuid4()),
                    target=target,
                    state="idle",
                    options={},
                )

                updated_client = self.model_copy(update={"channel": channel})
                return FlextResult.ok(updated_client)
            except Exception as e:
                return FlextResult.fail(f"Channel creation failed: {e}")

    class GrpcStream(Entity):
        """gRPC stream entity representing streaming operations and flow control.

        Domain entity that encapsulates gRPC streaming functionality including
        unary, server streaming, client streaming, and bidirectional streaming.
        Provides comprehensive stream management for the FLEXT gRPC platform.

        Attributes:
          method_name: Name of the gRPC method associated with this stream
          stream_type: Type of streaming operation (unary, server/client/bidirectional)

        Stream Types:
          - unary: Single request, single response (traditional RPC)
          - server_streaming: Single request, multiple responses from server
          - client_streaming: Multiple requests from client, single response
          - bidirectional: Multiple requests and responses in both directions

        Domain Rules:
          - Method name cannot be empty or whitespace-only
          - Stream type must be one of the valid streaming types
          - All stream configuration must be consistent

        Example:
          >>> from datetime import UTC, datetime, timezone
          >>> stream = Stream(
          ...     id="data-stream",
          ...     method_name="StreamData",
          ...     stream_type="bidirectional",
          ...     created_at=datetime.now(timezone.utc),
          ... )
          >>> print(stream.is_bidirectional)
          True
          >>> print(stream.is_streaming)
          True

        """

        method_name: str = ""
        stream_type: FlextGrpcTypings.GrpcStreamType = "unary"
        grpc_stub: object | None = None

        @field_validator("method_name")
        @classmethod
        def validate_method_name(cls, v: str) -> str:
            """Validate method name is not empty."""
            if not v or not v.strip():
                msg = "Method name cannot be empty"
                raise ValueError(msg)
            return v.strip()

        @field_validator("stream_type")
        @classmethod
        def validate_stream_type(cls, v: str) -> str:
            """Validate stream type is valid."""
            valid_stream_types = FlextGrpcConstants.Literals.STREAM_TYPES
            if v not in valid_stream_types:
                msg = f"Invalid stream type: {v}"
                raise ValueError(msg)
            return v

        def validate_business_rules(self: Self) -> FlextResult[None]:
            """Validate stream domain business rules and configuration.

            Ensures stream configuration meets gRPC streaming requirements including
            method name validation and stream type validation.

            Returns:
                FlextResult[None]: Success with None data, or failure with error

            Domain Rules Validated:
                - Method name cannot be empty or whitespace-only
                - Stream type must be valid gRPC streaming type
                - All stream configuration must be consistent

            Example:
                >>> stream = Stream(
                ...     id="invalid-stream",
                ...     method_name="",
                ...     stream_type="unary",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> result: FlextResult[object] = stream.validate_business_rules()
                >>> print(result.is_failure)
                True
                >>> print(result.error)
                'Stream method name cannot be empty'

            """
            if not self.method_name or not self.method_name.strip():
                return FlextResult[None].fail("Stream method name cannot be empty")

            valid_stream_types = FlextGrpcConstants.Literals.STREAM_TYPES
            if self.stream_type not in valid_stream_types:
                return FlextResult[None].fail(
                    f"Invalid stream type: {self.stream_type}"
                )

            return FlextResult[None].ok(None)

        @property
        def is_streaming(self: Self) -> bool:
            """Check if stream supports streaming operations.

            Returns:
                bool: True if stream type supports streaming, False for unary

            Example:
                >>> unary_stream = Stream(
                ...     id="unary-stream",
                ...     method_name="GetUser",
                ...     stream_type="unary",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(unary_stream.is_streaming)
                False

                >>> server_stream = Stream(
                ...     id="server-stream",
                ...     method_name="StreamData",
                ...     stream_type="server_streaming",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(server_stream.is_streaming)
                True

            """
            return self.stream_type != "unary"

        @property
        def is_server_streaming(self: Self) -> bool:
            """Check if stream supports server streaming operations.

            Returns:
                bool: True if server streaming, False otherwise

            Example:
                >>> stream = Stream(
                ...     id="server-stream",
                ...     method_name="StreamData",
                ...     stream_type="server_streaming",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(stream.is_server_streaming)
                True

            """
            return self.stream_type == "server_streaming"

        @property
        def is_client_streaming(self: Self) -> bool:
            """Check if stream supports client streaming operations.

            Returns:
                bool: True if client streaming, False otherwise

            Example:
                >>> stream = Stream(
                ...     id="client-stream",
                ...     method_name="UploadData",
                ...     stream_type="client_streaming",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(stream.is_client_streaming)
                True

            """
            return self.stream_type == "client_streaming"

        @property
        def is_bidirectional(self: Self) -> bool:
            """Check if stream supports bidirectional streaming operations.

            Returns:
                bool: True if bidirectional streaming, False otherwise

            Example:
                >>> stream = Stream(
                ...     id="bidirectional-stream",
                ...     method_name="Chat",
                ...     stream_type="bidirectional",
                ...     created_at=datetime.now(timezone.utc),
                ... )
                >>> print(stream.is_bidirectional)
                True

            """
            return self.stream_type == "bidirectional"


# Module-level aliases for backward compatibility (will be removed in future versions)
FlextGrpcChannel = FlextGrpcEntities.Channel
FlextGrpcClient = FlextGrpcEntities.Client
FlextGrpcServer = FlextGrpcEntities.Server
FlextGrpcStream = FlextGrpcEntities.GrpcStream
FlextGrpcService = FlextGrpcEntities.Service


__all__ = [
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcEntities",
    "FlextGrpcServer",
    "FlextGrpcService",
    "FlextGrpcStream",
]
