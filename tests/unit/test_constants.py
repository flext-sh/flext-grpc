"""Tests for flext_grpc.constants module."""

from flext_grpc.constants import FlextGrpcConstants


class TestFlextGrpcConstants:
    """Test cases for FlextGrpcConstants class."""

    def test_network_constants(self) -> None:
        """Test network constants."""
        assert FlextGrpcConstants.GrpcNetwork.DEFAULT_HOST == "127.0.0.1"
        assert FlextGrpcConstants.GrpcNetwork.DEFAULT_GRPC_PORT == 50051
        assert FlextGrpcConstants.Network.MIN_PORT == 1
        assert FlextGrpcConstants.Network.MAX_PORT == 65535

    def test_service_constants(self) -> None:
        """Test service constants."""
        assert FlextGrpcConstants.Service.DEFAULT_MAX_WORKERS == 10
        assert FlextGrpcConstants.Service.MIN_WORKERS == 1
        assert FlextGrpcConstants.Service.MAX_WORKERS == 100

    def test_validation_constants(self) -> None:
        """Test validation constants."""
        assert FlextGrpcConstants.GrpcValidation.ADDRESS_PARTS_COUNT == 2
        assert FlextGrpcConstants.GrpcValidation.MAX_PORT_NUMBER == 65535

    def test_streaming_constants(self) -> None:
        """Test streaming constants."""
        assert FlextGrpcConstants.Streaming.CLIENT_STREAMING_BUFFER_THRESHOLD == 10
        assert FlextGrpcConstants.Streaming.SERVER_STREAMING_BATCH_SIZE == 100
        assert FlextGrpcConstants.Streaming.BIDIRECTIONAL_STREAMING_QUEUE_SIZE == 1000
