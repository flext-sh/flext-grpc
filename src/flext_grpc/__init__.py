# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
from flext_grpc.__version__ import *

if _t.TYPE_CHECKING:
    from _utilities.grpc import FlextGrpcUtilitiesGrpc, grpc

    from flext_core.decorators import d
    from flext_core.exceptions import e
    from flext_core.handlers import h
    from flext_core.mixins import x
    from flext_core.result import r
    from flext_core.service import s
    from flext_grpc.api import FlextGrpc
    from flext_grpc.client import FlextGrpcClient
    from flext_grpc.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.errors import (
        FlextGrpcConfigurationError,
        FlextGrpcConnectionError,
        FlextGrpcError,
        FlextGrpcTimeoutError,
        FlextGrpcValidationError,
    )
    from flext_grpc.metrics import FlextGrpcMetrics
    from flext_grpc.models import FlextGrpcModels, m
    from flext_grpc.protocols import FlextGrpcProtocols, p
    from flext_grpc.server import FlextGrpcServer
    from flext_grpc.settings import FlextGrpcSettings
    from flext_grpc.stream import FlextGrpcStream
    from flext_grpc.stubs import (
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server,
    )
    from flext_grpc.typings import FlextGrpcTypes, t
    from flext_grpc.utilities import FlextGrpcUtilities, u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "._utilities",
        ".proto",
        ".services",
    ),
    build_lazy_import_map(
        {
            ".__version__": (
                "__author__",
                "__author_email__",
                "__description__",
                "__license__",
                "__title__",
                "__url__",
                "__version__",
                "__version_info__",
            ),
            ".api": ("FlextGrpc",),
            ".client": ("FlextGrpcClient",),
            ".connection_pool": ("FlextGrpcConnectionPool",),
            ".constants": (
                "FlextGrpcConstants",
                "c",
            ),
            ".errors": (
                "FlextGrpcConfigurationError",
                "FlextGrpcConnectionError",
                "FlextGrpcError",
                "FlextGrpcTimeoutError",
                "FlextGrpcValidationError",
            ),
            ".metrics": ("FlextGrpcMetrics",),
            ".models": (
                "FlextGrpcModels",
                "m",
            ),
            ".protocols": (
                "FlextGrpcProtocols",
                "p",
            ),
            ".server": ("FlextGrpcServer",),
            ".settings": ("FlextGrpcSettings",),
            ".stream": ("FlextGrpcStream",),
            ".stubs": (
                "FlextGrpcServiceServicer",
                "FlextGrpcServiceStub",
                "add_FlextGrpcServiceServicer_to_server",
            ),
            ".typings": (
                "FlextGrpcTypes",
                "t",
            ),
            ".utilities": (
                "FlextGrpcUtilities",
                "u",
            ),
            "_utilities.grpc": (
                "FlextGrpcUtilitiesGrpc",
                "grpc",
            ),
            "flext_core.decorators": ("d",),
            "flext_core.exceptions": ("e",),
            "flext_core.handlers": ("h",),
            "flext_core.mixins": ("x",),
            "flext_core.result": ("r",),
            "flext_core.service": ("s",),
        },
    ),
    exclude_names=(
        "cleanup_submodule_namespace",
        "install_lazy_exports",
        "lazy_getattr",
        "logger",
        "merge_lazy_imports",
        "output",
        "output_reporting",
    ),
    module_name=__name__,
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)

__all__ = [
    "FlextGrpc",
    "FlextGrpcClient",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcConnectionPool",
    "FlextGrpcConstants",
    "FlextGrpcError",
    "FlextGrpcMetrics",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "FlextGrpcSettings",
    "FlextGrpcStream",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcUtilitiesGrpc",
    "FlextGrpcValidationError",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "add_FlextGrpcServiceServicer_to_server",
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
]
