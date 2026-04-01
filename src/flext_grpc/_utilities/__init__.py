# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""FLEXT gRPC utilities submodules."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_grpc.services import FlextGrpcServices

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextGrpcServices": ["flext_grpc.services", "FlextGrpcServices"],
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
