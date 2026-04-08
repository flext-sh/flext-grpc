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
    "stubs": "flext_grpc.proto.stubs",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, publish_all=False)
