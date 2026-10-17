# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Protocols package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._protocols.base import FlextGrpcProtocolsBase
    from flext_grpc._protocols.channel_protocols import (
        Channel,
        FlextGrpcProtocolsChannel,
        GrpcChannel,
        GrpcChannelCredentials,
        GrpcReadyFuture,
    )
    from flext_grpc._protocols.config import FlextGrpcProtocolsConfig
    from flext_grpc._protocols.connection_protocols import (
        Client,
        ClientConnection,
        FlextGrpcProtocolsConnection,
        GrpcCallFailure,
        GrpcStub,
    )
    from flext_grpc._protocols.resource_protocols import (
        EntityFactory,
        FlextGrpcProtocolsResource,
        GrpcCallbackFunction,
        GrpcResource,
        GrpcRuntime,
        OperationHandler,
        ResourceManager,
    )
    from flext_grpc._protocols.server_protocols import (
        FlextGrpcProtocolsServer,
        GrpcRpcHandler,
        GrpcServer,
        GrpcServicer,
        GrpcServicerContext,
        Server,
        ServerLifecycle,
    )
    from flext_grpc._protocols.service_protocols import (
        Configuration,
        FlextGrpcProtocolsService,
        GrpcMethodHandler,
        Metrics,
        Service,
    )
    from flext_grpc._protocols.stream_protocols import (
        FlextGrpcProtocolsStream,
        GrpcMessage,
        GrpcStream,
        Streaming,
        StreamProcessor,
    )


__all__: tuple[str, ...] = (
    "Channel",
    "Client",
    "ClientConnection",
    "Configuration",
    "EntityFactory",
    "FlextGrpcProtocolsBase",
    "FlextGrpcProtocolsChannel",
    "FlextGrpcProtocolsConfig",
    "FlextGrpcProtocolsConnection",
    "FlextGrpcProtocolsResource",
    "FlextGrpcProtocolsServer",
    "FlextGrpcProtocolsService",
    "FlextGrpcProtocolsStream",
    "GrpcCallFailure",
    "GrpcCallbackFunction",
    "GrpcChannel",
    "GrpcChannelCredentials",
    "GrpcMessage",
    "GrpcMethodHandler",
    "GrpcReadyFuture",
    "GrpcResource",
    "GrpcRpcHandler",
    "GrpcRuntime",
    "GrpcServer",
    "GrpcServicer",
    "GrpcServicerContext",
    "GrpcStream",
    "GrpcStub",
    "Metrics",
    "OperationHandler",
    "ResourceManager",
    "Server",
    "ServerLifecycle",
    "Service",
    "StreamProcessor",
    "Streaming",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "Channel": ".channel_protocols",
        "Client": ".connection_protocols",
        "ClientConnection": ".connection_protocols",
        "Configuration": ".service_protocols",
        "EntityFactory": ".resource_protocols",
        "FlextGrpcProtocolsBase": ".base",
        "FlextGrpcProtocolsChannel": ".channel_protocols",
        "FlextGrpcProtocolsConfig": ".config",
        "FlextGrpcProtocolsConnection": ".connection_protocols",
        "FlextGrpcProtocolsResource": ".resource_protocols",
        "FlextGrpcProtocolsServer": ".server_protocols",
        "FlextGrpcProtocolsService": ".service_protocols",
        "FlextGrpcProtocolsStream": ".stream_protocols",
        "GrpcCallFailure": ".connection_protocols",
        "GrpcCallbackFunction": ".resource_protocols",
        "GrpcChannel": ".channel_protocols",
        "GrpcChannelCredentials": ".channel_protocols",
        "GrpcMessage": ".stream_protocols",
        "GrpcMethodHandler": ".service_protocols",
        "GrpcReadyFuture": ".channel_protocols",
        "GrpcResource": ".resource_protocols",
        "GrpcRpcHandler": ".server_protocols",
        "GrpcRuntime": ".resource_protocols",
        "GrpcServer": ".server_protocols",
        "GrpcServicer": ".server_protocols",
        "GrpcServicerContext": ".server_protocols",
        "GrpcStream": ".stream_protocols",
        "GrpcStub": ".connection_protocols",
        "Metrics": ".service_protocols",
        "OperationHandler": ".resource_protocols",
        "ResourceManager": ".resource_protocols",
        "Server": ".server_protocols",
        "ServerLifecycle": ".server_protocols",
        "Service": ".service_protocols",
        "StreamProcessor": ".stream_protocols",
        "Streaming": ".stream_protocols",
    }),
    public_exports=__all__,
)
