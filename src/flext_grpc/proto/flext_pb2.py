"""Generated protobuf code for FLEXT gRPC services - stub implementation."""

# This would normally be generated from .proto files
# For now, creating minimal stubs for compatibility


class Empty:
    """Empty message for gRPC calls."""

    pass


class HealthCheckRequest:
    """Health check request message."""

    def __init__(self):
        self.service = ""


class HealthCheckResponse:
    """Health check response message."""

    def __init__(self):
        self.status = 0  # SERVING = 1, NOT_SERVING = 2


class ComponentHealth:
    """Component health status message."""

    def __init__(self):
        self.component_name = ""
        self.status = 0
        self.details = ""
