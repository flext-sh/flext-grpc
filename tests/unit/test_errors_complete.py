"""Comprehensive tests for FLEXT gRPC error classes.

Tests all error classes and their specific attributes to achieve 100% coverage.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc.errors import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
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
        """Test FlextGrpcError inherits from FlextError."""
        from flext_core import FlextError

        error = FlextGrpcError("test")
        assert isinstance(error, FlextError)


class TestFlextGrpcValidationError:
    """Test gRPC validation error with field context."""

    def test_validation_error_with_field_name(self) -> None:
        """Test validation error stores field_name attribute."""
        message = "Invalid field value"
        field_name = "username"

        error = FlextGrpcValidationError(message, field_name)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.field_name == field_name

    def test_validation_error_without_field_name(self) -> None:
        """Test validation error with None field_name."""
        message = "General validation error"

        error = FlextGrpcValidationError(message, None)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.field_name is None

    def test_validation_error_default_field_name(self) -> None:
        """Test validation error with default field_name parameter."""
        message = "Default validation error"

        error = FlextGrpcValidationError(message)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.field_name is None

    def test_validation_error_inheritance(self) -> None:
        """Test FlextGrpcValidationError inherits correctly."""
        from flext_core import FlextValidationError

        error = FlextGrpcValidationError("test")
        assert isinstance(error, FlextValidationError)


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
        from flext_core import FlextConnectionError

        error = FlextGrpcConnectionError("test")
        assert isinstance(error, FlextConnectionError)


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
        from flext_core import FlextTimeoutError

        error = FlextGrpcTimeoutError("test")
        assert isinstance(error, FlextTimeoutError)


class TestFlextGrpcConfigurationError:
    """Test gRPC configuration error with config context."""

    def test_configuration_error_with_all_params(self) -> None:
        """Test configuration error with all parameters."""
        message = "Invalid configuration"
        config_key = "port"
        config_value = -1

        error = FlextGrpcConfigurationError(message, config_key, config_value)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.config_key == config_key
        assert error.config_value == config_value

    def test_configuration_error_with_minimal_params(self) -> None:
        """Test configuration error with only message."""
        message = "Configuration error"

        error = FlextGrpcConfigurationError(message)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.config_key is None
        assert error.config_value is None

    def test_configuration_error_with_key_only(self) -> None:
        """Test configuration error with config_key but no value."""
        message = "Missing configuration"
        config_key = "host"

        error = FlextGrpcConfigurationError(message, config_key)

        # flext-core adds error type prefix to messages
        assert message in str(error)
        assert error.config_key == config_key
        assert error.config_value is None

    def test_configuration_error_inheritance(self) -> None:
        """Test FlextGrpcConfigurationError inherits correctly."""
        from flext_core import FlextConfigurationError

        error = FlextGrpcConfigurationError("test")
        assert isinstance(error, FlextConfigurationError)


class TestErrorIntegration:
    """Test error classes work together in realistic scenarios."""

    def test_all_errors_are_exceptions(self) -> None:
        """Test all error classes can be raised as exceptions."""
        errors = [
            FlextGrpcError("base error"),
            FlextGrpcValidationError("validation error", "field"),
            FlextGrpcConnectionError("connection error"),
            FlextGrpcTimeoutError("timeout error"),
            FlextGrpcConfigurationError("config error", "key", "value"),
        ]

        for error in errors:
            # Should be able to raise without issues
            assert isinstance(error, Exception)
            assert len(str(error)) > 0

    def test_error_hierarchy_consistency(self) -> None:
        """Test error hierarchy follows flext-core patterns."""
        from flext_core import FlextError

        # All should inherit from FlextError through their specific parents
        errors = [
            FlextGrpcError("test"),
            FlextGrpcValidationError("test"),
            FlextGrpcConnectionError("test"),
            FlextGrpcTimeoutError("test"),
            FlextGrpcConfigurationError("test"),
        ]

        for error in errors:
            assert isinstance(error, FlextError)

    def test_error_with_complex_scenarios(self) -> None:
        """Test errors in complex real-world scenarios."""
        # Validation error with Unicode field name
        unicode_error = FlextGrpcValidationError(
            "Invalid value for field 'データ'",
            "データ"
        )
        assert unicode_error.field_name == "データ"

        # Configuration error with complex object
        complex_config = {"nested": {"key": "value"}, "list": [1, 2, 3]}
        config_error = FlextGrpcConfigurationError(
            "Complex config failed",
            "complex_setting",
            complex_config
        )
        assert config_error.config_value == complex_config
