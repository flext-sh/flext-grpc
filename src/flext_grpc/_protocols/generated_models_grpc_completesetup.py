# AUTO-GENERATED FILE — Regenerate with: make gen
"""Source-derived structural model contract.

Copyright (c) 2026 FLEXT Team. All rights reserved.
src/flext_grpc/_protocols/generated_models_grpc_completesetup
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable

from flext_grpc._protocols import (
    FlextGrpcProtocolsConnection,
    FlextGrpcProtocolsServer,
    FlextGrpcProtocolsService,
)


class FlextGrpcGrpcProtocolsGeneratedModelsCompleteSetup:
    """Own the structural model contract declared by this module."""

    @runtime_checkable
    class CompleteSetup(Protocol):
        """Structural data contract projected from the owning model."""

        server: FlextGrpcProtocolsServer.Server
        client: FlextGrpcProtocolsConnection.Client
        service: FlextGrpcProtocolsService.Service
        target: str


__all__: list[str] = [
    "FlextGrpcGrpcProtocolsGeneratedModelsCompleteSetup",
]
