"""Legacy shim: basic aliases for error/request/response/status types.

Historically this module re-exported symbols from a different location.
To satisfy type checking without depending on unfollowed imports, we
define minimal Protocol-based placeholders that downstream code can import.
"""

from __future__ import annotations

from typing import Protocol, TypedDict


class FlextGrpcError(Exception):
    """Base gRPC error type for FLEXT."""


class FlextGrpcRequest(TypedDict, total=False):
    """Represent a gRPC request payload."""

    method: str
    payload: dict[str, object]


class FlextGrpcResponse(TypedDict, total=False):
    """Represent a gRPC response payload."""

    status: str
    data: dict[str, object] | None
    error: str | None


class FlextGrpcStatus(Protocol):
    """Protocol describing minimal gRPC status fields."""

    code: int
    message: str


# Backward-compatibility re-exports expected by tests
from .typings import (  # noqa: E402
    TGrpcChannelState,
    TGrpcEntityId,
    TGrpcHost,
    TGrpcMethodName,
    TGrpcPort,
    TGrpcServerState,
    TGrpcServiceName,
    TGrpcStreamType,
    TGrpcTarget,
    TGrpcTimeout,
    flext_grpc_parse_target,
    flext_grpc_validate_target,
)

__all__: list[str] = [
    "FlextGrpcError",
    "FlextGrpcRequest",
    "FlextGrpcResponse",
    "FlextGrpcStatus",
    # types
    "TGrpcChannelState",
    "TGrpcEntityId",
    "TGrpcHost",
    "TGrpcMethodName",
    "TGrpcPort",
    "TGrpcServerState",
    "TGrpcServiceName",
    "TGrpcStreamType",
    "TGrpcTarget",
    "TGrpcTimeout",
    # helpers
    "flext_grpc_parse_target",
    "flext_grpc_validate_target",
]
