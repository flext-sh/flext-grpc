"""FLEXT gRPC Exceptions - Namespace Class Pattern.

Comprehensive exception handling for the FLEXT gRPC framework,
extending flext-core error foundation with domain-specific error types.
Designed for precise error handling, debugging support, and enterprise-grade
error reporting across all gRPC operations.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import override

from flext_core import FlextCore


class FlextGrpcExceptions:
    """Namespace class for FLEXT gRPC exceptions.

    Single unified class with nested exception classes following FLEXT
    namespace pattern. Extends flext-core error foundation while enabling
    specific gRPC error handling with comprehensive context and debugging support.

    This namespace enables comprehensive error handling patterns:
    - Catch all gRPC errors with single base exception type
    - Maintain consistency with flext-core error patterns
    - Enable error classification and routing
    - Support enterprise error monitoring and reporting
    - Provide nested access to specialized exception types

    Usage:
      Access nested exception classes:

      >>> from flext_grpc.exceptions import FlextGrpcExceptions
      >>> raise FlextGrpcExceptions.ValidationError("Invalid input")

      Catch all gRPC errors:

      >>> try:
      ...     grpc_operation()
      ... except FlextGrpcExceptions.BaseError as e:
      ...     logger.error(f"gRPC operation failed: {e}")

    Error Hierarchy:
      All nested exceptions inherit from BaseError, enabling both
      specific and general error handling depending on requirements.
    """

    class BaseError(FlextCore.Exceptions.BaseError):
        """Base exception for all FLEXT gRPC platform errors.

        Root exception class for the FLEXT gRPC error hierarchy, providing
        a common base for all gRPC-specific exceptions. Extends the flext-core
        FlextCore.Exceptions foundation while enabling specific gRPC error handling.

        This base class enables comprehensive error handling patterns:
        - Catch all gRPC errors with single exception type
        - Maintain consistency with flext-core error patterns
        - Enable error classification and routing
        - Support enterprise error monitoring and reporting

        Usage:
          Use as base for all gRPC-specific exceptions or catch-all:

          >>> try:
          ...     grpc_operation()
          ... except FlextGrpcExceptions.BaseError as e:
          ...     logger.error(f"gRPC operation failed: {e}")
          ...     # Handle any gRPC-related error

        Error Hierarchy:
          All FLEXT gRPC exceptions inherit from this base class,
          enabling both specific and general error handling patterns
          depending on application requirements.
        """

        def _extract_common_kwargs(
            self, kwargs: FlextCore.Types.Dict
        ) -> tuple[FlextCore.Types.Dict | None, str | None, str | None]:
            """Extract common error parameters from kwargs."""
            context = kwargs.get("context")
            correlation_id = kwargs.get("correlation_id")
            error_code = kwargs.get("error_code")

            # Ensure proper types
            if context is not None and not isinstance(context, dict):
                context = None
            if correlation_id is not None and not isinstance(correlation_id, str):
                correlation_id = None
            if error_code is not None and not isinstance(error_code, str):
                error_code = None

            return context, correlation_id, error_code

        def _build_context(
            self, base_context: FlextCore.Types.Dict | None
        ) -> FlextCore.Types.Dict:
            """Build complete error context."""
            context = base_context or {}

            # Add gRPC-specific context if not present
            if "error_type" not in context:
                context["error_type"] = "grpc_error"
            if "component" not in context:
                context["component"] = "flext_grpc"

            return context

        @override
        def __init__(
            self,
            message: str,
            **kwargs: object,
        ) -> None:
            """Initialize gRPC error with context using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )

    class ValidationError(BaseError):
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
          ... except FlextGrpcExceptions.ValidationError as e:
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
        def __init__(
            self,
            message: str,
            *,
            field_name: str | None = None,
            **kwargs: object,
        ) -> None:
            """Initialize validation error with message and optional field context using helpers.

            Args:
                message: Detailed validation error message for user feedback.
                field_name: Name of field that failed validation.
                    Provides context for error identification and resolution.
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store field_name before extracting common kwargs
            self.field_name = field_name

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with validation-specific fields
            context = self._build_context(
                base_context,
                field_name=field_name,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_VALIDATION_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )

        def _build_context(
            self,
            base_context: FlextCore.Types.Dict | None,
            field_name: str | None = None,
        ) -> FlextCore.Types.Dict:
            """Build validation error context with field-specific information."""
            context = super()._build_context(base_context)

            # Add validation-specific context
            if field_name is not None:
                context["field_name"] = field_name
                context["error_type"] = "validation_error"

            return context

    class ConnectionError(BaseError):
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
          ... except FlextGrpcExceptions.ConnectionError as e:
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

        @override
        def __init__(
            self,
            message: str,
            **kwargs: object,
        ) -> None:
            """Initialize connection error with context using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_CONNECTION_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )

    class TimeoutError(BaseError):
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
          ... except FlextGrpcExceptions.TimeoutError as e:
          ...     logger.warning(f"Operation timed out: {e}")
          ...     # Adjust timeout or implement processing
          ...     metrics.increment("grpc.timeout.ProcessLargeDataset")

        Integration:
          Used throughout the platform for:
          - Remote method call timeout handling
          - Stream operation deadline management
          - Configuration timeout validation
          - Performance monitoring and SLA tracking

        """

        @override
        def __init__(
            self,
            message: str,
            **kwargs: object,
        ) -> None:
            """Initialize timeout error with context using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_TIMEOUT_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )

    class ConfigurationError(BaseError):
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
          ... except FlextGrpcExceptions.ConfigurationError as e:
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
            *,
            config_key: str | None = None,
            config_value: object = None,
            **kwargs: object,
        ) -> None:
            """Initialize configuration error with detailed context information using helpers.

            Args:
                message: Detailed configuration error message for user feedback.
                config_key: Configuration key that caused the error.
                    Provides context for identifying and fixing configuration issues.
                config_value: Invalid configuration value for analysis.
                    Enables debugging and validation rule development.
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Store config-specific attributes before extracting common kwargs
            self.config_key = config_key
            self.config_value = config_value

            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context with configuration-specific fields
            context = self._build_context(
                base_context,
                config_key=config_key,
                config_value=config_value,
            )

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_CONFIG_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )

        def _build_context(
            self,
            base_context: FlextCore.Types.Dict | None,
            config_key: str | None = None,
            config_value: object = None,
        ) -> FlextCore.Types.Dict:
            """Build configuration error context with config-specific information."""
            context = super()._build_context(base_context)

            # Add configuration-specific context
            if config_key is not None:
                context["config_key"] = config_key
            if config_value is not None:
                context["config_value"] = config_value
                context["error_type"] = "configuration_error"

            return context

    class ChannelError(BaseError):
        """gRPC channel error for channel state and lifecycle issues.

        Specialized error for gRPC channel management and state transition
        failures. Provides context for channel state, connection issues,
        and channel lifecycle errors.
        """

        @override
        def __init__(
            self,
            message: str,
            **kwargs: object,
        ) -> None:
            """Initialize channel error with context using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_CHANNEL_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )

    class ServiceError(BaseError):
        """gRPC service error for service registration and management issues.

        Specialized error for gRPC service definition, registration,
        and management failures. Provides context for service-specific
        errors and troubleshooting.
        """

        @override
        def __init__(
            self,
            message: str,
            **kwargs: object,
        ) -> None:
            """Initialize service error with context using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_SERVICE_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )

    class StreamError(BaseError):
        """gRPC stream error for streaming operation issues.

        Specialized error for gRPC streaming operations including
        stream creation, data flow, and stream lifecycle errors.
        Provides context for streaming-specific troubleshooting.
        """

        @override
        def __init__(
            self,
            message: str,
            **kwargs: object,
        ) -> None:
            """Initialize stream error with context using helpers.

            Args:
                message: Error message
                **kwargs: Additional context (context, correlation_id, error_code)

            """
            # Extract common parameters using helper
            base_context, correlation_id, error_code = self._extract_common_kwargs(
                kwargs
            )

            # Build context
            context = self._build_context(base_context)

            # Call parent with complete error information
            super().__init__(
                message,
                error_code=error_code or "GRPC_STREAM_ERROR",
                metadata=context,
                correlation_id=correlation_id,
            )


__all__ = [
    "FlextGrpcExceptions",
]
