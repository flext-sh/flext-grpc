# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports

if TYPE_CHECKING:
    from examples.constants import ExamplesFlextGrpcConstants
    from examples.models import ExamplesFlextGrpcModels
    from examples.protocols import ExamplesFlextGrpcProtocols
    from examples.typings import ExamplesFlextGrpcTypes, t
    from examples.utilities import ExamplesFlextGrpcUtilities, u
    from flext_core import d, e, h, r, x
    from flext_grpc import c, m, p, s


__all__: tuple[str, ...] = (
    "ExamplesFlextGrpcConstants",
    "ExamplesFlextGrpcModels",
    "ExamplesFlextGrpcProtocols",
    "ExamplesFlextGrpcTypes",
    "ExamplesFlextGrpcUtilities",
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
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "ExamplesFlextGrpcConstants": ".constants",
        "ExamplesFlextGrpcModels": ".models",
        "ExamplesFlextGrpcProtocols": ".protocols",
        "ExamplesFlextGrpcTypes": ".typings",
        "ExamplesFlextGrpcUtilities": ".utilities",
        "c": "flext_grpc",
        "d": "flext_core",
        "e": "flext_core",
        "h": "flext_core",
        "m": "flext_grpc",
        "p": "flext_grpc",
        "r": "flext_core",
        "s": "flext_grpc",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_core",
    }),
    public_exports=__all__,
)
