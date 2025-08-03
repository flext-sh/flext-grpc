"""FLEXT gRPC Errors - Enterprise error hierarchy with comprehensive context.

This module provides a comprehensive error hierarchy for the FLEXT gRPC platform,
extending the flext-core error foundation with domain-specific error types.
Designed for precise error handling, debugging support, and enterprise-grade
error reporting across all gRPC operations.

Error Hierarchy Design:
    The FLEXT gRPC error system follows Clean Architecture principles:
    - Minimal duplication: Extends flext-core errors rather than recreating
    - Domain-specific context: Adds gRPC-specific error information
    - Consistent patterns: Maintains error handling consistency across platform
    - Rich context: Provides detailed information for debugging and monitoring
    - Type safety: Enables proper exception handling and error classification

Error Categories:
    - FlextGrpcError: Base error for all gRPC-specific exceptions
    - FlextGrpcValidationError: Field validation failures with context
    - FlextGrpcConnectionError: Network connection and communication errors
    - FlextGrpcTimeoutError: Operation timeout and deadline violations
    - FlextGrpcConfigurationError: Configuration validation and setup errors

Contextual Information:
    Each error type provides relevant context:
    - Validation errors include field names and validation rules
    - Configuration errors include keys and invalid values
    - Connection errors include channel and network context
    - Timeout errors include deadline and operation context

Example:
    Comprehensive error handling with context:

    >>> from flext_grpc.errors import (
    ...     FlextGrpcValidationError,
    ...     FlextGrpcConnectionError,
    ...     FlextGrpcConfigurationError,
    ... )
    >>>
    >>> try:
    ...     # Configuration validation
    ...     config = FlextGrpcConfig(port=-1)
    ... except FlextGrpcConfigurationError as e:
    ...     print(f"Config error in {e.config_key}: {e.message}")
    ...     print(f"Invalid value: {e.config_value}")
    >>>
    >>> try:
    ...     # Field validation
    ...     server = FlextGrpcServer(host="")
    ... except FlextGrpcValidationError as e:
    ...     print(f"Validation error in field {e.field_name}: {e.message}")
    >>>
    >>> try:
    ...     # Connection handling
    ...     client.connect()
    ... except FlextGrpcConnectionError as e:
    ...     print(f"Connection failed: {e.message}")

Integration:
    - Built on flext-core error foundation for ecosystem consistency
    - Provides gRPC-specific context while maintaining base functionality
    - Supports enterprise error reporting and monitoring systems
    - Enables precise error handling and recovery mechanisms

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_core import (
    FlextConfigurationError,
    FlextConnectionError,
    FlextError,
    FlextTimeoutError,
    FlextValidationError,
)

# =============================================================================
# MINIMAL GRPC-SPECIFIC ERRORS - NO DUPLICATION
# =============================================================================


class FlextGrpcError(FlextError):
    """Base exception for all FLEXT gRPC platform errors.

    Root exception class for the FLEXT gRPC error hierarchy, providing
    a common base for all gRPC-specific exceptions. Extends the flext-core
    FlextError foundation while enabling specific gRPC error handling.

    This base class enables comprehensive error handling patterns:
    - Catch all gRPC errors with single exception type
    - Maintain consistency with flext-core error patterns
    - Enable error classification and routing
    - Support enterprise error monitoring and reporting

    Usage:
        Use as base for all gRPC-specific exceptions or catch-all:

        >>> try:
        ...     grpc_operation()
        ... except FlextGrpcError as e:
        ...     logger.error(f"gRPC operation failed: {e}")
        ...     # Handle any gRPC-related error

    Error Hierarchy:
        All FLEXT gRPC exceptions inherit from this base class,
        enabling both specific and general error handling patterns
        depending on application requirements.
    """


class FlextGrpcValidationError(FlextValidationError):
    """gRPC validation error with comprehensive field context and validation details.

    Specialized validation error for gRPC entity and configuration validation
    failures. Provides detailed context about validation failures including
    field names, validation rules, and error details for debugging and
    user feedback.

    This error type enables precise validation error handling:
    - Field-specific error identification and reporting
    - Detailed validation rule information
    - User-friendly error messages for configuration issues
    - Developer-focused debugging information

    Attributes:
        field_name (str | None): Name of the field that failed validation.
            Provides context for identifying specific validation failures.
            None when validation error is not field-specific.

    Example:
        Field validation error handling:

        >>> try:
        ...     server = FlextGrpcServer(host="", port=50051)
        ... except FlextGrpcValidationError as e:
        ...     if e.field_name:
        ...         print(f"Validation failed for field '{e.field_name}': {e}")
        ...     else:
        ...         print(f"General validation error: {e}")
        Validation failed for field 'host': Host cannot be empty

    Integration:
        Used throughout the platform for:
        - Entity validation in domain layer
        - Configuration validation in settings
        - API parameter validation
        - User input validation and feedback

    """

    def __init__(self, message: str, field_name: str | None = None) -> None:
        """Initialize validation error with message and optional field context.

        Args:
            message (str): Detailed validation error message for user feedback.
            field_name (str | None): Name of field that failed validation.
                Provides context for error identification and resolution.

        """
        super().__init__(message)
        self.field_name = field_name


class FlextGrpcConnectionError(FlextConnectionError):
    """gRPC connection error with comprehensive network and channel context.

    Specialized connection error for gRPC network communication failures.
    Provides detailed context about connection issues including channel
    state, network conditions, and error details for troubleshooting
    and monitoring.

    This error type enables precise connection error handling:
    - Network-specific error identification and diagnosis
    - Channel state information for debugging
    - Connection retry logic and recovery mechanisms
    - Enterprise monitoring and alerting integration

    Common Causes:
        - Server unavailable or unreachable
        - Network connectivity issues
        - Channel configuration problems
        - Authentication and authorization failures
        - Load balancer and proxy issues

    Example:
        Connection error handling with retry logic:

        >>> try:
        ...     client = create_client("unreachable-server:50051")
        ...     platform.connect_client(client)
        ... except FlextGrpcConnectionError as e:
        ...     logger.warning(f"Connection failed: {e}")
        ...     # Implement retry logic or fallback
        ...     backup_client = create_client("backup-server:50051")

    Integration:
        Used throughout the platform for:
        - Client connection establishment failures
        - Channel lifecycle management errors
        - Network communication issues
        - Service discovery and routing problems

    """


class FlextGrpcTimeoutError(FlextTimeoutError):
    """gRPC timeout error with comprehensive deadline and operation context.

    Specialized timeout error for gRPC operation deadline violations.
    Provides detailed context about timeout conditions including operation
    duration, configured deadlines, and timing information for performance
    analysis and optimization.

    This error type enables precise timeout error handling:
    - Operation-specific timeout identification and analysis
    - Deadline configuration validation and tuning
    - Performance monitoring and optimization
    - Enterprise SLA monitoring and alerting

    Common Causes:
        - Network latency exceeding configured timeouts
        - Server processing delays and resource constraints
        - Large data transfer operations
        - Cascading timeout failures in distributed systems
        - Inadequate timeout configuration for operation complexity

    Example:
        Timeout error handling with performance monitoring:

        >>> try:
        ...     response = platform.make_call(client, "ProcessLargeDataset", dataset)
        ... except FlextGrpcTimeoutError as e:
        ...     logger.warning(f"Operation timed out: {e}")
        ...     # Adjust timeout or implement async processing
        ...     metrics.increment("grpc.timeout.ProcessLargeDataset")

    Integration:
        Used throughout the platform for:
        - Remote method call timeout handling
        - Stream operation deadline management
        - Configuration timeout validation
        - Performance monitoring and SLA tracking

    """


class FlextGrpcConfigurationError(FlextConfigurationError):
    """gRPC configuration error with comprehensive configuration context.

    Specialized configuration error for gRPC setup and configuration validation
    failures. Provides detailed context about configuration issues including
    specific keys, invalid values, and validation rules for debugging and
    configuration correction.

    This error type enables precise configuration error handling:
    - Configuration key and value identification
    - Validation rule information for correction
    - Enterprise configuration management integration
    - Deployment and environment-specific error handling

    Attributes:
        config_key (str | None): Configuration key that caused the error.
            Provides context for identifying specific configuration issues.
            None when error is not key-specific.
        config_value (object): Invalid configuration value that caused the error.
            Enables debugging and configuration validation analysis.

    Common Causes:
        - Invalid port numbers or host addresses
        - Incorrect timeout or worker count configurations
        - Missing required configuration parameters
        - Environment variable parsing failures
        - Configuration file format or content errors

    Example:
        Configuration error handling with detailed context:

        >>> try:
        ...     config = FlextGrpcConfig(port=999999)  # Invalid port
        ... except FlextGrpcConfigurationError as e:
        ...     print(f"Configuration error in '{e.config_key}': {e}")
        ...     print(f"Invalid value: {e.config_value}")
        ...     # Provide user-friendly error correction guidance
        Configuration error in 'port': Port 999999 must be between 1024 and 65535
        Invalid value: 999999

    Integration:
        Used throughout the platform for:
        - Configuration validation during startup
        - Environment variable parsing and validation
        - Runtime configuration updates and validation
        - Enterprise configuration management systems

    """

    def __init__(
        self,
        message: str,
        config_key: str | None = None,
        config_value: object = None,
    ) -> None:
        """Initialize configuration error with detailed context information.

        Args:
            message (str): Detailed configuration error message for user feedback.
            config_key (str | None): Configuration key that caused the error.
                Provides context for identifying and fixing configuration issues.
            config_value (object): Invalid configuration value for analysis.
                Enables debugging and validation rule development.

        """
        super().__init__(message)
        self.config_key = config_key
        self.config_value = config_value


# =============================================================================
# EXPORTS - Only minimal gRPC-specific errors
# =============================================================================


__all__ = [
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
]
