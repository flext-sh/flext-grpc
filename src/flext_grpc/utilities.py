"""FLEXT gRPC utilities facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_cli import FlextCliUtilities

from flext_grpc._utilities.base import FlextGrpcUtilitiesBase
from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc
from flext_grpc._utilities.grpc_runtime import FlextGrpcUtilitiesGrpcRuntime
from flext_grpc._utilities.grpc_service import FlextGrpcUtilitiesGrpcService
from flext_grpc._utilities.grpc_signatures import FlextGrpcUtilitiesGrpcSignatures


class FlextGrpcUtilities(FlextCliUtilities, FlextGrpcUtilitiesBase):
    """Utilities for gRPC operations in the FLEXT ecosystem."""

    class Grpc(
        FlextGrpcUtilitiesGrpcSignatures,
        FlextGrpcUtilitiesBase,
        FlextGrpcUtilitiesGrpc,
        FlextGrpcUtilitiesGrpcRuntime,
        FlextGrpcUtilitiesGrpcService,
    ):
        """Public gRPC utility namespace with explicit local signatures.

        This nested class re-exports the factory/validation helpers from
        ``FlextGrpcUtilitiesGrpc`` so that static type checkers see concrete
        return types for ``u.Grpc.*`` calls inside ``flext_grpc`` services.
        """


u = FlextGrpcUtilities

__all__: list[str] = ["FlextGrpcUtilities", "u"]
