"""FLEXT gRPC Exceptions.

Comprehensive exception handling for the FLEXT gRPC framework,
extending flext-core error foundation with domain-specific error types.
Designed for precise error handling, debugging support, and enterprise-grade
error reporting across all gRPC operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextExceptions


class FlextGrpcError(FlextExceptions.BaseError):
    """Base exception for all FLEXT gRPC platform errors.

    Root exception class for the FLEXT gRPC error hierarchy, providing
    a common base for all gRPC-specific exceptions. Extends the flext-core
    FlextExceptions foundation while enabling specific gRPC error handling.

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


class FlextGrpcValidationError(FlextGrpcError):
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
      ...     server = FlextGrpcServer(
      ...         host="", port=FlextGrpcConstants.Network.DEFAULT_PORT
      ...     )
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

    @override
    def __init__(self, message: str, field_name: str | None = None) -> None:
        """Initialize validation error with message and optional field context.

        Args:
            message (str): Detailed validation error message for user feedback.
            field_name (str | None): Name of field that failed validation.
                Provides context for error identification and resolution.

        Returns:
            object: Description of return value.

        """
        super().__init__(message)
        self.field_name = field_name


class FlextGrpcConnectionError(FlextGrpcError):
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
      ...     client = create_client(
      ...         f"unreachable-server:{FlextGrpcConstants.Network.DEFAULT_PORT}"
      ...     )
      ...     platform.connect_client(client)
      ... except FlextGrpcConnectionError as e:
      ...     logger.warning(f"Connection failed: {e}")
      ...     # Implement retry logic or fallback
      ...     backup_client = create_client(
      ...         f"backup-server:{FlextGrpcConstants.Network.DEFAULT_PORT}"
      ...     )

    Integration:
      Used throughout the platform for:
      - Client connection establishment failures
      - Channel lifecycle management errors
      - Network communication issues
      - Service discovery and routing problems

    """


class FlextGrpcTimeoutError(FlextGrpcError):
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


class FlextGrpcConfigurationError(FlextGrpcError):
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
      ...     config: dict["str", "object"] = FlextGrpcConfig(
      ...         port=999999
      ...     )  # Invalid port
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

    @override
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


class FlextGrpcChannelError(FlextGrpcError):
    """gRPC channel error for channel state and lifecycle issues.

    Specialized error for gRPC channel management and state transition
    failures. Provides context for channel state, connection issues,
    and channel lifecycle errors.
    """


class FlextGrpcServiceError(FlextGrpcError):
    """gRPC service error for service registration and management issues.

    Specialized error for gRPC service definition, registration,
    and management failures. Provides context for service-specific
    errors and troubleshooting.
    """


class FlextGrpcStreamError(FlextGrpcError):
    """gRPC stream error for streaming operation issues.

    Specialized error for gRPC streaming operations including
    stream creation, data flow, and stream lifecycle errors.
    Provides context for streaming-specific troubleshooting.
    """


__all__ = [
    "FlextGrpcChannelError",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcServiceError",
    "FlextGrpcStreamError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
]
