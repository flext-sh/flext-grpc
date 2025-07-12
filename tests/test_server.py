"""Real tests for gRPC server functionality."""

from __future__ import annotations

import asyncio
from concurrent import futures
from unittest.mock import AsyncMock, MagicMock, patch

import grpc
import pytest
from grpc import aio

# Mock the proto imports since they may not be generated yet
with patch.dict("sys.modules", {
    "flext_grpc.proto": MagicMock(),
    "flext_grpc.proto.flext_pb2": MagicMock(),
    "flext_grpc.proto.flext_pb2_grpc": MagicMock(),
}):
    from flext_grpc.server import FlextGRPCServer
    from flext_grpc.server_implementation import FlextServiceServicer


class TestFlextServiceServicer:
    """Test cases for Flext gRPC service implementation."""

    @pytest.fixture
    def mock_command_bus(self) -> AsyncMock:
        """Create a mock command bus."""
        return AsyncMock()

    @pytest.fixture
    def mock_query_bus(self) -> AsyncMock:
        """Create a mock query bus."""
        return AsyncMock()

    @pytest.fixture
    def servicer(self, mock_command_bus: AsyncMock, mock_query_bus: AsyncMock) -> FlextServiceServicer:
        """Create a servicer instance with mocked dependencies."""
        return FlextServiceServicer(
            command_bus=mock_command_bus,
            query_bus=mock_query_bus,
        )

    @pytest.mark.asyncio
    async def test_health_check(self, servicer: FlextServiceServicer) -> None:
        """Test health check endpoint."""
        # Mock request and context
        request = MagicMock()
        context = MagicMock()
        
        # Call health check
        response = await servicer.HealthCheck(request, context)
        
        # Verify response
        assert response is not None
        assert hasattr(response, "status")
        assert response.status == "SERVING"

    @pytest.mark.asyncio
    async def test_create_pipeline_success(
        self,
        servicer: FlextServiceServicer,
        mock_command_bus: AsyncMock,
    ) -> None:
        """Test successful pipeline creation."""
        # Mock request
        request = MagicMock()
        request.name = "test-pipeline"
        request.pipeline_type = "DATABASE_SYNC"
        request.config = {"tap": "tap-postgres", "target": "target-snowflake"}
        
        # Mock context
        context = MagicMock()
        context.set_code = MagicMock()
        context.set_details = MagicMock()
        
        # Mock command bus response
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.value = MagicMock(id="pipeline-123")
        mock_command_bus.execute.return_value = mock_result
        
        # Call create pipeline
        response = await servicer.CreatePipeline(request, context)
        
        # Verify command bus was called
        mock_command_bus.execute.assert_called_once()
        
        # Verify response
        assert response is not None
        assert response.pipeline_id == "pipeline-123"
        
        # Verify context not set to error
        context.set_code.assert_not_called()

    @pytest.mark.asyncio
    async def test_create_pipeline_failure(
        self,
        servicer: FlextServiceServicer,
        mock_command_bus: AsyncMock,
    ) -> None:
        """Test pipeline creation failure."""
        # Mock request
        request = MagicMock()
        request.name = "invalid-pipeline"
        
        # Mock context
        context = MagicMock()
        context.set_code = MagicMock()
        context.set_details = MagicMock()
        
        # Mock command bus error response
        mock_result = MagicMock()
        mock_result.success = False
        mock_result.error = MagicMock(message="Invalid pipeline configuration")
        mock_command_bus.execute.return_value = mock_result
        
        # Call create pipeline
        response = await servicer.CreatePipeline(request, context)
        
        # Verify error handling
        context.set_code.assert_called_with(grpc.StatusCode.INVALID_ARGUMENT)
        context.set_details.assert_called_with("Invalid pipeline configuration")

    @pytest.mark.asyncio
    async def test_list_pipelines(
        self,
        servicer: FlextServiceServicer,
        mock_query_bus: AsyncMock,
    ) -> None:
        """Test listing pipelines."""
        # Mock request
        request = MagicMock()
        request.page_size = 10
        request.page_token = ""
        
        # Mock query bus response
        mock_pipelines = [
            MagicMock(id="p1", name="Pipeline 1"),
            MagicMock(id="p2", name="Pipeline 2"),
        ]
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.value = mock_pipelines
        mock_query_bus.execute.return_value = mock_result
        
        # Call list pipelines
        context = MagicMock()
        response = await servicer.ListPipelines(request, context)
        
        # Verify response
        assert response is not None
        assert len(response.pipelines) == 2
        assert response.pipelines[0].id == "p1"
        assert response.pipelines[1].id == "p2"

    @pytest.mark.asyncio
    async def test_execute_pipeline(
        self,
        servicer: FlextServiceServicer,
        mock_command_bus: AsyncMock,
    ) -> None:
        """Test pipeline execution."""
        # Mock request
        request = MagicMock()
        request.pipeline_id = "pipeline-123"
        request.parameters = {"full_refresh": True}
        
        # Mock execution result
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.value = MagicMock(
            execution_id="exec-456",
            status="RUNNING",
        )
        mock_command_bus.execute.return_value = mock_result
        
        # Call execute pipeline
        context = MagicMock()
        response = await servicer.ExecutePipeline(request, context)
        
        # Verify response
        assert response is not None
        assert response.execution_id == "exec-456"
        assert response.status == "RUNNING"

    @pytest.mark.asyncio
    async def test_stream_logs(self, servicer: FlextServiceServicer) -> None:
        """Test log streaming."""
        # Mock request
        request = MagicMock()
        request.execution_id = "exec-123"
        request.follow = True
        
        # Mock log service
        mock_log_entries = [
            MagicMock(timestamp="2025-01-01T00:00:00", level="INFO", message="Starting"),
            MagicMock(timestamp="2025-01-01T00:00:01", level="INFO", message="Processing"),
            MagicMock(timestamp="2025-01-01T00:00:02", level="INFO", message="Completed"),
        ]
        
        async def mock_stream():
            for entry in mock_log_entries:
                yield entry
        
        with patch.object(servicer, "_log_service") as mock_log_service:
            mock_log_service.stream.return_value = mock_stream()
            
            # Collect streamed logs
            context = MagicMock()
            logs = []
            async for log_entry in servicer.StreamLogs(request, context):
                logs.append(log_entry)
            
            # Verify logs
            assert len(logs) == 3
            assert logs[0].message == "Starting"
            assert logs[2].message == "Completed"


