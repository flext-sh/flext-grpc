# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext grpc package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

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

if TYPE_CHECKING:
    from flext_core import *

    from flext_grpc import (
        api,
        constants,
        errors,
        models,
        protocols,
        services,
        settings,
        typings,
        utilities,
    )
    from flext_grpc.api import *
    from flext_grpc.constants import *
    from flext_grpc.errors import *
    from flext_grpc.models import *
    from flext_grpc.proto import *
    from flext_grpc.protocols import *
    from flext_grpc.services import *
    from flext_grpc.settings import *
    from flext_grpc.typings import *
    from flext_grpc.utilities import *

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = {
    "FlextGrpc": "flext_grpc.api",
    "FlextGrpcConfigurationError": "flext_grpc.errors",
    "FlextGrpcConnectionError": "flext_grpc.errors",
    "FlextGrpcConstants": "flext_grpc.constants",
    "FlextGrpcError": "flext_grpc.errors",
    "FlextGrpcModels": "flext_grpc.models",
    "FlextGrpcProtocols": "flext_grpc.protocols",
    "FlextGrpcServiceServicer": "flext_grpc.proto.stubs",
    "FlextGrpcServiceStub": "flext_grpc.proto.stubs",
    "FlextGrpcServices": "flext_grpc.services",
    "FlextGrpcSettings": "flext_grpc.settings",
    "FlextGrpcTimeoutError": "flext_grpc.errors",
    "FlextGrpcTypes": "flext_grpc.typings",
    "FlextGrpcUtilities": "flext_grpc.utilities",
    "FlextGrpcValidationError": "flext_grpc.errors",
    "add_FlextGrpcServiceServicer_to_server": "flext_grpc.proto.stubs",
    "api": "flext_grpc.api",
    "c": ["flext_grpc.constants", "FlextGrpcConstants"],
    "constants": "flext_grpc.constants",
    "d": "flext_core",
    "e": "flext_core",
    "errors": "flext_grpc.errors",
    "h": "flext_core",
    "m": ["flext_grpc.models", "FlextGrpcModels"],
    "models": "flext_grpc.models",
    "p": ["flext_grpc.protocols", "FlextGrpcProtocols"],
    "proto": "flext_grpc.proto",
    "protocols": "flext_grpc.protocols",
    "r": "flext_core",
    "s": "flext_core",
    "services": "flext_grpc.services",
    "settings": "flext_grpc.settings",
    "stubs": "flext_grpc.proto.stubs",
    "t": ["flext_grpc.typings", "FlextGrpcTypes"],
    "typings": "flext_grpc.typings",
    "u": ["flext_grpc.utilities", "FlextGrpcUtilities"],
    "utilities": "flext_grpc.utilities",
    "x": "flext_core",
}


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, sorted(_LAZY_IMPORTS))
