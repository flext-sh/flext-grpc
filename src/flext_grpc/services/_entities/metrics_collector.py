"""Metrics collector implementation entity (ENFORCE-067: one class per module)."""

from __future__ import annotations

import threading

from flext_grpc import m, t, u

from .metric_value import FlextGrpcMetricValueModel


class FlextGrpcMetricsCollectorImpl:
    """Dedicated metrics collection with thread safety."""

    def __init__(self) -> None:
        """Initialize metrics collector with thread-safe storage."""
        super().__init__()
        self._metrics = m.Grpc.Payload(values={})
        self._lock = threading.RLock()

    def all_metrics(self) -> m.Grpc.Payload:
        """Get all metrics snapshot."""
        with self._lock:
            vals = self._metrics.values
            return m.Grpc.Payload(values=dict(vals))

    def metric(self, key: str) -> t.JsonValue | None:
        """Thread-safe metric retrieval.

        Returns:
        Metric value or None if not found

        """
        with self._lock:
            vals = self._metrics.values
            value: t.JsonValue | None = vals.get(key)
            return value

    def record_metric(self, key: str, value: t.JsonValue | None) -> None:
        """Thread-safe metric recording.

        Args:
        key: Metric identifier
        value: Metric value (JSON-serializable: str, int, float, bool, list, dict, None)

        """

        def _normalize_value(val: t.JsonValue | None) -> t.JsonValue | None:
            if val is None:
                return ""
            if u.primitive(val):
                return val
            return str(val)

        with self._lock:
            normalized = FlextGrpcMetricValueModel(value=value)
            json_val = _normalize_value(normalized.value)
            existing = self._metrics.values
            updated_values: t.MutableMappingKV[str, t.JsonValue | None] = dict(existing)
            updated_values[key] = json_val
            self._metrics = m.Grpc.Payload(values=updated_values)


__all__: list[str] = ["FlextGrpcMetricsCollectorImpl"]
