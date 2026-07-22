"""Behavioral tests for the flext-grpc protocol contracts.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

These tests assert the OBSERVABLE contract of the runtime-checkable
``p.Grpc.*`` protocols: what ``typing.is_protocol`` reports, and how
``isinstance`` behaves against conforming and non-conforming duck objects.
The set of declared members per protocol is the public structural contract,
so it is exercised through the only mechanism callers actually rely on --
structural ``isinstance`` narrowing -- never through private attributes.
"""

from __future__ import annotations

from typing import Protocol, is_protocol, runtime_checkable

import pytest

from flext_grpc import FlextGrpcProtocols, t
from flext_tests import tm
from tests import p

# Public structural contract: protocol name -> required method members.
# Each row states the methods a concrete implementation MUST provide to
# satisfy the runtime-checkable protocol (verified via isinstance below).
_PROTOCOL_CONTRACTS: t.MappingKV[str, tuple[str, ...]] = {
    "Server": (
        "add_service",
        "configure_port",
        "server_status",
        "start_server",
        "stop_server",
    ),
    "Client": (
        "client_status",
        "connect_client",
        "disconnect_client",
        "make_call",
        "validate_connection",
    ),
    "Streaming": (
        "close_stream",
        "create_stream",
        "handle_bidirectional_streaming",
        "handle_client_streaming",
        "handle_server_streaming",
        "send_data",
    ),
    "Service": (
        "create_service",
        "register_service",
        "service_methods",
        "validate_service",
    ),
    "Channel": (
        "channel_state",
        "close_channel",
        "create_channel",
        "wait_for_state_change",
    ),
    "Metrics": (
        "collect_client_metrics",
        "collect_server_metrics",
        "collect_stream_metrics",
        "global_metrics",
        "start_metrics_collection",
        "stop_metrics_collection",
    ),
    "Configuration": (
        "create_client_config",
        "create_server_config",
        "parse_address",
        "validate_address",
        "validate_config",
    ),
}

_PROTOCOL_NAMES: tuple[str, ...] = tuple(_PROTOCOL_CONTRACTS)


def _build_conforming_instance(members: tuple[str, ...]) -> object:
    """Create an object exposing exactly ``members`` as callables."""
    namespace = {name: (lambda self, *a, **k: None) for name in members}
    return type("Conforming", (), namespace)()


def _build_partial_instance(members: tuple[str, ...], *, omit: str) -> object:
    """Create an object exposing every member except ``omit``."""
    namespace = {name: (lambda self, *a, **k: None) for name in members if name != omit}
    return type("Partial", (), namespace)()


class TestsFlextGrpcProtocolsUnit:
    """Behavioral contract tests for the ``p.Grpc.*`` protocols."""

    @pytest.mark.parametrize("protocol_name", _PROTOCOL_NAMES)
    def test_grpc_protocol_is_a_protocol(self, protocol_name: str) -> None:
        """Each Grpc member is reported as a typing Protocol."""
        protocol = getattr(p.Grpc, protocol_name)

        tm.that(is_protocol(protocol), eq=True)

    @pytest.mark.parametrize("protocol_name", _PROTOCOL_NAMES)
    def test_conforming_object_satisfies_protocol(self, protocol_name: str) -> None:
        """An object exposing all required members passes isinstance."""
        members = _PROTOCOL_CONTRACTS[protocol_name]
        protocol = getattr(p.Grpc, protocol_name)

        instance = _build_conforming_instance(members)

        tm.that(isinstance(instance, protocol), eq=True)

    @pytest.mark.parametrize(
        ("protocol_name", "missing_member"),
        [
            (name, member)
            for name, members in _PROTOCOL_CONTRACTS.items()
            for member in members
        ],
    )
    def test_object_missing_one_member_fails_protocol(
        self, protocol_name: str, missing_member: str
    ) -> None:
        """Omitting any single required member fails isinstance narrowing."""
        members = _PROTOCOL_CONTRACTS[protocol_name]
        protocol = getattr(p.Grpc, protocol_name)

        instance = _build_partial_instance(members, omit=missing_member)

        tm.that(isinstance(instance, protocol), eq=False)

    @pytest.mark.parametrize("protocol_name", _PROTOCOL_NAMES)
    def test_unrelated_object_fails_protocol(self, protocol_name: str) -> None:
        """A plain object with none of the members fails isinstance."""
        protocol = getattr(p.Grpc, protocol_name)

        tm.that(isinstance(object(), protocol), eq=False)

    @pytest.mark.parametrize("protocol_name", _PROTOCOL_NAMES)
    def test_protocol_is_runtime_checkable(self, protocol_name: str) -> None:
        """The protocol supports isinstance without raising (runtime_checkable)."""
        protocol = getattr(p.Grpc, protocol_name)

        # A non-runtime-checkable Protocol raises TypeError here; a
        # runtime-checkable one returns a bool. Reaching the assert proves
        # the observable runtime-checkability contract.
        result = isinstance(object(), protocol)

        tm.that(result, eq=False)

    def test_test_protocol_namespace_composes_source_namespace(self) -> None:
        """The tests Grpc namespace inherits the source Grpc protocols."""
        tm.that(p.Grpc.__mro__, has=FlextGrpcProtocols.Grpc)

    @pytest.mark.parametrize("protocol_name", _PROTOCOL_NAMES)
    def test_test_namespace_exposes_same_protocol_object(
        self, protocol_name: str
    ) -> None:
        """Access via the tests namespace resolves the source protocol."""
        assert getattr(p.Grpc, protocol_name) is getattr(
            FlextGrpcProtocols.Grpc, protocol_name
        )

    def test_conforming_object_can_type_narrow_via_protocol(self) -> None:
        """A user-defined class declared against the protocol is recognized."""

        @runtime_checkable
        class _Marker(Protocol):
            def start_server(self) -> None: ...

        # Sanity guard that our conforming builder yields real callables the
        # protocol machinery accepts, independent of the source definitions.
        instance = _build_conforming_instance(_PROTOCOL_CONTRACTS["Server"])

        tm.that(isinstance(instance, _Marker), eq=True)
