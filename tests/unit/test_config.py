"""Unit tests for gRPC configuration.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from flext_grpc import FlextGrpcConfig


class TestFlextGrpcConfig:
    """Comprehensive unit tests for FlextGrpcConfig with enterprise testing standards.

    Test suite for FlextGrpcConfig covering creation, validation, field constraints,
    and error handling. Ensures configuration behaves correctly across all scenarios
    including edge cases and error conditions.

    Test Categories:
      - Creation Testing: Valid and invalid configuration creation scenarios
      - Validation Testing: Field validation and constraint enforcement
      - Error Testing: Invalid input handling and error reporting
      - Default Testing: Default value behavior and validation
      - Integration Testing: Configuration usage patterns
    """

    def test_create_valid_config_with_defaults(self) -> None:
        """Test creating configuration with default values."""
        config = FlextGrpcConfig()

        assert config.host == "localhost"
        assert config.port == 50051
        assert config.max_workers == 10
        assert config.timeout == 30.0

    def test_create_valid_config_with_custom_values(self) -> None:
        """Test creating configuration with custom values."""
        config = FlextGrpcConfig(
            host="api.example.com",
            port=8080,
            max_workers=20,
            timeout=30.0,
        )

        assert config.host == "api.example.com"
        assert config.port == 8080
        assert config.max_workers == 20
        assert config.timeout == 30.0

    def test_invalid_empty_host(self) -> None:
        """Test configuration creation with empty host fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(host="")

        assert "Host cannot be empty" in str(exc_info.value)

    def test_invalid_whitespace_host(self) -> None:
        """Test configuration creation with whitespace-only host fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(host="   ")

        assert "Host cannot be empty" in str(exc_info.value)

    def test_invalid_port_too_low(self) -> None:
        """Test configuration creation with port below minimum fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(port=0)

        error_msg = str(exc_info.value)
        assert "Port 0 must be between 1 and 65535" in error_msg

    def test_invalid_port_too_high(self) -> None:
        """Test configuration creation with port above maximum fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(port=70000)

        error_msg = str(exc_info.value)
        assert "Port 70000 must be between 1 and 65535" in error_msg

    def test_invalid_max_workers_zero(self) -> None:
        """Test configuration creation with zero max_workers fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(max_workers=0)

        assert "Max workers 0 must be between" in str(exc_info.value)

    def test_invalid_max_workers_negative(self) -> None:
        """Test configuration creation with negative max_workers fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(max_workers=-1)

        assert "Max workers -1 must be between" in str(exc_info.value)

    def test_valid_boundary_values(self) -> None:
        """Test configuration with boundary values passes validation."""
        config = FlextGrpcConfig(
            host="a",  # Minimum valid host
            port=1,  # Minimum valid port
            max_workers=1,  # Minimum valid workers
            timeout=0.1,  # Minimum meaningful timeout
        )

        assert config.host == "a"
        assert config.port == 1
        assert config.max_workers == 1
        assert config.timeout == 0.1

    def test_get_address_method(self) -> None:
        """Test get_address method returns formatted address."""
        config = FlextGrpcConfig(host="localhost", port=50051)

        assert config.get_address() == "localhost:50051"

    def test_host_strip_whitespace(self) -> None:
        """Test host validation strips whitespace from valid hosts."""
        config = FlextGrpcConfig(host="  localhost  ")

        assert config.host == "localhost"

    def test_invalid_timeout_zero(self) -> None:
        """Test configuration creation with zero timeout fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(timeout=0.0)

        assert "Timeout 0.0 must be between" in str(exc_info.value)

    def test_invalid_timeout_negative(self) -> None:
        """Test configuration creation with negative timeout fails validation."""
        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcConfig(timeout=-1.0)

        assert "Timeout -1.0 must be between" in str(exc_info.value)
