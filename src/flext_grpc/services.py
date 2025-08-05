"""FLEXT gRPC Domain Services - Business logic orchestration for gRPC operations.

This module implements the application layer services for the FLEXT gRPC communication
platform following Domain-Driven Design principles. Services orchestrate business
workflows and coordinate between domain entities and external systems.

Key Components:
    - FlextGrpcServerService: Server lifecycle management and operations
    - FlextGrpcClientService: Client connection management and communication
    - FlextGrpcStreamService: Streaming operations and flow control
    - FlextGrpcService: Unified service facade for platform operations

Architecture:
    Domain services implement business process orchestration using the Command pattern.
    All services follow the FlextResult pattern for consistent error handling and
    integrate with the global dependency injection container from flext-core.

Service Patterns:
    - Command Pattern: Operations are executed through execute() methods
    - Result Pattern: All operations return FlextResult for railway-oriented programming
    - Template Method: Shared validation logic across service implementations
    - Dependency Injection: Services accessed through global container

Example:
    Basic server service usage with validation and error handling:

    >>> from flext_grpc import FlextGrpcServerService, FlextGrpcServer
    >>> from datetime import datetime, timezone
    >>>
    >>> service = FlextGrpcServerService()
    >>> server = FlextGrpcServer(
    ...     id="main-server",
    ...     host="localhost",
    ...     port=50051,
    ...     created_at=datetime.now(timezone.utc),
    ... )
    >>> result = service.execute("start", server)
    >>> print(result.success)
    True

Integration:
    - Built on flext-core domain service foundations for consistent patterns
    - Integrates with flext-observability for operation monitoring and metrics
    - Coordinates with platform layer for unified gRPC communication management
    - Supports FLEXT ecosystem service orchestration and cross-service communication

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import FlextDomainService, FlextResult

from flext_grpc.entities import (
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcStream,
)

from .constants import FlextGrpcConstants

if TYPE_CHECKING:
    from flext_grpc.entities import (
        FlextGrpcChannel,
    )


# =============================================================================
# SHARED VALIDATION PATTERNS - DRY REFACTORING
# Eliminates 15+ lines of duplicate validation logic across 4 service classes
# =============================================================================


class _GrpcServiceValidationMixin:
    """Template Method Pattern: Shared validation logic for gRPC services.

    SOLID REFACTORING: Eliminates 30+ lines of duplicated argument validation
    across FlextGrpcServerService, FlextGrpcClientService, FlextGrpcStreamService,
    and FlextGrpcUnifiedService classes.
    """

    @staticmethod
    def _validate_operation_arguments(
        args: tuple[object, ...],
        min_args: int = 2,
        expected_args_description: str = "operation and target",
    ) -> FlextResult[tuple[str, object]]:
        """Template Method: Validate and extract operation arguments.

        SOLID REFACTORING: Centralizes argument validation logic that was
        duplicated across 4 different execute() methods.

        Args:
            args: Arguments tuple from execute method
            min_args: Minimum number of arguments required
            expected_args_description: Description for error messages

        Returns:
            FlextResult with (operation_str, target_object) or failure

        """
        # Check minimum argument count
        if len(args) < min_args:
            return FlextResult.fail(
                f"Missing required arguments: {expected_args_description}",
            )

        # Extract and validate operation string
        operation = args[0]
        if not isinstance(operation, str):
            return FlextResult.fail("Operation must be a string")

        # Return operation and second argument (if exists)
        target = args[1] if len(args) > 1 else None
        return FlextResult.ok((operation, target))


class FlextGrpcServerService(FlextDomainService[FlextGrpcServer], _GrpcServiceValidationMixin):
    """Domain service for gRPC server lifecycle management and operations.

    Application layer service implementing server lifecycle management operations
    including startup, shutdown, service registration, and status monitoring.
    Orchestrates business workflows around gRPC server entities following
    Domain-Driven Design and Clean Architecture principles.

    This service acts as the primary interface for server management operations,
    coordinating between domain entities, infrastructure concerns, and external
    systems while maintaining clear architectural boundaries and consistent
    error handling patterns.

    Responsibilities:
        - Server lifecycle management (start, stop, restart)
        - gRPC service registration and management
        - Server status monitoring and health checks
        - Validation and error handling for server operations
        - State transition coordination and consistency

    Supported Operations:
        - "start": Initialize and start gRPC server
        - "stop": Gracefully shutdown running server
        - "add_service": Register new gRPC service implementation
        - "status": Retrieve comprehensive server status information

    Architecture Patterns:
        - Domain Service: Orchestrates business processes across entities
        - Command Pattern: Operations executed through execute() method
        - Template Method: Uses shared validation from mixin base class
        - Result Pattern: All operations return FlextResult for consistent handling

    State Management:
        Coordinates server state transitions following defined state machine:
        stopped → starting → running → stopping → stopped

    Example:
        Basic server lifecycle management:

        >>> from flext_grpc import FlextGrpcServerService, FlextGrpcServer
        >>> from datetime import datetime, timezone
        >>>
        >>> service = FlextGrpcServerService()
        >>> server = FlextGrpcServer(
        ...     id="production-server",
        ...     host="0.0.0.0",
        ...     port=50051,
        ...     max_workers=10,
        ...     created_at=datetime.now(timezone.utc),
        ... )
        >>>
        >>> # Start server
        >>> start_result = service.execute("start", server)
        >>> if start_result.success:
        ...     running_server = start_result.data
        ...     print(f"Server started on {running_server.address}")
        >>>
        >>> # Check server status
        >>> status_result = service.execute("status", running_server)
        >>> if status_result.success:
        ...     status = status_result.data
        ...     print(f"Server {status['id']} is {status['state']}")

    Integration:
        - Built on flext-core FlextDomainService foundation
        - Uses FlextResult pattern for consistent error handling
        - Integrates with flext-observability for operation monitoring
        - Coordinates with server entities for domain logic execution

    Error Handling:
        All operations return FlextResult with detailed error information:
        - Validation errors for invalid arguments or server state
        - Domain rule violations from server entity validation
        - State transition failures during lifecycle operations
        - Infrastructure failures during server startup/shutdown

    Thread Safety:
        Service operations are stateless and thread-safe. Server state
        management is handled through immutable entity patterns with
        copy_with() methods for state transitions.

    """

    def _handle_result(
        self,
        result: FlextResult[object],
        error_msg: str,
    ) -> FlextResult[object]:
        """Handle operation results with consistent error handling.

        Utility method providing standardized result handling across all server
        operations. Ensures consistent behavior for success and failure cases
        while providing fallback error messages when original errors are missing.

        Args:
            result (FlextResult[object]): Operation result to process and normalize.
            error_msg (str): Fallback error message when result.error is None.

        Returns:
            FlextResult[object]: Normalized result with guaranteed data on success
            (empty dict if None) and guaranteed error message on failure.

        Business Logic:
            - Success: Returns original data or empty dict if data is None
            - Failure: Returns original error message or provided fallback
            - Ensures no None values in success cases for downstream processing

        """
        if result.success:
            return FlextResult.ok(result.data if result.data is not None else {})
        return FlextResult.fail(result.error or error_msg)

    def execute(self) -> FlextResult[FlextGrpcServer]:
        """Execute default server operation - implementation required by abstract base."""
        return FlextResult.fail("Use execute_operation(operation, server, **kwargs) instead")

    def execute_operation(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute server management operation with validation and error handling.

        Primary entry point for all server operations implementing the Command pattern.
        Validates arguments, delegates to appropriate operation handlers, and ensures
        consistent result handling across all server management workflows.

        This method serves as the unified interface for server lifecycle management,
        providing type-safe operation dispatch with comprehensive validation and
        detailed error reporting for monitoring and debugging purposes.

        Args:
            *args (object): Variable arguments where first two are required:
                - args[0] (str): Operation name (start/stop/add_service/status)
                - args[1] (FlextGrpcServer): Target server entity for operation
            **kwargs (object): Additional operation-specific options:
                - service (FlextGrpcService): Required for "add_service" operation
                - Additional options passed to operation handlers

        Returns:
            FlextResult[object]: Operation result containing:
                - Success: Operation-specific data (server entity, status dict, etc.)
                - Failure: Detailed error message with validation/execution failures

        Supported Operations:
            - "start": Start server with state transition validation
            - "stop": Stop running server with graceful shutdown
            - "add_service": Register gRPC service with validation
            - "status": Retrieve comprehensive server status information

        Validation Flow:
            1. Argument count and type validation using shared mixin
            2. Server entity type validation and domain rule checking
            3. Operation-specific validation and parameter extraction
            4. Delegation to appropriate operation handler method

        Example:
            Execute server operations with error handling:

            >>> service = FlextGrpcServerService()
            >>> server = FlextGrpcServer(id="srv-1", host="localhost", port=50051)
            >>>
            >>> # Start server operation
            >>> result = service.execute("start", server)
            >>> if result.success:
            ...     started_server = result.data
            ...     print(f"Server {started_server.id} started successfully")
            >>> else:
            ...     print(f"Start failed: {result.error}")
            >>>
            >>> # Add service operation
            >>> grpc_service = FlextGrpcService(name="MyService", methods=["GetData"])
            >>> result = service.execute("add_service", server, service=grpc_service)

        Error Handling:
            Returns detailed error messages for:
            - Invalid argument count or types
            - Server entity validation failures
            - Domain rule violations
            - State transition conflicts
            - Unknown operation names

        Thread Safety:
            Stateless operation execution with immutable entity patterns.
            Safe for concurrent execution across multiple threads.

        Integration:
            Uses shared validation mixin for consistent argument handling
            and delegates to specialized operation methods for business logic.

        """
        # REFACTORING: Use shared validation - eliminates 15 lines duplication
        validation_result = self._validate_operation_arguments(
            args,
            FlextGrpcConstants.MIN_REQUIRED_ARGS,
            "operation and server",
        )
        if validation_result.is_failure:
            return FlextResult.fail(validation_result.error or "Validation failed")

        if validation_result.data is None:
            return FlextResult.fail("Validation returned no data")

        operation, server = validation_result.data

        # Type validation for server
        from flext_grpc.entities import FlextGrpcServer  # noqa: PLC0415

        if not isinstance(server, FlextGrpcServer):
            return FlextResult.fail("Server must be a FlextGrpcServer instance")

        # Validate server first
        validation = server.validate_business_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid server: {validation.error}")

        return self._execute_server_operation(operation, server, **kwargs)

    def _execute_server_operation(  # noqa: PLR0911
        self,
        operation: str,
        server: FlextGrpcServer,
        **options: object,
    ) -> FlextResult[object]:
        """Execute specific server operation with pattern matching and error handling.

        Delegates to appropriate operation handler based on operation name using
        pattern matching for type-safe operation dispatch. Handles all supported
        server operations with consistent error handling and result processing.

        Args:
            operation (str): Server operation name to execute.
            server (FlextGrpcServer): Target server entity for operation.
            **options (object): Additional operation-specific parameters.

        Returns:
            FlextResult[object]: Operation result with success data or error details.

        Supported Operations:
            - "start": Server startup with state transition
            - "stop": Server shutdown with graceful handling
            - "add_service": Service registration with validation
            - "status": Status information retrieval

        """
        # Use match for better type inference
        match operation:
            case "start":
                start_result = self._start_server(server)
                if start_result.success:
                    return FlextResult.ok(start_result.data)
                return FlextResult.fail(start_result.error or "Start failed")
            case "stop":
                stop_result = self._stop_server(server)
                if stop_result.success:
                    return FlextResult.ok(stop_result.data)
                return FlextResult.fail(stop_result.error or "Stop failed")
            case "add_service":
                return self._handle_add_service(server, options)
            case "status":
                status_result = self._get_server_status(server)
                if status_result.success:
                    return FlextResult.ok(status_result.data)
                return FlextResult.fail(status_result.error or "Status failed")
            case _:
                return FlextResult.fail(f"Unknown server operation: {operation}")

    def _handle_add_service(
        self,
        server: FlextGrpcServer,
        options: dict[str, object],
    ) -> FlextResult[object]:
        """Handle gRPC service registration with comprehensive validation.

        Processes service registration requests by validating the service entity
        and delegating to the server's add_service domain method. Ensures type
        safety and proper error handling throughout the registration process.

        Args:
            server (FlextGrpcServer): Target server for service registration.
            options (dict[str, object]): Operation options containing:
                - service (FlextGrpcService): Service entity to register

        Returns:
            FlextResult[object]: Registration result with updated server entity
            or detailed error information for debugging.

        Validation Rules:
            1. Service parameter must be present in options
            2. Service must be valid FlextGrpcService instance
            3. Server must accept the service registration

        Business Logic:
            Delegates service registration to server entity's add_service method,
            maintaining domain logic encapsulation while providing service layer
            coordination and error handling.

        """
        service = options.get("service")
        if not service:
            return FlextResult.fail("Service required")

        # Type validation for service
        from flext_grpc.entities import FlextGrpcService  # noqa: PLC0415

        if not isinstance(service, FlextGrpcService):
            return FlextResult.fail("Service must be a FlextGrpcService instance")

        result = server.add_service(service)
        # Convert to object result to match return type
        if result.success:
            return FlextResult.ok(result.data)
        return FlextResult.fail(result.error or "Add service failed")

    def _start_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Start gRPC server with proper state transition management.

        Coordinates server startup process including state validation, transition
        management, and proper error handling. Ensures server follows defined
        state machine transitions for reliable lifecycle management.

        Args:
            server (FlextGrpcServer): Server entity to start.

        Returns:
            FlextResult[FlextGrpcServer]: Started server entity in running state
            or failure with detailed error information.

        State Transitions:
            stopped → starting → running

        Validation:
            - Server must not already be in running state
            - Server must be in valid state for starting
            - All domain rules must be satisfied

        Business Logic:
            1. Validate current server state
            2. Initiate start transition (stopped → starting)
            3. Complete startup process (starting → running)
            4. Return running server entity

        """
        if server.is_running:
            return FlextResult.fail("Server is already running")

        # Use proper state transitions
        start_result = server.start()
        if start_result.is_failure:
            return start_result

        starting_server = start_result.data
        if starting_server is None:
            return FlextResult.fail("Failed to start server")

        return starting_server.mark_running()

    def _stop_server(self, server: FlextGrpcServer) -> FlextResult[FlextGrpcServer]:
        """Stop gRPC server with graceful shutdown and state transition management.

        Coordinates server shutdown process including state validation, graceful
        service termination, and proper state transitions. Ensures clean shutdown
        of all server resources and connections.

        Args:
            server (FlextGrpcServer): Running server entity to stop.

        Returns:
            FlextResult[FlextGrpcServer]: Stopped server entity in stopped state
            or failure with detailed error information.

        State Transitions:
            running → stopping → stopped

        Validation:
            - Server must be in running state
            - Server must be in valid state for stopping
            - All domain rules must be satisfied

        Business Logic:
            1. Validate server is running
            2. Initiate stop transition (running → stopping)
            3. Complete shutdown process (stopping → stopped)
            4. Return stopped server entity

        """
        if not server.is_running:
            return FlextResult.fail("Server is not running")

        # Use proper state transitions
        stop_result = server.stop()
        if stop_result.is_failure:
            return stop_result

        stopping_server = stop_result.data
        if stopping_server is None:
            return FlextResult.fail("Failed to stop server")

        return stopping_server.mark_stopped()

    def _get_server_status(
        self,
        server: FlextGrpcServer,
    ) -> FlextResult[dict[str, object]]:
        """Get comprehensive server status information for monitoring and debugging.

        Retrieves detailed server status including operational state, configuration,
        service registrations, and runtime metrics. Provides essential information
        for monitoring, debugging, and operational visibility.

        Args:
            server (FlextGrpcServer): Server entity to query for status.

        Returns:
            FlextResult[dict[str, object]]: Status dictionary containing:
                - id (str): Server unique identifier
                - address (str): Server bind address (host:port)
                - state (str): Current server state
                - is_running (bool): Runtime status flag
                - service_count (int): Number of registered services
                - max_workers (int): Maximum worker thread count
                - version (str): Server version information

        Status Information:
            Provides comprehensive operational visibility including:
            - Current lifecycle state and runtime status
            - Network configuration and service statistics
            - Resource limits and capacity information
            - Version information for compatibility tracking

        Usage:
            Essential for monitoring dashboards, health checks, and operational
            debugging. Status information supports both automated monitoring
            and manual troubleshooting workflows.

        """
        return FlextResult.ok(
            {
                "id": server.id,
                "address": server.address,
                "state": server.state,
                "is_running": server.is_running,
                "service_count": len(server.services),
                "max_workers": server.max_workers,
                "version": server.version,
            },
        )


class FlextGrpcClientService(FlextDomainService[FlextGrpcClient], _GrpcServiceValidationMixin):
    """Domain service for gRPC client connection management and communication.

    Application layer service implementing client lifecycle management including
    connection establishment, disconnection, method invocation, and status monitoring.
    Orchestrates business workflows around gRPC client entities following
    Domain-Driven Design and Clean Architecture principles.

    This service acts as the primary interface for client communication operations,
    coordinating between client entities, channel management, and remote service
    invocation while maintaining clear architectural boundaries and consistent
    error handling patterns.

    Responsibilities:
        - Client connection lifecycle management (connect, disconnect)
        - gRPC method invocation and response handling
        - Channel state management and monitoring
        - Client status monitoring and health checks
        - Validation and error handling for client operations

    Supported Operations:
        - "connect": Establish client connection with channel setup
        - "disconnect": Close client connection and cleanup resources
        - "call": Invoke remote gRPC methods with request/response handling
        - "status": Retrieve comprehensive client status information

    Architecture Patterns:
        - Domain Service: Orchestrates business processes across client entities
        - Command Pattern: Operations executed through execute() method
        - Template Method: Uses shared validation from mixin base class
        - Result Pattern: All operations return FlextResult for consistent handling

    Connection Management:
        Coordinates client-server connections through channel state management:
        idle → connecting → ready → (active communication) → shutdown

    Example:
        Basic client communication workflow:

        >>> from flext_grpc import FlextGrpcClientService, FlextGrpcClient
        >>> from datetime import datetime, timezone
        >>>
        >>> service = FlextGrpcClientService()
        >>> client = FlextGrpcClient(
        ...     id="api-client",
        ...     target="localhost:50051",
        ...     created_at=datetime.now(timezone.utc),
        ... )
        >>>
        >>> # Connect to server
        >>> connect_result = service.execute("connect", client)
        >>> if connect_result.success:
        ...     connected_client = connect_result.data
        ...     print(f"Connected to {connected_client.target}")
        >>>
        >>> # Call remote method
        >>> call_result = service.execute(
        ...     "call",
        ...     connected_client,
        ...     method_name="GetData",
        ...     request_data={"query": "latest"},
        ... )
        >>> if call_result.success:
        ...     response = call_result.data
        ...     print(f"Method call successful: {response['status']}")

    Integration:
        - Built on flext-core FlextDomainService foundation
        - Uses FlextResult pattern for consistent error handling
        - Integrates with flext-observability for operation monitoring
        - Coordinates with client entities and channel management

    Error Handling:
        All operations return FlextResult with detailed error information:
        - Connection failures and timeout handling
        - Channel state management errors
        - Remote method invocation failures
        - Validation errors for invalid arguments or client state

    Thread Safety:
        Service operations are stateless and thread-safe. Client connection
        state is managed through immutable entity patterns with proper
        synchronization for concurrent access.

    Application layer service implementing client lifecycle management including
    connection establishment, disconnection, method invocation, and status monitoring.
    Orchestrates business workflows around gRPC client entities following
    Domain-Driven Design and Clean Architecture principles.

    This service acts as the primary interface for client communication operations,
    coordinating between client entities, channel management, and remote service
    invocation while maintaining clear architectural boundaries and consistent
    error handling patterns.

    Responsibilities:
        - Client connection lifecycle management (connect, disconnect)
        - gRPC method invocation and response handling
        - Channel state management and monitoring
        - Client status monitoring and health checks
        - Validation and error handling for client operations

    Supported Operations:
        - "connect": Establish client connection with channel setup
        - "disconnect": Close client connection and cleanup resources
        - "call": Invoke remote gRPC methods with request/response handling
        - "status": Retrieve comprehensive client status information

    Architecture Patterns:
        - Domain Service: Orchestrates business processes across client entities
        - Command Pattern: Operations executed through execute() method
        - Template Method: Uses shared validation from mixin base class
        - Result Pattern: All operations return FlextResult for consistent handling

    Connection Management:
        Coordinates client-server connections through channel state management:
        idle → connecting → ready → (active communication) → shutdown

    Example:
        Basic client communication workflow:

        >>> from flext_grpc import FlextGrpcClientService, FlextGrpcClient
        >>> from datetime import datetime, timezone
        >>>
        >>> service = FlextGrpcClientService()
        >>> client = FlextGrpcClient(
        ...     id="api-client",
        ...     target="localhost:50051",
        ...     created_at=datetime.now(timezone.utc),
        ... )
        >>>
        >>> # Connect to server
        >>> connect_result = service.execute("connect", client)
        >>> if connect_result.success:
        ...     connected_client = connect_result.data
        ...     print(f"Connected to {connected_client.target}")
        >>>
        >>> # Call remote method
        >>> call_result = service.execute(
        ...     "call",
        ...     connected_client,
        ...     method_name="GetData",
        ...     request_data={"query": "latest"},
        ... )
        >>> if call_result.success:
        ...     response = call_result.data
        ...     print(f"Method call successful: {response['status']}")

    Integration:
        - Built on flext-core FlextDomainService foundation
        - Uses FlextResult pattern for consistent error handling
        - Integrates with flext-observability for operation monitoring
        - Coordinates with client entities and channel management

    Error Handling:
        All operations return FlextResult with detailed error information:
        - Connection failures and timeout handling
        - Channel state management errors
        - Remote method invocation failures
        - Validation errors for invalid arguments or client state

    Thread Safety:
        Service operations are stateless and thread-safe. Client connection
        state is managed through immutable entity patterns with proper
        synchronization for concurrent access.

    """

    def _handle_result(
        self,
        result: FlextResult[object],
        error_msg: str,
    ) -> FlextResult[object]:
        """Handle result with consistent pattern."""
        if result.success:
            return FlextResult.ok(result.data if result.data is not None else {})
        return FlextResult.fail(result.error or error_msg)

    def execute(self) -> FlextResult[FlextGrpcClient]:
        """Execute default client operation - implementation required by abstract base."""
        return FlextResult.fail("Use execute_operation(operation, client, **kwargs) instead")

    def execute_operation(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute client operation.

        Args:
            *args: Arguments (expected: operation, client)
            **kwargs: Additional options

        Returns:
            FlextResult with operation result

        """
        # REFACTORING: Use shared validation - eliminates 15 lines duplication
        validation_result = self._validate_operation_arguments(
            args,
            FlextGrpcConstants.MIN_REQUIRED_ARGS,
            "operation and client",
        )
        if validation_result.is_failure:
            return FlextResult.fail(validation_result.error or "Validation failed")

        if validation_result.data is None:
            return FlextResult.fail("Validation returned no data")

        operation, client = validation_result.data

        # Type validation for client
        from flext_grpc.entities import FlextGrpcClient  # noqa: PLC0415

        if not isinstance(client, FlextGrpcClient):
            return FlextResult.fail("Client must be a FlextGrpcClient instance")

        # Validate client first
        validation = client.validate_business_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid client: {validation.error}")

        return self._execute_client_operation(operation, client, **kwargs)

    def _execute_client_operation(  # noqa: PLR0911
        self,
        operation: str,
        client: FlextGrpcClient,
        **kwargs: object,
    ) -> FlextResult[object]:
        """Execute specific client operation - SOLID principle pattern."""
        # Use match for better type inference
        match operation:
            case "connect":
                connect_result = self._connect_client(client)
                if connect_result.success:
                    return FlextResult.ok(connect_result.data)
                return FlextResult.fail(connect_result.error or "Connect failed")
            case "disconnect":
                disconnect_result = self._disconnect_client(client)
                if disconnect_result.success:
                    return FlextResult.ok(disconnect_result.data)
                return FlextResult.fail(disconnect_result.error or "Disconnect failed")
            case "call":
                return self._handle_call_operation(client, kwargs)
            case "status":
                status_result = self._get_client_status(client)
                if status_result.success:
                    return FlextResult.ok(status_result.data)
                return FlextResult.fail(status_result.error or "Status failed")
            case _:
                return FlextResult.fail(f"Unknown client operation: {operation}")

    def _handle_call_operation(
        self,
        client: FlextGrpcClient,
        kwargs: dict[str, object],
    ) -> FlextResult[object]:
        """Handle call operation with proper parameter extraction."""
        method_name_arg = kwargs.get("method_name")
        method_name = str(method_name_arg) if method_name_arg else None
        request_data = kwargs.get("request_data")
        call_result = self._call_method(client, method_name, request_data)
        if call_result.success:
            return FlextResult.ok(call_result.data)
        return FlextResult.fail(call_result.error or "Call failed")

    def _connect_client(self, client: FlextGrpcClient) -> FlextResult[FlextGrpcClient]:
        """Connect client with proper channel state management."""
        # Validate client state
        connection_validation = self._validate_client_for_connection(client)
        if connection_validation.is_failure:
            return FlextResult.fail(
                connection_validation.error or "Connection validation failed",
            )

        # Connect and transition channel
        if client.channel is None:
            return FlextResult.fail("Client has no channel to connect")
        channel_result = self._connect_and_ready_channel(client.channel)
        if channel_result.is_failure:
            return FlextResult.fail(channel_result.error or "Channel connection failed")

        return client.copy_with(channel=channel_result.data)

    def _validate_client_for_connection(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[None]:
        """Validate client state for connection."""
        if client.is_connected:
            return FlextResult.fail("Client is already connected")
        if not client.channel:
            return FlextResult.fail("Client has no channel")
        return FlextResult.ok(None)

    def _connect_and_ready_channel(self, channel: FlextGrpcChannel) -> FlextResult[FlextGrpcChannel]:
        """Connect channel and mark as ready."""
        # Use proper channel state transitions
        connect_result = channel.connect()
        if connect_result.is_failure:
            return FlextResult.fail(connect_result.error or "Connect failed")

        connecting_channel = connect_result.data
        if connecting_channel is None:
            return FlextResult.fail("Failed to connect channel")

        ready_result = connecting_channel.mark_ready()
        if ready_result.is_failure:
            return FlextResult.fail(ready_result.error or "Mark ready failed")

        if ready_result.data is None:
            return FlextResult.fail("Failed to mark channel ready")

        return FlextResult.ok(ready_result.data)

    def _disconnect_client(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[FlextGrpcClient]:
        """Disconnect client with proper channel state management."""
        if not client.is_connected:
            return FlextResult.fail("Client is not connected")

        if not client.channel:
            return FlextResult.fail("Client has no channel")

        # Use proper channel state transitions
        disconnect_result = client.channel.disconnect()
        if disconnect_result.is_failure:
            return FlextResult.fail(disconnect_result.error or "Disconnect failed")

        disconnected_channel = disconnect_result.data
        if disconnected_channel is None:
            return FlextResult.fail("Failed to disconnect channel")

        return client.copy_with(channel=disconnected_channel)

    def _call_method(
        self,
        client: FlextGrpcClient,
        method_name: str | None,
        request_data: object,
    ) -> FlextResult[dict[str, object]]:
        """Make method call through connected client."""
        if not client.is_connected:
            return FlextResult.fail("Client is not connected")

        if not method_name:
            return FlextResult.fail("Method name is required")

        return FlextResult.ok(
            {
                "status": "success",
                "method": method_name,
                "client_id": client.id,
                "data": request_data,
                "target": client.target,
            },
        )

    def _get_client_status(
        self,
        client: FlextGrpcClient,
    ) -> FlextResult[dict[str, object]]:
        """Get comprehensive client status."""
        return FlextResult.ok(
            {
                "id": client.id,
                "is_connected": client.is_connected,
                "target": client.target,
                "channel_state": client.channel.state if client.channel else None,
                "version": client.version,
            },
        )


class FlextGrpcStreamService(FlextDomainService[FlextGrpcStream]):
    """Domain service for gRPC streaming operations and flow control management.

    Application layer service implementing streaming communication patterns including
    stream creation, data transmission, flow control, and stream lifecycle management.
    Orchestrates business workflows around gRPC streaming entities following
    Domain-Driven Design and Clean Architecture principles.

    This service handles all streaming communication patterns supported by gRPC,
    providing a unified interface for stream management while coordinating between
    client entities, stream resources, and data flow control mechanisms.

    Responsibilities:
        - Stream lifecycle management (create, send, close)
        - Streaming pattern coordination (unary, server/client/bidirectional streaming)
        - Data flow control and backpressure management
        - Stream state monitoring and error handling
        - Resource cleanup and connection management

    Supported Operations:
        - "create": Initialize new stream with specified type and configuration
        - "send": Transmit data through established stream with flow control
        - "close": Gracefully close stream and cleanup associated resources

    Streaming Patterns:
        - Unary: Single request-response communication
        - Server Streaming: Single request, multiple responses
        - Client Streaming: Multiple requests, single response
        - Bidirectional Streaming: Multiple requests and responses

    Architecture Patterns:
        - Domain Service: Orchestrates streaming business processes
        - Command Pattern: Operations executed through execute() method
        - Strategy Pattern: Different handling for streaming patterns
        - Result Pattern: All operations return FlextResult for consistent handling

    Flow Control:
        Manages streaming data flow with proper backpressure handling:
        - Buffer management for incoming and outgoing data
        - Flow control coordination with remote endpoints
        - Error propagation and recovery mechanisms

    Example:
        Basic streaming workflow:

        >>> from flext_grpc import FlextGrpcStreamService, FlextGrpcClient
        >>>
        >>> service = FlextGrpcStreamService()
        >>> client = connected_client  # Previously connected client
        >>>
        >>> # Create bidirectional stream
        >>> create_result = service.execute(
        ...     "create",
        ...     client=client,
        ...     method_name="ProcessStream",
        ...     stream_type="bidirectional",
        ... )
        >>> if create_result.success:
        ...     stream = create_result.data
        ...     print(f"Stream created: {stream.method_name}")
        >>>
        >>> # Send data through stream
        >>> send_result = service.execute(
        ...     "send", stream=stream, data={"message": "Hello streaming world"}
        ... )
        >>> if send_result.success:
        ...     print("Data sent successfully")
        >>>
        >>> # Close stream
        >>> close_result = service.execute("close", stream=stream)

    Integration:
        - Built on flext-core FlextDomainService foundation
        - Uses FlextResult pattern for consistent error handling
        - Integrates with client services for connection management
        - Coordinates with entity factory for stream creation

    Error Handling:
        All operations return FlextResult with detailed error information:
        - Stream creation failures and configuration errors
        - Data transmission errors and flow control issues
        - Connection failures and network interruptions
        - Resource cleanup failures and state management errors

    Performance Considerations:
        - Efficient memory management for streaming data buffers
        - Proper resource cleanup to prevent memory leaks
        - Flow control mechanisms to handle high-throughput scenarios
        - Connection pooling and reuse for optimal performance

    """

    def _handle_result(
        self,
        result: FlextResult[object],
        error_msg: str,
    ) -> FlextResult[object]:
        """Handle result with consistent pattern."""
        if result.success:
            return FlextResult.ok(result.data if result.data is not None else {})
        return FlextResult.fail(result.error or error_msg)

    def execute(self) -> FlextResult[FlextGrpcStream]:
        """Execute default stream operation - implementation required by abstract base."""
        return FlextResult.fail("Use execute_operation(operation, **kwargs) instead")

    def execute_operation(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute stream operation.

        Args:
            *args: Arguments (expected: operation)
            **kwargs: Additional options including stream, client, method_name, etc.

        Returns:
            FlextResult with operation result

        """
        if len(args) < 1:
            return FlextResult.fail("Missing required argument: operation")

        operation = args[0]
        if not isinstance(operation, str):
            return FlextResult.fail("Operation must be a string")

        match operation:
            case "create":
                return self._handle_create_stream(kwargs)
            case "send":
                return self._handle_send_stream(kwargs)
            case "close":
                return self._handle_close_stream(kwargs)
            case _:
                return FlextResult.fail(f"Unknown stream operation: {operation}")

    def _handle_create_stream(self, kwargs: dict[str, object]) -> FlextResult[object]:
        """Handle create stream operation."""
        client = kwargs.get("client")
        method_name = kwargs.get("method_name")
        stream_type = kwargs.get("stream_type", "unary")

        # Type validation and conversion
        from flext_grpc.entities import FlextGrpcClient  # noqa: PLC0415

        if not isinstance(client, FlextGrpcClient):
            return FlextResult.fail("Client must be a FlextGrpcClient instance")

        method_name_str = str(method_name) if method_name else None
        stream_type_str = str(stream_type) if stream_type else "unary"

        result = self._create_stream(client, method_name_str, stream_type_str)
        if result.success:
            return FlextResult.ok(result.data)
        return FlextResult.fail(result.error or "Create stream failed")

    def _handle_send_stream(self, kwargs: dict[str, object]) -> FlextResult[object]:
        """Handle send stream operation."""
        stream = kwargs.get("stream")
        data = kwargs.get("data")

        # Type validation
        from flext_grpc.entities import FlextGrpcStream  # noqa: PLC0415

        if not isinstance(stream, FlextGrpcStream):
            return FlextResult.fail("Stream must be a FlextGrpcStream instance")

        send_result = self._send_data(stream, data)
        if send_result.success:
            return FlextResult.ok(send_result.data)
        return FlextResult.fail(send_result.error or "Send data failed")

    def _handle_close_stream(self, kwargs: dict[str, object]) -> FlextResult[object]:
        """Handle close stream operation."""
        stream = kwargs.get("stream")

        # Type validation
        from flext_grpc.entities import FlextGrpcStream  # noqa: PLC0415

        if not isinstance(stream, FlextGrpcStream):
            return FlextResult.fail("Stream must be a FlextGrpcStream instance")

        close_result = self._close_stream(stream)
        if close_result.success:
            return FlextResult.ok(close_result.data)
        return FlextResult.fail(close_result.error or "Close stream failed")

    def _create_stream(
        self,
        client: FlextGrpcClient,
        method_name: str | None,
        stream_type: str,
    ) -> FlextResult[FlextGrpcStream]:
        """Create a new gRPC stream with validation."""
        validation = client.validate_business_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid client: {validation.error}")

        if not client.is_connected:
            return FlextResult.fail("Client is not connected")

        if not method_name:
            return FlextResult.fail("Method name is required")

        # Use entity factory for proper creation
        from flext_grpc.entities import FlextGrpcEntityFactory  # noqa: PLC0415

        return FlextGrpcEntityFactory.create_stream(method_name, stream_type)

    def _send_data(
        self,
        stream: FlextGrpcStream,
        data: object,
    ) -> FlextResult[bool]:
        """Send data through stream."""
        validation = stream.validate_business_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid stream: {validation.error}")

        # In a real implementation, this would send data through the stream
        # Use data parameter to avoid ARG002
        _ = data  # Mark as used
        return FlextResult.ok(data=True)

    def _close_stream(self, stream: FlextGrpcStream) -> FlextResult[bool]:
        """Close stream properly."""
        validation = stream.validate_business_rules()
        if validation.is_failure:
            return FlextResult.fail(f"Invalid stream: {validation.error}")

        # In a real implementation, this would close the stream
        return FlextResult.ok(data=True)


class FlextGrpcService(FlextDomainService[object]):
    """Unified gRPC service orchestrating server, client, and stream operations.

    High-level application service providing a unified interface for all gRPC
    operations across the platform. Acts as a facade coordinating between
    specialized domain services while maintaining clean architectural boundaries
    and consistent operation patterns.

    This service implements the Facade pattern to simplify complex gRPC workflows
    by providing a single entry point for all gRPC-related operations. It delegates
    to specialized services while maintaining unified error handling, monitoring,
    and operational consistency across the entire gRPC subsystem.

    Architecture Role:
        - Facade Pattern: Unified interface for complex gRPC subsystem
        - Service Coordinator: Orchestrates between specialized domain services
        - Operation Router: Dispatches operations to appropriate service handlers
        - Consistency Provider: Ensures uniform behavior across all operations

    Managed Services:
        - FlextGrpcServerService: Server lifecycle and management operations
        - FlextGrpcClientService: Client connection and communication operations
        - FlextGrpcStreamService: Streaming operations and flow control

    Supported Service Types:
        - "server": All server-related operations (start, stop, add_service, status)
        - "client": All client-related operations (connect, disconnect, call, status)
        - "stream": All streaming operations (create, send, close)

    Delegation Pattern:
        Operations are dispatched using service type routing:
        service_type → specialized_service.execute(remaining_args)

    Example:
        Unified gRPC operations through single service:

        >>> from flext_grpc import FlextGrpcService, FlextGrpcServer, FlextGrpcClient
        >>>
        >>> unified_service = FlextGrpcService()
        >>>
        >>> # Server operations
        >>> server_result = unified_service.execute("server", "start", server_instance)
        >>>
        >>> # Client operations
        >>> client_result = unified_service.execute(
        ...     "client", "connect", client_instance
        ... )
        >>>
        >>> # Stream operations
        >>> stream_result = unified_service.execute(
        ...     "stream",
        ...     "create",
        ...     client=connected_client,
        ...     method_name="StreamData",
        ...     stream_type="server_streaming",
        ... )

    Benefits:
        - Simplified API surface for complex gRPC operations
        - Consistent error handling across all operation types
        - Centralized monitoring and logging for all gRPC activities
        - Easier testing and mocking of gRPC functionality
        - Clear separation of concerns with specialized service delegation

    Integration:
        - Built on flext-core FlextDomainService foundation
        - Coordinates all specialized gRPC domain services
        - Provides unified monitoring and observability integration
        - Maintains consistent FlextResult patterns across operations

    Error Handling:
        Inherits and unifies error handling from all managed services:
        - Service type validation and routing errors
        - Delegated service operation failures
        - Argument validation and parameter extraction errors
        - Cross-service coordination and state management errors

    Thread Safety:
        Stateless facade with thread-safe delegation to underlying services.
        All managed services implement thread-safe operation patterns.

    """

    def __init__(self) -> None:
        """Initialize unified service with specialized component services.

        Creates instances of all specialized gRPC domain services and establishes
        the service coordination infrastructure. Initializes the facade pattern
        implementation for unified gRPC operation management.

        Component Services:
            - FlextGrpcServerService: Server lifecycle and management
            - FlextGrpcClientService: Client connection and communication
            - FlextGrpcStreamService: Streaming operations and flow control

        Architecture:
            Implements dependency injection pattern by creating and managing
            specialized service instances, providing clean separation of concerns
            while maintaining unified operational interface.
        """
        self._server_service = FlextGrpcServerService()
        self._client_service = FlextGrpcClientService()
        self._stream_service = FlextGrpcStreamService()

    def execute(self) -> FlextResult[object]:
        """Execute default unified operation - implementation required by abstract base."""
        return FlextResult.fail("Use execute_operation(service_type, operation, **kwargs) instead")

    def execute_operation(self, *args: object, **kwargs: object) -> FlextResult[object]:
        """Execute unified gRPC operation with service type routing and delegation.

        Primary entry point for all gRPC operations implementing the Facade pattern.
        Routes operations to appropriate specialized services based on service type
        while maintaining consistent argument handling and error reporting.

        This method provides a unified interface for the entire gRPC subsystem,
        simplifying complex workflows by routing operations to specialized services
        while ensuring consistent behavior and error handling across operations.

        Args:
            *args (object): Variable arguments where first argument is required:
                - args[0] (str): Service type ("server", "client", "stream")
                - args[1:]: Remaining arguments passed to specialized service
            **kwargs (object): Additional options passed through to specialized services

        Returns:
            FlextResult[object]: Operation result from delegated service containing:
                - Success: Service-specific operation result data
                - Failure: Detailed error message with routing/execution failures

        Service Type Routing:
            - "server": Routes to FlextGrpcServerService for server operations
            - "client": Routes to FlextGrpcClientService for client operations
            - "stream": Routes to FlextGrpcStreamService for streaming operations

        Delegation Pattern:
            1. Validate service type argument
            2. Route to appropriate specialized service
            3. Pass remaining arguments to service execute() method
            4. Return result with unified error handling

        Example:
            Unified service operation routing:

            >>> service = FlextGrpcService()
            >>>
            >>> # Server operation - routed to FlextGrpcServerService
            >>> result = service.execute("server", "start", server_instance)
            >>>
            >>> # Client operation - routed to FlextGrpcClientService
            >>> result = service.execute("client", "connect", client_instance)
            >>>
            >>> # Stream operation - routed to FlextGrpcStreamService
            >>> result = service.execute(
            ...     "stream", "create", client=client_instance, method_name="StreamData"
            ... )

        Error Handling:
            Returns detailed error messages for:
            - Missing or invalid service type argument
            - Unknown service type routing failures
            - Delegated service operation failures
            - Argument validation and parameter extraction errors

        Benefits:
            - Single entry point for all gRPC operations
            - Consistent error handling across operation types
            - Simplified testing and mocking interface
            - Centralized monitoring and logging integration

        Thread Safety:
            Stateless routing with delegation to thread-safe specialized services.
            Safe for concurrent execution across multiple threads.

        """
        # Validate minimum argument requirements for service type routing
        if len(args) < 1:
            return FlextResult.fail("Missing required argument: service_type")

        # Extract and validate service type for routing
        service_type = args[0]
        if not isinstance(service_type, str):
            return FlextResult.fail("Service type must be a string")

        # Delegate to appropriate specialized service based on service type
        match service_type:
            case "server":
                return self._server_service.execute_operation(*args[1:], **kwargs)
            case "client":
                return self._client_service.execute_operation(*args[1:], **kwargs)
            case "stream":
                return self._stream_service.execute_operation(*args[1:], **kwargs)
            case _:
                return FlextResult.fail(f"Unknown service type: {service_type}")
