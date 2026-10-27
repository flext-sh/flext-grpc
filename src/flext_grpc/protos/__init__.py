# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc.protos package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_grpc.protos.flext_pb2 import (
    DESCRIPTOR,
    EchoRequest,
    EchoResponse,
    HealthRequest,
    HealthResponse,
)
from flext_grpc.protos.flext_pb2_grpc import (
    GRPC_GENERATED_VERSION,
    RPC_PYTHON_METHOD_NAMES,
    FlextGrpcServiceServicer,
    FlextGrpcServiceStub,
    add_flext_grpc_service_servicer_to_server,
)

__all__: tuple[str, ...] = (
    "DESCRIPTOR",
    "GRPC_GENERATED_VERSION",
    "RPC_PYTHON_METHOD_NAMES",
    "EchoRequest",
    "EchoResponse",
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "HealthRequest",
    "HealthResponse",
    "add_flext_grpc_service_servicer_to_server",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "DESCRIPTOR": ".flext_pb2",
        "GRPC_GENERATED_VERSION": ".flext_pb2_grpc",
        "RPC_PYTHON_METHOD_NAMES": ".flext_pb2_grpc",
        "EchoRequest": ".flext_pb2",
        "EchoResponse": ".flext_pb2",
        "FlextGrpcServiceServicer": ".flext_pb2_grpc",
        "FlextGrpcServiceStub": ".flext_pb2_grpc",
        "HealthRequest": ".flext_pb2",
        "HealthResponse": ".flext_pb2",
        "add_flext_grpc_service_servicer_to_server": ".flext_pb2_grpc",
    }),
    public_exports=__all__,
)
