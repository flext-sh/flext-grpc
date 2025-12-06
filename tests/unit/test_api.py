"""Tests for flext_grpc.api module."""

import pytest
from pydantic import BaseModel

from flext_grpc.api import (
    FlextGrpc,
    GenericOperationSpec,
    GenericRequest,
    GenericResponse,
)
from flext_grpc.config import FlextGrpcConfig


class TestFlextGrpc:
    """Test cases for FlextGrpc class."""

    def test_init(self) -> None:
        """Test FlextGrpc initialization."""
        grpc = FlextGrpc()
        assert grpc is not None

    def test_init_with_config(self) -> None:
        """Test FlextGrpc initialization with config."""
        config = FlextGrpcConfig()
        grpc = FlextGrpc()
        grpc._config = config  # Set config manually for test
        assert grpc.grpc_config == config

    def test_create_server(self) -> None:
        """Test server creation."""
        grpc = FlextGrpc()
        result = grpc.create_entity("server", host="localhost", port=50051)
        assert result.is_success
        server = result.unwrap()
        assert server.host == "localhost"
        assert server.port == 50051

    def test_create_client(self) -> None:
        """Test client creation."""
        grpc = FlextGrpc()
        result = grpc.create_entity("client", target="localhost:50051")
        assert result.is_success
        client = result.unwrap()
        assert client.channel is not None

    def test_create_stream(self) -> None:
        """Test stream creation."""
        grpc = FlextGrpc()
        result = grpc.create_entity(
            "stream",
            method_name="test_method",
            stream_type="unary",
        )
        assert result.is_success
        stream = result.unwrap()
        assert stream.method_name == "test_method"
        assert stream.stream_type == "unary"

    def test_validate_target(self) -> None:
        """Test target validation."""
        grpc = FlextGrpc()
        assert grpc.validate_target("localhost:50051")
        assert not grpc.validate_target("invalid")
        assert not grpc.validate_target("localhost:99999")

    def test_parse_address(self) -> None:
        """Test address parsing."""
        grpc = FlextGrpc()
        result = grpc.parse_address("localhost:50051")
        assert result.is_success
        host, port = result.unwrap()
        assert host == "localhost"
        assert port == 50051

    def test_create_channel(self) -> None:
        """Test channel creation."""
        grpc = FlextGrpc()
        result = grpc.create_channel(target="localhost:50051")
        assert result.is_success
        channel = result.unwrap()
        assert channel.target == "localhost:50051"
        assert channel.state == "idle"

    def test_create_service(self) -> None:
        """Test service creation."""
        grpc = FlextGrpc()
        result = grpc.create_service(name="TestService", methods=["method1", "method2"])
        assert result.is_success
        service = result.unwrap()
        assert service.name == "TestService"
        assert service.methods == ["method1", "method2"]

    def test_execute_method(self) -> None:
        """Test execute method."""
        grpc = FlextGrpc()
        result = grpc.execute()
        assert result.is_success
        config = result.unwrap()
        assert isinstance(config, FlextGrpcConfig)

    def test_create_server_direct(self) -> None:
        """Test direct server creation."""
        grpc = FlextGrpc()
        result = grpc.create_server(host="127.0.0.1", port=8080)
        assert result.is_success
        server = result.unwrap()
        assert server.host == "127.0.0.1"
        assert server.port == 8080

    def test_create_client_direct(self) -> None:
        """Test direct client creation."""
        grpc = FlextGrpc()
        result = grpc.create_client(target="127.0.0.1:8080")
        assert result.is_success
        client = result.unwrap()
        assert client.channel.target == "127.0.0.1:8080"

    def test_create_entity_invalid_type(self) -> None:
        """Test create_entity with invalid entity type."""
        grpc = FlextGrpc()
        result = grpc.create_entity("invalid_type")
        assert result.is_failure
        assert "Unknown entity type" in result.error

    def test_validate_target_invalid(self) -> None:
        """Test target validation with invalid targets."""
        grpc = FlextGrpc()
        assert not grpc.validate_target("")
        assert not grpc.validate_target("no_port")
        assert not grpc.validate_target("localhost")  # Missing port
        assert not grpc.validate_target(":50051")  # Missing host
        assert not grpc.validate_target("localhost:99999")  # Invalid port

    def test_parse_address_invalid(self) -> None:
        """Test address parsing with invalid addresses."""
        grpc = FlextGrpc()
        result = grpc.parse_address("invalid_address")
        assert result.is_failure
        assert "Invalid address" in result.error

    def test_create_channel_with_options(self) -> None:
        """Test channel creation with custom options."""
        grpc = FlextGrpc()
        options = {"timeout": 30, "compression": "gzip"}
        result = grpc.create_channel(target="localhost:50051", options=options)
        assert result.is_success
        channel = result.unwrap()
        assert channel.options == options

    def test_create_service_defaults(self) -> None:
        """Test service creation with defaults."""
        grpc = FlextGrpc()
        result = grpc.create_service()
        assert result.is_success
        service = result.unwrap()
        assert service.name == "DefaultService"
        assert service.methods == ["default_method"]

    def test_validate_entity_type(self) -> None:
        """Test entity type validation."""
        # Test valid entity types
        assert GenericOperationSpec.validate_entity_type("server") == "server"
        assert GenericOperationSpec.validate_entity_type("client") == "client"
        assert GenericOperationSpec.validate_entity_type("channel") == "channel"
        assert GenericOperationSpec.validate_entity_type("service") == "service"
        assert GenericOperationSpec.validate_entity_type("stream") == "stream"

        # Test invalid entity types
        with pytest.raises(ValueError, match="Unsupported entity type"):
            GenericOperationSpec.validate_entity_type("invalid")

    def test_generic_request_creation(self) -> None:
        """Test GenericRequest creation."""

        class TestData(BaseModel):
            value: str

        operation = GenericOperationSpec(name="test_operation", entity_type="server")
        request = GenericRequest[TestData](
            operation=operation,
            data=TestData(value="test"),
        )
        assert request.data.value == "test"
        assert request.operation.name == "test_operation"
        assert request.is_valid

    def test_generic_response_creation(self) -> None:
        """Test GenericResponse creation."""

        class TestData(BaseModel):
            result: str

        response = GenericResponse[TestData](
            success=True,
            data=TestData(result="success"),
        )
        assert response.data.result == "success"
        assert response.success is True
        assert not response.has_error
