"""Metric value model entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_grpc.typings import t


class FlextGrpcMetricValueModel(FlextCliModels.Value):
    """Normalized metric measurement value model."""

    value: t.JsonValue | None = FlextCliModels.Field(
        description="Normalized metric measurement value",
    )


__all__: list[str] = ["FlextGrpcMetricValueModel"]
