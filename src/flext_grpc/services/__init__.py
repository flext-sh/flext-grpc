# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations
from flext_core.lazy import  install_lazy_exports


_LAZY_IMPORTS = {
    "FlextGrpcClient": ("flext_grpc.services.client", "FlextGrpcClient"),
    "FlextGrpcConnectionPool": ("flext_grpc.services.connection_pool", "FlextGrpcConnectionPool"),
    "FlextGrpcMetrics": ("flext_grpc.services.metrics", "FlextGrpcMetrics"),
    "FlextGrpcServer": ("flext_grpc.services.server", "FlextGrpcServer"),
    "FlextGrpcServices": ("flext_grpc.services._compat", "FlextGrpcServices"),
    "FlextGrpcStream": ("flext_grpc.services.stream", "FlextGrpcStream"),
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
