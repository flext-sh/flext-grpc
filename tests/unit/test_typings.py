"""Behavioral tests for the flext_grpc gRPC target contract.

Exercises the public ``FlextGrpcUtilities.Grpc`` target helpers through their
observable contract only: return values of ``validate_target`` (bool) and
``parse_target`` (``tuple[str, int]`` or a raised ``ValueError``).
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests.utilities import u


class TestsFlextGrpcTypesUnit:
    """Behavioral contract for the gRPC ``host:port`` target helpers."""

    @pytest.mark.parametrize(
        "target",
        [
            "localhost:50051",
            "127.0.0.1:8080",
            "my-service.com:443",
            "service.domain.com:443",
        ],
    )
    def test_validate_target_accepts_wellformed_host_port(self, target: str) -> None:
        """A syntactically valid host:port with an in-range port validates true."""
        tm.that(u.Grpc.validate_target(target), eq=True)

    @pytest.mark.parametrize(
        "target",
        [
            "",
            "invalid",
            "localhost",
            ":50051",
            "localhost:",
            "invalid@host:50051",
            "localhost:0",
            "localhost:65536",
            "localhost:99999",
        ],
    )
    def test_validate_target_rejects_malformed_or_out_of_range(
        self,
        target: str,
    ) -> None:
        """Missing host/port, bad host chars, or out-of-range ports validate false."""
        tm.that(u.Grpc.validate_target(target), eq=False)

    @pytest.mark.parametrize(
        ("target", "expected"),
        [
            ("localhost:50051", ("localhost", 50051)),
            ("127.0.0.1:8080", ("127.0.0.1", 8080)),
            ("service.domain.com:443", ("service.domain.com", 443)),
        ],
    )
    def test_parse_target_splits_into_host_and_int_port(
        self,
        target: str,
        expected: tuple[str, int],
    ) -> None:
        """Parsing a valid target yields the host string and integer port."""
        tm.that(u.Grpc.parse_target(target), eq=expected)

    @pytest.mark.parametrize(
        "target",
        ["invalid", "", "localhost", ":50051", "localhost:99999"],
    )
    def test_parse_target_raises_value_error_on_invalid(self, target: str) -> None:
        """Parsing a target that fails validation raises ``ValueError``."""
        with pytest.raises(ValueError, match="Invalid gRPC target"):
            u.Grpc.parse_target(target)

    @pytest.mark.parametrize(
        "target",
        [
            "localhost:50051",
            "127.0.0.1:8080",
            "invalid",
            "localhost:99999",
            "",
        ],
    )
    def test_parse_target_succeeds_iff_validate_target_true(self, target: str) -> None:
        """Invariant: ``parse_target`` returns cleanly exactly when validation passes."""
        is_valid = u.Grpc.validate_target(target)
        if is_valid:
            host, port = u.Grpc.parse_target(target)
            tm.that(f"{host}:{port}", eq=target)
        else:
            with pytest.raises(ValueError, match="Invalid gRPC target"):
                u.Grpc.parse_target(target)
