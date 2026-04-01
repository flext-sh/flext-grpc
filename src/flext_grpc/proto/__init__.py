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
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_grpc.proto.stubs import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextGrpcServiceServicer": "flext_grpc.proto.stubs",
    "FlextGrpcServiceStub": "flext_grpc.proto.stubs",
    "add_FlextGrpcServiceServicer_to_server": "flext_grpc.proto.stubs",
    "stubs": "flext_grpc.proto.stubs",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
