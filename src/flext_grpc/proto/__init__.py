"""FLEXT gRPC Proto Stubs - Service definitions and message types.

Provides Pydantic-based message types and service stubs for gRPC operations.
These are used by services.py until full protobuf code generation is in place.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import t
from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_grpc.proto.stubs import (
        EchoRequest,
        EchoResponse,
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        HealthRequest,
        HealthResponse,
        add_FlextGrpcServiceServicer_to_server,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "EchoRequest": ("flext_grpc.proto.stubs", "EchoRequest"),
    "EchoResponse": ("flext_grpc.proto.stubs", "EchoResponse"),
    "FlextGrpcServiceServicer": ("flext_grpc.proto.stubs", "FlextGrpcServiceServicer"),
    "FlextGrpcServiceStub": ("flext_grpc.proto.stubs", "FlextGrpcServiceStub"),
    "HealthRequest": ("flext_grpc.proto.stubs", "HealthRequest"),
    "HealthResponse": ("flext_grpc.proto.stubs", "HealthResponse"),
    "add_FlextGrpcServiceServicer_to_server": (
        "flext_grpc.proto.stubs",
        "add_FlextGrpcServiceServicer_to_server",
    ),
}

__all__ = [
    "EchoRequest",
    "EchoResponse",
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "HealthRequest",
    "HealthResponse",
    "add_FlextGrpcServiceServicer_to_server",
]


def __getattr__(name: str) -> t.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
