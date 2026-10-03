"""Tests for flext_grpc.api module.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_grpc import FlextGrpc, FlextGrpcSettings
from tests import m

if TYPE_CHECKING:
    from tests import t


class TestsFlextGrpcApi:
    """Test cases for FlextGrpc class."""

    @staticmethod
    def test_init() -> None:
        """Test FlextGrpc initialization."""
        tm.that(FlextGrpc(), none=False)

    @staticmethod
    def test_init_with_config() -> None:
        """Test FlextGrpc initialization with settings."""
        tm.that(FlextGrpc().grpc_config, is_=FlextGrpcSettings)
        tm.that(
            FlextGrpcSettings.model_validate({}),
            eq=FlextGrpcSettings.model_validate({}),
        )

    @staticmethod
    @pytest.mark.parametrize(
        ("host", "port"), [("localhost", 50051), ("127.0.0.1", 8080)],
    )
    def test_create_server(host: str, port: int) -> None:
        """Test server creation across canonical address shapes."""
        server: m.Grpc.Server = tm.ok(FlextGrpc().create_server(host=host, port=port))
        tm.that(server.host, eq=host)
        tm.that(server.port, eq=port)

    @staticmethod
    @pytest.mark.parametrize("target", ["localhost:50051", "127.0.0.1:8080"])
    def test_create_client(target: str) -> None:
        """Test client creation across canonical address shapes."""
        client: m.Grpc.Client = tm.ok(FlextGrpc().create_client(target=target))
        channel = tm.not_none(client.channel)
        tm.that(channel.target, eq=target)

    @staticmethod
    def test_create_stream() -> None:
        """Test stream creation."""
        stream: m.Grpc.GrpcStream = tm.ok(
            FlextGrpc().create_stream(method_name="test_method", stream_type="unary"),
        )
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    @staticmethod
    @pytest.mark.parametrize("target", ["localhost:50051"], ids=["valid"])
    def test_validate_target_valid(target: str) -> None:
        """Valid targets pass validation."""
        tm.that(FlextGrpc().validate_target(target), eq=True)

    @staticmethod
    @pytest.mark.parametrize(
        "target", ["", "no_port", "localhost", ":50051", "localhost:99999", "invalid"],
    )
    def test_validate_target_invalid(target: str) -> None:
        """Invalid targets fail validation."""
        tm.that(FlextGrpc().validate_target(target), eq=False)

    @staticmethod
    def test_parse_address() -> None:
        """Test address parsing."""
        parsed: tuple[str, int] = tm.ok(FlextGrpc().parse_address("localhost:50051"))
        host, port = parsed
        tm.that(host, eq="localhost")
        tm.that(port, eq=50051)

    @staticmethod
    def test_parse_address_invalid() -> None:
        """Test address parsing with invalid addresses."""
        tm.fail(FlextGrpc().parse_address("invalid_address"), has="Invalid address")

    @staticmethod
    def test_create_channel() -> None:
        """Test channel creation."""
        channel: m.Grpc.Channel = tm.ok(
            FlextGrpc().create_channel(target="localhost:50051"),
        )
        tm.that(channel.target, eq="localhost:50051")
        tm.that(channel.state, eq="idle")

    @staticmethod
    def test_create_channel_with_options() -> None:
        """Test channel creation with custom options."""
        options: t.JsonMapping | None = {"timeout": 30, "compression": "gzip"}
        channel: m.Grpc.Channel = tm.ok(
            FlextGrpc().create_channel(target="localhost:50051", options=options),
        )
        tm.that(channel.options, eq=options)

    @staticmethod
    @pytest.mark.parametrize("name", ["TestService", "DefaultService"])
    def test_create_service(name: str) -> None:
        """Test service creation across method shapes."""
        methods = (
            ["method1", "method2"] if name == "TestService" else ["default_method"]
        )
        service: m.Grpc.Service = tm.ok(
            FlextGrpc().create_service(name=name, methods=methods),
        )
        tm.that(service.name, eq=name)
        tm.that(service.methods, eq=methods)

    @staticmethod
    def test_execute_method() -> None:
        """Test execute method."""
        tm.ok(FlextGrpc().execute(), is_=FlextGrpcSettings)

    @staticmethod
    @pytest.mark.parametrize(
        "entity_type", ["server", "client", "channel", "service", "stream"],
    )
    def test_validate_entity_type_accepts(entity_type: t.Grpc.EntityKind) -> None:
        """OperationSpec accepts every canonical entity_type literal."""
        spec = m.Grpc.OperationSpec(
            name="op", entity_type=entity_type, method_name=None, parameters={},
        )
        tm.that(spec.entity_type, eq=entity_type)

    @staticmethod
    def test_validate_entity_type_rejects_invalid() -> None:
        """OperationSpec rejects unknown entity_type values."""
        with pytest.raises(m.ValidationError):
            m.Grpc.OperationSpec.model_validate({
                "name": "op",
                "entity_type": "invalid",
            })

    @staticmethod
    def test_request_creation() -> None:
        """Test request creation."""
        operation = m.Grpc.OperationSpec(
            name="test_operation", entity_type="server",
            method_name=None, parameters={},
        )
        request = m.Grpc.Request(
            operation=operation, entity=None, data={"value": "test"},
        )
        tm.that(request.data, eq={"value": "test"})
        tm.that(request.operation.name, eq="test_operation")
        tm.that(request.model_dump().get("valid"), eq=True)

    @staticmethod
    def test_response_creation() -> None:
        """Test response creation."""
        data = m.Grpc.StreamInfo(
            stream_id="stream-1",
            stream_type="unary",
            target="localhost:50051",
            created_at=datetime.now(UTC),
            total_requests_sent=0,
            average_latency_ms=0.0,
            error_count=0,
        )
        response = m.Grpc.Response(success=True, data=data, error=None, metadata={})
        tm.that(response.data, eq=data)
        tm.that(response.success, eq=True)
        tm.that(response.model_dump().get("has_error"), eq=False)
