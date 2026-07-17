"""Behavioral tests for public gRPC service components.

Every test asserts observable public contract: ``r[T]`` outcomes, public model
state, and documented edge-case behavior. No private attribute access, no
internal-collaborator spying, no line-coverage pokes.
"""

from __future__ import annotations

from socket import AF_INET, SOCK_STREAM, socket
from typing import TYPE_CHECKING

import pytest
from flext_tests import tm

from flext_grpc import FlextGrpc, c, t

if TYPE_CHECKING:
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.services.metrics import FlextGrpcMetrics


class TestsFlextGrpcServices:
    """Public contract of FlextGrpc facade and its service components."""

    class TestsRuntimeRoundTrip:
        """Real grpcio round trips through the public facade."""

        def test_echo_and_health_round_trip(self, grpc_facade: FlextGrpc) -> None:
            """Serve and call both generated RPCs over a loopback channel."""
            with socket(AF_INET, SOCK_STREAM) as available_port:
                available_port.bind(("127.0.0.1", 0))
                port = available_port.getsockname()[1]

            server_result = grpc_facade.create_server(host="127.0.0.1", port=port)
            tm.ok(server_result)
            server = server_result.unwrap()
            start_result = grpc_facade.start_server(server)
            tm.ok(start_result)
            started_server = start_result.unwrap()
            try:
                client_result = grpc_facade.connect_client(f"127.0.0.1:{port}")
                tm.ok(client_result)
                client = client_result.unwrap()
                try:
                    echo_result = grpc_facade.make_call(
                        client,
                        c.Grpc.ServiceMethod.ECHO.value,
                        {"message": "flext-round-trip"},
                    )
                    tm.ok(echo_result)
                    echo = echo_result.unwrap()
                    tm.that(echo.values["message"], eq="flext-round-trip")
                    tm.that(echo.values["server_id"], eq=f"127.0.0.1:{port}")

                    health_result = grpc_facade.make_call(
                        client,
                        c.Grpc.ServiceMethod.HEALTH_CHECK.value,
                        {"service": "FlextGrpcService"},
                    )
                    tm.ok(health_result)
                    health = health_result.unwrap()
                    tm.that(health.values["status"], eq="SERVING")
                finally:
                    tm.ok(grpc_facade.disconnect_client(client))
            finally:
                tm.ok(grpc_facade.stop_server(started_server))

    # -- Facade: create_stream -------------------------------------------

    def test_create_stream_succeeds_and_carries_method_name(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """create_stream returns a success carrying the requested method name."""
        result = grpc_facade.create_stream(method_name="test_method")

        tm.ok(result)
        stream = result.unwrap()
        tm.that(stream.method_name, eq="test_method")

    def test_create_stream_defaults_are_applied(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """create_stream applies documented defaults when no args are passed."""
        stream = grpc_facade.create_stream().unwrap()

        tm.that(stream.method_name, eq="DefaultMethod")
        tm.that(stream.stream_type.value, eq="unary")

    def test_close_stream_returns_same_stream_identity(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """close_stream succeeds and returns a stream with the same method name."""
        stream = grpc_facade.create_stream(method_name="to_close").unwrap()

        closed = grpc_facade.close_stream(stream)

        tm.ok(closed)
        tm.that(closed.unwrap().method_name, eq="to_close")

    # -- Facade: execute --------------------------------------------------

    def test_execute_returns_configured_settings(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """Execute succeeds and yields the facade's settings object."""
        result = grpc_facade.execute()

        tm.ok(result)
        tm.that(result.unwrap(), none=False)

    # -- Facade: connect_client ------------------------------------------

    def test_connect_client_fails_fast_for_unreachable_target(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """Connecting to an unreachable target yields a failure with an error."""
        result = grpc_facade.connect_client("127.0.0.1:1")

        tm.fail(result)
        assert result.error

    # -- Facade: validate_target -----------------------------------------

    @pytest.mark.parametrize(
        ("target", "expected"),
        [
            ("localhost:50051", True),
            ("127.0.0.1:1", True),
            ("host", False),
            ("", False),
            (" ", False),
            ("a:b", False),
            ("host:70000", False),
        ],
    )
    def test_validate_target_recognizes_host_port_form(
        self,
        grpc_facade: FlextGrpc,
        target: str,
        expected: bool,
    ) -> None:
        """validate_target accepts only well-formed host:port within range."""
        assert grpc_facade.validate_target(target) is expected

    # -- Facade: parse_address -------------------------------------------

    def test_parse_address_splits_host_and_port(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """parse_address returns the (host, port) tuple for a valid address."""
        result = grpc_facade.parse_address("localhost:50051")

        tm.ok(result)
        tm.that(result.unwrap(), eq=("localhost", 50051))

    @pytest.mark.parametrize("address", ["host", "bad:x", ""])
    def test_parse_address_fails_for_malformed_input(
        self,
        grpc_facade: FlextGrpc,
        address: str,
    ) -> None:
        """parse_address fails with a descriptive error for malformed input."""
        result = grpc_facade.parse_address(address)

        tm.fail(result)
        tm.that((result.error or ""), has="Invalid address")

    # -- ConnectionPool ---------------------------------------------------

    def test_connection_pool_cleanup_succeeds_when_empty(
        self,
        connection_pool: FlextGrpcConnectionPool.ConnectionPool,
    ) -> None:
        """Cleanup succeeds and reports True even with no active channels."""
        result = connection_pool.cleanup()

        tm.ok(result)
        tm.that(result.unwrap(), eq=True)

    def test_connection_pool_acquire_on_empty_pool_fails_not_found(
        self,
        connection_pool: FlextGrpcConnectionPool.ConnectionPool,
    ) -> None:
        """Acquire on an empty pool fails with a not-found error code."""
        result = connection_pool.acquire()

        tm.fail(result)
        tm.that(result.error_code, eq="NOT_FOUND_ERROR")

    def test_connection_pool_cleanup_is_idempotent(
        self,
        connection_pool: FlextGrpcConnectionPool.ConnectionPool,
    ) -> None:
        """Repeated cleanup calls keep succeeding (idempotent invariant)."""
        tm.ok(connection_pool.cleanup())
        tm.ok(connection_pool.cleanup())

    # -- MetricsCollector -------------------------------------------------

    def test_metrics_record_then_retrieve_roundtrip(
        self,
        metrics_collector: FlextGrpcMetrics.MetricsCollector,
    ) -> None:
        """A recorded metric is retrievable by key and exposed in the payload."""
        metrics_collector.record_metric("test_key", "test_value")

        tm.that(metrics_collector.metric("test_key"), eq="test_value")
        payload = metrics_collector.all_metrics()
        tm.that(payload.values["test_key"], eq="test_value")

    def test_metrics_unknown_key_returns_none(
        self,
        metrics_collector: FlextGrpcMetrics.MetricsCollector,
    ) -> None:
        """Retrieving an unrecorded key returns None."""
        tm.that(metrics_collector.metric("absent"), none=True)

    @pytest.mark.parametrize(
        ("value", "expected"),
        [
            ("v", "v"),
            (5, 5),
            (True, True),
            (None, ""),
            ([1, 2], "[1, 2]"),
        ],
    )
    def test_metrics_value_normalization(
        self,
        metrics_collector: FlextGrpcMetrics.MetricsCollector,
        value: t.JsonValue | None,
        expected: t.JsonValue,
    ) -> None:
        """record_metric normalizes: None -> '', primitives pass, else str()."""
        metrics_collector.record_metric("k", value)

        tm.that(metrics_collector.metric("k"), eq=expected)

    def test_metrics_all_metrics_returns_independent_snapshot(
        self,
        metrics_collector: FlextGrpcMetrics.MetricsCollector,
    ) -> None:
        """all_metrics returns a snapshot that later records do not mutate."""
        metrics_collector.record_metric("first", "1")
        snapshot = metrics_collector.all_metrics()

        metrics_collector.record_metric("second", "2")

        tm.that(snapshot.values, lacks="second")
        tm.that(snapshot.values["first"], eq="1")
