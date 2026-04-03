# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Services package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING as _TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if _TYPE_CHECKING:
    from flext_core import FlextTypes
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
    from flext_grpc.services import (
        _compat,
        client,
        connection_pool,
        metrics,
        server,
        stream,
    )
    from flext_grpc.services._compat import FlextGrpcServices
    from flext_grpc.services.client import FlextGrpcClient
    from flext_grpc.services.connection_pool import FlextGrpcConnectionPool
    from flext_grpc.services.metrics import FlextGrpcMetrics
    from flext_grpc.services.server import FlextGrpcServer
    from flext_grpc.services.stream import FlextGrpcStream

_LAZY_IMPORTS: FlextTypes.LazyImportIndex = {
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
