# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core import build_lazy_import_map, install_lazy_exports
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
    from flext_grpc.cli import FlextGrpcCli, main
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
    "FlextGrpcCli",
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

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextGrpcConfig", "config"),
            "._settings": ("FlextGrpcSettings", "settings"),
            ".api": ("FlextGrpc", "grpc"),
            ".base": ("FlextGrpcServiceBase", "s"),
            ".cli": ("FlextGrpcCli", "main"),
            ".constants": ("FlextGrpcConstants", "c"),
            ".errors": ("FlextGrpcErrors",),
            ".models": ("FlextGrpcModels", "m"),
            ".proto": ("proto",),
            ".proto.servicer": ("FlextGrpcProtoServicer",),
            ".proto.stub": ("FlextGrpcServiceStub",),
            ".protocols": ("FlextGrpcProtocols", "p"),
            ".services": ("services",),
            ".services.api_runtime": ("FlextGrpcApiRuntime",),
            ".services.client": ("FlextGrpcClient",),
            ".services.connection_pool": ("FlextGrpcConnectionPool",),
            ".services.metrics": ("FlextGrpcMetrics",),
            ".services.server": ("FlextGrpcServer",),
            ".services.stream": ("FlextGrpcStream",),
            ".typings": ("FlextGrpcTypes", "t"),
            ".utilities": ("FlextGrpcUtilities", "u"),
            "flext_core": ("d", "e", "h", "r", "x"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    ),
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
