"""Tests for flext_grpc.api module."""

from flext_grpc.api import FlextGrpc
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
        grpc = FlextGrpc(config)
        assert grpc is not None

    def test_create_server(self) -> None:
        """Test server creation."""
        grpc = FlextGrpc()
        result = grpc.create_server()
        assert result.is_success

    def test_create_client(self) -> None:
        """Test client creation."""
        grpc = FlextGrpc()
        result = grpc.create_client()
        assert result.is_success

    def test_create_stream(self) -> None:
        """Test stream creation."""
        grpc = FlextGrpc()
        result = grpc.create_stream("test_method", "unary")
        assert result.is_success

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
