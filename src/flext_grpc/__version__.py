# AUTO-GENERATED FILE — Regenerate with: make gen
"""Package version and metadata for flext-grpc.

Subclass of ``FlextVersion`` — overrides only ``_metadata``.
All derived attributes (``__version__``, ``__title__``, etc.) are
computed automatically via ``FlextVersion.__init_subclass__``.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from importlib.metadata import PackageMetadata, metadata
from typing import TYPE_CHECKING

from flext_core import FlextVersion

if TYPE_CHECKING:
    from flext_core import t


class FlextGrpcVersion(FlextVersion):
    """flext-grpc version — MRO-derived from FlextVersion."""

    _metadata: PackageMetadata | t.StrMapping = metadata("flext-grpc")


__version__ = FlextGrpcVersion.__version__
__version_info__ = FlextGrpcVersion.__version_info__
__title__ = FlextGrpcVersion.__title__
__description__ = FlextGrpcVersion.__description__
__author__ = FlextGrpcVersion.__author__
__author_email__ = FlextGrpcVersion.__author_email__
__license__ = FlextGrpcVersion.__license__
__url__ = FlextGrpcVersion.__url__
__all__: list[str] = [
    "FlextGrpcVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
]
