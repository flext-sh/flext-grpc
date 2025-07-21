"""Test configuration for flext-grpc.

Provides pytest fixtures and configuration for testing gRPC services and clients
using flext-core patterns and real gRPC communication.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

import pytest

if TYPE_CHECKING:
    from collections.abc import Generator


# Test environment setup
@pytest.fixture(autouse=True)
def set_test_environment() -> Generator[None]:
    """Set test environment variables."""
    os.environ["FLEXT_ENV"] = "test"
    os.environ["FLEXT_LOG_LEVEL"] = "debug"
    os.environ["FLEXT_GRPC_DEBUG"] = "true"
    yield
    # Cleanup
    os.environ.pop("FLEXT_ENV", None)
    os.environ.pop("FLEXT_LOG_LEVEL", None)
    os.environ.pop("FLEXT_GRPC_DEBUG", None)


# gRPC server fixtures
@pytest.fixture
def grpc_server_config() -> dict[str, Any]:
    """GRPC server configuration for testing."""
    return {
        "host": "localhost",
        "port": 50051,
        "max_workers": 4,
        "max_receive_message_length": 4 * 1024 * 1024,
        "max_send_message_length": 4 * 1024 * 1024,
        "reflection_enabled": True,
        "health_check_enabled": True,
    }


@pytest.fixture
async def grpc_server(grpc_server_config: dict[str, Any]) -> Any:
    """GRPC server for testing."""
    from flext_grpc.server import FlextGrpcServer

    # TODO: Implement start/stop methods for test server
    return FlextGrpcServer()


@pytest.fixture
async def grpc_client(grpc_server_config: dict[str, Any]) -> Any:
    """GRPC client for testing."""
    from flext_grpc.client import FlextGRPCClientOld

    client = FlextGRPCClientOld(
        host=grpc_server_config["host"],
        port=grpc_server_config["port"],
    )
    client.connect()  # Sync method
    return client
    # client.disconnect()  # TODO: Implement disconnect method


# gRPC service fixtures
@pytest.fixture
def pipeline_service_stub() -> Any:
    """Pipeline service stub for testing."""
    # from flext_grpc.services.pipeline_pb2_grpc import PipelineServiceStub
    # TODO: Implement when protobuf services are generated
    return None


@pytest.fixture
def plugin_service_stub() -> Any:
    """Plugin service stub for testing."""
    # from flext_grpc.services.plugin_pb2_grpc import PluginServiceStub
    # TODO: Implement when protobuf services are generated
    return None


@pytest.fixture
def monitoring_service_stub() -> Any:
    """Monitoring service stub for testing."""
    # from flext_grpc.services.monitoring_pb2_grpc import MonitoringServiceStub
    # TODO: Implement when protobuf services are generated
    return None


# Protocol buffer message fixtures
@pytest.fixture
def sample_pipeline_request() -> dict[str, Any]:
    """Sample pipeline request for testing."""
    return {
        "name": "test-pipeline",
        "description": "Test pipeline for gRPC testing",
        "extractor": "tap-postgres",
        "loader": "target-snowflake",
        "config": {
            "database_url": "postgresql://localhost/test",
            "warehouse": "test_warehouse",
        },
    }


@pytest.fixture
def sample_plugin_request() -> dict[str, Any]:
    """Sample plugin request for testing."""
    return {
        "name": "test-plugin",
        "type": "extractor",
        "package": "tap-test",
        "version": "1.0.0",
        "config": {
            "api_key": "test_key",
            "base_url": "https://api.test.com",
        },
    }


@pytest.fixture
def sample_execution_request() -> dict[str, Any]:
    """Sample execution request for testing."""
    return {
        "pipeline_id": "test-pipeline-id",
        "full_refresh": False,
        "environment": "test",
        "metadata": {
            "triggered_by": "test",
            "execution_type": "manual",
        },
    }


# gRPC interceptor fixtures
@pytest.fixture
def auth_interceptor() -> Any:
    """Authentication interceptor for testing."""
    # from flext_grpc.interceptors.auth import AuthInterceptor
    # TODO: Implement when interceptors are created
    return None


@pytest.fixture
def logging_interceptor() -> Any:
    """Logging interceptor for testing."""
    # from flext_grpc.interceptors.logging import LoggingInterceptor
    # TODO: Implement when interceptors are created
    return None


@pytest.fixture
def metrics_interceptor() -> Any:
    """Metrics interceptor for testing."""
    # from flext_grpc.interceptors.metrics import MetricsInterceptor
    # TODO: Implement when interceptors are created
    return None


# gRPC channel fixtures
@pytest.fixture
def insecure_channel() -> Any:
    """Insecure gRPC channel for testing."""
    import grpc

    channel = grpc.insecure_channel("localhost:50051")
    yield channel
    channel.close()


@pytest.fixture
def secure_channel() -> Any:
    """Secure gRPC channel for testing."""
    import grpc

    credentials = grpc.ssl_channel_credentials()
    channel = grpc.secure_channel("localhost:50051", credentials)
    yield channel
    channel.close()


# Error handling fixtures
@pytest.fixture
def grpc_error_scenarios() -> list[dict[str, Any]]:
    """GRPC error scenarios for testing."""
    return [
        {
            "code": "INVALID_ARGUMENT",
            "message": "Invalid pipeline configuration",
            "details": {"field": "name", "error": "required"},
        },
        {
            "code": "NOT_FOUND",
            "message": "Pipeline not found",
            "details": {"pipeline_id": "non-existent"},
        },
        {
            "code": "PERMISSION_DENIED",
            "message": "Insufficient permissions",
            "details": {"required_permission": "pipeline:execute"},
        },
        {
            "code": "INTERNAL",
            "message": "Internal server error",
            "details": {"error_id": "internal-500"},
        },
    ]


# Performance fixtures
@pytest.fixture
def grpc_load_test_config() -> dict[str, Any]:
    """GRPC load testing configuration."""
    return {
        "concurrent_requests": 10,
        "total_requests": 100,
        "request_rate": 10,  # requests per second
        "timeout_seconds": 30,
    }


# Streaming fixtures
@pytest.fixture
def streaming_request_data() -> list[dict[str, Any]]:
    """Sample streaming request data."""
    return [
        {"batch_id": 1, "records": [{"id": 1, "data": "test1"}]},
        {"batch_id": 2, "records": [{"id": 2, "data": "test2"}]},
        {"batch_id": 3, "records": [{"id": 3, "data": "test3"}]},
    ]


# Pytest markers for test categorization
def pytest_configure(config: pytest.Config) -> None:
    """Configure pytest markers."""
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "grpc: gRPC service tests")
    config.addinivalue_line("markers", "streaming: gRPC streaming tests")
    config.addinivalue_line("markers", "performance: Performance tests")
    config.addinivalue_line("markers", "security: Security tests")
    config.addinivalue_line("markers", "slow: Slow tests")


# Mock gRPC services
@pytest.fixture
def mock_pipeline_service() -> Any:
    """Mock pipeline service for testing."""

    class MockPipelineService:
        async def create_pipeline(self, request: Any, context: Any) -> dict[str, str]:
            return {"id": "test-pipeline-id", "status": "created"}

        async def get_pipeline(self, request: Any, context: Any) -> dict[str, str]:
            return {"id": request.id, "name": "Test Pipeline"}

        async def list_pipelines(
            self,
            request: Any,
            context: Any,
        ) -> dict[str, list[Any]]:
            return {"pipelines": []}

        async def execute_pipeline(self, request: Any, context: Any) -> dict[str, str]:
            return {"execution_id": "test-execution-id", "status": "started"}

    return MockPipelineService()


@pytest.fixture
def mock_plugin_service() -> Any:
    """Mock plugin service for testing."""

    class MockPluginService:
        async def install_plugin(self, request: Any, context: Any) -> dict[str, str]:
            return {"name": request.name, "status": "installed"}

        async def list_plugins(
            self,
            request: Any,
            context: Any,
        ) -> dict[str, list[Any]]:
            return {"plugins": []}

        async def get_plugin(self, request: Any, context: Any) -> dict[str, str]:
            return {"name": request.name, "status": "enabled"}

    return MockPluginService()
