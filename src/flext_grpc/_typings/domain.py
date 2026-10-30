"""FLEXT gRPC domain type aliases.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Literal

from flext_cli import FlextCliTypes

from flext_grpc import c


class FlextGrpcTypesDomain:
    EntityKind = Literal[
        "server", "client", "channel", "service", c.ProcessingMode.STREAM
    ]
    Headers = Mapping[str, str]
    ConfigDict = Mapping[
        str,
        FlextCliTypes.Scalar | FlextCliTypes.JsonValue | None,
    ]


__all__: list[str] = ["FlextGrpcTypesDomain"]
