"""Tests for flext_grpc.api module."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from flext_tests import tm
from pydantic import ValidationError

from flext_grpc import FlextGrpc, FlextGrpcSettings
from tests import m

if TYPE_CHECKING:
    from tests import t


class TestsFlextGrpcApi:
    """Test cases for FlextGrpc class."""

    def test_init(self) -> None:
        """Test FlextGrpc initialization."""
        tm.that(FlextGrpc(), none=False)

    def test_init_with_config(self) -> None:
        """Test FlextGrpc initialization with settings."""
        tm.that(FlextGrpc().grpc_config, is_=FlextGrpcSettings)
        tm.that(
            FlextGrpcSettings.model_validate({}),
            eq=FlextGrpcSettings.model_validate({}),
        )

    @pytest.mark.parametrize(
        ("host", "port"),
        [("localhost", 50051), ("127.0.0.1", 8080)],
    )
    def test_create_server(self, host: str, port: int) -> None:
        """Test server creation across canonical address shapes."""
        server: m.Grpc.Server = tm.ok(
            FlextGrpc().create_server(host=host, port=port),
        )
        tm.that(server.host, eq=host)
        tm.that(server.port, eq=port)

    @pytest.mark.parametrize("target", ["localhost:50051", "127.0.0.1:8080"])
    def test_create_client(self, target: str) -> None:
        """Test client creation across canonical address shapes."""
        client: m.Grpc.Client = tm.ok(FlextGrpc().create_client(target=target))
        assert client.channel is not None
        tm.that(client.channel.target, eq=target)

    def test_create_stream(self) -> None:
        """Test stream creation."""
        stream: m.Grpc.GrpcStream = tm.ok(
            FlextGrpc().create_stream(method_name="test_method", stream_type="unary"),
        )
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    @pytest.mark.parametrize(
        "target",
        ["localhost:50051"],
        ids=["valid"],
    )
    def test_validate_target_valid(self, target: str) -> None:
        """Valid targets pass validation."""
        tm.that(FlextGrpc().validate_target(target), eq=True)

    @pytest.mark.parametrize(
        "target",
        ["", "no_port", "localhost", ":50051", "localhost:99999", "invalid"],
    )
    def test_validate_target_invalid(self, target: str) -> None:
        """Invalid targets fail validation."""
        tm.that(FlextGrpc().validate_target(target), eq=False)

    def test_parse_address(self) -> None:
        """Test address parsing."""
        parsed: tuple[str, int] = tm.ok(FlextGrpc().parse_address("localhost:50051"))
        host, port = parsed
        tm.that(host, eq="localhost")
        tm.that(port, eq=50051)

    def test_parse_address_invalid(self) -> None:
        """Test address parsing with invalid addresses."""
        tm.fail(FlextGrpc().parse_address("invalid_address"), has="Invalid address")

    def test_create_channel(self) -> None:
        """Test channel creation."""
        channel: m.Grpc.Channel = tm.ok(
            FlextGrpc().create_channel(target="localhost:50051"),
        )
        tm.that(channel.target, eq="localhost:50051")
        tm.that(channel.state, eq="idle")

    def test_create_channel_with_options(self) -> None:
        """Test channel creation with custom options."""
        options: t.JsonMapping | None = {"timeout": 30, "compression": "gzip"}
        channel: m.Grpc.Channel = tm.ok(
            FlextGrpc().create_channel(target="localhost:50051", options=options),
        )
        tm.that(channel.options, eq=options)

    @pytest.mark.parametrize(
        "name",
        ["TestService", "DefaultService"],
    )
    def test_create_service(self, name: str) -> None:
        """Test service creation across method shapes."""
        methods = (
            ["method1", "method2"] if name == "TestService" else ["default_method"]
        )
        service: m.Grpc.Service = tm.ok(
            FlextGrpc().create_service(name=name, methods=methods),
        )
        tm.that(service.name, eq=name)
        tm.that(service.methods, eq=methods)

    def test_execute_method(self) -> None:
        """Test execute method."""
        tm.ok(FlextGrpc().execute(), is_=FlextGrpcSettings)

    @pytest.mark.parametrize(
        "entity_type",
        ["server", "client", "channel", "service", "stream"],
    )
    def test_validate_entity_type_accepts(self, entity_type: t.Grpc.EntityKind) -> None:
        """OperationSpec accepts every canonical entity_type literal."""
        spec = m.Grpc.OperationSpec(
            name="op",
            entity_type=entity_type,
            method_name=None,
            parameters={},
        )
        tm.that(spec.entity_type, eq=entity_type)

    def test_validate_entity_type_rejects_invalid(self) -> None:
        """OperationSpec rejects unknown entity_type values."""
        with pytest.raises(ValidationError):
            m.Grpc.OperationSpec.model_validate({
                "name": "op",
                "entity_type": "invalid",
            })

    def test_request_creation(self) -> None:
        operation = m.Grpc.OperationSpec(
            name="test_operation",
            entity_type="server",
            method_name=None,
            parameters={},
        )
        request = m.Grpc.Request(
            operation=operation,
            entity=None,
            data={"value": "test"},
        )
        tm.that(request.data, eq={"value": "test"})
        tm.that(request.operation.name, eq="test_operation")
        tm.that(request.model_dump().get("valid"), eq=True)

    def test_response_creation(self) -> None:
        data = m.Grpc.StreamInfo(
            stream_id="stream-1",
            stream_type="unary",
            target="localhost:50051",
            created_at=datetime.now(UTC),
            total_requests_sent=0,
            average_latency_ms=0.0,
            error_count=0,
        )
        response = m.Grpc.Response(
            success=True,
            data=data,
            error=None,
            metadata={},
        )
        tm.that(response.data, eq=data)
        tm.that(response.success, eq=True)
        tm.that(response.model_dump().get("has_error"), eq=False)
