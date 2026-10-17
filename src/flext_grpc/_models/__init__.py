# AUTO-GENERATED FILE — Regenerate with: make gen
"""Flext Grpc. Models package.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from types import MappingProxyType
from typing import TYPE_CHECKING

from flext_core.lazy import install_lazy_exports

if TYPE_CHECKING:
    from flext_grpc._models.base import FlextGrpcModelsBase
    from flext_grpc._models.channel_models import (
        Channel,
        ChannelConfig,
        ClientConfig,
        Entity,
        FlextGrpcModelsChannel,
        OperationSpec,
        Request,
        Response,
        StateMachine,
        StateTransition,
    )
    from flext_grpc._models.config import FlextGrpcConfigModels
    from flext_grpc._models.message_models import (
        EchoRequest,
        EchoResponse,
        FlextGrpcModelsMessage,
        HealthCheck,
        HealthRequest,
        HealthResponse,
        OperationExecutionRequest,
        Payload,
        StreamInfo,
    )
    from flext_grpc._models.runtime_models import (
        Client,
        CompleteSetup,
        FlextGrpcModelsRuntime,
        GrpcStream,
        Server,
        Service,
        StreamRuntimeState,
    )


__all__: tuple[str, ...] = (
    "Channel",
    "ChannelConfig",
    "Client",
    "ClientConfig",
    "CompleteSetup",
    "EchoRequest",
    "EchoResponse",
    "Entity",
    "FlextGrpcConfigModels",
    "FlextGrpcModelsBase",
    "FlextGrpcModelsChannel",
    "FlextGrpcModelsMessage",
    "FlextGrpcModelsRuntime",
    "GrpcStream",
    "HealthCheck",
    "HealthRequest",
    "HealthResponse",
    "OperationExecutionRequest",
    "OperationSpec",
    "Payload",
    "Request",
    "Response",
    "Server",
    "Service",
    "StateMachine",
    "StateTransition",
    "StreamInfo",
    "StreamRuntimeState",
)

install_lazy_exports(
    __name__,
    globals(),
    MappingProxyType({
        "Channel": ".channel_models",
        "ChannelConfig": ".channel_models",
        "Client": ".runtime_models",
        "ClientConfig": ".channel_models",
        "CompleteSetup": ".runtime_models",
        "EchoRequest": ".message_models",
        "EchoResponse": ".message_models",
        "Entity": ".channel_models",
        "FlextGrpcConfigModels": ".config",
        "FlextGrpcModelsBase": ".base",
        "FlextGrpcModelsChannel": ".channel_models",
        "FlextGrpcModelsMessage": ".message_models",
        "FlextGrpcModelsRuntime": ".runtime_models",
        "GrpcStream": ".runtime_models",
        "HealthCheck": ".message_models",
        "HealthRequest": ".message_models",
        "HealthResponse": ".message_models",
        "OperationExecutionRequest": ".message_models",
        "OperationSpec": ".channel_models",
        "Payload": ".message_models",
        "Request": ".channel_models",
        "Response": ".channel_models",
        "Server": ".runtime_models",
        "Service": ".runtime_models",
        "StateMachine": ".channel_models",
        "StateTransition": ".channel_models",
        "StreamInfo": ".message_models",
        "StreamRuntimeState": ".runtime_models",
    }),
    public_exports=__all__,
)
