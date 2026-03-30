# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext grpc package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

from flext_grpc.__version__ import (
    __author__ as __author__,
    __author_email__ as __author_email__,
    __description__ as __description__,
    __license__ as __license__,
    __title__ as __title__,
    __url__ as __url__,
    __version__ as __version__,
    __version_info__ as __version_info__,
)

if TYPE_CHECKING:
    from flext_grpc import (
        api as api,
        constants as constants,
        errors as errors,
        models as models,
        proto as proto,
        protocols as protocols,
        services as services,
        settings as settings,
        typings as typings,
        utilities as utilities,
    )
    from flext_grpc.api import FlextGrpc as FlextGrpc
    from flext_grpc.constants import (
        FlextGrpcConstants as FlextGrpcConstants,
        FlextGrpcConstants as c,
    )
    from flext_grpc.errors import (
        FlextGrpcConfigurationError as FlextGrpcConfigurationError,
        FlextGrpcConnectionError as FlextGrpcConnectionError,
        FlextGrpcError as FlextGrpcError,
        FlextGrpcTimeoutError as FlextGrpcTimeoutError,
        FlextGrpcValidationError as FlextGrpcValidationError,
    )
    from flext_grpc.models import (
        FlextGrpcModels as FlextGrpcModels,
        FlextGrpcModels as m,
    )
    from flext_grpc.proto import stubs as stubs
    from flext_grpc.proto.stubs import (
        FlextGrpcServiceServicer as FlextGrpcServiceServicer,
        FlextGrpcServiceStub as FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server as add_FlextGrpcServiceServicer_to_server,
    )
    from flext_grpc.protocols import (
        FlextGrpcProtocols as FlextGrpcProtocols,
        FlextGrpcProtocols as p,
    )
    from flext_grpc.services import FlextGrpcServices as FlextGrpcServices
    from flext_grpc.settings import FlextGrpcSettings as FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes as FlextGrpcTypes, FlextGrpcTypes as t
    from flext_grpc.utilities import (
        FlextGrpcUtilities as FlextGrpcUtilities,
        FlextGrpcUtilities as u,
    )

_LAZY_IMPORTS: Mapping[str, Sequence[str]] = {
    "FlextGrpc": ["flext_grpc.api", "FlextGrpc"],
    "FlextGrpcConfigurationError": ["flext_grpc.errors", "FlextGrpcConfigurationError"],
    "FlextGrpcConnectionError": ["flext_grpc.errors", "FlextGrpcConnectionError"],
    "FlextGrpcConstants": ["flext_grpc.constants", "FlextGrpcConstants"],
    "FlextGrpcError": ["flext_grpc.errors", "FlextGrpcError"],
    "FlextGrpcModels": ["flext_grpc.models", "FlextGrpcModels"],
    "FlextGrpcProtocols": ["flext_grpc.protocols", "FlextGrpcProtocols"],
    "FlextGrpcServiceServicer": ["flext_grpc.proto.stubs", "FlextGrpcServiceServicer"],
    "FlextGrpcServiceStub": ["flext_grpc.proto.stubs", "FlextGrpcServiceStub"],
    "FlextGrpcServices": ["flext_grpc.services", "FlextGrpcServices"],
    "FlextGrpcSettings": ["flext_grpc.settings", "FlextGrpcSettings"],
    "FlextGrpcTimeoutError": ["flext_grpc.errors", "FlextGrpcTimeoutError"],
    "FlextGrpcTypes": ["flext_grpc.typings", "FlextGrpcTypes"],
    "FlextGrpcUtilities": ["flext_grpc.utilities", "FlextGrpcUtilities"],
    "FlextGrpcValidationError": ["flext_grpc.errors", "FlextGrpcValidationError"],
    "add_FlextGrpcServiceServicer_to_server": [
        "flext_grpc.proto.stubs",
        "add_FlextGrpcServiceServicer_to_server",
    ],
    "api": ["flext_grpc.api", ""],
    "c": ["flext_grpc.constants", "FlextGrpcConstants"],
    "constants": ["flext_grpc.constants", ""],
    "d": ["flext_core", "d"],
    "e": ["flext_core", "e"],
    "errors": ["flext_grpc.errors", ""],
    "h": ["flext_core", "h"],
    "m": ["flext_grpc.models", "FlextGrpcModels"],
    "models": ["flext_grpc.models", ""],
    "p": ["flext_grpc.protocols", "FlextGrpcProtocols"],
    "proto": ["flext_grpc.proto", ""],
    "protocols": ["flext_grpc.protocols", ""],
    "r": ["flext_core", "r"],
    "s": ["flext_core", "s"],
    "services": ["flext_grpc.services", ""],
    "settings": ["flext_grpc.settings", ""],
    "stubs": ["flext_grpc.proto.stubs", ""],
    "t": ["flext_grpc.typings", "FlextGrpcTypes"],
    "typings": ["flext_grpc.typings", ""],
    "u": ["flext_grpc.utilities", "FlextGrpcUtilities"],
    "utilities": ["flext_grpc.utilities", ""],
    "x": ["flext_core", "x"],
}

_EXPORTS: Sequence[str] = [
    "FlextGrpc",
    "FlextGrpcConfigurationError",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcError",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "add_FlextGrpcServiceServicer_to_server",
    "api",
    "c",
    "constants",
    "d",
    "e",
    "errors",
    "h",
    "m",
    "models",
    "p",
    "proto",
    "protocols",
    "r",
    "s",
    "services",
    "settings",
    "stubs",
    "t",
    "typings",
    "u",
    "utilities",
    "x",
]


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, _EXPORTS)
