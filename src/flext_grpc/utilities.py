"""FLEXT gRPC Utilities - Essential utilities for gRPC operations.

Simplified utilities module containing only actively used methods.
Follows FLEXT standards with minimal, focused functionality.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT

"""

from __future__ import annotations

from collections.abc import Mapping

from flext_core import FlextUtilities, r

from flext_grpc import c, m, t
from flext_grpc._utilities.grpc import FlextGrpcUtilitiesGrpc


class FlextGrpcUtilities(FlextUtilities):
    """Utilities for gRPC operations in FLEXT ecosystem.

    Provides helper methods for gRPC channel, server, and stream management.
    Follows FLEXT patterns with minimal, focused functionality.
    """

    @classmethod
    def create_channel_entity(
        cls,
        target: str,
        options: Mapping[str, t.ContainerValue | None] | None = None,
    ) -> r[m.Grpc.Channel]:
        """Delegate to Grpc.create_channel_entity."""
        return cls.Grpc.create_channel_entity(target=target, options=options)

    @classmethod
    def create_client_entity(
        cls,
        target: str,
        options: Mapping[str, t.ContainerValue | None] | None = None,
    ) -> r[m.Grpc.Client]:
        """Delegate to Grpc.create_client_entity."""
        return cls.Grpc.create_client_entity(target=target, options=options)

    @classmethod
    def create_server_entity(
        cls,
        host: str = c.Grpc.GrpcNetwork.DEFAULT_HOST,
        port: int = c.Grpc.GrpcNetwork.DEFAULT_GRPC_PORT,
        max_workers: int = c.Grpc.Service.DEFAULT_MAX_WORKERS,
    ) -> r[m.Grpc.Server]:
        """Delegate to Grpc.create_server_entity."""
        return cls.Grpc.create_server_entity(
            host=host,
            port=port,
            max_workers=max_workers,
        )

    @classmethod
    def create_service_entity(
        cls,
        name: str,
        methods: t.StrSequence | None = None,
    ) -> r[m.Grpc.Service]:
        """Delegate to Grpc.create_service_entity."""
        return cls.Grpc.create_service_entity(name=name, methods=methods)

    @classmethod
    def create_stream_entity(
        cls,
        method_name: str,
        stream_type: c.Grpc.GrpcOperations | str,
    ) -> r[m.Grpc.GrpcStream]:
        """Delegate to Grpc.create_stream_entity."""
        return cls.Grpc.create_stream_entity(
            method_name=method_name,
            stream_type=stream_type,
        )

    class Grpc(FlextGrpcUtilitiesGrpc):
        """gRPC-specific utility methods."""


u = FlextGrpcUtilities

__all__ = ["FlextGrpcUtilities", "u"]
