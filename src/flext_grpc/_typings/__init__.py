# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._typings.base import FlextGrpcTypingsBase
    from flext_grpc._typings.domain import FlextGrpcTypesDomain


__all__: tuple[str, ...] = ("FlextGrpcTypesDomain", "FlextGrpcTypingsBase")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcTypesDomain": ".domain",
        "FlextGrpcTypingsBase": ".base",
    }),
    public_exports=__all__,
)
