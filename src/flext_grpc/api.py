"""FLEXT gRPC - Generic Unified Facade with Patterns.

Generic facade using extensive Pydantic models, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc.services import (
    FlextGrpcApiRuntime,
    FlextGrpcClient,
    FlextGrpcConnectionPool,
    FlextGrpcMetrics,
    FlextGrpcServer,
    FlextGrpcStream,
)


class FlextGrpc(
    FlextGrpcApiRuntime,
    FlextGrpcMetrics,
    FlextGrpcConnectionPool,
    FlextGrpcServer,
    FlextGrpcClient,
    FlextGrpcStream,
):
    """Generic unified gRPC facade with SOLID patterns and minimal code.

    Uses MRO composition from service mixins, functional composition,
    Pydantic v2 models, and delegation to reduce bloat while maintaining
    full functionality with Python 3.13+ features.
    """


grpc: FlextGrpc = FlextGrpc.fetch_global()
"""Shared FlextGrpc facade instance."""

__all__: list[str] = ["FlextGrpc", "grpc"]
