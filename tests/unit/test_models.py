"""Tests for flext_grpc.models module."""

from flext_grpc.models import FlextGrpcModels


class TestFlextGrpcModels:
    """Test cases for FlextGrpcModels class."""

    def test_server_config(self) -> None:
        """Test server config model."""
        config = FlextGrpcModels.GrpcConfig.ServerConfig()
        assert config.host == "127.0.0.1"
        assert config.port == 50051
        assert config.max_workers == 10

    def test_client_config(self) -> None:
        """Test client config model."""
        config = FlextGrpcModels.GrpcConfig.ClientConfig()
        assert config.target == "127.0.0.1:50051"

    def test_channel_config(self) -> None:
        """Test channel config model."""
        config = FlextGrpcModels.GrpcConfig.ChannelConfig(address="localhost:50051")
        assert config.address == "localhost:50051"

    def test_stream_info(self) -> None:
        """Test stream info model."""
        stream_info = FlextGrpcModels.Grpc.StreamInfo(
            stream_id="test",
            stream_type="unary",
            target="localhost:50051",
        )
        assert stream_info.stream_id == "test"
        assert stream_info.stream_type == "unary"
        assert stream_info.target == "localhost:50051"
