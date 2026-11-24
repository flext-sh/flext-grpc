# AUTO-GENERATED FILE — Regenerate with: make gen
"""Tests package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
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
        config,
        grpc,
        main,
        settings,
    )
    from flext_grpc.protos import (
        DESCRIPTOR,
        GRPC_GENERATED_VERSION,
        RPC_PYTHON_METHOD_NAMES,
        EchoRequest,
        EchoResponse,
        FlextGrpcServiceServicer,
        FlextGrpcServiceStub,
        HealthRequest,
        HealthResponse,
        add_flext_grpc_service_servicer_to_server,
    )
    from flext_grpc.services import (
        FlextGrpcApiRuntime,
        FlextGrpcClient,
        FlextGrpcConnectionPool,
        FlextGrpcConnectionPoolImpl,
        FlextGrpcMetrics,
        FlextGrpcMetricsCollectorImpl,
        FlextGrpcServer,
        FlextGrpcStream,
    )
    from tests.base import TestsFlextGrpcServiceBase, s
    from tests.constants import TestsFlextGrpcConstants, c
    from tests.models import TestsFlextGrpcModels, m
    from tests.protocols import TestsFlextGrpcProtocols, p
    from tests.settings import TestsFlextGrpcSettings
    from tests.typings import TestsFlextGrpcTypes, t
    from tests.utilities import TestsFlextGrpcUtilities, u


__all__: tuple[str, ...] = (
    "DESCRIPTOR",
    "GRPC_GENERATED_VERSION",
    "RPC_PYTHON_METHOD_NAMES",
    "EchoRequest",
    "EchoResponse",
    "FlextGrpc",
    "FlextGrpcApiRuntime",
    "FlextGrpcClient",
    "FlextGrpcConfig",
    "FlextGrpcConnectionPool",
    "FlextGrpcConnectionPoolImpl",
    "FlextGrpcConstants",
    "FlextGrpcErrors",
    "FlextGrpcMetrics",
    "FlextGrpcMetricsCollectorImpl",
    "FlextGrpcModels",
    "FlextGrpcModelsConfigNamespace",
    "FlextGrpcProtocols",
    "FlextGrpcServer",
    "FlextGrpcServiceBase",
    "FlextGrpcServiceServicer",
    "FlextGrpcServiceStub",
    "FlextGrpcSettings",
    "FlextGrpcStream",
    "FlextGrpcTypes",
    "FlextGrpcUtilities",
    "FlextGrpcVersion",
    "HealthRequest",
    "HealthResponse",
    "TestsFlextGrpcConstants",
    "TestsFlextGrpcModels",
    "TestsFlextGrpcProtocols",
    "TestsFlextGrpcServiceBase",
    "TestsFlextGrpcSettings",
    "TestsFlextGrpcTypes",
    "TestsFlextGrpcUtilities",
    "add_flext_grpc_service_servicer_to_server",
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
        "DESCRIPTOR": "flext_grpc.protos",
        "GRPC_GENERATED_VERSION": "flext_grpc.protos",
        "RPC_PYTHON_METHOD_NAMES": "flext_grpc.protos",
        "EchoRequest": "flext_grpc.protos",
        "EchoResponse": "flext_grpc.protos",
        "FlextGrpc": "flext_grpc",
        "FlextGrpcApiRuntime": "flext_grpc.services",
        "FlextGrpcClient": "flext_grpc.services",
        "FlextGrpcConfig": "flext_grpc",
        "FlextGrpcConnectionPool": "flext_grpc.services",
        "FlextGrpcConnectionPoolImpl": "flext_grpc.services",
        "FlextGrpcConstants": "flext_grpc",
        "FlextGrpcErrors": "flext_grpc",
        "FlextGrpcMetrics": "flext_grpc.services",
        "FlextGrpcMetricsCollectorImpl": "flext_grpc.services",
        "FlextGrpcModels": "flext_grpc",
        "FlextGrpcModelsConfigNamespace": "flext_grpc",
        "FlextGrpcProtocols": "flext_grpc",
        "FlextGrpcServer": "flext_grpc.services",
        "FlextGrpcServiceBase": "flext_grpc",
        "FlextGrpcServiceServicer": "flext_grpc.protos",
        "FlextGrpcServiceStub": "flext_grpc.protos",
        "FlextGrpcSettings": "flext_grpc",
        "FlextGrpcStream": "flext_grpc.services",
        "FlextGrpcTypes": "flext_grpc",
        "FlextGrpcUtilities": "flext_grpc",
        "FlextGrpcVersion": "flext_grpc",
        "HealthRequest": "flext_grpc.protos",
        "HealthResponse": "flext_grpc.protos",
        "TestsFlextGrpcConstants": ".constants",
        "TestsFlextGrpcModels": ".models",
        "TestsFlextGrpcProtocols": ".protocols",
        "TestsFlextGrpcServiceBase": ".base",
        "TestsFlextGrpcSettings": ".settings",
        "TestsFlextGrpcTypes": ".typings",
        "TestsFlextGrpcUtilities": ".utilities",
        "add_flext_grpc_service_servicer_to_server": "flext_grpc.protos",
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
