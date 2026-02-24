"""Internal aliases for re-export in __init__.py.

This module contains derived aliases that cannot be expressed as simple
re-exports in __init__.py. They are imported and re-exported from __init__.py
to satisfy RUF067 requirements.
"""

from __future__ import annotations

from flext_core import FlextExceptions

from flext_grpc.models import FlextGrpcModels

# Exception type aliases
FlextGrpcError = FlextExceptions.BaseError
FlextGrpcSettingsurationError = FlextExceptions.ConfigurationError
FlextGrpcConnectionError = FlextExceptions.ConnectionError
FlextGrpcTimeoutError = FlextExceptions.TimeoutError
FlextGrpcValidationError = FlextExceptions.ValidationError

# Model type aliases
GrpcHealthCheck = FlextGrpcModels.Grpc.GrpcHealthCheck
GrpcRequest = FlextGrpcModels.Grpc.GrpcRequest
ServiceDefinition = FlextGrpcModels.Grpc.ServiceDefinition
ServiceMetrics = FlextGrpcModels.Grpc.ServiceMetrics
StreamInfo = FlextGrpcModels.Grpc.StreamInfo
StreamMetrics = FlextGrpcModels.Grpc.StreamMetrics

__all__ = [
    "FlextGrpcConnectionError",
    "FlextGrpcError",
    "FlextGrpcSettingsurationError",
    "FlextGrpcTimeoutError",
    "FlextGrpcValidationError",
    "GrpcHealthCheck",
    "GrpcRequest",
    "ServiceDefinition",
    "ServiceMetrics",
    "StreamInfo",
    "StreamMetrics",
]
