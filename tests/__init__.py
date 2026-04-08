# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Tests package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from tests.constants import TestsFlextGrpcConstants, TestsFlextGrpcConstants as c
    from tests.models import TestsFlextGrpcModels, TestsFlextGrpcModels as m
    from tests.protocols import TestsFlextGrpcProtocols, TestsFlextGrpcProtocols as p
    from tests.typings import TestsFlextGrpcTypes, TestsFlextGrpcTypes as t
    from tests.utilities import TestsFlextGrpcUtilities, TestsFlextGrpcUtilities as u
_LAZY_IMPORTS = {
    "TestsFlextGrpcConstants": ("tests.constants", "TestsFlextGrpcConstants"),
    "TestsFlextGrpcModels": ("tests.models", "TestsFlextGrpcModels"),
    "TestsFlextGrpcProtocols": ("tests.protocols", "TestsFlextGrpcProtocols"),
    "TestsFlextGrpcTypes": ("tests.typings", "TestsFlextGrpcTypes"),
    "TestsFlextGrpcUtilities": ("tests.utilities", "TestsFlextGrpcUtilities"),
    "c": ("tests.constants", "TestsFlextGrpcConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("tests.models", "TestsFlextGrpcModels"),
    "p": ("tests.protocols", "TestsFlextGrpcProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "t": ("tests.typings", "TestsFlextGrpcTypes"),
    "u": ("tests.utilities", "TestsFlextGrpcUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcUtilities",
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
