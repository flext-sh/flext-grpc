# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

if _t.TYPE_CHECKING:
    from examples.typings import (
        CompleteSetup,
        ExamplesFlextGrpcTypes,
        ExamplesFlextGrpcTypes as t,
    )
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import r
    from flext_core.service import s
    from flext_core.utilities import FlextUtilities as u
_LAZY_IMPORTS = build_lazy_import_map(
    {
        ".typings": (
            "CompleteSetup",
            "ExamplesFlextGrpcTypes",
        ),
        "flext_core.decorators": ("d",),
        "flext_core.exceptions": ("e",),
        "flext_core.handlers": ("h",),
        "flext_core.mixins": ("x",),
        "flext_core.result": ("r",),
        "flext_core.service": ("s",),
    },
    alias_groups={
        ".typings": (("t", "ExamplesFlextGrpcTypes"),),
        "flext_core.constants": (("c", "FlextConstants"),),
        "flext_core.models": (("m", "FlextModels"),),
        "flext_core.protocols": (("p", "FlextProtocols"),),
        "flext_core.utilities": (("u", "FlextUtilities"),),
    },
)

__all__ = [
    "CompleteSetup",
    "ExamplesFlextGrpcTypes",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
