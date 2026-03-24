"""Tests for flext_grpc.typings module."""

from __future__ import annotations

import pytest
from flext_tests import tm

from flext_grpc import t


class TestFlextGrpcTypes:
    """Test cases for FlextGrpcTypes class."""

    def test_grpc_validation(self) -> None:
        """Test gRPC validation."""
        tm.that(t.Grpc.GrpcValidation.validate_target("localhost:50051"), eq=True)
        tm.that(t.Grpc.GrpcValidation.validate_target("invalid"), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target("localhost:99999"), eq=False)

    def test_parse_target(self) -> None:
        """Test target parsing."""
        host, port = t.Grpc.GrpcValidation.parse_target("localhost:50051")
        tm.that(host, eq="localhost")
        tm.that(port, eq=50051)

    def test_parse_target_invalid(self) -> None:
        """Test invalid target parsing."""
        with pytest.raises(ValueError):
            t.Grpc.GrpcValidation.parse_target("invalid")

    def test_validate_target_edge_cases(self) -> None:
        """Test edge cases for target validation."""
        tm.that(t.Grpc.GrpcValidation.validate_target(""), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target("localhost"), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target(":50051"), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target("localhost:"), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target("invalid@host:50051"), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target("localhost:0"), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target("localhost:65536"), eq=False)
        tm.that(t.Grpc.GrpcValidation.validate_target("localhost:50051"), eq=True)
        tm.that(t.Grpc.GrpcValidation.validate_target("127.0.0.1:8080"), eq=True)
        tm.that(t.Grpc.GrpcValidation.validate_target("my-service.com:443"), eq=True)

    def test_parse_target_edge_cases(self) -> None:
        """Test edge cases for target parsing."""
        tm.that(t.Grpc.GrpcValidation.parse_target("localhost:50051"), eq=(
            "localhost",
            50051,
        ))
        tm.that(t.Grpc.GrpcValidation.parse_target("127.0.0.1:8080"), eq=(
            "127.0.0.1",
            8080,
        ))
        tm.that(t.Grpc.GrpcValidation.parse_target("service.domain.com:443"), eq=(
            "service.domain.com",
            443,
        ))
