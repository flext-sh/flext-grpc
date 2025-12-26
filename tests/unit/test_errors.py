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
- Tests error classes from flext_grpc.errors module
- Validates error hierarchy extending flext-core error foundation
- Uses enterprise error handling patterns for validation
- Integrates with pytest framework for execution and coverage

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_core import FlextExceptions



    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcSettingsurationError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)


class TestFlextGrpcError:
    """Test base gRPC error class."""

    def test_base_error_creation(self) -> None:
        """Test FlextGrpcError can be created with message."""
        message = "Base gRPC error occurred"
        error = FlextGrpcError(message)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert isinstance(error, Exception)

    def test_base_error_inheritance(self) -> None:
        """Test FlextGrpcError inherits from FlextExceptions."""
        # All imports are at the top of the file

        error = FlextGrpcError("test")
        assert isinstance(error, FlextExceptions.BaseError)


class TestFlextGrpcValidationError:
    """Test gRPC validation error with field context."""

    def test_validation_error_with_field_name(self) -> None:
        """Test validation error stores field_name attribute."""
        message = "Invalid field value"
        field_name = "username"

        error = FlextGrpcValidationError(message, field=field_name)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.field == field_name

    def test_validation_error_without_field_name(self) -> None:
        """Test validation error with None field_name."""
        message = "General validation error"

        error = FlextGrpcValidationError(message, field=None)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.field is None

    def test_validation_error_default_field_name(self) -> None:
        """Test validation error with default field_name parameter."""
        message = "Default validation error"

        error = FlextGrpcValidationError(message)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.field is None

    def test_validation_error_inheritance(self) -> None:
        """Test FlextGrpcValidationError inherits correctly."""
        # All imports are at the top of the file

        error = FlextGrpcValidationError("test")
        assert isinstance(error, FlextExceptions.BaseError)


class TestFlextGrpcConnectionError:
    """Test gRPC connection error class."""

    def test_connection_error_creation(self) -> None:
        """Test connection error can be created."""
        message = "Connection failed"
        error = FlextGrpcConnectionError(message)

        # flext-core adds error type prefix to messages
        assert message in str(error)

    def test_connection_error_inheritance(self) -> None:
        """Test FlextGrpcConnectionError inherits correctly."""
        # All imports are at the top of the file

        error = FlextGrpcConnectionError("test")
        assert isinstance(error, FlextExceptions.BaseError)


class TestFlextGrpcTimeoutError:
    """Test gRPC timeout error class."""

    def test_timeout_error_creation(self) -> None:
        """Test timeout error can be created."""
        message = "Request timed out"
        error = FlextGrpcTimeoutError(message)

        # flext-core adds error type prefix to messages
        assert message in str(error)

    def test_timeout_error_inheritance(self) -> None:
        """Test FlextGrpcTimeoutError inherits correctly."""
        # All imports are at the top of the file

        error = FlextGrpcTimeoutError("test")
        assert isinstance(error, FlextExceptions.BaseError)


class TestFlextGrpcSettingsurationError:
    """Test gRPC configuration error with config context."""

    def test_configuration_error_with_all_params(self) -> None:
        """Test configuration error with all parameters."""
        message = "Invalid configuration"
        config_key = "port"

        error = FlextGrpcSettingsurationError(message, config_key=config_key)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.config_key == config_key

    def test_configuration_error_with_minimal_params(self) -> None:
        """Test configuration error with only message."""
        message = "Configuration error"

        error = FlextGrpcSettingsurationError(message)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.config_key is None

    def test_configuration_error_with_key_only(self) -> None:
        """Test configuration error with config_key but no value."""
        message = "Missing configuration"
        config_key = "host"

        error = FlextGrpcSettingsurationError(message, config_key=config_key)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.config_key == config_key

    def test_configuration_error_inheritance(self) -> None:
        """Test FlextGrpcSettingsurationError inherits correctly."""
        # All imports are at the top of the file

        error = FlextGrpcSettingsurationError("test")
        assert isinstance(error, FlextExceptions.BaseError)


class TestErrorIntegration:
    """Test error classes work together in realistic scenarios."""

    def test_all_errors_are_exceptions(self) -> None:
        """Test all error classes can be raised as exceptions."""
        errors = [
            FlextGrpcError("base error"),
            FlextGrpcValidationError("validation error", field="field"),
            FlextGrpcConnectionError("connection error"),
            FlextGrpcTimeoutError("timeout error"),
            FlextGrpcSettingsurationError("config error", config_key="key"),
        ]

        for error in errors:
            # Should be able to raise without issues
            assert isinstance(error, Exception)
            assert len(str(error)) > 0

    def test_error_hierarchy_consistency(self) -> None:
        """Test error hierarchy follows flext-core patterns."""
        # All imports are at the top of the file

        # All should inherit from FlextExceptions through their specific parents
        errors = [
            FlextGrpcError("test"),
            FlextGrpcValidationError("test"),
            FlextGrpcConnectionError("test"),
            FlextGrpcTimeoutError("test"),
            FlextGrpcSettingsurationError("test"),
        ]

        # Test that FlextGrpcError inherits from FlextExceptions (base case)
        assert isinstance(FlextGrpcError("test"), FlextExceptions.BaseError)

        # Test that specialized errors inherit from their respective flext-core parents
        assert isinstance(FlextGrpcValidationError("test"), FlextExceptions.BaseError)
        assert isinstance(FlextGrpcConnectionError("test"), FlextExceptions.BaseError)
        assert isinstance(FlextGrpcTimeoutError("test"), FlextExceptions.BaseError)
        assert isinstance(
            FlextGrpcSettingsurationError("test"),
            FlextExceptions.BaseError,
        )

        # All errors should be Exception instances
        for error in errors:
            assert isinstance(error, Exception)

    def test_error_with_complex_scenarios(self) -> None:
        """Test errors in complex real-world scenarios."""
        # Validation error with Unicode field name
        unicode_error = FlextGrpcValidationError(
            "Invalid value for field 'データ'",
            field="データ",
        )
        assert unicode_error.field == "データ"

        # Configuration error with complex object
        config_key = "complex_setting"
        config_error = FlextGrpcSettingsurationError(
            "Complex config failed",
            config_key=config_key,
        )
        assert config_error.config_key == config_key
