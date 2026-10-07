# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.proto package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc.proto.servicer import FlextGrpcProtoServicer
    from flext_grpc.proto.stub import FlextGrpcServiceStub


__all__: tuple[str, ...] = ("FlextGrpcProtoServicer", "FlextGrpcServiceStub")

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpcProtoServicer": ".servicer",
        "FlextGrpcServiceStub": ".stub",
    }),
    public_exports=__all__,
)
