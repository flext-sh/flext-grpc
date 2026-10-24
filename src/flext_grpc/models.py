# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_grpc._models import (
    FlextGrpcConfigModels,
    FlextGrpcModelsBase,
    FlextGrpcModelsChannel,
    FlextGrpcModelsMessage,
    FlextGrpcModelsRuntime,
)


class FlextGrpcModels(FlextCliModels):
    """gRPC domain models extending flext-core m.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Grpc(
        FlextGrpcModelsBase,
        FlextGrpcModelsChannel,
        FlextGrpcConfigModels,
        FlextGrpcModelsMessage,
        FlextGrpcModelsRuntime,
    ):
        """Domain models for gRPC core business entities."""


m = FlextGrpcModels

__all__: list[str] = ["FlextGrpcModels", "m"]
