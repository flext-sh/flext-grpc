"""FLEXT gRPC Types.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import Literal

from flext_cli import FlextCliTypes

from ._typings.base import FlextGrpcTypingsBase


class FlextGrpcTypes(FlextCliTypes):
    """gRPC-specific type definitions extending t via MRO."""

    class Grpc(FlextGrpcTypingsBase):
        """gRPC domain namespace (flat members per AGENTS.md §149)."""

        type EntityKind = Literal["server", "client", "channel", "service", "stream"]
        type Headers = FlextCliTypes.StrMapping
        type ConfigDict = FlextCliTypes.MappingKV[
            str, FlextCliTypes.Scalar | FlextCliTypes.JsonValue | None
        ]


t = FlextGrpcTypes
__all__: list[str] = ["FlextGrpcTypes", "t"]
