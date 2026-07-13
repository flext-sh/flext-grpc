"""Behavioral tests for flext_grpc.entities (gRPC domain models)."""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import c, m


class TestsFlextGrpcEntities:
    """Public-contract behavior of the gRPC entity models."""

    @pytest.fixture
    def channel(self) -> m.Grpc.Channel:
        """Idle channel bound to a concrete target."""
        return m.Grpc.Channel(
            target="localhost:50051",
            state=c.Grpc.ChannelState.IDLE,
            options={},
            domain_events=[],
        )

    @pytest.fixture
    def server(self) -> m.Grpc.Server:
        """Return a stopped server with no registered services."""
        return m.Grpc.Server(
            host="localhost",
            port=50051,
            services=[],
            domain_events=[],
        )

    # ---- Server -----------------------------------------------------------

    def test_server_exposes_constructor_field_state(self) -> None:
        """Server surfaces host, port and explicit max_workers as public state."""
        server = m.Grpc.Server(
            host="localhost",
            port=50051,
            max_workers=10,
            services=[],
            domain_events=[],
        )
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)
        tm.that(server.max_workers, eq=10)

    def test_server_defaults_max_workers_when_omitted(self) -> None:
        """Omitting max_workers yields the documented default of 10."""
        server = m.Grpc.Server(
            host="localhost", port=50051, services=[], domain_events=[]
        )
        tm.that(server.max_workers, eq=10)

    def test_server_lifecycle_transitions_through_running_and_stopped(
        self,
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

    def test_server_start_does_not_mutate_original(self, server: m.Grpc.Server) -> None:
        """Transitions return a new entity, leaving the source stopped (immutability)."""
        tm.ok(server.start())
        tm.that(server.state, eq="stopped")

    def test_server_mark_stopped_rejected_from_stopped(
        self,
        server: m.Grpc.Server,
    ) -> None:
        """mark_stopped from an already-stopped state fails with an explanatory error."""
        tm.fail(server.mark_stopped(), has="Cannot mark stopped")

    def test_server_add_service_appends_to_public_services(
        self,
        server: m.Grpc.Server,
    ) -> None:
        """add_service returns a server whose services include the added entry."""
        service = object()
        updated = tm.ok(server.add_service(service))
        tm.that(list(updated.services), eq=[service])
        tm.that(list(server.services), eq=[])

    def test_server_business_rules_reject_empty_host(self) -> None:
        """validate_business_rules fails for a server bound to an empty host."""
        server = m.Grpc.Server(host="", port=50051, services=[], domain_events=[])
        tm.fail(server.validate_business_rules(), has="host cannot be empty")

    @pytest.mark.parametrize(
        ("port", "max_workers"),
        [(70000, 10), (50051, 0)],
        ids=["out-of-range-port", "zero-workers"],
    )
    def test_server_construction_rejects_out_of_range_numeric_fields(
        self,
        port: int,
        max_workers: int,
    ) -> None:
        """Port and worker-count bounds are enforced at construction time."""
        with pytest.raises(ValueError):
            m.Grpc.Server(
                host="localhost",
                port=port,
                max_workers=max_workers,
                services=[],
                domain_events=[],
            )

    def test_server_business_rules_pass_for_valid_config(
        self,
        server: m.Grpc.Server,
    ) -> None:
        """A well-formed server validates successfully."""
        tm.ok(server.validate_business_rules())

    # ---- Channel ----------------------------------------------------------

    def test_channel_exposes_target(self, channel: m.Grpc.Channel) -> None:
        """Channel surfaces its configured target address."""
        tm.that(channel.target, eq="localhost:50051")

    def test_channel_connect_transitions_idle_to_connecting(
        self,
        channel: m.Grpc.Channel,
    ) -> None:
        """Connect moves an idle channel to the connecting state."""
        tm.that(tm.ok(channel.connect()).state, eq="connecting")

    def test_channel_reaches_ready_then_returns_to_idle(
        self,
        channel: m.Grpc.Channel,
    ) -> None:
        """Connect -> mark_ready -> disconnect drives the readiness cycle."""
        ready = tm.ok(tm.ok(channel.connect()).mark_ready())
        tm.that(ready.state, eq="ready")
        tm.that(ready.ready(), eq=True)
        tm.that(tm.ok(ready.disconnect()).state, eq="idle")

    def test_channel_mark_ready_rejected_from_idle(
        self,
        channel: m.Grpc.Channel,
    ) -> None:
        """mark_ready requires a connecting channel; idle input fails."""
        tm.fail(channel.mark_ready())

    def test_channel_business_rules_pass_with_target(
        self,
        channel: m.Grpc.Channel,
    ) -> None:
        """A channel with a non-empty target validates successfully."""
        tm.ok(channel.validate_business_rules())

    def test_channel_business_rules_fail_without_target(self) -> None:
        """An empty target fails validation with a descriptive error."""
        channel = m.Grpc.Channel(target="", options={}, domain_events=[])
        tm.fail(channel.validate_business_rules(), has="cannot be empty")

    def test_channel_copy_with_overrides_target(
        self,
        channel: m.Grpc.Channel,
    ) -> None:
        """copy_with returns a new channel carrying the overridden target."""
        tm.that(
            tm.ok(channel.copy_with(target="127.0.0.1:8080")).target,
            eq="127.0.0.1:8080",
        )

    # ---- Client -----------------------------------------------------------

    def test_client_constructs_without_channel(self) -> None:
        """A client can be created without an attached channel."""
        tm.that(m.Grpc.Client(options={}, domain_events=[]).channel, none=True)

    def test_client_retains_attached_channel(
        self,
        channel: m.Grpc.Channel,
    ) -> None:
        """A channel passed at construction is exposed via the public field."""
        client = m.Grpc.Client(channel=channel, options={}, domain_events=[])
        tm.that(client.channel, eq=channel)

    def test_client_connect_to_attaches_channel_for_target(self) -> None:
        """connect_to yields a client whose channel points at the requested target."""
        client = m.Grpc.Client(options={}, domain_events=[])
        connected = tm.ok(client.connect_to("localhost:50051"))
        attached = connected.channel
        assert attached is not None
        tm.that(attached.target, eq="localhost:50051")

    def test_client_business_rules_pass_with_valid_channel(
        self,
        channel: m.Grpc.Channel,
    ) -> None:
        """A client holding a valid channel validates successfully."""
        client = m.Grpc.Client(channel=channel, options={}, domain_events=[])
        tm.ok(client.validate_business_rules())

    def test_client_business_rules_fail_with_invalid_channel(self) -> None:
        """A client wrapping an invalid (empty-target) channel fails validation."""
        bad_channel = m.Grpc.Channel(target="", options={}, domain_events=[])
        client = m.Grpc.Client(channel=bad_channel, options={}, domain_events=[])
        tm.fail(client.validate_business_rules(), has="Invalid channel")

    # ---- Service ----------------------------------------------------------

    def test_service_exposes_name_and_methods(self) -> None:
        """Service surfaces its name and registered methods."""
        service = m.Grpc.Service(
            name="TestService", methods=["m1", "m2"], domain_events=[]
        )
        tm.that(service.name, eq="TestService")
        tm.that(list(service.methods), eq=["m1", "m2"])

    @pytest.mark.parametrize(
        ("name", "methods"),
        [("TestService", []), ("", ["m1"]), ("  ", ["m1"]), ("S", [" "])],
        ids=["empty-methods", "empty-name", "blank-name", "blank-method"],
    )
    def test_service_construction_rejects_invalid_name_or_methods(
        self,
        name: str,
        methods: list[str],
    ) -> None:
        """Service construction raises on empty/blank name or method entries."""
        with pytest.raises(ValueError):
            m.Grpc.Service(name=name, methods=methods, domain_events=[])

    def test_service_add_method_appends_and_is_queryable(self) -> None:
        """add_method returns a service exposing the new method via has_method."""
        service = m.Grpc.Service(name="S", methods=["m1"], domain_events=[])
        updated = tm.ok(service.add_method("m2"))
        tm.that(updated.has_method("m2"), eq=True)
        tm.that(service.has_method("m2"), eq=False)

    def test_service_add_method_rejects_duplicate(self) -> None:
        """Adding an already-registered method fails rather than duplicating it."""
        service = m.Grpc.Service(name="S", methods=["m1"], domain_events=[])
        tm.fail(service.add_method("m1"), has="Invalid method")

    # ---- GrpcStream -------------------------------------------------------

    def test_stream_exposes_identity_and_type(self) -> None:
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

    @pytest.mark.parametrize("method_name", ["", "   "], ids=["empty", "blank"])
    def test_stream_construction_rejects_empty_method_name(
        self,
        method_name: str,
    ) -> None:
        """GrpcStream requires a non-empty method_name."""
        with pytest.raises(ValueError):
            m.Grpc.GrpcStream(
                unique_id="s",
                method_name=method_name,
                stream_type=c.Grpc.GrpcOperations.UNARY,
                domain_events=[],
            )
