"""Behavioral tests for flext_grpc.entities (gRPC domain models).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c, m


@pytest.fixture
def channel() -> m.Grpc.Channel:
    """Idle channel bound to a concrete target.

    Returns:
        The resulting ``m.Grpc.Channel``.
    """
    return m.Grpc.Channel(
        target="localhost:50051",
        state=c.Grpc.ChannelState.IDLE,
        options={},
        domain_events=[],
    )


class TestsFlextGrpcServerEntities:
    """Public-contract behavior of the gRPC server entity."""

    @staticmethod
    @pytest.fixture
    def server() -> m.Grpc.Server:
        """Return a stopped server with no registered services."""
        return m.Grpc.Server(
            host="localhost", port=50051, services=[], domain_events=[],
        )

    # ---- Server -----------------------------------------------------------

    @staticmethod
    def test_server_exposes_constructor_field_state() -> None:
        """Server surfaces host, port and explicit max_workers as public state."""
        server = m.Grpc.Server(
            host="localhost", port=50051, max_workers=10, services=[], domain_events=[],
        )
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)
        tm.that(server.max_workers, eq=10)

    @staticmethod
    def test_server_defaults_max_workers_when_omitted() -> None:
        """Omitting max_workers yields the documented default of 10."""
        server = m.Grpc.Server(
            host="localhost", port=50051, services=[], domain_events=[],
        )
        tm.that(server.max_workers, eq=10)

    @staticmethod
    def test_server_lifecycle_transitions_through_running_and_stopped(
        server: m.Grpc.Server,
    ) -> None:
        """Start -> mark_running -> stop -> mark_stopped walks the full lifecycle."""
        starting = tm.ok(server.start())
        tm.that(starting.state, eq="starting")
        running = tm.ok(starting.mark_running())
        tm.that(running.state, eq="running")
        stopping = tm.ok(running.stop())
        tm.that(stopping.state, eq="stopping")
        tm.that(tm.ok(stopping.mark_stopped()).state, eq="stopped")

    @staticmethod
    def test_server_start_does_not_mutate_original(server: m.Grpc.Server) -> None:
        """Transitions return a new entity, source left stopped (immutability)."""
        tm.ok(server.start())
        tm.that(server.state, eq="stopped")

    @staticmethod
    def test_server_mark_stopped_rejected_from_stopped(
        server: m.Grpc.Server,
    ) -> None:
        """mark_stopped from an already-stopped state fails with an error."""
        tm.fail(server.mark_stopped(), has="Cannot mark stopped")

    @staticmethod
    def test_server_add_service_appends_to_public_services(
        server: m.Grpc.Server,
    ) -> None:
        """add_service returns a server whose services include the added entry."""
        service = object()
        updated = tm.ok(server.add_service(service))
        updated_services = list(updated.services)
        tm.that(len(updated_services), eq=1)
        assert updated_services[0] is service
        tm.that(list(server.services), eq=[])

    @staticmethod
    def test_server_business_rules_reject_empty_host() -> None:
        """validate_business_rules fails for a server bound to an empty host."""
        server = m.Grpc.Server(host="", port=50051, services=[], domain_events=[])
        tm.fail(server.validate_business_rules(), has="host cannot be empty")

    @staticmethod
    @pytest.mark.parametrize(
        ("port", "max_workers", "match"),
        [(70000, 10, "less_than_equal"), (50051, 0, "greater_than_equal")],
        ids=["out-of-range-port", "zero-workers"],
    )
    def test_server_construction_rejects_out_of_range_numeric_fields(
        port: int, max_workers: int, match: str,
    ) -> None:
        """Port and worker-count bounds are enforced at construction time."""
        with pytest.raises(ValueError, match=match):
            m.Grpc.Server(
                host="localhost",
                port=port,
                max_workers=max_workers,
                services=[],
                domain_events=[],
            )

    @staticmethod
    def test_server_business_rules_pass_for_valid_config(
        server: m.Grpc.Server,
    ) -> None:
        """A well-formed server validates successfully."""
        tm.ok(server.validate_business_rules())


class TestsFlextGrpcChannelEntities:
    """Public-contract behavior of the gRPC channel entity."""

    # ---- Channel ----------------------------------------------------------

    @staticmethod
    def test_channel_exposes_target(channel: m.Grpc.Channel) -> None:
        """Channel surfaces its configured target address."""
        tm.that(channel.target, eq="localhost:50051")

    @staticmethod
    def test_channel_connect_transitions_idle_to_connecting(
        channel: m.Grpc.Channel,
    ) -> None:
        """Connect moves an idle channel to the connecting state."""
        tm.that(tm.ok(channel.connect()).state, eq="connecting")

    @staticmethod
    def test_channel_reaches_ready_then_returns_to_idle(
        channel: m.Grpc.Channel,
    ) -> None:
        """Connect -> mark_ready -> disconnect drives the readiness cycle."""
        ready = tm.ok(tm.ok(channel.connect()).mark_ready())
        tm.that(ready.state, eq="ready")
        tm.that(ready.ready(), eq=True)
        tm.that(tm.ok(ready.disconnect()).state, eq="idle")

    @staticmethod
    def test_channel_mark_ready_rejected_from_idle(
        channel: m.Grpc.Channel,
    ) -> None:
        """mark_ready requires a connecting channel; idle input fails."""
        tm.fail(channel.mark_ready())

    @staticmethod
    def test_channel_business_rules_pass_with_target(
        channel: m.Grpc.Channel,
    ) -> None:
        """A channel with a non-empty target validates successfully."""
        tm.ok(channel.validate_business_rules())

    @staticmethod
    def test_channel_business_rules_fail_without_target() -> None:
        """An empty target fails validation with a descriptive error."""
        channel = m.Grpc.Channel(target="", options={}, domain_events=[])
        tm.fail(channel.validate_business_rules(), has="cannot be empty")

    @staticmethod
    def test_channel_copy_with_overrides_target(channel: m.Grpc.Channel) -> None:
        """copy_with returns a new channel carrying the overridden target."""
        tm.that(
            tm.ok(channel.copy_with(target="127.0.0.1:8080")).target,
            eq="127.0.0.1:8080",
        )


class TestsFlextGrpcClientServiceStreamEntities:
    """Public-contract behavior of the gRPC client, service, and stream entities."""

    # ---- Client -----------------------------------------------------------

    @staticmethod
    def test_client_constructs_without_channel() -> None:
        """A client can be created without an attached channel."""
        tm.that(m.Grpc.Client(options={}, domain_events=[]).channel, none=True)

    @staticmethod
    def test_client_retains_attached_channel(channel: m.Grpc.Channel) -> None:
        """A channel passed at construction is exposed via the public field."""
        client = m.Grpc.Client(channel=channel, options={}, domain_events=[])
        tm.that(client.channel, eq=channel)

    @staticmethod
    def test_client_connect_to_attaches_channel_for_target() -> None:
        """connect_to yields a client whose channel points at the requested target."""
        client = m.Grpc.Client(options={}, domain_events=[])
        connected = tm.ok(client.connect_to("localhost:50051"))
        attached = tm.not_none(connected.channel)
        tm.that(attached.target, eq="localhost:50051")

    @staticmethod
    def test_client_business_rules_pass_with_valid_channel(
        channel: m.Grpc.Channel,
    ) -> None:
        """A client holding a valid channel validates successfully."""
        client = m.Grpc.Client(channel=channel, options={}, domain_events=[])
        tm.ok(client.validate_business_rules())

    @staticmethod
    def test_client_business_rules_fail_with_invalid_channel() -> None:
        """A client wrapping an invalid (empty-target) channel fails validation."""
        bad_channel = m.Grpc.Channel(target="", options={}, domain_events=[])
        client = m.Grpc.Client(channel=bad_channel, options={}, domain_events=[])
        tm.fail(client.validate_business_rules(), has="Invalid channel")

    # ---- Service ----------------------------------------------------------

    @staticmethod
    def test_service_exposes_name_and_methods() -> None:
        """Service surfaces its name and registered methods."""
        service = m.Grpc.Service(
            name="TestService", methods=["m1", "m2"], domain_events=[],
        )
        tm.that(service.name, eq="TestService")
        tm.that(list(service.methods), eq=["m1", "m2"])

    @staticmethod
    @pytest.mark.parametrize(
        ("name", "methods", "match"),
        [
            ("TestService", [], "methods cannot be empty"),
            ("", ["m1"], "name cannot be empty"),
            ("  ", ["m1"], "name cannot be empty"),
            ("S", [" "], "method cannot be empty"),
        ],
        ids=["empty-methods", "empty-name", "blank-name", "blank-method"],
    )
    def test_service_construction_rejects_invalid_name_or_methods(
        name: str, methods: list[str], match: str,
    ) -> None:
        """Service construction raises on empty/blank name or method entries."""
        with pytest.raises(ValueError, match=match):
            m.Grpc.Service(name=name, methods=methods, domain_events=[])

    @staticmethod
    def test_service_add_method_appends_and_is_queryable() -> None:
        """add_method returns a service exposing the new method via has_method."""
        service = m.Grpc.Service(name="S", methods=["m1"], domain_events=[])
        updated = tm.ok(service.add_method("m2"))
        tm.that(updated.has_method("m2"), eq=True)
        tm.that(service.has_method("m2"), eq=False)

    @staticmethod
    def test_service_add_method_rejects_duplicate() -> None:
        """Adding an already-registered method fails rather than duplicating it."""
        service = m.Grpc.Service(name="S", methods=["m1"], domain_events=[])
        tm.fail(service.add_method("m1"), has="Invalid method")

    # ---- GrpcStream -------------------------------------------------------

    @staticmethod
    def test_stream_exposes_identity_and_type() -> None:
        """GrpcStream surfaces its id, method name and stream type."""
        stream = m.Grpc.GrpcStream(
            unique_id="test_stream",
            method_name="test_method",
            stream_type=c.Grpc.GrpcOperations.UNARY,
            domain_events=[],
        )
        tm.that(stream.unique_id, eq="test_stream")
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    @staticmethod
    @pytest.mark.parametrize("method_name", ["", "   "], ids=["empty", "blank"])
    def test_stream_construction_rejects_empty_method_name(
        method_name: str,
    ) -> None:
        """GrpcStream requires a non-empty method_name."""
        with pytest.raises(ValueError, match="method_name cannot be empty"):
            m.Grpc.GrpcStream(
                unique_id="s",
                method_name=method_name,
                stream_type=c.Grpc.GrpcOperations.UNARY,
                domain_events=[],
            )
