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
    from flext_core import d, e, h, r, s, x

    from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc
    from flext_grpc.api import FlextGrpc, grpc
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.errors import (
        FlextGrpcConfigurationError,
        FlextGrpcConnectionError,
        FlextGrpcError,
        FlextGrpcTimeoutError,
        FlextGrpcValidationError,
    )
    from flext_grpc.models import FlextGrpcModels, m
    from flext_grpc.proto.stubs import (
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server,
    )
    from flext_grpc.protocols import FlextGrpcProtocols, p
    from flext_grpc.services.api_runtime import FlextGrpcApiRuntime
    from flext_grpc.services.client import FlextGrpcClient
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.services.metrics import FlextGrpcMetrics
    from flext_grpc.services.server import FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream
    from flext_grpc.settings import FlextGrpcSettings
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
            "._utilities.grpc": ("FlextGrpcUtilitiesGrpc",),
            ".api": (
                "FlextGrpc",
                "grpc",
            ),
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
            ".models": (
                "FlextGrpcModels",
                "m",
            ),
            ".proto.stubs": (
                "FlextGrpcServiceServicer",
                "FlextGrpcServiceStub",
                "add_FlextGrpcServiceServicer_to_server",
            ),
            ".protocols": (
                "FlextGrpcProtocols",
                "p",
            ),
            ".services.api_runtime": ("FlextGrpcApiRuntime",),
            ".services.client": ("FlextGrpcClient",),
            ".services.connection_pool": ("FlextGrpcConnectionPool",),
            ".services.metrics": ("FlextGrpcMetrics",),
            ".services.server": ("FlextGrpcServer",),
            ".services.stream": ("FlextGrpcStream",),
            ".settings": ("FlextGrpcSettings",),
            ".typings": (
                "FlextGrpcTypes",
                "t",
            ),
            ".utilities": (
                "FlextGrpcUtilities",
                "u",
            ),
            "flext_core": (
                "d",
                "e",
                "h",
                "r",
                "s",
                "x",
            ),
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

__all__: list[str] = [
    "FlextGrpc",
    "FlextGrpcApiRuntime",
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
