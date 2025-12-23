"""Tests for flext_grpc.entities module."""

import pytest

from flext_grpc.constants import c
from flext_grpc.entities import FlextGrpcEntities


class TestFlextGrpcEntities:
    """Test cases for FlextGrpcEntities class."""

    def test_grpc_server_creation(self) -> None:
        """Test gRPC server entity creation."""
        server = FlextGrpcEntities.Server(host="localhost", port=50051, max_workers=10)
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 10

    def test_grpc_client_creation(self) -> None:
        """Test gRPC client entity creation."""
        client = FlextGrpcEntities.Client()
        # Note: target property was removed, access channel.target if needed
        assert client is not None

    def test_grpc_channel_creation(self) -> None:
        """Test gRPC channel entity creation."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        assert channel.target == "localhost:50051"

    def test_grpc_stream_creation(self) -> None:
        """Test gRPC stream entity creation."""
        stream = FlextGrpcEntities.GrpcStream(
            unique_id="test_stream",
            method_name="test_method",
            stream_type=c.Grpc.GrpcOperations.UNARY,
        )
        assert stream.unique_id == "test_stream"
        assert stream.method_name == "test_method"
        assert stream.stream_type == "unary"

    def test_service_creation_with_validation(self) -> None:
        """Test service creation with validation."""
        service = FlextGrpcEntities.Service(
            name="TestService",
            methods=["method1", "method2"],
        )
        assert service.name == "TestService"
        assert service.methods == ["method1", "method2"]

    def test_service_validation_empty_methods(self) -> None:
        """Test service validation fails with empty methods."""
        with pytest.raises(ValueError):  # Pydantic validation error
            FlextGrpcEntities.Service(name="TestService", methods=[])

    def test_service_validation_empty_name(self) -> None:
        """Test service validation fails with empty name."""
        with pytest.raises(ValueError):  # Pydantic validation error
            FlextGrpcEntities.Service(name="", methods=["method1"])

    def test_channel_business_rules(self) -> None:
        """Test channel business rules validation."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        result = channel.validate_business_rules()
        assert result.is_success

    def test_channel_business_rules_empty_target(self) -> None:
        """Test channel business rules fail with empty target."""
        channel = FlextGrpcEntities.Channel(target="")
        result = channel.validate_business_rules()
        assert result.is_failure
        assert "cannot be empty" in result.error

    def test_channel_state_machine(self) -> None:
        """Test channel state machine transitions."""
        channel = FlextGrpcEntities.Channel(
            target="localhost:50051", state=c.Grpc.ChannelState.IDLE
        )
        result = channel.connect()
        assert result.is_success
        connected_channel = result.value
        assert connected_channel.state == "connecting"

    def test_entity_copy_with(self) -> None:
        """Test entity copy_with method."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        result = channel.copy_with(target="127.0.0.1:8080")
        assert result.is_success
        new_channel = result.value
        assert new_channel.target == "127.0.0.1:8080"

    def test_server_creation_defaults(self) -> None:
        """Test server creation with defaults."""
        server = FlextGrpcEntities.Server(host="localhost", port=50051)
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 10  # default

    def test_client_with_channel(self) -> None:
        """Test client creation with channel."""
        channel = FlextGrpcEntities.Channel(target="localhost:50051")
        client = FlextGrpcEntities.Client(channel=channel)
        assert client.channel == channel
