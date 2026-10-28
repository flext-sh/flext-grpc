"""Metrics collector implementation entity (ENFORCE-067: one class per module).

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

import threading
from collections.abc import MutableMapping

from flext_grpc import m, t, u


class FlextGrpcMetricsCollectorImpl:
    """Dedicated metrics collection with thread safety."""

    def __init__(self) -> None:
        """Initialize metrics collector with thread-safe storage."""
        super().__init__()
        self._metrics = m.Grpc.Payload(values={})
        self._lock = threading.RLock()

    def all_metrics(self) -> m.Grpc.Payload:
        """Get all metrics snapshot.

        Returns:
            The resulting ``m.Grpc.Payload``.

        """
        with self._lock:
            vals = self._metrics.values
            return m.Grpc.Payload(values=dict(vals))

    def metric(self, key: str) -> t.JsonValue | None:
        """Retrieve one metric by key in a thread-safe manner.

        Args:
            key: Metric identifier.

        Returns:
            Metric value, or ``None`` when the key is unknown.

        """
        with self._lock:
            vals = self._metrics.values
            value: t.JsonValue | None = vals.get(key)
            return value

    def record_metric(self, key: str, value: t.JsonValue | None) -> None:
        """Record one metric value in a thread-safe manner.

        Args:
            key: Metric identifier.
            value: JSON-serializable metric value.

        """

        def _normalize_value(val: t.JsonValue | None) -> t.JsonValue | None:
            if val is None:
                return ""
            if u.primitive(val):
                return val
            return str(val)

        with self._lock:
            normalized = m.Grpc.Payload(values={key: value})
            json_val = _normalize_value(normalized.values[key])
            existing = self._metrics.values
            updated_values: MutableMapping[str, t.JsonValue | None] = dict(existing)
            updated_values[key] = json_val
            self._metrics = m.Grpc.Payload(values=updated_values)


__all__: list[str] = ["FlextGrpcMetricsCollectorImpl"]
