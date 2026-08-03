# @generated AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import build_lazy_import_map, install_lazy_exports

from .__version__ import __author__ as __author__
from .__version__ import __author_email__ as __author_email__
from .__version__ import __description__ as __description__
from .__version__ import __license__ as __license__
from .__version__ import __title__ as __title__
from .__version__ import __url__ as __url__
from .__version__ import __version__ as __version__
from .__version__ import __version_info__ as __version_info__

if TYPE_CHECKING:
    from flext_core import d as d
    from flext_core import e as e
    from flext_core import h as h
    from flext_core import r as r
    from flext_core import x as x

    from ._config import FlextGrpcConfig as FlextGrpcConfig
    from ._config import config as config
    from ._settings import FlextGrpcSettings as FlextGrpcSettings
    from ._settings import settings as settings
    from .api import FlextGrpc as FlextGrpc
    from .api import grpc as grpc
    from .base import FlextGrpcServiceBase as FlextGrpcServiceBase

    s: type[FlextGrpcServiceBase]
    from .constants import FlextGrpcConstants as FlextGrpcConstants

    c: type[FlextGrpcConstants]
    from .models import FlextGrpcModels as FlextGrpcModels

    m: type[FlextGrpcModels]
    from .protocols import FlextGrpcProtocols as FlextGrpcProtocols

    p: type[FlextGrpcProtocols]
    from .typings import FlextGrpcTypes as FlextGrpcTypes

    t: type[FlextGrpcTypes]
    from .utilities import FlextGrpcUtilities as FlextGrpcUtilities

    u: type[FlextGrpcUtilities]

_LAZY_MODULES: dict[str, tuple[str, ...]] = {
    "._config": ("FlextGrpcConfig", "config"),
    "._settings": ("FlextGrpcSettings", "settings"),
    ".api": ("FlextGrpc", "grpc"),
    ".base": ("FlextGrpcServiceBase", "s"),
    ".constants": ("FlextGrpcConstants", "c"),
    ".models": ("FlextGrpcModels", "m"),
    ".protocols": ("FlextGrpcProtocols", "p"),
    ".typings": ("FlextGrpcTypes", "t"),
    ".utilities": ("FlextGrpcUtilities", "u"),
    "flext_core": ("d", "e", "h", "r", "x"),
}


_LAZY_ALIAS_GROUPS: dict[str, tuple[tuple[str, str], ...]] = {}


_LAZY_IMPORTS = build_lazy_import_map(
    _LAZY_MODULES, alias_groups=_LAZY_ALIAS_GROUPS, sort_keys=False
)

_PUBLIC_EXPORTS: tuple[str, ...] = (
    "FlextGrpc",
    "FlextGrpcConfig",
    "FlextGrpcConstants",
    "FlextGrpcModels",
    "FlextGrpcProtocols",
    "FlextGrpcServiceBase",
    "FlextGrpcSettings",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "c",
    "config",
    "d",
    "e",
    "grpc",
    "h",
    "m",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

__all__: tuple[str, ...] = tuple(_PUBLIC_EXPORTS)

install_lazy_exports(__name__, globals(), _LAZY_IMPORTS, public_exports=__all__)
