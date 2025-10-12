"""Tests for flext_grpc.exceptions module."""

from flext_grpc.exceptions import FlextGrpcExceptions


class TestFlextGrpcExceptions:
    """Test cases for FlextGrpcExceptions class."""

    def test_base_error(self) -> None:
        """Test base error creation."""
        error = FlextGrpcExceptions.BaseError("Test error")
        assert error.message == "Test error"

    def test_validation_error(self) -> None:
        """Test validation error creation."""
        error = FlextGrpcExceptions.ValidationError("Validation failed")
        assert error.message == "Validation failed"

    def test_connection_error(self) -> None:
        """Test connection error creation."""
        error = FlextGrpcExceptions.ConnectionError("Connection failed")
        assert error.message == "Connection failed"

    def test_timeout_error(self) -> None:
        """Test timeout error creation."""
        error = FlextGrpcExceptions.TimeoutError("Operation timed out")
        assert error.message == "Operation timed out"

    def test_configuration_error(self) -> None:
        """Test configuration error creation."""
        error = FlextGrpcExceptions.ConfigurationError("Configuration failed")
        assert error.message == "Configuration failed"
