"""Tests for flext_grpc.models module."""

from __future__ import annotations

from flext_tests import tm

from flext_grpc import FlextGrpcModels


class TestFlextGrpcModels:
    """Test cases for FlextGrpcModels class."""

    def test_server_config(self) -> None:
        """Test server config model."""
        config = FlextGrpcModels.Grpc.ServerConfig(
            host="127.0.0.1", port=50051, max_workers=10, timeout=30.0
        )
        tm.that(config.host == "127.0.0.1", eq=True)
        tm.that(config.port == 50051, eq=True)
        tm.that(config.max_workers == 10, eq=True)

    def test_client_config(self) -> None:
        """Test client config model."""
        config = FlextGrpcModels.Grpc.ClientConfig(
            target="127.0.0.1:50051", timeout=30.0
        )
        tm.that(config.target == "127.0.0.1:50051", eq=True)

    def test_channel_config(self) -> None:
        """Test channel config model."""
        config = FlextGrpcModels.Grpc.ChannelConfig(address="localhost:50051")
        tm.that(config.address == "localhost:50051", eq=True)

    def test_stream_info(self) -> None:
        """Test stream info model."""
        stream_info = FlextGrpcModels.Grpc.StreamInfo.model_validate({
            "stream_id": "test",
            "stream_type": "unary",
            "target": "localhost:50051",
        })
        tm.that(stream_info.stream_id == "test", eq=True)
        tm.that(stream_info.stream_type == "unary", eq=True)
        tm.that(stream_info.target == "localhost:50051", eq=True)
