"""Tests for flext_grpc.constants module."""

from __future__ import annotations

from flext_tests import tm

from flext_grpc import FlextGrpcConstants


class TestFlextGrpcConstants:
    """Test cases for FlextGrpcConstants class."""

    def test_network_constants(self) -> None:
        """Test network constants."""
        tm.that(FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST, eq="127.0.0.1")
        tm.that(FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT, eq=50051)
        tm.that(FlextGrpcConstants.Grpc.GrpcNetwork.MIN_PORT, eq=1)
        tm.that(FlextGrpcConstants.Grpc.GrpcNetwork.MAX_PORT, eq=65535)

    def test_service_constants(self) -> None:
        """Test service constants."""
        tm.that(FlextGrpcConstants.Grpc.Service.DEFAULT_MAX_WORKERS, eq=10)
        tm.that(FlextGrpcConstants.Grpc.Service.MIN_WORKERS, eq=1)
        tm.that(FlextGrpcConstants.Grpc.Service.MAX_WORKERS, eq=100)

    def test_validation_constants(self) -> None:
        """Test validation constants."""
        tm.that(FlextGrpcConstants.Grpc.GrpcValidation.ADDRESS_PARTS_COUNT, eq=2)
        tm.that(FlextGrpcConstants.Grpc.GrpcValidation.MAX_PORT_NUMBER, eq=65535)

    def test_streaming_constants(self) -> None:
        """Test streaming constants."""
        tm.that(FlextGrpcConstants.Grpc.Streaming.CLIENT_STREAMING_BUFFER_THRESHOLD, eq=10)
        tm.that(FlextGrpcConstants.Grpc.Streaming.SERVER_STREAMING_BATCH_SIZE, eq=100)
        tm.that(
            (
                FlextGrpcConstants.Grpc.Streaming.BIDIRECTIONAL_STREAMING_QUEUE_SIZE
                == 1000
            ),
            eq=True,
        )
