# AUTO-GENERATED FILE — Regenerate with: make gen
"""Lazy export map part."""

from __future__ import annotations

from flext_core.lazy import build_lazy_import_map

FLEXT_GRPC_LAZY_IMPORTS_PART_01 = build_lazy_import_map(
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
        "flext_core._root_typing_parts": (
            "d",
            "e",
            "h",
            "r",
            "x",
        ),
    },
)

__all__: list[str] = ["FLEXT_GRPC_LAZY_IMPORTS_PART_01"]
