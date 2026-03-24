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
        tm.that(config.host, eq="127.0.0.1")
        tm.that(config.port, eq=50051)
        tm.that(config.max_workers, eq=10)

    def test_client_config(self) -> None:
        """Test client config model."""
        config = FlextGrpcModels.Grpc.ClientConfig(
            target="127.0.0.1:50051", timeout=30.0
        )
        tm.that(config.target, eq="127.0.0.1:50051")

    def test_channel_config(self) -> None:
        """Test channel config model."""
        config = FlextGrpcModels.Grpc.ChannelConfig(address="localhost:50051")
        tm.that(config.address, eq="localhost:50051")

    def test_stream_info(self) -> None:
        """Test stream info model."""
        stream_info = FlextGrpcModels.Grpc.StreamInfo.model_validate({
            "stream_id": "test",
            "stream_type": "unary",
            "target": "localhost:50051",
        })
        tm.that(stream_info.stream_id, eq="test")
        tm.that(stream_info.stream_type, eq="unary")
        tm.that(stream_info.target, eq="localhost:50051")
