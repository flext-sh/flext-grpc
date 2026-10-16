"""FLEXT gRPC Models - Consolidated Pydantic v2 Models.

Unified namespace with nested classes following FLEXT principles and SOLID design.
All domain models consolidated into a single class with nested structures.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliModels

from flext_grpc._models import (
    channel_models as _channel_models,
    message_models as _message_models,
    runtime_models as _runtime_models,
)
from flext_grpc._models.base import FlextGrpcModelsBase
from flext_grpc._models.config import FlextGrpcConfigModels


class FlextGrpcModels(FlextCliModels):
    """gRPC domain models extending flext-core m.

    Consolidated namespace class containing all gRPC domain models as nested classes.
    Follows FLEXT principles with clean separation of concerns and SOLID design.
    """

    # =========================================================================
    # DOMAIN MODELS - Core business entities
    # =========================================================================

    class Grpc(FlextGrpcModelsBase, FlextGrpcConfigModels):
        """Domain models for gRPC core business entities."""

        # =====================================================================
        # PROTO MESSAGE MODELS - RPC request/response messages
        # =====================================================================

        EchoRequest = _message_models.EchoRequest
        EchoResponse = _message_models.EchoResponse
        HealthRequest = _message_models.HealthRequest
        HealthResponse = _message_models.HealthResponse
        StreamInfo = _message_models.StreamInfo
        HealthCheck = _message_models.HealthCheck
        OperationExecutionRequest = _message_models.OperationExecutionRequest
        ClientConfig = _channel_models.ClientConfig
        ChannelConfig = _channel_models.ChannelConfig
        StateTransition = _channel_models.StateTransition
        StateMachine = _channel_models.StateMachine
        OperationSpec = _channel_models.OperationSpec
        Request = _channel_models.Request
        Response = _channel_models.Response
        Payload = _message_models.Payload
        Entity = _channel_models.Entity
        Channel = _channel_models.Channel
        Server = _runtime_models.Server
        Service = _runtime_models.Service
        Client = _runtime_models.Client
        GrpcStream = _runtime_models.GrpcStream
        StreamRuntimeState = _runtime_models.StreamRuntimeState
        CompleteSetup = _runtime_models.CompleteSetup


m = FlextGrpcModels

__all__: list[str] = ["FlextGrpcModels", "m"]
