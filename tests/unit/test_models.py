"""Tests for flext_grpc.models module."""

from __future__ import annotations

from flext_tests import tm

from tests import m


class TestsFlextGrpcModelsUnit:
    """Test cases for FlextGrpcModels class."""

    def test_server_config(self) -> None:
        """Test server settings model."""
        settings = m.Grpc.ServerConfig(
            host="127.0.0.1",
            port=50051,
            max_workers=10,
            timeout=30.0,
        )
        tm.that(settings.host, eq="127.0.0.1")
        tm.that(settings.port, eq=50051)
        tm.that(settings.max_workers, eq=10)

    def test_client_config(self) -> None:
        """Test client settings model."""
        settings = m.Grpc.ClientConfig(
            target="127.0.0.1:50051",
            timeout=30.0,
        )
        tm.that(settings.target, eq="127.0.0.1:50051")

    def test_channel_config(self) -> None:
        """Test channel settings model."""
        settings = m.Grpc.ChannelConfig(address="localhost:50051")
        tm.that(settings.address, eq="localhost:50051")

    def test_stream_info(self) -> None:
        """Test stream info model."""
        stream_info = m.Grpc.StreamInfo.model_validate({
            "stream_id": "test",
            "stream_type": "unary",
            "target": "localhost:50051",
        })
        tm.that(stream_info.stream_id, eq="test")
        tm.that(stream_info.stream_type, eq="unary")
        tm.that(stream_info.target, eq="localhost:50051")
