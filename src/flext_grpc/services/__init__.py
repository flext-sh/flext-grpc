# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextGrpcClient": ("flext_grpc.services.client", "FlextGrpcClient"),
    "FlextGrpcConnectionPool": (
        "flext_grpc.services.connection_pool",
        "FlextGrpcConnectionPool",
    ),
    "FlextGrpcMetrics": ("flext_grpc.services.metrics", "FlextGrpcMetrics"),
    "FlextGrpcServer": ("flext_grpc.services.server", "FlextGrpcServer"),
    "FlextGrpcServices": ("flext_grpc.services._compat", "FlextGrpcServices"),
    "FlextGrpcStream": ("flext_grpc.services.stream", "FlextGrpcStream"),
    "c": ("flext_core.constants", "FlextConstants"),
    "client": "flext_grpc.services.client",
    "connection_pool": "flext_grpc.services.connection_pool",
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "metrics": "flext_grpc.services.metrics",
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "server": "flext_grpc.services.server",
    "stream": "flext_grpc.services.stream",
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
