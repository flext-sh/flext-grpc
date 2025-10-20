"""Tests for flext_grpc.typings module."""

import pytest

from flext_grpc.typings import FlextGrpcTypes


class TestFlextGrpcTypes:
    """Test cases for FlextGrpcTypes class."""

    def test_grpc_validation(self) -> None:
        """Test gRPC validation."""
        assert FlextGrpcTypes.GrpcValidation.validate_target("localhost:50051")
        assert not FlextGrpcTypes.GrpcValidation.validate_target("invalid")
        assert not FlextGrpcTypes.GrpcValidation.validate_target("localhost:99999")

    def test_parse_target(self) -> None:
        """Test target parsing."""
        host, port = FlextGrpcTypes.GrpcValidation.parse_target("localhost:50051")
        assert host == "localhost"
        assert port == 50051

    def test_parse_target_invalid(self) -> None:
        """Test invalid target parsing."""
        with pytest.raises(ValueError):
            FlextGrpcTypes.GrpcValidation.parse_target("invalid")
