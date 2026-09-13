"""Metrics collection service mixin for flext-grpc."""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import m, s

from ._entities.metric_value import FlextGrpcMetricValueModel
from ._entities.metrics_collector import FlextGrpcMetricsCollectorImpl


class FlextGrpcMetrics(s):
    """Mixin providing metrics collection for FlextGrpc facade."""

    _FlextGrpcMetricValueModel: ClassVar[type[FlextGrpcMetricValueModel]] = (
        FlextGrpcMetricValueModel
    )
    MetricsCollector: ClassVar[type[FlextGrpcMetricsCollectorImpl]] = (
        FlextGrpcMetricsCollectorImpl
    )

    _metrics_collector: FlextGrpcMetricsCollectorImpl = m.PrivateAttr(
        default_factory=FlextGrpcMetricsCollectorImpl
    )


__all__: list[str] = ["FlextGrpcMetrics"]
