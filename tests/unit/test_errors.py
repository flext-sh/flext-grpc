"""Unit tests for gRPC error handling.

Contextual information testing, and error handling pattern verification.

Test Coverage: The module ensures comprehensive coverage of error system functionality:
- Error Hierarchy: Base error class and specialized error type testing
- Contextual Information: Error-specific context and metadata validation
- Error Initialization: Error creation with proper parameter handling
- Error Reporting: Error message and context information validation
- Exception Handling: Error propagation and handling pattern testing

Testing Architecture: Error testing follows enterprise testing principles:
- Hierarchy Testing: Base class and inheritance validation
- Context Validation: Error-specific context information testing
- Initialization Testing: Error creation with various parameter combinations
- Message Testing: Error message clarity and consistency validation
- Integration Testing: Error usage in service and entity contexts

Testing Patterns: All error tests follow enterprise testing standards:
- AAA Pattern: Arrange, Act, Assert structure for clarity
- Exception Testing: Proper exception creation and handling validation
- Context Validation: Error context information accuracy testing
- Message Verification: Error message clarity and consistency checking
- Inheritance Testing: Error hierarchy and polymorphism validation

Coverage Goals: Tests all error classes and their specific attributes to achieve 100% coverage with comprehensive validation of error creation, context, and usage patterns.

Integration:
- Tests error classes from flext_grpc module
- Validates error hierarchy extending flext-core error foundation
- Uses enterprise error handling patterns for validation
- Integrates with pytest framework for execution and coverage

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_tests import e, tm

from flext_grpc.errors import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    GrpcValidationError,
)


class TestsFlextGrpcErrors:
    """Test base gRPC error class."""

    def test_base_error_creation(self) -> None:
        """Test FlextGrpcError can be created with message."""
        message = "Base gRPC error occurred"
        error = FlextGrpcError(message)
        tm.that(str(error), has=message)
        tm.that(error, is_=Exception)

    def test_base_error_inheritance(self) -> None:
        """Test FlextGrpcError inherits from e."""
        error = FlextGrpcError("test")
        tm.that(error, is_=e.BaseError)

    """Test gRPC validation error with field context."""

    def test_validation_error_with_field_name(self) -> None:
        """Test validation error stores field_name attribute."""
        message = "Invalid field value"
        field_name = "username"
        error = GrpcValidationError(message, field=field_name)
        tm.that(str(error), has=message)
        tm.that(error.field, eq=field_name)

    def test_validation_error_without_field_name(self) -> None:
        """Test validation error with None field_name."""
        message = "General validation error"
        error = GrpcValidationError(message, field=None)
        tm.that(str(error), has=message)
        tm.that(error.field, none=True)

    def test_validation_error_default_field_name(self) -> None:
        """Test validation error with default field_name parameter."""
        message = "Default validation error"
        error = GrpcValidationError(message)
        tm.that(str(error), has=message)
        tm.that(error.field, none=True)

    def test_validation_error_inheritance(self) -> None:
        """Test GrpcValidationError inherits correctly."""
        error = GrpcValidationError("test")
        tm.that(error, is_=e.BaseError)

    """Test gRPC connection error class."""

    def test_connection_error_creation(self) -> None:
        """Test connection error can be created."""
        message = "Connection failed"
        error = FlextGrpcConnectionError(message)
        tm.that(str(error), has=message)

    def test_connection_error_inheritance(self) -> None:
        """Test FlextGrpcConnectionError inherits correctly."""
        error = FlextGrpcConnectionError("test")
        tm.that(error, is_=e.BaseError)

    """Test gRPC timeout error class."""

    def test_timeout_error_creation(self) -> None:
        """Test timeout error can be created."""
        message = "Request timed out"
        error = FlextGrpcTimeoutError(message)
        tm.that(str(error), has=message)

    def test_timeout_error_inheritance(self) -> None:
        """Test FlextGrpcTimeoutError inherits correctly."""
        error = FlextGrpcTimeoutError("test")
        tm.that(error, is_=e.BaseError)

    """Test gRPC configuration error with settings context."""

    def test_configuration_error_with_all_params(self) -> None:
        """Test configuration error with all parameters."""
        message = "Invalid configuration"
        config_key = "port"
        error = FlextGrpcConfigurationError(message, config_key=config_key)
        tm.that(str(error), has=message)
        tm.that(error.config_key, eq=config_key)

    def test_configuration_error_with_minimal_params(self) -> None:
        """Test configuration error with only message."""
        message = "Configuration error"
        error = FlextGrpcConfigurationError(message)
        tm.that(str(error), has=message)
        tm.that(error.config_key, none=True)

    def test_configuration_error_with_key_only(self) -> None:
        """Test configuration error with config_key but no value."""
        message = "Missing configuration"
        config_key = "host"
        error = FlextGrpcConfigurationError(message, config_key=config_key)
        tm.that(str(error), has=message)
        tm.that(error.config_key, eq=config_key)

    def test_configuration_error_inheritance(self) -> None:
        """Test FlextGrpcConfigurationError inherits correctly."""
        error = FlextGrpcConfigurationError("test")
        tm.that(error, is_=e.BaseError)

    """Test error classes work together in realistic scenarios."""

    def test_all_errors_are_exceptions(self) -> None:
        """Test all error classes can be raised as exceptions."""
        errors = [
            FlextGrpcError("base error"),
            GrpcValidationError("validation error", field="field"),
            FlextGrpcConnectionError("connection error"),
            FlextGrpcTimeoutError("timeout error"),
            FlextGrpcConfigurationError("settings error", config_key="key"),
        ]
        for error in errors:
            tm.that(error, is_=Exception)
            tm.that(len(str(error)) > 0, eq=True)

    def test_error_hierarchy_consistency(self) -> None:
        """Test error hierarchy follows flext-core patterns."""
        errors = [
            FlextGrpcError("test"),
            GrpcValidationError("test"),
            FlextGrpcConnectionError("test"),
            FlextGrpcTimeoutError("test"),
            FlextGrpcConfigurationError("test"),
        ]
        tm.that(FlextGrpcError("test"), is_=e.BaseError)
        tm.that(GrpcValidationError("test"), is_=e.BaseError)
        tm.that(FlextGrpcConnectionError("test"), is_=e.BaseError)
        tm.that(FlextGrpcTimeoutError("test"), is_=e.BaseError)
        tm.that(FlextGrpcConfigurationError("test"), is_=e.BaseError)
        for error in errors:
            tm.that(error, is_=Exception)

    def test_error_with_complex_scenarios(self) -> None:
        """Test errors in complex real-world scenarios."""
        unicode_error = GrpcValidationError(
            "Invalid value for field 'データ'",
            field="データ",
        )
        tm.that(unicode_error.field, eq="データ")
        config_key = "complex_setting"
        config_error = FlextGrpcConfigurationError(
            "Complex settings failed",
            config_key=config_key,
        )
        tm.that(config_error.config_key, eq=config_key)
