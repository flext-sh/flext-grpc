"""FLEXT Module.

Copyright (c) 2025 FLEXT Team. All rights reserved. SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import re
from typing import Literal, NewType, Protocol, runtime_checkable

from flext_core import FlextLogger, FlextTypes


class FlextGrpcTypes(FlextTypes):
    """Unified gRPC type definitions extending flext-core FlextTypes.

    Single unified class containing all gRPC type definitions
    following SOLID principles and FLEXT ecosystem patterns.

    Uses FlextTypes inheritance to reduce code duplication and ensure
    consistent type patterns across the FLEXT ecosystem.
    """

    # =============================================================================
    # NETWORK CONSTANTS
    # =============================================================================
    MIN_PORT = 1
    MAX_PORT = 65535

    # =============================================================================
    # GRPC CORE TYPES - Basic gRPC types extending FlextTypes
    # =============================================================================

    class Core(FlextTypes.Core):
        """Core gRPC types extending flext-core types."""

        # gRPC target and identification types
        GrpcTarget = NewType("GrpcTarget", str)
        GrpcMethodName = NewType("GrpcMethodName", str)
        GrpcServiceName = NewType("GrpcServiceName", str)
        GrpcHost = NewType("GrpcHost", str)
        GrpcPort = NewType("GrpcPort", int)
        GrpcEntityId = NewType("GrpcEntityId", str)
        GrpcTimeout = NewType("GrpcTimeout", float)

        # gRPC state types
        GrpcChannelState = Literal[
            "idle",
            "connecting",
            "ready",
            "transient_failure",
            "shutdown",
        ]
        GrpcServerState = Literal["stopped", "starting", "running", "stopping"]
        GrpcStreamType = Literal[
            "unary",
            "server_streaming",
            "client_streaming",
            "bidirectional",
        ]

    # =============================================================================
    # GRPC STREAMING TYPES
    # =============================================================================

    class Streaming:
        """gRPC streaming operation types."""

        StreamRequestData = NewType("StreamRequestData", str)
        StreamResponse = NewType("StreamResponse", FlextTypes.Core.Dict)
        StreamRequestIterator = NewType("StreamRequestIterator", object)
        StreamResponseIterator = NewType("StreamResponseIterator", object)

    # =============================================================================
    # GRPC PROTOCOLS - Protocol definitions for gRPC interfaces
    # =============================================================================

    class Protocols:
        """gRPC protocol types for interface definitions."""

        @runtime_checkable
        class GrpcChannel(Protocol):
            """Protocol for minimal gRPC channel operations."""

            def close(self: object) -> None:
                """Close the channel."""

            def unsubscribe(self, callback: object) -> None:
                """Remove a subscription callback from the channel."""

        @runtime_checkable
        class GrpcServer(Protocol):
            """Protocol for minimal gRPC server operations."""

            def add_generic_rpc_handlers(self, handlers: FlextTypes.Core.List) -> None:
                """Add generic RPC handlers."""

            def start(self: object) -> None:
                """Start the server."""

            def stop(self, grace: float | None) -> None:
                """Stop the server with optional grace period."""

        @runtime_checkable
        class GrpcStub(Protocol):
            """Protocol for minimal gRPC client stub."""

            def __init__(self, channel: FlextGrpcTypes.Protocols.GrpcChannel) -> None:
                """Initialize the stub with a channel."""

    # =============================================================================
    # GRPC VALIDATION - Helper functions for gRPC operations
    # =============================================================================

    class Validation:
        """gRPC validation utilities."""

        @staticmethod
        def validate_target(target: str) -> bool:
            """Validate a gRPC target string in the form host:port."""
            if not target or ":" not in target:
                return False
            try:
                host, port_str = target.split(":", 1)
                if not host or not port_str:
                    return False
                if not re.match(r"^[a-zA-Z0-9.-]+$", host):
                    return False
                port = int(port_str)
                return FlextGrpcTypes.MIN_PORT <= port <= FlextGrpcTypes.MAX_PORT
            except (ValueError, AttributeError):
                logger = FlextLogger(__name__)
                logger.debug("Invalid gRPC target: %s", target)
                return False

        @staticmethod
        def parse_target(target: str) -> tuple[str, int]:
            """Parse a validated gRPC target into (host, port).

            Raises ValueError if the target is invalid. Prefer checking with
            validate_target() beforehand when you need a boolean.

            Returns:
                    tuple[str, int]:: Description of return value.

            """
            if not FlextGrpcTypes.Validation.validate_target(target):
                msg = f"Invalid gRPC target: {target}"
                raise ValueError(msg)
            host, port_str = target.split(":", 1)
            return (host, int(port_str))


__all__ = [
    "FlextGrpcTypes",
]
