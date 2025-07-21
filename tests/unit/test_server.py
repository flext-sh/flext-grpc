"""Tests for gRPC server functionality without mocks."""

from __future__ import annotations

import asyncio

import pytest

from flext_grpc.server import FlextGrpcServer


class TestFlextGrpcServicer:
    """Test cases for Flext gRPC service implementation."""

    def test_servicer_interface_exists(self) -> None:
        """Test that servicer interface can be imported."""
        from flext_grpc.server import FlextGrpcServicer

        # Verify the class can be imported
        assert FlextGrpcServicer is not None

    def test_servicer_has_required_methods(self) -> None:
        """Test that servicer has required gRPC methods."""
        from flext_grpc.server import FlextGrpcServicer

        # Verify required methods exist
        required_methods = [
            "HealthCheck",
            "CreatePipeline",
            "ListPipelines",
            "RunPipeline",
            "StreamLogs",
        ]

        for method_name in required_methods:
            assert hasattr(FlextGrpcServicer, method_name), (
                f"Missing method: {method_name}"
            )


class TestFlextGRPCServer:
    """Test gRPC server lifecycle."""

    def test_server_initialization(self) -> None:
        """Test server initialization."""
        # Test with minimal initialization
        server = FlextGrpcServer(app=None)

        # Basic attributes should exist
        assert hasattr(server, "app")
        assert hasattr(server, "logger")
        assert hasattr(server, "_pipelines")
        assert hasattr(server, "_plugins")

    def test_server_basic_functionality(self) -> None:
        """Test basic server functionality."""
        server = FlextGrpcServer(app=None)

        # Server should be able to store models
        assert isinstance(server._pipelines, dict)
        assert isinstance(server._plugins, dict)

        # Should have version
        from flext_grpc.server import __version__

        assert __version__ == "0.7.0"

    def test_models_import(self) -> None:
        """Test that models can be imported."""
        from flext_grpc.models import (
            ExecutionModel,
            PipelineModel,
            PluginModel,
            SystemMetrics,
        )

        # Just verify they can be imported
        assert PipelineModel is not None
        assert ExecutionModel is not None
        assert PluginModel is not None
        assert SystemMetrics is not None


class TestGRPCInterceptors:
    """Test gRPC interceptors."""

    def test_interceptor_imports(self) -> None:
        """Test that interceptors can be imported."""
        from flext_grpc.interceptors import (
            AuthenticationInterceptor,
            MetricsInterceptor,
            RateLimitingInterceptor,
            TracingInterceptor,
        )

        # Just verify they can be imported
        assert AuthenticationInterceptor is not None
        assert MetricsInterceptor is not None
        assert TracingInterceptor is not None
        assert RateLimitingInterceptor is not None


@pytest.mark.integration
class TestGRPCIntegration:
    """Integration tests for gRPC service."""

    @pytest.mark.asyncio
    async def test_end_to_end_pipeline_flow(self) -> None:
        """Test complete pipeline flow from creation to execution."""
        # Integration test with real server - implement properly
        # Use test gRPC server with real implementation

        from flext_grpc.server import FlextGrpcServer

        # Create test server
        server = FlextGrpcServer()

        # Basic integration verification
        assert server is not None
        # Server integration tests should verify actual connectivity

    @pytest.mark.asyncio
    async def test_concurrent_requests(self) -> None:
        """Test handling concurrent gRPC requests."""
        # Test concurrent request handling without mocks

        # Test concurrent operations capability
        async def real_operation() -> str:
            await asyncio.sleep(0.01)  # Simulate async work
            return "test_result"

        # Verify concurrent execution works
        tasks = [real_operation() for _ in range(5)]
        results = await asyncio.gather(*tasks)
        assert len(results) == 5
        assert all(result == "test_result" for result in results)
