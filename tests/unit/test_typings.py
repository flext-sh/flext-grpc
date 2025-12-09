"""Tests for flext_grpc.typings module."""

import pytest

from flext_grpc.typings import t


class TestFlextGrpcTypes:
    """Test cases for FlextGrpcTypes class."""

    def test_grpc_validation(self) -> None:
        """Test gRPC validation."""
        assert t.GrpcValidation.validate_target("localhost:50051")
        assert not t.GrpcValidation.validate_target("invalid")
        assert not t.GrpcValidation.validate_target("localhost:99999")

    def test_parse_target(self) -> None:
        """Test target parsing."""
        host, port = t.GrpcValidation.parse_target("localhost:50051")
        assert host == "localhost"
        assert port == 50051

    def test_parse_target_invalid(self) -> None:
        """Test invalid target parsing."""
        with pytest.raises(ValueError):
            t.GrpcValidation.parse_target("invalid")

    def test_validate_target_edge_cases(self) -> None:
        """Test edge cases for target validation."""
        # Test empty string
        assert not t.GrpcValidation.validate_target("")

        # Test no colon
        assert not t.GrpcValidation.validate_target("localhost")

        # Test empty host
        assert not t.GrpcValidation.validate_target(":50051")

        # Test empty port
        assert not t.GrpcValidation.validate_target("localhost:")

        # Test invalid host characters
        assert not t.GrpcValidation.validate_target("invalid@host:50051")

        # Test port too low
        assert not t.GrpcValidation.validate_target("localhost:0")

        # Test port too high
        assert not t.GrpcValidation.validate_target("localhost:65536")

        # Test valid cases
        assert t.GrpcValidation.validate_target("localhost:50051")
        assert t.GrpcValidation.validate_target("127.0.0.1:8080")
        assert t.GrpcValidation.validate_target("my-service.com:443")

    def test_parse_target_edge_cases(self) -> None:
        """Test edge cases for target parsing."""
        # Test various valid targets
        assert t.GrpcValidation.parse_target("localhost:50051") == (
            "localhost",
            50051,
        )
        assert t.GrpcValidation.parse_target("127.0.0.1:8080") == (
            "127.0.0.1",
            8080,
        )
        assert t.GrpcValidation.parse_target("service.domain.com:443") == (
            "service.domain.com",
            443,
        )
