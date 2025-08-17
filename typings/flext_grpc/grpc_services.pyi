from flext_core import FlextContainer, FlextResult

from flext_grpc.entities import (
    FlextGrpcClient,
    FlextGrpcServer,
    FlextGrpcService,
    FlextGrpcStream,
)

__all__ = [
    "FlextGrpcClientService",
    "FlextGrpcPlatform",
    "FlextGrpcServerService",
    "FlextGrpcStreamService",
]

type TGrpcServerEntity = FlextGrpcServer
type TGrpcClientEntity = FlextGrpcClient
type TGrpcStreamEntity = FlextGrpcStream
type TGrpcServiceDef = FlextGrpcService
type TMethodCallResult = dict[str, object]

class FlextGrpcServerService:
    def execute(
        self, command: str, server: TGrpcServerEntity, *args: object, **kwargs: object
    ) -> FlextResult[TGrpcServerEntity | dict[str, object]]: ...

class FlextGrpcClientService:
    def execute(
        self, command: str, client: TGrpcClientEntity, *args: object, **kwargs: object
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]: ...

class FlextGrpcStreamService:
    def execute(
        self, command: str, stream: TGrpcStreamEntity, *args: object, **kwargs: object
    ) -> FlextResult[TGrpcStreamEntity | TMethodCallResult]: ...

class FlextGrpcPlatform:
    def __init__(self, container: FlextContainer | None = None) -> None: ...
    def start_server(
        self, server: TGrpcServerEntity
    ) -> FlextResult[TGrpcServerEntity | dict[str, object]]: ...
    def stop_server(
        self, server: TGrpcServerEntity
    ) -> FlextResult[TGrpcServerEntity | dict[str, object]]: ...
    def connect_client(
        self, client: TGrpcClientEntity
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]: ...
    def disconnect_client(
        self, client: TGrpcClientEntity
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]: ...
    def make_call(
        self, client: TGrpcClientEntity, method: str, request: object
    ) -> FlextResult[TGrpcClientEntity | TMethodCallResult | dict[str, object]]: ...
    def create_stream(
        self, stream: TGrpcStreamEntity
    ) -> FlextResult[TGrpcStreamEntity | TMethodCallResult]: ...
    def get_server_status(
        self, server: TGrpcServerEntity
    ) -> FlextResult[dict[str, object]]: ...
    def get_client_status(
        self, client: TGrpcClientEntity
    ) -> FlextResult[dict[str, object]]: ...
