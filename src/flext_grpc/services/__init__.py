# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_grpc.services._compat as _flext_grpc_services__compat

    _compat = _flext_grpc_services__compat
    import flext_grpc.services.client as _flext_grpc_services_client
    from flext_grpc.services._compat import FlextGrpcServices

    client = _flext_grpc_services_client
    import flext_grpc.services.connection_pool as _flext_grpc_services_connection_pool
    from flext_grpc.services.client import FlextGrpcClient

    connection_pool = _flext_grpc_services_connection_pool
    import flext_grpc.services.metrics as _flext_grpc_services_metrics
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool

    metrics = _flext_grpc_services_metrics
    import flext_grpc.services.server as _flext_grpc_services_server
    from flext_grpc.services.metrics import FlextGrpcMetrics

    server = _flext_grpc_services_server
    import flext_grpc.services.stream as _flext_grpc_services_stream
    from flext_grpc.services.server import FlextGrpcServer

    stream = _flext_grpc_services_stream
    from flext_core.constants import FlextConstants as c
    from flext_core.decorators import FlextDecorators as d
    from flext_core.exceptions import FlextExceptions as e
    from flext_core.handlers import FlextHandlers as h
    from flext_core.mixins import FlextMixins as x
    from flext_core.models import FlextModels as m
    from flext_core.protocols import FlextProtocols as p
    from flext_core.result import FlextResult as r
    from flext_core.service import FlextService as s
    from flext_core.typings import FlextTypes as t
    from flext_core.utilities import FlextUtilities as u
    from flext_grpc.services.stream import FlextGrpcStream
_LAZY_IMPORTS = {
    "FlextGrpcClient": "flext_grpc.services.client",
    "FlextGrpcConnectionPool": "flext_grpc.services.connection_pool",
    "FlextGrpcMetrics": "flext_grpc.services.metrics",
    "FlextGrpcServer": "flext_grpc.services.server",
    "FlextGrpcServices": "flext_grpc.services._compat",
    "FlextGrpcStream": "flext_grpc.services.stream",
    "_compat": "flext_grpc.services._compat",
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

__all__ = [
    "FlextGrpcClient",
    "FlextGrpcConnectionPool",
    "FlextGrpcMetrics",
    "FlextGrpcServer",
    "FlextGrpcServices",
    "FlextGrpcStream",
    "_compat",
    "c",
    "client",
    "connection_pool",
    "d",
    "e",
    "h",
    "m",
    "metrics",
    "p",
    "r",
    "s",
    "server",
    "stream",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
