"""Tests for flext_grpc.constants module."""

from __future__ import annotations

from flext_tests import tm

from flext_grpc import FlextGrpcConstants


class TestFlextGrpcConstants:
    """Test cases for FlextGrpcConstants class."""

    def test_network_constants(self) -> None:
        """Test network constants."""
        tm.that(
            FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_HOST == "127.0.0.1", eq=True
        )
        tm.that(FlextGrpcConstants.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT == 50051, eq=True)
        tm.that(FlextGrpcConstants.Grpc.GrpcNetwork.MIN_PORT == 1, eq=True)
        tm.that(FlextGrpcConstants.Grpc.GrpcNetwork.MAX_PORT == 65535, eq=True)

    def test_service_constants(self) -> None:
        """Test service constants."""
        tm.that(FlextGrpcConstants.Grpc.Service.DEFAULT_MAX_WORKERS == 10, eq=True)
        tm.that(FlextGrpcConstants.Grpc.Service.MIN_WORKERS == 1, eq=True)
        tm.that(FlextGrpcConstants.Grpc.Service.MAX_WORKERS == 100, eq=True)

    def test_validation_constants(self) -> None:
        """Test validation constants."""
        tm.that(
            FlextGrpcConstants.Grpc.GrpcValidation.ADDRESS_PARTS_COUNT == 2, eq=True
        )
        tm.that(
            FlextGrpcConstants.Grpc.GrpcValidation.MAX_PORT_NUMBER == 65535, eq=True
        )

    def test_streaming_constants(self) -> None:
        """Test streaming constants."""
        tm.that(
            FlextGrpcConstants.Grpc.Streaming.CLIENT_STREAMING_BUFFER_THRESHOLD == 10,
            eq=True,
        )
        tm.that(
            FlextGrpcConstants.Grpc.Streaming.SERVER_STREAMING_BATCH_SIZE == 100,
            eq=True,
        )
        tm.that(
            (
                FlextGrpcConstants.Grpc.Streaming.BIDIRECTIONAL_STREAMING_QUEUE_SIZE
                == 1000
            ),
            eq=True,
        )
