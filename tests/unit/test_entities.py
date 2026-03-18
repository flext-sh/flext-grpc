"""Tests for flext_grpc.entities module."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_grpc import FlextGrpcModels

FlextGrpcEntities = FlextGrpcModels.Grpc


class TestFlextGrpcEntities:
    """Test cases for FlextGrpcEntities class."""

    def test_grpc_server_creation(self) -> None:
        """Test gRPC server entity creation."""
        server = FlextGrpcEntities.Server(host="localhost", port=50051, max_workers=10)
        tm.that(server.host == "localhost", eq=True)
        tm.that(server.port == 50051, eq=True)
        tm.that(server.max_workers == 10, eq=True)

    def test_grpc_client_creation(self) -> None:
        """Test gRPC client entity creation."""
        client = FlextGrpcEntities.Client()
        tm.that(client is not None, eq=True)

    def test_grpc_channel_creation(self) -> None:
        """Test gRPC channel entity creation."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        tm.that(channel.target == "localhost:50051", eq=True)

    def test_grpc_stream_creation(self) -> None:
        """Test gRPC stream entity creation."""
        stream = FlextGrpcEntities.GrpcStream(
            unique_id="test_stream", method_name="test_method", stream_type="unary"
        )
        tm.that(stream.unique_id == "test_stream", eq=True)
        tm.that(stream.method_name == "test_method", eq=True)
        tm.that(stream.stream_type == "unary", eq=True)

    def test_service_creation_with_validation(self) -> None:
        """Test service creation with validation."""
        service = FlextGrpcEntities.Service(
            name="TestService", methods=["method1", "method2"]
        )
        tm.that(service.name == "TestService", eq=True)
        tm.that(service.methods == ["method1", "method2"], eq=True)

    def test_service_validation_empty_methods(self) -> None:
        """Test service validation fails with empty methods."""
        with pytest.raises(ValueError):
            FlextGrpcEntities.Service(name="TestService", methods=[])

    def test_service_validation_empty_name(self) -> None:
        """Test service validation fails with empty name."""
        with pytest.raises(ValueError):
            FlextGrpcEntities.Service(name="", methods=["method1"])

    def test_channel_business_rules(self) -> None:
        """Test channel business rules validation."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        result = channel.validate_business_rules()
        tm.that(result.is_success, eq=True)

    def test_channel_business_rules_empty_target(self) -> None:
        """Test channel business rules fail with empty target."""
        channel = FlextGrpcEntities.Channel(target="")
        result = channel.validate_business_rules()
        tm.that(result.is_failure, eq=True)
        tm.that(result.error and "cannot be empty" in result.error, eq=True)

    def test_channel_state_machine(self) -> None:
        """Test channel state machine transitions."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051", state="idle")
        result = channel.connect()
        tm.that(result.is_success, eq=True)
        connected_channel = result.value
        tm.that(connected_channel.state == "connecting", eq=True)

    def test_entity_copy_with(self) -> None:
        """Test entity copy_with method."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        result = channel.copy_with(target="127.0.0.1:8080")
        tm.that(result.is_success, eq=True)
        new_channel = result.value
        tm.that(new_channel.target == "127.0.0.1:8080", eq=True)

    def test_server_creation_defaults(self) -> None:
        """Test server creation with defaults."""
        server = FlextGrpcEntities.Server(host="localhost", port=50051)
        tm.that(server.host == "localhost", eq=True)
        tm.that(server.port == 50051, eq=True)
        tm.that(server.max_workers == 10, eq=True)

    def test_client_with_channel(self) -> None:
        """Test client creation with channel."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        client = FlextGrpcEntities.Client(channel=channel)
        tm.that(client.channel == channel, eq=True)
