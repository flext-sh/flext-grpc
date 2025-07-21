"""Comprehensive tests for gRPC server functionality without mocks.

This module provides real implementation tests for FlextGrpcServer
following the project's no-mock policy.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime

import pytest
from flext_core.domain.pipeline import PipelineName

from flext_grpc.server import FlextGrpcServer


class TestFlextGrpcServerComprehensive:
    """Comprehensive tests for gRPC server functionality."""

    def test_server_initialization_comprehensive(self) -> None:
        """Test comprehensive server initialization."""
        server = FlextGrpcServer(app=None)

        # Verify all expected attributes exist
        assert hasattr(server, "app")
        assert hasattr(server, "logger")
        assert hasattr(server, "_pipelines")
        assert hasattr(server, "_plugins")
        assert hasattr(server, "_executions")

        # Verify initial state
        assert server.app is None
        assert isinstance(server._pipelines, dict)
        assert isinstance(server._plugins, dict)
        assert isinstance(server._executions, dict)
        assert len(server._pipelines) == 0
        assert len(server._plugins) == 0
        assert len(server._executions) == 0

    def test_server_pipeline_storage(self) -> None:
        """Test server pipeline storage functionality."""
        from flext_grpc.models import PipelineModel

        server = FlextGrpcServer(app=None)

        # Create a test pipeline using flext-core Pipeline model
        from flext_core.domain.pipeline import PipelineName

        pipeline_name = PipelineName(value="test-pipeline")
        pipeline = PipelineModel(
            pipeline_name=pipeline_name,
            pipeline_description="Test pipeline",
            pipeline_is_active=True,
        )
        pipeline.create()  # This will set created_at/updated_at
        pipeline_id = pipeline.pipeline_id

        # Store pipeline
        server._pipelines[str(pipeline_id)] = pipeline

        # Verify storage
        assert len(server._pipelines) == 1
        assert str(pipeline_id) in server._pipelines
        stored_pipeline = server._pipelines[str(pipeline_id)]
        assert str(stored_pipeline.pipeline_name) == "test-pipeline"
        assert stored_pipeline.pipeline_description == "Test pipeline"

    def test_server_plugin_storage(self) -> None:
        """Test server plugin storage functionality."""
        from flext_grpc.models import PluginModel

        server = FlextGrpcServer(app=None)

        # Create a test plugin using flext-core PluginMetadata model
        plugin = PluginModel(
            name="test-plugin",
            version="1.0.0",
            author="test",
            capabilities=["extractor"],
            requirements=["tap-test"],
            config_schema={"api_key": {"type": "string"}},
        )

        # Store plugin with generated ID
        plugin_id = "test-plugin-id"
        server._plugins[plugin_id] = plugin

        # Verify storage
        assert len(server._plugins) == 1
        assert plugin_id in server._plugins
        stored_plugin = server._plugins[plugin_id]
        assert stored_plugin.name == "test-plugin"
        assert "extractor" in stored_plugin.capabilities

    def test_server_execution_storage(self) -> None:
        """Test server execution storage functionality."""
        from flext_grpc.models import ExecutionModel

        server = FlextGrpcServer(app=None)

        # Create a test execution using flext-core PipelineExecution model
        from flext_core.domain.pipeline import ExecutionStatus, PipelineId

        pipeline_id = PipelineId()
        execution = ExecutionModel(
            pipeline_id=pipeline_id,
            execution_status=ExecutionStatus.RUNNING,
            started_at=datetime.now(UTC),
            result={"environment": "test"},
        )

        # Store execution
        execution_id = execution.execution_id
        server._executions[str(execution_id)] = execution

        # Verify storage
        assert len(server._executions) == 1
        assert str(execution_id) in server._executions
        stored_execution = server._executions[str(execution_id)]
        assert stored_execution.execution_status == ExecutionStatus.RUNNING

    def test_server_multiple_entities(self) -> None:
        """Test server with multiple pipelines, plugins, and executions."""
        from flext_grpc.models import ExecutionModel, PipelineModel, PluginModel

        server = FlextGrpcServer(app=None)

        # Create multiple entities
        for i in range(3):
            # Pipeline
            pipeline_name = PipelineName(value=f"pipeline-{i}")
            pipeline = PipelineModel(
                pipeline_name=pipeline_name,
                pipeline_description=f"Test pipeline {i}",
                pipeline_is_active=True,
            )
            pipeline.create()  # This will set created_at/updated_at
            pipeline_id = pipeline.pipeline_id
            server._pipelines[str(pipeline_id)] = pipeline

            # Plugin
            plugin = PluginModel(
                name=f"plugin-{i}",
                version="1.0.0",
                author="test",
                capabilities=["extractor"],
                requirements=[f"tap-test-{i}"],
                config_schema={"index": {"type": "integer"}},
            )
            plugin_id = f"plugin-{i}-id"
            server._plugins[str(plugin_id)] = plugin

            # Execution
            from flext_core.domain.pipeline import ExecutionStatus

            execution = ExecutionModel(
                pipeline_id=pipeline_id,
                execution_status=ExecutionStatus.SUCCESS,
                started_at=datetime.now(UTC),
                completed_at=datetime.now(UTC),
                result={"index": i},
            )
            execution_id = execution.execution_id
            server._executions[str(execution_id)] = execution

        # Verify all entities are stored
        assert len(server._pipelines) == 3
        assert len(server._plugins) == 3
        assert len(server._executions) == 3

        # Verify entity names/properties
        pipeline_names = [str(p.pipeline_name) for p in server._pipelines.values()]
        assert "pipeline-0" in pipeline_names
        assert "pipeline-1" in pipeline_names
        assert "pipeline-2" in pipeline_names

    def test_server_logger_functionality(self) -> None:
        """Test server logger functionality."""
        server = FlextGrpcServer(app=None)

        # Verify logger exists and is properly configured
        assert server.logger is not None
        assert hasattr(server.logger, "info")
        assert hasattr(server.logger, "error")
        assert hasattr(server.logger, "debug")
        assert hasattr(server.logger, "warning")

    @pytest.mark.asyncio
    async def test_server_async_compatibility(self) -> None:
        """Test server compatibility with async operations."""
        server = FlextGrpcServer(app=None)

        # Test that server can be used in async context
        async def async_operation() -> str:
            # Simulate async work with server
            await asyncio.sleep(0.001)
            return f"Processed {len(server._pipelines)} pipelines"

        result = await async_operation()
        assert "Processed 0 pipelines" in result

    def test_server_version_info(self) -> None:
        """Test server version information."""
        from flext_grpc.server import __version__

        # Verify version is accessible
        assert __version__ is not None
        assert isinstance(__version__, str)
        assert __version__ == "0.7.0"

    def test_server_models_integration(self) -> None:
        """Test integration between server and models."""
        from flext_grpc.models import (
            ExecutionModel,
            PipelineModel,
            PluginModel,
            SystemMetrics,
        )

        server = FlextGrpcServer(app=None)

        # Verify all model types work with server
        assert PipelineModel is not None
        assert ExecutionModel is not None
        assert PluginModel is not None
        assert SystemMetrics is not None

        # Test that models can be instantiated
        pipeline_name = PipelineName(value="integration-test")
        pipeline = PipelineModel(
            pipeline_name=pipeline_name,
            pipeline_description="Integration test pipeline",
            pipeline_is_active=True,
        )
        pipeline.create()  # This will set created_at/updated_at
        pipeline_id = pipeline.pipeline_id

        # Test integration with server storage
        server._pipelines[str(pipeline_id)] = pipeline
        assert len(server._pipelines) == 1


class TestServerConverterIntegration:
    """Test server integration with converter utilities."""

    def test_server_with_converters(self) -> None:
        """Test server integration with protobuf converters."""
        from flext_grpc.converters import dict_to_struct, struct_to_dict

        server = FlextGrpcServer(app=None)
        assert server is not None  # Verify server can be created

        # Test converter functionality that server might use
        test_config = {
            "database": "test_db",
            "host": "localhost",
            "port": 5432,
            "ssl": True,
        }

        # Convert to protobuf struct
        config_struct = dict_to_struct(test_config)
        assert config_struct is not None

        # Convert back to dict
        converted_config = struct_to_dict(config_struct)
        assert converted_config["database"] == "test_db"
        assert converted_config["host"] == "localhost"
        assert converted_config["port"] == 5432
        assert converted_config["ssl"] is True


@pytest.mark.integration
class TestGRPCServerIntegration:
    """Integration tests for complete gRPC server functionality."""

    @pytest.mark.asyncio
    async def test_server_full_integration(self) -> None:
        """Test complete server integration."""
        server = FlextGrpcServer()

        # Test server initialization and basic functionality
        assert server is not None
        assert hasattr(server, "_pipelines")
        assert hasattr(server, "_plugins")
        assert hasattr(server, "_executions")

        # Basic integration test - server should be ready for gRPC operations
        # In a full integration test, this would include actual gRPC calls

    @pytest.mark.asyncio
    async def test_concurrent_server_operations(self) -> None:
        """Test concurrent operations on server."""
        server = FlextGrpcServer()

        # Simulate concurrent operations
        async def store_entity(index: int) -> str:
            from flext_grpc.models import PipelineModel

            await asyncio.sleep(0.001)  # Simulate async work

            from flext_core.domain.pipeline import PipelineId, PipelineName

            pipeline_id = PipelineId()
            pipeline = PipelineModel(
                id=pipeline_id.value,
                pipeline_name=PipelineName(value=f"concurrent-pipeline-{index}"),
                pipeline_description=f"Concurrent test pipeline {index}",
                pipeline_is_active=True,
            )

            server._pipelines[str(pipeline_id)] = pipeline
            return f"stored-{index}"

        # Run concurrent operations
        tasks = [store_entity(i) for i in range(5)]
        results = await asyncio.gather(*tasks)

        # Verify all operations completed
        assert len(results) == 5
        assert all("stored-" in result for result in results)
        assert len(server._pipelines) == 5
