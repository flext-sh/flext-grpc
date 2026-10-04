"""Behavioral tests for the flext_grpc.constants public contract.

Exercises the observable contract of ``FlextGrpcConstants.Grpc``: the
published constant values, their invariants (ordering / range validity),
the ``StrEnum`` members, the enum-derived frozensets, and the compiled
regex patterns' match behavior.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c

Grpc = c.Grpc


class TestsFlextGrpcConstantsUnit:
    """Public-contract tests for FlextGrpcConstants."""

    @staticmethod
    @pytest.mark.parametrize(
        ("name", "expected"),
        [
            ("NETWORK_DEFAULT_HOST", "127.0.0.1"),
            ("NETWORK_DEFAULT_GRPC_PORT", 50051),
            ("NETWORK_MIN_PORT", 1),
            ("NETWORK_MAX_PORT", 65535),
            ("SERVICE_DEFAULT_MAX_WORKERS", 10),
            ("VALIDATION_ADDRESS_PARTS_COUNT", 2),
            ("VALIDATION_MAX_PORT_NUMBER", 65535),
            ("CLIENT_STREAMING_BUFFER_THRESHOLD", 10),
            ("SERVER_STREAMING_BATCH_SIZE", 100),
            ("BIDIRECTIONAL_STREAMING_QUEUE_SIZE", 1000),
        ],
    )
    def test_published_constant_values(name: str, expected: str | int) -> None:
        """Each published constant exposes its contracted value."""
        tm.that(getattr(Grpc, name), eq=expected)

    @staticmethod
    def test_port_bounds_are_ordered() -> None:
        """The minimum port stays strictly below the maximum port."""
        assert Grpc.NETWORK_MIN_PORT < Grpc.NETWORK_MAX_PORT

    @staticmethod
    def test_default_grpc_port_within_valid_port_range() -> None:
        """The default port is a valid TCP port within the declared range."""
        assert Grpc.NETWORK_MIN_PORT <= Grpc.NETWORK_DEFAULT_GRPC_PORT
        assert Grpc.NETWORK_DEFAULT_GRPC_PORT <= Grpc.NETWORK_MAX_PORT

    @staticmethod
    def test_max_port_matches_validation_max() -> None:
        """Network max port and validation max port express the same limit."""
        tm.that(Grpc.NETWORK_MAX_PORT, eq=Grpc.VALIDATION_MAX_PORT_NUMBER)

    @staticmethod
    @pytest.mark.parametrize(
        "host", ["127.0.0.1", "localhost", "grpc-server", "example.com"]
    )
    def test_host_pattern_accepts_valid_hosts(host: str) -> None:
        """The compiled host pattern matches syntactically valid hosts."""
        tm.that(Grpc.NETWORK_HOST_RE.match(host), none=False)

    @staticmethod
    @pytest.mark.parametrize(
        "host", ["bad host", "under_score!", "with/slash", "colon:port"]
    )
    def test_host_pattern_rejects_invalid_hosts(host: str) -> None:
        """The compiled host pattern rejects hosts with illegal characters."""
        tm.that(Grpc.NETWORK_HOST_RE.match(host), none=True)

    @staticmethod
    @pytest.mark.parametrize(
        ("text", "expected_group"),
        [("Version 1.2.3", "1.2.3"), ("version 4.5.6 build", "4.5.6")],
    )
    def test_version_pattern_captures_semver(
        text: str,
        expected_group: str,
    ) -> None:
        """The version pattern extracts the semantic version, case-insensitively."""
        match = tm.not_none(Grpc.VALIDATION_VERSION_RE.search(text))
        tm.that(match.group(1), eq=expected_group)

    @staticmethod
    def test_version_pattern_returns_none_without_version() -> None:
        """The version pattern yields no match when no version is present."""
        tm.that(Grpc.VALIDATION_VERSION_RE.search("no digits here"), none=True)

    @staticmethod
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
    def test_enum_members_expose_string_values(member: str, value: str) -> None:
        """Each StrEnum member equals its contracted string value."""
        tm.that(member, eq=value)
        tm.that(member, is_=str)

    @staticmethod
    @pytest.mark.parametrize(
        ("frozenset_attr", "enum_attr"),
        [
            ("CHANNEL_STATES", "ChannelState"),
            ("SERVER_STATES", "ServerState"),
            ("STREAM_TYPES", "GrpcOperations"),
        ],
    )
    def test_frozensets_derive_from_their_enums(
        frozenset_attr: str,
        enum_attr: str,
    ) -> None:
        """Each published frozenset equals the value set of its source enum."""
        collection = getattr(Grpc, frozenset_attr)
        enum = getattr(Grpc, enum_attr)
        tm.that(collection, is_=frozenset)
        tm.that(collection, eq={member.value for member in enum})

    @staticmethod
    def test_enum_values_are_unique() -> None:
        """@unique enums never expose duplicate values across their members."""
        for enum_name in ("ChannelState", "ServerState", "ServiceMethod"):
            enum = getattr(Grpc, enum_name)
            values = [member.value for member in enum]
            tm.that(len(values), eq=len(set(values)))
