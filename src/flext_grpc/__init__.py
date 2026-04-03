# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext grpc package."""

from __future__ import annotations

import typing as _t

from flext_core.decorators import FlextDecorators as d
from flext_core.exceptions import FlextExceptions as e
from flext_core.handlers import FlextHandlers as h
from flext_core.lazy import install_lazy_exports, merge_lazy_imports
from flext_core.mixins import FlextMixins as x
from flext_core.result import FlextResult as r
from flext_core.service import FlextService as s
from flext_grpc.__version__ import *
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
from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc, grpc, logger
from flext_grpc.api import FlextGrpc
from flext_grpc.constants import FlextGrpcConstants, FlextGrpcConstants as c
from flext_grpc.errors import (
    FlextGrpcConfigurationError,
    FlextGrpcConnectionError,
    FlextGrpcError,
    FlextGrpcTimeoutError,
    FlextGrpcValidationError,
)
from flext_grpc.models import FlextGrpcModels, FlextGrpcModels as m
from flext_grpc.proto.stubs import (
    FlextGrpcServiceServicer,
    FlextGrpcServiceStub,
    add_FlextGrpcServiceServicer_to_server,
)
from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
from flext_grpc.services._compat import FlextGrpcServices
from flext_grpc.services.client import FlextGrpcClient
from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
from flext_grpc.services.metrics import FlextGrpcMetrics
from flext_grpc.services.server import FlextGrpcServer
from flext_grpc.services.stream import FlextGrpcStream
from flext_grpc.settings import FlextGrpcSettings
from flext_grpc.typings import FlextGrpcTypes, FlextGrpcTypes as t
from flext_grpc.utilities import FlextGrpcUtilities, FlextGrpcUtilities as u

if _t.TYPE_CHECKING:
    import flext_grpc._utilities as _flext_grpc__utilities

    _utilities = _flext_grpc__utilities
    import flext_grpc.api as _flext_grpc_api

    api = _flext_grpc_api
    import flext_grpc.constants as _flext_grpc_constants

    constants = _flext_grpc_constants
    import flext_grpc.errors as _flext_grpc_errors

    errors = _flext_grpc_errors
    import flext_grpc.models as _flext_grpc_models

    models = _flext_grpc_models
    import flext_grpc.proto as _flext_grpc_proto

    proto = _flext_grpc_proto
    import flext_grpc.proto.stubs as _flext_grpc_proto_stubs

    stubs = _flext_grpc_proto_stubs
    import flext_grpc.protocols as _flext_grpc_protocols

    protocols = _flext_grpc_protocols
    import flext_grpc.services as _flext_grpc_services

    services = _flext_grpc_services
    import flext_grpc.services.client as _flext_grpc_services_client

    client = _flext_grpc_services_client
    import flext_grpc.services.connection_pool as _flext_grpc_services_connection_pool

    connection_pool = _flext_grpc_services_connection_pool
    import flext_grpc.services.metrics as _flext_grpc_services_metrics

    metrics = _flext_grpc_services_metrics
    import flext_grpc.services.server as _flext_grpc_services_server

    server = _flext_grpc_services_server
    import flext_grpc.services.stream as _flext_grpc_services_stream

    stream = _flext_grpc_services_stream
    import flext_grpc.settings as _flext_grpc_settings

    settings = _flext_grpc_settings
    import flext_grpc.typings as _flext_grpc_typings

    typings = _flext_grpc_typings
    import flext_grpc.utilities as _flext_grpc_utilities

    utilities = _flext_grpc_utilities

    _ = (
        FlextGrpc,
        FlextGrpcClient,
        FlextGrpcConfigurationError,
        FlextGrpcConnectionError,
        FlextGrpcConnectionPool,
        FlextGrpcConstants,
        FlextGrpcError,
        FlextGrpcMetrics,
        FlextGrpcModels,
        FlextGrpcProtocols,
        FlextGrpcServer,
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        FlextGrpcServices,
        FlextGrpcSettings,
        FlextGrpcStream,
        FlextGrpcTimeoutError,
        FlextGrpcTypes,
        FlextGrpcUtilities,
        FlextGrpcUtilitiesGrpc,
        FlextGrpcValidationError,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        _utilities,
        add_FlextGrpcServiceServicer_to_server,
        api,
        c,
        client,
        connection_pool,
        constants,
        d,
        e,
        errors,
        grpc,
        h,
        logger,
        m,
        metrics,
        models,
        p,
        proto,
        protocols,
        r,
        s,
        server,
        services,
        settings,
        stream,
        stubs,
        t,
        typings,
        u,
        utilities,
        x,
    )
_LAZY_IMPORTS = merge_lazy_imports(
    (
        "flext_grpc._utilities",
        "flext_grpc.proto",
        "flext_grpc.services",
    ),
    {
        "FlextGrpc": "flext_grpc.api",
        "FlextGrpcConfigurationError": "flext_grpc.errors",
        "FlextGrpcConnectionError": "flext_grpc.errors",
        "FlextGrpcConstants": "flext_grpc.constants",
        "FlextGrpcError": "flext_grpc.errors",
        "FlextGrpcModels": "flext_grpc.models",
        "FlextGrpcProtocols": "flext_grpc.protocols",
        "FlextGrpcSettings": "flext_grpc.settings",
        "FlextGrpcTimeoutError": "flext_grpc.errors",
        "FlextGrpcTypes": "flext_grpc.typings",
        "FlextGrpcUtilities": "flext_grpc.utilities",
        "FlextGrpcValidationError": "flext_grpc.errors",
        "__author__": "flext_grpc.__version__",
        "__author_email__": "flext_grpc.__version__",
        "__description__": "flext_grpc.__version__",
        "__license__": "flext_grpc.__version__",
        "__title__": "flext_grpc.__version__",
        "__url__": "flext_grpc.__version__",
        "__version__": "flext_grpc.__version__",
        "__version_info__": "flext_grpc.__version__",
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
