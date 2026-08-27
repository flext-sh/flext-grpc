# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package."""

from __future__ import annotations

from typing import TYPE_CHECKING

from types import MappingProxyType

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
    from flext_core import d, e, h, r, x

    from ._config import FlextGrpcConfig, config
    from ._settings import FlextGrpcSettings, settings
    from .api import FlextGrpc, grpc
    from .base import FlextGrpcServiceBase, FlextGrpcServiceBase as s
    from .constants import FlextGrpcConstants, FlextGrpcConstants as c
    from .models import FlextGrpcModels, FlextGrpcModels as m
    from .protocols import FlextGrpcProtocols, FlextGrpcProtocols as p
    from .typings import FlextGrpcTypes, FlextGrpcTypes as t
    from .utilities import FlextGrpcUtilities, FlextGrpcUtilities as u
__all__: tuple[str, ...] = (
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

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType(
        build_lazy_import_map(
            MappingProxyType({
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
            }),
            alias_groups=MappingProxyType({}),
            sort_keys=False,
        )
    ),
    public_exports=__all__,
)
