# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x

    from flext_grpc import services as services
    from flext_grpc.__version__ import (
        FlextGrpcVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_grpc._config import FlextGrpcConfig, config
    from flext_grpc._settings import FlextGrpcSettings, settings
    from flext_grpc.api import FlextGrpc, grpc
    from flext_grpc.base import FlextGrpcServiceBase, s
    from flext_grpc.cli import main
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.errors import FlextGrpcErrors
    from flext_grpc.models import FlextGrpcModels, m
    from flext_grpc.protocols import FlextGrpcProtocols, p
    from flext_grpc.typings import FlextGrpcTypes, t
    from flext_grpc.utilities import FlextGrpcUtilities, u


__all__: tuple[str, ...] = (
    "FlextGrpc",
    "FlextGrpcConfig",
    "FlextGrpcConstants",
    "FlextGrpcErrors",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceBase",
    "FlextGrpcSettings",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
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
    "services",
    "settings",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpc": ".api",
        "FlextGrpcConfig": "._config",
        "FlextGrpcConstants": ".constants",
        "FlextGrpcErrors": ".errors",
        "FlextGrpcModels": ".models",
        "FlextGrpcProtocols": ".protocols",
        "FlextGrpcServiceBase": ".base",
        "FlextGrpcSettings": "._settings",
        "FlextGrpcTypes": ".typings",
        "FlextGrpcUtilities": ".utilities",
        "FlextGrpcVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "c": ".constants",
        "config": "._config",
        "d": "flext_core",
        "e": "flext_core",
        "grpc": ".api",
        "h": "flext_core",
        "m": ".models",
        "main": ".cli",
        "p": ".protocols",
        "r": "flext_core",
        "s": ".base",
        "services": ".services",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_core",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_grpc.__version__ import __version__
