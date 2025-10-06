"""Tests for flext_grpc.services module."""

from flext_grpc.services import FlextGrpcServices


class TestFlextGrpcServices:
    """Test cases for FlextGrpcServices class."""

    def test_init(self) -> None:
        """Test FlextGrpcServices initialization."""
        services = FlextGrpcServices()
        assert services is not None

    def test_create_server(self) -> None:
        """Test server creation."""
        services = FlextGrpcServices()
        result = services.create_server()
        assert result.is_success

    def test_create_client(self) -> None:
        """Test client creation."""
        services = FlextGrpcServices()
        result = services.create_client()
        assert result.is_success

    def test_create_stream(self) -> None:
        """Test stream creation."""
        services = FlextGrpcServices()
        result = services.create_stream("unary", "test_method")
        assert result.is_success
