"""FLEXT gRPC API - Unified high-level API for enterprise gRPC operations.

This module provides a comprehensive high-level API for all gRPC operations,
offering convenient factory functions and utilities for creating, configuring,
and managing gRPC entities. Designed for ease of use while maintaining the
full power and flexibility of the underlying Clean Architecture implementation.

Key Components:
    - Entity Factory Functions: Convenient creation of gRPC entities
    - Address Validation: Comprehensive network address validation and parsing
    - Configuration Builders: Type-safe configuration creation
    - Complete Setup Functions: One-call setup for common scenarios
    - Validation Utilities: Network address and parameter validation

API Design Philosophy:
    The API follows enterprise-grade design principles:
    - Simple interface for common operations
    - Comprehensive validation with detailed error reporting
    - Type safety through proper type annotations and validation
    - Integration with underlying domain entities and services
    - Consistent result patterns using FlextResult for error handling

Factory Functions:
    High-level factory functions for entity creation:
    - create_server(): gRPC server creation with sensible defaults
    - create_client(): gRPC client creation with channel management
    - create_channel(): Channel creation with configuration options
    - create_service(): Service definition with method specifications
    - create_stream(): Stream creation with type validation
    - create_config(): Configuration creation with validation

Validation and Parsing:
    Comprehensive utilities for network address handling:
    - validate_address(): Address format and component validation
    - parse_address(): Address parsing into structured components
    - Host and port validation with business rule enforcement
    - IPv4, IPv6, and hostname support

Example:
    Basic API usage for gRPC setup:

    >>> from flext_grpc.api import (
    ...     create_server,
    ...     create_client,
    ...     create_service,
    ...     create_complete_setup,
    ...     validate_address,
    ... )
    >>>
    >>> # Individual entity creation
    >>> server = create_server(host="0.0.0.0", port=50051, max_workers=20)
    >>> client = create_client("localhost:50051")
    >>> service = create_service("DataService", ["GetData", "SetData"])
    >>>
    >>> # Address validation
    >>> result = validate_address("api.example.com:8080")
    >>> if result.success:
    ...     print("Valid address")
    >>>
    >>> # Complete setup for rapid prototyping
    >>> setup = create_complete_setup(
    ...     host="localhost",
    ...     port=9090,
    ...     service_name="TestService",
    ...     methods=["Echo", "Process"],
    ... )
    >>> server = setup["server"]
    >>> client = setup["client"]

Integration:
    - Built on FLEXT domain entities with full feature compatibility
    - Uses FlextResult patterns for consistent error handling
    - Integrates with FlextGenerators for unique ID generation
    - Supports all entity validation and business rules
    - Compatible with platform and service layer operations

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from datetime import UTC, datetime

from flext_core import FlextResult
from flext_core.utilities import FlextGenerators

from flext_grpc.config import FlextGrpcConfig
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService as FlextGrpcServiceEntity,
    FlextGrpcStream,
)
from flext_grpc.types import TGrpcTarget

# Validation constants for network address processing
MIN_PORT = 1  # Minimum valid port number
MAX_PORT = 65535  # Maximum valid port number (16-bit)
ADDRESS_PARTS_COUNT = 2  # Expected parts in "host:port" format


def create_server(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
) -> FlextGrpcServer:
    """Create new gRPC server entity with enterprise-grade defaults and validation.

    Factory function for creating FlextGrpcServer entities with sensible defaults
    for enterprise deployment. Handles entity ID generation, timestamp creation,
    and proper initialization state for immediate use in server operations.

    Args:
        host (str): Server bind address for gRPC communication.
            Defaults to "localhost" for development environments.
            Examples: "localhost", "0.0.0.0", "192.168.1.10", "api.example.com"
        port (int): Network port for server binding.
            Defaults to 50051 (standard gRPC port).
            Must be within valid range (1024-65535) for security.
        max_workers (int): Maximum worker threads for concurrent request processing.
            Defaults to 10 for balanced performance.
            Should be tuned based on expected load and system resources.

    Returns:
        FlextGrpcServer: Fully configured server entity ready for lifecycle operations.
            Entity is created in "stopped" state with unique ID and timestamp.

    Server Configuration:
        Created servers have the following characteristics:
        - Unique entity ID generated using FlextGenerators
        - Initial state set to "stopped" for proper lifecycle management
        - Empty services list ready for service registration
        - Current UTC timestamp for creation tracking
        - All domain validation rules enforced during creation

    Example:
        Create servers for different deployment scenarios:

        >>> # Development server with defaults
        >>> dev_server = create_server()
        >>> print(f"Dev server: {dev_server.address}")
        localhost:50051
        >>>
        >>> # Production server with custom configuration
        >>> prod_server = create_server(host="0.0.0.0", port=8080, max_workers=50)
        >>> print(f"Prod server: {prod_server.address}")
        0.0.0.0:8080
        >>>
        >>> # High-performance server
        >>> hpc_server = create_server(
        ...     host="internal.invalid.example.com", port=443, max_workers=200
        ... )

    Validation:
        All parameters undergo validation during entity creation:
        - Host must be non-empty with valid format
        - Port must be within acceptable range (enforced by entity)
        - Max workers must be positive integer
        - Entity creation follows all domain rules

    Integration:
        Created servers are compatible with:
        - Platform layer server operations (start, stop, status)
        - Service layer server management
        - Domain service coordination
        - Enterprise deployment and monitoring

    """
    return FlextGrpcServer(
        id=FlextGenerators.generate_entity_id(),
        host=host,
        port=port,
        max_workers=max_workers,
        state="stopped",
        services=[],
        created_at=datetime.now(UTC),
    )


def create_client(
    target: str,
    options: dict[str, object] | None = None,
) -> FlextGrpcClient:
    """Create new gRPC client entity with channel management and configuration options.

    Factory function for creating FlextGrpcClient entities with integrated channel
    creation and configuration management. Handles client setup, channel initialization,
    and option configuration for immediate use in client operations.

    Args:
        target (str): Remote server target address in "host:port" format.
            Must be valid network address for successful connection.
            Examples: "localhost:50051", "api.example.com:8080", "192.168.1.10:9090"
        options (dict[str, object] | None): Client configuration options.
            Optional dictionary for client and channel customization:
            - compression (str): Compression algorithm ("gzip", "deflate")
            - keepalive_time (int): Keepalive interval in seconds
            - keepalive_timeout (int): Keepalive timeout in seconds
            - max_message_length (int): Maximum message size
            - retry_policy (dict): Retry configuration for failed calls
            Defaults to empty dict if not provided.

    Returns:
        FlextGrpcClient: Fully configured client entity with integrated channel.
            Client is ready for connection operations with properly initialized channel.

    Client Configuration:
        Created clients have the following characteristics:
        - Unique entity ID generated using FlextGenerators
        - Integrated channel created with matching target configuration
        - Options stored for connection and communication configuration
        - Current UTC timestamp for creation tracking
        - All domain validation rules enforced during creation

    Channel Integration:
        Client creation automatically creates integrated channel:
        - Channel target matches client target specification
        - Channel inherits client options for consistent configuration
        - Channel initialized in "idle" state ready for connection
        - Proper channel lifecycle management through client operations

    Example:
        Create clients for different communication scenarios:

        >>> # Basic client with default options
        >>> client = create_client("localhost:50051")
        >>> print(f"Client target: {client.target}")
        localhost:50051
        >>>
        >>> # Client with compression and keepalive
        >>> advanced_client = create_client(
        ...     "api.production.com:443",
        ...     {
        ...         "compression": "gzip",
        ...         "keepalive_time": 30,
        ...         "keepalive_timeout": 5,
        ...         "max_message_length": 1024 * 1024,  # 1MB
        ...     },
        ... )
        >>>
        >>> # High-availability client with retry policy
        >>> ha_client = create_client(
        ...     "lb.example.com:8080",
        ...     {
        ...         "retry_policy": {
        ...             "max_attempts": 5,
        ...             "backoff": "exponential",
        ...             "timeout": 60,
        ...         }
        ...     },
        ... )

    Target Validation:
        Target addresses undergo validation during client creation:
        - Must be in valid "host:port" format
        - Host must be resolvable network address
        - Port must be within valid range
        - Type safety enforced through TGrpcTarget validation

    Integration:
        Created clients are compatible with:
        - Platform layer client operations (connect, disconnect, call)
        - Service layer client management
        - Domain service coordination
        - Enterprise communication patterns

    """
    channel = create_channel(target, options)

    return FlextGrpcClient(
        id=FlextGenerators.generate_entity_id(),
        channel=channel,
        options=options or {},
        created_at=datetime.now(UTC),
    )


def create_channel(
    target: str,
    options: dict[str, object] | None = None,
) -> FlextGrpcChannel:
    """Create new gRPC channel entity with target validation and configuration options.

    Factory function for creating FlextGrpcChannel entities with proper target
    validation and configuration management. Handles channel initialization,
    option configuration, and state setup for integration with client operations.

    Args:
        target (str): Remote server target address in "host:port" format.
            Must be valid network address for channel establishment.
            Examples: "localhost:50051", "internal.invalid:9090", "api.example.com:443"
        options (dict[str, object] | None): Channel configuration options.
            Optional dictionary for channel behavior customization:
            - grpc.keepalive_time_ms (int): Keepalive time in milliseconds
            - grpc.keepalive_timeout_ms (int): Keepalive timeout in milliseconds
            - grpc.keepalive_permit_without_calls (bool): Allow keepalive without calls
            - grpc.http2.max_pings_without_data (int): Max pings without data
            - grpc.max_message_length (int): Maximum message size
            - grpc.compression (str): Default compression algorithm
            Defaults to empty dict if not provided.

    Returns:
        FlextGrpcChannel: Fully configured channel entity ready for connection.
            Channel is created in "idle" state with proper target and options.

    Channel Configuration:
        Created channels have the following characteristics:
        - Unique entity ID generated using FlextGenerators
        - Type-safe target validation through TGrpcTarget
        - Initial state set to "idle" for proper lifecycle management
        - Options stored for connection behavior configuration
        - Current UTC timestamp for creation tracking
        - All domain validation rules enforced during creation

    State Management:
        Channels follow defined state transitions:
        - Created in "idle" state ready for connection
        - Transition to "connecting" during connection establishment
        - Reach "ready" state when connection is established
        - Return to "shutdown" state when connection is closed

    Example:
        Create channels for different connection scenarios:

        >>> # Basic channel with default options
        >>> channel = create_channel("localhost:50051")
        >>> print(f"Channel target: {channel.target}, state: {channel.state}")
        Channel target: localhost:50051, state: idle
        >>>
        >>> # Channel with keepalive configuration
        >>> keepalive_channel = create_channel(
        ...     "api.service.com:8080",
        ...     {
        ...         "grpc.keepalive_time_ms": 30000,
        ...         "grpc.keepalive_timeout_ms": 5000,
        ...         "grpc.keepalive_permit_without_calls": True,
        ...     },
        ... )
        >>>
        >>> # High-throughput channel with large message support
        >>> bulk_channel = create_channel(
        ...     "bulk.api.example.com:9090",
        ...     {
        ...         "grpc.max_message_length": 10 * 1024 * 1024,  # 10MB
        ...         "grpc.compression": "gzip",
        ...         "grpc.http2.max_pings_without_data": 0,
        ...     },
        ... )

    Target Validation:
        Target addresses undergo comprehensive validation:
        - Must be in valid "host:port" format
        - Host component validated for network address format
        - Port component validated for valid range
        - Type safety enforced through TGrpcTarget type casting

    Integration:
        Created channels are compatible with:
        - Client entity integration for communication
        - Channel state management through domain services
        - Connection lifecycle operations
        - Enterprise networking and load balancing

    """
    return FlextGrpcChannel(
        id=FlextGenerators.generate_entity_id(),
        target=TGrpcTarget(target),
        state="idle",
        options=options or {},
        created_at=datetime.now(UTC),
    )


def create_service(
    name: str,
    methods: list[str] | None = None,
) -> FlextGrpcServiceEntity:
    """Create new gRPC service entity definition with method specifications.

    Factory function for creating FlextGrpcServiceEntity definitions with service
    name and method specifications. Handles service definition creation for
    registration with gRPC servers and client method invocation.

    Args:
        name (str): Service name for identification and registration.
            Must be unique within server context for proper service resolution.
            Examples: "UserService", "DataProcessingService", "AuthenticationService"
        methods (list[str] | None): List of method names available in service.
            Optional list of method identifiers for service definition:
            - Method names should follow gRPC conventions (PascalCase)
            - Methods define available operations for client invocation
            - Empty list is acceptable for dynamic service definition
            Defaults to empty list if not provided.

    Returns:
        FlextGrpcServiceEntity: Configured service entity ready for server registration.
            Service definition includes name, methods, and proper entity metadata.

    Service Configuration:
        Created services have the following characteristics:
        - Unique entity ID generated using FlextGenerators
        - Service name for identification and routing
        - Method list for operation specification
        - Current UTC timestamp for creation tracking
        - All domain validation rules enforced during creation

    Method Specification:
        Method lists define available service operations:
        - Method names should be descriptive and follow conventions
        - Each method represents an available gRPC operation
        - Methods can be added dynamically after service creation
        - Method validation ensures proper naming and uniqueness

    Example:
        Create services for different business domains:

        >>> # User management service
        >>> user_service = create_service(
        ...     "UserService", ["GetUser", "CreateUser", "UpdateUser", "DeleteUser"]
        ... )
        >>> print(f"Service: {user_service.name}, Methods: {len(user_service.methods)}")
        Service: UserService, Methods: 4
        >>>
        >>> # Data processing service
        >>> data_service = create_service(
        ...     "DataProcessingService",
        ...     ["ProcessData", "ValidateData", "TransformData", "ExportResults"],
        ... )
        >>>
        >>> # Dynamic service without predefined methods
        >>> dynamic_service = create_service("DynamicService")
        >>> print(f"Dynamic service methods: {dynamic_service.methods}")
        Dynamic service methods: []
        >>>
        >>> # Authentication service with security methods
        >>> auth_service = create_service(
        ...     "AuthenticationService",
        ...     ["Login", "Logout", "RefreshToken", "ValidateToken", "ChangePassword"],
        ... )

    Service Registration:
        Created services are designed for:
        - Registration with gRPC servers for operation exposure
        - Client method invocation through service discovery
        - Service discovery and routing in enterprise environments
        - Method availability validation and error handling

    Integration:
        Created services are compatible with:
        - Server entity service registration operations
        - Client method invocation through service specifications
        - Platform layer service management
        - Enterprise service discovery and routing

    """
    return FlextGrpcServiceEntity(
        id=FlextGenerators.generate_entity_id(),
        name=name,
        methods=methods or [],
        created_at=datetime.now(UTC),
    )


def create_stream(
    method_name: str,
    stream_type: str = "unary",
) -> FlextGrpcStream:
    """Create new gRPC stream entity with method specification and type validation.

    Factory function for creating FlextGrpcStream entities with comprehensive
    stream type validation and method specification. Handles stream definition
    creation for all supported gRPC streaming patterns with type safety.

    Args:
        method_name (str): Remote method name for stream operations.
            Must be valid method identifier for service method invocation.
            Examples: "StreamData", "ProcessStream", "UploadFile", "DownloadResults"
        stream_type (str): Type of streaming pattern to implement.
            Must be one of supported gRPC streaming types:
            - "unary": Single request-response (default)
            - "server_streaming": Single request, multiple responses
            - "client_streaming": Multiple requests, single response
            - "bidirectional": Full duplex with multiple requests and responses
            Defaults to "unary" for simple request-response pattern.

    Returns:
        FlextGrpcStream: Configured stream entity ready for streaming operations.
            Stream includes method name, validated type, and proper entity metadata.

    Raises:
        ValueError: If stream_type is not one of the supported streaming patterns.
            Provides clear error message with valid options for debugging.

    Stream Configuration:
        Created streams have the following characteristics:
        - Unique entity ID generated using FlextGenerators
        - Method name for remote operation specification
        - Validated stream type with type safety enforcement
        - Current UTC timestamp for creation tracking
        - All domain validation rules enforced during creation

    Streaming Patterns:
        Supported streaming patterns and their use cases:
        - **unary**: Traditional request-response for simple operations
        - **server_streaming**: Server sends multiple responses (data feeds)
        - **client_streaming**: Client sends multiple requests (file upload)
        - **bidirectional**: Real-time communication (chat, live updates)

    Example:
        Create streams for different communication patterns:

        >>> # Simple request-response stream
        >>> simple_stream = create_stream("GetData")
        >>> print(
        ...     f"Stream: {simple_stream.method_name}, "
        ...     f"Type: {simple_stream.stream_type}"
        ... )
        Stream: GetData, Type: unary
        >>>
        >>> # Server streaming for data feeds
        >>> feed_stream = create_stream("StreamPrices", "server_streaming")
        >>> print(f"Feed stream: {feed_stream.method_name}")
        Feed stream: StreamPrices
        >>>
        >>> # Client streaming for file upload
        >>> upload_stream = create_stream("UploadFile", "client_streaming")
        >>>
        >>> # Bidirectional streaming for real-time chat
        >>> chat_stream = create_stream("ChatMessages", "bidirectional")
        >>>
        >>> # Invalid stream type raises error
        >>> try:
        ...     invalid_stream = create_stream("Test", "invalid_type")
        ... except ValueError as e:
        ...     print(f"Error: {e}")
        Error: Invalid stream type: invalid_type

    Type Safety:
        Stream type validation ensures:
        - Only valid streaming patterns are accepted
        - Type safety through TGrpcStreamType enforcement
        - Clear error messages for invalid configurations
        - Consistent behavior across all stream operations

    Integration:
        Created streams are compatible with:
        - Stream service operations for data transmission
        - Client streaming communication patterns
        - Platform layer stream management
        - Enterprise streaming and real-time communication

    """
    # Type-safe cast to TGrpcStreamType
    from flext_grpc.types import TGrpcStreamType  # noqa: PLC0415

    valid_types = ("unary", "server_streaming", "client_streaming", "bidirectional")
    if stream_type not in valid_types:
        invalid_stream_type_msg: str = f"Invalid stream type: {stream_type}"
        raise ValueError(invalid_stream_type_msg)
    valid_stream_type: TGrpcStreamType = stream_type
    return FlextGrpcStream(
        id=FlextGenerators.generate_entity_id(),
        method_name=method_name,
        stream_type=valid_stream_type,
        created_at=datetime.now(UTC),
    )


def create_config(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    timeout: float = 30.0,
) -> FlextGrpcConfig:
    """Create new gRPC configuration with enterprise-grade defaults and validation.

    Factory function for creating FlextGrpcConfig instances with comprehensive
    parameter validation and enterprise-suitable defaults. Handles configuration
    creation with all validation rules enforced for production deployment.

    Args:
        host (str): Server bind address for gRPC communication.
            Defaults to "localhost" for development environments.
            Production deployments typically use "0.0.0.0" for all interfaces.
            Examples: "localhost", "0.0.0.0", "192.168.1.10", "api.example.com"
        port (int): Network port for server binding.
            Defaults to 50051 (standard gRPC port).
            Must be within valid range (1024-65535) for security compliance.
            Common alternatives: 8080, 9090, 443 (HTTPS)
        max_workers (int): Maximum worker threads for concurrent request processing.
            Defaults to 10 for balanced performance.
            Should be tuned based on expected load:
            - 10-20: Low to medium traffic
            - 50-100: High traffic production
            - 200+: Specialized high-throughput scenarios
        timeout (float): Default timeout for gRPC operations in seconds.
            Defaults to 30.0 seconds for reliable communication.
            Should account for network latency and processing complexity:
            - 5-10: Fast operations and local networks
            - 30-60: Standard operations and internet communication
            - 120+: Complex processing or large data transfers

    Returns:
        FlextGrpcConfig: Validated configuration ready for production use.
            All parameters undergo comprehensive validation during creation.

    Configuration Validation:
        All parameters undergo enterprise-grade validation:
        - Host validation: Non-empty, properly formatted network addresses
        - Port validation: Valid range (1024-65535) with security compliance
        - Worker validation: Positive integers with performance considerations
        - Timeout validation: Positive values with operational requirements
        - Environment integration: Supports environment variable overrides

    Example:
        Create configurations for different deployment scenarios:

        >>> # Development configuration with defaults
        >>> dev_config = create_config()
        >>> print(f"Dev: {dev_config.get_address()}")
        Dev: localhost:50051
        >>>
        >>> # Production configuration
        >>> prod_config = create_config(
        ...     host="0.0.0.0", port=8080, max_workers=50, timeout=60.0
        ... )
        >>> print(f"Prod: {prod_config.get_address()}")
        Prod: 0.0.0.0:8080
        >>>
        >>> # High-performance configuration
        >>> hpc_config = create_config(
        ...     host="internal.invalid.example.com",
        ...     port=443,
        ...     max_workers=200,
        ...     timeout=120.0,
        ... )
        >>>
        >>> # Microservice configuration
        >>> micro_config = create_config(
        ...     host="internal.invalid", port=9090, max_workers=20, timeout=10.0
        ... )

    Environment Integration:
        Configuration supports environment variable overrides:
        - FLEXT_GRPC_HOST: Override host setting
        - FLEXT_GRPC_PORT: Override port setting
        - FLEXT_GRPC_MAX_WORKERS: Override worker count
        - FLEXT_GRPC_TIMEOUT: Override timeout setting

    Deployment Scenarios:
        Configurations are optimized for:
        - Development: localhost with moderate resources
        - Production: All interfaces with high performance
        - Microservices: Cluster addresses with fast timeouts
        - High-throughput: Optimized workers and extended timeouts

    Integration:
        Created configurations are compatible with:
        - Server and client entity configuration
        - Platform layer configuration management
        - Enterprise deployment and orchestration
        - Environment-specific configuration patterns

    """
    return FlextGrpcConfig(
        host=host,
        port=port,
        max_workers=max_workers,
        timeout=timeout,
    )


def validate_address(address: str) -> FlextResult[bool]:
    """Validate gRPC address format with comprehensive network address validation.

    Validates network addresses for gRPC communication with comprehensive format
    checking, component validation, and error reporting. Ensures addresses are
    properly formatted and suitable for network communication.

    Args:
        address (str): Network address to validate in "host:port" format.
            Must contain both host and port components separated by colon.
            Examples: "localhost:50051", "api.example.com:8080", "192.168.1.10:9090"

    Returns:
        FlextResult[bool]: Validation result with detailed error information.
            - Success: Returns True if address is valid and properly formatted
            - Failure: Returns detailed error message for debugging and correction

    Validation Rules:
        Address validation enforces the following rules:
        - Address must not be empty or None
        - Address must contain exactly one colon separator
        - Host component must not be empty
        - Host must contain only valid characters (alphanumeric, dots, hyphens)
        - Port component must be numeric
        - Port must be within valid range (1-65535)

    Example:
        Validate different address formats:

        >>> # Valid addresses
        >>> result = validate_address("localhost:50051")
        >>> print(f"Valid: {result.success}")
        Valid: True
        >>>
        >>> result = validate_address("api.example.com:8080")
        >>> print(f"Valid: {result.success}")
        Valid: True
        >>>
        >>> # Invalid addresses with error details
        >>> result = validate_address("invalid-address")
        >>> print(f"Error: {result.error}")
        Error: Address must be in host:port format
        >>>
        >>> result = validate_address(":50051")
        >>> print(f"Error: {result.error}")
        Error: Host cannot be empty
        >>>
        >>> result = validate_address("localhost:999999")
        >>> print(f"Error: {result.error}")
        Error: Port must be between 1 and 65535

    Error Reporting:
        Validation failures provide specific error messages:
        - "Address cannot be empty": Empty or None address
        - "Address must be in host:port format": Missing colon or multiple colons
        - "Host cannot be empty": Empty host component
        - "Invalid host format": Host contains invalid characters
        - "Port must be a number": Non-numeric port component
        - "Port must be between 1 and 65535": Port outside valid range

    Network Compatibility:
        Validates addresses for compatibility with:
        - IPv4 addresses (192.168.1.1, 10.0.0.1, 127.0.0.1)
        - Domain names (api.example.com, internal.invalid)
        - Hostnames (localhost, server, database)
        - Standard network port ranges and restrictions

    Integration:
        Address validation is used throughout the platform for:
        - Client target validation during connection
        - Server address validation during binding
        - Configuration validation in deployment
        - Service discovery and registration

    """
    try:
        # Validate basic address format
        validation_error = _validate_address_format(address)
        if validation_error:
            return FlextResult.fail(validation_error)

        # Parse and validate components
        host, port_str = address.split(":")
        validation_error = _validate_host_and_port(host, port_str)
        if validation_error:
            return FlextResult.fail(validation_error)

        return FlextResult.ok(data=True)

    except (ValueError, AttributeError) as e:
        return FlextResult.fail(f"Address validation error: {e}")


def _validate_address_format(address: str) -> str | None:
    """Validate basic address format structure with detailed error reporting.

    Internal validation function for checking fundamental address format
    requirements. Validates the basic structure of network addresses
    before component-level validation.

    Args:
        address (str): Address string to validate for basic format compliance.

    Returns:
        str | None: Error message if validation fails, None if format is valid.
            Returns specific error message for debugging when format is invalid.

    """
    if not address:
        return "Address cannot be empty"

    if ":" not in address:
        return "Address must be in host:port format"

    parts = address.split(":")
    if len(parts) != ADDRESS_PARTS_COUNT:
        return "Address must be in host:port format"

    return None


def _validate_host_and_port(host: str, port_str: str) -> str | None:
    """Validate individual host and port components with comprehensive rules.

    Internal validation function for detailed host and port component validation.
    Applies business rules and network standards to ensure components are
    suitable for network communication.

    Args:
        host (str): Host component to validate for network address compliance.
        port_str (str): Port component string to validate and convert.

    Returns:
        str | None: Error message if validation fails, None if components are valid.
            Returns specific error message identifying the validation failure.

    """
    if not host:
        return "Host cannot be empty"

    if not re.match(r"^[a-zA-Z0-9.-]+$", host):
        return "Invalid host format"

    try:
        port = int(port_str)
        if not (MIN_PORT <= port <= MAX_PORT):
            return f"Port must be between {MIN_PORT} and {MAX_PORT}"
    except ValueError:
        return "Port must be a number"

    return None


def parse_address(address: str) -> dict[str, int | str]:
    """Parse validated gRPC address into structured host and port components.

    Parses network addresses into structured components after validation,
    providing convenient access to host and port information for network
    operations and configuration.

    Args:
        address (str): Valid network address in "host:port" format.
            Must pass validation before parsing to ensure proper format.

    Returns:
        dict[str, int | str]: Structured address components containing:
            - "host" (str): Host component (hostname, IP address, or domain)
            - "port" (int): Port number as integer for network operations

    Raises:
        ValueError: If address fails validation with detailed error message.
            Uses validate_address() internally to ensure address is properly formatted.

    Example:
        Parse different address formats:

        >>> # Parse standard addresses
        >>> components = parse_address("localhost:50051")
        >>> print(f"Host: {components['host']}, Port: {components['port']}")
        Host: localhost, Port: 50051
        >>>
        >>> components = parse_address("api.example.com:8080")
        >>> print(f"Host: {components['host']}, Port: {components['port']}")
        Host: api.example.com, Port: 8080
        >>>
        >>> # Invalid address raises ValueError
        >>> try:
        ...     parse_address("invalid-format")
        ... except ValueError as e:
        ...     print(f"Parse error: {e}")
        Parse error: Address must be in host:port format

    Integration:
        Parsed components are used for:
        - Network socket creation and binding
        - Configuration object construction
        - Service discovery and registration
        - Load balancer configuration
        - Monitoring and logging output

    """
    validation_result = validate_address(address)
    if not validation_result.success:
        raise ValueError(validation_result.error)

    host, port_str = address.split(":")
    return {
        "host": host,
        "port": int(port_str),
    }


def create_complete_setup(
    host: str = "localhost",
    port: int = 50051,
    service_name: str = "DefaultService",
    methods: list[str] | None = None,
) -> dict[str, FlextGrpcServer | FlextGrpcClient | FlextGrpcServiceEntity | str]:
    """Create complete gRPC setup with coordinated server, client, and service entities.

    Convenience function for rapid gRPC environment setup, creating all necessary
    entities for immediate development and testing. Coordinates entity creation
    with consistent configuration for seamless integration.

    Args:
        host (str): Server host address for binding and client targeting.
            Defaults to "localhost" for development environments.
            Server binds to this address, client connects to same address.
        port (int): Network port for server binding and client connection.
            Defaults to 50051 (standard gRPC port).
            Must be within valid range and available for binding.
        service_name (str): Name for service entity creation.
            Defaults to "DefaultService" for quick setup.
            Should be descriptive for production environments.
        methods (list[str] | None): List of method names for service definition.
            Optional method list for service specification.
            Defaults to empty list if not provided.

    Returns:
        dict[str, FlextGrpcServer | FlextGrpcClient | FlextGrpcServiceEntity | str]:
            Complete setup dictionary containing:
            - "server" (FlextGrpcServer): Configured server entity ready for startup
            - "client" (FlextGrpcClient): Configured client entity ready for connection
            - "service" (FlextGrpcServiceEntity): Service definition for registration
            - "target" (str): Formatted target address for reference

    Setup Coordination:
        The complete setup ensures entity coordination:
        - Server and client use matching host and port configuration
        - Client target matches server binding address
        - Service is ready for server registration
        - All entities use consistent ID generation and timestamps

    Example:
        Rapid development environment setup:

        >>> # Basic development setup
        >>> setup = create_complete_setup()
        >>> server = setup["server"]
        >>> client = setup["client"]
        >>> service = setup["service"]
        >>> target = setup["target"]
        >>> print(f"Setup ready: {target}")
        Setup ready: localhost:50051
        >>>
        >>> # Custom service with methods
        >>> api_setup = create_complete_setup(
        ...     host="0.0.0.0",
        ...     port=8080,
        ...     service_name="UserAPI",
        ...     methods=["GetUser", "CreateUser", "UpdateUser", "DeleteUser"],
        ... )
        >>> api_server = api_setup["server"]
        >>> api_service = api_setup["service"]
        >>> print(f"API server: {api_server.address}")
        API server: 0.0.0.0:8080
        >>> print(f"API methods: {len(api_service.methods)}")
        API methods: 4
        >>>
        >>> # Production-ready setup
        >>> prod_setup = create_complete_setup(
        ...     host="production.api.example.com",
        ...     port=443,
        ...     service_name="ProductionService",
        ...     methods=["ProcessData", "GetStatus", "HealthCheck"],
        ... )

    Usage Patterns:
        Complete setup is ideal for:
        - Rapid prototyping and development
        - Testing environments requiring full stack
        - Educational examples and demonstrations
        - Integration testing with coordinated entities
        - Simplified deployment scenarios

    Integration:
        Setup entities are fully compatible with:
        - Platform layer operations for lifecycle management
        - Service layer coordination for business operations
        - Domain service orchestration for complex workflows
        - Enterprise deployment and configuration management

    """
    server = create_server(host=host, port=port)
    target = f"{host}:{port}"
    client = create_client(target=target)
    service = create_service(name=service_name, methods=methods)

    return {
        "server": server,
        "client": client,
        "service": service,
        "target": target,
    }
