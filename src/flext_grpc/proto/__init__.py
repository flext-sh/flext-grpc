"""Protocol buffer definitions for FLEXT gRPC services."""

from typing import Any

# Import generated protobuf modules
try:
    from flext_grpc.proto import flext_pb2
    from flext_grpc.proto import flext_pb2_grpc
except ImportError:
    # Fallback for when proto files are not generated yet
    import types

    # Create mock modules for TYPE_CHECKING
    flext_pb2 = types.ModuleType("flext_pb2")
    flext_pb2_grpc = types.ModuleType("flext_pb2_grpc")

    # Add basic mock classes aligned with proto definition
    class MockHealthStatus:
        def __init__(self, **kwargs: Any) -> None:
            self.healthy = kwargs.get("healthy", True)
            self.components = kwargs.get("components", {})
            self.timestamp = kwargs.get("timestamp")

    class MockComponentHealth:
        def __init__(self, **kwargs: Any) -> None:
            self.name = kwargs.get("name", "")
            self.healthy = kwargs.get("healthy", True)
            self.message = kwargs.get("message", "")
            self.metadata = kwargs.get("metadata", {})

    class MockSystemStats:
        def __init__(self, **kwargs: Any) -> None:
            self.active_pipelines = kwargs.get("active_pipelines", 0)
            self.total_executions = kwargs.get("total_executions", 0)
            self.success_rate = kwargs.get("success_rate", 100.0)
            self.uptime_seconds = kwargs.get("uptime_seconds", 3600)
            self.cpu_usage = kwargs.get("cpu_usage", 0.0)
            self.memory_usage = kwargs.get("memory_usage", 0.0)
            self.active_connections = kwargs.get("active_connections", 1)

    class MockPipelineResponse:
        def __init__(self, **kwargs: Any) -> None:
            self.pipeline = kwargs.get("pipeline", MockPipeline())

    class MockListPipelinesResponse:
        def __init__(self, **kwargs: Any) -> None:
            self.pipelines = kwargs.get("pipelines", [])
            self.total = kwargs.get("total", 0)
            self.limit = kwargs.get("limit", 50)
            self.offset = kwargs.get("offset", 0)

    class MockExecutionResponse:
        def __init__(self, **kwargs: Any) -> None:
            self.execution = kwargs.get("execution", MockExecution())

    class MockExecution:
        def __init__(self, **kwargs: Any) -> None:
            self.id = kwargs.get("id", "")
            self.pipeline_id = kwargs.get("pipeline_id", "")
            self.status = kwargs.get("status", 0)

    class MockPipeline:
        def __init__(self, **kwargs: Any) -> None:
            self.id = kwargs.get("id", "")
            self.name = kwargs.get("name", "")
            self.description = kwargs.get("description", "")

    # Add missing request types
    class MockCreatePipelineRequest:
        def __init__(self, **kwargs: Any) -> None:
            self.name = kwargs.get("name", "")
            self.description = kwargs.get("description", "")
            self.extractor = kwargs.get("extractor", "")
            self.loader = kwargs.get("loader", "")
            self.transform = kwargs.get("transform", "")
            self.config = kwargs.get("config")

    class MockGetPipelineRequest:
        def __init__(self, **kwargs: Any) -> None:
            self.id = kwargs.get("id", "")

    class MockListPipelinesRequest:
        def __init__(self, **kwargs: Any) -> None:
            self.filter = kwargs.get("filter", "")
            self.offset = kwargs.get("offset", 0)
            self.limit = kwargs.get("limit", 50)

    class MockRunPipelineRequest:
        def __init__(self, **kwargs: Any) -> None:
            self.pipeline_id = kwargs.get("pipeline_id", "")
            self.full_refresh = kwargs.get("full_refresh", False)
            self.env_vars = kwargs.get("env_vars", {})

    class MockListPluginsRequest:
        def __init__(self, **kwargs: Any) -> None:
            self.type = kwargs.get("type", 0)  # PLUGIN_TYPE_UNSPECIFIED
            self.installed_only = kwargs.get("installed_only", False)

    class MockStreamLogsRequest:
        def __init__(self, **kwargs: Any) -> None:
            self.execution_id = kwargs.get("execution_id", "")
            self.follow = kwargs.get("follow", False)

    # Add missing response types
    class MockPlugin:
        def __init__(self, **kwargs: Any) -> None:
            self.name = kwargs.get("name", "")
            self.type = kwargs.get("type", 0)
            self.version = kwargs.get("version", "")
            self.description = kwargs.get("description", "")
            self.installed = kwargs.get("installed", False)
            self.settings = kwargs.get("settings")
            self.installed_at = kwargs.get("installed_at")

    class MockListPluginsResponse:
        def __init__(self, **kwargs: Any) -> None:
            self.plugins = kwargs.get("plugins", [])
            self.total = kwargs.get("total", 0)

    class MockLogEntry:
        def __init__(self, **kwargs: Any) -> None:
            self.timestamp = kwargs.get("timestamp", "")
            self.level = kwargs.get("level", "INFO")
            self.message = kwargs.get("message", "")
            self.execution_id = kwargs.get("execution_id", "")

    # Add enum constants
    PLUGIN_TYPE_UNSPECIFIED = 0
    PLUGIN_TYPE_EXTRACTOR = 1
    PLUGIN_TYPE_LOADER = 2
    PLUGIN_TYPE_TRANSFORMER = 3
    PLUGIN_TYPE_ORCHESTRATOR = 4
    PLUGIN_TYPE_UTILITY = 5

    STATUS_UNSPECIFIED = 0
    STATUS_PENDING = 1
    STATUS_RUNNING = 2
    STATUS_SUCCESS = 3
    STATUS_FAILED = 4
    STATUS_CANCELLED = 5

    class MockFlextServiceServicer:
        pass

    class MockFlextServiceStub:
        def __init__(self, channel: Any) -> None:
            self.channel = channel

        def HealthCheck(self, request: Any = None) -> Any:
            return MockHealthStatus()

        def CreatePipeline(self, request: Any = None) -> Any:
            return MockPipelineResponse()

        def GetPipeline(self, request: Any = None) -> Any:
            return MockPipelineResponse()

        def ListPipelines(self, request: Any = None) -> Any:
            return MockListPipelinesResponse()

        def ExecutePipeline(self, request: Any = None) -> Any:
            return MockExecutionResponse()

    def mock_add_servicer_to_server(servicer: Any, server: Any) -> None:
        pass

    flext_pb2.HealthStatus = MockHealthStatus
    flext_pb2.ComponentHealth = MockComponentHealth
    flext_pb2.SystemStats = MockSystemStats
    flext_pb2.PipelineResponse = MockPipelineResponse
    flext_pb2.ListPipelinesResponse = MockListPipelinesResponse
    flext_pb2.ExecutionResponse = MockExecutionResponse
    flext_pb2.Pipeline = MockPipeline
    flext_pb2.Execution = MockExecution
    flext_pb2.Plugin = MockPlugin
    flext_pb2.LogEntry = MockLogEntry

    # Request types
    flext_pb2.CreatePipelineRequest = MockCreatePipelineRequest
    flext_pb2.GetPipelineRequest = MockGetPipelineRequest
    flext_pb2.ListPipelinesRequest = MockListPipelinesRequest
    flext_pb2.RunPipelineRequest = MockRunPipelineRequest
    flext_pb2.ListPluginsRequest = MockListPluginsRequest
    flext_pb2.StreamLogsRequest = MockStreamLogsRequest

    # Response types
    flext_pb2.ListPluginsResponse = MockListPluginsResponse

    # Enum constants
    flext_pb2.PLUGIN_TYPE_UNSPECIFIED = PLUGIN_TYPE_UNSPECIFIED
    flext_pb2.PLUGIN_TYPE_EXTRACTOR = PLUGIN_TYPE_EXTRACTOR
    flext_pb2.PLUGIN_TYPE_LOADER = PLUGIN_TYPE_LOADER
    flext_pb2.PLUGIN_TYPE_TRANSFORMER = PLUGIN_TYPE_TRANSFORMER
    flext_pb2.PLUGIN_TYPE_ORCHESTRATOR = PLUGIN_TYPE_ORCHESTRATOR
    flext_pb2.PLUGIN_TYPE_UTILITY = PLUGIN_TYPE_UTILITY

    flext_pb2.STATUS_UNSPECIFIED = STATUS_UNSPECIFIED
    flext_pb2.STATUS_PENDING = STATUS_PENDING
    flext_pb2.STATUS_RUNNING = STATUS_RUNNING
    flext_pb2.STATUS_SUCCESS = STATUS_SUCCESS
    flext_pb2.STATUS_FAILED = STATUS_FAILED
    flext_pb2.STATUS_CANCELLED = STATUS_CANCELLED

    flext_pb2_grpc.FlextServiceServicer = MockFlextServiceServicer
    flext_pb2_grpc.FlextServiceStub = MockFlextServiceStub
    flext_pb2_grpc.add_FlextServiceServicer_to_server = mock_add_servicer_to_server

__all__ = ["flext_pb2", "flext_pb2_grpc"]
