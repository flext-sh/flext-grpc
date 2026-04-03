# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext grpc package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports
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

if _TYPE_CHECKING:
    from flext_core import FlextTypes
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_grpc import (
        _utilities,
        api,
        client,
        connection_pool,
        constants,
        errors,
        metrics,
        models,
        proto,
        protocols,
        server,
        services,
        settings,
        stream,
        stubs,
        typings,
        utilities,
    )
    from flext_grpc._utilities import FlextGrpcUtilitiesGrpc, grpc, logger
    from flext_grpc.api import FlextGrpc
    from flext_grpc.constants import FlextGrpcConstants, FlextGrpcConstants as c
    from flext_grpc.errors import FlextGrpcError
    from flext_grpc.models import FlextGrpcModels, FlextGrpcModels as m
    from flext_grpc.proto import FlextGrpcServiceServicer
    from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
    from flext_grpc.services import (
        FlextGrpcClient,
        FlextGrpcConnectionPool,
        FlextGrpcMetrics,
        FlextGrpcServer,
        FlextGrpcServices,
        FlextGrpcStream,
    )
    from flext_grpc.settings import FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes, FlextGrpcTypes as t
    from flext_grpc.utilities import FlextGrpcUtilities, FlextGrpcUtilities as u

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = merge_lazy_imports(
    (
        "flext_grpc._utilities",
        "flext_grpc.proto",
        "flext_grpc.services",
    ),
    {
        "FlextGrpc": "flext_grpc.api",
        "FlextGrpcConstants": "flext_grpc.constants",
        "FlextGrpcError": "flext_grpc.errors",
        "FlextGrpcModels": "flext_grpc.models",
        "FlextGrpcProtocols": "flext_grpc.protocols",
        "FlextGrpcSettings": "flext_grpc.settings",
        "FlextGrpcTypes": "flext_grpc.typings",
        "FlextGrpcUtilities": "flext_grpc.utilities",
        "_utilities": "flext_grpc._utilities",
        "api": "flext_grpc.api",
        "c": ("flext_grpc.constants", "FlextGrpcConstants"),
        "client": "flext_grpc.client",
        "connection_pool": "flext_grpc.connection_pool",
        "constants": "flext_grpc.constants",
        "d": ("flext_core.decorators", "FlextDecorators"),
        "e": ("flext_core.exceptions", "FlextExceptions"),
        "errors": "flext_grpc.errors",
        "h": ("flext_core.handlers", "FlextHandlers"),
        "m": ("flext_grpc.models", "FlextGrpcModels"),
        "metrics": "flext_grpc.metrics",
        "models": "flext_grpc.models",
        "p": ("flext_grpc.protocols", "FlextGrpcProtocols"),
        "proto": "flext_grpc.proto",
        "protocols": "flext_grpc.protocols",
        "r": ("flext_core.result", "FlextResult"),
        "s": ("flext_core.service", "FlextService"),
        "server": "flext_grpc.server",
        "services": "flext_grpc.services",
        "settings": "flext_grpc.settings",
        "stream": "flext_grpc.stream",
        "stubs": "flext_grpc.stubs",
        "t": ("flext_grpc.typings", "FlextGrpcTypes"),
        "typings": "flext_grpc.typings",
        "u": ("flext_grpc.utilities", "FlextGrpcUtilities"),
        "utilities": "flext_grpc.utilities",
        "x": ("flext_core.mixins", "FlextMixins"),
    },
)


install_lazy_exports(
    __name__,
    globals(),
    _LAZY_IMPORTS,
    [
        "__all__",
        "__author__",
        "__author_email__",
        "__description__",
        "__license__",
        "__title__",
        "__url__",
        "__version__",
        "__version_info__",
    ],
)
