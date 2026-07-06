# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export registry."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map, merge_lazy_imports

_LOCAL_LAZY_IMPORTS = build_lazy_import_map(
    {
        "._utilities": ("_utilities",),
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
        ".services": ("services",),
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
            "x",
        ),
    },
)

FLEXT_GRPC_LAZY_IMPORTS = merge_lazy_imports(
    (".services",),
    _LOCAL_LAZY_IMPORTS,
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
    module_name="flext_grpc",
)

__all__: list[str] = ["FLEXT_GRPC_LAZY_IMPORTS"]
