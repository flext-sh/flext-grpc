# AUTO-GENERATED FILE — Regenerate with: make gen
"""gRPC protocols for FLEXT ecosystem.

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

from flext_cli import p as flext_cli_p

from flext_grpc._protocols import (
    FlextGrpcProtocolsBase,
    FlextGrpcProtocolsChannel,
    FlextGrpcProtocolsConnection,
    FlextGrpcProtocolsResource,
    FlextGrpcProtocolsServer,
    FlextGrpcProtocolsService,
    FlextGrpcProtocolsStream,
)


class FlextGrpcProtocols(flext_cli_p):
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

    class Grpc(
        FlextGrpcProtocolsBase,
        FlextGrpcProtocolsChannel,
        FlextGrpcProtocolsConnection,
        FlextGrpcProtocolsService,
        FlextGrpcProtocolsResource,
        FlextGrpcProtocolsStream,
        FlextGrpcProtocolsServer,
    ):
        """gRPC domain-specific protocols.

        Provides protocols for gRPC server management, client communication,
        streaming operations, service definitions, channel management,
        metrics collection, and configuration.
        """


p = FlextGrpcProtocols
__all__: list[str] = ["FlextGrpcProtocols", "p"]
