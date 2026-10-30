# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT gRPC Types.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import t as flext_cli_t

from flext_grpc._typings import FlextGrpcTypesDomain, FlextGrpcTypingsBase


class FlextGrpcTypes(flext_cli_t):
    """gRPC-specific type definitions extending t via MRO."""

    class Grpc(FlextGrpcTypingsBase, FlextGrpcTypesDomain):
        """gRPC domain namespace (flat members per AGENTS.md §149)."""


t = FlextGrpcTypes
__all__: list[str] = ["FlextGrpcTypes", "t"]
