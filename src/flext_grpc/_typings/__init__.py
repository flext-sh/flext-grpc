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
    from flext_grpc._typings.grpc import ConfigDict, EntityKind, Headers


__all__: tuple[str, ...] = (
    "ConfigDict",
    "EntityKind",
    "FlextGrpcTypingsBase",
    "Headers",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "ConfigDict": ".grpc",
        "EntityKind": ".grpc",
        "FlextGrpcTypingsBase": ".base",
        "Headers": ".grpc",
    }),
    public_exports=__all__,
)
