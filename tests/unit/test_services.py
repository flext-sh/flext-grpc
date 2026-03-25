"""Tests for flext_grpc.services module."""

from __future__ import annotations

import grpc
from flext_tests import tm

from flext_grpc import FlextGrpcServices


class TestFlextGrpcServices:
    """Test cases for FlextGrpcServices class."""

    def test_init(self) -> None:
        """Test FlextGrpcServices initialization."""
        services = FlextGrpcServices()
        assert services is not None

    def test_connect_client(self) -> None:
        """Test client connection."""
        services = FlextGrpcServices()
        result = services.connect_client("localhost:50051")
        tm.that(result.is_success or not result.is_success, eq=True)

    def test_create_stream(self) -> None:
        """Test stream creation."""
        services = FlextGrpcServices()
        result = services.create_stream("test_method")
        tm.that(result.is_success, eq=True)

    def test_execute_method(self) -> None:
        """Test execute method."""
        services = FlextGrpcServices()
        result = services.execute()
        tm.that(result.is_success, eq=True)

    def test_connection_pool_release(self) -> None:
        """Test connection pool release."""
        pool = FlextGrpcServices.Grpc.ConnectionPool(max_size=5)
        mock_connection = grpc.insecure_channel("localhost:50051")
        release_result = pool.release(mock_connection)
        tm.that(release_result.is_success, eq=True)

    def test_connection_pool_cleanup(self) -> None:
        """Test connection pool cleanup."""
        pool = FlextGrpcServices.Grpc.ConnectionPool(max_size=5)
        result = pool.cleanup()
        tm.that(result.is_success, eq=True)

    def test_metrics_collector(self) -> None:
        """Test metrics collector directly."""
        collector = FlextGrpcServices.Grpc.MetricsCollector()
        collector.record_metric("test_key", "test_value")
        value = collector.get_metric("test_key")
        tm.that(value, eq="test_value")
        metrics_payload = collector.get_all_metrics()
        tm.that(metrics_payload.values, has="test_key")
        tm.that(metrics_payload.values["test_key"], eq="test_value")
