# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Proto package."""

from __future__ import annotations

import typing as _t

from flext_core.lazy import install_lazy_exports

if _t.TYPE_CHECKING:
    import flext_grpc.proto.stubs as _flext_grpc_proto_stubs

    stubs = _flext_grpc_proto_stubs
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
    from flext_grpc.proto.stubs import (
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server,
    )

    _ = (
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server,
        c,
        d,
        e,
        h,
        m,
        p,
        r,
        s,
        stubs,
        t,
        u,
        x,
    )
_LAZY_IMPORTS = {
    "FlextGrpcServiceServicer": "flext_grpc.proto.stubs",
    "FlextGrpcServiceStub": "flext_grpc.proto.stubs",
    "add_FlextGrpcServiceServicer_to_server": "flext_grpc.proto.stubs",
    "c": ("flext_core.constants", "FlextConstants"),
    "d": ("flext_core.decorators", "FlextDecorators"),
    "e": ("flext_core.exceptions", "FlextExceptions"),
    "h": ("flext_core.handlers", "FlextHandlers"),
    "m": ("flext_core.models", "FlextModels"),
    "p": ("flext_core.protocols", "FlextProtocols"),
    "r": ("flext_core.result", "FlextResult"),
    "s": ("flext_core.service", "FlextService"),
    "stubs": "flext_grpc.proto.stubs",
    "t": ("flext_core.typings", "FlextTypes"),
    "u": ("flext_core.utilities", "FlextUtilities"),
    "x": ("flext_core.mixins", "FlextMixins"),
}

__all__ = [
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "add_FlextGrpcServiceServicer_to_server",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "r",
    "s",
    "stubs",
    "t",
    "u",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
