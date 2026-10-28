# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_core import (
        build_lazy_import_map,
        cleanup_submodule_namespace,
        core,
        d,
        e,
        h,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        merge_lazy_imports,
        normalize_lazy_imports,
        r,
        resolve_lazy_members,
        x,
    )

    from flext_grpc.__version__ import (
        FlextGrpcVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
    )
    from flext_grpc._config import FlextGrpcConfig, config
    from flext_grpc._settings import FlextGrpcSettings, settings
    from flext_grpc.api import FlextGrpc, grpc
    from flext_grpc.base import FlextGrpcServiceBase, s
    from flext_grpc.cli import main
    from flext_grpc.config_models import FlextGrpcModelsConfigNamespace
    from flext_grpc.constants import FlextGrpcConstants, c
    from flext_grpc.errors import FlextGrpcErrors
    from flext_grpc.models import FlextGrpcModels, m
    from flext_grpc.protocols import FlextGrpcProtocols, p
    from flext_grpc.typings import FlextGrpcTypes, t
    from flext_grpc.utilities import FlextGrpcUtilities, u


__all__: tuple[str, ...] = (
    "FlextGrpc",
    "FlextGrpcConfig",
    "FlextGrpcConstants",
    "FlextGrpcErrors",
    "FlextGrpcModels",
    "FlextGrpcModelsConfigNamespace",
    "FlextGrpcProtocols",
    "FlextGrpcServiceBase",
    "FlextGrpcSettings",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcVersion",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "build_lazy_import_map",
    "c",
    "cleanup_submodule_namespace",
    "config",
    "core",
    "d",
    "e",
    "grpc",
    "h",
    "install_lazy_exports",
    "lazy",
    "lazy_getattr",
    "lazy_member",
    "m",
    "main",
    "merge_lazy_imports",
    "normalize_lazy_imports",
    "p",
    "r",
    "resolve_lazy_members",
    "s",
    "settings",
    "t",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "FlextGrpc": ".api",
        "FlextGrpcConfig": "._config",
        "FlextGrpcModelsConfigNamespace": ".config_models",
        "FlextGrpcConstants": ".constants",
        "FlextGrpcErrors": ".errors",
        "FlextGrpcModels": ".models",
        "FlextGrpcProtocols": ".protocols",
        "FlextGrpcServiceBase": ".base",
        "FlextGrpcSettings": "._settings",
        "FlextGrpcTypes": ".typings",
        "FlextGrpcUtilities": ".utilities",
        "FlextGrpcVersion": ".__version__",
        "__author__": ".__version__",
        "__author_email__": ".__version__",
        "__description__": ".__version__",
        "__license__": ".__version__",
        "__title__": ".__version__",
        "__url__": ".__version__",
        "__version_info__": ".__version__",
        "build_lazy_import_map": "flext_core",
        "c": ".constants",
        "cleanup_submodule_namespace": "flext_core",
        "config": "._config",
        "core": "flext_core",
        "d": "flext_core",
        "e": "flext_core",
        "grpc": ".api",
        "h": "flext_core",
        "install_lazy_exports": "flext_core",
        "lazy": "flext_core",
        "lazy_getattr": "flext_core",
        "lazy_member": "flext_core",
        "m": ".models",
        "main": ".cli",
        "merge_lazy_imports": "flext_core",
        "normalize_lazy_imports": "flext_core",
        "p": ".protocols",
        "r": "flext_core",
        "resolve_lazy_members": "flext_core",
        "s": ".base",
        "settings": "._settings",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_core",
    }),
    public_exports=__all__,
)

if not TYPE_CHECKING:
    from flext_grpc.__version__ import __version__
