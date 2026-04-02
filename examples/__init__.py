# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Examples package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from examples import typings
    from flext_core import FlextTypes

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
    "typings": "examples.typings",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
