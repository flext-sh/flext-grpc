# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_grpc._utilities.grpc as _flext_grpc__utilities_grpc

    grpc = _flext_grpc__utilities_grpc
    from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc, logger
_LAZY_IMPORTS = {
    "FlextGrpcUtilitiesGrpc": "flext_grpc._utilities.grpc",
    "grpc": "flext_grpc._utilities.grpc",
    "logger": "flext_grpc._utilities.grpc",
}

__all__ = [
    "FlextGrpcUtilitiesGrpc",
    "grpc",
    "logger",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
