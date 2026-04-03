# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Utilities package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_grpc import grpc
    from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc, logger

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "FlextGrpcUtilitiesGrpc": "flext_grpc.grpc",
    "grpc": "flext_grpc.grpc",
    "logger": "flext_grpc.grpc",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
