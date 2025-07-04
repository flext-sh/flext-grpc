"""Generated gRPC service code for FLEXT services - stub implementation."""


class HealthServicer:
    """Health check service."""

    def Check(self, request, context):
        """Check health status."""
        from . import flext_pb2
        response = flext_pb2.HealthCheckResponse()
        response.status = 1  # SERVING
        return response


class HealthStub:
    """Health check client stub."""

    def __init__(self, channel) -> None:
        self.channel = channel

    def Check(self, request):
        """Check health status."""
        from . import flext_pb2
        response = flext_pb2.HealthCheckResponse()
        response.status = 1  # SERVING
        return response


class FlextServiceServicer:
    """Main FLEXT service implementation."""

    def ListPipelines(self, request, context):
        """List available pipelines."""
        from . import flext_pb2
        return flext_pb2.Empty()

    def RunPipeline(self, request, context):
        """Run a pipeline."""
        from . import flext_pb2
        return flext_pb2.Empty()


class FlextServiceStub:
    """FLEXT service client stub."""

    def __init__(self, channel) -> None:
        self.channel = channel
