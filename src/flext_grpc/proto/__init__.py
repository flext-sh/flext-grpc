# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""FLEXT gRPC Proto Stubs - Service definitions and message types.

Provides Pydantic-based message types and service stubs for gRPC operations.
These are used by services.py until full protobuf code generation is in place.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_grpc.proto.stubs import (
        EchoRequest,
        EchoResponse,
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        HealthRequest,
        HealthResponse,
        add_FlextGrpcServiceServicer_to_server,
    )

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "EchoRequest": ("flext_grpc.proto.stubs", "EchoRequest"),
    "EchoResponse": ("flext_grpc.proto.stubs", "EchoResponse"),
    "FlextGrpcServiceServicer": ("flext_grpc.proto.stubs", "FlextGrpcServiceServicer"),
    "FlextGrpcServiceStub": ("flext_grpc.proto.stubs", "FlextGrpcServiceStub"),
    "HealthRequest": ("flext_grpc.proto.stubs", "HealthRequest"),
    "HealthResponse": ("flext_grpc.proto.stubs", "HealthResponse"),
    "add_FlextGrpcServiceServicer_to_server": ("flext_grpc.proto.stubs", "add_FlextGrpcServiceServicer_to_server"),
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


_LAZY_CACHE: dict[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
