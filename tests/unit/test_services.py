"""Tests for public gRPC service components."""

from __future__ import annotations

from flext_tests import tm

from flext_grpc import FlextGrpc, FlextGrpcConnectionPool, FlextGrpcMetrics
from tests import m


class TestsFlextGrpcServices:
    """Test public gRPC service components without legacy compat shims."""

    def test_connect_client_invalid_target_fails(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """Client connection should fail fast for an unreachable target."""
        result = grpc_facade.connect_client("127.0.0.1:1")
        tm.that(result.failure, eq=True)

    def test_create_stream(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """Stream creation uses the public facade contract."""
        result = grpc_facade.create_stream(method_name="test_method")
        tm.that(result.success, eq=True)

    def test_execute_returns_settings(
        self,
        grpc_facade: FlextGrpc,
    ) -> None:
        """Execute returns the configured facade settings."""
        result = grpc_facade.execute()
        tm.that(result.success, eq=True)

    def test_connection_pool_cleanup(
        self,
        connection_pool: FlextGrpcConnectionPool.ConnectionPool,
    ) -> None:
        """Connection pool cleanup succeeds even with no active channels."""
        result = connection_pool.cleanup()
        tm.that(result.success, eq=True)

    def test_metrics_collector(
        self,
        metrics_collector: FlextGrpcMetrics.MetricsCollector,
    ) -> None:
        """Metrics collector records and exposes normalized payload values."""
        metrics_collector.record_metric("test_key", "test_value")
        value = metrics_collector.metric("test_key")
        tm.that(value, eq="test_value")
        metrics_payload: m.Grpc.Payload = metrics_collector.all_metrics()
        tm.that(metrics_payload.values, has="test_key")
        tm.that(metrics_payload.values["test_key"], eq="test_value")
