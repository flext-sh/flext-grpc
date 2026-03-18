"""Tests for flext_grpc.utilities module."""

from __future__ import annotations

from flext_tests import tm

from flext_grpc import FlextGrpcUtilities


class TestFlextGrpcUtilities:
    """Test cases for FlextGrpcUtilities class."""

    def test_init(self) -> None:
        """Test FlextGrpcUtilities initialization."""
        utilities = FlextGrpcUtilities()
        tm.that(utilities is not None, eq=True)

    def test_system_utilities(self) -> None:
        """Test system utilities."""
        utilities = FlextGrpcUtilities()
        tm.that(hasattr(utilities, "Grpc"), eq=True)

    def test_grpc_parse_address(self) -> None:
        """Test gRPC address parsing utility."""
        parsed = FlextGrpcUtilities.Grpc.parse_address("localhost:50051")
        tm.that(parsed is not None, eq=True)
        host, port = parsed
        tm.that(host == "localhost", eq=True)
        tm.that(port == 50051, eq=True)

    def test_grpc_validate_port(self) -> None:
        """Test gRPC port validation utility."""
        tm.that(FlextGrpcUtilities.Grpc.validate_port(50051), eq=True)
        tm.that(not FlextGrpcUtilities.Grpc.validate_port(0), eq=True)

    def test_create_client_entity(self) -> None:
        """Test client entity creation."""
        result = FlextGrpcUtilities.create_client_entity("localhost:50051")
        tm.that(result.is_success, eq=True)
        client = result.value
        tm.that(client is not None, eq=True)
        tm.that(client.channel is not None, eq=True)
        tm.that(client.channel.target == "localhost:50051", eq=True)

    def test_create_server_entity(self) -> None:
        """Test server entity creation."""
        result = FlextGrpcUtilities.create_server_entity("localhost", 50051)
        tm.that(result.is_success, eq=True)
        server = result.value
        tm.that(server.host == "localhost", eq=True)
        tm.that(server.port == 50051, eq=True)

    def test_create_channel_entity(self) -> None:
        """Test channel entity creation."""
        result = FlextGrpcUtilities.create_channel_entity("localhost:50051")
        tm.that(result.is_success, eq=True)
        channel = result.value
        tm.that(channel.target == "localhost:50051", eq=True)

    def test_create_service_entity(self) -> None:
        """Test service entity creation."""
        result = FlextGrpcUtilities.create_service_entity("TestService")
        tm.that(result.is_success, eq=True)
        service = result.value
        tm.that(service.name == "TestService", eq=True)

    def test_create_stream_entity(self) -> None:
        """Test stream entity creation."""
        result = FlextGrpcUtilities.create_stream_entity("test_method", "unary")
        tm.that(result.is_success, eq=True)
        stream = result.value
        tm.that(stream.method_name == "test_method", eq=True)
        tm.that(stream.stream_type == "unary", eq=True)

    def test_grpc_get_system_info(self) -> None:
        """Test system info retrieval."""
        info = FlextGrpcUtilities.Grpc.get_system_info()
        tm.that(isinstance(info, dict), eq=True)

    def test_grpc_format_address(self) -> None:
        """Test gRPC address formatting."""
        address = FlextGrpcUtilities.Grpc.format_address("localhost", 50051)
        tm.that(address == "localhost:50051", eq=True)

    def test_grpc_validate_host(self) -> None:
        """Test gRPC host validation."""
        tm.that(FlextGrpcUtilities.Grpc.validate_host("localhost"), eq=True)
        tm.that(not FlextGrpcUtilities.Grpc.validate_host(""), eq=True)

    def test_grpc_get_channel_state_name(self) -> None:
        """Test channel state name retrieval."""
        name = FlextGrpcUtilities.Grpc.get_channel_state_name("idle")
        tm.that(isinstance(name, str), eq=True)

    def test_grpc_get_server_state_name(self) -> None:
        """Test server state name retrieval."""
        name = FlextGrpcUtilities.Grpc.get_server_state_name("stopped")
        tm.that(isinstance(name, str), eq=True)
