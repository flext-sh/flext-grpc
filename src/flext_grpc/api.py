"""FLEXT gRPC - Generic Unified Facade with Patterns.

Generic facade using extensive Pydantic models, SOLID delegation,
functional composition, and Python 3.13+ patterns for minimal code.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from flext_grpc.services.api_runtime import FlextGrpcApiRuntime
from flext_grpc.services.client import FlextGrpcClient
from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
from flext_grpc.services.metrics import FlextGrpcMetrics
from flext_grpc.services.server import FlextGrpcServer
from flext_grpc.services.stream import FlextGrpcStream


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

    pass


grpc = FlextGrpc.fetch_global()

__all__: list[str] = ["FlextGrpc", "grpc"]
