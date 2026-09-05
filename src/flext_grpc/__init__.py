# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from . import proto as proto
    from . import services as services
    from enum import StrEnum, unique
    from flext_core import FlextConstants, d, h, r, x
    from typing import ClassVar, Final, TYPE_CHECKING

    from ._config import FlextGrpcConfig, config
    from ._settings import FlextGrpcSettings, settings
    from .api import FlextGrpc, grpc
    from .base import FlextGrpcServiceBase, FlextGrpcServiceBase as s
    from .constants import FlextGrpcConstants, FlextGrpcConstants as c
    from .errors import FlextGrpcErrors, e
    from .models import FlextGrpcModels, FlextGrpcModels as m
    from .proto.stubs import (
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        add_flext_grpc_service_servicer_to_server,
    )
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
    "TYPE_CHECKING",
    "ClassVar",
    "Final",
    "FlextConstants",
    "FlextGrpc",
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConfig",
    "FlextGrpcConnectionPool",
    "FlextGrpcConstants",
    "FlextGrpcErrors",
    "FlextGrpcMetrics",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceBase",
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "FlextGrpcSettings",
    "FlextGrpcStream",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "StrEnum",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "add_flext_grpc_service_servicer_to_server",
    "c",
    "config",
    "d",
    "e",
    "grpc",
    "h",
    "m",
    "p",
    "proto",
    "r",
    "s",
    "services",
    "settings",
    "t",
    "u",
    "unique",
    "x",
)

_LAZY_IMPORTS = MappingProxyType(
    build_lazy_import_map(
        MappingProxyType({
            "._config": ("FlextGrpcConfig", "config"),
            "._settings": ("FlextGrpcSettings", "settings"),
            ".api": ("FlextGrpc", "grpc"),
            ".base": ("FlextGrpcServiceBase", "s"),
            ".constants": ("FlextGrpcConstants", "c"),
            ".errors": ("FlextGrpcErrors", "e"),
            ".models": ("FlextGrpcModels", "m"),
            ".proto": ("proto",),
            ".proto.stubs": (
                "FlextGrpcServiceServicer",
                "FlextGrpcServiceStub",
                "add_flext_grpc_service_servicer_to_server",
            ),
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
            "enum": ("StrEnum", "unique"),
            "flext_core": ("FlextConstants", "d", "h", "r", "x"),
            "typing": ("ClassVar", "Final", "TYPE_CHECKING"),
        }),
        alias_groups=MappingProxyType({}),
        sort_keys=False,
    )
)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
