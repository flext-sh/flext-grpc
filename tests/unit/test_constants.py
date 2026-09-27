"""Behavioral tests for the flext_grpc.constants public contract.

Exercises the observable contract of ``FlextGrpcConstants.Grpc``: the
published constant values, their invariants (ordering / range validity),
the ``StrEnum`` members, the enum-derived frozensets, and the compiled
regex patterns' match behavior.
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c

Grpc = c.Grpc


class TestsFlextGrpcConstantsUnit:
    """Public-contract tests for FlextGrpcConstants."""

    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            ("NETWORK_DEFAULT_HOST", "127.0.0.1"),
            ("NETWORK_DEFAULT_GRPC_PORT", 50051),
            ("NETWORK_MIN_PORT", 1),
            ("NETWORK_MAX_PORT", 65535),
            ("SERVICE_DEFAULT_MAX_WORKERS", 10),
            ("SERVICE_MIN_WORKERS", 1),
            ("SERVICE_MAX_WORKERS", 100),
            ("VALIDATION_ADDRESS_PARTS_COUNT", 2),
            ("VALIDATION_MAX_PORT_NUMBER", 65535),
            ("CLIENT_STREAMING_BUFFER_THRESHOLD", 10),
            ("SERVER_STREAMING_BATCH_SIZE", 100),
            ("BIDIRECTIONAL_STREAMING_QUEUE_SIZE", 1000),
        ],
    )
    def test_published_constant_values(self, name: str, expected: str | int) -> None:
        """Each published constant exposes its contracted value."""
        tm.that(getattr(Grpc, name), eq=expected)

    @pytest.mark.parametrize(
        ("lower", "upper"),
        [
            ("NETWORK_MIN_PORT", "NETWORK_MAX_PORT"),
            ("SERVICE_MIN_WORKERS", "SERVICE_MAX_WORKERS"),
            ("PERFORMANCE_MIN_MESSAGE_LENGTH", "PERFORMANCE_DEFAULT_MESSAGE_LENGTH"),
            ("PERFORMANCE_DEFAULT_MESSAGE_LENGTH", "PERFORMANCE_MAX_MESSAGE_LENGTH"),
            (
                "PERFORMANCE_MIN_THREAD_POOL_SIZE",
                "PERFORMANCE_DEFAULT_THREAD_POOL_SIZE",
            ),
            (
                "PERFORMANCE_DEFAULT_THREAD_POOL_SIZE",
                "PERFORMANCE_MAX_THREAD_POOL_SIZE",
            ),
            ("STREAMING_MIN_BUFFER_SIZE", "STREAMING_DEFAULT_BUFFER_SIZE"),
            ("STREAMING_DEFAULT_BUFFER_SIZE", "STREAMING_MAX_BUFFER_SIZE"),
        ],
    )
    def test_range_bounds_are_ordered(self, lower: str, upper: str) -> None:
        """Min/default/max bound pairs preserve a strict ordering invariant."""
        assert getattr(Grpc, lower) < getattr(Grpc, upper)

    def test_default_and_min_workers_are_within_bounds(self) -> None:
        """The default worker count falls inside the declared worker range."""
        assert Grpc.SERVICE_MIN_WORKERS <= Grpc.SERVICE_DEFAULT_MAX_WORKERS
        assert Grpc.SERVICE_DEFAULT_MAX_WORKERS <= Grpc.SERVICE_MAX_WORKERS

    def test_default_grpc_port_within_valid_port_range(self) -> None:
        """The default port is a valid TCP port within the declared range."""
        assert Grpc.NETWORK_MIN_PORT <= Grpc.NETWORK_DEFAULT_GRPC_PORT
        assert Grpc.NETWORK_DEFAULT_GRPC_PORT <= Grpc.NETWORK_MAX_PORT

    def test_max_port_matches_validation_max(self) -> None:
        """Network max port and validation max port express the same limit."""
        tm.that(Grpc.NETWORK_MAX_PORT, eq=Grpc.VALIDATION_MAX_PORT_NUMBER)

    @pytest.mark.parametrize(
        "host", ["127.0.0.1", "localhost", "grpc-server", "example.com"]
    )
    def test_host_pattern_accepts_valid_hosts(self, host: str) -> None:
        """The compiled host pattern matches syntactically valid hosts."""
        tm.that(Grpc.NETWORK_HOST_RE.match(host), none=False)

    @pytest.mark.parametrize(
        "host", ["bad host", "under_score!", "with/slash", "colon:port"]
    )
    def test_host_pattern_rejects_invalid_hosts(self, host: str) -> None:
        """The compiled host pattern rejects hosts with illegal characters."""
        tm.that(Grpc.NETWORK_HOST_RE.match(host), none=True)

    @pytest.mark.parametrize(
        ("text", "expected_group"),
        [("Version 1.2.3", "1.2.3"), ("version 4.5.6 build", "4.5.6")],
    )
    def test_version_pattern_captures_semver(
        self, text: str, expected_group: str
    ) -> None:
        """The version pattern extracts the semantic version, case-insensitively."""
        match = tm.not_none(Grpc.VALIDATION_VERSION_RE.search(text))
        tm.that(match.group(1), eq=expected_group)

    def test_version_pattern_returns_none_without_version(self) -> None:
        """The version pattern yields no match when no version is present."""
        tm.that(Grpc.VALIDATION_VERSION_RE.search("no digits here"), none=True)

    @pytest.mark.parametrize(
        ("member", "value"),
        [
            (Grpc.ChannelState.IDLE, "idle"),
            (Grpc.ChannelState.READY, "ready"),
            (Grpc.ServerState.STOPPED, "stopped"),
            (Grpc.ServerState.RUNNING, "running"),
            (Grpc.GrpcOperations.UNARY, "unary"),
            (Grpc.ServiceMethod.ECHO, "Echo"),
            (Grpc.ServiceMethod.HEALTH_CHECK, "HealthCheck"),
            (Grpc.CompressionTypes.NONE, "none"),
        ],
    )
    def test_enum_members_expose_string_values(self, member: str, value: str) -> None:
        """Each StrEnum member equals its contracted string value."""
        tm.that(member, eq=value)
        tm.that(member, is_=str)

    @pytest.mark.parametrize(
        ("frozenset_attr", "enum_attr"),
        [
            ("CHANNEL_STATES", "ChannelState"),
            ("SERVER_STATES", "ServerState"),
            ("STREAM_TYPES", "GrpcOperations"),
        ],
    )
    def test_frozensets_derive_from_their_enums(
        self, frozenset_attr: str, enum_attr: str
    ) -> None:
        """Each published frozenset equals the value set of its source enum."""
        collection = getattr(Grpc, frozenset_attr)
        enum = getattr(Grpc, enum_attr)
        tm.that(collection, is_=frozenset)
        tm.that(collection, eq={member.value for member in enum})

    def test_enum_values_are_unique(self) -> None:
        """@unique enums never expose duplicate values across their members."""
        for enum_name in ("ChannelState", "ServerState", "ServiceMethod"):
            enum = getattr(Grpc, enum_name)
            values = [member.value for member in enum]
            tm.that(len(values), eq=len(set(values)))
