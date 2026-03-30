# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Examples package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples import typings as typings

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "typings": ["examples.typings", ""],
}

_EXPORTS: Sequence[str] = [
    "typings",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
