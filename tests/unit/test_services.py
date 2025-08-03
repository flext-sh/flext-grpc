"""FLEXT gRPC Service Testing - Comprehensive unit tests for domain services.

This module provides comprehensive unit testing for all FLEXT gRPC domain services,
following enterprise testing standards with service operation validation, business
logic testing, and comprehensive error handling verification.

Test Coverage:
    The module ensures comprehensive coverage of all service operations:
    - FlextGrpcService: Unified service operations and command handling
    - Server Operations: Server lifecycle management and state transitions
    - Client Operations: Client connection management and communication
    - Stream Operations: Stream management and type validation
    - Error Handling: Comprehensive failure scenario testing

Testing Architecture:
    Service testing follows Clean Architecture and Domain-Driven Design principles:
    - Business Logic Testing: Service operations and business rule enforcement
    - Command Handling: Service command execution and result validation
    - State Management: Entity state transitions through service operations
    - Error Propagation: Service error handling and failure recovery
    - Integration Testing: Service coordination and dependency management

Testing Patterns:
    All service tests follow enterprise testing standards:
    - AAA Pattern: Arrange, Act, Assert structure for clarity
    - Service Isolation: Services tested with mocked dependencies
    - Operation Validation: Each service operation thoroughly tested
    - Error Scenarios: Comprehensive failure case testing
    - Result Pattern: FlextResult pattern validation throughout

Example:
    Standard service testing pattern used throughout module:

    >>> def test_service_operation_success():
    ...     # Arrange: Set up service and test data
    ...     service = FlextGrpcService()
    ...     entity = create_valid_entity()
    ...
    ...     # Act: Execute service operation
    ...     result = service.execute("operation", entity)
    ...
    ...     # Assert: Verify successful execution and state
    ...     assert result.is_success
    ...     assert result.data.state == expected_state

Integration:
    - Tests services from flext_grpc.services module
    - Validates service operations on entities from flext_grpc.entities
    - Uses flext-core FlextResult patterns for operation validation
    - Integrates with pytest framework for execution and reporting

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

from flext_core.utilities import FlextGenerators

from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService as FlextGrpcServiceEntity,
    FlextGrpcStream,
)
from flext_grpc.services import FlextGrpcService
from flext_grpc.types import TGrpcTarget

if TYPE_CHECKING:
    from flext_core import FlextResult


def _assert_error_contains(result: FlextResult[object], expected_text: str) -> None:
    """Helper to assert error contains expected text - DRY principle."""
    assert result.is_failure
    if result.error is None or expected_text not in result.error:
        raise AssertionError(f"Expected '{expected_text}' in {result.error}")


def _assert_server_result(result: FlextResult[object]) -> FlextGrpcServer:
    """Helper to validate and return server result - DRY principle."""
    assert result.is_success
    assert result.data is not None
    if not isinstance(result.data, FlextGrpcServer):
        raise TypeError(f"Expected FlextGrpcServer, got {type(result.data)}")
    return result.data


def _assert_client_result(result: FlextResult[object]) -> FlextGrpcClient:
    """Helper to validate and return client result - DRY principle."""
    assert result.is_success
    assert result.data is not None
    if not isinstance(result.data, FlextGrpcClient):
        raise TypeError(f"Expected FlextGrpcClient, got {type(result.data)}")
    return result.data


def _assert_dict_result(result: FlextResult[object]) -> dict[str, object]:
    """Helper to validate and return dict result - DRY principle."""
    assert result.is_success
    assert result.data is not None
    if not isinstance(result.data, dict):
        raise TypeError(f"Expected dict, got {type(result.data)}")
    return result.data


class TestFlextGrpcService:
    """Test FlextGrpcService application service."""

    def setup_method(self) -> None:
        """Set up test fixtures."""
        self.service = FlextGrpcService()

        self.server = FlextGrpcServer(
            id=FlextGenerators.generate_entity_id(),
            host="localhost",
            port=50051,
            created_at=datetime.now(UTC),
        )

        self.channel = FlextGrpcChannel(
            id=FlextGenerators.generate_entity_id(),
            target=TGrpcTarget("localhost:50051"),
            state="idle",
            created_at=datetime.now(UTC),
        )

        self.client = FlextGrpcClient(
            id=FlextGenerators.generate_entity_id(),
            channel=self.channel,
            created_at=datetime.now(UTC),
        )

    def test_execute_without_operation_type_fails(self) -> None:
        """Test execute without operation type fails."""
        result = self.service.execute()
        _assert_error_contains(result, "Missing required argument: service_type")

    def test_execute_with_unknown_operation_type_fails(self) -> None:
        """Test execute with unknown operation type fails."""
        result = self.service.execute("unknown_type")
        _assert_error_contains(result, "Unknown service type: unknown_type")

    def test_server_start_operation(self) -> None:
        """Test server start operation."""
        result = self.service.execute("server", "start", self.server)
        started_server = _assert_server_result(result)
        if started_server.state != "running":
            raise AssertionError(f"Expected 'running', got {started_server.state}")

    def test_server_start_already_running_fails(self) -> None:
        """Test starting already running server fails."""
        running_server = self.server.copy_with(state="running").data
        assert running_server is not None
        result = self.service.execute("server", "start", running_server)
        _assert_error_contains(result, "Server is already running")

    def test_server_start_invalid_server_fails(self) -> None:
        """Test starting invalid server fails."""
        # Create invalid server directly - copy_with will fail validation
        from flext_grpc.entities import FlextGrpcServer

        invalid_server = FlextGrpcServer(
            id=self.server.id,
            host="",  # Invalid empty host
            port=self.server.port,
            created_at=self.server.created_at,
        )
        result = self.service.execute("server", "start", invalid_server)
        _assert_error_contains(result, "Invalid server")

    def test_server_stop_operation(self) -> None:
        """Test server stop operation."""
        running_server = self.server.copy_with(state="running").data
        assert running_server is not None
        result = self.service.execute("server", "stop", running_server)
        stopped_server = _assert_server_result(result)
        if stopped_server.state != "stopped":
            raise AssertionError(f"Expected 'stopped', got {stopped_server.state}")

    def test_server_stop_not_running_fails(self) -> None:
        """Test stopping non-running server fails."""
        result = self.service.execute("server", "stop", self.server)
        _assert_error_contains(result, "Server is not running")

    def test_server_add_service_operation(self) -> None:
        """Test server add service operation."""
        service_entity = FlextGrpcServiceEntity(
            id=FlextGenerators.generate_entity_id(),
            name="TestService",
            methods=["test_method"],
            created_at=datetime.now(UTC),
        )

        result = self.service.execute(
            "server", "add_service", self.server, service=service_entity
        )
        updated_server = _assert_server_result(result)
        if len(updated_server.services) != 1:
            raise AssertionError(f"Expected 1, got {len(updated_server.services)}")

    def test_server_add_service_without_service_fails(self) -> None:
        """Test server add service without service fails."""
        result = self.service.execute("server", "add_service", self.server)
        _assert_error_contains(result, "Service required")

    def test_server_status_operation(self) -> None:
        """Test server status operation."""
        result = self.service.execute("server", "status", self.server)
        status = _assert_dict_result(result)
        if status["address"] != "localhost:50051":
            raise AssertionError(
                f"Expected {'localhost:50051'}, got {status['address']}"
            )
        assert status["state"] == "stopped"
        if status["is_running"]:
            raise AssertionError(f"Expected False, got {status['is_running']}")
        assert status["service_count"] == 0
        if status["max_workers"] != 10:
            raise AssertionError(f"Expected {10}, got {status['max_workers']}")

    def test_server_unknown_operation_fails(self) -> None:
        """Test server unknown operation fails."""
        result = self.service.execute("server", "unknown_op", self.server)
        assert result.is_failure
        _assert_error_contains(result, "Unknown server operation: unknown_op")

    def test_client_connect_operation(self) -> None:
        """Test client connect operation."""
        result = self.service.execute("client", "connect", self.client)
        connected_client = _assert_client_result(result)
        if connected_client.channel is None:
            msg = "Expected channel to be present"
            raise AssertionError(msg)
        if connected_client.channel.state != "ready":
            raise AssertionError(
                f"Expected {'ready'}, got {connected_client.channel.state}"
            )

    def test_client_connect_already_connected_fails(self) -> None:
        """Test connecting already connected client fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        assert ready_channel is not None
        connected_client = self.client.copy_with(channel=ready_channel).data
        assert connected_client is not None

        result = self.service.execute("client", "connect", connected_client)
        assert result.is_failure
        _assert_error_contains(result, "Client is already connected")

    def test_client_connect_no_channel_fails(self) -> None:
        """Test connecting client without channel fails."""
        no_channel_client = self.client.copy_with(channel=None).data
        assert no_channel_client is not None
        result = self.service.execute("client", "connect", no_channel_client)
        assert result.is_failure
        _assert_error_contains(result, "Client has no channel")

    def test_client_disconnect_operation(self) -> None:
        """Test client disconnect operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        assert ready_channel is not None
        connected_client = self.client.copy_with(channel=ready_channel).data
        assert connected_client is not None

        result = self.service.execute("client", "disconnect", connected_client)
        disconnected_client = _assert_client_result(result)
        if disconnected_client.channel is None:
            msg = "Expected channel to be present"
            raise AssertionError(msg)
        if disconnected_client.channel.state != "idle":
            raise AssertionError(
                f"Expected {'idle'}, got {disconnected_client.channel.state}"
            )

    def test_client_disconnect_not_connected_fails(self) -> None:
        """Test disconnecting non-connected client fails."""
        result = self.service.execute("client", "disconnect", self.client)
        assert result.is_failure
        _assert_error_contains(result, "Client is not connected")

    def test_client_call_operation(self) -> None:
        """Test client call operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        assert ready_channel is not None
        connected_client = self.client.copy_with(channel=ready_channel).data
        assert connected_client is not None

        result = self.service.execute(
            "client",
            "call",
            connected_client,
            method_name="test_method",
            request_data={"key": "value"},
        )
        response = _assert_dict_result(result)
        if response["status"] != "success":
            raise AssertionError(f"Expected 'success', got {response['status']}")
        assert response["method"] == "test_method"
        assert connected_client is not None
        if response["client_id"] != connected_client.id:
            raise AssertionError(
                f"Expected {connected_client.id}, got {response['client_id']}"
            )
        assert response["data"] == {"key": "value"}

    def test_client_call_not_connected_fails(self) -> None:
        """Test calling with non-connected client fails."""
        result = self.service.execute(
            "client",
            "call",
            self.client,
            method_name="test_method",
        )
        assert result.is_failure
        _assert_error_contains(result, "Client is not connected")

    def test_client_call_no_method_name_fails(self) -> None:
        """Test calling without method name fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        assert ready_channel is not None
        connected_client = self.client.copy_with(channel=ready_channel).data
        assert connected_client is not None

        result = self.service.execute("client", "call", connected_client)
        assert result.is_failure
        _assert_error_contains(result, "Method name is required")

    def test_client_status_operation(self) -> None:
        """Test client status operation."""
        result = self.service.execute("client", "status", self.client)
        status = _assert_dict_result(result)
        if status["is_connected"]:
            raise AssertionError(f"Expected False, got {status['is_connected']}")
        assert status["target"] == "localhost:50051"
        if status["channel_state"] != "idle":
            raise AssertionError(f"Expected {'idle'}, got {status['channel_state']}")

    def test_client_unknown_operation_fails(self) -> None:
        """Test client unknown operation fails."""
        result = self.service.execute("client", "unknown_op", self.client)
        assert result.is_failure
        _assert_error_contains(result, "Unknown client operation: unknown_op")

    def test_stream_create_operation(self) -> None:
        """Test stream create operation."""
        ready_channel = self.channel.copy_with(state="ready").data
        assert ready_channel is not None
        connected_client = self.client.copy_with(channel=ready_channel).data
        assert connected_client is not None

        result = self.service.execute(
            "stream",
            "create",
            client=connected_client,
            method_name="stream_method",
            stream_type="server_streaming",
        )
        assert result.is_success
        assert result.data is not None
        # Type-safe cast since we know stream operations return FlextGrpcStream
        from flext_grpc.entities import FlextGrpcStream

        if not isinstance(result.data, FlextGrpcStream):
            raise TypeError(f"Expected FlextGrpcStream, got {type(result.data)}")
        stream = result.data
        if stream.method_name != "stream_method":
            raise AssertionError(
                f"Expected {'stream_method'}, got {stream.method_name}"
            )
        assert stream.stream_type == "server_streaming"

    def test_stream_create_no_client_fails(self) -> None:
        """Test stream create without client fails."""
        result = self.service.execute("stream", "create", method_name="test")
        assert result.is_failure
        if (
            result.error is None
            or "Client must be a FlextGrpcClient instance" not in result.error
        ):
            raise AssertionError(
                f"Expected {'Client must be a FlextGrpcClient instance'} in {result.error}"
            )

    def test_stream_create_client_not_connected_fails(self) -> None:
        """Test stream create with disconnected client fails."""
        result = self.service.execute(
            "stream",
            "create",
            client=self.client,
            method_name="test",
        )
        assert result.is_failure
        _assert_error_contains(result, "Client is not connected")

    def test_stream_create_no_method_name_fails(self) -> None:
        """Test stream create without method name fails."""
        ready_channel = self.channel.copy_with(state="ready").data
        assert ready_channel is not None
        connected_client = self.client.copy_with(channel=ready_channel).data
        assert connected_client is not None

        result = self.service.execute("stream", "create", client=connected_client)
        assert result.is_failure
        _assert_error_contains(result, "Method name is required")

    def test_stream_send_operation(self) -> None:
        """Test stream send operation."""

        stream = FlextGrpcStream(
            id=FlextGenerators.generate_entity_id(),
            method_name="test_method",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        result = self.service.execute("stream", "send", stream=stream)
        assert result.is_success
        if not (result.data):
            raise AssertionError(f"Expected True, got {result.data}")

    def test_stream_close_operation(self) -> None:
        """Test stream close operation."""

        stream = FlextGrpcStream(
            id=FlextGenerators.generate_entity_id(),
            method_name="test_method",
            stream_type="unary",
            created_at=datetime.now(UTC),
        )

        result = self.service.execute("stream", "close", stream=stream)
        assert result.is_success
        if not (result.data):
            raise AssertionError(f"Expected True, got {result.data}")

    def test_stream_unknown_operation_fails(self) -> None:
        """Test stream unknown operation fails."""
        result = self.service.execute("stream", "unknown_op")
        assert result.is_failure
        if (
            result.error is None
            or "Unknown stream operation: unknown_op" not in result.error
        ):
            raise AssertionError(
                f"Expected {'Unknown stream operation: unknown_op'} in {result.error}"
            )
