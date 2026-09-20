# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import (
    __author__ as __author__, __author_email__ as __author_email__, __description__ as __description__, __license__ as __license__,
    __title__ as __title__, __url__ as __url__, __version__ as __version__, __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_core import d, e, h, r, x

    from . import proto, services
    from ._config import FlextGrpcConfig, config
    from ._settings import FlextGrpcSettings, settings
    from .api import FlextGrpc, grpc
    from .base import FlextGrpcServiceBase, FlextGrpcServiceBase as s
    from .cli import FlextGrpcCli
    from .constants import FlextGrpcConstants, FlextGrpcConstants as c
    from .errors import FlextGrpcErrors
    from .models import FlextGrpcModels, FlextGrpcModels as m
    from .proto.servicer import FlextGrpcProtoServicer
    from .proto.stub import FlextGrpcServiceStub
    from .protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
    from .services.api_runtime import FlextGrpcApiRuntime
    from .services.client import FlextGrpcClient
    from .services.connection_pool import FlextGrpcConnectionPool
    from .services.metrics import FlextGrpcMetrics
    from .services.server import FlextGrpcServer
    from .services.stream import FlextGrpcStream
    from .typings import FlextGrpcTypes, FlextGrpcTypes as t
    from .utilities import FlextGrpcUtilities, FlextGrpcUtilities as u
__all__: tuple[str, ...] = (
    "FlextGrpc", "FlextGrpcApiRuntime", "FlextGrpcCli", "FlextGrpcClient",
    "FlextGrpcConfig", "FlextGrpcConnectionPool", "FlextGrpcConstants", "FlextGrpcErrors",
    "FlextGrpcMetrics", "FlextGrpcModels", "FlextGrpcProtoServicer", "FlextGrpcProtocols",
    "FlextGrpcServer", "FlextGrpcServiceBase", "FlextGrpcServiceStub", "FlextGrpcSettings",
    "FlextGrpcStream", "FlextGrpcTypes", "FlextGrpcUtilities", "__author__",
    "__author_email__", "__description__", "__license__", "__title__",
    "__url__", "__version__", "__version_info__", "c",
    "config", "d", "e", "grpc",
    "h", "m", "p", "proto",
    "r", "s", "services", "settings",
    "t", "u", "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextGrpcConfig", "config"),
            "._settings": ("FlextGrpcSettings", "settings"),
            ".api": ("FlextGrpc", "grpc"),
            ".base": ("FlextGrpcServiceBase", "s"),
            ".cli": ("FlextGrpcCli",),
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
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
