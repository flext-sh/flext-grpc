# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._models.base import FlextGrpcModelsBase
    from flext_grpc._models.config import FlextGrpcConfigModels
    from flext_grpc._models.metric_value import FlextGrpcMetricValueModel
    from flext_grpc._models.stream_state import FlextGrpcStreamRuntimeState


__all__: tuple[str, ...] = (
    "FlextGrpcConfigModels",
    "FlextGrpcMetricValueModel",
    "FlextGrpcModelsBase",
    "FlextGrpcStreamRuntimeState",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcConfigModels": ".config",
        "FlextGrpcMetricValueModel": ".metric_value",
        "FlextGrpcModelsBase": ".base",
        "FlextGrpcStreamRuntimeState": ".stream_state",
    }),
    public_exports=__all__,
)
