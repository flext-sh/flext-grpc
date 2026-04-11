"""Metrics collection service mixin for flext-grpc."""

from __future__ import annotations

import threading

from pydantic import Field

from flext_grpc import m, t, u


class FlextGrpcMetrics:
    """Mixin providing metrics collection for FlextGrpc facade."""

    class _MetricValueModel(m.Value):
        value: t.OptionalContainerValue = Field(
            description="Normalized metric measurement value"
        )

    class MetricsCollector:
        """Dedicated metrics collection with thread safety."""

        def __init__(self) -> None:
            """Initialize metrics collector with thread-safe storage."""
            super().__init__()
            self._metrics = m.Grpc.Payload(values={})
            self._lock = threading.RLock()

        def all_metrics(self) -> m.Grpc.Payload:
            """Get all metrics snapshot."""
            with self._lock:
                return m.Grpc.Payload(values=dict(self._metrics.values))

        def metric(self, key: str) -> t.OptionalContainerValue | None:
            """Thread-safe metric retrieval.

            Returns:
            Metric value or None if not found

            """
            with self._lock:
                return self._metrics.values.get(key)

        def record_metric(self, key: str, value: t.OptionalContainerValue) -> None:
            """Thread-safe metric recording.

            Args:
            key: Metric identifier
            value: Metric value (JSON-serializable: str, int, float, bool, list, dict, None)

            """

            def _normalize_value(
                val: t.OptionalContainerValue,
            ) -> t.OptionalContainerValue:
                if val is None:
                    return ""
                if u.primitive(val):
                    return val
                return str(val)

            with self._lock:
                normalized = FlextGrpcMetrics._MetricValueModel(value=value)
                json_val = _normalize_value(normalized.value)
                updated_values: dict[str, t.OptionalContainerValue] = dict(
                    self._metrics.values
                )
                updated_values[key] = json_val
                self._metrics = m.Grpc.Payload(values=updated_values)


__all__ = ["FlextGrpcMetrics"]
