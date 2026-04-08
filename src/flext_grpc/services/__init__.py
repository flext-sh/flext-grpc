# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextGrpcClient": ".client",
    "FlextGrpcConnectionPool": ".connection_pool",
    "FlextGrpcMetrics": ".metrics",
    "FlextGrpcServer": ".server",
    "FlextGrpcServices": "._compat",
    "FlextGrpcStream": ".stream",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
