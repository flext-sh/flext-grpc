# AUTO-GENERATED FILE — Regenerate with: make gen
"""FLEXT gRPC utilities facade.

Copyright (c) 2026 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from collections.abc import (
    Iterable,
    Iterator,
    Mapping,
    MutableMapping,
    MutableSequence,
    Sequence,
)

from flext_cli import u as flext_cli_u

from flext_grpc._utilities import (
    FlextGrpcUtilitiesBase,
    FlextGrpcUtilitiesGrpc,
    FlextGrpcUtilitiesGrpcRuntime,
    FlextGrpcUtilitiesGrpcService,
    FlextGrpcUtilitiesSchemaCodegen,
)


class FlextGrpcUtilities(flext_cli_u, FlextGrpcUtilitiesBase):
    """Utilities for gRPC operations in the FLEXT ecosystem."""

    class Grpc(
        FlextGrpcUtilitiesGrpc,
        FlextGrpcUtilitiesGrpcRuntime,
        FlextGrpcUtilitiesGrpcService,
        FlextGrpcUtilitiesSchemaCodegen,
        FlextGrpcUtilitiesBase,
    ):
        """Public gRPC utility namespace with explicit local signatures.

        This nested class re-exports the factory/validation helpers from
        ``FlextGrpcUtilitiesGrpc`` so that static type checkers see concrete
        return types for ``u.Grpc.*`` calls inside ``flext_grpc`` services.
        """


u = FlextGrpcUtilities
__all__: list[str] = ["FlextGrpcUtilities", "u"]
