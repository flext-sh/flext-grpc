"""Metrics collection service mixin for flext-grpc."""

from __future__ import annotations

import threading

from flext_grpc import m, t, u


class FlextGrpcMetrics:
    """Mixin providing metrics collection for FlextGrpc facade."""

    class _MetricValueModel(m.Value):
        value: t.OptionalContainerValueMapping

    class MetricsCollector:
        """Dedicated metrics collection with thread safety."""

        def __init__(self) -> None:
            """Initialize metrics collector with thread-safe storage."""
            super().__init__()
            self._metrics = m.Grpc.Payload(values={})
            self._lock = threading.RLock()

        def get_all_metrics(self) -> m.Grpc.Payload:
            """Get all metrics snapshot."""
            with self._lock:
                return m.Grpc.Payload(values=self._metrics.values.copy())

        def get_metric(self, key: str) -> t.OptionalContainerValueMapping | None:
            """Thread-safe metric retrieval.

            Returns:
            Metric value or None if not found

            """
            with self._lock:
                return self._metrics.values.get(key)

        def record_metric(
            self, key: str, value: t.OptionalContainerValueMapping
        ) -> None:
            """Thread-safe metric recording.

            Args:
            key: Metric identifier
            value: Metric value (JSON-serializable: str, int, float, bool, list, dict, None)

            """

            def _normalize_value(
                val: t.OptionalContainerValueMapping,
            ) -> t.OptionalContainerValueMapping:
                if val is None:
                    return ""
                if u.is_primitive(val):
                    return val
                return str(val)

            with self._lock:
                normalized = FlextGrpcMetrics._MetricValueModel(value=value)
                json_val = _normalize_value(normalized.value)
                self._metrics.values[key] = json_val


__all__ = ["FlextGrpcMetrics"]
