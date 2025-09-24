"""Models for gRPC operations.

This module provides data models for gRPC operations.
"""

from flext_core import FlextModels


class FlextGrpcModels:
    """Models for gRPC operations."""

    Core = FlextModels

    GrpcMessage = dict[str, object]
    GrpcMessages = list[GrpcMessage]
    FlextGrpcChannel = object  # Placeholder for gRPC channel type
