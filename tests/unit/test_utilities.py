"""Tests for flext_grpc.utilities module."""

from flext_grpc.utilities import FlextGrpcUtilities


class TestFlextGrpcUtilities:
    """Test cases for FlextGrpcUtilities class."""

    def test_init(self) -> None:
        """Test FlextGrpcUtilities initialization."""
        utilities = FlextGrpcUtilities()
        assert utilities is not None

    def test_system_utilities(self) -> None:
        """Test system utilities."""
        utilities = FlextGrpcUtilities()
        assert hasattr(utilities, "SystemUtilities")

    def test_protobuf_utilities(self) -> None:
        """Test protobuf utilities."""
        utilities = FlextGrpcUtilities()
        assert hasattr(utilities, "ProtobufUtilities")
