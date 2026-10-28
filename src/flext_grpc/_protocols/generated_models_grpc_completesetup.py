"""Generated models grpc completesetup module.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_grpc/_protocols/generated_models_grpc_completesetup
SPDX-License-Identifier: MIT
"""

# AUTO-GENERATED FILE — Regenerate with: make gen
from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_grpc._protocols import (
        FlextGrpcProtocolsConnection,
        FlextGrpcProtocolsServer,
        FlextGrpcProtocolsService,
    )


class FlextGrpcModelsProtocolsGrpcGeneratedCompleteSetup:
    @runtime_checkable
    class CompleteSetup(Protocol):
        server: FlextGrpcProtocolsServer.Server
        client: FlextGrpcProtocolsConnection.Client
        service: FlextGrpcProtocolsService.Service
        target: str


__all__ = ["FlextGrpcModelsProtocolsGrpcGeneratedCompleteSetup"]
