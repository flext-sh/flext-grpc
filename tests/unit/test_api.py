"""Tests for flext_grpc.api module."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest
from flext_tests import tm
from pydantic import ValidationError

from flext_grpc import FlextGrpc, FlextGrpcModels, FlextGrpcSettings, t


class TestFlextGrpc:
    """Test cases for FlextGrpc class."""

    def test_init(self) -> None:
        """Test FlextGrpc initialization."""
        grpc = FlextGrpc()
        tm.that(grpc, none=False)

    def test_init_with_config(self) -> None:
        """Test FlextGrpc initialization with config."""
        config = FlextGrpcSettings.model_validate({})
        grpc = FlextGrpc(config=config)
        tm.that(grpc.grpc_config, eq=config)

    def test_create_server(self) -> None:
        """Test server creation."""
        grpc = FlextGrpc()
        result = grpc.create_server(host="localhost", port=50051)
        tm.that(result.is_success, eq=True)
        server = result.value
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)

    def test_create_client(self) -> None:
        """Test client creation."""
        grpc = FlextGrpc()
        result = grpc.create_client(target="localhost:50051")
        tm.that(result.is_success, eq=True)
        client = result.value
        tm.that(client.channel, none=False)

    def test_create_stream(self) -> None:
        """Test stream creation."""
        grpc = FlextGrpc()
        result = grpc.create_stream(method_name="test_method", stream_type="unary")
        tm.that(result.is_success, eq=True)
        stream = result.value
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    def test_validate_target(self) -> None:
        """Test target validation."""
        grpc = FlextGrpc()
        tm.that(grpc.validate_target("localhost:50051"), eq=True)
        tm.that(not grpc.validate_target("invalid"), eq=True)
        tm.that(not grpc.validate_target("localhost:99999"), eq=True)

    def test_parse_address(self) -> None:
        """Test address parsing."""
        grpc = FlextGrpc()
        result = grpc.parse_address("localhost:50051")
        tm.that(result.is_success, eq=True)
        host, port = result.value
        tm.that(host, eq="localhost")
        tm.that(port, eq=50051)

    def test_create_channel(self) -> None:
        """Test channel creation."""
        grpc = FlextGrpc()
        result = grpc.create_channel(target="localhost:50051")
        tm.that(result.is_success, eq=True)
        channel = result.value
        tm.that(channel.target, eq="localhost:50051")
        tm.that(channel.state, eq="idle")

    def test_create_service(self) -> None:
        """Test service creation."""
        grpc = FlextGrpc()
        result = grpc.create_service(name="TestService", methods=["method1", "method2"])
        tm.that(result.is_success, eq=True)
        service: FlextGrpcModels.Grpc.Service = result.value
        tm.that(service.name, eq="TestService")
        tm.that(service.methods, eq=["method1", "method2"])

    def test_execute_method(self) -> None:
        """Test execute method."""
        grpc = FlextGrpc()
        result = grpc.execute()
        tm.that(result.is_success, eq=True)
        config = result.value
        tm.that(config, is_=FlextGrpcSettings)

    def test_create_server_direct(self) -> None:
        """Test direct server creation."""
        grpc = FlextGrpc()
        result = grpc.create_server(host="127.0.0.1", port=8080)
        tm.that(result.is_success, eq=True)
        server = result.value
        tm.that(server.host, eq="127.0.0.1")
        tm.that(server.port, eq=8080)

    def test_create_client_direct(self) -> None:
        """Test direct client creation."""
        grpc = FlextGrpc()
        result = grpc.create_client(target="127.0.0.1:8080")
        tm.that(result.is_success, eq=True)
        client = result.value
        tm.that(
            client.channel is not None and client.channel.target == "127.0.0.1:8080",
            eq=True,
        )

    def test_validate_target_invalid(self) -> None:
        """Test target validation with invalid targets."""
        grpc = FlextGrpc()
        tm.that(not grpc.validate_target(""), eq=True)
        tm.that(not grpc.validate_target("no_port"), eq=True)
        tm.that(not grpc.validate_target("localhost"), eq=True)
        tm.that(not grpc.validate_target(":50051"), eq=True)
        tm.that(not grpc.validate_target("localhost:99999"), eq=True)

    def test_parse_address_invalid(self) -> None:
        """Test address parsing with invalid addresses."""
        grpc = FlextGrpc()
        result = grpc.parse_address("invalid_address")
        tm.that(result.is_failure, eq=True)
        tm.that(result.error and "Invalid address" in result.error, eq=True)

    def test_create_channel_with_options(self) -> None:
        """Test channel creation with custom options."""
        grpc = FlextGrpc()
        options: t.GrpcOptions = {"timeout": 30, "compression": "gzip"}
        result = grpc.create_channel(target="localhost:50051", options=options)
        tm.that(result.is_success, eq=True)
        channel = result.value
        tm.that(channel.options, eq=options)

    def test_create_service_defaults(self) -> None:
        """Test service creation with defaults."""
        grpc = FlextGrpc()
        result = grpc.create_service(name="DefaultService", methods=["default_method"])
        tm.that(result.is_success, eq=True)
        service: FlextGrpcModels.Grpc.Service = result.value
        tm.that(service.name, eq="DefaultService")
        tm.that(service.methods, eq=["default_method"])

    def test_validate_entity_type(self) -> None:
        """Test entity type validation via OperationSpec model."""
        server_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="server", method_name=None, parameters={}
        )
        client_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="client", method_name=None, parameters={}
        )
        channel_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="channel", method_name=None, parameters={}
        )
        service_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="service", method_name=None, parameters={}
        )
        stream_spec = FlextGrpcModels.Grpc.OperationSpec(
            name="op", entity_type="stream", method_name=None, parameters={}
        )
        tm.that(server_spec.entity_type, eq="server")
        tm.that(client_spec.entity_type, eq="client")
        tm.that(channel_spec.entity_type, eq="channel")
        tm.that(service_spec.entity_type, eq="service")
        tm.that(stream_spec.entity_type, eq="stream")
        with pytest.raises(ValidationError):
            FlextGrpcModels.Grpc.OperationSpec.model_validate({
                "name": "op",
                "entity_type": "invalid",
            })

    def test_request_creation(self) -> None:
        operation = FlextGrpcModels.Grpc.OperationSpec(
            name="test_operation",
            entity_type="server",
            method_name=None,
            parameters={},
        )
        request = FlextGrpcModels.Grpc.Request(
            operation=operation,
            entity=None,
            data={"value": "test"},
        )
        tm.that(request.data, eq={"value": "test"})
        tm.that(request.operation.name, eq="test_operation")
        tm.that(request.model_dump().get("is_valid") is True, eq=True)

    def test_response_creation(self) -> None:
        data = FlextGrpcModels.Grpc.StreamInfo(
            stream_id="stream-1",
            stream_type="unary",
            target="localhost:50051",
            created_at=datetime.now(UTC),
            total_requests_sent=0,
            average_latency_ms=0.0,
            error_count=0,
        )
        response = FlextGrpcModels.Grpc.Response(
            success=True,
            data=data,
            error=None,
            metadata={},
        )
        tm.that(response.data, eq=data)
        tm.that(response.success is True, eq=True)
        tm.that(response.model_dump().get("has_error") is False, eq=True)
