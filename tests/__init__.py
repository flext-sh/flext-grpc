# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from examples import (
        ExamplesFlextGrpcConstants,
        ExamplesFlextGrpcModels,
        ExamplesFlextGrpcProtocols,
        ExamplesFlextGrpcTypes,
        ExamplesFlextGrpcUtilities,
    )
    from flext_core import d, e, h, r, x
    from flext_tests import api, td, tf, tk, tm

    from flext_grpc import (
        FlextGrpc,
        FlextGrpcConfig,
        FlextGrpcConstants,
        FlextGrpcErrors,
        FlextGrpcModels,
        FlextGrpcModelsConfigNamespace,
        FlextGrpcProtocols,
        FlextGrpcServiceBase,
        FlextGrpcSettings,
        FlextGrpcTypes,
        FlextGrpcUtilities,
        FlextGrpcVersion,
        __author__,
        __author_email__,
        __description__,
        __license__,
        __title__,
        __url__,
        __version__,
        __version_info__,
        config,
        grpc,
        main,
        settings,
    )
    from tests.base import TestsFlextGrpcServiceBase, s
    from tests.constants import TestsFlextGrpcConstants, c
    from tests.models import TestsFlextGrpcModels, m
    from tests.protocols import TestsFlextGrpcProtocols, p
    from tests.settings import TestsFlextGrpcSettings
    from tests.typings import TestsFlextGrpcTypes, t
    from tests.utilities import TestsFlextGrpcUtilities, u


__all__: tuple[str, ...] = (
    "ExamplesFlextGrpcConstants",
    "ExamplesFlextGrpcModels",
    "ExamplesFlextGrpcProtocols",
    "ExamplesFlextGrpcTypes",
    "ExamplesFlextGrpcUtilities",
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
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcServiceBase",
    "TestsFlextGrpcSettings",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcUtilities",
    "__author__",
    "__author_email__",
    "__description__",
    "__license__",
    "__title__",
    "__url__",
    "__version__",
    "__version_info__",
    "api",
    "c",
    "config",
    "d",
    "e",
    "grpc",
    "h",
    "m",
    "main",
    "p",
    "r",
    "s",
    "settings",
    "t",
    "td",
    "tf",
    "tk",
    "tm",
    "u",
    "x",
)

install_lazy_exports(
    __name__,
    globals(),
    {
        "ExamplesFlextGrpcConstants": "examples",
        "ExamplesFlextGrpcModels": "examples",
        "ExamplesFlextGrpcProtocols": "examples",
        "ExamplesFlextGrpcTypes": "examples",
        "ExamplesFlextGrpcUtilities": "examples",
        "FlextGrpc": "flext_grpc",
        "FlextGrpcConfig": "flext_grpc",
        "FlextGrpcConstants": "flext_grpc",
        "FlextGrpcErrors": "flext_grpc",
        "FlextGrpcModels": "flext_grpc",
        "FlextGrpcModelsConfigNamespace": "flext_grpc",
        "FlextGrpcProtocols": "flext_grpc",
        "FlextGrpcServiceBase": "flext_grpc",
        "FlextGrpcSettings": "flext_grpc",
        "FlextGrpcTypes": "flext_grpc",
        "FlextGrpcUtilities": "flext_grpc",
        "FlextGrpcVersion": "flext_grpc",
        "TestsFlextGrpcConstants": ".constants",
        "TestsFlextGrpcModels": ".models",
        "TestsFlextGrpcProtocols": ".protocols",
        "TestsFlextGrpcServiceBase": ".base",
        "TestsFlextGrpcSettings": ".settings",
        "TestsFlextGrpcTypes": ".typings",
        "TestsFlextGrpcUtilities": ".utilities",
        "__author__": "flext_grpc",
        "__author_email__": "flext_grpc",
        "__description__": "flext_grpc",
        "__license__": "flext_grpc",
        "__title__": "flext_grpc",
        "__url__": "flext_grpc",
        "__version__": "flext_grpc",
        "__version_info__": "flext_grpc",
        "api": "flext_tests",
        "c": ".constants",
        "config": "flext_grpc",
        "d": "flext_core",
        "e": "flext_core",
        "grpc": "flext_grpc",
        "h": "flext_core",
        "m": ".models",
        "main": "flext_grpc",
        "p": ".protocols",
        "r": "flext_core",
        "s": ".base",
        "settings": "flext_grpc",
        "t": ".typings",
        "td": "flext_tests",
        "tf": "flext_tests",
        "tk": "flext_tests",
        "tm": "flext_tests",
        "u": ".utilities",
        "x": "flext_core",
    },
    public_exports=__all__,
)
