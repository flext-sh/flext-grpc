"""Tests for flext_grpc.typings module."""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import u


class TestsFlextGrpcTypesUnit:
    """Test cases for FlextGrpcTypes class."""

    def test_grpc_validation(self) -> None:
        """Test gRPC validation."""
        tm.that(u.Grpc.validate_target("localhost:50051"), eq=True)
        tm.that(not u.Grpc.validate_target("invalid"), eq=True)
        tm.that(not u.Grpc.validate_target("localhost:99999"), eq=True)

    def test_parse_target(self) -> None:
        """Test target parsing."""
        host, port = u.Grpc.parse_target("localhost:50051")
        tm.that(host, eq="localhost")
        tm.that(port, eq=50051)

    def test_parse_target_invalid(self) -> None:
        """Test invalid target parsing."""
        with pytest.raises(ValueError):
            u.Grpc.parse_target("invalid")

    def test_validate_target_edge_cases(self) -> None:
        """Test edge cases for target validation."""
        tm.that(not u.Grpc.validate_target(""), eq=True)
        tm.that(not u.Grpc.validate_target("localhost"), eq=True)
        tm.that(not u.Grpc.validate_target(":50051"), eq=True)
        tm.that(not u.Grpc.validate_target("localhost:"), eq=True)
        tm.that(
            not u.Grpc.validate_target("invalid@host:50051"),
            eq=True,
        )
        tm.that(not u.Grpc.validate_target("localhost:0"), eq=True)
        tm.that(not u.Grpc.validate_target("localhost:65536"), eq=True)
        tm.that(u.Grpc.validate_target("localhost:50051"), eq=True)
        tm.that(u.Grpc.validate_target("127.0.0.1:8080"), eq=True)
        tm.that(u.Grpc.validate_target("my-service.com:443"), eq=True)

    def test_parse_target_edge_cases(self) -> None:
        """Test edge cases for target parsing."""
        tm.that(
            u.Grpc.parse_target("localhost:50051"),
            eq=(
                "localhost",
                50051,
            ),
        )
        tm.that(
            u.Grpc.parse_target("127.0.0.1:8080"),
            eq=(
                "127.0.0.1",
                8080,
            ),
        )
        tm.that(
            u.Grpc.parse_target("service.domain.com:443"),
            eq=(
                "service.domain.com",
                443,
            ),
        )
