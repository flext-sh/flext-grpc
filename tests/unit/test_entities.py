"""Tests for flext_grpc.entities module."""

from flext_grpc.entities import FlextGrpcEntities


class TestFlextGrpcEntities:
    """Test cases for FlextGrpcEntities class."""

    def test_grpc_server_creation(self) -> None:
        """Test gRPC server entity creation."""
        server = FlextGrpcEntities.GrpcServer(
            host="localhost", port=50051, max_workers=10
        )
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 10

    def test_grpc_client_creation(self) -> None:
        """Test gRPC client entity creation."""
        client = FlextGrpcEntities.GrpcClient(target="localhost:50051")
        assert client.target == "localhost:50051"

    def test_grpc_channel_creation(self) -> None:
        """Test gRPC channel entity creation."""
        channel = FlextGrpcEntities.GrpcChannel(address="localhost:50051")
        assert channel.address == "localhost:50051"

    def test_grpc_stream_creation(self) -> None:
        """Test gRPC stream entity creation."""
        stream = FlextGrpcEntities.GrpcStream(
            id="test_stream", method_name="test_method", stream_type="unary"
        )
        assert stream.id == "test_stream"
        assert stream.method_name == "test_method"
        assert stream.stream_type == "unary"
