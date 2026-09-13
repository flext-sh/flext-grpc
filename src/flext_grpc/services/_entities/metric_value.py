"""Metric value model entity (ENFORCE-067: one class per module)."""

from __future__ import annotations

from flext_grpc import m, t, u


class FlextGrpcMetricValueModel(m.Value):
    """Normalized metric measurement value model."""

    value: t.JsonValue | None = u.Field(
        description="Normalized metric measurement value"
    )


__all__: list[str] = ["FlextGrpcMetricValueModel"]
