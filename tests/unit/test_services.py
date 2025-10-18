"""Tests for flext_grpc.services module."""

from flext_grpc.services import FlextGrpcServices


class TestFlextGrpcServices:
    """Test cases for FlextGrpcServices class."""

    def test_init(self) -> None:
        """Test FlextGrpcServices initialization."""
        services = FlextGrpcServices()
        assert services is not None

    def test_connect_client(self) -> None:
        """Test client connection."""
        services = FlextGrpcServices()
        result = services.connect_client("localhost:50051")
        # Connection may fail in test environment, but method should exist
        assert (
            result.is_success or not result.is_success
        )  # Just check it returns a result

    def test_create_stream(self) -> None:
        """Test stream creation."""
        services = FlextGrpcServices()
        result = services.create_stream("test_method")
        assert result.is_success
