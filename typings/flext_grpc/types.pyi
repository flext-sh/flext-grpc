from typing import Protocol, TypedDict

from flext_grpc.typings import (
    TGrpcChannelState as TGrpcChannelState,
    TGrpcEntityId as TGrpcEntityId,
    TGrpcHost as TGrpcHost,
    TGrpcMethodName as TGrpcMethodName,
    TGrpcPort as TGrpcPort,
    TGrpcServerState as TGrpcServerState,
    TGrpcServiceName as TGrpcServiceName,
    TGrpcStreamType as TGrpcStreamType,
    TGrpcTarget as TGrpcTarget,
    TGrpcTimeout as TGrpcTimeout,
    flext_grpc_parse_target as flext_grpc_parse_target,
    flext_grpc_validate_target as flext_grpc_validate_target,
)

__all__ = [
    "FlextGrpcError",
    "FlextGrpcRequest",
    "FlextGrpcResponse",
    "FlextGrpcStatus",
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
    "flext_grpc_parse_target",
    "flext_grpc_validate_target",
]

class FlextGrpcError(Exception): ...

class FlextGrpcRequest(TypedDict, total=False):
    method: str
    payload: dict[str, object]

class FlextGrpcResponse(TypedDict, total=False):
    status: str
    data: dict[str, object] | None
    error: str | None

class FlextGrpcStatus(Protocol):
    code: int
    message: str
