"""gRPC protocols for FLEXT ecosystem.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_grpc._protocols import FlextGrpcProtocolsBase
from flext_grpc._protocols.channel_protocols import FlextGrpcProtocolsChannel
from flext_grpc._protocols.connection_protocols import FlextGrpcProtocolsConnection
from flext_grpc._protocols.resource_protocols import FlextGrpcProtocolsResource
from flext_grpc._protocols.server_protocols import FlextGrpcProtocolsServer
from flext_grpc._protocols.service_protocols import FlextGrpcProtocolsService
from flext_grpc._protocols.stream_protocols import FlextGrpcProtocolsStream


class FlextGrpcProtocols(FlextCliProtocols):
    """Unified gRPC protocols extending p.

    Extends p to inherit all foundation protocols (Result, Service, etc.)
    and adds gRPC-specific protocols in the Grpc namespace.

    Architecture:
    - EXTENDS: p (inherits Foundation, Domain, Application, etc.)
    - ADDS: gRPC-specific protocols in Grpc namespace
    - PROVIDES: Root-level alias `p` for convenient access

    Usage:
    from flext_grpc import p

    # Foundation protocols (inherited)
    result: p.Result[str]
    service: p.Grpc.Service[str]

    # gRPC-specific protocols
    server: p.Grpc.Server
    client: p.Grpc.Client
    """

    @runtime_checkable
    class Grpc(FlextGrpcProtocolsBase, Protocol):
        """gRPC domain-specific protocols.

        Provides protocols for gRPC server management, client communication,
        streaming operations, service definitions, channel management,
        metrics collection, and configuration.
        """

        ClientConnection = FlextGrpcProtocolsConnection.ClientConnection
        ServerLifecycle = FlextGrpcProtocolsServer.ServerLifecycle
        StreamProcessor = FlextGrpcProtocolsStream.StreamProcessor
        GrpcServicer = FlextGrpcProtocolsServer.GrpcServicer
        Server = FlextGrpcProtocolsServer.Server
        GrpcMessage = FlextGrpcProtocolsStream.GrpcMessage
        Client = FlextGrpcProtocolsConnection.Client
        GrpcStream = FlextGrpcProtocolsStream.GrpcStream
        Streaming = FlextGrpcProtocolsStream.Streaming
        GrpcMethodHandler = FlextGrpcProtocolsService.GrpcMethodHandler
        Service = FlextGrpcProtocolsService.Service
        Channel = FlextGrpcProtocolsChannel.Channel
        Metrics = FlextGrpcProtocolsService.Metrics
        Configuration = FlextGrpcProtocolsService.Configuration
        GrpcResource = FlextGrpcProtocolsResource.GrpcResource
        ResourceManager = FlextGrpcProtocolsResource.ResourceManager
        GrpcCallbackFunction = FlextGrpcProtocolsResource.GrpcCallbackFunction
        GrpcChannel = FlextGrpcProtocolsChannel.GrpcChannel
        GrpcRpcHandler = FlextGrpcProtocolsServer.GrpcRpcHandler
        GrpcReadyFuture = FlextGrpcProtocolsChannel.GrpcReadyFuture
        GrpcServer = FlextGrpcProtocolsServer.GrpcServer
        GrpcServicerContext = FlextGrpcProtocolsServer.GrpcServicerContext
        GrpcStub = FlextGrpcProtocolsConnection.GrpcStub
        GrpcChannelCredentials = FlextGrpcProtocolsChannel.GrpcChannelCredentials
        GrpcCallFailure = FlextGrpcProtocolsConnection.GrpcCallFailure
        GrpcRuntime = FlextGrpcProtocolsResource.GrpcRuntime
        EntityFactory = FlextGrpcProtocolsResource.EntityFactory
        OperationHandler = FlextGrpcProtocolsResource.OperationHandler


p = FlextGrpcProtocols

__all__: list[str] = ["FlextGrpcProtocols", "p"]
