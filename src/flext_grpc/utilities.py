"""FLEXT gRPC utilities facade."""

from __future__ import annotations

from flext_cli import u
from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc


class FlextGrpcUtilities(u, FlextGrpcUtilitiesGrpc):
    """Utilities for gRPC operations in the FLEXT ecosystem."""

    class Grpc(FlextGrpcUtilitiesGrpc):
        """gRPC-specific utility namespace."""


u = FlextGrpcUtilities

__all__: list[str] = ["FlextGrpcUtilities", "u"]
