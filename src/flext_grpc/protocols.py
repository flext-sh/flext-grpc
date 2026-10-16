"""gRPC protocols for FLEXT ecosystem.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_cli import FlextCliProtocols

from flext_grpc._protocols import (
    FlextGrpcProtocolsBase,
    channel_protocols as _channel_protocols,
    connection_protocols as _connection_protocols,
    resource_protocols as _resource_protocols,
    server_protocols as _server_protocols,
    service_protocols as _service_protocols,
    stream_protocols as _stream_protocols,
)


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

        ClientConnection = _connection_protocols.ClientConnection
        ServerLifecycle = _server_protocols.ServerLifecycle
        StreamProcessor = _stream_protocols.StreamProcessor
        GrpcServicer = _server_protocols.GrpcServicer
        Server = _server_protocols.Server
        GrpcMessage = _stream_protocols.GrpcMessage
        Client = _connection_protocols.Client
        GrpcStream = _stream_protocols.GrpcStream
        Streaming = _stream_protocols.Streaming
        GrpcMethodHandler = _service_protocols.GrpcMethodHandler
        Service = _service_protocols.Service
        Channel = _channel_protocols.Channel
        Metrics = _service_protocols.Metrics
        Configuration = _service_protocols.Configuration
        GrpcResource = _resource_protocols.GrpcResource
        ResourceManager = _resource_protocols.ResourceManager
        GrpcCallbackFunction = _resource_protocols.GrpcCallbackFunction
        GrpcChannel = _channel_protocols.GrpcChannel
        GrpcRpcHandler = _server_protocols.GrpcRpcHandler
        GrpcReadyFuture = _channel_protocols.GrpcReadyFuture
        GrpcServer = _server_protocols.GrpcServer
        GrpcServicerContext = _server_protocols.GrpcServicerContext
        GrpcStub = _connection_protocols.GrpcStub
        GrpcChannelCredentials = _channel_protocols.GrpcChannelCredentials
        GrpcCallFailure = _connection_protocols.GrpcCallFailure
        GrpcRuntime = _resource_protocols.GrpcRuntime
        EntityFactory = _resource_protocols.EntityFactory
        OperationHandler = _resource_protocols.OperationHandler


p = FlextGrpcProtocols

__all__: list[str] = ["FlextGrpcProtocols", "p"]
