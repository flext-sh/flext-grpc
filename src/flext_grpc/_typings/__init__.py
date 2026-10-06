# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Typings package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._typings.base import FlextGrpcTypingsBase


__all__: tuple[str, ...] = ("FlextGrpcTypingsBase",)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({"FlextGrpcTypingsBase": ".base"}),
    public_exports=__all__,
)
