"""FLEXT gRPC Types - Domain types and protocols.

Copyright (c) 2025 FLEXT Contributors
SPDX-License-Identifier: MIT
"""

from __future__ import annotations

import re
from typing import Literal, NewType, Protocol, runtime_checkable

# Constants for port validation
MIN_PORT = 1
MAX_PORT = 65535

# =============================================================================
# DOMAIN TYPES - Clean and focused
# =============================================================================

# Communication Types
TGrpcTarget = NewType("TGrpcTarget", str)  # host:port format
TGrpcMethodName = NewType("TGrpcMethodName", str)  # service/method format
TGrpcServiceName = NewType("TGrpcServiceName", str)  # service identifier

# State Types
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

# Configuration Types
TGrpcHost = NewType("TGrpcHost", str)
TGrpcPort = NewType("TGrpcPort", int)
TGrpcTimeout = NewType("TGrpcTimeout", float)

# =============================================================================
# PROTOCOLS - For gRPC library integration
# =============================================================================


@runtime_checkable
class TGrpcChannel(Protocol):
    """Protocol for grpc.Channel objects."""

    def close(self) -> None:
        """Close the channel."""

    def unsubscribe(self, callback: object) -> None:
        """Unsubscribe from channel state changes."""


@runtime_checkable
class TGrpcServer(Protocol):
    """Protocol for grpc.Server objects."""

    def add_generic_rpc_handlers(self, handlers: list[object]) -> None:
        """Add RPC handlers to server."""

    def start(self) -> None:
        """Start the server."""

    def stop(self, grace: float | None) -> None:
        """Stop the server."""


@runtime_checkable
class TGrpcStub(Protocol):
    """Protocol for gRPC stub objects."""

    def __init__(self, channel: TGrpcChannel) -> None:
        """Initialize stub with channel."""


# =============================================================================
# VALIDATION FUNCTIONS
# =============================================================================


def flext_grpc_validate_target(target: str) -> bool:
    """Validate gRPC target format (host:port)."""
    if not target or ":" not in target:
        return False

    try:
        host, port_str = target.split(":", 1)
        if not host or not port_str:
            return False

        # Basic hostname validation
        if not re.match(r"^[a-zA-Z0-9.-]+$", host):
            return False

        # Port validation
        port = int(port_str)
        return MIN_PORT <= port <= MAX_PORT

    except (ValueError, AttributeError):
        return False


def flext_grpc_parse_target(target: str) -> tuple[str, int] | None:
    """Parse gRPC target into host and port."""
    if not flext_grpc_validate_target(target):
        return None

    host, port_str = target.split(":", 1)
    return (host, int(port_str))
