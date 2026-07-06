# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import (
    build_lazy_import_map,
    install_lazy_exports,
    merge_lazy_imports,
)
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
    from flext_core._root_typing_parts.facades import d, e, h, r, x
    from flext_grpc.api import FlextGrpc, grpc
    from flext_grpc.base import FlextGrpcServiceBase, s
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.models import FlextGrpcModels, m
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
    (".services",),
    build_lazy_import_map(
        {
            ".api": (
                "FlextGrpc",
                "grpc",
            ),
            ".base": (
                "FlextGrpcServiceBase",
                "s",
            ),
            ".constants": (
                "FlextGrpcConstants",
                "c",
            ),
            ".models": (
                "FlextGrpcModels",
                "m",
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
            "flext_core._root_typing_parts.facades": (
                "d",
                "e",
                "h",
                "r",
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
        "pytest_addoption",
        "pytest_collect_file",
        "pytest_collection_modifyitems",
        "pytest_configure",
        "pytest_runtest_setup",
        "pytest_runtest_teardown",
        "pytest_sessionfinish",
        "pytest_sessionstart",
        "pytest_terminal_summary",
        "pytest_warning_recorded",
    ),
    module_name=__name__,
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
    public_exports=__all__,
)
