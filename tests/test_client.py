"""Real tests for gRPC client functionality."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import grpc
import pytest

# Mock the proto imports
with patch.dict("sys.modules", {
    "flext_grpc.proto": MagicMock(),
    "flext_grpc.proto.flext_pb2": MagicMock(),
    "flext_grpc.proto.flext_pb2_grpc": MagicMock(),
}):
    from flext_grpc.client import FlextGRPCClient, ConnectionPool


class TestFlextGRPCClient:
    """Test cases for gRPC client."""

    @pytest.fixture
    def mock_channel(self) -> AsyncMock:
        """Create a mock gRPC channel."""
        return AsyncMock()

    @pytest.fixture
    def mock_stub(self) -> MagicMock:
        """Create a mock gRPC stub."""
        return MagicMock()

    @pytest.fixture
    def client(self, mock_channel: AsyncMock, mock_stub: MagicMock) -> FlextGRPCClient:
        """Create a client instance with mocked dependencies."""
        with patch("grpc.aio.insecure_channel", return_value=mock_channel):
            with patch("flext_grpc.proto.flext_pb2_grpc.FlextServiceStub", return_value=mock_stub):
                client = FlextGRPCClient(
                    host="localhost",
                    port=50051,
                )
                client._stub = mock_stub
                return client

    def test_client_initialization(self) -> None:
        """Test client initialization."""
        client = FlextGRPCClient(
            host="localhost",
            port=50051,
            timeout=30,
        )
        
        assert client.host == "localhost"
        assert client.port == 50051
        assert client.timeout == 30
        assert client.address == "localhost:50051"

    @pytest.mark.asyncio
    async def test_health_check(self, client: FlextGRPCClient, mock_stub: MagicMock) -> None:
        """Test health check call."""
        # Mock response
        mock_response = MagicMock()
        mock_response.status = "SERVING"
        mock_stub.HealthCheck.return_value = mock_response
        
        # Call health check
        result = await client.health_check()
        
        # Verify
        assert result["status"] == "SERVING"
        mock_stub.HealthCheck.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_pipeline(self, client: FlextGRPCClient, mock_stub: MagicMock) -> None:
        """Test pipeline creation."""
        # Mock response
        mock_response = MagicMock()
        mock_response.pipeline_id = "pipeline-123"
        mock_response.created_at = "2025-01-01T00:00:00Z"
        mock_stub.CreatePipeline.return_value = mock_response
        
        # Call create pipeline
        result = await client.create_pipeline(
            name="test-pipeline",
            pipeline_type="DATABASE_SYNC",
            config={"tap": "tap-postgres", "target": "target-snowflake"},
        )
        
        # Verify
        assert result["pipeline_id"] == "pipeline-123"
        mock_stub.CreatePipeline.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_pipelines(self, client: FlextGRPCClient, mock_stub: MagicMock) -> None:
        """Test listing pipelines."""
        # Mock response
        mock_pipeline1 = MagicMock()
        mock_pipeline1.id = "p1"
        mock_pipeline1.name = "Pipeline 1"
        
        mock_pipeline2 = MagicMock()
        mock_pipeline2.id = "p2"
        mock_pipeline2.name = "Pipeline 2"
        
        mock_response = MagicMock()
        mock_response.pipelines = [mock_pipeline1, mock_pipeline2]
        mock_response.next_page_token = ""
        mock_stub.ListPipelines.return_value = mock_response
        
        # Call list pipelines
        result = await client.list_pipelines(page_size=10)
        
        # Verify
        assert len(result["pipelines"]) == 2
        assert result["pipelines"][0]["id"] == "p1"
        assert result["pipelines"][1]["id"] == "p2"

    @pytest.mark.asyncio
    async def test_execute_pipeline(self, client: FlextGRPCClient, mock_stub: MagicMock) -> None:
        """Test pipeline execution."""
        # Mock response
        mock_response = MagicMock()
        mock_response.execution_id = "exec-456"
        mock_response.status = "RUNNING"
        mock_stub.ExecutePipeline.return_value = mock_response
        
        # Call execute pipeline
        result = await client.execute_pipeline(
            pipeline_id="pipeline-123",
            parameters={"full_refresh": True},
        )
        
        # Verify
        assert result["execution_id"] == "exec-456"
        assert result["status"] == "RUNNING"

    @pytest.mark.asyncio
    async def test_error_handling(self, client: FlextGRPCClient, mock_stub: MagicMock) -> None:
        """Test error handling."""
        # Mock gRPC error
        mock_stub.GetPipeline.side_effect = grpc.aio.AioRpcError(
            code=grpc.StatusCode.NOT_FOUND,
            details="Pipeline not found",
        )
        
        # Call should raise exception
        with pytest.raises(grpc.aio.AioRpcError) as exc_info:
            await client.get_pipeline("non-existent")
        
        assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

    @pytest.mark.asyncio
    async def test_timeout_handling(self, client: FlextGRPCClient, mock_stub: MagicMock) -> None:
        """Test timeout handling."""
        # Mock timeout
        mock_stub.CreatePipeline.side_effect = asyncio.TimeoutError()
        
        # Call should raise timeout
        with pytest.raises(asyncio.TimeoutError):
            await client.create_pipeline(
                name="timeout-test",
                pipeline_type="DATABASE_SYNC",
                config={},
            )

    def test_client_with_tls(self) -> None:
        """Test client with TLS configuration."""
        client = FlextGRPCClient(
            host="secure.example.com",
            port=443,
            tls_enabled=True,
            tls_ca_cert="/path/to/ca.pem",
        )
        
        assert client.tls_enabled
        assert client.tls_ca_cert == "/path/to/ca.pem"

    def test_client_with_auth(self) -> None:
        """Test client with authentication."""
        client = FlextGRPCClient(
            host="localhost",
            port=50051,
            auth_token="Bearer eyJ0eXAiOiJKV1Q...",
        )
        
        assert client.auth_token == "Bearer eyJ0eXAiOiJKV1Q..."


class TestConnectionPool:
    """Test gRPC connection pooling."""

    def test_pool_initialization(self) -> None:
        """Test connection pool initialization."""
        pool = ConnectionPool(
            address="localhost:50051",
            max_connections=10,
            min_connections=2,
        )
        
        assert pool.address == "localhost:50051"
        assert pool.max_connections == 10
        assert pool.min_connections == 2
        assert pool.active_connections == 0

    @pytest.mark.asyncio
    async def test_acquire_release_connection(self) -> None:
        """Test acquiring and releasing connections."""
        pool = ConnectionPool(
            address="localhost:50051",
            max_connections=5,
        )
        
        # Mock channel creation
        mock_channel = AsyncMock()
        with patch("grpc.aio.insecure_channel", return_value=mock_channel):
            # Acquire connection
            conn = await pool.acquire()
            assert conn is not None
            assert pool.active_connections == 1
            
            # Release connection
            await pool.release(conn)
            assert pool.active_connections == 0

    @pytest.mark.asyncio
    async def test_connection_limit(self) -> None:
        """Test connection pool limits."""
        pool = ConnectionPool(
            address="localhost:50051",
            max_connections=2,
        )
        
        mock_channels = [AsyncMock() for _ in range(3)]
        with patch("grpc.aio.insecure_channel", side_effect=mock_channels):
            # Acquire max connections
            conn1 = await pool.acquire()
            conn2 = await pool.acquire()
            
            assert pool.active_connections == 2
            
            # Try to acquire one more (should wait or fail)
            with pytest.raises(asyncio.TimeoutError):
                await asyncio.wait_for(pool.acquire(), timeout=0.1)

    @pytest.mark.asyncio
    async def test_connection_health_check(self) -> None:
        """Test connection health checking."""
        pool = ConnectionPool(
            address="localhost:50051",
            health_check_interval=1,
        )
        
        # Mock unhealthy connection
        mock_channel = AsyncMock()
        mock_channel.get_state.return_value = grpc.ChannelConnectivity.TRANSIENT_FAILURE
        
        with patch("grpc.aio.insecure_channel", return_value=mock_channel):
            conn = await pool.acquire()
            
            # Check health
            is_healthy = await pool.is_healthy(conn)
            assert not is_healthy


class TestClientRetry:
    """Test client retry logic."""

    @pytest.mark.asyncio
    async def test_retry_on_transient_failure(self) -> None:
        """Test retry on transient failures."""
        client = FlextGRPCClient(
            host="localhost",
            port=50051,
            max_retries=3,
            retry_delay=0.1,
        )
        
        # Mock stub that fails twice then succeeds
        mock_stub = MagicMock()
        mock_response = MagicMock(pipeline_id="success")
        mock_stub.CreatePipeline.side_effect = [
            grpc.aio.AioRpcError(code=grpc.StatusCode.UNAVAILABLE),
            grpc.aio.AioRpcError(code=grpc.StatusCode.UNAVAILABLE),
            mock_response,
        ]
        
        client._stub = mock_stub
        
        # Should succeed after retries
        result = await client.create_pipeline(
            name="retry-test",
            pipeline_type="DATABASE_SYNC",
            config={},
        )
        
        assert result["pipeline_id"] == "success"
        assert mock_stub.CreatePipeline.call_count == 3

    @pytest.mark.asyncio
    async def test_no_retry_on_permanent_failure(self) -> None:
        """Test no retry on permanent failures."""
        client = FlextGRPCClient(
            host="localhost",
            port=50051,
            max_retries=3,
        )
        
        # Mock stub that returns permanent error
        mock_stub = MagicMock()
        mock_stub.GetPipeline.side_effect = grpc.aio.AioRpcError(
            code=grpc.StatusCode.NOT_FOUND,
            details="Pipeline not found",
        )
        
        client._stub = mock_stub
        
        # Should fail immediately without retries
        with pytest.raises(grpc.aio.AioRpcError):
            await client.get_pipeline("non-existent")
        
        # Should only be called once (no retries)
        assert mock_stub.GetPipeline.call_count == 1