"""Metric value model entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc.models import m
from flext_grpc.typings import t
from flext_grpc.utilities import u


class FlextGrpcMetricValueModel(m.Value):
    """Normalized metric measurement value model."""

    value: t.JsonValue | None = u.Field(
        description="Normalized metric measurement value",
    )


__all__: list[str] = ["FlextGrpcMetricValueModel"]
