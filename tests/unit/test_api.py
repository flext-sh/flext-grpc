"""FLEXT gRPC API Testing - Comprehensive unit tests for public API functions.

This module provides comprehensive unit testing for all FLEXT gRPC public API functions,
following enterprise testing standards with factory function validation, configuration
testing, and integration pattern verification.

Test Coverage:
    The module ensures comprehensive coverage of all public API functions:
    - Factory Functions: create_server, create_client, create_channel, create_service
    - Configuration Functions: create_config with validation and defaults
    - Validation Functions: validate_address, parse_address with error handling
    - Utility Functions: create_complete_setup for rapid development scenarios
    - Stream Functions: create_stream with type validation and configuration

Testing Architecture:
    API testing follows enterprise testing principles:
    - Function Isolation: Each API function tested independently
    - Parameter Validation: All parameter combinations and edge cases tested
    - Return Value Validation: Entity creation and configuration verification
    - Error Handling: Invalid input handling and error reporting validation
    - Integration Testing: API function coordination and entity compatibility

Testing Patterns:
    All API tests follow enterprise testing standards:
    - AAA Pattern: Arrange, Act, Assert structure for clarity
    - Boundary Testing: Valid and invalid parameter boundary conditions
    - Default Validation: Default parameter behavior verification
    - Error Scenarios: Comprehensive failure case testing and error messages
    - Factory Pattern: Entity creation validation through factory functions

# Test Constants - Configuration values for consistent testing
EXPECTED_BULK_SIZE = 2         # Expected size for bulk operations
EXPECTED_TOTAL_PAGES = 8       # Expected pagination count
EXPECTED_DATA_COUNT = 3        # Expected data elements in test scenarios

Example:
    Standard API function testing pattern used throughout module:

    >>> def test_create_entity_with_valid_parameters():
    ...     # Arrange: Set up valid parameters
    ...     params = create_valid_parameters()
    ...
    ...     # Act: Call API function
    ...     entity = create_server(**params)
    ...
    ...     # Assert: Verify entity creation and validation
    ...     assert entity is not None
    ...     assert entity.validate_domain_rules().is_success

Integration:
    - Tests API functions from flext_grpc.api module
    - Validates entity creation through factory patterns
    - Uses flext-core patterns for consistent entity behavior
    - Integrates with pytest framework for execution and coverage

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from flext_grpc.api import (
    create_channel,
    create_client,
    create_complete_setup,
    create_config,
    create_server,
    create_service,
    create_stream,
    parse_address,
    validate_address,
)
from flext_grpc.config import FlextGrpcConfig
from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)


class TestAPIFunctions:
    """Test API factory functions."""

    def test_create_server(self) -> None:
        """Test create_server function."""
        server = create_server()
        assert isinstance(server, FlextGrpcServer)
        if server.host != "localhost":
            raise AssertionError(f"Expected {'localhost'}, got {server.host}")
        assert server.port == 50051
        if server.max_workers != 10:
            raise AssertionError(f"Expected {10}, got {server.max_workers}")
        assert server.state == "stopped"
        if len(server.services) != 0:
            raise AssertionError(f"Expected {0}, got {len(server.services)}")

        # Test with custom parameters
        custom_server = create_server("0.0.0.0", 8080, 20)
        if custom_server.host != "0.0.0.0":
            raise AssertionError(f"Expected {'0.0.0.0'}, got {custom_server.host}")
        assert custom_server.port == 8080
        if custom_server.max_workers != 20:
            raise AssertionError(f"Expected {20}, got {custom_server.max_workers}")

    def test_create_client(self) -> None:
        """Test create_client function."""
        client = create_client("localhost:50051")
        assert isinstance(client, FlextGrpcClient)
        assert client.channel is not None
        if client.channel.target != "localhost:50051":
            raise AssertionError(
                f"Expected {'localhost:50051'}, got {client.channel.target}"
            )
        assert client.channel.state == "idle"

        # Test with options
        options: dict[str, object] = {"timeout": 30}
        client_with_options = create_client("localhost:50051", options)
        if client_with_options.options != options:
            raise AssertionError(
                f"Expected {options}, got {client_with_options.options}"
            )

    def test_create_channel(self) -> None:
        """Test create_channel function."""
        channel = create_channel("localhost:50051")
        assert isinstance(channel, FlextGrpcChannel)
        if channel.target != "localhost:50051":
            raise AssertionError(f"Expected {'localhost:50051'}, got {channel.target}")
        assert channel.state == "idle"

        # Test with options
        options: dict[str, object] = {"compression": "gzip"}
        channel_with_options = create_channel("localhost:50051", options)
        if channel_with_options.options != options:
            raise AssertionError(
                f"Expected {options}, got {channel_with_options.options}"
            )

    def test_create_service(self) -> None:
        """Test create_service function."""
        service = create_service("TestService")
        assert isinstance(service, FlextGrpcService)
        if service.name != "TestService":
            raise AssertionError(f"Expected {'TestService'}, got {service.name}")
        assert len(service.methods) == 0

        # Test with methods
        methods = ["method1", "method2"]
        service_with_methods = create_service("TestService", methods)
        if service_with_methods.methods != methods:
            raise AssertionError(
                f"Expected {methods}, got {service_with_methods.methods}"
            )

    def test_create_stream(self) -> None:
        """Test create_stream function."""
        stream = create_stream("test_method")
        assert isinstance(stream, FlextGrpcStream)
        if stream.method_name != "test_method":
            raise AssertionError(f"Expected {'test_method'}, got {stream.method_name}")
        assert stream.stream_type == "unary"

        # Test with custom stream type
        server_stream = create_stream("test_method", "server_streaming")
        if server_stream.stream_type != "server_streaming":
            raise AssertionError(
                f"Expected {'server_streaming'}, got {server_stream.stream_type}"
            )

    def test_create_stream_invalid_type(self) -> None:
        """Test create_stream with invalid stream type raises ValueError."""
        with pytest.raises(ValueError, match="Invalid stream type: invalid_type"):
            create_stream("test_method", "invalid_type")  # type: ignore[arg-type]

    def test_create_config(self) -> None:
        """Test create_config function."""
        config = create_config()
        assert isinstance(config, FlextGrpcConfig)
        if config.host != "localhost":
            raise AssertionError(f"Expected {'localhost'}, got {config.host}")
        assert config.port == 50051
        if config.max_workers != 10:
            raise AssertionError(f"Expected {10}, got {config.max_workers}")
        assert config.timeout == 30.0

        # Test with custom parameters
        custom_config = create_config("0.0.0.0", 8080, 20, 60.0)
        if custom_config.host != "0.0.0.0":
            raise AssertionError(f"Expected {'0.0.0.0'}, got {custom_config.host}")
        assert custom_config.port == 8080
        if custom_config.max_workers != 20:
            raise AssertionError(f"Expected {20}, got {custom_config.max_workers}")
        assert custom_config.timeout == 60.0

    def test_validate_address(self) -> None:
        """Test validate_address function."""
        # Valid addresses
        valid_addresses = [
            "localhost:50051",
            "127.0.0.1:8080",
            "example.com:443",
        ]

        for address in valid_addresses:
            result = validate_address(address)
            assert result.is_success, f"Address {address} should be valid"
            if not (result.data):
                raise AssertionError(f"Expected True, got {result.data}")

        # Invalid addresses
        invalid_addresses = [
            "",
            "localhost",
            ":50051",
            "localhost:",
            "localhost:abc",
            "localhost:-1",
            "localhost:70000",
            "host:port:extra",  # Test line 796 - too many parts
        ]

        for address in invalid_addresses:
            result = validate_address(address)
            assert result.is_failure, f"Address {address} should be invalid"

    def test_validate_address_exception_handling(self) -> None:
        """Test validate_address exception handling for lines 769-770."""
        # Test with an address that might cause AttributeError or ValueError
        result = validate_address(None)  # type: ignore[arg-type]
        assert result.is_failure
        # The error should either be empty address error or exception error
        assert (
            "Address cannot be empty" in result.error
            or "Address validation error:" in result.error
        )

    def test_parse_address(self) -> None:
        """Test parse_address function."""
        # Valid parsing
        result = parse_address("localhost:50051")
        if result != {"host": "localhost", "port": 50051}:
            raise AssertionError(
                f'Expected {{"host": "localhost", "port": 50051}}, got {result}'
            )

        result = parse_address("127.0.0.1:8080")
        if result != {"host": "127.0.0.1", "port": 8080}:
            raise AssertionError(
                f'Expected {{"host": "127.0.0.1", "port": 8080}}, got {result}'
            )

        # Invalid parsing should raise ValueError
        with pytest.raises(ValueError, match="Port must be a number"):
            parse_address("invalid:address")

        with pytest.raises(ValueError, match="Address must be in host:port format"):
            parse_address("missing_port")

        with pytest.raises(ValueError, match="Invalid host format"):
            parse_address("invalid_port:abc")

    def test_create_complete_setup(self) -> None:
        """Test create_complete_setup function."""
        setup = create_complete_setup()
        self._validate_setup_components(setup)
        self._validate_default_values(setup)
        self._validate_custom_setup()

    def _validate_setup_components(self, setup: dict[str, object]) -> None:
        """Validate setup components are present and correct types."""
        # Check all components are created
        required_keys = ["server", "client", "service", "target"]
        for key in required_keys:
            if key not in setup:
                raise AssertionError(f"Expected {key} in {setup}")

        # Check types
        from flext_grpc.entities import (
            FlextGrpcClient,
            FlextGrpcServer,
            FlextGrpcService,
        )

        assert isinstance(setup["server"], FlextGrpcServer)
        assert isinstance(setup["client"], FlextGrpcClient)
        assert isinstance(setup["service"], FlextGrpcService)
        assert isinstance(setup["target"], str)

    def _validate_default_values(self, setup: dict[str, object]) -> None:
        """Validate default values in setup."""
        from flext_grpc.entities import (
            FlextGrpcClient,
            FlextGrpcServer,
            FlextGrpcService,
        )

        server = setup["server"]
        client = setup["client"]
        service = setup["service"]
        target = setup["target"]

        assert isinstance(server, FlextGrpcServer)
        assert isinstance(client, FlextGrpcClient)
        assert isinstance(service, FlextGrpcService)

        if server.host != "localhost":
            raise AssertionError(f"Expected localhost, got {server.host}")
        assert server.port == 50051
        if client.target != "localhost:50051":
            raise AssertionError(f"Expected localhost:50051, got {client.target}")
        assert service.name == "DefaultService"
        if target != "localhost:50051":
            raise AssertionError(f"Expected localhost:50051, got {target}")

    def _validate_custom_setup(self) -> None:
        """Validate custom setup parameters."""
        custom_setup = create_complete_setup(
            "0.0.0.0",
            8080,
            "CustomService",
            ["method1", "method2"],
        )

        from flext_grpc.entities import FlextGrpcServer, FlextGrpcService

        custom_server = custom_setup["server"]
        custom_service = custom_setup["service"]

        assert isinstance(custom_server, FlextGrpcServer)
        assert custom_server.host == "0.0.0.0"
        assert custom_server.port == 8080

        assert isinstance(custom_service, FlextGrpcService)
        assert custom_service.name == "CustomService"
        assert custom_service.methods == ["method1", "method2"]
        assert custom_setup["target"] == "0.0.0.0:8080"

    def test_factory_functions_create_valid_entities(self) -> None:
        """Test that all factory functions create valid entities."""
        # Create entities
        server = create_server()
        client = create_client("localhost:50051")
        channel = create_channel("localhost:50051")
        service = create_service("TestService", ["method1"])
        stream = create_stream("test_method", "server_streaming")

        # Validate all entities
        assert server.validate_domain_rules().is_success
        assert client.validate_domain_rules().is_success
        assert channel.validate_domain_rules().is_success
        assert service.validate_domain_rules().is_success
        assert stream.validate_domain_rules().is_success

    def test_factory_functions_use_proper_ids(self) -> None:
        """Test that factory functions generate proper IDs."""
        server = create_server()
        client = create_client("localhost:50051")
        channel = create_channel("localhost:50051")
        service = create_service("TestService")
        stream = create_stream("test_method")

        # All should have non-empty IDs
        assert server.id
        assert client.id
        assert channel.id
        assert service.id
        assert stream.id

        # IDs should be unique
        ids = [server.id, client.id, channel.id, service.id, stream.id]
        if len(set(ids)) != len(ids):  # All unique
            raise AssertionError(f"Expected {len(ids)}, got {len(set(ids))}")

    def test_factory_functions_use_proper_timestamps(self) -> None:
        """Test that factory functions generate proper timestamps."""

        before = datetime.now(UTC)

        server = create_server()
        client = create_client("localhost:50051")
        channel = create_channel("localhost:50051")
        service = create_service("TestService")
        stream = create_stream("test_method")

        after = datetime.now(UTC)

        # All should have timestamps within expected range
        entities = [server, client, channel, service, stream]
        for entity in entities:
            assert before <= entity.created_at <= after
