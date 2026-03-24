"""Tests for flext_grpc.utilities module."""

from __future__ import annotations

from flext_tests import tm

from flext_grpc import FlextGrpcUtilities


class TestFlextGrpcUtilities:
    """Test cases for FlextGrpcUtilities class."""

    def test_init(self) -> None:
        """Test FlextGrpcUtilities initialization."""
        utilities = FlextGrpcUtilities()
        tm.that(utilities, none=False)

    def test_system_utilities(self) -> None:
        """Test system utilities."""
        utilities = FlextGrpcUtilities()
        tm.that(hasattr(utilities, "Grpc"), eq=True)

    def test_grpc_parse_address(self) -> None:
        """Test gRPC address parsing utility."""
        parsed = FlextGrpcUtilities.Grpc.parse_address("localhost:50051")
        assert parsed is not None
        host, port = parsed
        tm.that(host, eq="localhost")
        tm.that(port, eq=50051)

    def test_grpc_validate_port(self) -> None:
        """Test gRPC port validation utility."""
        tm.that(FlextGrpcUtilities.Grpc.validate_port(50051), eq=True)
        tm.that(FlextGrpcUtilities.Grpc.validate_port(0), eq=False)

    def test_create_client_entity(self) -> None:
        """Test client entity creation."""
        result = FlextGrpcUtilities.create_client_entity("localhost:50051")
        tm.that(result.is_success, eq=True)
        client = result.value
        assert client is not None
        assert client.channel is not None
        tm.that(client.channel.target, eq="localhost:50051")

    def test_create_server_entity(self) -> None:
        """Test server entity creation."""
        result = FlextGrpcUtilities.create_server_entity("localhost", 50051)
        tm.that(result.is_success, eq=True)
        server = result.value
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)

    def test_create_channel_entity(self) -> None:
        """Test channel entity creation."""
        result = FlextGrpcUtilities.create_channel_entity("localhost:50051")
        tm.that(result.is_success, eq=True)
        channel = result.value
        tm.that(channel.target, eq="localhost:50051")

    def test_create_service_entity(self) -> None:
        """Test service entity creation."""
        result = FlextGrpcUtilities.create_service_entity("TestService")
        tm.that(result.is_success, eq=True)
        service = result.value
        tm.that(service.name, eq="TestService")

    def test_create_stream_entity(self) -> None:
        """Test stream entity creation."""
        result = FlextGrpcUtilities.create_stream_entity("test_method", "unary")
        tm.that(result.is_success, eq=True)
        stream = result.value
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    def test_grpc_get_system_info(self) -> None:
        """Test system info retrieval."""
        info = FlextGrpcUtilities.Grpc.get_system_info()
        tm.that(isinstance(info, dict), eq=True)

    def test_grpc_format_address(self) -> None:
        """Test gRPC address formatting."""
        address = FlextGrpcUtilities.Grpc.format_address("localhost", 50051)
        tm.that(address, eq="localhost:50051")

    def test_grpc_validate_host(self) -> None:
        """Test gRPC host validation."""
        tm.that(FlextGrpcUtilities.Grpc.validate_host("localhost"), eq=True)
        tm.that(FlextGrpcUtilities.Grpc.validate_host(""), eq=False)

    def test_grpc_get_channel_state_name(self) -> None:
        """Test channel state name retrieval."""
        name = FlextGrpcUtilities.Grpc.get_channel_state_name("idle")
        tm.that(isinstance(name, str), eq=True)

    def test_grpc_get_server_state_name(self) -> None:
        """Test server state name retrieval."""
        name = FlextGrpcUtilities.Grpc.get_server_state_name("stopped")
        tm.that(isinstance(name, str), eq=True)
