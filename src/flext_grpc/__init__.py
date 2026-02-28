"""Enterprise gRPC Communication Platform for FLEXT ecosystem.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from flext_core._utilities.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextExceptions as e, d, h, r, s, x

    from flext_grpc.__version__ import __version__, __version_info__
    from flext_grpc.api import (
        FlextGrpc,
        GenericOperationSpec,
        GenericRequest,
        GenericResponse,
    )
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.errors import (
        FlextGrpcConnectionError,
        FlextGrpcError,
        FlextGrpcSettingsurationError,
        FlextGrpcTimeoutError,
        FlextGrpcValidationError,
    )
    from flext_grpc.models import FlextGrpcModels, m
    from flext_grpc.proto import FlextGrpcServiceStub
    from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
    from flext_grpc.services import (
        ConnectionPool,
        FlextGrpcServices,
        GrpcClientManager,
        GrpcServerManager,
        GrpcStreamManager,
        MetricsCollector,
        ServicePayload,
    )
    from flext_grpc.settings import FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes, t
    from flext_grpc.utilities import FlextGrpcUtilities, u

# Lazy import mapping: export_name -> (module_path, attr_name)
_LAZY_IMPORTS: dict[str, tuple[str, str]] = {
    "ConnectionPool": ("flext_grpc.services", "ConnectionPool"),
    "FlextGrpc": ("flext_grpc.api", "FlextGrpc"),
    "FlextGrpcConnectionError": ("flext_grpc.errors", "FlextGrpcConnectionError"),
    "FlextGrpcConstants": ("flext_grpc.constants", "FlextGrpcConstants"),
    "FlextGrpcError": ("flext_grpc.errors", "FlextGrpcError"),
    "FlextGrpcModels": ("flext_grpc.models", "FlextGrpcModels"),
    "FlextGrpcProtocols": ("flext_grpc.protocols", "FlextGrpcProtocols"),
    "FlextGrpcServiceStub": ("flext_grpc.proto", "FlextGrpcServiceStub"),
    "FlextGrpcServices": ("flext_grpc.services", "FlextGrpcServices"),
    "FlextGrpcSettings": ("flext_grpc.settings", "FlextGrpcSettings"),
    "FlextGrpcSettingsurationError": ("flext_grpc.errors", "FlextGrpcSettingsurationError"),
    "FlextGrpcTimeoutError": ("flext_grpc.errors", "FlextGrpcTimeoutError"),
    "FlextGrpcTypes": ("flext_grpc.typings", "FlextGrpcTypes"),
    "FlextGrpcUtilities": ("flext_grpc.utilities", "FlextGrpcUtilities"),
    "FlextGrpcValidationError": ("flext_grpc.errors", "FlextGrpcValidationError"),
    "GenericOperationSpec": ("flext_grpc.api", "GenericOperationSpec"),
    "GenericRequest": ("flext_grpc.api", "GenericRequest"),
    "GenericResponse": ("flext_grpc.api", "GenericResponse"),
    "GrpcClientManager": ("flext_grpc.services", "GrpcClientManager"),
    "GrpcServerManager": ("flext_grpc.services", "GrpcServerManager"),
    "GrpcStreamManager": ("flext_grpc.services", "GrpcStreamManager"),
    "MetricsCollector": ("flext_grpc.services", "MetricsCollector"),
    "ServicePayload": ("flext_grpc.services", "ServicePayload"),
    "__version__": ("flext_grpc.__version__", "__version__"),
    "__version_info__": ("flext_grpc.__version__", "__version_info__"),
    "c": ("flext_grpc.constants", "c"),
    "d": ("flext_core", "d"),
    "e": ("flext_core", "FlextExceptions"),
    "h": ("flext_core", "h"),
    "m": ("flext_grpc.models", "m"),
    "p": ("flext_grpc.protocols", "FlextGrpcProtocols"),
    "r": ("flext_core", "r"),
    "s": ("flext_core", "s"),
    "t": ("flext_grpc.typings", "t"),
    "u": ("flext_grpc.utilities", "u"),
    "x": ("flext_core", "x"),
}

__all__ = [
    "ConnectionPool",
    "FlextGrpc",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcError",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "FlextGrpcSettingsurationError",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
    "GenericOperationSpec",
    "GenericRequest",
    "GenericResponse",
    "GrpcClientManager",
    "GrpcServerManager",
    "GrpcStreamManager",
    "MetricsCollector",
    "ServicePayload",
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
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    """Lazy-load module attributes on first access (PEP 562)."""
    return lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)


def __dir__() -> list[str]:
    """Return list of available attributes for dir() and autocomplete."""
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
