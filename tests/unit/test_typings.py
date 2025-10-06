"""Tests for flext_grpc.typings module."""

import pytest

from flext_grpc.typings import FlextGrpcTypings


class TestFlextGrpcTypings:
    """Test cases for FlextGrpcTypings class."""

    def test_grpc_validation(self) -> None:
        """Test gRPC validation."""
        assert FlextGrpcTypings.GrpcValidation.validate_target("localhost:50051")
        assert not FlextGrpcTypings.GrpcValidation.validate_target("invalid")
        assert not FlextGrpcTypings.GrpcValidation.validate_target("localhost:99999")

    def test_parse_target(self) -> None:
        """Test target parsing."""
        host, port = FlextGrpcTypings.GrpcValidation.parse_target("localhost:50051")
        assert host == "localhost"
        assert port == 50051

    def test_parse_target_invalid(self) -> None:
        """Test invalid target parsing."""
        with pytest.raises(ValueError):
            FlextGrpcTypings.GrpcValidation.parse_target("invalid")