class TestFlextGRPCServer:
    """Test gRPC server lifecycle."""

    @pytest.fixture
    def server(self) -> FlextGRPCServer:
        """Create a server instance."""
        return FlextGRPCServer(
            host="localhost",
            port=50051,
            max_workers=10,
        )

    def test_server_initialization(self, server: FlextGRPCServer) -> None:
        """Test server initialization."""
        assert server.host == "localhost"
        assert server.port == 50051
        assert server.max_workers == 10
        assert server._server is None

    @pytest.mark.asyncio
    async def test_server_start_stop(self, server: FlextGRPCServer) -> None:
        """Test server start and stop."""
        # Mock the actual gRPC server
        mock_grpc_server = AsyncMock()
        
        with patch("grpc.aio.server", return_value=mock_grpc_server):
            # Start server
            await server.start()
            
            # Verify server was created and started
            assert server._server is not None
            mock_grpc_server.start.assert_called_once()
            
            # Stop server
            await server.stop()
            
            # Verify server was stopped
            mock_grpc_server.stop.assert_called_once()

    def test_server_with_tls(self) -> None:
        """Test server with TLS configuration."""
        server = FlextGRPCServer(
            host="0.0.0.0",
            port=50051,
            tls_cert_path="/path/to/cert.pem",
            tls_key_path="/path/to/key.pem",
        )
        
        assert server.tls_enabled
        assert server.tls_cert_path == "/path/to/cert.pem"
        assert server.tls_key_path == "/path/to/key.pem"


class TestGRPCInterceptors:
    """Test gRPC interceptors."""

    def test_auth_interceptor(self) -> None:
        """Test authentication interceptor."""
        from flext_grpc.interceptors import AuthInterceptor
        
        interceptor = AuthInterceptor(
            public_key_path="/path/to/public.pem",
            skip_auth_methods=["HealthCheck"],
        )
        
        assert interceptor.public_key_path == "/path/to/public.pem"
        assert "HealthCheck" in interceptor.skip_auth_methods

    def test_logging_interceptor(self) -> None:
        """Test logging interceptor."""
        from flext_grpc.interceptors import LoggingInterceptor
        
        interceptor = LoggingInterceptor(
            log_level="DEBUG",
            log_request_body=True,
        )
        
        assert interceptor.log_level == "DEBUG"
        assert interceptor.log_request_body is True

    def test_metrics_interceptor(self) -> None:
        """Test metrics interceptor."""
        from flext_grpc.interceptors import MetricsInterceptor
        
        interceptor = MetricsInterceptor(
            prometheus_enabled=True,
            metrics_port=9090,
        )
        
        assert interceptor.prometheus_enabled is True
        assert interceptor.metrics_port == 9090


@pytest.mark.integration
class TestGRPCIntegration:
    """Integration tests for gRPC service."""

    @pytest.mark.asyncio
    async def test_end_to_end_pipeline_flow(self) -> None:
        """Test complete pipeline flow from creation to execution."""
        # This would require a running server and client
        # Marked as integration test to be run separately
        pytest.skip("Integration test - requires running server")

    @pytest.mark.asyncio
    async def test_concurrent_requests(self) -> None:
        """Test handling concurrent gRPC requests."""
        # This would test server's ability to handle multiple concurrent calls
        pytest.skip("Integration test - requires running server")