"""Generated protobuf code for FLEXT gRPC services - stub implementation."""

# This would normally be generated from .proto files
# For now, creating minimal stubs for compatibility


class Empty:
    """Empty message for gRPC calls."""


class HealthCheckRequest:
    """Health check request message."""

    def __init__(self) -> None:
        self.service = ""


class HealthCheckResponse:
    """Health check response message."""

    def __init__(self) -> None:
        self.status = 0  # SERVING = 1, NOT_SERVING = 2


class ComponentHealth:
    """Component health status message."""

    def __init__(self) -> None:
        self.component_name = ""
        self.status = 0
        self.details = ""
