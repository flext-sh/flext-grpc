from flext_core import FlextResult

from flext_grpc.config import FlextGrpcConfig as FlextGrpcConfig
from flext_grpc.entities import (
    FlextGrpcChannel as FlextGrpcChannel,
    FlextGrpcClient as FlextGrpcClient,
    FlextGrpcServer as FlextGrpcServer,
    FlextGrpcService as FlextGrpcServiceEntity,
    FlextGrpcStream as FlextGrpcStream,
)
from flext_grpc.typings import (
    TGrpcStreamType as TGrpcStreamType,
    TGrpcTarget as TGrpcTarget,
)

MIN_PORT: int
MAX_PORT: int
ADDRESS_PARTS_COUNT: int

def create_server(
    host: str = "localhost", port: int = 50051, max_workers: int = 10
) -> FlextGrpcServer: ...
def create_client(
    target: str, options: dict[str, object] | None = None
) -> FlextGrpcClient: ...
def create_channel(
    target: str, options: dict[str, object] | None = None
) -> FlextGrpcChannel: ...
def create_service(
    name: str, methods: list[str] | None = None
) -> FlextGrpcServiceEntity: ...
def create_stream(method_name: str, stream_type: str = "unary") -> FlextGrpcStream: ...
def create_config(
    host: str = "localhost",
    port: int = 50051,
    max_workers: int = 10,
    timeout: float = 30.0,
) -> FlextGrpcConfig: ...
def validate_address(address: str) -> FlextResult[bool]: ...
def parse_address(address: str) -> dict[str, int | str]: ...
def create_complete_setup(
    host: str = "localhost",
    port: int = 50051,
    service_name: str = "DefaultService",
    methods: list[str] | None = None,
) -> dict[str, FlextGrpcServer | FlextGrpcClient | FlextGrpcServiceEntity | str]: ...
