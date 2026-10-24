"""FLEXT gRPC domain type aliases.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Literal

from flext_cli import FlextCliTypes
from flext_core import c

type EntityKind = Literal[
    "server", "client", "channel", "service", c.ProcessingMode.STREAM
]
type Headers = FlextCliTypes.StrMapping
type ConfigDict = FlextCliTypes.MappingKV[
    str,
    FlextCliTypes.Scalar | FlextCliTypes.JsonValue | None,
]

__all__: list[str] = ["ConfigDict", "EntityKind", "Headers"]
