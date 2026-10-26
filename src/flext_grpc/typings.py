# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT gRPC Types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import t

from flext_grpc._typings import FlextGrpcTypingsBase, grpc as _grpc_types


class FlextGrpcTypes(t):
    """gRPC-specific type definitions extending t via MRO."""

    class Grpc(FlextGrpcTypingsBase):
        """gRPC domain namespace (flat members per AGENTS.md §149)."""

        EntityKind = _grpc_types.EntityKind
        Headers = _grpc_types.Headers
        ConfigDict = _grpc_types.ConfigDict


t = FlextGrpcTypes
__all__: list[str] = ["FlextGrpcTypes", "t"]
