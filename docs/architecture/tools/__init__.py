# AUTO-GENERATED FILE — Regenerate with: make gen
"""Docs.architecture.tools package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if TYPE_CHECKING:
    from .validate_docs import (
        ArchitectureValidator,
        ValidationResults,
        ValidationSummary,
    )
__all__: tuple[str, ...] = (
    "ArchitectureValidator",
    "ValidationResults",
    "ValidationSummary",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType(
        build_lazy_import_map(
            MappingProxyType({
                ".validate_docs": (
                    "ArchitectureValidator",
                    "ValidationResults",
                    "ValidationSummary",
                )
            }),
            alias_groups=MappingProxyType({}),
            sort_keys=False,
        )
    ),
    public_exports=__all__,
)
