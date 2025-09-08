"""FLEXT gRPC Domain Models.

This module provides the main domain models for gRPC communication,
following Clean Architecture and SOLID principles. Contains all entities
that represent the core domain concepts.
Copyright (c) 2025 FLEXT Team. All rights reserved.

SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

from flext_grpc.entities import (
    FlextGrpcChannel,
    FlextGrpcClient,
    FlextGrpcEntity,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)

__all__ = [
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcEntity",
    "FlextGrpcServer",
    "FlextGrpcService",
    "FlextGrpcStream",
]
