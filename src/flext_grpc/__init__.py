# AUTO-GENERATED FILE — DO NOT EDIT MANUALLY.
# Regenerate with: make codegen
#
"""Flext grpc package."""

from __future__ import annotations

from collections.abc import Mapping, MutableMapping, Sequence
from typing import TYPE_CHECKING

from flext_core.lazy import cleanup_submodule_namespace, lazy_getattr

if TYPE_CHECKING:
    from flext_core import FlextTypes, d, e, h, r, s, x

    from flext_grpc import proto
    from flext_grpc.__version__ import (
        __all__,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_grpc.api import FlextGrpc
    from flext_grpc.constants import FlextGrpcConstants, FlextGrpcConstants as c
    from flext_grpc.errors import (
        FlextGrpcConnectionError,
        FlextGrpcError,
        FlextGrpcSettingsurationError,
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
    from flext_grpc.services import FlextGrpcServices
    from flext_grpc.settings import FlextGrpcSettings
    from flext_grpc.typings import FlextGrpcTypes, FlextGrpcTypes as t
    from flext_grpc.utilities import FlextGrpcUtilities, FlextGrpcUtilities as u

_LAZY_IMPORTS: Mapping[str, tuple[str, str]] = {
    "FlextGrpc": ("flext_grpc.api", "FlextGrpc"),
    "FlextGrpcConnectionError": ("flext_grpc.errors", "FlextGrpcConnectionError"),
    "FlextGrpcConstants": ("flext_grpc.constants", "FlextGrpcConstants"),
    "FlextGrpcError": ("flext_grpc.errors", "FlextGrpcError"),
    "FlextGrpcModels": ("flext_grpc.models", "FlextGrpcModels"),
    "FlextGrpcProtocols": ("flext_grpc.protocols", "FlextGrpcProtocols"),
    "FlextGrpcServiceServicer": ("flext_grpc.proto.stubs", "FlextGrpcServiceServicer"),
    "FlextGrpcServiceStub": ("flext_grpc.proto.stubs", "FlextGrpcServiceStub"),
    "FlextGrpcServices": ("flext_grpc.services", "FlextGrpcServices"),
    "FlextGrpcSettings": ("flext_grpc.settings", "FlextGrpcSettings"),
    "FlextGrpcSettingsurationError": ("flext_grpc.errors", "FlextGrpcSettingsurationError"),
    "FlextGrpcTimeoutError": ("flext_grpc.errors", "FlextGrpcTimeoutError"),
    "FlextGrpcTypes": ("flext_grpc.typings", "FlextGrpcTypes"),
    "FlextGrpcUtilities": ("flext_grpc.utilities", "FlextGrpcUtilities"),
    "FlextGrpcValidationError": ("flext_grpc.errors", "FlextGrpcValidationError"),
    "__all__": ("flext_grpc.__version__", "__all__"),
    "__author__": ("flext_grpc.__version__", "__author__"),
    "__author_email__": ("flext_grpc.__version__", "__author_email__"),
    "__description__": ("flext_grpc.__version__", "__description__"),
    "__license__": ("flext_grpc.__version__", "__license__"),
    "__title__": ("flext_grpc.__version__", "__title__"),
    "__url__": ("flext_grpc.__version__", "__url__"),
    "__version__": ("flext_grpc.__version__", "__version__"),
    "__version_info__": ("flext_grpc.__version__", "__version_info__"),
    "add_FlextGrpcServiceServicer_to_server": ("flext_grpc.proto.stubs", "add_FlextGrpcServiceServicer_to_server"),
    "c": ("flext_grpc.constants", "FlextGrpcConstants"),
    "d": ("flext_core", "d"),
    "e": ("flext_core", "e"),
    "h": ("flext_core", "h"),
    "m": ("flext_grpc.models", "FlextGrpcModels"),
    "p": ("flext_grpc.protocols", "FlextGrpcProtocols"),
    "proto": ("flext_grpc.proto", ""),
    "r": ("flext_core", "r"),
    "s": ("flext_core", "s"),
    "t": ("flext_grpc.typings", "FlextGrpcTypes"),
    "u": ("flext_grpc.utilities", "FlextGrpcUtilities"),
    "x": ("flext_core", "x"),
}

__all__ = [
    "FlextGrpc",
    "FlextGrpcConnectionError",
    "FlextGrpcConstants",
    "FlextGrpcError",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "FlextGrpcServices",
    "FlextGrpcSettings",
    "FlextGrpcSettingsurationError",
    "FlextGrpcTimeoutError",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcValidationError",
    "__all__",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "add_FlextGrpcServiceServicer_to_server",
    "c",
    "d",
    "e",
    "h",
    "m",
    "p",
    "proto",
    "r",
    "s",
    "t",
    "u",
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
