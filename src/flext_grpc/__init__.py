# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext grpc package."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports, merge_lazy_imports

if TYPE_CHECKING:
    from flext_grpc.__version__ import *
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

_LAZY_IMPORTS: Mapping[str, str | Sequence[str]] = merge_lazy_imports(
    ("flext_grpc.proto",),
    {
        "FlextGrpc": "flext_grpc.api",
        "FlextGrpcConfigurationError": "flext_grpc.errors",
        "FlextGrpcConnectionError": "flext_grpc.errors",
        "FlextGrpcConstants": "flext_grpc.constants",
        "FlextGrpcError": "flext_grpc.errors",
        "FlextGrpcModels": "flext_grpc.models",
        "FlextGrpcProtocols": "flext_grpc.protocols",
        "FlextGrpcServices": "flext_grpc.services",
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
        "api": "flext_grpc.api",
        "c": ("flext_grpc.constants", "FlextGrpcConstants"),
        "constants": "flext_grpc.constants",
        "d": "flext_core",
        "e": "flext_core",
        "errors": "flext_grpc.errors",
        "h": "flext_core",
        "m": ("flext_grpc.models", "FlextGrpcModels"),
        "models": "flext_grpc.models",
        "p": ("flext_grpc.protocols", "FlextGrpcProtocols"),
        "proto": "flext_grpc.proto",
        "protocols": "flext_grpc.protocols",
        "r": "flext_core",
        "s": "flext_core",
        "services": "flext_grpc.services",
        "settings": "flext_grpc.settings",
        "t": ("flext_grpc.typings", "FlextGrpcTypes"),
        "typings": "flext_grpc.typings",
        "u": ("flext_grpc.utilities", "FlextGrpcUtilities"),
        "utilities": "flext_grpc.utilities",
        "x": "flext_core",
    },
)


install_lazy_exports(__name__, globals(), _LAZY_IMPORTS)
