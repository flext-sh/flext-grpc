"""Tests for public gRPC service components."""

from __future__ import annotations

from flext_tests import tm

from flext_grpc import FlextGrpc
from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
from flext_grpc.services.metrics import FlextGrpcMetrics
from tests.models import m


class TestsFlextGrpcServices:
    """Test public gRPC service components without legacy compat shims."""

    def test_connect_client_invalid_target_fails(self, grpc_facade: FlextGrpc) -> None:
        """Client connection should fail fast for an unreachable target."""
        tm.fail(grpc_facade.connect_client("127.0.0.1:1"))

    def test_create_stream(self, grpc_facade: FlextGrpc) -> None:
        """Stream creation uses the public facade contract."""
        tm.ok(grpc_facade.create_stream(method_name="test_method"))

    def test_execute_returns_settings(self, grpc_facade: FlextGrpc) -> None:
        """Execute returns the configured facade settings."""
        tm.ok(grpc_facade.execute())

    def test_connection_pool_cleanup(
        self, connection_pool: FlextGrpcConnectionPool.ConnectionPool
    ) -> None:
        """Connection pool cleanup succeeds even with no active channels."""
        tm.ok(connection_pool.cleanup())

    def test_metrics_collector(
        self, metrics_collector: FlextGrpcMetrics.MetricsCollector
    ) -> None:
        """Metrics collector records and exposes normalized payload values."""
        metrics_collector.record_metric("test_key", "test_value")
        tm.that(metrics_collector.metric("test_key"), eq="test_value")
        payload: m.Grpc.Payload = metrics_collector.all_metrics()
        tm.that(payload.values, has="test_key")
        tm.that(payload.values["test_key"], eq="test_value")
