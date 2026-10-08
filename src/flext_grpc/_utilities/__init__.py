# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Utilities package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._utilities.base import FlextGrpcUtilitiesBase
    from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc
    from flext_grpc._utilities.grpc_runtime import FlextGrpcUtilitiesGrpcRuntime
    from flext_grpc._utilities.grpc_service import FlextGrpcUtilitiesGrpcService


__all__: tuple[str, ...] = (
    "FlextGrpcUtilitiesBase",
    "FlextGrpcUtilitiesGrpc",
    "FlextGrpcUtilitiesGrpcRuntime",
    "FlextGrpcUtilitiesGrpcService",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcUtilitiesBase": ".base",
        "FlextGrpcUtilitiesGrpc": ".grpc",
        "FlextGrpcUtilitiesGrpcRuntime": ".grpc_runtime",
        "FlextGrpcUtilitiesGrpcService": ".grpc_service",
    }),
    public_exports=__all__,
)
