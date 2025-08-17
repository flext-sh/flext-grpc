from flext_core import FlextEntity, FlextResult

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
    "FlextGrpcChannel",
    "FlextGrpcClient",
    "FlextGrpcEntity",
    "FlextGrpcServer",
    "FlextGrpcService",
    "FlextGrpcStream",
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
    "create_grpc_client",
    "create_grpc_server",
    "flext_grpc_parse_target",
    "flext_grpc_validate_target",
]

class FlextGrpcEntity(FlextEntity):
    @property
    def entity_type(self) -> str: ...

class FlextGrpcServer(FlextGrpcEntity):
    host: TGrpcHost
    port: TGrpcPort
    max_workers: int
    state: TGrpcServerState
    ssl_enabled: bool
    def validate_business_rules(self) -> FlextResult[None]: ...
    def start(self) -> FlextResult[FlextGrpcServer]: ...
    def mark_running(self) -> FlextResult[FlextGrpcServer]: ...
    def stop(self) -> FlextResult[FlextGrpcServer]: ...
    def mark_stopped(self) -> FlextResult[FlextGrpcServer]: ...

class FlextGrpcClient(FlextGrpcEntity):
    target: TGrpcTarget
    ssl_enabled: bool
    channel_state: TGrpcChannelState
    def validate_business_rules(self) -> FlextResult[None]: ...
    def connect(self) -> FlextResult[FlextGrpcClient]: ...
    def mark_ready(self) -> FlextResult[FlextGrpcClient]: ...
    def disconnect(self) -> FlextResult[FlextGrpcClient]: ...

class FlextGrpcChannel(FlextGrpcEntity):
    target: TGrpcTarget
    state: TGrpcChannelState
    def validate_business_rules(self) -> FlextResult[None]: ...

class FlextGrpcService(FlextGrpcEntity):
    name: TGrpcServiceName
    methods: list[TGrpcMethodName]
    def validate_business_rules(self) -> FlextResult[None]: ...

class FlextGrpcStream(FlextGrpcEntity):
    stream_type: TGrpcStreamType
    method_name: TGrpcMethodName
    def validate_business_rules(self) -> FlextResult[None]: ...

def create_grpc_server(
    server_id: str,
    host: str,
    port: int,
    max_workers: int = 10,
    *,
    ssl_enabled: bool = False,
) -> FlextResult[FlextGrpcServer]: ...
def create_grpc_client(
    client_id: str, target: str, *, ssl_enabled: bool = False
) -> FlextResult[FlextGrpcClient]: ...
