"""Metrics collection service mixin for flext-grpc.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import ClassVar

from flext_grpc import m, s
from flext_grpc.services._entities.metrics_collector import (
    FlextGrpcMetricsCollectorImpl,
)


class FlextGrpcMetrics(s):
    """Mixin providing metrics collection for FlextGrpc facade."""

    MetricsCollector: ClassVar[type[FlextGrpcMetricsCollectorImpl]] = (
        FlextGrpcMetricsCollectorImpl
    )

    _metrics_collector: FlextGrpcMetricsCollectorImpl = m.PrivateAttr(
        default_factory=FlextGrpcMetricsCollectorImpl,
    )


__all__: list[str] = ["FlextGrpcMetrics", "FlextGrpcMetricsCollectorImpl"]
