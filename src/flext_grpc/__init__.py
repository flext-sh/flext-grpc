"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextExceptions as e, d, h, r, s, x

    from flext_grpc import (
        FlextGrpc,
        FlextGrpcProtocols,
        FlextGrpcProtocols as p,
        FlextGrpcServices,
        FlextGrpcServiceStub,
        FlextGrpcSettings,
        __version__,
        __version_info__,
        c,
        m,
        t,
        u,
    )

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "FlextGrpc": ("flext_grpc.api", "FlextGrpc"),
    "FlextGrpcProtocols": ("flext_grpc.protocols", "FlextGrpcProtocols"),
    "FlextGrpcServiceStub": ("flext_grpc.proto", "FlextGrpcServiceStub"),
    "FlextGrpcServices": ("flext_grpc.services", "FlextGrpcServices"),
    "FlextGrpcSettings": ("flext_grpc.settings", "FlextGrpcSettings"),
    "__version__": ("flext_grpc.__version__", "__version__"),
    "__version_info__": ("flext_grpc.__version__", "__version_info__"),
    "c": ("flext_grpc.constants", "c"),
    "d": ("flext_core", "d"),
    "e": ("flext_core", "FlextExceptions"),
    "h": ("flext_core", "h"),
    "m": ("flext_grpc.models", "m"),
    "p": ("flext_grpc.protocols", "FlextGrpcProtocols"),
    "r": ("flext_core", "r"),
    "s": ("flext_core", "s"),
    "t": ("flext_grpc.typings", "t"),
    "u": ("flext_grpc.utilities", "u"),
    "x": ("flext_core", "x"),
}

__all__ = [
    "FlextGrpc",
    "FlextGrpcProtocols",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "__version__",
    "__version_info__",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
