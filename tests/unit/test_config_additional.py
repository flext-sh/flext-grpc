"""Additional tests for flext_grpc.config module.

Tests additional functionality to improve coverage.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_grpc.config import FlextGrpcConfig


class TestFlextGrpcConfigAdditional:
    """Additional tests for FlextGrpcConfig to improve coverage."""

    def test_config_with_empty_host(self) -> None:
        """Test config with empty host."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(host="")

    def test_config_with_whitespace_host(self) -> None:
        """Test config with whitespace-only host."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(host="   ")

    def test_config_with_invalid_port_zero(self) -> None:
        """Test config with port 0."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(port=0)

    def test_config_with_invalid_port_negative(self) -> None:
        """Test config with negative port."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(port=-1)

    def test_config_with_invalid_port_high(self) -> None:
        """Test config with port > 65535."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(port=70000)

    def test_config_with_invalid_max_workers_zero(self) -> None:
        """Test config with max_workers 0."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(max_workers=0)

    def test_config_with_invalid_max_workers_negative(self) -> None:
        """Test config with negative max_workers."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(max_workers=-1)

    def test_config_with_invalid_max_workers_high(self) -> None:
        """Test config with max_workers > 100."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(max_workers=101)

    def test_config_with_invalid_timeout_zero(self) -> None:
        """Test config with timeout 0."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(timeout=0)

    def test_config_with_invalid_timeout_negative(self) -> None:
        """Test config with negative timeout."""
        with pytest.raises(ValidationError):
            FlextGrpcConfig(timeout=-1)

    def test_config_with_valid_minimum_values(self) -> None:
        """Test config with minimum valid values."""
        config = FlextGrpcConfig(host="localhost", port=1, max_workers=1, timeout=1.0)

        assert config.host == "localhost"
        assert config.port == 1
        assert config.max_workers == 1
        assert config.timeout == 1.0

    def test_config_with_valid_maximum_values(self) -> None:
        """Test config with maximum valid values."""
        config = FlextGrpcConfig(
            host="example.com", port=65535, max_workers=100, timeout=300.0
        )

        assert config.host == "example.com"
        assert config.port == 65535
        assert config.max_workers == 100
        assert config.timeout == 300.0

    def test_config_with_default_values(self) -> None:
        """Test config with default values."""
        config = FlextGrpcConfig()

        assert config.host == "localhost"
        assert config.port == 50051
        assert config.max_workers == 4
        assert config.timeout == 30.0

    def test_config_with_partial_values(self) -> None:
        """Test config with partial values."""
        config = FlextGrpcConfig(host="custom-host", port=8080)

        assert config.host == "custom-host"
        assert config.port == 8080
        assert config.max_workers == 4  # Default
        assert config.timeout == 30.0  # Default

    def test_config_with_string_port(self) -> None:
        """Test config with string port (should be converted)."""
        config = FlextGrpcConfig(port="8080")

        assert config.port == 8080
        assert isinstance(config.port, int)

    def test_config_with_string_max_workers(self) -> None:
        """Test config with string max_workers (should be converted)."""
        config = FlextGrpcConfig(max_workers="20")

        assert config.max_workers == 20
        assert isinstance(config.max_workers, int)

    def test_config_with_string_timeout(self) -> None:
        """Test config with string timeout (should be converted)."""
        config = FlextGrpcConfig(timeout="60.5")

        assert config.timeout == 60.5
        assert isinstance(config.timeout, float)

    def test_config_with_float_port(self) -> None:
        """Test config with float port (should be converted to int)."""
        config = FlextGrpcConfig(port=8080.0)

        assert config.port == 8080
        assert isinstance(config.port, int)

    def test_config_with_float_max_workers(self) -> None:
        """Test config with float max_workers (should be converted to int)."""
        config = FlextGrpcConfig(max_workers=20.0)

        assert config.max_workers == 20
        assert isinstance(config.max_workers, int)

    def test_config_with_int_timeout(self) -> None:
        """Test config with int timeout (should be converted to float)."""
        config = FlextGrpcConfig(timeout=60)

        assert config.timeout == 60.0
        assert isinstance(config.timeout, float)

    def test_config_with_edge_case_hosts(self) -> None:
        """Test config with edge case host values."""
        # Test with IP address
        config = FlextGrpcConfig(host="127.0.0.1")
        assert config.host == "127.0.0.1"

        # Test with domain name
        config = FlextGrpcConfig(host="example.com")
        assert config.host == "example.com"

        # Test with subdomain
        config = FlextGrpcConfig(host="api.example.com")
        assert config.host == "api.example.com"

    def test_config_validation_error_messages(self) -> None:
        """Test config validation error messages."""
        # Test host validation error
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(host="")
        assert "Host cannot be empty" in str(exc_info.value)

        # Test port validation error
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(port=0)
        assert "Port 0 must be between 1 and 65535" in str(exc_info.value)

        # Test max_workers validation error
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(max_workers=0)
        assert "Max workers 0 must be between 1 and 100" in str(exc_info.value)

        # Test timeout validation error
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(timeout=0)
        assert "Timeout 0.0 must be between 0.1 and 300.0 seconds" in str(
            exc_info.value
        )

    def test_config_with_boolean_values(self) -> None:
        """Test config with boolean values (should be converted)."""
        # Boolean True should convert to 1
        config = FlextGrpcConfig(max_workers=True)
        assert config.max_workers == 1

        # Boolean False should convert to 0 (invalid)
        with pytest.raises(ValidationError):
            FlextGrpcConfig(max_workers=False)

    def test_config_with_none_values(self) -> None:
        """Test config with None values (should raise ValidationError)."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(host=None, port=None, max_workers=None, timeout=None)

        # Verify the error message contains expected text
        error_str = str(exc_info.value)
        assert "Input should be a valid string" in error_str
        assert "Input should be a valid integer" in error_str
        assert "Input should be a valid number" in error_str

    def test_config_with_whitespace_trimming(self) -> None:
        """Test config with whitespace trimming."""
        config = FlextGrpcConfig(host="  localhost  ")

        assert config.host == "localhost"  # Should be trimmed

    def test_config_with_scientific_notation(self) -> None:
        """Test config with scientific notation values."""
        config = FlextGrpcConfig(timeout=1e2)  # 100.0

        assert config.timeout == 100.0
        assert isinstance(config.timeout, float)

    def test_config_with_very_large_timeout(self) -> None:
        """Test config with very large timeout value."""
        config = FlextGrpcConfig(timeout=300.0)  # Maximum allowed timeout

        assert config.timeout == 300.0

    def test_config_with_decimal_timeout(self) -> None:
        """Test config with decimal timeout value."""
        config = FlextGrpcConfig(timeout=30.5)

        assert config.timeout == 30.5

    def test_config_with_edge_case_port_boundaries(self) -> None:
        """Test config with edge case port boundaries."""
        # Test boundary values
        config = FlextGrpcConfig(port=1)  # Minimum valid
        assert config.port == 1

        config = FlextGrpcConfig(port=65535)  # Maximum valid
        assert config.port == 65535

    def test_config_with_edge_case_max_workers_boundaries(self) -> None:
        """Test config with edge case max_workers boundaries."""
        # Test boundary values
        config = FlextGrpcConfig(max_workers=1)  # Minimum valid
        assert config.max_workers == 1

        config = FlextGrpcConfig(max_workers=100)  # Maximum valid
        assert config.max_workers == 100

    def test_config_with_edge_case_timeout_boundaries(self) -> None:
        """Test config with edge case timeout boundaries."""
        # Test minimum valid timeout
        config = FlextGrpcConfig(timeout=0.1)
        assert config.timeout == 0.1

        # Test maximum valid timeout
        config = FlextGrpcConfig(timeout=300.0)
        assert config.timeout == 300.0
