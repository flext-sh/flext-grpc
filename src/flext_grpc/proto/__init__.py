# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Proto package."""

from __future__ import annotations

from flext_core.lazy import install_lazy_exports

_LAZY_IMPORTS = {
    "FlextGrpcServiceServicer": ("flext_grpc.proto.stubs", "FlextGrpcServiceServicer"),
    "FlextGrpcServiceStub": ("flext_grpc.proto.stubs", "FlextGrpcServiceStub"),
    "add_FlextGrpcServiceServicer_to_server": (
        "flext_grpc.proto.stubs",
        "add_FlextGrpcServiceServicer_to_server",
    ),
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


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
