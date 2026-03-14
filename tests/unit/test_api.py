"""Tests for flext_grpc.api module."""

import pytest
from pydantic import ValidationError

from flext_grpc import FlextGrpc, FlextGrpcModels, FlextGrpcSettings, t


class TestFlextGrpc:
    """Test cases for FlextGrpc class."""

    def test_init(self) -> None:
        """Test FlextGrpc initialization."""
        grpc = FlextGrpc()
        assert grpc is not None

    def test_init_with_config(self) -> None:
        """Test FlextGrpc initialization with config."""
        config = FlextGrpcSettings()
        grpc = FlextGrpc(config=config)
        assert grpc.grpc_config == config

    def test_create_server(self) -> None:
        """Test server creation."""
        grpc = FlextGrpc()
        result = grpc.create_server(host="localhost", port=50051)
        assert result.is_success
        server = result.value
        assert server.host == "localhost"
        assert server.port == 50051

    def test_create_client(self) -> None:
        """Test client creation."""
        grpc = FlextGrpc()
        result = grpc.create_client(target="localhost:50051")
        assert result.is_success
        client = result.value
        assert client.channel is not None

    def test_create_stream(self) -> None:
        """Test stream creation."""
        grpc = FlextGrpc()
        result = grpc.create_stream(method_name="test_method", stream_type="unary")
        assert result.is_success
        stream = result.value
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
        host, port = result.value
        assert host == "localhost"
        assert port == 50051

    def test_create_channel(self) -> None:
        """Test channel creation."""
        grpc = FlextGrpc()
        result = grpc.create_channel(target="localhost:50051")
        assert result.is_success
        channel = result.value
        assert channel.target == "localhost:50051"
        assert channel.state == "idle"

    def test_create_service(self) -> None:
        """Test service creation."""
        grpc = FlextGrpc()
        result = grpc.create_service(name="TestService", methods=["method1", "method2"])
        assert result.is_success
        service: FlextGrpcModels.Grpc.Service = result.value
        assert service.name == "TestService"
        assert service.methods == ["method1", "method2"]

    def test_execute_method(self) -> None:
        """Test execute method."""
        grpc = FlextGrpc()
        result = grpc.execute()
        assert result.is_success
        config = result.value
        assert isinstance(config, FlextGrpcSettings)

    def test_create_server_direct(self) -> None:
        """Test direct server creation."""
        grpc = FlextGrpc()
        result = grpc.create_server(host="127.0.0.1", port=8080)
        assert result.is_success
        server = result.value
        assert server.host == "127.0.0.1"
        assert server.port == 8080

    def test_create_client_direct(self) -> None:
        """Test direct client creation."""
        grpc = FlextGrpc()
        result = grpc.create_client(target="127.0.0.1:8080")
        assert result.is_success
        client = result.value
        assert client.channel is not None and client.channel.target == "127.0.0.1:8080"

    def test_validate_target_invalid(self) -> None:
        """Test target validation with invalid targets."""
        grpc = FlextGrpc()
        assert not grpc.validate_target("")
        assert not grpc.validate_target("no_port")
        assert not grpc.validate_target("localhost")
        assert not grpc.validate_target(":50051")
        assert not grpc.validate_target("localhost:99999")

    def test_parse_address_invalid(self) -> None:
        """Test address parsing with invalid addresses."""
        grpc = FlextGrpc()
        result = grpc.parse_address("invalid_address")
        assert result.is_failure
        assert result.error and "Invalid address" in result.error

    def test_create_channel_with_options(self) -> None:
        """Test channel creation with custom options."""
        grpc = FlextGrpc()
        options: t.GrpcOptions = {"timeout": 30, "compression": "gzip"}
        result = grpc.create_channel(target="localhost:50051", options=options)
        assert result.is_success
        channel = result.value
        assert channel.options == options

    def test_create_service_defaults(self) -> None:
        """Test service creation with defaults."""
        grpc = FlextGrpc()
        result = grpc.create_service(name="DefaultService", methods=["default_method"])
        assert result.is_success
        service: FlextGrpcModels.Grpc.Service = result.value
        assert service.name == "DefaultService"
        assert service.methods == ["default_method"]

    def test_validate_entity_type(self) -> None:
        """Test entity type validation via OperationSpec model."""
        server_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="server"
        )
        client_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="client"
        )
        channel_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="channel"
        )
        service_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="service"
        )
        stream_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="stream"
        )
        assert server_spec.entity_type == "server"
        assert client_spec.entity_type == "client"
        assert channel_spec.entity_type == "channel"
        assert service_spec.entity_type == "service"
        assert stream_spec.entity_type == "stream"
        with pytest.raises(ValidationError):
            FlextGrpcModels.Grpc.OperationSpec({
                "name": "op",
                "entity_type": "invalid",
            })

    def test_request_creation(self) -> None:
        operation = FlextGrpcModels.Grpc.OperationSpec(
            name="test_operation", entity_type="server"
        )
        request = FlextGrpcModels.Grpc.Request(
            operation=operation, data={"value": "test"}
        )
        assert request.data == {"value": "test"}
        assert request.operation.name == "test_operation"
        assert request.model_dump().get("is_valid") is True

    def test_response_creation(self) -> None:
        data = FlextGrpcModels.Grpc.StreamInfo(
            stream_id="stream-1", stream_type="unary", target="localhost:50051"
        )
        response = FlextGrpcModels.Grpc.Response(success=True, data=data)
        assert response.data == data
        assert response.success is True
        assert response.model_dump().get("has_error") is False
