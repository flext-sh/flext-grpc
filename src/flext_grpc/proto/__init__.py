# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT gRPC Proto Stubs - Service definitions and message types.

Provides Pydantic-based message types and service stubs for gRPC operations.
These are used by services.py until full protobuf code generation is in place.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc.proto import stubs as stubs
    from flext_grpc.proto.stubs import (
        FlextGrpcServiceServicer as FlextGrpcServiceServicer,
        FlextGrpcServiceStub as FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server as add_FlextGrpcServiceServicer_to_server,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextGrpcServiceServicer": ["flext_grpc.proto.stubs", "FlextGrpcServiceServicer"],
    "FlextGrpcServiceStub": ["flext_grpc.proto.stubs", "FlextGrpcServiceStub"],
    "add_FlextGrpcServiceServicer_to_server": [
        "flext_grpc.proto.stubs",
        "add_FlextGrpcServiceServicer_to_server",
    ],
    "stubs": ["flext_grpc.proto.stubs", ""],
}

_EXPORTS: Sequence[str] = [
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "add_FlextGrpcServiceServicer_to_server",
    "stubs",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
