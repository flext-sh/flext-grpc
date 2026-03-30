# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make gen
#
"""Flext grpc package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

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
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_grpc import (
        api,
        constants,
        errors,
        models,
        proto,
        protocols,
        services,
        settings,
        typings,
        utilities,
    )
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
    from flext_grpc.proto import stubs
    from flext_grpc.proto.stubs import (
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        add_FlextGrpcServiceServicer_to_server,
    )
    from flext_grpc.protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
    from flext_grpc.services import FlextGrpcServices
    from flext_grpc.settings import FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes, FlextGrpcTypes as t
    from flext_grpc.utilities import FlextGrpcUtilities, FlextGrpcUtilities as u

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

__all__ = [
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


_LAZY_CACHE: MutableMapping[str, FlextTypes.ModuleExport] = {}


def __getattr__(name: str) -> FlextTypes.ModuleExport:
    """Lazy-load module attributes on first access (PEP 562).

    A local cache ``_LAZY_CACHE`` persists resolved objects across repeated
    accesses during process lifetime.

    Args:
        name: Attribute name requested by dir()/import.

    Returns:
        Lazy-loaded module export type.

    Raises:
        AttributeError: If attribute not registered.

    """
    if name in _LAZY_CACHE:
        return _LAZY_CACHE[name]

    value = lazy_getattr(name, _LAZY_IMPORTS, globals(), __name__)
    _LAZY_CACHE[name] = value
    return value


def __dir__() -> Sequence[str]:
    """Return list of available attributes for dir() and autocomplete.

    Returns:
        List of public names from module exports.

    """
    return sorted(__all__)


cleanup_submodule_namespace(__name__, _LAZY_IMPORTS)
