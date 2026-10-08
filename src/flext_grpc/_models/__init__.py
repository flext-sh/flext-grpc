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


__all__: tuple[str, ...] = ("FlextGrpcConfigModels", "FlextGrpcModelsBase")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcConfigModels": ".config",
        "FlextGrpcModelsBase": ".base",
    }),
    public_exports=__all__,
)
