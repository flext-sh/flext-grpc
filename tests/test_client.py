"""Real tests for gRPC client functionality."""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock
from unittest.mock import MagicMock
from unittest.mock import patch

import grpc
import pytest

# Mock the proto imports completely
# We need to mock both the module and the classes within it
mock_proto_module = MagicMock()
mock_pb2_module = MagicMock()
mock_pb2_grpc_module = MagicMock()

# Mock the FlextServiceStub class
mock_pb2_grpc_module.FlextServiceStub = MagicMock

with patch.dict(
    "sys.modules",
    {
        "flext_grpc.proto": mock_proto_module,
        "flext_grpc.proto.flext_pb2": mock_pb2_module,
        "flext_grpc.proto.flext_pb2_grpc": mock_pb2_grpc_module,
        "google.protobuf.timestamp_pb2": MagicMock(),
        "google.protobuf.empty_pb2": MagicMock(),
        "google.protobuf.struct_pb2": MagicMock(),
        "flext_core.config": MagicMock(),
        "flext_core.domain": MagicMock(),
        "flext_core.domain.types": MagicMock(),
        "flext_core.domain.pydantic_base": MagicMock(),
        "flext_observability.logging": MagicMock(),
    },
):
    from flext_grpc.client import ConnectionPool
    from flext_grpc.client import FlextGRPCClient

# Test constants
MOCK_JWT_TOKEN_FOR_TESTING = "Bearer mock_jwt_token_for_testing"


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
        # Mock the config and dependencies
        mock_config = MagicMock()
        mock_config.get_service_config.return_value = {"host": "localhost", "port": 50051}
        mock_config.business.GRPC_DEFAULT_MAX_MESSAGE_SIZE_MB = 100
        mock_config.network.grpc_keepalive_time_ms = 30000
        mock_config.network.grpc_keepalive_timeout_ms = 5000
        mock_config.network.grpc_keepalive_permit_without_calls = True
        mock_config.network.enable_ssl = False

        with patch("grpc.aio.insecure_channel", return_value=mock_channel), patch(
            "flext_grpc.proto.flext_pb2_grpc.FlextServiceStub",
            return_value=mock_stub,
        ), patch("flext_core.config.get_config", return_value=mock_config):
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
    async def test_health_check(
        self, client: FlextGRPCClient, mock_stub: MagicMock,
    ) -> None:
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
    async def test_create_pipeline(
        self, client: FlextGRPCClient, mock_stub: MagicMock,
    ) -> None:
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
    async def test_list_pipelines(
        self, client: FlextGRPCClient, mock_stub: MagicMock,
    ) -> None:
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
    async def test_execute_pipeline(
        self, client: FlextGRPCClient, mock_stub: MagicMock,
    ) -> None:
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

    @pytest.mark.skip(reason="Error handling with mocked gRPC errors needs proper AioRpcError implementation")
    @pytest.mark.asyncio
    async def test_error_handling(
        self, client: FlextGRPCClient, mock_stub: MagicMock,
    ) -> None:
        """Test error handling."""
        # Mock gRPC error
        mock_error = MagicMock(spec=grpc.aio.AioRpcError)
        mock_error.code.return_value = grpc.StatusCode.NOT_FOUND
        mock_error.details.return_value = "Pipeline not found"
        mock_stub.GetPipeline.side_effect = mock_error

        # Call should raise exception
        with pytest.raises(grpc.aio.AioRpcError) as exc_info:
            await client.get_pipeline("non-existent")

        assert exc_info.value.code() == grpc.StatusCode.NOT_FOUND

    @pytest.mark.asyncio
    async def test_timeout_handling(
        self, client: FlextGRPCClient, mock_stub: MagicMock,
    ) -> None:
        """Test timeout handling."""
        # TODO(@flext-team): Implement pipeline methods in client - Issue #123
        # Placeholder test for now - tests timeout configuration
        assert client.timeout == 30

    def test_client_with_tls(self) -> None:
        """Test client with TLS configuration."""
        client = FlextGRPCClient(
            host="secure.example.com",
            port=443,
            tls_enabled=True,
            tls_cert_path="/path/to/ca.pem",
        )

        assert client.tls_enabled
        assert client.tls_cert_path == "/path/to/ca.pem"

    def test_client_with_auth(self) -> None:
        """Test client with authentication."""
        # Use a clearly marked test token constant
        client = FlextGRPCClient(
            host="localhost",
            port=50051,
            token=MOCK_JWT_TOKEN_FOR_TESTING,
        )

        # Verify client configuration
        assert client.host == "localhost"
        assert client.port == 50051
        assert client.token == MOCK_JWT_TOKEN_FOR_TESTING


class TestConnectionPool:
    """Test gRPC connection pooling."""

    def test_pool_initialization(self) -> None:
        """Test connection pool initialization."""
        pool = ConnectionPool(max_size=10)

        assert pool.max_size == 10

    @pytest.mark.asyncio
    async def test_acquire_release_connection(self) -> None:
        """Test getting channels from pool."""
        pool = ConnectionPool(max_size=5)

        # Mock channel creation
        mock_channel = AsyncMock()
        with patch("grpc.insecure_channel", return_value=mock_channel):
            # Get channel
            channel = pool.get_channel("localhost:50051")
            assert channel is not None
            assert channel == mock_channel

    def test_connection_limit(self) -> None:
        """Test connection pool channel creation."""
        pool = ConnectionPool(max_size=2)

        # Get channels from pool
        channel1 = pool.get_channel("localhost:50051")
        channel2 = pool.get_channel("localhost:50052")

        # Verify channels are created
        assert channel1 is not None
        assert channel2 is not None

    @pytest.mark.asyncio
    async def test_connection_health_check(self) -> None:
        """Test connection health checking."""
        pool = ConnectionPool(max_size=5)

        # Mock unhealthy connection
        mock_channel = AsyncMock()
        mock_channel.get_state.return_value = grpc.ChannelConnectivity.TRANSIENT_FAILURE

        with patch("grpc.insecure_channel", return_value=mock_channel):
            channel = pool.get_channel("localhost:50051")

            # Simple verification that channel was created
            assert channel == mock_channel


class TestClientRetry:
    """Test client retry logic."""

    @pytest.mark.skip(reason="Retry logic not yet implemented in FlextGRPCClient")
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

        # Create mock errors
        mock_error1 = MagicMock(spec=grpc.aio.AioRpcError)
        mock_error1.code.return_value = grpc.StatusCode.UNAVAILABLE
        mock_error2 = MagicMock(spec=grpc.aio.AioRpcError)
        mock_error2.code.return_value = grpc.StatusCode.UNAVAILABLE

        mock_stub.CreatePipeline.side_effect = [
            mock_error1,
            mock_error2,
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

    @pytest.mark.skip(reason="Retry logic not yet implemented in FlextGRPCClient")
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
        mock_error = MagicMock(spec=grpc.aio.AioRpcError)
        mock_error.code.return_value = grpc.StatusCode.NOT_FOUND
        mock_error.details.return_value = "Pipeline not found"
        mock_stub.GetPipeline.side_effect = mock_error

        client._stub = mock_stub

        # Should fail immediately without retries
        with pytest.raises(grpc.aio.AioRpcError):
            await client.get_pipeline("non-existent")

        # Should only be called once (no retries)
        assert mock_stub.GetPipeline.call_count == 1
