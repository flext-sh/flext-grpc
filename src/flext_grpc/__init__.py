# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import install_lazy_exports
from flext_grpc.__version__ import (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x
    from flext_grpc import proto, services
    from flext_grpc._config import FlextGrpcConfig, config
    from flext_grpc._settings import FlextGrpcSettings, settings
    from flext_grpc.api import FlextGrpc, grpc
    from flext_grpc.base import FlextGrpcServiceBase, s
    from flext_grpc.cli import main
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.errors import FlextGrpcErrors
    from flext_grpc.models import FlextGrpcModels, m
    from flext_grpc.proto.servicer import FlextGrpcProtoServicer
    from flext_grpc.proto.stub import FlextGrpcServiceStub
    from flext_grpc.protocols import FlextGrpcProtocols, p
    from flext_grpc.services.api_runtime import FlextGrpcApiRuntime
    from flext_grpc.services.client import FlextGrpcClient
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.services.metrics import FlextGrpcMetrics
    from flext_grpc.services.server import FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream
    from flext_grpc.typings import FlextGrpcTypes, t
    from flext_grpc.utilities import FlextGrpcUtilities, u


__all__: tuple[str, ...] = (
    "FlextGrpc",
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConfig",
    "FlextGrpcConnectionPool",
    "FlextGrpcConstants",
    "FlextGrpcErrors",
    "FlextGrpcMetrics",
    "FlextGrpcModels",
    "FlextGrpcProtoServicer",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceBase",
    "FlextGrpcServiceStub",
    "FlextGrpcSettings",
    "FlextGrpcStream",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
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
    "proto",
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
        "FlextGrpcApiRuntime": ".services.api_runtime",
        "FlextGrpcClient": ".services.client",
        "FlextGrpcConfig": "._config",
        "FlextGrpcConnectionPool": ".services.connection_pool",
        "FlextGrpcConstants": ".constants",
        "FlextGrpcErrors": ".errors",
        "FlextGrpcMetrics": ".services.metrics",
        "FlextGrpcModels": ".models",
        "FlextGrpcProtoServicer": ".proto.servicer",
        "FlextGrpcProtocols": ".protocols",
        "FlextGrpcServer": ".services.server",
        "FlextGrpcServiceBase": ".base",
        "FlextGrpcServiceStub": ".proto.stub",
        "FlextGrpcSettings": "._settings",
        "FlextGrpcStream": ".services.stream",
        "FlextGrpcTypes": ".typings",
        "FlextGrpcUtilities": ".utilities",
        "c": ".constants",
        "config": "._config",
        "d": "flext_core",
        "e": "flext_core",
        "grpc": ".api",
        "h": "flext_core",
        "m": ".models",
        "main": ".cli",
        "p": ".protocols",
        "proto": ".proto",
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
