from typing import Protocol

from _typeshed import Incomplete

__all__ = [
    "TGrpcChannel",
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
    "flext_grpc_validate_target",
]

TGrpcTarget: Incomplete
TGrpcMethodName: Incomplete
TGrpcServiceName: Incomplete
TGrpcHost: Incomplete
TGrpcPort: Incomplete
TGrpcEntityId: Incomplete
TGrpcTimeout: Incomplete
TGrpcChannelState: Incomplete
TGrpcServerState: Incomplete
TGrpcStreamType: Incomplete

class TGrpcChannel(Protocol):
    def close(self) -> None: ...
    def unsubscribe(self, callback: object) -> None: ...

class TGrpcServer(Protocol):
    def add_generic_rpc_handlers(self, handlers: list[object]) -> None: ...
    def start(self) -> None: ...
    def stop(self, grace: float | None) -> None: ...

class TGrpcStub(Protocol):
    def __init__(self, channel: TGrpcChannel) -> None: ...

def flext_grpc_validate_target(target: str) -> bool: ...
def flext_grpc_parse_target(target: str) -> tuple[str, int]: ...
