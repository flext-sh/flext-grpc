"""FLEXT gRPC Proto Servicer - service-side registration primitives.

Provides the runtime servicer base and server-registration helper used by
services.py until full protobuf code generation is in place. Split from
stub.py (ENFORCE-067: one top-level class per module).

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

from flext_grpc.protocols import FlextGrpcProtocols


class FlextGrpcServiceServicer:
    """Base class for gRPC service implementations."""


def add_flext_grpc_service_servicer_to_server(
    servicer: FlextGrpcProtocols.Grpc.GrpcServicer,
    server: FlextGrpcProtocols.Grpc.GrpcServer,
) -> None:
    """Add gRPC service servicer to server."""


__all__ = ["FlextGrpcServiceServicer", "add_flext_grpc_service_servicer_to_server"]
