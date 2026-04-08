# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc, grpc
_LAZY_IMPORTS = {
    "FlextGrpcUtilitiesGrpc": ("flext_grpc._utilities.grpc", "FlextGrpcUtilitiesGrpc"),
    "grpc": ("flext_grpc._utilities.grpc", "grpc"),
}

__all__ = [
    "FlextGrpcUtilitiesGrpc",
    "grpc",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
