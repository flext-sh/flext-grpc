# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Internal utilities subpackage."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes

    from flext_grpc._utilities import grpc
    from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc, logger

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextGrpcUtilitiesGrpc": "flext_grpc._utilities.grpc",
    "grpc": "flext_grpc._utilities.grpc",
    "logger": "flext_grpc._utilities.grpc",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
