# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Flext grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core.typings import FlextTypes

    from flext_grpc.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_grpc.api import FlextGrpc
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.errors import (
        FlextGrpcConnectionError,
        FlextGrpcError,
        FlextGrpcSettingsurationError,
        FlextGrpcTimeoutError,
        FlextGrpcValidationError,
    )
    from flext_grpc.models import m
    from flext_grpc.protocols import FlextGrpcProtocols, p
    from flext_grpc.services import (
        ClientConnection,
        ConnectionPool,
        FlextGrpcServices,
        GrpcClientManager,
        GrpcServerManager,
        GrpcStreamManager,
        MetricsCollector,
        ServerLifecycle,
        ServicePayload,
        StreamProcessor,
    )
    from flext_grpc.settings import FlextGrpcModels, FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes, t
    from flext_grpc.utilities import FlextGrpcUtilities, u

_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "ClientConnection": ("flext_grpc.services", "ClientConnection"),
    "ConnectionPool": ("flext_grpc.services", "ConnectionPool"),
    "FlextGrpc": ("flext_grpc.api", "FlextGrpc"),
    "FlextGrpcConnectionError": ("flext_grpc.errors", "FlextGrpcConnectionError"),
    "FlextGrpcConstants": ("flext_grpc.constants", "FlextGrpcConstants"),
    "FlextGrpcError": ("flext_grpc.errors", "FlextGrpcError"),
    "FlextGrpcModels": ("flext_grpc.settings", "FlextGrpcModels"),
    "FlextGrpcProtocols": ("flext_grpc.protocols", "FlextGrpcProtocols"),
    "FlextGrpcServices": ("flext_grpc.services", "FlextGrpcServices"),
    "FlextGrpcSettings": ("flext_grpc.settings", "FlextGrpcSettings"),
    "FlextGrpcSettingsurationError": (
        "flext_grpc.errors",
        "FlextGrpcSettingsurationError",
    ),
    "FlextGrpcTimeoutError": ("flext_grpc.errors", "FlextGrpcTimeoutError"),
    "FlextGrpcTypes": ("flext_grpc.typings", "FlextGrpcTypes"),
    "FlextGrpcUtilities": ("flext_grpc.utilities", "FlextGrpcUtilities"),
    "FlextGrpcValidationError": ("flext_grpc.errors", "FlextGrpcValidationError"),
    "GrpcClientManager": ("flext_grpc.services", "GrpcClientManager"),
    "GrpcServerManager": ("flext_grpc.services", "GrpcServerManager"),
    "GrpcStreamManager": ("flext_grpc.services", "GrpcStreamManager"),
    "MetricsCollector": ("flext_grpc.services", "MetricsCollector"),
    "ServerLifecycle": ("flext_grpc.services", "ServerLifecycle"),
    "ServicePayload": ("flext_grpc.services", "ServicePayload"),
    "StreamProcessor": ("flext_grpc.services", "StreamProcessor"),
    "__all__": ("flext_grpc.__version__", "__all__"),
    "__author__": ("flext_grpc.__version__", "__author__"),
    "__author_email__": ("flext_grpc.__version__", "__author_email__"),
    "__description__": ("flext_grpc.__version__", "__description__"),
    "__license__": ("flext_grpc.__version__", "__license__"),
    "__title__": ("flext_grpc.__version__", "__title__"),
    "__url__": ("flext_grpc.__version__", "__url__"),
    "__version__": ("flext_grpc.__version__", "__version__"),
    "__version_info__": ("flext_grpc.__version__", "__version_info__"),
    "c": ("flext_grpc.constants", "c"),
    "m": ("flext_grpc.models", "m"),
    "p": ("flext_grpc.protocols", "p"),
    "t": ("flext_grpc.typings", "t"),
    "u": ("flext_grpc.utilities", "u"),
}

__all__ = [
    "ClientConnection",
    "ConnectionPool",
    "FlextGrpc",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcError",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "FlextGrpcSettingsurationError",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
    "GrpcClientManager",
    "GrpcServerManager",
    "GrpcStreamManager",
    "MetricsCollector",
    "ServerLifecycle",
    "ServicePayload",
    "StreamProcessor",
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "m",
    "p",
    "t",
    "u",
]


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
