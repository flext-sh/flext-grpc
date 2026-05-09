"""Tests for flext_grpc.utilities module."""

from __future__ import annotations

from flext_tests import tm

from tests import u


class TestsFlextGrpcUtilitiesUnit:
    """Test cases for u class."""

    def test_init(self) -> None:
        """Test u initialization."""
        tm.that(u(), none=False)

    def test_grpc_parse_address(self) -> None:
        """Test gRPC address parsing utility."""
        parsed = u.Grpc.parse_address("localhost:50051")
        tm.that(parsed, none=False)
        host, port = parsed
        tm.that(host, eq="localhost")
        tm.that(port, eq=50051)

    def test_grpc_validate_port(self) -> None:
        """Test gRPC port validation utility."""
        tm.that(u.Grpc.validate_port(50051), eq=True)
        tm.that(u.Grpc.validate_port(0), eq=False)

    def test_create_client_entity(self) -> None:
        """Test client entity creation."""
        client = tm.ok(u.Grpc.create_client_entity("localhost:50051"))
        assert client.channel is not None
        tm.that(client.channel.target, eq="localhost:50051")

    def test_create_server_entity(self) -> None:
        """Test server entity creation."""
        server = tm.ok(u.Grpc.create_server_entity("localhost", 50051))
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)

    def test_create_channel_entity(self) -> None:
        """Test channel entity creation."""
        channel = tm.ok(u.Grpc.create_channel_entity("localhost:50051"))
        tm.that(channel.target, eq="localhost:50051")

    def test_create_service_entity(self) -> None:
        """Test service entity creation."""
        service = tm.ok(u.Grpc.create_service_entity("TestService"))
        tm.that(service.name, eq="TestService")

    def test_create_stream_entity(self) -> None:
        """Test stream entity creation."""
        stream = tm.ok(u.Grpc.create_stream_entity("test_method", "unary"))
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    def test_grpc_get_system_info(self) -> None:
        """Test system info retrieval."""
        tm.that(u.Grpc.system_info(), is_=dict)

    def test_grpc_format_address(self) -> None:
        """Test gRPC address formatting."""
        tm.that(u.Grpc.format_address("localhost", 50051), eq="localhost:50051")

    def test_grpc_validate_host(self) -> None:
        """Test gRPC host validation."""
        tm.that(u.Grpc.validate_host("localhost"), eq=True)
        tm.that(u.Grpc.validate_host(""), eq=False)

    def test_grpc_get_channel_state_name(self) -> None:
        """Test channel state name retrieval."""
        tm.that(u.Grpc.channel_state_name("idle"), is_=str)

    def test_grpc_get_server_state_name(self) -> None:
        """Test server state name retrieval."""
        tm.that(u.Grpc.server_state_name("stopped"), is_=str)
