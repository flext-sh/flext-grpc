# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext grpc package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_grpc.__version__ import *

if _t.TYPE_CHECKING:
    import flext_grpc._utilities as _flext_grpc__utilities

    _utilities = _flext_grpc__utilities
    import flext_grpc.api as _flext_grpc_api
    from flext_grpc._utilities import FlextGrpcUtilitiesGrpc, grpc, logger

    api = _flext_grpc_api
    import flext_grpc.constants as _flext_grpc_constants
    from flext_grpc.api import FlextGrpc

    constants = _flext_grpc_constants
    import flext_grpc.errors as _flext_grpc_errors
    from flext_grpc.constants import FlextGrpcConstants, FlextGrpcConstants as c

    errors = _flext_grpc_errors
    import flext_grpc.models as _flext_grpc_models
    from flext_grpc.errors import (
        FlextGrpcConfigurationError,
        FlextGrpcConnectionError,
        FlextGrpcError,
        FlextGrpcTimeoutError,
        FlextGrpcValidationError,
    )

    models = _flext_grpc_models
    import flext_grpc.proto as _flext_grpc_proto
    from flext_grpc.models import FlextGrpcModels, FlextGrpcModels as m

    proto = _flext_grpc_proto
    import flext_grpc.protocols as _flext_grpc_protocols
    from flext_grpc.proto import (
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server,
        stubs,
    )

    protocols = _flext_grpc_protocols
    import flext_grpc.services as _flext_grpc_services
    from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p

    services = _flext_grpc_services
    import flext_grpc.settings as _flext_grpc_settings
    from flext_grpc.services import (
        FlextGrpcClient,
        FlextGrpcConnectionPool,
        FlextGrpcMetrics,
        FlextGrpcServer,
        FlextGrpcServices,
        FlextGrpcStream,
        client,
        connection_pool,
        metrics,
        server,
        stream,
    )

    settings = _flext_grpc_settings
    import flext_grpc.typings as _flext_grpc_typings
    from flext_grpc.settings import FlextGrpcSettings

    typings = _flext_grpc_typings
    import flext_grpc.utilities as _flext_grpc_utilities
    from flext_grpc.typings import FlextGrpcTypes, FlextGrpcTypes as t

    utilities = _flext_grpc_utilities
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_grpc.utilities import FlextGrpcUtilities, FlextGrpcUtilities as u
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_grpc._utilities",
        "flext_grpc.proto",
        "flext_grpc.services",
    ),
    {
        "FlextGrpc": ("flext_grpc.api", "FlextGrpc"),
        "FlextGrpcConfigurationError": (
            "flext_grpc.errors",
            "FlextGrpcConfigurationError",
        ),
        "FlextGrpcConnectionError": ("flext_grpc.errors", "FlextGrpcConnectionError"),
        "FlextGrpcConstants": ("flext_grpc.constants", "FlextGrpcConstants"),
        "FlextGrpcError": ("flext_grpc.errors", "FlextGrpcError"),
        "FlextGrpcModels": ("flext_grpc.models", "FlextGrpcModels"),
        "FlextGrpcProtocols": ("flext_grpc.protocols", "FlextGrpcProtocols"),
        "FlextGrpcSettings": ("flext_grpc.settings", "FlextGrpcSettings"),
        "FlextGrpcTimeoutError": ("flext_grpc.errors", "FlextGrpcTimeoutError"),
        "FlextGrpcTypes": ("flext_grpc.typings", "FlextGrpcTypes"),
        "FlextGrpcUtilities": ("flext_grpc.utilities", "FlextGrpcUtilities"),
        "FlextGrpcValidationError": ("flext_grpc.errors", "FlextGrpcValidationError"),
        "__author__": ("flext_grpc.__version__", "__author__"),
        "__author_email__": ("flext_grpc.__version__", "__author_email__"),
        "__description__": ("flext_grpc.__version__", "__description__"),
        "__license__": ("flext_grpc.__version__", "__license__"),
        "__title__": ("flext_grpc.__version__", "__title__"),
        "__url__": ("flext_grpc.__version__", "__url__"),
        "__version__": ("flext_grpc.__version__", "__version__"),
        "__version_info__": ("flext_grpc.__version__", "__version_info__"),
        "_utilities": "flext_grpc._utilities",
        "api": "flext_grpc.api",
        "c": ("flext_grpc.constants", "FlextGrpcConstants"),
        "constants": "flext_grpc.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "errors": "flext_grpc.errors",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_grpc.models", "FlextGrpcModels"),
        "models": "flext_grpc.models",
        "p": ("flext_grpc.protocols", "FlextGrpcProtocols"),
        "proto": "flext_grpc.proto",
        "protocols": "flext_grpc.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "services": "flext_grpc.services",
        "settings": "flext_grpc.settings",
        "t": ("flext_grpc.typings", "FlextGrpcTypes"),
        "typings": "flext_grpc.typings",
        "u": ("flext_grpc.utilities", "FlextGrpcUtilities"),
        "utilities": "flext_grpc.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)
_ = _LAZY_IMPORTS.pop("cleanup_submodule_namespace", None)
_ = _LAZY_IMPORTS.pop("install_lazy_exports", None)
_ = _LAZY_IMPORTS.pop("lazy_getattr", None)
_ = _LAZY_IMPORTS.pop("merge_lazy_imports", None)
_ = _LAZY_IMPORTS.pop("output", None)
_ = _LAZY_IMPORTS.pop("output_reporting", None)

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
    "FlextGrpcServices",
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
    "_utilities",
    "add_FlextGrpcServiceServicer_to_server",
    "api",
    "c",
    "client",
    "connection_pool",
    "constants",
    "d",
    "e",
    "errors",
    "grpc",
    "h",
    "logger",
    "m",
    "metrics",
    "models",
    "p",
    "proto",
    "protocols",
    "r",
    "s",
    "server",
    "services",
    "settings",
    "stream",
    "stubs",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
