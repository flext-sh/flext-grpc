"""FLEXT gRPC utilities facade."""

from __future__ import annotations

from flext_core import FlextUtilities

from flext_grpc import FlextGrpcUtilitiesGrpc


class FlextGrpcUtilities(FlextUtilities):
    """Utilities for gRPC operations in the FLEXT ecosystem."""

    class Grpc(FlextGrpcUtilitiesGrpc):
        """gRPC-specific utility namespace."""


u = FlextGrpcUtilities

__all__: list[str] = ["FlextGrpcUtilities", "u"]
