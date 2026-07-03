"""FLEXT gRPC Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_cli import t


class FlextGrpcTypes(t):
    """gRPC-specific type definitions extending t via MRO."""

    class Grpc:
        """gRPC domain namespace (flat members per AGENTS.md §149)."""

        type EntityKind = Literal["server", "client", "channel", "service", "stream"]
        type Headers = t.StrMapping
        type ConfigDict = t.MappingKV[str, t.Scalar | t.JsonValue | None]


t = FlextGrpcTypes
__all__: list[str] = ["FlextGrpcTypes", "t"]
