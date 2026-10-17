# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_grpc._models import (
    FlextGrpcConfigModels,
    FlextGrpcModelsBase,
    FlextGrpcModelsChannel,
    FlextGrpcModelsMessage,
    FlextGrpcModelsRuntime,
)


class FlextGrpcModels(FlextCliModels):
    """gRPC domain models extending flext-core m.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Grpc(
        FlextGrpcModelsBase,
        FlextGrpcModelsChannel,
        FlextGrpcConfigModels,
        FlextGrpcModelsMessage,
        FlextGrpcModelsRuntime,
    ):
        """Domain models for gRPC core business entities."""

        # =====================================================================
        # PROTO MESSAGE MODELS - RPC request/response messages
        # =====================================================================

        EchoRequest = FlextGrpcModelsMessage.EchoRequest
        EchoResponse = FlextGrpcModelsMessage.EchoResponse
        HealthRequest = FlextGrpcModelsMessage.HealthRequest
        HealthResponse = FlextGrpcModelsMessage.HealthResponse
        StreamInfo = FlextGrpcModelsMessage.StreamInfo
        HealthCheck = FlextGrpcModelsMessage.HealthCheck
        OperationExecutionRequest = FlextGrpcModelsMessage.OperationExecutionRequest
        ClientConfig = FlextGrpcModelsChannel.ClientConfig
        ChannelConfig = FlextGrpcModelsChannel.ChannelConfig
        StateTransition = FlextGrpcModelsChannel.StateTransition
        StateMachine = FlextGrpcModelsChannel.StateMachine
        OperationSpec = FlextGrpcModelsChannel.OperationSpec
        Request = FlextGrpcModelsChannel.Request
        Response = FlextGrpcModelsChannel.Response
        Payload = FlextGrpcModelsMessage.Payload
        Entity = FlextGrpcModelsChannel.Entity
        Channel = FlextGrpcModelsChannel.Channel
        Server = FlextGrpcModelsRuntime.Server
        Service = FlextGrpcModelsRuntime.Service
        Client = FlextGrpcModelsRuntime.Client
        GrpcStream = FlextGrpcModelsRuntime.GrpcStream
        StreamRuntimeState = FlextGrpcModelsRuntime.StreamRuntimeState
        CompleteSetup = FlextGrpcModelsRuntime.CompleteSetup


m = FlextGrpcModels

__all__: list[str] = ["FlextGrpcModels", "m"]
