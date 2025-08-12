"""FLEXT gRPC Types - Centralized type definitions and protocols.

This module centralizes all type aliases, Literal states, NewType wrappers and
Protocol contracts for the gRPC integration, following flext-core semantics.

- Prefer importing from this module rather than scattering across files
- Keep only one authoritative definition per type name
- Provide legacy-friendly helpers and re-exports when necessary
"""
from __future__ import annotations

import re
from typing import Literal, NewType, Protocol, runtime_checkable

from flext_core import get_logger

# Network validation constants for port range enforcement
MIN_PORT = 1
MAX_PORT = 65535

# =============================================================================
# DOMAIN AND COMMUNICATION TYPES
# =============================================================================
TGrpcTarget = NewType("TGrpcTarget", str)
TGrpcMethodName = NewType("TGrpcMethodName", str)
TGrpcServiceName = NewType("TGrpcServiceName", str)
TGrpcHost = NewType("TGrpcHost", str)
TGrpcPort = NewType("TGrpcPort", int)
TGrpcEntityId = NewType("TGrpcEntityId", str)
TGrpcTimeout = NewType("TGrpcTimeout", float)

# =============================================================================
# STATE TYPES
# =============================================================================
TGrpcChannelState = Literal["idle", "connecting", "ready", "transient_failure", "shutdown"]
TGrpcServerState = Literal["stopped", "starting", "running", "stopping"]
TGrpcStreamType = Literal["unary", "server_streaming", "client_streaming", "bidirectional"]


# =============================================================================
# PROTOCOLS
# =============================================================================
@runtime_checkable
class TGrpcChannel(Protocol):
    def close(self) -> None: ...
    def unsubscribe(self, callback: object) -> None: ...


@runtime_checkable
class TGrpcServer(Protocol):
    def add_generic_rpc_handlers(self, handlers: list[object]) -> None: ...
    def start(self) -> None: ...
    def stop(self, grace: float | None) -> None: ...


@runtime_checkable
class TGrpcStub(Protocol):
    def __init__(self, channel: TGrpcChannel) -> None: ...


# =============================================================================
# VALIDATION HELPERS
# =============================================================================

def flext_grpc_validate_target(target: str) -> bool:
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
        logger = get_logger(__name__)
        logger.debug("Invalid gRPC target: %s", target)
        return False


def flext_grpc_parse_target(target: str) -> tuple[str, int]:
    """Parse a validated gRPC target into (host, port).

    Raises ValueError if the target is invalid. Prefer checking with
    flext_grpc_validate_target() beforehand when you need a boolean.
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
    # Types
    "TGrpcTarget",
    "TGrpcTimeout",
    "flext_grpc_parse_target",
    # Helpers
    "flext_grpc_validate_target",
]
