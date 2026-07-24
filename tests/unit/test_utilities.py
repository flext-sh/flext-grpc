"""Behavioral tests for the flext_grpc utilities public contract.

These tests exercise only the observable public behavior of
``FlextGrpcUtilities.Grpc`` (exposed here via the ``u`` test facade):
return values, ``r[T]`` outcomes, raised exceptions and public model
state. No private attributes, internal collaborators or implementation
details are inspected.
"""

from __future__ import annotations

import pytest
from flext_tests import tm

from tests import p, u


class TestsFlextGrpcUtilitiesUnit:
    """Public-contract behavior of the gRPC utility namespace."""

    # ------------------------------------------------------------------
    # Facade instantiation
    # ------------------------------------------------------------------

    def test_facade_exposes_grpc_namespace(self) -> None:
        # Coord-note (settings/facade lane): the utilities facade is a namespace,
        # not a bare-instantiable object (FlextUtilitiesLogging now requires name);
        # assert the real contract — the Grpc namespace + its static helpers exist.
        """The utilities facade exposes a usable ``Grpc`` helper namespace."""
        tm.that(u.Grpc, none=False)
        tm.that(callable(u.Grpc.parse_address), eq=True)

    # ------------------------------------------------------------------
    # parse_address / parse_target
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        ("address", "expected_host", "expected_port"),
        [
            ("localhost:50051", "localhost", 50051),
            ("127.0.0.1:1", "127.0.0.1", 1),
            ("example.com:65535", "example.com", 65535),
        ],
    )
    def test_parse_address_returns_host_and_int_port(
        self, address: str, expected_host: str, expected_port: int
    ) -> None:
        """A valid address parses into a (host, int-port) pair."""
        host, port = u.Grpc.parse_address(address)
        tm.that(host, eq=expected_host)
        tm.that(port, eq=expected_port)
        tm.that(port, is_=int)

    def test_parse_address_matches_parse_target(self) -> None:
        """parse_address and parse_target agree on the same valid input."""
        tm.that(
            u.Grpc.parse_address("localhost:50051"),
            eq=u.Grpc.parse_target("localhost:50051"),
        )

    @pytest.mark.parametrize(
        "bad_address", ["nocolon", "", "host:", ":50051", "host:notaport", "host:0"]
    )
    def test_parse_address_rejects_invalid_target(self, bad_address: str) -> None:
        """Parsing an invalid target raises ValueError naming the target."""
        with pytest.raises(ValueError, match="Invalid gRPC target"):
            u.Grpc.parse_address(bad_address)

    def test_format_then_parse_is_round_trip(self) -> None:
        """format_address and parse_address are inverse operations."""
        formatted = u.Grpc.format_address("localhost", 50051)
        tm.that(u.Grpc.parse_address(formatted), eq=("localhost", 50051))

    # ------------------------------------------------------------------
    # validate_target
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        ("target", "expected"),
        [
            ("localhost:50051", True),
            ("127.0.0.1:1", True),
            ("host:65535", True),
            ("host:65536", False),
            ("host:0", False),
            ("host:", False),
            (":50051", False),
            ("nocolon", False),
            ("", False),
        ],
    )
    def test_validate_target_reflects_host_port_validity(
        self, target: str, expected: bool
    ) -> None:
        """validate_target accepts only well-formed host:port strings."""
        tm.that(u.Grpc.validate_target(target), eq=expected)

    # ------------------------------------------------------------------
    # validate_port / validate_host
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        ("port", "expected"),
        [
            (1, True),
            (50051, True),
            (65535, True),
            (0, False),
            (65536, False),
            (-1, False),
        ],
    )
    def test_validate_port_enforces_inclusive_range(
        self, port: int, expected: bool
    ) -> None:
        """Ports are valid only within the inclusive 1..65535 range."""
        tm.that(u.Grpc.validate_port(port), eq=expected)

    @pytest.mark.parametrize(
        ("host", "expected"),
        [("localhost", True), ("127.0.0.1", True), ("", False), ("   ", False)],
    )
    def test_validate_host_requires_non_blank(self, host: str, expected: bool) -> None:
        """A host is valid only when it is non-empty after stripping."""
        tm.that(u.Grpc.validate_host(host), eq=expected)

    # ------------------------------------------------------------------
    # format_address
    # ------------------------------------------------------------------

    def test_format_address_joins_host_and_port(self) -> None:
        """format_address renders the canonical host:port form."""
        tm.that(u.Grpc.format_address("localhost", 50051), eq="localhost:50051")

    # ------------------------------------------------------------------
    # channel_state_name / server_state_name
    # ------------------------------------------------------------------

    @pytest.mark.parametrize(
        ("state", "expected"),
        [
            ("ready", "ready"),
            ("IDLE", "idle"),
            ("Ready", "ready"),
            ("bogus", "unknown"),
        ],
    )
    def test_channel_state_name_normalizes_known_states(
        self, state: str, expected: str
    ) -> None:
        """Known channel states normalize to lowercase; others map to unknown."""
        tm.that(u.Grpc.channel_state_name(state), eq=expected)

    @pytest.mark.parametrize(
        ("state", "expected"),
        [
            ("running", "running"),
            ("STOPPED", "stopped"),
            ("Starting", "starting"),
            ("nope", "unknown"),
        ],
    )
    def test_server_state_name_normalizes_known_states(
        self, state: str, expected: str
    ) -> None:
        """Known server states normalize to lowercase; others map to unknown."""
        tm.that(u.Grpc.server_state_name(state), eq=expected)

    # ------------------------------------------------------------------
    # system_info
    # ------------------------------------------------------------------

    def test_system_info_exposes_network_defaults_and_states(self) -> None:
        """system_info returns the documented public configuration mapping."""
        info = u.Grpc.system_info()
        tm.that(info, is_=dict)
        tm.that(
            info,
            keys=[
                "default_host",
                "default_port",
                "min_port",
                "max_port",
                "channel_states",
                "server_states",
            ],
        )
        tm.that(info["min_port"], eq=1)
        tm.that(info["max_port"], eq=65535)

    # ------------------------------------------------------------------
    # Entity factories — success paths (r[T] outcomes + public state)
    # ------------------------------------------------------------------

    def test_create_channel_entity_carries_target(self) -> None:
        """A created channel entity exposes the requested target."""
        channel: p.Grpc.Channel = tm.ok(u.Grpc.create_channel_entity("localhost:50051"))
        tm.that(channel.target, eq="localhost:50051")

    def test_create_client_entity_wraps_channel_with_target(self) -> None:
        """A created client entity is backed by a channel on the same target."""
        client: p.Grpc.Client = tm.ok(u.Grpc.create_client_entity("localhost:50051"))
        channel = tm.not_none(client.channel)
        tm.that(channel.target, eq="localhost:50051")

    def test_create_server_entity_carries_host_and_port(self) -> None:
        """A created server entity exposes the requested host and port."""
        server: p.Grpc.Server = tm.ok(u.Grpc.create_server_entity("localhost", 50051))
        tm.that(server.host, eq="localhost")
        tm.that(server.port, eq=50051)

    def test_create_service_entity_defaults_to_minimal_method_set(self) -> None:
        """A service created without methods gets a minimal valid method set."""
        service: p.Grpc.Service = tm.ok(u.Grpc.create_service_entity("TestService"))
        tm.that(service.name, eq="TestService")
        tm.that(service.methods, empty=False)

    def test_create_service_entity_preserves_supplied_methods(self) -> None:
        """Explicit methods are preserved on the created service entity."""
        service: p.Grpc.Service = tm.ok(
            u.Grpc.create_service_entity("Svc", methods=["A", "B"])
        )
        tm.that(service.methods, eq=["A", "B"])

    def test_create_stream_entity_carries_method_and_type(self) -> None:
        """A created stream entity exposes its method name and stream type."""
        stream: p.Grpc.GrpcStream = tm.ok(
            u.Grpc.create_stream_entity("test_method", "unary")
        )
        tm.that(stream.method_name, eq="test_method")
        tm.that(stream.stream_type, eq="unary")

    # ------------------------------------------------------------------
    # Entity factories — error paths
    # ------------------------------------------------------------------

    @pytest.mark.parametrize("bad_port", [0, 65536])
    def test_create_server_entity_rejects_out_of_range_port(
        self, bad_port: int
    ) -> None:
        """An out-of-range port yields a failed result (not an invented entity)."""
        tm.fail(u.Grpc.create_server_entity("localhost", bad_port))

    def test_create_stream_entity_rejects_unknown_stream_type(self) -> None:
        """An unsupported stream type raises ValueError from the enum contract."""
        with pytest.raises(ValueError, match="GrpcOperations"):
            u.Grpc.create_stream_entity("m", "server_streaming")
