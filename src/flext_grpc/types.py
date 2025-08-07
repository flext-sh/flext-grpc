"""FLEXT gRPC Types - Comprehensive type definitions and protocols for enterprise gRPC.

This module provides the complete type system for the FLEXT gRPC platform,
including domain-specific types, communication protocols, state definitions,
and validation utilities. Designed for type safety, protocol compliance,
and enterprise-grade gRPC operations.

Type System Overview:
    The FLEXT gRPC type system provides comprehensive type safety:
    - Domain Types: Business-specific type definitions with semantic meaning
    - Communication Types: Network and service communication specifications
    - State Types: Lifecycle and operational state definitions
    - Configuration Types: Type-safe configuration and validation
    - Protocol Definitions: Integration contracts with gRPC libraries
    - Validation Functions: Type-safe validation and parsing utilities

Architecture Integration:
    Types are designed to integrate seamlessly with Clean Architecture:
    - Domain Layer: Business entity type definitions and validation
    - Application Layer: Service communication and coordination types
    - Infrastructure Layer: gRPC library integration protocols
    - Interface Layer: API type safety and validation

Type Safety Benefits:
    - Compile-time type checking with mypy and similar tools
    - IDE support with autocomplete and error detection
    - Runtime validation through protocol checking
    - Clear semantic meaning through NewType definitions
    - Consistent behavior across the entire platform

Example:
    Using FLEXT gRPC types for type-safe development:

    >>> from flext_grpc.types import (
    ...     TGrpcTarget,
    ...     TGrpcChannelState,
    ...     TGrpcStreamType,
    ...     flext_grpc_validate_target,
    ...     flext_grpc_parse_target,
    ... )
    >>>
    >>> # Type-safe target creation
    >>> target: TGrpcTarget = TGrpcTarget("api.example.com:50051")
    >>> if flext_grpc_validate_target(target):
    ...     host, port = flext_grpc_parse_target(target)
    ...     print(f"Connecting to {host}:{port}")
    >>>
    >>> # State type safety
    >>> channel_state: TGrpcChannelState = "ready"
    >>> stream_type: TGrpcStreamType = "bidirectional"
    >>>
    >>> # Protocol checking for library integration
    >>> from grpc import Channel
    >>> if isinstance(channel_obj, TGrpcChannel):
    ...     channel_obj.close()  # Type-safe protocol usage

Integration:
    - Integrated with all FLEXT gRPC entities for type consistency
    - Compatible with gRPC Python libraries through protocol definitions
    - Supports mypy and other type checkers for static analysis
    - Enables IDE support for development productivity

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

import re
from typing import Literal, NewType, Protocol, runtime_checkable

from flext_core import get_logger

# Network validation constants for port range enforcement
MIN_PORT = 1  # Minimum valid port number (system minimum)
MAX_PORT = 65535  # Maximum valid port number (16-bit maximum)

# =============================================================================
# DOMAIN TYPES - Clean and focused
# =============================================================================

# Communication Types - Network and service communication specifications
TGrpcTarget = NewType("TGrpcTarget", str)  # Network target in "host:port" format
TGrpcMethodName = NewType("TGrpcMethodName", str)  # gRPC method name for service calls
TGrpcServiceName = NewType(
    "TGrpcServiceName",
    str,
)  # Service identifier for registration

# State Types - Lifecycle and operational state definitions
TGrpcChannelState = Literal[
    "idle",  # Channel created but not connected
    "connecting",  # Connection establishment in progress
    "ready",  # Channel ready for communication
    "transient_failure",  # Temporary connection failure
    "shutdown",  # Channel closed and unusable
]

TGrpcServerState = Literal[
    "stopped",  # Server not running, can be started
    "starting",  # Server startup in progress
    "running",  # Server active and accepting requests
    "stopping",  # Server shutdown in progress
]

TGrpcStreamType = Literal[
    "unary",  # Single request-response communication
    "server_streaming",  # Single request, multiple responses
    "client_streaming",  # Multiple requests, single response
    "bidirectional",  # Full duplex communication
]

# Configuration Types - Type-safe configuration parameters
TGrpcHost = NewType("TGrpcHost", str)  # Network host address (hostname, IP)
TGrpcPort = NewType("TGrpcPort", int)  # Network port number (1-65535)
TGrpcTimeout = NewType("TGrpcTimeout", float)  # Operation timeout in seconds

# =============================================================================
# PROTOCOLS - For gRPC library integration
# =============================================================================


@runtime_checkable
class TGrpcChannel(Protocol):
    """Protocol definition for gRPC channel objects with lifecycle management.

    Protocol defining the interface contract for gRPC channel implementations,
    ensuring compatibility with standard gRPC Python libraries while providing
    type safety and clear behavioral contracts.

    This protocol enables duck typing with actual gRPC channel objects while
    maintaining type safety and enabling proper integration testing through
    mock implementations that satisfy the protocol contract.

    Methods:
        close(): Graceful channel closure with resource cleanup
        unsubscribe(): Callback management for channel state monitoring

    Usage:
        Used for type checking and protocol compliance validation:
        >>> from grpc import insecure_channel
        >>> channel = insecure_channel("localhost:50051")
        >>> assert isinstance(channel, TGrpcChannel)  # Protocol compliance
        >>> channel.close()  # Type-safe method access

    """

    def close(self) -> None:
        """Close the gRPC channel gracefully with proper resource cleanup.

        Initiates graceful channel shutdown, closing all active connections
        and releasing associated resources. Should be called when channel
        is no longer needed to prevent resource leaks.
        """

    def unsubscribe(self, callback: object) -> None:
        """Unsubscribe callback from channel state change notifications.

        Removes previously registered callback from channel state monitoring,
        preventing further notifications when channel state changes. Used
        for cleanup in connection management scenarios.

        Args:
            callback (object): Previously registered callback to remove.

        """


@runtime_checkable
class TGrpcServer(Protocol):
    """Protocol definition for gRPC server objects with service management.

    Protocol defining the interface contract for gRPC server implementations,
    ensuring compatibility with standard gRPC Python libraries while providing
    type safety and clear operational contracts.

    This protocol enables integration with actual gRPC server objects while
    maintaining type safety and enabling comprehensive testing through mock
    implementations that satisfy the protocol requirements.

    Methods:
        add_generic_rpc_handlers(): Service registration and handler management
        start(): Server startup and initialization
        stop(): Graceful server shutdown with optional grace period

    Usage:
        Used for server lifecycle management with type safety:
        >>> from grpc import server
        >>> from concurrent.futures import ThreadPoolExecutor
        >>> grpc_server = server(ThreadPoolExecutor(max_workers=10))
        >>> assert isinstance(grpc_server, TGrpcServer)  # Protocol compliance
        >>> grpc_server.start()  # Type-safe server operations

    """

    def add_generic_rpc_handlers(self, handlers: list[object]) -> None:
        """Add gRPC service handlers to server for request processing.

        Registers service implementations with the server, enabling request
        routing and processing for registered gRPC services. Handlers define
        the available methods and their implementations.

        Args:
            handlers (list[object]): List of gRPC service handler objects
                implementing the service methods and request processing logic.

        """

    def start(self) -> None:
        """Start the gRPC server and begin accepting client connections.

        Initiates server startup sequence, binding to configured address,
        starting worker threads, and beginning request acceptance. Server
        becomes ready to process client requests after successful startup.
        """

    def stop(self, grace: float | None) -> None:
        """Stop the gRPC server gracefully with optional grace period.

        Initiates server shutdown sequence, stopping acceptance of new
        connections and allowing existing requests to complete within
        the specified grace period before forcing termination.

        Args:
            grace (float | None): Maximum time in seconds to wait for
                active requests to complete. None for immediate shutdown.

        """


@runtime_checkable
class TGrpcStub(Protocol):
    """Protocol definition for gRPC client stub objects with channel integration.

    Protocol defining the interface contract for gRPC client stub implementations,
    ensuring compatibility with generated gRPC stub classes while providing
    type safety and clear initialization contracts.

    This protocol enables type-safe integration with generated gRPC stubs
    while maintaining flexibility for testing and mock implementations
    that satisfy the protocol requirements.

    Initialization:
        __init__(): Stub creation with channel dependency injection

    Usage:
        Used for type-safe stub creation and method invocation:
        >>> from myservice_pb2_grpc import MyServiceStub
        >>> from grpc import insecure_channel
        >>> channel = insecure_channel("localhost:50051")
        >>> stub = MyServiceStub(channel)
        >>> assert isinstance(stub, TGrpcStub)  # Protocol compliance
    """

    def __init__(self, channel: TGrpcChannel) -> None:
        """Initialize gRPC client stub with channel for server communication.

        Creates client stub instance with provided channel for remote
        service method invocation. Stub provides typed methods for
        calling remote gRPC service operations.

        Args:
            channel (TGrpcChannel): gRPC channel for server communication.
                Must be properly configured channel ready for connection.

        """


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================


def flext_grpc_validate_target(target: str) -> bool:
    """Validate gRPC target format with comprehensive network address validation.

    Validates network target addresses for gRPC communication, ensuring proper
    format, valid host specification, and acceptable port ranges. Provides
    robust validation for network connectivity and security compliance.

    Args:
        target (str): Network target address to validate in "host:port" format.
            Must contain valid host and port components for network communication.

    Returns:
        bool: True if target is valid and suitable for gRPC communication,
            False if target format or components are invalid.

    Validation Rules:
        - Target must be non-empty string with colon separator
        - Host component must be non-empty with valid characters
        - Host must contain only alphanumeric characters, dots, and hyphens
        - Port component must be numeric and within valid range (1-65535)
        - Format must be exactly "host:port" with single colon

    Example:
        Validate different target formats:

        >>> # Valid targets
        >>> assert flext_grpc_validate_target("localhost:50051") == True
        >>> assert flext_grpc_validate_target("api.example.com:8080") == True
        >>> assert flext_grpc_validate_target("192.168.1.10:9090") == True
        >>>
        >>> # Invalid targets
        >>> assert flext_grpc_validate_target("") == False
        >>> assert flext_grpc_validate_target("invalid-format") == False
        >>> assert flext_grpc_validate_target(":50051") == False
        >>> assert flext_grpc_validate_target("localhost:999999") == False

    Network Compatibility:
        Validates targets for compatibility with:
        - IPv4 addresses and standard hostnames
        - Domain names and fully qualified domain names
        - Standard network port ranges and restrictions
        - gRPC communication requirements and protocols

    Integration:
        Used throughout the platform for:
        - Client target validation during connection setup
        - Configuration validation in deployment scenarios
        - Service discovery and registration validation
        - Network address parsing and processing

    """
    if not target or ":" not in target:
        return False

    try:
        host, port_str = target.split(":", 1)
        if not host or not port_str:
            return False

        # Basic hostname validation
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            return False

        # Port validation
        port = int(port_str)
        return MIN_PORT <= port <= MAX_PORT

    except (ValueError, AttributeError) as e:
        # EXPLICIT TRANSPARENCY: gRPC target validation fallback
        logger = get_logger(__name__)
        logger.debug(f"Target validation failed for '{target}': {type(e).__name__}: {e}")
        logger.info("Returning False for invalid target format - expected behavior")
        return False


def flext_grpc_parse_target(target: str) -> tuple[str, int] | None:
    """Parse validated gRPC target into structured host and port components.

    Parses network target addresses into structured components after validation,
    providing convenient access to host and port information for network
    operations, configuration, and connection establishment.

    Args:
        target (str): Network target address to parse in "host:port" format.
            Must be valid target that passes flext_grpc_validate_target() check.

    Returns:
        tuple[str, int] | None: Parsed components if target is valid:
            - tuple[0] (str): Host component (hostname, IP address, domain)
            - tuple[1] (int): Port number as integer for network operations
            Returns None if target validation fails.

    Parsing Process:
        1. Validates target format using flext_grpc_validate_target()
        2. Splits target on colon separator into host and port
        3. Converts port component to integer for network usage
        4. Returns structured tuple for convenient access

    Example:
        Parse different target formats:

        >>> # Parse valid targets
        >>> host, port = flext_grpc_parse_target("localhost:50051")
        >>> print(f"Host: {host}, Port: {port}")
        Host: localhost, Port: 50051
        >>>
        >>> result = flext_grpc_parse_target("api.example.com:8080")
        >>> if result:
        ...     host, port = result
        ...     print(f"Connecting to {host}:{port}")
        Connecting to api.example.com:8080
        >>>
        >>> # Invalid targets return None
        >>> result = flext_grpc_parse_target("invalid-format")
        >>> assert result is None

    Error Handling:
        Returns None for invalid targets rather than raising exceptions,
        enabling graceful error handling and validation workflows in
        calling code without exception management overhead.

    Integration:
        Parsed components are used for:
        - Network socket creation and connection establishment
        - Configuration object construction and validation
        - Service discovery and registration processing
        - Load balancer configuration and routing
        - Monitoring and logging output formatting

    """
    if not flext_grpc_validate_target(target):
        return None

    host, port_str = target.split(":", 1)
    return (host, int(port_str))
