"""FLEXT gRPC Types - Centralized type definitions and protocols.

This module centralizes all type aliases, Literal states, NewType wrappers and
Protocol contracts for the gRPC integration, following flext-core semantics.

Copyright (c) 2025 FLEXT Team. All rights reserved.
SPDX-License-Identifier: MIT.
"""

from __future__ import annotations

import re
from typing import Literal, NewType, Protocol, runtime_checkable

from flext_core import FlextLogger, FlextTypes

# Network validation constants for port range enforcement
MIN_PORT = 1
MAX_PORT = 65535


TGrpcTarget = NewType("TGrpcTarget", str)
TGrpcMethodName = NewType("TGrpcMethodName", str)
TGrpcServiceName = NewType("TGrpcServiceName", str)
TGrpcHost = NewType("TGrpcHost", str)
TGrpcPort = NewType("TGrpcPort", int)
TGrpcEntityId = NewType("TGrpcEntityId", str)
TGrpcTimeout = NewType("TGrpcTimeout", float)


TGrpcChannelState = Literal[
    "idle",
    "connecting",
    "ready",
    "transient_failure",
    "shutdown",
]
TGrpcServerState = Literal["stopped", "starting", "running", "stopping"]
TGrpcStreamType = Literal[
    "unary",
    "server_streaming",
    "client_streaming",
    "bidirectional",
]


TStreamRequestData = NewType("TStreamRequestData", str)
TStreamResponse = NewType("TStreamResponse", FlextTypes.Core.Dict)
TStreamRequestIterator = NewType("TStreamRequestIterator", object)
TStreamResponseIterator = NewType("TStreamResponseIterator", object)


@runtime_checkable
class TGrpcChannel(Protocol):
    """Protocol for minimal gRPC channel operations."""

    def close(self) -> None:
        """Close the channel."""

    def unsubscribe(self, callback: object) -> None:
        """Remove a subscription callback from the channel."""


@runtime_checkable
class TGrpcServer(Protocol):
    """Protocol for minimal gRPC server operations."""

    def add_generic_rpc_handlers(self, handlers: FlextTypes.Core.List) -> None:
        """Add generic RPC handlers."""

    def start(self) -> None:
        """Start the server."""

    def stop(self, grace: float | None) -> None:
        """Stop the server with optional grace period."""


@runtime_checkable
class TGrpcStub(Protocol):
    """Protocol for minimal gRPC client stub."""

    def __init__(self, channel: TGrpcChannel) -> None:
        """Initialize the stub with a channel."""


def flext_grpc_validate_target(target: str) -> bool:
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
        return MIN_PORT <= port <= MAX_PORT
    except (ValueError, AttributeError):
        logger = FlextLogger(__name__)
        logger.debug("Invalid gRPC target: %s", target)
        return False


def flext_grpc_parse_target(target: str) -> tuple[str, int]:
    """Parse a validated gRPC target into (host, port).

    Raises ValueError if the target is invalid. Prefer checking with
    flext_grpc_validate_target() beforehand when you need a boolean.

    Returns:
            tuple[str, int]:: Description of return value.

    """
    if not flext_grpc_validate_target(target):
        msg = f"Invalid gRPC target: {target}"
        raise ValueError(msg)
    host, port_str = target.split(":", 1)
    return (host, int(port_str))


__all__ = [
    # Protocols
    "TGrpcChannel",
    # States
    "TGrpcChannelState",
    "TGrpcEntityId",
    "TGrpcHost",
    "TGrpcMethodName",
    "TGrpcPort",
    "TGrpcServer",
    "TGrpcServerState",
    "TGrpcServiceName",
    "TGrpcStreamType",
    "TGrpcStub",
    "TGrpcTarget",
    "TGrpcTimeout",
    "flext_grpc_parse_target",
    # Helpers
    "flext_grpc_validate_target",
]
