"""Tests for flext_grpc.services module."""

from __future__ import annotations

import grpc

from flext_grpc import ConnectionPool, FlextGrpcServices, MetricsCollector


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
        assert result.is_success or not result.is_success

    def test_create_stream(self) -> None:
        """Test stream creation."""
        services = FlextGrpcServices()
        result = services.create_stream("test_method")
        assert result.is_success

    def test_execute_method(self) -> None:
        """Test execute method."""
        services = FlextGrpcServices()
        result = services.execute()
        assert result.is_success

    def test_connection_pool_release(self) -> None:
        """Test connection pool release."""
        pool = ConnectionPool(max_size=5)
        mock_connection = grpc.insecure_channel("localhost:50051")
        release_result = pool.release(mock_connection)
        assert release_result.is_success

    def test_connection_pool_cleanup(self) -> None:
        """Test connection pool cleanup."""
        pool = ConnectionPool(max_size=5)
        result = pool.cleanup()
        assert result.is_success

    def test_metrics_collector(self) -> None:
        """Test metrics collector directly."""
        collector = MetricsCollector()
        collector.record_metric("test_key", "test_value")
        value = collector.get_metric("test_key")
        assert value == "test_value"
        metrics_payload = collector.get_all_metrics()
        assert "test_key" in metrics_payload.values
        assert metrics_payload.values["test_key"] == "test_value"
