"""Protocol buffer definitions for FLEXT gRPC services."""

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

    # Add basic mock classes
    class MockHealthResponse:
        def __init__(self, **kwargs) -> None: pass

    class MockCreatePipelineResponse:
        def __init__(self, **kwargs) -> None: pass

    class MockGetPipelineResponse:
        def __init__(self, **kwargs) -> None: pass

    class MockListPipelinesResponse:
        def __init__(self, **kwargs) -> None: pass

    class MockPipeline:
        def __init__(self, **kwargs) -> None: pass

    class MockFlextServiceServicer:
        pass

    def mock_add_servicer_to_server(servicer, server) -> None: pass

    flext_pb2.HealthResponse = MockHealthResponse
    flext_pb2.CreatePipelineResponse = MockCreatePipelineResponse
    flext_pb2.GetPipelineResponse = MockGetPipelineResponse
    flext_pb2.ListPipelinesResponse = MockListPipelinesResponse
    flext_pb2.Pipeline = MockPipeline

    flext_pb2_grpc.FlextServiceServicer = MockFlextServiceServicer
    flext_pb2_grpc.add_FlextServiceServicer_to_server = mock_add_servicer_to_server

__all__ = ["flext_pb2", "flext_pb2_grpc"]
