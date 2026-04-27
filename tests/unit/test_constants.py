"""Tests for flext_grpc.constants module."""

from __future__ import annotations

from flext_tests import tm

from tests import c


class TestsFlextGrpcConstantsUnit:
    """Test cases for FlextGrpcConstants class."""

    def test_network_constants(self) -> None:
        """Test network constants."""
        tm.that(c.Grpc.NETWORK_DEFAULT_HOST, eq="127.0.0.1")
        tm.that(c.Grpc.NETWORK_DEFAULT_GRPC_PORT, eq=50051)
        tm.that(c.Grpc.NETWORK_MIN_PORT, eq=1)
        tm.that(c.Grpc.NETWORK_MAX_PORT, eq=65535)

    def test_service_constants(self) -> None:
        """Test service constants."""
        tm.that(c.Grpc.SERVICE_DEFAULT_MAX_WORKERS, eq=10)
        tm.that(c.Grpc.SERVICE_MIN_WORKERS, eq=1)
        tm.that(c.Grpc.SERVICE_MAX_WORKERS, eq=100)

    def test_validation_constants(self) -> None:
        """Test validation constants."""
        tm.that(c.Grpc.VALIDATION_ADDRESS_PARTS_COUNT, eq=2)
        tm.that(c.Grpc.VALIDATION_MAX_PORT_NUMBER, eq=65535)

    def test_streaming_constants(self) -> None:
        """Test streaming constants."""
        tm.that(
            c.Grpc.STREAMING_CLIENT_STREAMING_BUFFER_THRESHOLD,
            eq=10,
        )
        tm.that(c.Grpc.STREAMING_SERVER_STREAMING_BATCH_SIZE, eq=100)
        tm.that(
            (c.Grpc.STREAMING_BIDIRECTIONAL_STREAMING_QUEUE_SIZE == 1000),
            eq=True,
        )
