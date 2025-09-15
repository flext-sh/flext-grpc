"""Unit tests for gRPC entities.

The module ensures comprehensive coverage of all entity behaviors:
- FlextGrpcChannel: Network channel lifecycle and state management testing
- FlextGrpcServer: Server entity validation and lifecycle operation testing
- FlextGrpcClient: Client entity creation and connection management testing
- FlextGrpcService: Service definition and method specification testing
- FlextGrpcStream: Stream entity creation and type validation testing

Testing Architecture: Entity testing follows Clean Architecture testing principles:
- Domain Logic Testing: Pure business logic validation without external dependencies
- Entity Validation: Comprehensive domain rule validation and constraint testing
- State Management: Complete lifecycle and state transition validation
- Boundary Conditions: Edge cases and invalid input handling
- Error Scenarios: Comprehensive failure case testing and error reporting

Testing Patterns: All tests follow enterprise testing standards:
- AAA Pattern: Arrange, Act, Assert structure for clarity
- Isolation: No external dependencies or side effects
- Deterministic: Consistent results across multiple runs
- Fast Execution: Sub-100ms execution for rapid feedback
- Descriptive Names: Clear test intent and coverage description

Integration:
- Validates entities created by flext_grpc.entities module
- Uses flext-core testing utilities for data generation
- Integrates with pytest framework for execution and reporting
- Supports coverage analysis and quality gate enforcement

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from flext_core import FlextUtilities
from pydantic_core import ValidationError

from flext_grpc import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
    TGrpcTarget,
)

# Constants
EXPECTED_BULK_SIZE = 2


class TestFlextGrpcChannel:
    """Comprehensive unit tests for FlextGrpcChannel entity with enterprise testing standards.

    Test suite for FlextGrpcChannel domain entity covering creation, validation,
    state management, and business rule enforcement. Ensures entity behaves
    correctly across all scenarios including edge cases and error conditions.

    Test Categories:
      - Creation Testing: Valid and invalid channel creation scenarios
      - Validation Testing: Domain rule validation and constraint enforcement
      - State Management: Channel state transitions and lifecycle validation
      - Error Handling: Invalid input handling and error reporting
      - Business Rules: Channel-specific business logic validation

    Coverage Focus:
      - Target address validation and format compliance
      - Channel state management and transition rules
      - Options configuration and validation
      - Entity lifecycle and immutable state handling
      - Integration with type system and validation utilities
    """

    def test_create_valid_channel(self) -> None:
        """Test creating a valid gRPC channel entity with proper configuration.

        Validates that FlextGrpcChannel can be created with valid parameters
        and passes domain rule validation. Tests fundamental entity creation
        pattern with proper target address and state initialization.

        Test Flow:
            1. Arrange: Create channel with valid target and state
            2. Act: Validate domain rules
            3. Assert: Validation succeeds and properties are correct
        """
        channel = FlextGrpcChannel(
            id=FlextUtilities.Generators.generate_entity_id(),
            target=TGrpcTarget("localhost:50051"),
            state="idle",
            created_at=datetime.now(UTC),
        )

        validation = channel.validate_business_rules()
        assert validation.success
        if channel.target != "localhost:50051":
            msg: str = f"Expected {'localhost:50051'}, got {channel.target}"
            raise AssertionError(msg)
        assert channel.state == "idle"

    def test_invalid_empty_target(self) -> None:
        """Test channel creation with empty target fails domain validation.

        Validates that FlextGrpcChannel properly enforces target validation
        rules and rejects empty target addresses. Tests boundary condition
        handling and proper error reporting for invalid configurations.

        Test Flow:
            1. Arrange: Create channel with empty target
            2. Act: Validate domain rules
            3. Assert: Validation fails with appropriate error message
        """
        channel = FlextGrpcChannel(
            id=FlextUtilities.Generators.generate_entity_id(),
            target=TGrpcTarget(""),
            created_at=datetime.now(UTC),
        )

        validation = channel.validate_business_rules()
        assert validation.is_failure
        if validation.error is None or "target cannot be empty" not in validation.error:
            msg: str = f"Expected {'target cannot be empty'} in {validation.error}"
            raise AssertionError(msg)

    def test_invalid_channel_state(self) -> None:
        """Test channel with invalid state fails validation."""
        # Pydantic validates types at creation time
        # All imports are at the top of the file

        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcChannel(
                id=FlextUtilities.Generators.generate_entity_id(),
                target=TGrpcTarget("localhost:50051"),
                state="invalid_state",
                created_at=datetime.now(UTC),
            )

        # Verify the error message contains expected text
        error_str = str(exc_info.value)
        if "Input should be" not in error_str:
            msg: str = f"Expected validation error for invalid state, got: {error_str}"
            raise AssertionError(msg)

    def test_channel_connection_lifecycle(self) -> None:
        """Test channel connection state transitions."""
        channel = FlextGrpcChannel(
            id=FlextUtilities.Generators.generate_entity_id(),
            target=TGrpcTarget("localhost:50051"),
            state="idle",
            created_at=datetime.now(UTC),
        )

        # Connect
        connecting_result = channel.connect()
        assert connecting_result.success
        connecting_channel = connecting_result.data
        assert connecting_channel is not None
        if connecting_channel.state != "connecting":
            msg: str = f"Expected {'connecting'}, got {connecting_channel.state}"
            raise AssertionError(msg)

        # Mark ready
        ready_result = connecting_channel.mark_ready()
        assert ready_result.success
        ready_channel = ready_result.data
        assert ready_channel is not None
        if ready_channel.state != "ready":
            msg: str = f"Expected {'ready'}, got {ready_channel.state}"
            raise AssertionError(msg)
        assert ready_channel.is_ready()

        # Disconnect
        idle_result = ready_channel.disconnect()
        assert idle_result.success
        idle_channel = idle_result.data
        assert idle_channel is not None
        if idle_channel.state != "idle":
            msg: str = f"Expected {'idle'}, got {idle_channel.state}"
            raise AssertionError(msg)
        assert not idle_channel.is_ready()

    def test_invalid_state_transitions(self) -> None:
        """Test invalid state transitions fail."""
        channel = FlextGrpcChannel(
            id=FlextUtilities.Generators.generate_entity_id(),
            target=TGrpcTarget("localhost:50051"),
            state="ready",
            created_at=datetime.now(UTC),
        )

        # Cannot connect from ready state
        connect_result = channel.connect()
        assert connect_result.is_failure
        if (
            connect_result.error is None
            or "Cannot connect from state: ready" not in connect_result.error
        ):
            msg: str = f"Expected {'Cannot connect from state: ready'} in {connect_result.error}"
            raise AssertionError(msg)

        # Cannot mark ready from ready state
        ready_result = channel.mark_ready()
        assert ready_result.is_failure
        if (
            ready_result.error is None
            or "Cannot mark ready from state: ready" not in ready_result.error
        ):
            msg: str = f"Expected {'Cannot mark ready from state: ready'} in {ready_result.error}"
            raise AssertionError(msg)


class TestFlextGrpcServer:
    """Test FlextGrpcServer entity."""

    def test_create_valid_server(self) -> None:
        """Test creating a valid server."""
        server = FlextGrpcServer(
            id=FlextUtilities.Generators.generate_entity_id(),
            host="localhost",
            port=50051,
            max_workers=10,
            created_at=datetime.now(UTC),
        )

        validation = server.validate_business_rules()
        assert validation.success
        if server.address != "localhost:50051":
            msg: str = f"Expected {'localhost:50051'}, got {server.address}"
            raise AssertionError(msg)
        assert not server.is_running

    def test_invalid_server_configuration(self) -> None:
        """Test invalid server configurations fail validation."""
        # Empty host
        server1 = FlextGrpcServer(
            id=FlextUtilities.Generators.generate_entity_id(),
            host="",
            port=50051,
            created_at=datetime.now(UTC),
        )
        validation1 = server1.validate_business_rules()
        assert validation1.is_failure
        if validation1.error is None or "host cannot be empty" not in validation1.error:
            msg: str = f"Expected {'host cannot be empty'} in {validation1.error}"
            raise AssertionError(msg)

        # Invalid port
        server2 = FlextGrpcServer(
            id=FlextUtilities.Generators.generate_entity_id(),
            host="localhost",
            port=70000,  # Too high
            created_at=datetime.now(UTC),
        )
        validation2 = server2.validate_business_rules()
        assert validation2.is_failure
        if validation2.error is None or "Invalid port" not in validation2.error:
            msg: str = f"Expected {'Invalid port'} in {validation2.error}"
            raise AssertionError(msg)

        # Invalid max_workers
        server3 = FlextGrpcServer(
            id=FlextUtilities.Generators.generate_entity_id(),
            host="localhost",
            port=50051,
            max_workers=0,
            created_at=datetime.now(UTC),
        )
        validation3 = server3.validate_business_rules()
        assert validation3.is_failure
        if (
            validation3.error is None
            or "Max workers must be >= 1" not in validation3.error
        ):
            msg: str = f"Expected {'Max workers must be >= 1'} in {validation3.error}"
            raise AssertionError(msg)

    def test_server_lifecycle(self) -> None:
        """Test server lifecycle state transitions."""
        server = FlextGrpcServer(
            id=FlextUtilities.Generators.generate_entity_id(),
            host="localhost",
            port=50051,
            created_at=datetime.now(UTC),
        )

        # Start server
        starting_result = server.start()
        assert starting_result.success
        starting_server = starting_result.data
        assert starting_server is not None
        if starting_server.state != "starting":
            msg: str = f"Expected {'starting'}, got {starting_server.state}"
            raise AssertionError(msg)

        # Mark running
        running_result = starting_server.mark_running()
        assert running_result.success
        running_server = running_result.data
        assert running_server is not None
        if running_server.state != "running":
            msg: str = f"Expected {'running'}, got {running_server.state}"
            raise AssertionError(msg)
        assert running_server.is_running

        # Stop server
        stopping_result = running_server.stop()
        assert stopping_result.success
        stopping_server = stopping_result.data
        assert stopping_server is not None
        if stopping_server.state != "stopping":
            msg: str = f"Expected {'stopping'}, got {stopping_server.state}"
            raise AssertionError(msg)

        # Mark stopped
        stopped_result = stopping_server.mark_stopped()
        assert stopped_result.success
        stopped_server = stopped_result.data
        assert stopped_server is not None
        if stopped_server.state != "stopped":
            msg: str = f"Expected {'stopped'}, got {stopped_server.state}"
            raise AssertionError(msg)
        assert not stopped_server.is_running

    def test_add_service_to_server(self) -> None:
        """Test adding services to server."""
        server = FlextGrpcServer(
            id=FlextUtilities.Generators.generate_entity_id(),
            host="localhost",
            port=50051,
            created_at=datetime.now(UTC),
        )

        service = FlextGrpcService(
            id=FlextUtilities.Generators.generate_entity_id(),
            name="TestService",
            methods=["test_method"],
            created_at=datetime.now(UTC),
        )

        # Add service
        updated_result = server.add_service(service)
        assert updated_result.success
        updated_server = updated_result.data
        assert updated_server is not None
        if len(updated_server.services) != 1:
            msg: str = f"Expected {1}, got {len(updated_server.services)}"
            raise AssertionError(msg)

        # Cannot add same service twice
        duplicate_result = updated_server.add_service(service)
        assert duplicate_result.is_failure
        if (
            duplicate_result.error is None
            or "Service already exists" not in duplicate_result.error
        ):
            msg: str = (
                f"Expected {'Service already exists'} in {duplicate_result.error}"
            )
            raise AssertionError(msg)


class TestFlextGrpcService:
    """Test FlextGrpcService entity."""

    def test_create_valid_service(self) -> None:
        """Test creating a valid service."""
        service = FlextGrpcService(
            id=FlextUtilities.Generators.generate_entity_id(),
            name="TestService",
            methods=["method1", "method2"],
            created_at=datetime.now(UTC),
        )

        validation = service.validate_business_rules()
        assert validation.success
        assert service.has_method("method1")
        assert service.has_method("method2")
        assert not service.has_method("method3")

    def test_invalid_service_configuration(self) -> None:
        """Test invalid service configurations fail validation."""
        # Empty name
        service1 = FlextGrpcService(
            id=FlextUtilities.Generators.generate_entity_id(),
            name="",
            methods=["method1"],
            created_at=datetime.now(UTC),
        )
        validation1 = service1.validate_business_rules()
        assert validation1.is_failure
        if validation1.error is None or "name cannot be empty" not in validation1.error:
            msg: str = f"Expected {'name cannot be empty'} in {validation1.error}"
            raise AssertionError(msg)

        # No methods
        service2 = FlextGrpcService(
            id=FlextUtilities.Generators.generate_entity_id(),
            name="TestService",
            methods=[],
            created_at=datetime.now(UTC),
        )
        validation2 = service2.validate_business_rules()
        assert validation2.is_failure
        if (
            validation2.error is None
            or "must have at least one method" not in validation2.error
        ):
            msg: str = (
                f"Expected {'must have at least one method'} in {validation2.error}"
            )
            raise AssertionError(msg)

    def test_add_method(self) -> None:
        """Test adding methods to service."""
        service = FlextGrpcService(
            id=FlextUtilities.Generators.generate_entity_id(),
            name="TestService",
            methods=["method1"],
            created_at=datetime.now(UTC),
        )

        # Add new method
        updated_result = service.add_method("method2")
        assert updated_result.success
        updated_service = updated_result.data
        assert updated_service is not None
        if len(updated_service.methods) != EXPECTED_BULK_SIZE:
            msg: str = f"Expected {2}, got {len(updated_service.methods)}"
            raise AssertionError(msg)
        assert updated_service.has_method("method2")

        # Cannot add existing method
        duplicate_result = updated_service.add_method("method1")
        assert duplicate_result.is_failure
        if (
            duplicate_result.error is None
            or "Method already exists" not in duplicate_result.error
        ):
            msg: str = f"Expected {'Method already exists'} in {duplicate_result.error}"
            raise AssertionError(msg)


class TestFlextGrpcClient:
    """Test FlextGrpcClient entity."""

    def test_create_valid_client(self) -> None:
        """Test creating a valid client."""
        channel = FlextGrpcChannel(
            id=FlextUtilities.Generators.generate_entity_id(),
            target=TGrpcTarget("localhost:50051"),
            state="ready",
            created_at=datetime.now(UTC),
        )

        client = FlextGrpcClient(
            id=FlextUtilities.Generators.generate_entity_id(),
            channel=channel,
            created_at=datetime.now(UTC),
        )

        validation = client.validate_business_rules()
        assert validation.success
        assert client.is_connected
        if client.target != "localhost:50051":
            msg: str = f"Expected {'localhost:50051'}, got {client.target}"
            raise AssertionError(msg)

    def test_client_without_channel(self) -> None:
        """Test client without channel."""
        client = FlextGrpcClient(
            id=FlextUtilities.Generators.generate_entity_id(),
            channel=None,
            created_at=datetime.now(UTC),
        )

        validation = client.validate_business_rules()
        assert validation.success
        assert not client.is_connected
        assert client.target is None

    def test_connect_to_target(self) -> None:
        """Test connecting client to target."""
        client = FlextGrpcClient(
            id=FlextUtilities.Generators.generate_entity_id(),
            channel=None,
            created_at=datetime.now(UTC),
        )

        connected_result = client.connect_to("localhost:8080")
        assert connected_result.success
        connected_client = connected_result.data
        assert connected_client is not None
        assert connected_client.channel is not None
        if connected_client.target != "localhost:8080":
            msg: str = f"Expected {'localhost:8080'}, got {connected_client.target}"
            raise AssertionError(msg)


class TestFlextGrpcStream:
    """Test FlextGrpcStream entity."""

    def test_create_valid_stream(self) -> None:
        """Test creating a valid stream."""
        stream = FlextGrpcStream(
            id=FlextUtilities.Generators.generate_entity_id(),
            method_name="TestMethod",
            stream_type="server_streaming",
            created_at=datetime.now(UTC),
        )

        validation = stream.validate_business_rules()
        assert validation.success
        assert stream.is_streaming
        assert stream.is_server_streaming
        assert not stream.is_client_streaming
        assert not stream.is_bidirectional

    def test_invalid_stream_configuration(self) -> None:
        """Test invalid stream configurations fail validation."""
        # Empty method name - this should fail domain validation
        stream1 = FlextGrpcStream(
            id=FlextUtilities.Generators.generate_entity_id(),
            method_name="",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )
        validation1 = stream1.validate_business_rules()
        assert validation1.is_failure
        if (
            validation1.error is None
            or "method name cannot be empty" not in validation1.error
        ):
            msg: str = (
                f"Expected {'method name cannot be empty'} in {validation1.error}"
            )
            raise AssertionError(msg)

        # Invalid stream type - Pydantic validates at creation time
        # All imports are at the top of the file

        with pytest.raises(ValidationError) as exc_info:
            FlextGrpcStream(
                id=FlextUtilities.Generators.generate_entity_id(),
                method_name="TestMethod",
                stream_type="invalid_type",
                created_at=datetime.now(UTC),
            )

        # Verify the error message contains expected text
        error_str = str(exc_info.value)
        if "Input should be" not in error_str:
            msg: str = (
                f"Expected validation error for invalid stream type, got: {error_str}"
            )
            raise AssertionError(msg)

    def test_stream_type_detection(self) -> None:
        """Test stream type detection methods."""
        # Unary stream
        unary_stream = FlextGrpcStream(
            id=FlextUtilities.Generators.generate_entity_id(),
            method_name="TestMethod",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )
        assert not unary_stream.is_streaming
        assert not unary_stream.is_server_streaming
        assert not unary_stream.is_client_streaming
        assert not unary_stream.is_bidirectional

        # Server streaming
        server_stream = FlextGrpcStream(
            id=FlextUtilities.Generators.generate_entity_id(),
            method_name="TestMethod",
            stream_type="server_streaming",
            created_at=datetime.now(UTC),
        )
        assert server_stream.is_streaming
        assert server_stream.is_server_streaming
        assert not server_stream.is_client_streaming
        assert not server_stream.is_bidirectional

        # Client streaming
        client_stream = FlextGrpcStream(
            id=FlextUtilities.Generators.generate_entity_id(),
            method_name="TestMethod",
            stream_type="client_streaming",
            created_at=datetime.now(UTC),
        )
        assert client_stream.is_streaming
        assert not client_stream.is_server_streaming
        assert client_stream.is_client_streaming
        assert not client_stream.is_bidirectional

        # Bidirectional streaming
        bi_stream = FlextGrpcStream(
            id=FlextUtilities.Generators.generate_entity_id(),
            method_name="TestMethod",
            stream_type="bidirectional",
            created_at=datetime.now(UTC),
        )
        assert bi_stream.is_streaming
        assert bi_stream.is_server_streaming
        assert bi_stream.is_client_streaming
        assert bi_stream.is_bidirectional
