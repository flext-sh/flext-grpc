r"""FLEXT gRPC Type Testing - Comprehensive unit tests for type system and validation.

This module provides comprehensive unit testing for all FLEXT gRPC type definitions,
validation functions, and type safety utilities, following enterprise testing standards
with comprehensive type validation and protocol compliance testing.

Test Coverage:
    The module ensures comprehensive coverage of type system functionality:
    - Type Definitions: NewType validation and semantic meaning verification
    - Validation Functions: Network address and parameter validation testing
    - Protocol Compliance: gRPC library integration protocol testing
    - Type Safety: Static and runtime type checking validation
    - Parsing Functions: Address parsing and component extraction testing

Testing Architecture:
    Type testing follows enterprise testing principles:
    - Type Safety Testing: Validation of type definitions and constraints
    - Function Validation: Type validation and parsing function testing
    - Protocol Testing: gRPC protocol compliance and integration testing
    - Boundary Conditions: Edge cases and invalid input handling
    - Error Handling: Type validation error reporting and recovery

Testing Patterns:
    All type tests follow enterprise testing standards:
    - AAA Pattern: Arrange, Act, Assert structure for clarity
    - Type Validation: Comprehensive type constraint testing
    - Function Testing: Validation and parsing function verification
    - Error Scenarios: Invalid type handling and error reporting
    - Protocol Compliance: gRPC library integration validation

Example:
    Standard type testing pattern used throughout module:

    >>> def test_type_validation_success():
    ...     # Arrange: Set up valid type data
    ...     valid_target = \"localhost:50051\"
    ...
    ...     # Act: Validate type
    ...     result = flext_grpc_validate_target(valid_target)
    ...
    ...     # Assert: Verify validation success:
    ...     assert result is True

Integration:
    - Tests type definitions from flext_grpc.types module
    - Validates type safety and protocol compliance
    - Uses enterprise validation patterns for type checking
    - Integrates with pytest framework for execution and coverage

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_grpc import (
    TGrpcTarget,
    flext_grpc_parse_target,
    flext_grpc_validate_target,
)


class TestGrpcTypes:
    """Test gRPC type definitions and validation."""

    def test_grpc_target_type(self) -> None:
        """Test TGrpcTarget type."""
        target = TGrpcTarget("localhost:50051")
        if target != "localhost:50051":
            raise AssertionError(f"Expected {'localhost:50051'}, got {target}")
        assert isinstance(target, str)

    def test_validate_target_valid_cases(self) -> None:
        """Test valid target validation cases."""
        valid_targets = [
            "localhost:50051",
            "127.0.0.1:8080",
            "example.com:443",
            "api-server:9000",
            "test.domain.com:50051",
        ]

        for target in valid_targets:
            assert flext_grpc_validate_target(target), (
                f"Target {target} should be valid"
            )

    def test_validate_target_invalid_cases(self) -> None:
        """Test invalid target validation cases."""
        invalid_targets = [
            "",  # Empty
            "localhost",  # No port
            ":50051",  # No host
            "localhost:",  # Empty port
            "localhost:abc",  # Non-numeric port
            "localhost:-1",  # Negative port
            "localhost:0",  # Port 0
            "localhost:70000",  # Port too high
            "invalid host:50051",  # Invalid host with space
            "localhost:50051:extra",  # Too many colons
        ]

        for target in invalid_targets:
            assert not flext_grpc_validate_target(target), (
                f"Target {target} should be invalid"
            )

    def test_parse_target_valid_cases(self) -> None:
        """Test valid target parsing cases."""
        test_cases = [
            ("localhost:50051", ("localhost", 50051)),
            ("127.0.0.1:8080", ("127.0.0.1", 8080)),
            ("example.com:443", ("example.com", 443)),
            ("api-server:9000", ("api-server", 9000)),
        ]

        for target, expected in test_cases:
            result = flext_grpc_parse_target(target)
            if result != expected:
                raise AssertionError(
                    f"Expected {expected}, got {result}. Parsing {target} should return {expected}",
                )

    def test_parse_target_invalid_cases(self) -> None:
        """Test invalid target parsing cases."""
        invalid_targets = [
            "",
            "localhost",
            ":50051",
            "localhost:",
            "localhost:abc",
            "localhost:-1",
            "localhost:70000",
        ]

        for target in invalid_targets:
            result = flext_grpc_parse_target(target)
            assert result is None, f"Parsing {target} should return None"

    def test_edge_cases(self) -> None:
        """Test edge cases for validation and parsing."""
        # Minimum valid port
        assert flext_grpc_validate_target("localhost:1")
        result = flext_grpc_parse_target("localhost:1")
        if result != ("localhost", 1):
            raise AssertionError(f"Expected {('localhost', 1)}, got {result}")

        # Maximum valid port
        assert flext_grpc_validate_target("localhost:65535")
        result = flext_grpc_parse_target("localhost:65535")
        if result != ("localhost", 65535):
            raise AssertionError(f"Expected {('localhost', 65535)}, got {result}")

        # Port boundaries
        assert not flext_grpc_validate_target("localhost:0")
        assert not flext_grpc_validate_target("localhost:65536")

    def test_hostname_patterns(self) -> None:
        """Test various hostname patterns."""
        valid_hostnames = [
            "localhost",
            "127.0.0.1",
            "api.example.com",
            "sub-domain.example.com",
            "host123",
            "123host",
            "host.123",
        ]

        for hostname in valid_hostnames:
            target = f"{hostname}:50051"
            assert flext_grpc_validate_target(target), (
                f"Hostname {hostname} should be valid"
            )

        invalid_hostnames = [
            "host with space",
            "host@invalid",
            "host#invalid",
            "host/invalid",
        ]

        for hostname in invalid_hostnames:
            target = f"{hostname}:50051"
            assert not flext_grpc_validate_target(target), (
                f"Hostname {hostname} should be invalid"
            )
