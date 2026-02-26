"""Tests for flext_grpc.utilities module."""

from google.protobuf.message import Message

from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilities:
    """Test cases for FlextGrpcUtilities class."""

    def test_init(self) -> None:
        """Test FlextGrpcUtilities initialization."""
        utilities = FlextGrpcUtilities()
        assert utilities is not None

    def test_system_utilities(self) -> None:
        """Test system utilities."""
        utilities = FlextGrpcUtilities()
        assert hasattr(utilities, "Grpc")

    def test_grpc_parse_address(self) -> None:
        """Test gRPC address parsing utility."""
        host, port = FlextGrpcUtilities.Grpc.parse_address("localhost:50051")
        assert host == "localhost"
        assert port == 50051

    def test_grpc_validate_port(self) -> None:
        """Test gRPC port validation utility."""
        assert FlextGrpcUtilities.Grpc.validate_port(50051)
        assert not FlextGrpcUtilities.Grpc.validate_port(0)

    def test_create_client_entity(self) -> None:
        """Test client entity creation."""
        result = FlextGrpcUtilities.create_client_entity("localhost:50051")
        assert result.is_success
        client = result.value
        assert client is not None
        assert client.channel is not None
        assert client.channel.target == "localhost:50051"

    def test_create_server_entity(self) -> None:
        """Test server entity creation."""
        result = FlextGrpcUtilities.create_server_entity("localhost", 50051)
        assert result.is_success
        server = result.value
        assert server.host == "localhost"
        assert server.port == 50051

    def test_create_channel_entity(self) -> None:
        """Test channel entity creation."""
        result = FlextGrpcUtilities.create_channel_entity("localhost:50051")
        assert result.is_success
        channel = result.value
        assert channel.target == "localhost:50051"

    def test_create_service_entity(self) -> None:
        """Test service entity creation."""
        result = FlextGrpcUtilities.create_service_entity("TestService")
        assert result.is_success
        service = result.value
        assert service.name == "TestService"

    def test_create_stream_entity(self) -> None:
        """Test stream entity creation."""
        result = FlextGrpcUtilities.create_stream_entity("test_method", "unary")
        assert result.is_success
        stream = result.value
        assert stream.method_name == "test_method"
        assert stream.stream_type == "unary"

    def test_grpc_get_system_info(self) -> None:
        """Test system info retrieval."""
        info = FlextGrpcUtilities.Grpc.get_system_info()
        assert isinstance(info, dict)

    def test_grpc_format_address(self) -> None:
        """Test gRPC address formatting."""
        address = FlextGrpcUtilities.Grpc.format_address("localhost", 50051)
        assert address == "localhost:50051"

    def test_grpc_validate_host(self) -> None:
        """Test gRPC host validation."""
        assert FlextGrpcUtilities.Grpc.validate_host("localhost")
        assert not FlextGrpcUtilities.Grpc.validate_host("")

    def test_grpc_get_channel_state_name(self) -> None:
        """Test channel state name retrieval."""
        name = FlextGrpcUtilities.Grpc.get_channel_state_name("idle")
        assert isinstance(name, str)

    def test_grpc_get_server_state_name(self) -> None:
        """Test server state name retrieval."""
        name = FlextGrpcUtilities.Grpc.get_server_state_name("stopped")
        assert isinstance(name, str)
