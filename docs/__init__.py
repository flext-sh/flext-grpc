# AUTO-GENERATED FILE — Regenerate with: make gen
"""Docs package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x

    from flext_grpc import c, config, grpc, m, main, p, s, settings, t, u


__all__: tuple[str, ...] = (
    "c",
    "config",
    "d",
    "e",
    "grpc",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "c": "flext_grpc",
        "config": "flext_grpc",
        "d": "flext_core",
        "e": "flext_core",
        "grpc": "flext_grpc",
        "h": "flext_core",
        "m": "flext_grpc",
        "main": "flext_grpc",
        "p": "flext_grpc",
        "r": "flext_core",
        "s": "flext_grpc",
        "settings": "flext_grpc",
        "t": "flext_grpc",
        "u": "flext_grpc",
        "x": "flext_core",
    },
    public_exports=__all__,
)
