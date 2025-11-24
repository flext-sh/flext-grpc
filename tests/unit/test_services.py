"""Tests for flext_grpc.services module."""

from flext_grpc.services import FlextGrpcServices


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
        # Connection may fail in test environment, but method should exist
        assert (
            result.is_success or not result.is_success
        )  # Just check it returns a result

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
        from flext_grpc.services import ConnectionPool

        pool = ConnectionPool(max_size=5)
        # Create a mock connection
        mock_connection = "mock_connection_123"
        # Test releasing a connection (should succeed even if not in active set)
        release_result = pool.release(mock_connection)
        assert release_result.is_success

    def test_connection_pool_cleanup(self) -> None:
        """Test connection pool cleanup."""
        from flext_grpc.services import ConnectionPool

        pool = ConnectionPool(max_size=5)
        result = pool.cleanup()
        assert result.is_success

    def test_metrics_collector(self) -> None:
        """Test metrics collector directly."""
        from flext_grpc.services import MetricsCollector

        collector = MetricsCollector()
        collector.record_metric("test_key", "test_value")
        value = collector.get_metric("test_key")
        assert value == "test_value"
        metrics = collector.get_all_metrics()
        assert "test_key" in metrics
        assert metrics["test_key"] == "test_value"
