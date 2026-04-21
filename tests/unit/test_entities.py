"""Tests for flext_grpc.entities module."""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c, m


class TestFlextGrpcEntities:
    """Test cases for FlextGrpcEntities class."""

    def test_grpc_server_creation(self) -> None:
        """Test gRPC server entity creation."""
        server = m.Grpc.Server(
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            domain_events=[],
        )
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)
        tm.that(server.max_workers, eq=10)

    def test_grpc_client_creation(self) -> None:
        """Test gRPC client entity creation."""
        client = m.Grpc.Client(options={}, domain_events=[])
        tm.that(client, none=False)

    def test_grpc_channel_creation(self) -> None:
        """Test gRPC channel entity creation."""
        channel = m.Grpc.Channel(
            target="localhost:50051",
            options={},
            domain_events=[],
        )
        tm.that(channel.target, eq="localhost:50051")

    def test_grpc_stream_creation(self) -> None:
        """Test gRPC stream entity creation."""
        stream = m.Grpc.GrpcStream(
            unique_id="test_stream",
            method_name="test_method",
            stream_type=c.Grpc.GrpcOperations.UNARY,
            domain_events=[],
        )
        tm.that(stream.unique_id, eq="test_stream")
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    def test_service_creation_with_validation(self) -> None:
        """Test service creation with validation."""
        service = m.Grpc.Service(
            name="TestService",
            methods=["method1", "method2"],
            domain_events=[],
        )
        tm.that(service.name, eq="TestService")
        tm.that(service.methods, eq=["method1", "method2"])

    def test_service_validation_empty_methods(self) -> None:
        """Test service validation fails with empty methods."""
        with pytest.raises(ValueError):
            m.Grpc.Service(name="TestService", methods=[], domain_events=[])

    def test_service_validation_empty_name(self) -> None:
        """Test service validation fails with empty name."""
        with pytest.raises(ValueError):
            m.Grpc.Service(name="", methods=["method1"], domain_events=[])

    def test_channel_business_rules(self) -> None:
        """Test channel business rules validation."""
        channel = m.Grpc.Channel(
            target="localhost:50051",
            options={},
            domain_events=[],
        )
        result = channel.validate_business_rules()
        tm.that(result.success, eq=True)

    def test_channel_business_rules_empty_target(self) -> None:
        """Test channel business rules fail with empty target."""
        channel = m.Grpc.Channel(target="", options={}, domain_events=[])
        result = channel.validate_business_rules()
        tm.that(result.failure, eq=True)
        tm.that(result.error and "cannot be empty" in result.error, eq=True)

    def test_channel_state_machine(self) -> None:
        """Test channel state machine transitions."""
        channel = m.Grpc.Channel(
            target="localhost:50051",
            state=c.Grpc.ChannelState.IDLE,
            options={},
            domain_events=[],
        )
        result = channel.connect()
        tm.that(result.success, eq=True)
        connected_channel = result.value
        tm.that(connected_channel.state, eq="connecting")

    def test_entity_copy_with(self) -> None:
        """Test entity copy_with method."""
        channel = m.Grpc.Channel(
            target="localhost:50051",
            options={},
            domain_events=[],
        )
        result = channel.copy_with(target="127.0.0.1:8080")
        tm.that(result.success, eq=True)
        new_channel = result.value
        tm.that(new_channel.target, eq="127.0.0.1:8080")

    def test_server_creation_defaults(self) -> None:
        """Test server creation with defaults."""
        server = m.Grpc.Server(
            host="localhost",
            port=50051,
            services=[],
            domain_events=[],
        )
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)
        tm.that(server.max_workers, eq=10)

    def test_client_with_channel(self) -> None:
        """Test client creation with channel."""
        channel = m.Grpc.Channel(
            target="localhost:50051",
            options={},
            domain_events=[],
        )
        client = m.Grpc.Client(channel=channel, options={}, domain_events=[])
        assert client.channel == channel
