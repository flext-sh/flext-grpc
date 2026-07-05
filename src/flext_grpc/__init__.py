# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports
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
from flext_grpc._exports import FLEXT_GRPC_LAZY_IMPORTS

if TYPE_CHECKING:
    from flext_core._root_typing_parts import d as d, e as e, h as h, r as r, x as x
    from flext_grpc.api import FlextGrpc as FlextGrpc, grpc as grpc
    from flext_grpc.base import FlextGrpcServiceBase as FlextGrpcServiceBase, s as s
    from flext_grpc.constants import FlextGrpcConstants as FlextGrpcConstants, c as c
    from flext_grpc.models import FlextGrpcModels as FlextGrpcModels, m as m
    from flext_grpc.protocols import FlextGrpcProtocols as FlextGrpcProtocols, p as p
    from flext_grpc.services.api_runtime import (
        FlextGrpcApiRuntime as FlextGrpcApiRuntime,
    )
    from flext_grpc.services.client import FlextGrpcClient as FlextGrpcClient
    from flext_grpc.services.connection_pool import (
        FlextGrpcConnectionPool as FlextGrpcConnectionPool,
    )
    from flext_grpc.services.metrics import FlextGrpcMetrics as FlextGrpcMetrics
    from flext_grpc.services.server import FlextGrpcServer as FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream as FlextGrpcStream
    from flext_grpc.settings import FlextGrpcSettings as FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes as FlextGrpcTypes, t as t
    from flext_grpc.utilities import FlextGrpcUtilities as FlextGrpcUtilities, u as u


_LAZY_IMPORTS = FLEXT_GRPC_LAZY_IMPORTS


_EAGER_EXPORTS = (
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
    __version_info__,
)


_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextGrpc",
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConnectionPool",
    "FlextGrpcConstants",
    "FlextGrpcMetrics",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceBase",
    "FlextGrpcSettings",
    "FlextGrpcStream",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "grpc",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
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

__all__: tuple[str, ...] = (
    "FlextGrpc",
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConnectionPool",
    "FlextGrpcConstants",
    "FlextGrpcMetrics",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceBase",
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
    "d",
    "e",
    "grpc",
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
    _LAZY_IMPORTS,
    public_exports=_PUBLIC_EXPORTS,
)
