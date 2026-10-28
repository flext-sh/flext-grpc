# AUTO-GENERATED FILE — Regenerate with: make gen
"""Examples package.

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
    from flext_core import d, e, h, r, x

    from examples.constants import ExamplesFlextGrpcConstants
    from examples.models import ExamplesFlextGrpcModels
    from examples.protocols import ExamplesFlextGrpcProtocols
    from examples.typings import ExamplesFlextGrpcTypes, t
    from examples.utilities import ExamplesFlextGrpcUtilities, u
    from flext_grpc import (
        build_lazy_import_map,
        c,
        cleanup_submodule_namespace,
        config,
        core,
        grpc,
        install_lazy_exports,
        lazy,
        lazy_getattr,
        lazy_member,
        m,
        main,
        merge_lazy_imports,
        normalize_lazy_imports,
        p,
        resolve_lazy_members,
        s,
        settings,
    )


__all__: tuple[str, ...] = (
    "ExamplesFlextGrpcConstants",
    "ExamplesFlextGrpcModels",
    "ExamplesFlextGrpcProtocols",
    "ExamplesFlextGrpcTypes",
    "ExamplesFlextGrpcUtilities",
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
        "ExamplesFlextGrpcConstants": ".constants",
        "ExamplesFlextGrpcModels": ".models",
        "ExamplesFlextGrpcProtocols": ".protocols",
        "ExamplesFlextGrpcTypes": ".typings",
        "ExamplesFlextGrpcUtilities": ".utilities",
        "build_lazy_import_map": "flext_grpc",
        "c": "flext_grpc",
        "cleanup_submodule_namespace": "flext_grpc",
        "config": "flext_grpc",
        "core": "flext_grpc",
        "d": "flext_core",
        "e": "flext_core",
        "grpc": "flext_grpc",
        "h": "flext_core",
        "install_lazy_exports": "flext_grpc",
        "lazy": "flext_grpc",
        "lazy_getattr": "flext_grpc",
        "lazy_member": "flext_grpc",
        "m": "flext_grpc",
        "main": "flext_grpc",
        "merge_lazy_imports": "flext_grpc",
        "normalize_lazy_imports": "flext_grpc",
        "p": "flext_grpc",
        "r": "flext_core",
        "resolve_lazy_members": "flext_grpc",
        "s": "flext_grpc",
        "settings": "flext_grpc",
        "t": ".typings",
        "u": ".utilities",
        "x": "flext_core",
    }),
    public_exports=__all__,
)
