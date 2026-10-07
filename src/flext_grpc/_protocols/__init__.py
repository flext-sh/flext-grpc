# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._protocols.base import FlextGrpcProtocolsBase
    from flext_grpc._protocols.config import FlextGrpcProtocolsConfig


__all__: tuple[str, ...] = ("FlextGrpcProtocolsBase", "FlextGrpcProtocolsConfig")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcProtocolsBase": ".base",
        "FlextGrpcProtocolsConfig": ".config",
    }),
    public_exports=__all__,
)
